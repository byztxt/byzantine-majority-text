"""Edition registry, release ranges, and curated paths."""

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EDITIONS_DIR = ROOT / "editions"
DIFFS_DIR = ROOT / "reports" / "diffs"
DOCS_DIR = ROOT / "docs"
DATA_RAW = ROOT / "data" / "raw"
PROVENANCE_DIR = ROOT / "data" / "provenance"

EDITIONS = {
    "rp2005": {
        "id": "rp2005",
        "title": "Robinson-Pierpont 2005, official print edition",
        "status": "official",
        "basis": "Published in print by Chilton Book Publishing, Southborough, Massachusetts",
        "release_prefixes": [],
        "source_kind": "official",
        "source_dir": "data/raw/rp2005/editions-rp2-ccat",
        "ascii_dir": "data/raw/rp2005/editions-rp2-ascii",
        "preformatted_dir": "data/raw/rp2005/editions-rp2-preformatted",
        "pdf": "data/raw/rp2005/official-pdf/editions-rp2.pdf",
        "pdf_url": "https://byzantinetext.com/wp-content/uploads/2016/11/editions-rp2.pdf",
    },
    "rp2005-2019": {
        "id": "rp2005-2019",
        "title": "Robinson-Pierpont 2005 lineage, 2019 repo revision",
        "status": "released",
        "basis": "Recovered from git tag v2.0.3 (textonly-beta-code + parsed)",
        "release_prefixes": ["v1.", "v2."],
        "source_kind": "historical",
        "tag": "v2.0.3",
        "pdf": "",
        "pdf_url": "",
    },
    "rp2018": {
        "id": "rp2018",
        "title": "Robinson-Pierpont 2018, official print edition",
        "status": "official",
        "basis": "Published in print by VTR, Nuremberg",
        "release_prefixes": [],
        "source_kind": "official",
        "source_dir": "data/raw/rp2018/rp2018-ccat",
        "ascii_dir": "data/raw/rp2018/rp2018-ascii-one-line-per-verse",
        "preformatted_dir": "data/raw/rp2018/rp2018-ascii",
        "pdf": "data/raw/rp2018/official-pdf/robinson-pierpont-2018-gnt-edition.pdf",
        "pdf_url": "https://byzantinetext.com/wp-content/uploads/2021/03/robinson-pierpont-2018-gnt-edition.pdf",
    },
    "rp2018-2023": {
        "id": "rp2018-2023",
        "title": "Robinson-Pierpont 2018 with 2023 adjustments (repo release)",
        "status": "released",
        "basis": "Current maintained source; 2018 edition plus 2023 adjustments",
        "release_prefixes": ["v3."],
        "source_kind": "current",
        "pdf": "",
        "pdf_url": "",
    },
}

BOOK_NAMES = {
    "MAT": "Matthew",
    "MAR": "Mark",
    "LUK": "Luke",
    "JOH": "John",
    "ACT": "Acts",
    "ROM": "Romans",
    "1CO": "First Corinthians",
    "2CO": "Second Corinthians",
    "GAL": "Galatians",
    "EPH": "Ephesians",
    "PHP": "Philippians",
    "COL": "Colossians",
    "1TH": "First Thessalonians",
    "2TH": "Second Thessalonians",
    "1TI": "First Timothy",
    "2TI": "Second Timothy",
    "TIT": "Titus",
    "PHM": "Philemon",
    "HEB": "Hebrews",
    "JAM": "James",
    "1PE": "First Peter",
    "2PE": "Second Peter",
    "1JO": "First John",
    "2JO": "Second John",
    "3JO": "Third John",
    "JUD": "Jude",
    "REV": "Revelation",
}

BOOK_ORDER = list(BOOK_NAMES)


def _version_key(tag: str):
    return tuple(int(part) for part in re.findall(r"\d+", tag))


def tags() -> list:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "tag", "--list"],
        capture_output=True,
        text=True,
        check=False,
    )
    return sorted(
        (tag for tag in result.stdout.splitlines() if tag),
        key=_version_key,
    )


def release_range(edition: dict) -> tuple:
    prefixes = edition.get("release_prefixes") or []
    if not prefixes:
        return "", ""
    matching = [tag for tag in tags() if any(tag.startswith(p) for p in prefixes)]
    if not matching:
        return "", ""
    return matching[0], matching[-1]


def edition_dir(edition_id: str) -> Path:
    return EDITIONS_DIR / edition_id


def metadata(edition_id: str) -> dict:
    edition = dict(EDITIONS[edition_id])
    first, last = release_range(edition)
    edition["first_release"] = first
    edition["latest_release"] = last
    edition["release_range"] = f"{first}-{last}" if first else ""
    return edition
