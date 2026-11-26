"""Archive member inventory and loading."""

import hashlib
import zipfile
from pathlib import Path

from byz.contract.encoding import detect_encoding, detect_eol

from . import sources


def _format_class(name: str) -> str:
    lower = name.lower()
    if lower == "greek.cct":
        return "doc"
    if lower.endswith(".cct"):
        return "ccat"
    if lower.endswith("_byz.txt"):
        return "ascii-one-line"
    if lower.endswith(".asc"):
        return "preformatted"
    if lower.endswith(".txt"):
        return "text"
    return "other"


def load_members(archive_path: Path) -> dict:
    members = {}
    with zipfile.ZipFile(archive_path) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            members[info.filename] = archive.read(info.filename)
    return members


def inventory_member(name: str, data: bytes) -> dict:
    encoding = detect_encoding(data)
    return {
        "member": name,
        "size": len(data),
        "crc": "",
        "sha256": hashlib.sha256(data).hexdigest(),
        "encoding": encoding,
        "eol": detect_eol(data),
        "format": _format_class(name),
    }


def inventory_archive(archive_path: Path, edition: str, name: str) -> list:
    records = []
    with zipfile.ZipFile(archive_path) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            data = archive.read(info.filename)
            record = inventory_member(info.filename, data)
            record.update(
                {
                    "edition": edition,
                    "archive": name,
                    "crc": f"{info.CRC:08x}",
                }
            )
            records.append(record)
    records.sort(key=lambda row: row["member"])
    return records


def inventory_all() -> list:
    rows = []
    for spec in sources.ARCHIVES:
        path = sources.ARCHIVE_DIR / spec["edition"] / spec["name"]
        if not path.exists():
            continue
        rows.extend(inventory_archive(path, spec["edition"], spec["name"]))
    return rows
