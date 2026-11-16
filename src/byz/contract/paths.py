"""Repository paths and canonical book identifiers for the baseline contract."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

SOURCE = ROOT / "source"
CCAT_DIR = SOURCE / "CCAT"
BP5_DIR = SOURCE / "Strongs"

CSV_DIR = ROOT / "csv-unicode"
CSV_CCAT = {
    "ccat/no-variants": CSV_DIR / "ccat" / "no-variants",
    "ccat/with-variants": CSV_DIR / "ccat" / "with-variants",
}
CSV_STRONGS = {
    "strongs/no-parsing": CSV_DIR / "strongs" / "no-parsing",
    "strongs/with-parsing": CSV_DIR / "strongs" / "with-parsing",
}

TEI_DIR = ROOT / "tei-xml-unicode" / "no-accents"
TEI_BYZ = TEI_DIR / "BYZ" / "byz.xml"
TEI_ASSETS = ROOT / "tei-xml-unicode" / "assets"
ESSAY_DIR = ROOT / "essay"
SCRIPTS_DIR = ROOT / "scripts"

REPORTS_DIR = ROOT / "reports" / "baseline"
DOCS_DIR = ROOT / "docs"
CONTRACT_DIR = DOCS_DIR / "contract"

# Number -> abbreviation used by the converters (scripts/csv_converter.py).
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

# Evidence for the derivation map, tied to the scripts that implement it.
DERIVATION_EVIDENCE = {
    "ccat": (
        "scripts/csv_converter.py: path_ccat_no_variants / "
        "path_ccat_with_variants, convert_book(drop_variants=...)"
    ),
    "strongs": (
        "scripts/csv_converter.py: path_strongs_with_parsing / "
        "path_strongs_no_parsing, convert_book(drop_parsing=...)"
    ),
    "tei": (
        "scripts/tei_xml_converter.py: path_no_accents_csv = "
        "'../csv-unicode/strongs/no-parsing'; convert_byz()/convert_book()"
    ),
}
