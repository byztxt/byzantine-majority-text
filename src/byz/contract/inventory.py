"""Hash, encoding, line-ending, and git metadata for every corpus file."""

import hashlib
import subprocess

from . import paths
from .encoding import decode, detect_encoding, detect_eol
from .model import FileRecord


def _specs():
    return [
        ("source/CCAT", paths.CCAT_DIR, "*.TXT", "ccat"),
        ("source/Strongs", paths.BP5_DIR, "*.BP5", "bp5"),
        (
            "csv-unicode/ccat/no-variants",
            paths.CSV_CCAT["ccat/no-variants"],
            "*.csv",
            "csv",
        ),
        (
            "csv-unicode/ccat/with-variants",
            paths.CSV_CCAT["ccat/with-variants"],
            "*.csv",
            "csv",
        ),
        (
            "csv-unicode/strongs/no-parsing",
            paths.CSV_STRONGS["strongs/no-parsing"],
            "*.csv",
            "csv",
        ),
        (
            "csv-unicode/strongs/with-parsing",
            paths.CSV_STRONGS["strongs/with-parsing"],
            "*.csv",
            "csv",
        ),
        ("tei-xml-unicode/no-accents", paths.TEI_DIR, "*.xml", "tei"),
        ("tei-xml-unicode/BYZ", paths.TEI_DIR / "BYZ", "*.xml", "tei-combined"),
        ("tei-xml-unicode/assets", paths.TEI_ASSETS, "*", "asset"),
        ("essay", paths.ESSAY_DIR, "*", "essay"),
        ("scripts", paths.SCRIPTS_DIR, "**/*", "script"),
    ]


def iter_specs(root=paths.ROOT):
    """Yield (dataset, path, format_class) for the corpus, deterministically."""
    for dataset, directory, pattern, format_class in _specs():
        directory = root / directory.relative_to(paths.ROOT)
        for path in sorted(directory.glob(pattern)):
            if not path.is_file():
                continue
            if "__pycache__" in path.parts or path.suffix in (".pyc", ".pyo"):
                continue
            if path.name in (".DS_Store",):
                continue
            yield dataset, path, format_class


DOC_FILES = [
    "README.md",
    "LICENSE",
    "source/README.md",
    "csv-unicode/README.md",
    "tei-xml-unicode/README.md",
    "essay/README.md",
    "scripts/README.md",
]


def iter_docs(root=paths.ROOT):
    for rel in DOC_FILES:
        path = root / rel
        if path.is_file():
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
    blobs = git_blob_hashes(root) if git else None
    records = []
    for dataset, path, format_class in list(iter_specs(root)) + list(iter_docs(root)):
        records.append(
            record_for(dataset, path, format_class, root=root, blobs=blobs, git=git)
        )
    return records
