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
        "note": (
            "The official `.CCT` archive is the accented source; the official "
            "ASCII archive supplies the unaccented text. Both archives contain "
            "LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 as **blank verse "
            "lines**, because those verses are not part of the Byzantine "
            "tradition. This edition therefore emits them as explicit empty "
            "records: the accented CSV has 7972 rows and the unaccented CSV "
            "7957, each with four empty rows, and both TEI views contain empty "
            "`<ab/>` elements for the four verses."
        ),
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
        "note": (
            "`textonly-beta-code`, `parsed`, the accented CSV (both views), the "
            "unaccented CSV, and the unaccented TEI are recovered byte-identically "
            "from git tag `v2.0.3`. The accented TEI (from the recovered accented "
            "CSV) and the Strong's views (from `parsed`) are generated here; "
            "`v2.0.3` itself has no accented TEI. The accented CSV (7968 rows), "
            "unaccented CSV (7953 rows), and unaccented TEI **omit** LUK 17:36, "
            "ACT 8:37, ACT 15:34, and ACT 24:7: the rows are absent and there is "
            "no empty `<ab/>`, even though the `textonly-beta-code` and `parsed` "
            "files in that tag do contain the blank verse lines. The generated "
            "accented TEI inherits that omission, while the generated Strong's "
            "views include the four verses as empty rows (7957 rows). The "
            "recovered artifacts must stay byte-identical, so the rows are "
            "deliberately not added back. The other three curated editions keep "
            "the verses as empty rows and empty `<ab/>` elements."
        ),
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
        "note": (
            "The official `.CCT` archive is the accented source; the official "
            "ASCII archive supplies the unaccented text. Both archives contain "
            "LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 as **blank verse "
            "lines**, because those verses are not part of the Byzantine "
            "tradition. This edition therefore emits them as explicit empty "
            "records: the accented CSV has 7972 rows and the unaccented CSV "
            "7957, each with four empty rows, and both TEI views contain empty "
            "`<ab/>` elements for the four verses."
        ),
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
        "note": (
            "The manifest separates the Greek-text commit (`source_commit`, from "
            "`source/CCAT`) from the Strong's/parsing commit (`strongs_commit`, "
            "from `source/Strongs`). LUK 17:36, ACT 8:37, ACT 15:34, and ACT "
            "24:7 are not part of the Byzantine tradition but are present in "
            "`source/CCAT`/`source/Strongs` as blank verse lines. This edition "
            "emits them as explicit empty records: 7972 accented CSV rows and "
            "7957 unaccented/Strong's CSV rows, each with four empty rows, and "
            "empty `<ab/>` elements in both TEI views."
        ),
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
    command = ["git", "-C", str(ROOT), "tag", "--list"]
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "cannot list git tags: "
            + " ".join(command)
            + f" exited {result.returncode}: {result.stderr.strip()}"
        )
    return sorted(
        (tag for tag in result.stdout.splitlines() if tag),
        key=_version_key,
    )


def release_range(edition: dict) -> tuple:
    prefixes = edition.get("release_prefixes") or []
    if not prefixes:
        # Official print editions have no repository release number.
        return "", ""
    matching = [tag for tag in tags() if any(tag.startswith(p) for p in prefixes)]
    if not matching:
        raise RuntimeError(
            f"released edition {edition['id']!r} has no git tags matching "
            f"{prefixes!r}; run `git tag --list` in {ROOT}"
        )
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
