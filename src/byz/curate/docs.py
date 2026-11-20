"""Generate docs/EDITIONS.md and the root README editions section."""

import json
import re

from .. import generated
from . import diff, editions

BEGIN = "<!-- editions:begin -->"
END = "<!-- editions:end -->"

# The canonical repository. `docs/` is one level below the root, so in-repo
# links from that file start with `../`. Keep this the only copy of the URL:
# `tests/curate/test_editions.py` asserts the literal appears once.
REPO_URL = "https://github.com/byztxt/byzantine-majority-text"


def _tag(tag: str) -> str:
    """Link one release tag; a tag range is two of these with a plain hyphen."""
    return f"[`{tag}`]({REPO_URL}/releases/tag/{tag})"


def _tag_range(first: str, last: str) -> str:
    # A range has no single canonical URL, so link both endpoints and leave the
    # hyphen as text rather than sending a click to the newest tag.
    return f"{_tag(first)}-{_tag(last)}"


def _commit(sha: str) -> str:
    return f"[`{sha}`]({REPO_URL}/commit/{sha})"


# A bare release tag in prose (the manifest's `basis` value, for example). A
# tag that is itself the entire inline-code span (`` `v1.2.3` ``) is skipped, so
# this helper is safe to apply to generated prose that has been through `_tag`
# first. It does not parse Markdown: a tag inside a longer code span, a link
# label, or a URL would be rewritten, so only apply it to plain prose.
_BARE_TAG_RE = re.compile(r"(?<![\w`])v\d+\.\d+\.\d+(?![\w`])")


def _link_bare_tags(text: str) -> str:
    """Link bare release tags that are not already an inline-code span.

    A tag counts as linked when it is delimited by a backtick or a word
    character on either side. This guarantees the output of `_tag` is not
    re-linked and that `` `v1.2.3` `` is left alone; it does not understand
    Markdown code spans or URLs in general.
    """
    return _BARE_TAG_RE.sub(lambda match: _tag(match.group(0)), text)


def _diff_dir(left: str, right: str) -> str:
    # Relative to `docs/`: the target is one level up, at the repository root.
    path = f"reports/diffs/{left}--{right}/"
    return f"[`{path}`](../{path})"


# Retired working-tree convenience trees (removed 2026-11-19). This is the one
# authoritative old -> new mapping; docs/EDITIONS.md renders it and the release
# note repeats the data rows. Nothing else may name these paths except
# `recover.py`/`history.py` (git pathspecs for tag `v2.0.3` history) and the
# tests that lock the deletion.
RETIRED_PATHS = (
    ("csv-unicode/ccat/no-variants", "editions/rp2018-2023/csv/accented/no-variants"),
    ("csv-unicode/ccat/with-variants", "editions/rp2018-2023/csv/accented/with-variants"),
    ("csv-unicode/strongs/with-parsing", "editions/rp2018-2023/csv/strongs/with-parsing"),
    ("csv-unicode/strongs/no-parsing", "editions/rp2018-2023/csv/strongs/no-parsing"),
    ("csv-unicode/strongs/no-parsing (second view)", "editions/rp2018-2023/csv/unaccented"),
    ("tei-xml-unicode/no-accents", "editions/rp2018-2023/tei/unaccented"),
    ("tei-xml-unicode/no-accents/BYZ/byz.xml", "editions/rp2018-2023/tei/unaccented/BYZ/byz.xml"),
    ("tei-xml-unicode/assets/coll.png", "docs/assets/coll.png"),
    ("tei-xml-unicode/assets/demo_collation.xlsx", "docs/assets/demo_collation.xlsx"),
    ("tei-xml-unicode/assets/demo_john_1.xml", "docs/assets/demo_john_1.xml"),
    ("tei-xml-unicode/README.md (CollateX walkthrough)", "docs/COLLATEX.md"),
    ("csv-unicode/README.md (multi-parsing note)", "docs/EDITIONS.md; source/README.md"),
)

# Rows whose left-hand side is a note about a retired path rather than a path
# itself. They render as plain text so no reader mistakes the parenthetical for
# part of a real path.
RETIRED_NON_PATHS = frozenset(
    {
        "csv-unicode/strongs/no-parsing (second view)",
        "tei-xml-unicode/README.md (CollateX walkthrough)",
        "csv-unicode/README.md (multi-parsing note)",
    }
)


