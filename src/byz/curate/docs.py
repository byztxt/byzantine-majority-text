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
        "the source files here are machine-readable companions.",
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
    lines.extend(
        [
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
            "calling it simply \"2005\" is misleading. Repo releases: `v1.0.0`-`v2.0.3`.",
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
            "to receive releases. Repo releases: `v3.0.0`-`v3.3.4` (and later tags).",
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
            "- Official editions: `csv/` and `tei/` are unaccented main-text exports",
            "  generated from the official ASCII. `source/ccat` holds the official",
            "  `.CCT` source; the PDF is the ultimate source of truth.",
            "- `rp2005-2019`: `csv/main` and `tei/no-accents` are the historical",
            "  released artifacts recovered from `v2.0.3`.",
            "- `rp2018-2023`: `csv/main` and `tei/no-accents` are copied from the",
            "  current working tree (accented CCAT no-variants CSV, unaccented TEI).",
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


def update_root_readme() -> str:
    path = editions.ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    block = [
        BEGIN,
        "## Curated editions",
        "",
        "The repository now ships four curated editions, with their CSV and TEI",
        "exports, instead of asking you to dig through git history:",
        "",
        "| Edition | Status | Repo releases |",
        "| --- | --- | --- |",
        "| `rp2005` | official print 2005 | none |",
        "| `rp2005-2019` | released 2019 revision | `v1.0.0`-`v2.0.3` |",
        "| `rp2018` | official print 2018 | none |",
        "| `rp2018-2023` | released 2018+2023 text | `v3.0.0`-`v3.3.4` |",
        "",
        "See [`docs/EDITIONS.md`](docs/EDITIONS.md) for the full explanation,",
        "PDF links, provenance, and checksums.",
        END,
    ]
    if BEGIN in text and END in text:
        before = text[: text.index(BEGIN)]
        after = text[text.index(END) + len(END) :]
        text = before.rstrip() + "\n\n" + "\n".join(block) + "\n" + after
    else:
        text = text.rstrip() + "\n\n" + "\n".join(block) + "\n"
    path.write_text(text, encoding="utf-8")
    return str(path)
