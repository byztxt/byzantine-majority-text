"""Official archive definitions and book mappings for reconciliation."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

ARCHIVE_DIR = ROOT / "data" / "raw" / "_archives"
RAW_DIR = ROOT / "data" / "raw"
PROVENANCE_DIR = ROOT / "data" / "provenance"
REPORTS_DIR = ROOT / "reports" / "reconciliation"
DOCS_DIR = ROOT / "docs"

# The Byzantine Text editions listing page from which the six archives were
# retrieved in November 2026. Recorded per archive as `source_page` and used
# for the generated prose in `docs/PROVENANCE.md`.
SOURCE_PAGE = "https://byzantinetext.com/study/editions/robinson-pierpont/"

# The pinned SHA-256 of each official archive. These values also appear in
# `data/provenance/*.toml`; `fetch.run()` refuses to record or extract an
# archive whose digest does not match. The archives themselves are committed
# under `data/raw/_archives/`, so the offline reconciliation tests can hash the
# real files without any network access.
ARCHIVES = [
    {
        "edition": "rp2005",
        "name": "editions-rp2-preformatted.zip",
        "url": "https://www.dropbox.com/s/ago0uhvmjndbsy5/editions-rp2-preformatted.zip?dl=0",
        "format": "preformatted",
        "sha256": "e8719d9eafa4239fb5131e80cc1b5584915ad2efd37aac2783fcc484e438f3a3",
    },
    {
        "edition": "rp2005",
        "name": "editions-rp2-ascii.zip",
        "url": "https://www.dropbox.com/s/oil2m3la4vsnbpb/editions-rp2-ascii.zip?dl=0",
        "format": "ascii-one-line",
        "sha256": "c85ccdcbccee55fbb0ca7744352330806f505514b28a6ae02302843f65a86a2a",
    },
    {
        "edition": "rp2005",
        "name": "editions-rp2-ccat.zip",
        "url": "https://www.dropbox.com/s/f3di0cgdflqjwq4/editions-rp2-ccat.zip?dl=0",
        "format": "ccat",
        "sha256": "d172e27a6adf77459cb08c2dc67a57b69239bb27605791c3d1cfaadcda97e2e2",
    },
    {
        "edition": "rp2018",
        "name": "rp2018-ascii.zip",
        "url": "https://www.dropbox.com/s/ug3i36zsvtg39x0/rp2018-ascii.zip?dl=0",
        "format": "preformatted",
        "sha256": "cd8634562b6c8ae77fb04c2045e306fb7bd3a1870944bb569926d6d94dc3991c",
    },
    {
        "edition": "rp2018",
        "name": "rp2018-ascii-one-line-per-verse.zip",
        "url": "https://www.dropbox.com/s/cr592513g0v2imc/rp2018-ascii-one-line-per-verse.zip?dl=0",
        "format": "ascii-one-line",
        "sha256": "5ea075d9d52d85511ce627be258fcc78e901d08e8a912dda96dffe977add7fb6",
    },
    {
        "edition": "rp2018",
        "name": "rp2018-ccat.ZIP",
        "url": "https://www.dropbox.com/s/u47y6wedewv4mv9/rp2018-ccat.ZIP?dl=0",
        "format": "ccat",
        "sha256": "55eae8ffc5679fc740318e7b520b283393ca09c66b7a6c1934336d54eca3a394",
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
