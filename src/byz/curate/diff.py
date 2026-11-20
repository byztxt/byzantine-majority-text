"""Successive edition diffs.

Each pair produces a Unicode-first report, a machine-readable CSV, and four
word-diff views: the Beta-code source tier, the exact Unicode main text for the
source-differing verses, the Unicode apparatus (with variants), and the full
normalised Unicode main text.
"""

import csv
import difflib
import re
import textwrap
from collections import Counter, defaultdict
from pathlib import Path

from byz import generated
from byz.contract import paths
from byz.reconcile import compare, normalize, sources

from . import editions

PAIRS = [
    ("rp2005", "rp2005-2019"),
    ("rp2005-2019", "rp2018"),
    ("rp2018", "rp2018-2023"),
    ("rp2005", "rp2018"),
]

# Word-diff tokens are either a run of non-whitespace (a word, with any
# attached punctuation) or a run of whitespace.  Keeping whitespace as tokens
# lets us detect pure-whitespace edits and leave them unmarked.
TOKEN_RE = re.compile(r"\S+|\s+")

PARAGRAPH_MARKER = "\u00b6"
APOSTROPHE_TABLE = str.maketrans({"\u2019": "'", "\u2018": "'"})

CSV_FIELDS = [
    "book",
    "chapter",
    "verse",
    "category",
    "source_word_diff",
    "text_word_diff",
    "source_left",
    "source_right",
    "text_left",
    "text_right",
    "text_changed",
    "apparatus_word_diff",
    "apparatus_changed",
]

# Shared with docs/EDITIONS.md so the explanation cannot drift.  The
# source-tier comparison runs `normalize.normalize_spacing`, which rewrites
# `\s*-\s*` to ` - `; the derived text keeps each artifact's raw dash spacing.
DERIVED_ONLY_TEXT = (
    "The source-tier comparison canonicalises dash spacing (`-` \u2194 ` - `), "
    "so raw dash-spacing differences are invisible there but survive in the "
    "derived text. All current derived-only cases are attached-vs-spaced dashes."
)


def derived_only_lines(width: int = 76) -> list:
    """Wrapped lines for the derived-only explanation."""
    return textwrap.wrap(DERIVED_ONLY_TEXT, width=width)


def _load_official(edition_id: str) -> dict:
    directory = editions.edition_dir(edition_id) / "source" / "ccat"
    books = {}
    for path in sorted(directory.glob("*.CCT")):
        abbr = sources.OFFICIAL_TO_ABBR.get(path.stem.upper())
        if abbr:
            books[abbr] = normalize.parse_cct(path.read_text())
    return books


def _load_historical(edition_id: str) -> dict:
    directory = editions.edition_dir(edition_id) / "source" / "textonly-beta-code"
    books = {}
    for path in sorted(directory.glob("*.CCT")):
        abbr = sources.OFFICIAL_TO_ABBR.get(path.stem.upper())
        if abbr:
            books[abbr] = normalize.parse_cct(path.read_text())
    return books


def _load_current(edition_id: str) -> dict:
    directory = editions.edition_dir(edition_id) / "source" / "CCAT"
    books = {}
    for path in sorted(directory.glob("*.TXT")):
        num = path.name.split("_", 1)[0]
        abbr = paths.NUM_TO_ABBR.get(num)
        if abbr:
            books[abbr] = normalize.parse_current_ccat(path.read_text())
    return books


def load_source(edition_id: str) -> dict:
    edition = editions.EDITIONS[edition_id]
    if edition["source_kind"] == "official":
        return _load_official(edition_id)
    if edition["source_kind"] == "historical":
        return _load_historical(edition_id)
    return _load_current(edition_id)


VIEWS = ("no-variants", "with-variants")


