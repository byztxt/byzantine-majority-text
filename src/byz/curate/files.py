"""Shared file hashing and glob helpers for the curation pipeline.

Build and verify must agree on exactly which files a manifest pins, so both
import the helpers here instead of duplicating the hash loop or the glob
expansion.
"""

import fnmatch
import hashlib
import subprocess
from pathlib import Path

from . import editions


def sha256_file(path: Path) -> str:
    """Return the SHA-256 of `path`, streamed so large files stay cheap."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def matching_files(root: Path, includes) -> dict:
    """Return `{relative POSIX path: Path}` for files matching `includes`.

    Every pattern is resolved against `root`; directories and duplicate
    matches are dropped, and the result is keyed by the path relative to
    `root` so the caller can compare it directly with a manifest file list.
    """
    matched = {}
    for include in includes:
        for path in root.glob(include):
            if path.is_file():
                matched[path.relative_to(root).as_posix()] = path
    return matched


def tracked_count(relative_dir: str, pattern: str = "*") -> int:
    """Return the number of tracked files under `relative_dir`.

    Used only for input folders that a manifest does not pin (the official
    `preformatted/` and `official-pdf/` trees). Counting `git ls-files` rather
    than globbing the directory means an untracked download cannot change a
    generated count. `pattern` is matched against the basename, so
    ``tracked_count("data/raw/print/rp2005/preformatted", "*.ASC")`` counts
    only the committed `.ASC` files.
    """
    # `-C` pins the repository root, so the count is the same no matter which
    # directory the caller ran `byz.build` from. This mirrors
    # `contract.inventory.tracked_paths`.
    command = [
        "git",
        "-C",
        str(editions.ROOT),
        "ls-files",
        "-z",
        "--",
        relative_dir,
    ]
    result = subprocess.run(
        command,
        capture_output=True,
        check=False,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "cannot list tracked files: "
            + " ".join(command)
            + f" exited {result.returncode}: {result.stderr.strip()}"
        )
    names = [name for name in result.stdout.split("\0") if name]
    return sum(
        1
        for name in names
        if fnmatch.fnmatchcase(Path(name).name, pattern)
    )
