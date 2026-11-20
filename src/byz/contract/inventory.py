"""Hash, encoding, line-ending, and git metadata for every corpus file."""

import hashlib
import os
import subprocess

from . import paths
from .encoding import decode, detect_encoding, detect_eol
from .model import FileRecord


def _specs():
    return [
        ("source/CCAT", paths.CCAT_DIR, "*.TXT", "ccat"),
        ("source/Strongs", paths.BP5_DIR, "*.BP5", "bp5"),
        (
            paths.dataset_name("csv/accented/no-variants"),
            paths.CSV_CCAT["csv/accented/no-variants"],
            "*.csv",
            "csv",
        ),
        (
            paths.dataset_name("csv/accented/with-variants"),
            paths.CSV_CCAT["csv/accented/with-variants"],
            "*.csv",
            "csv",
        ),
        (
            paths.dataset_name("csv/strongs/no-parsing"),
            paths.CSV_STRONGS["csv/strongs/no-parsing"],
            "*.csv",
            "csv",
        ),
        (
            paths.dataset_name("csv/strongs/with-parsing"),
            paths.CSV_STRONGS["csv/strongs/with-parsing"],
            "*.csv",
            "csv",
        ),
        (paths.TEI_DATASET, paths.TEI_DIR, "*.xml", "tei"),
        (paths.TEI_BYZ_DATASET, paths.TEI_DIR / "BYZ", "*.xml", "tei-combined"),
        (paths.ASSETS_DATASET, paths.ASSETS_DIR, "*", "asset"),
        ("essay", paths.ESSAY_DIR, "*", "essay"),
        ("scripts", paths.SCRIPTS_DIR, "**/*", "script"),
    ]


def tracked_paths(root=paths.ROOT):
    """Return the repository-relative paths git tracks below `root`.

    The contract describes the committed corpus, never a contributor's working
    tree. A stray local file (an editor backup, a downloaded draft, an untracked
    essay export) must not change `reports/baseline/files.csv`, or the committed
    report would disagree with a clean checkout and the determinism tests would
    fail. Filtering on `git ls-files` is the single source of that truth.

    This function requires a git checkout and a `git` binary on `PATH`; callers
    fail with a `RuntimeError` (never a bare `FileNotFoundError`) when it is
    absent.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            capture_output=True,
            check=False,
        )
    except OSError as error:
        raise RuntimeError(
            f"cannot run git to list tracked files under {root}: {error}"
        ) from error
    if result.returncode != 0:
        raise RuntimeError(
            f"cannot list tracked files under {root}: "
            f"{result.stderr.decode('utf-8', errors='replace').strip()}"
        )
    # Git separates names with NUL and reports them as repo-relative bytes;
    # surrogateescape matches how `pathlib` decodes the filesystem.
    return {
        os.fsdecode(name)
        for name in result.stdout.split(b"\0")
        if name
    }


def iter_specs(root=paths.ROOT, tracked=None):
    """Yield (dataset, path, format_class) for tracked corpus files.

    `tracked` may be supplied to avoid a second `git ls-files` call; otherwise
    it is computed from `root`.
    """
    if tracked is None:
        tracked = tracked_paths(root)
    for dataset, directory, pattern, format_class in _specs():
        directory = root / directory.relative_to(paths.ROOT)
        for path in sorted(directory.glob(pattern)):
            if not path.is_file():
                continue
            if "__pycache__" in path.parts or path.suffix in (".pyc", ".pyo"):
                continue
            if path.name in (".DS_Store",):
                continue
            try:
                relpath = path.relative_to(root).as_posix()
            except ValueError:
                continue
            if relpath not in tracked:
                # Untracked local file: not part of the committed corpus.
                continue
            yield dataset, path, format_class


DOC_FILES = [
    "README.md",
    "LICENSE",
    "source/README.md",
    "essay/README.md",
    "scripts/README.md",
]


def iter_docs(root=paths.ROOT, tracked=None):
    """Yield (dataset, path, format_class) for tracked documentation files.

    `tracked` may be supplied to avoid a second `git ls-files` call; otherwise
    it is computed from `root`. Like `iter_specs`, this never yields an
    untracked local file.
    """
    if tracked is None:
        tracked = tracked_paths(root)
    for rel in DOC_FILES:
        path = root / rel
        if not path.is_file():
            continue
        try:
            relpath = path.relative_to(root).as_posix()
        except ValueError:
            continue
        if relpath not in tracked:
            continue
        yield "docs", path, "doc"


def count_lines(text: str) -> int:
    return len(text.splitlines())


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_hashes(root=paths.ROOT) -> dict:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-s"],
        capture_output=True,
        text=True,
        check=False,
    )
    mapping = {}
    for line in result.stdout.splitlines():
        meta, _, relpath = line.partition("\t")
        parts = meta.split()
        if len(parts) >= 2:
            mapping[relpath] = parts[1]
    return mapping


def last_commit(root, relpath: str) -> str:
    result = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "log",
            "-1",
            "--format=%h|%cs",
            "--",
            relpath,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


def record_for(dataset, path, format_class, root=paths.ROOT, blobs=None, git=True):
    data = path.read_bytes()
    encoding = detect_encoding(data)
    text = decode(data, encoding)
    try:
        relpath = str(path.relative_to(root))
    except ValueError:
        relpath = str(path)
    blob = ""
    commit = ""
    if git:
        if blobs is None:
            blobs = git_blob_hashes(root)
        blob = blobs.get(relpath, "")
        commit = last_commit(root, relpath)
    return FileRecord(
        dataset=dataset,
        path=relpath,
        size=len(data),
        sha256=_sha256(data),
        lines=count_lines(text),
        encoding=encoding,
        eol=detect_eol(data),
        format_class=format_class,
        git_blob=blob,
        last_commit=commit,
    )


def inventory(root=paths.ROOT, git=True):
    """Return the inventory of the committed corpus.

    `git=False` skips per-file blob hash and last-commit metadata, but git is
    still required: the inventory only describes tracked files, so it always
    calls `tracked_paths(root)` (which raises a clear `RuntimeError` when git
    is unavailable).
    """
    blobs = git_blob_hashes(root) if git else None
    tracked = tracked_paths(root)
    records = []
    for dataset, path, format_class in list(
        iter_specs(root, tracked=tracked)
    ) + list(iter_docs(root, tracked=tracked)):
        records.append(
            record_for(dataset, path, format_class, root=root, blobs=blobs, git=git)
        )
    return records
