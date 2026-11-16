"""Official archive definitions and book mappings for reconciliation."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

ARCHIVE_DIR = ROOT / "data" / "raw" / "_archives"
RAW_DIR = ROOT / "data" / "raw"
PROVENANCE_DIR = ROOT / "data" / "provenance"
REPORTS_DIR = ROOT / "reports" / "reconciliation"
DOCS_DIR = ROOT / "docs"

ARCHIVES = [
    {
        "edition": "rp2005",
        "name": "editions-rp2-preformatted.zip",
        "url": "https://www.dropbox.com/s/ago0uhvmjndbsy5/editions-rp2-preformatted.zip?dl=0",
        "format": "preformatted",
    },
    {
        "edition": "rp2005",
        "name": "editions-rp2-ascii.zip",
        "url": "https://www.dropbox.com/s/oil2m3la4vsnbpb/editions-rp2-ascii.zip?dl=0",
        "format": "ascii-one-line",
    },
    {
        "edition": "rp2005",
        "name": "editions-rp2-ccat.zip",
        "url": "https://www.dropbox.com/s/f3di0cgdflqjwq4/editions-rp2-ccat.zip?dl=0",
        "format": "ccat",
    },
    {
        "edition": "rp2018",
        "name": "rp2018-ascii.zip",
        "url": "https://www.dropbox.com/s/ug3i36zsvtg39x0/rp2018-ascii.zip?dl=0",
        "format": "preformatted",
    },
    {
        "edition": "rp2018",
        "name": "rp2018-ascii-one-line-per-verse.zip",
        "url": "https://www.dropbox.com/s/cr592513g0v2imc/rp2018-ascii-one-line-per-verse.zip?dl=0",
        "format": "ascii-one-line",
    },
    {
        "edition": "rp2018",
        "name": "rp2018-ccat.ZIP",
        "url": "https://www.dropbox.com/s/u47y6wedewv4mv9/rp2018-ccat.ZIP?dl=0",
        "format": "ccat",
    },
]

# Current book abbreviation -> official CCAT/ASCII file prefix.
ABBR_TO_OFFICIAL = {
    "MAT": "MT",
    "MAR": "MR",
    "LUK": "LU",
    "JOH": "JOH",
    "ACT": "AC",
    "ROM": "RO",
    "1CO": "1CO",
    "2CO": "2CO",
    "GAL": "GA",
    "EPH": "EPH",
    "PHP": "PHP",
    "COL": "COL",
    "1TH": "1TH",
    "2TH": "2TH",
    "1TI": "1TI",
    "2TI": "2TI",
    "TIT": "TIT",
    "PHM": "PHM",
    "HEB": "HEB",
    "JAM": "JAS",
    "1PE": "1PE",
    "2PE": "2PE",
    "1JO": "1JO",
    "2JO": "2JO",
    "3JO": "3JO",
    "JUD": "JUDE",
    "REV": "RE",
    "PA": "PA",
    "ACT24": "AC24",
}

OFFICIAL_TO_ABBR = {value: key for key, value in ABBR_TO_OFFICIAL.items()}

# The four verse references that are intentionally blank because they are not
# part of the Byzantine tradition (D7).
INTENTIONAL_BLANKS = {
    ("LUK", 17, 36),
    ("ACT", 8, 37),
    ("ACT", 15, 34),
    ("ACT", 24, 7),
}