def load_text(edition_id: str, view: str = "no-variants") -> dict:
    """Load the Unicode accented text keyed by (book, chapter, verse).

    `view` is `no-variants` (the main text) or `with-variants` (the apparatus,
    where variant readings stay inside `{...}` braces). An unknown view is a
    programming error, not an empty file set, so it raises instead of returning
    `{}`; a missing edition or view raises `FileNotFoundError` naming the path.
    """
    if view not in VIEWS:
        raise ValueError(
            f"unknown view {view!r}; expected one of {', '.join(VIEWS)}"
        )
    directory = (
        editions.edition_dir(edition_id) / "csv" / "accented" / view
    )
    if not directory.is_dir():
        raise FileNotFoundError(
            f"no {view} CSV view for {edition_id}: {directory}"
        )
    verses = {}
    for path in sorted(directory.glob("*.csv")):
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                key = (path.stem, int(row["chapter"]), int(row["verse"]))
                verses[key] = row["text"]
    return verses


def normalize_text(text: str) -> str:
    """Comparison form of a Unicode verse.

    Paragraph markers are removed, apostrophe typography is mapped to a
    straight apostrophe, and whitespace runs are collapsed (not removed)
    before the word diff is computed.  Dash spacing is preserved, so ` - `
    and `-` still differ.  The exact text is kept separately in the CSV
    `text_left`/`text_right` columns.
    """
    text = text.replace(PARAGRAPH_MARKER, "").translate(APOSTROPHE_TABLE)
    return re.sub(r"\s+", " ", text).strip()


def _boundaries(tokens: list) -> tuple:
    """Split changed tokens into (leading whitespace, words, trailing space)."""
    start, end = 0, len(tokens)
    while start < end and not tokens[start].strip():
        start += 1
    while end > start and not tokens[end - 1].strip():
        end -= 1
    return (
        "".join(tokens[:start]),
        "".join(tokens[start:end]),
        "".join(tokens[end:]),
    )


def word_diff(left: str, right: str) -> str:
    """Return `left` with git `--word-diff` markers for changes to `right`.

    The text is reconstructed with markers, with removed words wrapped in
    `[-...-]` and added words in `{+...+}`.  Whitespace between changed words
    stays inside the markers, but whitespace at change boundaries may be
    normalised.  A change that is only whitespace is left unmarked.  Exact
    text is in `changes.csv` (`*_left`/`*_right`).
    """
    left_tokens = TOKEN_RE.findall(left)
    right_tokens = TOKEN_RE.findall(right)
    matcher = difflib.SequenceMatcher(
        None, left_tokens, right_tokens, autojunk=False
    )
    parts = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            parts.append("".join(left_tokens[i1:i2]))
            continue
        old_prefix, old_words, old_suffix = _boundaries(left_tokens[i1:i2])
        new_prefix, new_words, new_suffix = _boundaries(right_tokens[j1:j2])
        if not old_words and not new_words:
            # A pure-whitespace edit: show it, but do not pretend it is a word.
            parts.append(
                "".join(right_tokens[j1:j2]) or "".join(left_tokens[i1:i2])
            )
            continue
        parts.append(new_prefix or old_prefix)
        if old_words:
            parts.append(f"[-{old_words}-]")
        if new_words:
            parts.append(f"{{+{new_words}+}}")
        parts.append(new_suffix or old_suffix)
    return "".join(parts)


def _book_key(book: str) -> tuple:
    try:
        return (editions.BOOK_ORDER.index(book), book)
    except ValueError:
        return (len(editions.BOOK_ORDER), book)


def _verse_key(row: dict) -> tuple:
    return (_book_key(row["book"]), row["chapter"], row["verse"])


def _source_rows(left: dict, right: dict) -> list:
    rows = []
    for abbr in set(left) | set(right):
        metrics = compare.compare_maps(left.get(abbr, {}), right.get(abbr, {}))
        for difference in metrics["differences"]:
            rows.append(
                {
                    "book": abbr,
                    "chapter": difference["chapter"],
                    "verse": difference["verse"],
                    "category": difference["category"],
                    "source_left": difference["current"],
                    "source_right": difference["official"],
                }
            )
    rows.sort(key=_verse_key)
    return rows


