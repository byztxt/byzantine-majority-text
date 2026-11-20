"""Repository paths and canonical book identifiers for the baseline contract."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

SOURCE = ROOT / "source"
CCAT_DIR = SOURCE / "CCAT"
BP5_DIR = SOURCE / "Strongs"

# The current text has one home: its curated edition. Every current-text path
# and dataset name derives from this pair, so a path and a report label cannot
# drift apart.
CURRENT_EDITION = "rp2018-2023"
CURRENT_PREFIX = f"editions/{CURRENT_EDITION}"
CURRENT_DIR = ROOT / "editions" / CURRENT_EDITION

CSV_DIR = CURRENT_DIR / "csv"
CSV_CCAT = {
    "csv/accented/no-variants": CSV_DIR / "accented" / "no-variants",
    "csv/accented/with-variants": CSV_DIR / "accented" / "with-variants",
}
CSV_STRONGS = {
    "csv/strongs/no-parsing": CSV_DIR / "strongs" / "no-parsing",
    "csv/strongs/with-parsing": CSV_DIR / "strongs" / "with-parsing",
}

TEI_DIR = CURRENT_DIR / "tei" / "unaccented"
TEI_BYZ = TEI_DIR / "BYZ" / "byz.xml"
TEI_DATASET = f"{CURRENT_PREFIX}/tei/unaccented"
TEI_BYZ_DATASET = f"{TEI_DATASET}/BYZ"
ASSETS_DIR = ROOT / "docs" / "assets"
ASSETS_DATASET = "docs/assets"
ESSAY_DIR = ROOT / "essay"
SCRIPTS_DIR = ROOT / "scripts"


def dataset_name(key: str) -> str:
    """Repository-relative dataset name for a CSV view key."""
    return f"{CURRENT_PREFIX}/{key}"


REPORTS_DIR = ROOT / "reports" / "baseline"
DOCS_DIR = ROOT / "docs"
CONTRACT_DIR = DOCS_DIR / "contract"

# Number -> abbreviation used by the build (`src/byz/curate/build.py`).
BOOK_NUM_TO_ABBR = {
    "01": "MAT",
    "02": "MAR",
    "03": "LUK",
    "04": "JOH",
    "05": "ACT",
    "06": "ROM",
    "07": "1CO",
    "08": "2CO",
    "09": "GAL",
    "10": "EPH",
    "11": "PHP",
    "12": "COL",
    "13": "1TH",
    "14": "2TH",
    "15": "1TI",
    "16": "2TI",
    "17": "TIT",
    "18": "PHM",
    "19": "HEB",
    "20": "JAM",
    "21": "1PE",
    "22": "2PE",
    "23": "1JO",
    "24": "2JO",
    "25": "3JO",
    "26": "JUD",
    "27": "REV",
}

# The `a` section files are Byzantine variant sections, not separate books.
SECTION_NUM_TO_ABBR = {
    "04a": "PA",
    "05a": "ACT24",
}

NUM_TO_ABBR = {**BOOK_NUM_TO_ABBR, **SECTION_NUM_TO_ABBR}
ABBR_TO_NUM = {abbr: num for num, abbr in NUM_TO_ABBR.items()}
ABBR_TO_BOOK_ID = {abbr: f"B{num}" for num, abbr in BOOK_NUM_TO_ABBR.items()}
BOOK_ID_TO_ABBR = {book_id: abbr for abbr, book_id in ABBR_TO_BOOK_ID.items()}

CANONICAL_BOOKS = list(BOOK_NUM_TO_ABBR.values())
SECTION_ABBRS = list(SECTION_NUM_TO_ABBR.values())

VARIANT_CODES = frozenset("NBCMSE")

# Evidence for the derivation map, tied to the build functions that write each
# view.
DERIVATION_EVIDENCE = {
    "ccat": (
        "src/byz/curate/build.py: build_all -> recover.recover_all copies "
        "source/CCAT into the editions/rp2018-2023/source snapshot, then "
        "build_current -> parse_cct_current(drop_variants=...) -> write_csv"
    ),
    "strongs": (
        "src/byz/curate/build.py: build_all -> recover.recover_all copies "
        "source/Strongs into the editions/rp2018-2023/source snapshot, then "
        "build_current -> parse_bp5_strongs -> write_csv"
    ),
    "tei": (
        "src/byz/curate/build.py: build_current -> write_tei() "
        "from csv/strongs/no-parsing"
    ),
}
