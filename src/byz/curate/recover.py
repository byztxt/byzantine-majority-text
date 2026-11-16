"""Recover historical editions from git and freeze the current sources."""

import io
import shutil
import subprocess
import tarfile
from pathlib import Path

from byz.reconcile import sources

from . import editions

SOURCE_PREFIXES = [
    "textonly-beta-code/",
    "parsed/",
]
ARTIFACT_PREFIXES = [
    "csv-unicode/accents/no-variants/",
    "csv-unicode/accents/with-variants/",
    "csv-unicode/no-accents/",
    "tei-xml-unicode/no-accents/",
]


def _git_archive(tag: str, prefixes: list) -> dict:
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


def _write_files(dest: Path, files: dict) -> None:
    for relpath, data in files.items():
        path = dest / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def _copy_tree(src: Path, dest: Path) -> None:
    if not src.exists():
        raise SystemExit(f"missing source directory: {src}")
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def _fresh(edition_id: str) -> Path:
    path = editions.edition_dir(edition_id)
    if path.exists():
        shutil.rmtree(path)
    (path / "source").mkdir(parents=True)
    (path / "csv").mkdir()
    (path / "tei").mkdir()
    return path


def recover_historical(edition: dict) -> Path:
    dest = _fresh(edition["id"])
    files = _git_archive(
        edition["tag"], SOURCE_PREFIXES + ARTIFACT_PREFIXES
    )
    _write_files(
        dest / "source",
        {
            name: data
            for name, data in files.items()
            if any(name.startswith(prefix) for prefix in SOURCE_PREFIXES)
        },
    )
    # Keep the historical released artifacts as the edition's CSV/TEI.
    mapping = {
        "csv-unicode/accents/no-variants": "csv/accented/no-variants",
        "csv-unicode/accents/with-variants": "csv/accented/with-variants",
        "csv-unicode/no-accents": "csv/unaccented",
        "tei-xml-unicode/no-accents": "tei/unaccented",
    }
    for src_prefix, target in mapping.items():
        target_path = dest / target
        target_path.mkdir(parents=True, exist_ok=True)
        for name, data in files.items():
            if not name.startswith(src_prefix + "/"):
                continue
            rel = name[len(src_prefix) + 1 :]
            path = target_path / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    # Curated CSV/TEI filenames use the current book abbreviations.
    for sub in (
        "csv/accented/no-variants",
        "csv/accented/with-variants",
        "csv/unaccented",
        "tei/unaccented",
    ):
        for path in sorted((dest / sub).rglob("*")):
            if not path.is_file():
                continue
            abbr = sources.OFFICIAL_TO_ABBR.get(path.stem)
            if abbr and abbr != path.stem:
                path.rename(path.with_name(abbr + path.suffix))
    return dest


def recover_official(edition: dict) -> Path:
    dest = _fresh(edition["id"])
    # The official .CCT source is authoritative; the ASCII/preformatted archives
    # remain in data/raw and are referenced by the manifest/build step.
    _copy_tree(editions.ROOT / edition["source_dir"], dest / "source" / "ccat")
    return dest


def recover_current(edition: dict) -> Path:
    dest = _fresh(edition["id"])
    _copy_tree(editions.ROOT / "source" / "CCAT", dest / "source" / "CCAT")
    _copy_tree(editions.ROOT / "source" / "Strongs", dest / "source" / "Strongs")
    _copy_tree(
        editions.ROOT / "csv-unicode" / "ccat" / "no-variants",
        dest / "csv" / "accented" / "no-variants",
    )
    _copy_tree(
        editions.ROOT / "csv-unicode" / "ccat" / "with-variants",
        dest / "csv" / "accented" / "with-variants",
    )
    _copy_tree(
        editions.ROOT / "csv-unicode" / "strongs" / "with-parsing",
        dest / "csv" / "strongs" / "with-parsing",
    )
    _copy_tree(
        editions.ROOT / "csv-unicode" / "strongs" / "no-parsing",
        dest / "csv" / "strongs" / "no-parsing",
    )
    _copy_tree(
        editions.ROOT / "csv-unicode" / "strongs" / "no-parsing",
        dest / "csv" / "unaccented",
    )
    _copy_tree(
        editions.ROOT / "tei-xml-unicode" / "no-accents",
        dest / "tei" / "unaccented",
    )
    return dest


def recover_all() -> list:
    recovered = []
    for edition_id, edition in editions.EDITIONS.items():
        if edition["source_kind"] == "historical":
            recovered.append(recover_historical(edition))
        elif edition["source_kind"] == "official":
            recovered.append(recover_official(edition))
        elif edition["source_kind"] == "current":
            recovered.append(recover_current(edition))
        else:
            raise SystemExit(f"unknown source kind for {edition_id}")
    return recovered
