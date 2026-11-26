"""Generate docs/EDITIONS.md and the root README from its template."""

import json
import re

from .. import generated
from . import diff, editions

# The root README is a render of this template. The first line is a note for a
# human editor that the renderer strips, so a reader of the template knows which
# file to change; `update_root_readme()` is the only writer of the rendered file.
TEMPLATE_PATH = (
    editions.ROOT / "src" / "byz" / "curate" / "README.template.md"
)
TEMPLATE_NOTE = (
    "<!-- Template for README.md: edit this file, then run "
    "PYTHONPATH=src python3 -m byz.build. -->"
)
# Each token must appear exactly once, alone on its own line. The renderer
# raises rather than guessing when a template drifts.
TEMPLATE_TOKENS = ("CURATED_EDITIONS", "GENERATED_FILES")

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


# Retired working-tree convenience trees. This is the one authoritative
# old -> new mapping; docs/EDITIONS.md renders it. Nothing else may name
# these paths except `build.py`/`materialise.py`/`history.py` (git pathspecs for tag
# `v2.0.3` history) and the tests that lock the deletion.
RETIRED_PATHS = (
    ("csv-unicode/ccat/no-variants", "editions/rp2018-2023/csv/accented/no-variants"),
    ("csv-unicode/ccat/with-variants", "editions/rp2018-2023/csv/accented/with-variants"),
    ("csv-unicode/strongs/with-parsing", "editions/rp2018-2023/csv/strongs/with-parsing"),
    ("csv-unicode/strongs/no-parsing", "editions/rp2018-2023/csv/unaccented"),
    (
        "csv-unicode/strongs/no-parsing (numbers-only successor)",
        "editions/rp2018-2023/csv/strongs/no-parsing",
    ),
    ("tei-xml-unicode/no-accents", "editions/rp2018-2023/tei/unaccented"),
    ("tei-xml-unicode/no-accents/BYZ/byz.xml", "editions/rp2018-2023/tei/unaccented/BYZ/byz.xml"),
    ("tei-xml-unicode/assets/coll.png", "docs/assets/coll.png"),
    ("tei-xml-unicode/assets/demo_collation.xlsx", "docs/assets/demo_collation.xlsx"),
    ("tei-xml-unicode/assets/demo_john_1.xml", "docs/assets/demo_john_1.xml"),
    ("tei-xml-unicode/README.md (CollateX walkthrough)", "docs/COLLATEX.md"),
    ("csv-unicode/README.md (multi-parsing note)", "docs/EDITIONS.md; data/raw/repo/CONVENTIONS.md"),
)

# Rows whose left-hand side is a note about a retired path rather than a path
# itself. They render as plain text so no reader mistakes the parenthetical for
# part of a real path.
RETIRED_NON_PATHS = frozenset(
    {
        "csv-unicode/strongs/no-parsing (numbers-only successor)",
        "tei-xml-unicode/README.md (CollateX walkthrough)",
        "csv-unicode/README.md (multi-parsing note)",
    }
)


def _now_cell(new: str) -> str:
    """Render one or more `;`-separated targets as separate code spans."""
    return " and ".join(f"`{target.strip()}`" for target in new.split(";"))