def _add_text(
    rows: list,
    left_text: dict,
    right_text: dict,
    left_variants: dict,
    right_variants: dict,
) -> None:
    """Add the derived-text and apparatus views to each source-tier row."""
    for row in rows:
        key = (row["book"], row["chapter"], row["verse"])
        text_left = left_text.get(key, "")
        text_right = right_text.get(key, "")
        row["text_left"] = text_left
        row["text_right"] = text_right
        row["source_word_diff"] = word_diff(
            row["source_left"], row["source_right"]
        )
        # The readable Text view is the normalised form, so paragraph markers
        # and apostrophe/whitespace conventions cannot masquerade as changes.
        row["text_word_diff"] = word_diff(
            normalize_text(text_left), normalize_text(text_right)
        )
        row["text_changed"] = (
            "true"
            if normalize_text(text_left) != normalize_text(text_right)
            else "false"
        )
        # The apparatus view keeps the variant readings, so a change that the
        # main text drops still has a Unicode rendering here. Some Beta-code
        # encoding-order differences convert to the same Unicode; those rows
        # carry an empty marker set and the report names them explicitly.
        apparatus_left = normalize_text(left_variants.get(key, ""))
        apparatus_right = normalize_text(right_variants.get(key, ""))
        row["apparatus_word_diff"] = word_diff(apparatus_left, apparatus_right)
        row["apparatus_changed"] = (
            "true" if apparatus_left != apparatus_right else "false"
        )


def _derived_rows(left_text: dict, right_text: dict, categories: dict) -> list:
    """Every verse whose normalised Unicode main text differs."""
    rows = []
    for key in set(left_text) | set(right_text):
        text_left = left_text.get(key, "")
        text_right = right_text.get(key, "")
        if normalize_text(text_left) == normalize_text(text_right):
            continue
        rows.append(
            {
                "book": key[0],
                "chapter": key[1],
                "verse": key[2],
                "category": categories.get(key, ""),
                "left": text_left,
                "right": text_right,
            }
        )
    rows.sort(key=_verse_key)
    return rows


