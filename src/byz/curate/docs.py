"""Generate docs/EDITIONS.md and the root README editions section."""

import json

from . import editions

BEGIN = "<!-- editions:begin -->"
END = "<!-- editions:end -->"


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
        "| Edition | Status | Basis | Repo releases | PDF |",
        "| --- | --- | --- | --- | --- |",
    ]
    for edition_id in editions.EDITIONS:
        row = manifests.get(edition_id, {})
        release = (
            f"`{row.get('first_release')}`-`{row.get('latest_release')}`"
            if row.get("release_range")
            else "none"
        )
        pdf = "none"
        if row.get("pdf"):
            pdf = (
                f"[`{edition_id} PDF`]({row['pdf_url']}) "
                f"(`{row.get('pdf_sha256', '')}`)"
            )
        lines.append(
            f"| `{edition_id}` | {row.get('status', '')} | "
            f"{row.get('basis', '')} | {release} | {pdf} |"
        )
    hist = manifests.get("rp2005-2019", {})
    cur = manifests.get("rp2018-2023", {})
    hist_range = (
        f"`{hist.get('first_release')}`-`{hist.get('latest_release')}`"
        if hist.get("release_range")
        else "none"
    )
    cur_range = (
        f"`{cur.get('first_release')}`-`{cur.get('latest_release')}`"
        if cur.get("release_range")
        else "none"
    )
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
            "| `source/Strongs` | repo lineage, not in the six ZIPs | no | yes | no | yes |",
            "| `textonly-beta-code` (v2.0.3) | repo 2005 lineage, 2019 | yes | no | yes | no |",
            "| `parsed` (v2.0.3) | repo parsed lineage | no | yes | yes | yes |",
            "| `textonly-online-bible` (v2.0.3) | repo 2005 lineage | no | no | no | no |",
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
            "The repo's last pre-2023 text, recovered from tag `v2.0.3`",
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
            "and later minor fixes. It was first released in `v3.0.0` and continues",
            f"to receive releases. Repo releases: {cur_range} (and later tags).",
            "",
            "## Why the history looks messy",
            "",
            "- The 2005 lineage lived in `textonly-beta-code`, `parsed`, and",
            "  `csv-unicode` until 2023. It was last updated in 2019.",
            "- Commit `97371d7` (2023-05-30), merged as `v3.0.0`, switched the repo to",
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
            "  from `v2.0.3`.",
            "- `rp2018-2023`: the same views are copied or generated from the current",
            "  working tree.",
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
            "The byte-frozen `rp2005-2019` edition is the exception. Its",
            "`textonly-beta-code`, `parsed`, accented CSV (both views), unaccented",
            "CSV, and unaccented TEI are recovered byte-identically from `v2.0.3`.",
            "The accented TEI (from the recovered accented CSV) and the Strong's",
            "views (from `parsed`) are generated here, and `v2.0.3` itself has no",
            "accented TEI. The accented CSV (7968 rows), unaccented CSV (7953",
            "rows), and unaccented TEI **omit** the four verses: the rows are",
            "absent and there is no empty `<ab/>`, even though the source files in",
            "that tag do contain the blank verse lines. The generated accented TEI",
            "inherits the omission; the generated Strong's views include the four",
            "verses as empty rows (7957 rows). The recovered artifacts must stay",
            "byte-identical, so the rows are deliberately not added back; the",
            "edition README records the omission.",
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
            "## Known converter quirks",
            "",
            "Apparatus text is not fully preserved. The English notes inside",
            "`[[ ... ]]` are transliterated by the historical converter",
            "(`\"shorter ending\"` becomes `σηορτερ ενδινγ`), and apparatus quotes use",
            "the converter's beta-code diaeresis rendering (`\" ̈\"` for `\"+\"`). Both",
            "are pre-existing converter behaviour and outside the scope of edition",
            "curation; the main text is unaffected.",
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
            "Accented CSV also includes the `PA` and `ACT24` section files where the",
            "source provides them. TEI is the 27-book main text.",
            "",
            "```bash",
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
            f"- `{left}` -> `{right}`: "
            f"`reports/diffs/{left}--{right}/report.md`"
        )
    lines.extend(
        [
            "",
            "Successive diffs compare the **source-tier main text** (official `.CCT`,",
            "historical `textonly-beta-code`, or current `source/CCAT`), not the",
            "generated CSV/TEI views.",
            "",
            "## Source of truth",
            "",
            "If a PDF, an archive, and the curated source disagree, the PDF wins and",
            "the conflict must be flagged to the maintainer. Do not silently choose.",
            "",
        ]
    )
    path = editions.DOCS_DIR / "EDITIONS.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)


def _release_cell(row: dict) -> str:
    if row.get("release_range"):
        return f"`{row.get('first_release')}`-`{row.get('latest_release')}`"
    return "none"


def root_readme_block() -> list:
    """The generated `<!-- editions:begin -->` block for the root README."""
    manifests = {row["edition"]: row for row in _manifests()}
    block = [
        BEGIN,
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