# Where the code and inputs moved. This is a second old -> new mapping;
# `RETIRED_PATHS` above records the earlier removal of the convenience trees.
# Apart from the MAR 16:8 apparatus-literal correction (described in the
# "Apparatus literals" section), the bytes and hashes did not change: only the
# paths and the commands did.
#
# Each row carries an explicit `code` flag that controls only the left-hand
# cell: True renders it as a code span (a path or command), False renders plain
# prose (the final row, which describes the retired README body rather than
# naming a path). The right-hand cell is always a code span, because it always
# names a destination path or command. The right-hand column of the last row
# names the template rather than the rendered README, because that is where the
# prose is now edited.
MOVED_PATHS = (
    (
        "python3 scripts/fetch_official.py [--verify or --force]",
        "PYTHONPATH=src python3 -m byz.fetch [--verify or --force]",
        True,
    ),
    (
        "python3 scripts/recover_editions.py",
        "PYTHONPATH=src python3 -m byz.materialise",
        True,
    ),
    (
        "python3 scripts/build_editions.py",
        "PYTHONPATH=src python3 -m byz.build",
        True,
    ),
    (
        "python3 scripts/diff_editions.py",
        "PYTHONPATH=src python3 -m byz.diff",
        True,
    ),
    ("scripts/requirements.txt", "requirements.txt (repository root)", True),
    ("scripts/README.md", "docs/BUILD.md", True),
    ("scripts/beta_to_unicode_custom/", "src/byz/beta/", True),
    ("scripts/tei_xml_header.xml", "src/byz/curate/tei_xml_header.xml", True),
    ("source/CCAT", "data/raw/repo/rp2018-2023/ccat", True),
    ("source/Strongs", "data/raw/repo/rp2018-2023/strongs", True),
    ("source/README.md", "data/raw/repo/CONVENTIONS.md", True),
    (
        "the hand-written README body and its editions block",
        "src/byz/curate/README.template.md",
        False,
    ),
)


# Where the snapshots moved on 2026-11-25: each per-edition `source/` copy was
# deleted and its bytes are read from `data/` instead. `byz.verify` checks the
# manifest against those inputs. `rp2005-2019` is the one edition whose views
# were also regenerated: its 57 source files are inputs like any other, and the
# build no longer copies the `v2.0.3` release's CSV/TEI.
SNAPSHOT_MOVES = (
    (
        "editions/rp2005/source/ccat/",
        "data/raw/print/rp2005/ccat/",
    ),
    (
        "editions/rp2018/source/ccat/",
        "data/raw/print/rp2018/ccat/",
    ),
    (
        "editions/rp2018-2023/source/",
        "data/raw/repo/rp2018-2023/",
    ),
    (
        "editions/rp2005-2019/source/",
        "data/raw/repo/rp2005-2019/",
    ),
    (
        "manifest.json source_files",
        "manifest.json inputs",
    ),
)

# Where the inputs moved into the two source classes on 2026-11-25. The bytes
# and hashes did not change: this is a layout change only, so every row maps a
# retired input tree to its new home under `data/raw/print/` (published print
# editions) or `data/raw/repo/` (this repository's lineage). The last two rows
# are the consequences outside `data/raw/`: the hand-maintained `pdfs.toml`
# paths and the manifests' `pdf` key gain the `print/` segment. No compatibility
# shim, symlink, or stub exists for any retired path.
INPUT_CLASS_MOVES = (
    ("data/text/CCAT/", "data/raw/repo/rp2018-2023/ccat/"),
    ("data/text/Strongs/", "data/raw/repo/rp2018-2023/strongs/"),
    ("data/text/README.md", "data/raw/repo/CONVENTIONS.md"),
    (
        "data/raw/rp2005/editions-rp2-ccat/",
        "data/raw/print/rp2005/ccat/",
    ),
    (
        "data/raw/rp2005/editions-rp2-ascii/",
        "data/raw/print/rp2005/ascii/",
    ),
    (
        "data/raw/rp2005/editions-rp2-preformatted/",
        "data/raw/print/rp2005/preformatted/",
    ),
    (
        "data/raw/rp2005/official-pdf/",
        "data/raw/print/rp2005/official-pdf/",
    ),
    ("data/raw/rp2018/rp2018-ccat/", "data/raw/print/rp2018/ccat/"),
    (
        "data/raw/rp2018/rp2018-ascii-one-line-per-verse/",
        "data/raw/print/rp2018/ascii/",
    ),
    (
        "data/raw/rp2018/rp2018-ascii/",
        "data/raw/print/rp2018/preformatted/",
    ),
    (
        "data/raw/rp2018/official-pdf/",
        "data/raw/print/rp2018/official-pdf/",
    ),
    ("data/raw/_archives/", "data/raw/print/_archives/"),
    ("data/raw/rp2005-2019/", "data/raw/repo/rp2005-2019/"),
    (
        "data/provenance/pdfs.toml path",
        "data/raw/print/<edition>/official-pdf/",
    ),
    (
        "manifest pdf key",
        "data/raw/print/<edition>/official-pdf/",
    ),
)

