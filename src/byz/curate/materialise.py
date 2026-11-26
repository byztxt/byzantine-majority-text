"""Materialise the historical 2005-2019 inputs into `data/`.

The `rp2005-2019` edition's two source prefixes live in git tag `v2.0.3`, not in
the working tree. This module extracts them once into `data/raw/repo/rp2005-2019/`
and writes `data/provenance/rp2005-2019.toml`, so every input a build reads is
under `data/`.

The tag's released CSV/TEI artifacts are not inputs and are not materialised:
`byz.build` regenerates every view from the 57 source files with the current
pipeline, so the released artifacts are evidence of what the 2019 converter
produced, not what this repository publishes.
"""

import hashlib
import io
import json
import subprocess
import tarfile
from pathlib import Path

from byz import generated

from . import editions
from .files import sha256_file

HISTORICAL_TAG = editions.EDITIONS["rp2005-2019"]["tag"]
HISTORICAL_COMMIT = editions.EDITIONS["rp2005-2019"]["commit"]

# (tag prefix, data path under data/raw/repo/rp2005-2019/, expected file count).
# Both prefixes keep the tag's names. The tag's released-artifact prefixes are
# deliberately absent: they are not inputs, and `byz.build` regenerates every
# view from these 57 source files with the current pipeline.
PREFIX_MAP = (
    ("textonly-beta-code/", "textonly-beta-code/", 30),
    ("parsed/", "parsed/", 27),
)

HISTORICAL_INPUT_ROOT = "data/raw/repo/rp2005-2019"
HISTORICAL_PROVENANCE = "data/provenance/rp2005-2019.toml"

# Files the build writes next to the materialised sources. They are outputs,
# not tag content, so a re-run must leave them alone rather than refusing the
# tree as unexpected.
GENERATED_NEIGHBOURS = ("README.md",)


def sha256_file_bytes(data: bytes) -> str:
    """Return the SHA-256 of an in-memory byte string."""
    return hashlib.sha256(data).hexdigest()


def _git_archive(tag: str, prefixes: list) -> dict:
    """Return `{name: bytes}` for every file under `prefixes` in `tag`."""
    result = subprocess.run(
        ["git", "-C", str(editions.ROOT), "archive", tag],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"git archive failed for {tag}: {result.stderr!r}")
    files = {}
    with tarfile.open(fileobj=io.BytesIO(result.stdout), mode="r:") as archive:
        for member in archive.getmembers():
            if not member.isfile():
                continue
            if not any(member.name.startswith(prefix) for prefix in prefixes):
                continue
            extracted = archive.extractfile(member)
            if extracted is not None:
                files[member.name] = extracted.read()
    return files


def _data_path(tag_name: str) -> str:
    """Map one tag path to its path under `data/raw/repo/rp2005-2019/`."""
    for tag_prefix, data_prefix, _ in PREFIX_MAP:
        if tag_name.startswith(tag_prefix):
            return data_prefix + tag_name[len(tag_prefix) :]
    raise SystemExit(f"unmapped v2.0.3 path: {tag_name}")


def _expected_files() -> dict:
    """Return `{data-relative path: bytes}` for the 57 historical source files."""
    files = _git_archive(
        HISTORICAL_TAG, [tag_prefix for tag_prefix, _, _ in PREFIX_MAP]
    )
    for tag_prefix, _, expected_count in PREFIX_MAP:
        actual_count = sum(
            1 for name in files if name.startswith(tag_prefix)
        )
        if actual_count != expected_count:
            raise SystemExit(
                f"{HISTORICAL_TAG}:{tag_prefix} has {actual_count} files, "
                f"expected {expected_count}"
            )
    mapped = {_data_path(name): data for name, data in files.items()}
    if len(mapped) != sum(count for _, _, count in PREFIX_MAP):
        raise SystemExit(
            f"{HISTORICAL_TAG}: expected "
            f"{sum(count for _, _, count in PREFIX_MAP)} files, "
            f"mapped {len(mapped)}"
        )
    return mapped


def _provenance_text(files: dict) -> str:
    """Render the deterministic provenance TOML for the materialised tree."""
    lines = list(generated.toml_header())
    lines.extend(
        [
            "",
            'edition = "rp2005-2019"',
            f'tag = "{HISTORICAL_TAG}"',
            f'commit = "{HISTORICAL_COMMIT}"',
            f'method = "git archive {HISTORICAL_TAG}"',
            f'extracted = "{HISTORICAL_INPUT_ROOT}"',
            'generated_by = "PYTHONPATH=src python3 -m byz.materialise"',
        ]
    )
    for _, data_prefix, _ in sorted(PREFIX_MAP, key=lambda row: row[1]):
        count = sum(1 for path in files if path.startswith(data_prefix))
        lines.extend(
            [
                "",
                "[[prefixes]]",
                f"path = {json.dumps(data_prefix)}",
                f"files = {count}",
            ]
        )
    for path in sorted(files):
        size = len(files[path])
        lines.extend(
            [
                "",
                "[[files]]",
                f"path = {json.dumps(path)}",
                f'sha256 = "{sha256_file_bytes(files[path])}"',
                f"size = {size}",
            ]
        )
    return "\n".join(lines) + "\n"


def materialise_historical(dest_root: Path | None = None) -> Path:
    """Write the historical source tree and provenance under `dest_root`.

    The whole destination is validated before anything is written: an existing
    file with different bytes, or a stray extra file, is a loud failure instead
    of a silent overwrite or deletion. A second run on an intact tree writes
    nothing and returns the same destination.
    """
    root = Path(dest_root) if dest_root is not None else editions.ROOT
    files = _expected_files()
    destination = root / HISTORICAL_INPUT_ROOT

    existing = set()
    if destination.exists():
        existing = {
            path.relative_to(destination).as_posix()
            for path in destination.rglob("*")
            if path.is_file()
            and path.relative_to(destination).as_posix()
            not in GENERATED_NEIGHBOURS
        }
    unexpected = sorted(existing - set(files))
    if unexpected:
        raise SystemExit(
            f"{HISTORICAL_INPUT_ROOT}: unexpected file(s): "
            + ", ".join(unexpected)
        )
    for relpath in sorted(existing):
        actual = (destination / relpath).read_bytes()
        expected = files[relpath]
        if actual != expected:
            raise SystemExit(
                f"{relpath}: existing bytes differ from {HISTORICAL_TAG} "
                f"(sha256 {sha256_file(destination / relpath)}, "
                f"expected {sha256_file_bytes(expected)})"
            )

    for relpath in sorted(set(files) - existing):
        path = destination / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(files[relpath])

    provenance = root / HISTORICAL_PROVENANCE
    text = _provenance_text(files)
    if not provenance.is_file() or provenance.read_text(encoding="utf-8") != text:
        provenance.parent.mkdir(parents=True, exist_ok=True)
        provenance.write_text(text, encoding="utf-8")
    return destination