def _write_changes(path: Path, rows: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=CSV_FIELDS,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def _verse_diff(
    path: Path,
    left_id: str,
    right_id: str,
    label: str,
    entries: list,
    transform=word_diff,
    preamble: tuple = (),
) -> None:
    """Write a word-diff file with one `@@ BOOK C:V @@` hunk per verse.

    Each hunk is a single line of context plus `[-removed-]` and `{+added+}`
    markers, in the style of `git diff --word-diff`.  There are no `-`/`+`
    whole-verse lines and no line ranges: these files are readable diffs, not
    patchable line-based diffs.
    """
    lines = list(preamble)
    lines.append(f"# Word diff: {left_id} -> {right_id} ({label})")
    for entry in entries:
        category = f" [{entry['category']}]" if entry.get("category") else ""
        lines.append(
            f"@@ {entry['book']} {entry['chapter']}:{entry['verse']}"
            f"{category} @@"
        )
        lines.append(transform(entry["left"], entry["right"]))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _code_block(lines: list, text: str) -> None:
    lines.append("```")
    lines.append(text)
    lines.append("```")


def _report(
    left_id: str,
    right_id: str,
    rows: list,
    derived: list,
    path: Path,
) -> None:
    left = editions.metadata(left_id)
    right = editions.metadata(right_id)
    categories = Counter(row["category"] for row in rows)
    books = Counter(row["book"] for row in rows)
    apparatus_only = sum(1 for row in rows if row["text_changed"] == "false")
    apparatus_unicode = sum(
        1
        for row in rows
        if row["text_changed"] == "false" and row["apparatus_changed"] == "true"
    )
    apparatus_encoding_only = apparatus_only - apparatus_unicode
    source_keys = {
        (row["book"], row["chapter"], row["verse"]) for row in rows
    }
    derived_only = [
        row
        for row in derived
        if (row["book"], row["chapter"], row["verse"]) not in source_keys
    ]

    lines = [
        f"# Diff: {left_id} -> {right_id}",
        "",
        f"- **Left:** `{left_id}` ({left['status']}; {left['basis']})",
        f"- **Right:** `{right_id}` ({right['status']}; {right['basis']})",
        f"- **Source-tier differing verses:** {len(rows)}",
        f"- **Derived-text differing verses (normalised):** {len(derived)}",
        "- **Apparatus-only changes (source differs, main text identical):** "
        f"{apparatus_only}",
        f"- **Apparatus-only changes shown in Unicode:** {apparatus_unicode}",
        "- **Apparatus-only changes with no Unicode difference (Beta-code "
        f"encoding only):** {apparatus_encoding_only}",
        "- **Derived-only differences (text differs, source-tier comparison "
        f"unchanged):** {len(derived_only)}",
        "",
        "## Notation",
        "",
        "- **Text** is the Unicode accented main text from",
        f"  `editions/{left_id}/csv/accented/no-variants/` and",
        f"  `editions/{right_id}/csv/accented/no-variants/`.",
        "- **Source** is the edition's Beta-code source tier (official `.CCT`,",
        "  historical `textonly-beta-code`, or current `source/CCAT`).",
        "- `[-removed-]{+added+}` marks a word-level change, in the style of",
        "  `git diff --word-diff`. Text outside the markers is unchanged",
        "  context. Beta-code apparatus braces (`{N ... }`) are part of the",
        "  source text and can appear next to or inside the markers.",
        "- The marker delimiters are the fixed strings `[-`, `-]`, `{+`, `+}`; a",
        "  literal `-` or `>` next to a delimiter is part of the text (for",
        "  example, a dash-spacing change can render as",
        "  `[-εἶπεν --]{+εἶπεν-+}`).",
        "- Text comparison ignores paragraph markers (`\u00b6`) and normalises",
        "  apostrophe typography (`\u2019`/`\u2018` -> `'`) and whitespace; the",
        "  word-diff shown omits those conventions. The exact text is in",
        "  `changes.csv` (`text_left`/`text_right`).",
        "- **Apparatus** is the Unicode accented text with variants, from",
        f"  `editions/{left_id}/csv/accented/with-variants/` and",
        f"  `editions/{right_id}/csv/accented/with-variants/`.",
        "",
        "### Why the main text can be unchanged while the apparatus changes",
        "",
        "A variant reading lives inside literal `{...}` braces in the",
        "with-variants view; the main text drops the braces together with the",
        "note. When an edition adds or rewrites an apparatus note and the main",
        "reading does not move, the source tier and the apparatus differ while",
        "the main text stays identical. The rendered apparatus change therefore",
        "doubles the braces: the outer `{+` and `+}` are the diff markers, and",
        "the inner `{Byz ... }` is the reading itself, so an added variant",
        "renders as `{+{Byz \u03c4\u03b5 > \u03b4\u03b5 }+}`.",
        "",
        "An apparatus-only entry can take any of these shapes (they can",
        "combine): it has a Unicode difference and appears in `apparatus.diff`;",
        "it differs only in the Beta-code encoding and converts to the same",
        "Unicode, in which case the report names it as encoding-only and",
        "`apparatus.diff` omits it; or the exact main text changed without a",
        "normalised change, in which case the entry is also marked",
        "`see text.diff`.",
        "",
        "## Categories (source tier)",
        "",
        "| Category | Count |",
        "| --- | ---: |",
    ]
    for category, count in sorted(categories.items()):
        lines.append(f"| `{category}` | {count} |")
    lines.extend(
        [
            "",
            "## Books (source tier)",
            "",
            "| Book | Differing verses |",
            "| --- | ---: |",
        ]
    )
    for book in sorted(books, key=_book_key):
        lines.append(f"| `{book}` | {books[book]} |")

    main_text = [row for row in rows if row["text_changed"] == "true"]
    apparatus = [row for row in rows if row["text_changed"] == "false"]

    lines.extend(["", "## Main-text changes", ""])
    if not main_text:
        lines.extend(["None.", ""])
    for row in main_text:
        lines.append(
            f"### {row['book']} {row['chapter']}:{row['verse']} "
            f"\u00b7 `{row['category']}`"
        )
        lines.append("")
        lines.append("Text:")
        lines.append("")
        _code_block(lines, row["text_word_diff"])
        lines.extend(["", "Source (Beta code):", ""])
        _code_block(lines, row["source_word_diff"])
        lines.append("")

    lines.extend(["## Apparatus-only changes", ""])
    if not apparatus:
        lines.extend(
            [
                "None: every source-tier difference also changes the "
                "normalised main text.",
                "",
            ]
        )
    for row in apparatus:
        note = ""
        if row["text_left"] != row["text_right"]:
            note = (
                " \u2014 formatting-only (normalised text identical; "
                "see `text.diff`)"
            )
        lines.append(
            f"- `{row['book']} {row['chapter']}:{row['verse']}` \u00b7 "
            f"`{row['category']}`{note}"
        )
        if row["apparatus_changed"] == "true":
            lines.append(
                f"  - Apparatus (Unicode): `{row['apparatus_word_diff']}`"
            )
        else:
            lines.append(
                "  - Apparatus (Unicode): no difference after conversion to "
                "Unicode (Beta-code encoding only)"
            )
        lines.append(
            f"  - Apparatus (Beta code): `{row['source_word_diff']}`"
        )
    if apparatus:
        lines.append("")

    lines.extend(["## Derived-only differences", ""])
    if not derived_only:
        lines.extend(
            [
                "None: every derived-text difference is also a source-tier",
                "difference.",
                "",
            ]
        )
    else:
        lines.extend(derived_only_lines())
        lines.extend(
            [
                "",
                "They are listed in full in `derived.diff`.",
                "",
            ]
        )
        grouped = defaultdict(list)
        for row in derived_only:
            grouped[row["book"]].append(f"{row['chapter']}:{row['verse']}")
        for book in sorted(grouped, key=_book_key):
            lines.append(f"- `{book}`: {', '.join(grouped[book])}")
        lines.append("")

    generated.write_markdown(path, "\n".join(lines))


README_TEXT = """\
# Successive edition diffs

These directories are generated by `scripts/diff_editions.py`
(`src/byz/curate/diff.py`). Do not edit them by hand; rerun the script after a
source or converter change.

Each `<left>--<right>/` directory compares two curated editions:

| Directory | Comparison |
| --- | --- |
| `rp2005--rp2005-2019` | official 2005 -> released 2005+2019 |
| `rp2005-2019--rp2018` | released 2005+2019 -> official 2018 |
| `rp2018--rp2018-2023` | official 2018 -> released 2018+2023 |
| `rp2005--rp2018` | official 2005 -> official 2018 |

## Files

- `report.md` - Unicode-first human-readable report. `Main-text changes` lists
  the verses whose normalised Unicode text changes, with the Text word diff
  first and the Beta-code Source second. `Apparatus-only changes` compacts the
  remaining source-tier differences into one entry per verse, showing the
  Unicode Apparatus word diff first and the Beta-code diff second; an entry
  whose only change is Beta-code encoding says so instead of printing an empty
  diff. The Text diff is normalised: paragraph markers, apostrophe typography,
  and whitespace are omitted.
- `changes.csv` - one row per source-tier difference, with the category, the
  Beta-code source word diff, the Unicode Text word diff (`text_word_diff`),
  the Unicode Apparatus word diff (`apparatus_word_diff`), the full left/right
  source and exact text, and the `text_changed` and `apparatus_changed` flags.
  The word diffs are normalised; `text_left`/`text_right` are exact.
- `source.diff` - word-diff style, one line per verse, for the Beta-code
  source tier.
- `text.diff` - word-diff style, one line per verse, for the exact Unicode
  accented main text. It includes every source-differing verse whose exact text
  differs, including formatting-only changes such as a `\u00b6` edit.
  Paragraph markers and apostrophes are shown as stored.
- `apparatus.diff` - the word diff of the normalised Unicode accented text with
  variants (`csv/accented/with-variants`) for every apparatus-only change that
  has a Unicode difference (encoding-only rows are named in `report.md`).
  Variant readings stay inside `{...}` braces, and the braces are literal text
  inside the diff markers. `source.diff` is the Beta-code view of the same
  verses.
- `derived.diff` - the word diff of the normalised Unicode main text for every
  differing verse, not only the source-differing ones.

The `.diff` files are word-diff style, with one
`@@ BOOK CHAPTER:VERSE [category] @@` hunk and one marked line per verse,
not patchable line-based diffs: they have no line ranges and
no `-`/`+` whole-verse lines.

## Source and text

**Source** is the edition's Beta-code source tier: the official `.CCT` archive
for `rp2005`/`rp2018`, the recovered historical `textonly-beta-code` for
`rp2005-2019`, and the current `source/CCAT` for `rp2018-2023`.

**Text** is the derived Unicode accented main text in
`editions/<id>/csv/accented/no-variants/`.

**Apparatus** is the Unicode accented text with variants in
`editions/<id>/csv/accented/with-variants/`. The variant readings stay inside
literal `{...}` braces; the main text drops them.

## Notation

- `[-removed-]{+added+}` wraps changed words; unchanged text is context. The
  markers come from `difflib.SequenceMatcher` over words and whitespace.
  Beta-code apparatus braces (`{N ... }`) are part of the source text and can
  appear next to or inside the markers.
- The marker delimiters are the fixed strings `[-`, `-]`, `{+`, `+}`; a
  literal `-` or `>` next to a delimiter is part of the text (for example, a
  dash-spacing change can render as `[-εἶπεν --]{+εἶπεν-+}`).
- The Unicode Apparatus diff doubles the braces: the outer `{+`/`+}` are the
  diff markers and the inner `{...}` is the reading, so an added variant
  renders as `{+{Byz τε > δε }+}`. That is why the main text can be identical
  while the apparatus changes.
- The Text word diff is normalised: `\u00b6` is removed, `\u2019`/`\u2018`
  become `'`, and whitespace is collapsed (not removed). The exact text is in
  `changes.csv.text_left`/`text_right` and in `text.diff`.
- `@@ BOOK CHAPTER:VERSE [category] @@` opens a verse hunk. The category is
  the source-tier classification and is omitted in `derived.diff` when the
  verse is not a source-tier difference.

## The `derived.diff` caveat

`derived.diff` compares the normalised main text after removing paragraph
markers (`\u00b6`), mapping curly apostrophes (`\u2019`/`\u2018`) to `'`, and
collapsing whitespace.

__DERIVED_ONLY_NOTE__

Use `report.md`, `changes.csv`, `source.diff`, and `text.diff` for edition
changes; use `derived.diff` to audit everything a reader of the Unicode text
would see.

## Blank verses

LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 are empty rows in the
official/current editions and absent in `rp2005-2019`. The source-tier
comparison ignores row presence, so these four verses are out of scope for
these diffs.
"""

README_TEXT = README_TEXT.replace(
    "__DERIVED_ONLY_NOTE__", textwrap.fill(DERIVED_ONLY_TEXT, width=79)
)


def write_readme(path=None) -> Path:
    """Write `reports/diffs/README.md` from the same module as the diffs."""
    if path is None:
        path = editions.DIFFS_DIR / "README.md"
    return generated.write_markdown(path, README_TEXT)


def diff_pair(left_id: str, right_id: str) -> Path:
    left = load_source(left_id)
    right = load_source(right_id)
    rows = _source_rows(left, right)
    left_text = load_text(left_id)
    right_text = load_text(right_id)
    left_variants = load_text(left_id, "with-variants")
    right_variants = load_text(right_id, "with-variants")
    _add_text(rows, left_text, right_text, left_variants, right_variants)
    categories = {
        (row["book"], row["chapter"], row["verse"]): row["category"]
        for row in rows
    }
    derived = _derived_rows(left_text, right_text, categories)

    out = editions.DIFFS_DIR / f"{left_id}--{right_id}"
    out.mkdir(parents=True, exist_ok=True)
    _write_changes(out / "changes.csv", rows)

    _verse_diff(
        out / "source.diff",
        left_id,
        right_id,
        "Beta-code source tier",
        [
            {
                "book": row["book"],
                "chapter": row["chapter"],
                "verse": row["verse"],
                "category": row["category"],
                "left": row["source_left"],
                "right": row["source_right"],
            }
            for row in rows
        ],
    )
    _verse_diff(
        out / "text.diff",
        left_id,
        right_id,
        "exact Unicode accented main text",
        [
            {
                "book": row["book"],
                "chapter": row["chapter"],
                "verse": row["verse"],
                "category": row["category"],
                "left": row["text_left"],
                "right": row["text_right"],
            }
            for row in rows
            if row["text_left"] != row["text_right"]
        ],
        preamble=(
            "# Exact derived artifact text from csv/accented/no-variants, for",
            "# every source-differing verse whose exact text differs (including",
            "# formatting-only changes). Paragraph markers (\u00b6) and",
            "# apostrophe typography are shown as stored.",
            "# derived.diff is the normalised full view.",
        ),
    )
    _verse_diff(
        out / "apparatus.diff",
        left_id,
        right_id,
        "Unicode accented text with apparatus",
        [
            {
                "book": row["book"],
                "chapter": row["chapter"],
                "verse": row["verse"],
                "category": row["category"],
                "left": left_variants.get(
                    (row["book"], row["chapter"], row["verse"]), ""
                ),
                "right": right_variants.get(
                    (row["book"], row["chapter"], row["verse"]), ""
                ),
            }
            for row in rows
            if row["text_changed"] == "false"
            and row["apparatus_changed"] == "true"
        ],
        transform=lambda left, right: word_diff(
            normalize_text(left), normalize_text(right)
        ),
        preamble=(
            "# Unicode accented text with apparatus "
            "(csv/accented/with-variants),",
            "# for every apparatus-only change that has a Unicode difference. A row",
            "# whose difference exists only in the Beta-code encoding converts to the",
            "# same Unicode and is named in report.md instead. Variant readings stay",
            "# inside {...} braces, and those braces are literal text inside the diff",
            "# markers. source.diff is the Beta-code view of the same verses.",
        ),
    )
    _verse_diff(
        out / "derived.diff",
        left_id,
        right_id,
        "normalised Unicode accented main text",
        derived,
        transform=lambda left, right: word_diff(
            normalize_text(left), normalize_text(right)
        ),
        preamble=(
            "# Full normalised diff of the Unicode accented main text",
            "# (csv/accented/no-variants), for every differing verse.",
            "# Compared after removing paragraph markers (\u00b6), normalising "
            "apostrophe typography (\u2019/\u2018 -> ')",
            "# and collapsing whitespace runs; the text shown is normalised.",
            "# The source-tier comparison canonicalises dash spacing "
            "(`-` \u2194 ` - `),",
            "# so attached-vs-spaced dashes appear here but not in the "
            "source tier.",
            "# Includes typographic/converter-generation differences, not only "
            "edition changes.",
            "# Use report.md, changes.csv, source.diff, and text.diff for "
            "source-tier changes.",
        ),
    )
    _report(left_id, right_id, rows, derived, out / "report.md")
    return out


def diff_all() -> list:
    paths = [diff_pair(left, right) for left, right in PAIRS]
    write_readme()
    return paths
