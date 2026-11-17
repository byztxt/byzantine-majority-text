"""Recover historical editions from git and freeze the current sources."""

import io
import os
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


def _staging(edition_id: str) -> tuple:
    """Create a sibling staging tree; return (staging, final) paths.

    Nothing is deleted from the committed edition until the new tree has been
    fully recovered and validated, so a failed `git archive` or a missing source
    directory leaves the existing edition untouched.
    """
    final = editions.edition_dir(edition_id)
    staging = final.parent / f".{edition_id}.staging"
    if staging.exists():
        shutil.rmtree(staging)
    (staging / "source").mkdir(parents=True)
    (staging / "csv").mkdir()
    (staging / "tei").mkdir()
    return staging, final


def _swap(staging: Path, final: Path) -> Path:
    retired = final.parent / f".{final.name}.old"
    if retired.exists():
        shutil.rmtree(retired)
    if final.exists():
        final.rename(retired)
    os.replace(staging, final)
    if retired.exists():
        shutil.rmtree(retired)
    return final


def _recover(edition_id: str, populate) -> Path:
    staging, final = _staging(edition_id)
    try:
        populate(staging)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return _swap(staging, final)


def recover_historical(edition: dict) -> Path:
    def populate(dest: Path) -> None:
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

    return _recover(edition["id"], populate)


def recover_official(edition: dict) -> Path:
    def populate(dest: Path) -> None:
        # The official .CCT source is authoritative; the ASCII/preformatted
        # archives remain in data/raw and are referenced by the manifest/build
        # step.
        _copy_tree(
            editions.ROOT / edition["source_dir"], dest / "source" / "ccat"
        )

    return _recover(edition["id"], populate)


def recover_current(edition: dict) -> Path:
    def populate(dest: Path) -> None:
        _copy_tree(editions.ROOT / "source" / "CCAT", dest / "source" / "CCAT")
        _copy_tree(
            editions.ROOT / "source" / "Strongs", dest / "source" / "Strongs"
        )
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

    return _recover(edition["id"], populate)


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