# The released `v2.0.3` CSV/TEI are not inputs and are not used by the build.
# They remain evidence of what the 2019 converter produced; the edition is
# regenerated from the 57 source files by the current pipeline. This table maps
# each released-artifact prefix to the regenerated view, so the recovery stays
# auditable without treating those files as inputs.
RELEASED_ARTIFACT_MOVES = (
    (
        "csv-unicode/accents/no-variants/",
        "editions/rp2005-2019/csv/accented/no-variants/",
    ),
    (
        "csv-unicode/accents/with-variants/",
        "editions/rp2005-2019/csv/accented/with-variants/",
    ),
    (
        "csv-unicode/no-accents/",
        "editions/rp2005-2019/csv/unaccented/",
    ),
    (
        "tei-xml-unicode/no-accents/",
        "editions/rp2005-2019/tei/unaccented/",
    ),
)


def _moved_cell(text: str, code: bool) -> str:
    """Render a moved path/command as code, or prose as plain text.

    A trailing parenthetical stays prose because it qualifies the destination
    rather than forming part of the path: ``requirements.txt (repository
    root)`` renders as `` `requirements.txt` (repository root) ``.
    """
    if not code:
        return text
    destination, separator, note = text.partition(" (")
    if separator:
        return f"`{destination}` ({note}"
    return f"`{text}`"


def _retired_cell(old: str) -> str:
    """Render a retired path as a code span, or a note as plain text."""
    return old if old in RETIRED_NON_PATHS else f"`{old}`"


