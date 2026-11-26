"""Machine-readable contracts consumed by the validators and written to docs/."""

from . import paths

VARIANT_CODES = list("NBCMSE")

# Verses that are intentionally blank because they are not part of the
# Byzantine tradition (maintainer decision D7). Generated CSV/TEI keep them as
# explicit empty records (D8).
INTENTIONAL_BLANK_VERSES = frozenset(
    {
        ("LUK", 17, 36),
        ("ACT", 8, 37),
        ("ACT", 15, 34),
        ("ACT", 24, 7),
    }
)


def is_intentional_blank(book, chapter, verse) -> bool:
    return (book, int(chapter), int(verse)) in INTENTIONAL_BLANK_VERSES

CCAT_FILENAME = r"^(\d{2}a?)_([A-Z0-9]+)\.TXT$"
CCAT_LINE = r"^(\d{2}):(\d{2})(?:\s(.*))?$"
CCAT_VARIANT_PREFIX = r"^[NBCMSE]\s"

BP5_FILENAME = r"^(\d{2})_([A-Z0-9]+)\.BP5$"
BP5_LINE = r"^(\d{2})\.(\d{2})(?:\s(.*))?$"
BP5_STRONGS = r"^\d+$"
BP5_PARSING = r"^\{[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\}$"

CSV_HEADER = ["chapter", "verse", "text"]

TEI_ANCHOR = r"^B(\d{2})K(\d+)V(\d+)$"

DATASET_CONTRACTS = {
    paths.CCAT_DATASET: {
        "purpose": "Official accented Byzantine text in Beta code, with variants.",
        "filename": CCAT_FILENAME,
        "record": {"prefix": "chapter:verse", "line": CCAT_LINE},
        "variant": {
            "syntax": "{CODE OLD > NEW}",
            "codes": VARIANT_CODES,
            "prefix": CCAT_VARIANT_PREFIX,
        },
        "invariants": [
            "every non-blank line starts with chapter:verse",
            "variant braces are balanced and not nested",
            "variant content starts with a known code and contains '>'",
            "blank records are allowed only for the intentional blank verses",
        ],
    },
    paths.BP5_DATASET: {
        "purpose": "Official unaccented text with Strong's numbers and parsing.",
        "filename": BP5_FILENAME,
        "record": {"prefix": "chapter.verse", "line": BP5_LINE},
        "word": {"syntax": "word strongs {parsing} [strongs {parsing}]"},
        "strongs": BP5_STRONGS,
        "parsing": BP5_PARSING,
        "invariants": [
            "every non-blank line starts with chapter.verse",
            "every word is followed by a positive Strong's number and parsing code",
            "multi-parsing alternatives are allowed after the first pair",
            "blank records are allowed only for the intentional blank verses",
        ],
    },
    paths.dataset_name("csv/accented/no-variants"): {
        "purpose": "Unicode CSV of CCAT with variants removed.",
        "header": CSV_HEADER,
        "invariants": [
            "header is chapter,verse,text",
            "chapter and verse are integers",
            "text is non-empty except for the intentional blank verses",
            "no duplicate (chapter, verse) keys",
            "no Beta-code backslashes",
        ],
    },
    paths.dataset_name("csv/accented/with-variants"): {
        "purpose": "Unicode CSV of CCAT with variants retained.",
        "header": CSV_HEADER,
        "invariants": [
            "header is chapter,verse,text",
            "chapter and verse are integers",
            "text is non-empty except for the intentional blank verses",
            "no duplicate (chapter, verse) keys",
            "no Beta-code backslashes",
        ],
    },
    paths.dataset_name("csv/strongs/no-parsing"): {
        "purpose": "Unicode CSV of the unaccented text with Strong's numbers retained and morphology (`{...}`) dropped; consecutive identical numbers for one word collapse.",
        "header": CSV_HEADER,
        "invariants": [
            "header is chapter,verse,text",
            "chapter and verse are integers",
            "text is non-empty except for the intentional blank verses",
            "no duplicate (chapter, verse) keys",
            "Strong's numbers are present and morphology braces are absent",
            "consecutive identical Strong's numbers for one word are collapsed",
        ],
    },
    paths.dataset_name("csv/strongs/with-parsing"): {
        "purpose": "Unicode CSV of the Strong's text with parsing retained.",
        "header": CSV_HEADER,
        "invariants": [
            "header is chapter,verse,text",
            "chapter and verse are integers",
            "text is non-empty except for the intentional blank verses",
            "no duplicate (chapter, verse) keys",
        ],
    },
    paths.dataset_name("csv/unaccented"): {
        "purpose": "Plain unaccented Unicode text with no Strong's numbers or parsing.",
        "header": CSV_HEADER,
        "invariants": [
            "header is chapter,verse,text",
            "chapter and verse are integers",
            "text is non-empty except for the intentional blank verses",
            "no duplicate (chapter, verse) keys",
            "no Strong's numbers or morphology braces",
        ],
    },
    paths.TEI_DATASET: {
        "purpose": "Unaccented TEI-XML export generated from csv/unaccented.",
        "structure": "TEI/teiHeader/text/body/div[@type=book]/div[@type=chapter]/ab/w",
        "anchor": TEI_ANCHOR,
        "invariants": [
            "XML is well-formed",
            "each file has book divisions with known Bxx ids",
            "verse anchors are unique and match BxxKxVx",
            "no empty <w> elements",
            "intentional blank verses are empty <ab> elements",
        ],
    },
    paths.TEI_BYZ_DATASET: {
        "purpose": "Combined TEI-XML of all 27 books.",
        "structure": "same as per-book TEI, with 27 book divisions",
        "anchor": TEI_ANCHOR,
        "invariants": ["covers the same books as the per-book files"],
    },
}