def _now_cell(new: str) -> str:
    """Render one or more `;`-separated targets as separate code spans."""
    return " and ".join(f"`{target.strip()}`" for target in new.split(";"))


def _retired_cell(old: str) -> str:
    """Render a retired path as a code span, or a note as plain text."""
    return old if old in RETIRED_NON_PATHS else f"`{old}`"


def _manifests() -> list:
    rows = []
    for edition_id in editions.EDITIONS:
        path = editions.edition_dir(edition_id) / "manifest.json"
        if path.exists():
            rows.append(json.loads(path.read_text(encoding="utf-8")))
    return rows


def write_editions_doc() -> str:
    manifests = {row["edition"]: row for row in _manifests()}
    lines = [
        "# Editions",
        "",
        "This repository curates four Robinson-Pierpont texts. Two are **official**",
        "and two are **released**.",
        "",
        "- **Official** means published in print by Dr. Maurice A. Robinson.",
        "- **Released** means published as an artifact in this repository.",
        "",
        "The official PDFs are the ultimate source of truth. The ZIP archives and",
        "`source/` are the authoritative machine-readable text for the",
        "derivatives.",
        "",
        "For where everything lives in the repository, see the layout table in",
        "the [root README](../README.md#repository-layout).",
        "",
        "## The four editions",
        "",
        "| Edition | Status | Basis | Repo releases | PDF (committed) |",
        "| --- | --- | --- | --- | --- |",
    ]
    for edition_id in editions.EDITIONS:
        row = manifests.get(edition_id, {})
        release = (
            _tag_range(row.get("first_release"), row.get("latest_release"))
            if row.get("release_range")
            else "none"
        )
        pdf = "none"
        if row.get("pdf"):
            # docs/ is one level below the repository root, so the committed
            # PDF is linked relative to this file.
            pdf = (
                f"[`{edition_id} PDF`](../{row['pdf']}) "
                f"(`{row.get('pdf_sha256', '')}`)"
            )
        lines.append(
            f"| `{edition_id}` | {row.get('status', '')} | "
            f"{_link_bare_tags(row.get('basis', ''))} | {release} | {pdf} |"
        )
    hist = manifests.get("rp2005-2019", {})
    cur = manifests.get("rp2018-2023", {})
    hist_range = (
        _tag_range(hist.get("first_release"), hist.get("latest_release"))
        if hist.get("release_range")
        else "none"
    )
    cur_range = (
        _tag_range(cur.get("first_release"), cur.get("latest_release"))
        if cur.get("release_range")
        else "none"
    )
    retired_section = [
        "`rp2018-2023` also has a frozen `source/` snapshot, which intentionally",
        "duplicates the repository `source/` so the edition can be downloaded and",
        "verified on its own.",
        "",
        "See [`COLLATEX.md`](COLLATEX.md) for using the unaccented TEI with",
        "CollateX.",
        "",
        "## Where the old working-tree paths went",
        "",
        "`csv-unicode/` and `tei-xml-unicode/` were removed on 2026-11-19. The",
        "current text is `editions/rp2018-2023/`; the retired paths return 404 by",
        "design, with no redirects and no stubs.",
        "",
        "| Retired path | Now |",
        "| --- | --- |",
    ]
    retired_section += [
        f"| {_retired_cell(old)} | {_now_cell(new)} |"
        for old, new in RETIRED_PATHS
    ]
    retired_section += [
        "",
        "The bytes did not change: the files moved, and the edition's",
        "`manifest.json` records the same hashes as before the change. See",
        "[`RELEASE-NOTES.md`](RELEASE-NOTES.md) for the breaking-change note.",
    ]
    lines.extend(
        [
            "",
            "## Source feature matrix",
            "",
            "| Source | Provenance | Accents | Strong's | Apparatus | Parsing |",
            "| --- | --- | --- | --- | --- | --- |",
            "| Official 2005/2018 `ccat` (`.CCT`) | official archive | yes | no | yes | no |",
            "| Official 2005/2018 ASCII / preformatted | official archive | no | no | no | no |",
            "| Official 2005/2018 PDFs | published print | yes | no | yes | no |",
            "| `source/CCAT` | repo 2018+2023 | yes | no | yes | no |",
            "| `source/Strongs` | official files, not in the six ZIPs | no | yes | no | yes |",
            f"| `textonly-beta-code` ({_tag('v2.0.3')}) | repo 2005 lineage, 2019 | yes | no | yes | no |",
            f"| `parsed` ({_tag('v2.0.3')}) | repo parsed lineage | no | yes | yes | yes |",
            f"| `textonly-online-bible` ({_tag('v2.0.3')}) | repo 2005 lineage | no | no | no | no |",
            "",
            "## What each edition is",
            "",
            "### `rp2005` - official 2005",
            "",
            "The published 2005 print edition (Chilton Book Publishing, Southborough,",
            "Massachusetts). The PDF is the ultimate source of truth. The machine-",
            "readable source is the official `.CCT` archive. It has no repo release",
            "number.",
            "",
            "### `rp2005-2019` - released 2019 revision of the 2005 lineage",
            "",
            f"The repo's last pre-2023 text, recovered from tag {_tag('v2.0.3')}",
            "(`textonly-beta-code` and `parsed`). It was updated in 2019 and is not",
            "the official 2005 print edition. It matches the official 2018 archive in",
            "99.96% of verses and the official 2005 archive in 99.32%, which is why",
            f"calling it simply \"2005\" is misleading. Repo releases: {hist_range}.",
            "",
            "### `rp2018` - official 2018",
            "",
            "The published 2018 print edition (VTR, Nuremberg). The PDF is the",
            "ultimate source of truth. The machine-readable source is the official",
            "`.CCT` archive. It has no repo release number.",
            "",
            "### `rp2018-2023` - released 2018 with 2023 adjustments",
            "",
            "The current maintained text: the 2018 edition plus the 2023 adjustments",
            f"and later minor fixes. It was first released in {_tag('v3.0.0')} and continues",
            f"to receive releases. Repo releases: {cur_range} (and later tags).",
            "",
            "## Why the history looks messy",
            "",
            "- The 2005 lineage lived in `textonly-beta-code`, `parsed`, and",
            "  `csv-unicode` until 2023. It was last updated in 2019.",
            f"- Commit {_commit('97371d7')} (2023-05-30), merged as {_tag('v3.0.0')}, switched the repo to",
            "  the 2018 edition with 2023 adjustments and introduced `source/`.",
            "- The current tree therefore contains only the 2018+2023 text. The 2005",
            "  lineage is curated here so that nobody has to use `git show` to find it.",
            "",
            "## Layout, exports, and verification",
            "",
            "Each edition has `source/`, `csv/`, `tei/`, `manifest.json`, and",
            "`README.md`. The manifest records source and artifact SHA-256 hashes.",
            "",
            "- Official editions: accented CSV (with/without variants) and accented",
            "  TEI are generated from the official `.CCT`; unaccented CSV/TEI are",
            "  generated from the official ASCII. Strong's/parsing are absent because",
            "  the official URL files do not contain them.",
            "- `rp2005-2019`: accented with/without variants, unaccented, Strong's",
            "  with/no parsing, and accented/unaccented TEI are recovered or generated",
            f"  from {_tag('v2.0.3')}.",
            "- `rp2018-2023`: every view is generated from the edition's own",
            "  `source/` snapshot.",
            "",
            *retired_section,
            "",
            "## Blank verses and omitted rows",
            "",
            "LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 are not part of the",
            "Byzantine tradition. The official `.CCT` and ASCII archives contain",
            "them as **blank verse lines**, so they are real data, not conversion",
            "losses. `rp2005` and `rp2018` therefore emit explicit empty records:",
            "7972 accented CSV rows (four empty), 7957 unaccented CSV rows (four",
            "empty), and empty `<ab/>` elements in both TEI views.",
            "`rp2018-2023` behaves the same way (7972 / 7957 rows plus empty",
            "`<ab/>` elements).",
            "",
            "The recovered `rp2005-2019` edition is the exception. Its",
            "`textonly-beta-code`, `parsed`, accented no-variants CSV, unaccented",
            f"CSV, and unaccented TEI are recovered byte-identically from {_tag('v2.0.3')}.",
            f"The accented with-variants derivative differs from {_tag('v2.0.3')} only at",
            "MAR 16:8, where the apparatus literal is corrected. The accented TEI",
            "(from the recovered accented CSV) and the Strong's",
            f"views (from `parsed`) are generated here, and {_tag('v2.0.3')} itself has no",
            "accented TEI. The accented CSV (7968 rows), unaccented CSV (7953",
            "rows), and unaccented TEI **omit** the four verses: the rows are",
            "absent and there is no empty `<ab/>`, even though the source files in",
            "that tag do contain the blank verse lines. The generated accented TEI",
            "inherits the omission; the generated Strong's views include the four",
            "verses as empty rows (7957 rows). The recovered rows are deliberately",
            "not added back; the edition README records the omission.",
            "",
            "## TEI punctuation",
            "",
            "Generated TEI wraps each whitespace-separated token in `<w>`. A",
            "standalone `-` (the official text's dash and deletion marks) is",
            "emitted as `<pc>-</pc>`, and a leading `¶` becomes",
            "`<milestone unit=\"paragraph\" type=\"start\"/>` instead of being glued to",
            "the following word. Punctuation attached to a word stays inside its",
            "`<w>`. Only the accented TEI contains these two markers; the unaccented",
            "TEI has neither, so its markup is unchanged.",
            "",
            "## Apparatus literals",
            "",
            "Generated editions preserve apparatus literals verbatim: the quoted",
            "English notes in `[[ \"...\" ]]` (for example",
            "`[[ \"shorter ending\" ]]` in MAR 16:8) and the exact `\"+\"`",
            "quotation mark keep the source's case and spacing. `rp2005` and",
            "`rp2018` therefore show `[[ \"shorter ending\" ]]` from the official",
            "`.CCT` archives, while `rp2018-2023` shows `[[\"SHORTER ENDING\"]]`",
            "because `source/CCAT` is upper-case with no spaces inside the",
            "brackets. Before this fix the historical converter transliterated the",
            "notes (`σηορτερ ενδινγ`) and rendered `\"+\"` as `\" ̈\"`.",
            "",
            "All curated editions now preserve the literals. The recovered",
            f"`rp2005-2019` with-variants view is the {_tag('v2.0.3')} artifact with exactly",
            "one corrected row: MAR 16:8, where `[[ \"σηορτερ ενδινγ\" ]]` and",
            "`\" ̈\"` are restored to `[[ \"shorter ending\" ]]` and `\"+\"`. The",
            "recovered source files and the other historical views remain",
            f"byte-identical to {_tag('v2.0.3')}.",
            "",
            "## Derived artifacts by edition",
            "",
            "| Edition | Accented no-variants | Accented with-variants | Unaccented | Strong's with-parsing | Strong's no-parsing | Accented TEI | Unaccented TEI |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for edition_id in editions.EDITIONS:
        root = editions.edition_dir(edition_id)
        def has(*parts):
            return (root.joinpath(*parts)).is_dir()
        lines.append(
            f"| `{edition_id}` | "
            f"{'yes' if has('csv','accented','no-variants') else 'no'} | "
            f"{'yes' if has('csv','accented','with-variants') else 'no'} | "
            f"{'yes' if has('csv','unaccented') else 'no'} | "
            f"{'yes' if has('csv','strongs','with-parsing') else 'no'} | "
            f"{'yes' if has('csv','strongs','no-parsing') else 'no'} | "
            f"{'yes' if has('tei','accented') else 'no'} | "
            f"{'yes' if has('tei','unaccented') else 'no'} |"
        )
    lines.extend(
        [
            "",
            "Where a source carries accents, Strong's, apparatus, or parsing, the",
            "edition provides the corresponding derived view. Official editions",
            "have no Strong's/parsing view because those data are not in the official",
            "URL files.",
            "",
            "In `rp2018-2023`, `csv/unaccented/` and `csv/strongs/no-parsing/` hold",
            "the same bytes: they are two names for one text (the plain Unicode",
            "text and the Strong's view with parsing dropped). The duplication is",
            "intentional, and a test asserts the identity.",
            "",
            "### Inherited title quirks",
            "",
            "The unaccented TEI for `2TI` and `PHP` in `rp2018-2023` and",
            "`rp2005-2019` titles the books `Second Timoty` and `Phillipians`.",
            "Both spellings are inherited, not introduced here: `rp2018-2023`",
            "copies the retired `tei-xml-unicode/` convenience tree, and",
            f"`rp2005-2019` recovers the same titles from the {_tag('v2.0.3')} artifacts",
            "that tree held. They are preserved deliberately so the editions'",
            "TEI bytes stay unchanged. Every other title, and the whole",
            "accented TEI (in both editions), uses the corrected spellings.",
            "Do not \"fix\" them without a new edition release.",
            "",
            "In the `csv/strongs/with-parsing/` view a word may be followed by two",
            "sets of Strong's number and parsing code. These are alternative",
            "parsings of the same word (for example, a neuter form that can be",
            "either nominative or accusative), not two separate words; either",
            "parsing is applicable. The convention is explained in",
            "`source/README.md`.",
            "",
            "### Rebuilding the curated editions",
            "",
            "The official `.CCT` archives also contain the `PA` (Pericope Adulterae)",
            "and `ACT24` (Acts 24 appendix) sections, which are exported as separate",
            "accented CSV files; the TEI exports are the 27-book main text.",
            "",
            "To rebuild every curated edition from the committed archives,",
            f"`source/`, and git tag {_tag('v2.0.3')}, run these from the repository root",
            "(no network is needed):",
            "",
            "```bash",
            "python3 scripts/fetch_official.py --verify",
            "python3 scripts/recover_editions.py",
            "python3 scripts/build_editions.py",
            "python3 scripts/diff_editions.py",
            "```",
            "",
            "## Successive diffs",
            "",
        ]
    )
    for left, right in (
        ("rp2005", "rp2005-2019"),
        ("rp2005-2019", "rp2018"),
        ("rp2018", "rp2018-2023"),
        ("rp2005", "rp2018"),
    ):
        lines.append(
            f"- `{left}` -> `{right}` ({_diff_dir(left, right)})"
        )
    lines.extend(
        [
            "",
            "Each directory contains:",
            "",
            "- `report.md` - Unicode-first human-readable report.",
            "  `Main-text changes` lists the verses whose normalised Unicode text",
            "  changes, with the Text word diff (`[-removed-]{+added+}`, in the",
            "  style of `git diff --word-diff`) first and the Beta-code Source",
            "  second. `Apparatus-only changes` compacts the remaining",
            "  source-tier differences into one entry per verse, showing the",
            "  Unicode apparatus word diff first and the Beta-code diff second;",
            "  an entry whose only change is Beta-code encoding says so instead of",
            "  printing an empty diff. The Text diff is",
            "  normalised: paragraph markers (`\u00b6`), apostrophe typography,",
            "  and whitespace are omitted.",
            "- `changes.csv` - machine-readable rows with the category, the",
            "  Beta-code source word diff, the Unicode Text and Apparatus word",
            "  diffs, the full source/text left and right, and the",
            "  `text_changed` and `apparatus_changed` flags. The word diffs are",
            "  normalised; `text_left`/`text_right` are exact.",
            "- `source.diff` - word-diff style, one line per verse, for the",
            "  Beta-code source tier.",
            "- `text.diff` - the same word-diff view for the exact derived",
            "  Unicode accented main text (`csv/accented/no-variants`). It",
            "  includes formatting-only changes such as a `\u00b6` edit;",
            "  paragraph markers and apostrophes are shown as stored.",
            "- `apparatus.diff` - the word diff of the normalised Unicode",
            "  accented text with variants (`csv/accented/with-variants`) for",
            "  every apparatus-only change that has a Unicode difference",
            "  (encoding-only rows are named in `report.md`). Variant readings",
            "  stay inside `{...}` braces, and the braces are literal text",
            "  inside the diff markers. `source.diff` is the Beta-code view of",
            "  the same verses.",
            "- `derived.diff` - the word diff of the normalised Unicode main",
            "  text for every differing verse.",
            "",
        ]
    )
    lines.extend(diff.derived_only_lines())
    lines.extend(
        [
            "",
            "The `.diff` files are word-diff style, with one",
            "`@@ BOOK CHAPTER:VERSE [category] @@` hunk and one marked line per",
            "verse, not patchable line-based diffs: they have no line ranges and",
            "no `-`/`+` whole-verse lines.",
            "",
            "**Source** is the edition's Beta-code source tier: the official",
            "`.CCT` archive for `rp2005`/`rp2018`, the recovered",
            "`textonly-beta-code` for `rp2005-2019`, and `source/CCAT` for",
            "`rp2018-2023`. **Text** is the derived Unicode accented main text.",
            "**Apparatus** is the Unicode accented text with variants, from",
            "`editions/<id>/csv/accented/with-variants/`.",
            "",
            "`[-removed-]{+added+}` wraps changed words; unchanged text is",
            "context. Beta-code apparatus braces (`{N ... }`) remain part of the",
            "source text. In the Unicode apparatus the same reading sits inside",
            "literal `{...}` braces, so an added variant renders as",
            "`{+{Byz \u03c4\u03b5 > \u03b4\u03b5 }+}`: the outer markers are the diff and the inner",
            "braces are the reading.",
            "",
            "The marker delimiters are the fixed strings `[-`, `-]`, `{+`, `+}`;",
            "a literal `-` or `>` next to a delimiter is part of the text (for",
            "example, a dash-spacing change can render as",
            "`[-εἶπεν --]{+εἶπεν-+}`).",
            "",
            "`@@ BOOK CHAPTER:VERSE [category] @@` opens a verse",
            "hunk.",
            "Text comparison removes paragraph markers (`\u00b6`), maps curly",
            "apostrophes (`\u2019`/`\u2018`) to `'`, and collapses whitespace; the",
            "word-diff shown omits those conventions. The exact text is in",
            "`changes.csv` (`text_left`/`text_right`) and `text.diff`.",
            "`reports/diffs/README.md` is generated by the same script.",
            "",
            "## Source of truth",
            "",
            "If a PDF, an archive, and the curated source disagree, the PDF wins and",
            "the conflict is recorded for the maintainer instead of being resolved",
            "automatically.",
            "",
        ]
    )
    path = editions.DOCS_DIR / "EDITIONS.md"
    generated.write_markdown(path, "\n".join(lines))
    return str(path)


def _release_cell(row: dict) -> str:
    # The root README keeps plain tags: docs/EDITIONS.md is the linked reference.
    if row.get("release_range"):
        return f"`{row.get('first_release')}`-`{row.get('latest_release')}`"
    return "none"


def root_readme_block() -> list:
    """The generated `<!-- editions:begin -->` block for the root README."""
    manifests = {row["edition"]: row for row in _manifests()}
    block = [BEGIN]
    block.extend(generated.block_banner("python3 scripts/build_editions.py"))
    block.extend(
        [
            "",
            "## Curated editions",
            "",
            "Four editions are curated under [`editions/`](editions/), each with its",
            "own `source/`, `csv/`, `tei/`, `manifest.json`, and `README.md`.",
            "`rp2018-2023` is the current text, `rp2018` and `rp2005` are the official",
            "print editions, and `rp2005-2019` is the historical 2019 revision of the",
            "2005 lineage.",
            "",
            "| Edition | Status | Repo releases |",
            "| --- | --- | --- |",
        ]
    )
    for edition_id in editions.EDITIONS:
        row = manifests.get(edition_id, {})
        block.append(
            f"| `{edition_id}` | {row.get('status', '')} | {_release_cell(row)} |"
        )
    block.extend(
        [
            "",
            "See [`docs/EDITIONS.md`](docs/EDITIONS.md) and the",
            "[`editions/`](editions/) directory for the full explanation, PDF",
            "links, provenance, manifests, and checksums.",
            "",
            "## Generated files",
            "",
            "| Generated path | Regenerate with |",
            "| --- | --- |",
        ]
    )
    for row in generated.GENERATED_FILES:
        block.append(f"| {row['label']} | {row['command']} |")
    block.extend(
        [
            "",
            "Do not edit any file in this table by hand; the next run overwrites",
            "it. The rest of this README is hand-written.",
            "`data/provenance/pdfs.toml` is hand-maintained and is **not**",
            "generated.",
            "",
            END,
        ]
    )
    return block


def replace_block(text: str, block: str) -> str:
    """Replace (or append) the generated block without touching the rest."""
    if BEGIN in text and END in text:
        before = text[: text.index(BEGIN)].rstrip()
        after = text[text.index(END) + len(END) :].strip()
        text = before + "\n\n" + block + "\n"
        if after:
            text += "\n" + after + "\n"
        return text
    return text.rstrip() + "\n\n" + block + "\n"


def render_root_readme(text: str) -> str:
    """Return `text` with the generated editions block in place."""
    return replace_block(text, "\n".join(root_readme_block()))


def update_root_readme() -> str:
    path = editions.ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(render_root_readme(text), encoding="utf-8")
    return str(path)