def _manifests() -> list:
    rows = []
    for edition_id in editions.EDITIONS:
        path = editions.edition_dir(edition_id) / "manifest.json"
        if not path.is_file():
            # A missing manifest means the build has not run: rendering the
            # docs from a partial set would silently publish an incomplete
            # edition table.
            raise ValueError(f"missing edition manifest: {path}")
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
        "`data/raw/repo/rp2018-2023/` are the authoritative machine-readable text for the",
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
        "## Where the edition snapshots went (2026-11-25)",
        "",
        "Each edition used to carry a frozen copy of its inputs under `source/`.",
        "That copy was removed on 2026-11-25: every input now lives under `data/`,",
        "and `manifest.json` pins it by repository-relative path and SHA-256. An",
        "edition is outputs only (`csv/`, `tei/`, `manifest.json`, `README.md`).",
        "No `editions/<edition>/source/` directory remains.",
        "`byz.verify` (run as `PYTHONPATH=src python3 -m byz.verify`) checks the",
        "inputs against `data/` and the artifacts against the edition.",
        "",
        "| Retired snapshot | Now |",
        "| --- | --- |",
    ]
    retired_section += [
        f"| `{old}` | `{new}` |" for old, new in SNAPSHOT_MOVES
    ]
    retired_section += [
        "",
        "The revision releasing this change replaces `source_files` with",
        "`inputs`; `artifact_files` is unchanged for the three editions whose",
        "text does not change. A manifest that still has `source_files`, or",
        "lacks `inputs`, is invalid, and no input root may point under",
        "`editions/`.",
        "",
        f"Only two {_tag('v2.0.3')} prefixes are inputs: the 57",
        "`textonly-beta-code` and `parsed` files committed at",
        "`data/raw/repo/rp2005-2019/`. Only `byz.materialise` extracts the tag's",
        "files into `data/`; the build reads `data/` only. (`byz.reconcile`",
        "reads the tag with `git show` for historical comparison, and",
        "`byz.build` lists tags for the release ranges, but neither uses the",
        "tag's files as build inputs.)",
        "`rp2005-2019` is **regenerated** from those sources by the same pipeline",
        "as the other editions. Its released CSV/TEI are evidence of the 2019",
        "converter's output, not what this repository publishes: regeneration",
        "corrects the malformed apparatus codes (`{Ν`/`{Β` become",
        "`{NA`/`{Byz`) and normalises typography, without changing the main",
        "text's words.",
        "",
        f"The released-artifact prefixes of {_tag('v2.0.3')} map to the",
        "regenerated views as follows. Those outputs are now **regenerated**",
        "from the same tag's 57 sources, so they are not byte-identical to the",
        "release: the apparatus codes and the typography differ.",
        "",
        f"| Released {_tag('v2.0.3')} prefix | Regenerated view |",
        "| --- | --- |",
    ]
    retired_section += [
        f"| `{old}` | `{new}` |" for old, new in RELEASED_ARTIFACT_MOVES
    ]
    retired_section += [
        "",
        "See [`COLLATEX.md`](COLLATEX.md) for using the unaccented TEI with",
        "CollateX.",
        "",
        "## Where the inputs moved into the print and repo classes (2026-11-25)",
        "",
        "`data/raw/` has two source classes. `data/raw/print/` holds material",
        "from the published print editions, including the six committed ZIP",
        "archives; `data/raw/repo/` holds this repository's own lineage. Every",
        "input tree belongs to exactly one class, and each source folder is named",
        "after its edition id directly under its class.",
        "",
        "The current text stopped being a special case: `data/text/` no longer",
        "exists, and `data/raw/repo/rp2018-2023/{ccat,strongs}/` is a source",
        "snapshot like the 2019 lineage. The Beta-code, variant, parsing, and",
        "Strong's conventions moved to the hand-maintained",
        "`data/raw/repo/CONVENTIONS.md`, inside the repo class.",
        "",
        "| Retired input path | Now |",
        "| --- | --- |",
    ]
    retired_section += [
        f"| `{old}` | `{new}` |" for old, new in INPUT_CLASS_MOVES
    ]
    retired_section += [
        "",
        "Only the paths changed: every source byte and SHA-256 is unchanged, and",
        "all 672 edition CSV/TEI artifacts keep their `artifact_files` hashes.",
        "The two official `pdf` values in the manifests and in",
        "`data/provenance/pdfs.toml` gained the `print/` segment so the hand-",
        "maintained record and the generated manifest cannot disagree.",
        "These paths are not aliased: no symlink, stub README, `.gitkeep`, or",
        "duplicate tree exists, so a retired path simply fails.",
        "",
        "## Where the old working-tree paths went",
        "",
        "Earlier releases published the current text as `csv-unicode/` and",
        "`tei-xml-unicode/`. Those paths are not present here; this table maps",
        "them to the curated editions. The retired paths return 404 by",
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
        "Those `csv-unicode/` and `tei-xml-unicode/` views were the previous",
        "release's `rp2018-2023` files. The retired `strongs/no-parsing` bytes",
        "were plain unaccented text, so they now live in `csv/unaccented/`; the",
        "current `csv/strongs/no-parsing/` is the new numbers-only view and is",
        "not byte-identical to the retired path. The 2026-11-21 move kept every",
        "`artifact_files` hash, the 2026-11-25 change replaced `source_files`",
        "with `inputs`, and the 2026-11-26 review fix changed 54 numbers-only",
        "CSVs (27 per released edition) plus the two unaccented-TEI book titles.",
        "The retired `strongs/no-parsing` bytes still match `csv/unaccented/`;",
        "the retired unaccented TEI matches `tei/unaccented/` except for the two",
        "corrected titles.",
        "",
        "## Where the code and inputs moved",
        "",
        "Earlier releases ran `scripts/*.py` and kept the inputs under",
        "`source/`. Those paths are not present here; this table maps them to",
        "the current layout. There are no shims, symlinks, or redirect files:",
        "an old path or command fails.",
        "",
        "| Old path or command | Now |",
        "| --- | --- |",
    ]
    retired_section += [
        f"| {_moved_cell(old, code)} | {_moved_cell(new, True)} |"
        for old, new, code in MOVED_PATHS
    ]
    retired_section += [
        "",
        "The 2026-11-21 move changed only the paths and the commands; every",
        "`artifact_files` hash stayed the same. The 2026-11-25 change replaced",
        "`source_files` with `inputs` and regenerated `rp2005-2019` from its",
        "committed sources, so that edition's artifact hashes changed (the other",
        "three did not). Three metadata keys also changed (`generated_by`,",
        "`source_commit`, and `strongs_commit`), because they name the command",
        "and the git pathspecs that produce them. The `data/text/` targets in",
        "that table were themselves moved on 2026-11-25 into the repository",
        "source class, as the section",
        "*Where the inputs moved into the print and repo classes (2026-11-25)*",
        "below records.",
        "",
        "See [Apparatus literals](#apparatus-literals) for the historical",
        "converter's damaged notes and how the regenerated edition avoids them.",
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
            "| `data/raw/repo/rp2018-2023/ccat` | repo 2018+2023 | yes | no | yes | no |",
            "| `data/raw/repo/rp2018-2023/strongs` | official files, not in the six ZIPs | no | yes | no | yes |",
            "| `textonly-beta-code` (2019 sources) | `data/raw/repo/rp2005-2019/` | yes | no | yes | no |",
            "| `parsed` (2019 sources) | `data/raw/repo/rp2005-2019/` | no | yes | yes | yes |",
            "",
            "The `textonly-beta-code` and `parsed` sources are committed at",
            "`data/raw/repo/rp2005-2019/`, with `data/provenance/rp2005-2019.toml`",
            f"recording tag {_tag('v2.0.3')}, its commit, and every file hash.",
            "`byz.materialise` restores that tree from the tag. The tag's released",
            "CSV/TEI are not inputs and are not used by the build.",
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
            "The repo's last pre-2023 text. Its 2019 `textonly-beta-code` and",
            "`parsed` sources are committed at `data/raw/repo/rp2005-2019/`, and every",
            "view is regenerated from them by the current pipeline. It was updated",
            "in 2019 and is not the official 2005 print edition. It matches the",
            "official 2018 archive in",
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
            "Per-release change notes live in the repository's",
            f"[GitHub releases]({REPO_URL}/releases); this page describes the",
            "editions themselves.",
            "",
            "## Layout, exports, and verification",
            "",
            "Each edition has `csv/`, `tei/`, `manifest.json`, and `README.md`.",
            "The edition contains outputs only: its inputs live under `data/` and",
            "are pinned in the manifest's `inputs` list by repository-relative",
            "path and SHA-256. `PYTHONPATH=src python3 -m byz.verify` checks the",
            "inputs against `data/` and the artifacts against the edition; a",
            "downloaded edition can be checked for artifact integrity with",
            "`--edition-dir`. An edition can no longer verify its own inputs:",
            "`--edition-dir` checks the shipped artifacts only and cannot prove",
            "they came from the pinned inputs.",
            "",
            "- Official editions: accented CSV (with/without variants) and accented",
            "  TEI are generated from the official `.CCT`; unaccented CSV/TEI are",
            "  generated from the official ASCII. Strong's/parsing are absent because",
            "  the official URL files do not contain them.",
            "- `rp2005-2019`: accented with/without variants, unaccented,",
            "  Strong's with/no parsing, and accented/unaccented TEI are generated",
            "  from the 2019 sources committed at `data/raw/repo/rp2005-2019/`. Word",
            "  spacing in the unaccented view follows the parsed source.",
            "- `rp2018-2023`: every view is generated from the committed",
            "  `data/raw/repo/rp2018-2023/` inputs.",
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
            "`rp2005-2019` now behaves the same way as well. Its 2019 sources",
            "contain the four blank verse lines, and regeneration by the current",
            "pipeline emits explicit empty records: 7972 accented CSV rows, 7957",
            "unaccented/Strong's CSV rows, and empty `<ab/>` elements in both TEI",
            f"views. The artifacts released as {_tag('v2.0.3')} omitted the four rows; that",
            "omission is not reproduced.",
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
            "`rp2018` show `[[ \"shorter ending\" ]]` from the official `.CCT`",
            "archives, `rp2018-2023` shows `[[\"SHORTER ENDING\"]]` because",
            "`data/raw/repo/rp2018-2023/ccat` is upper-case with no spaces inside the brackets,",
            "and `rp2005-2019` takes the literal from its 2019 source.",
            "",
            "Before the fix the historical converter transliterated the notes",
            "(`σηορτερ ενδινγ`) and rendered `\"+\"` as `\" ̈\"`. The artifacts",
            f"released as {_tag('v2.0.3')} still carry that damage; this repository",
            "regenerates `rp2005-2019` from the sources, so the published view",
            "needs no post-correction.",
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
            "In `rp2018-2023` and `rp2005-2019`, `csv/unaccented/` is the plain",
            "unaccented text with no Strong's numbers and no parsing.",
            "`csv/strongs/no-parsing/` keeps the Strong's numbers and drops the",
            "`{...}` morphology, and `csv/strongs/with-parsing/` keeps both. The",
            "unaccented TEI is generated from `csv/unaccented/`. The plain-text",
            "and numbers-only views were byte-identical aliases before the",
            "2026-11-26 review fix; they are distinct now.",
            "",
            "### Book titles",
            "",
            "Every TEI book title uses `editions.BOOK_NAMES`, so `2TI` is",
            "`Second Timothy` and `PHP` is `Philippians` in both the accented",
            "and unaccented views. Two earlier spellings (`Second Timoty` and",
            "`Phillipians`) were inherited from the retired convenience pipeline",
            "and corrected on 2026-11-26.",
            "",
            "### Multi-parsing words",
            "",
            "In the `csv/strongs/with-parsing/` view a word may be followed by two",
            "sets of Strong's number and parsing code. These are alternative",
            "parsings of the same word (for example, a neuter form that can be",
            "either nominative or accusative), not two separate words; either",
            "parsing is applicable. `csv/strongs/no-parsing/` keeps each distinct",
            "alternative number but collapses consecutive identical numbers for",
            "one word (for example, `το 3588 3588` becomes `το 3588`, while",
            "2TI 2:6 `πρωτον 4412 4413` keeps both numbers). The convention is",
            "explained in `data/raw/repo/CONVENTIONS.md`.",
            "",
            "### Rebuilding the curated editions",
            "",
            "The official `.CCT` archives also contain the `PA` (Pericope Adulterae)",
            "and `ACT24` (Acts 24 appendix) sections, which are exported as separate",
            "accented CSV files; the TEI exports are the 27-book main text.",
            "",
            "To rebuild every curated edition from the committed `data/` inputs,",
            "run these from the repository root (no network is needed):",
            "",
            "```bash",
            "PYTHONPATH=src python3 -m byz.fetch --verify",
            "PYTHONPATH=src python3 -m byz.build",
            "PYTHONPATH=src python3 -m byz.diff",
            "PYTHONPATH=src python3 -m byz.verify",
            "```",
            "",
            "`byz.materialise` is an ingest command, not part of this rebuild: run",
            f"it only to restore `data/raw/repo/rp2005-2019/` from tag {_tag('v2.0.3')} when that",
            "tree is missing.",
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
            "Category names, with worked examples (including the `variant` vs",
            "`apparatus-code` distinction), are defined in",
            "[`reports/diffs/README.md`](../reports/diffs/README.md#categories).",
            "",
            "The `.diff` files are word-diff style, with one",
            "`@@ BOOK CHAPTER:VERSE [category] @@` hunk and one marked line per",
            "verse, not patchable line-based diffs: they have no line ranges and",
            "no `-`/`+` whole-verse lines.",
            "",
            "**Source** is the edition's Beta-code source tier: the official",
            "`.CCT` archive for `rp2005`/`rp2018`, the 2019",
            "`textonly-beta-code` sources at `data/raw/repo/rp2005-2019/` for",
            "`rp2005-2019`, and `data/raw/repo/rp2018-2023/ccat` for `rp2018-2023`.",
            "**Text** is the derived Unicode accented main text.",
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


def _curated_editions_section() -> list:
    """The `## Curated editions` section, rendered from the manifests."""
    manifests = {row["edition"]: row for row in _manifests()}
    section = [
        "## Curated editions",
        "",
        "Four editions are curated under [`editions/`](editions/), each with its",
        "own generated `csv/`, `tei/`, `manifest.json`, and `README.md`. Every",
        "edition is outputs only; its inputs live under `data/` and are pinned in",
        "the manifest. `rp2018-2023` is the current text, `rp2018` and `rp2005` are",
        "the official print editions, and `rp2005-2019` is the historical 2019",
        "revision of the 2005 lineage.",
        "",
        "| Edition | Status | Repo releases |",
        "| --- | --- | --- |",
    ]
    for edition_id in editions.EDITIONS:
        row = manifests.get(edition_id, {})
        section.append(
            f"| `{edition_id}` | {row.get('status', '')} | {_release_cell(row)} |"
        )
    section.extend(
        [
            "",
            "See [`docs/EDITIONS.md`](docs/EDITIONS.md) and the",
            "[`editions/`](editions/) directory for the full explanation, PDF",
            "links, provenance, manifests, and checksums.",
        ]
    )
    return section


def _generated_files_section() -> list:
    """The `## Generated files` section, rendered from the registry."""
    section = [
        "## Generated files",
        "",
        "| Generated path | Regenerate with |",
        "| --- | --- |",
    ]
    for row in generated.GENERATED_FILES:
        section.append(f"| {row['label']} | {row['command']} |")
    section.extend(
        [
            "",
            "Do not edit any file in this table by hand; the next run overwrites",
            "it. `data/provenance/pdfs.toml` is hand-maintained and is **not**",
            "generated.",
        ]
    )
    return section


def _sections() -> dict:
    return {
        "CURATED_EDITIONS": _curated_editions_section(),
        "GENERATED_FILES": _generated_files_section(),
    }


def render_root_readme(template: str) -> str:
    """Render the root README body from `template`.

    The template's first line must be `TEMPLATE_NOTE`; it is stripped. Each
    `{{TOKEN}}` must appear exactly once, alone on its own line, and is replaced
    by the matching generated section. The result carries no banner; the writer
    prepends one. Any drift raises `ValueError` naming the file or the token
    rather than producing a half-rendered README.
    """
    lines = template.splitlines()
    if not lines or lines[0] != TEMPLATE_NOTE:
        raise ValueError(
            f"{TEMPLATE_PATH.name}: the first line must be {TEMPLATE_NOTE!r}"
        )
    body = lines[1:]
    # A blank line after the edit note is a readability aid, not part of the
    # rendered body; the banner already separates itself from the title.
    while body and not body[0].strip():
        body.pop(0)

    found = re.findall(r"\{\{([A-Z_]+)\}\}", "\n".join(body))
    unknown = sorted(set(found) - set(TEMPLATE_TOKENS))
    if unknown:
        raise ValueError(
            f"{TEMPLATE_PATH.name}: unknown template token(s): {', '.join(unknown)}"
        )
    for token in TEMPLATE_TOKENS:
        count = found.count(token)
        if count == 0:
            raise ValueError(f"{TEMPLATE_PATH.name}: missing template token {token}")
        if count > 1:
            raise ValueError(f"{TEMPLATE_PATH.name}: duplicate template token {token}")

    sections = _sections()
    rendered = []
    for line in body:
        stripped = line.strip()
        if stripped.startswith("{{") and stripped.endswith("}}"):
            token = stripped[2:-2]
            if token not in sections:
                raise ValueError(
                    f"{TEMPLATE_PATH.name}: unknown template token {token}"
                )
            rendered.extend(sections[token])
        elif "{{" in line or "}}" in line:
            raise ValueError(
                f"{TEMPLATE_PATH.name}: a template token must be alone on its line"
            )
        else:
            rendered.append(line)
    while rendered and not rendered[-1].strip():
        rendered.pop()
    return "\n".join(rendered) + "\n"


def update_root_readme() -> str:
    """Render `README.md` from the template and write it with the banner."""
    path = editions.ROOT / "README.md"
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    generated.write_markdown(path, render_root_readme(template))
    return str(path)
