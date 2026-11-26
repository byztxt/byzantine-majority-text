"""Shared banner and registry for generated files.

Several packages write Markdown into the repository. This module is the single
place that defines the banner wording, the idempotent insertion helper, and the
list of paths the root README documents. It imports only the standard library
so `byz.curate`, `byz.contract`, and `byz.reconcile` can all depend on it
without a cycle.

The marker comment is deliberately stable: it makes insertion idempotent and
gives the tests a fixed string to look for. The visible blockquote below it is
what a reader sees on GitHub. The banner names no command and no relative link,
because the same banner is used at three different directory depths; the
registry below is the authoritative command list.

The root README is a fully generated file too: its prose lives in the template
`src/byz/curate/README.template.md`, which the build renders.
"""

from pathlib import Path

MARKDOWN_MARKER = "<!-- generated-file: do not edit by hand -->"
TOML_MARKER = "# generated-file: do not edit by hand"

MARKDOWN_BANNER = (
    MARKDOWN_MARKER,
    "> **Generated file. Do not edit by hand.**",
    '> See the "Generated files" section of the repository README for the command',
    "> that regenerates it.",
)

TOML_BANNER = (
    TOML_MARKER,
    '# See the "Generated files" section of the repository README for the command',
    "# that regenerates it.",
)

# Every generated Markdown file, relative to the repository root. Globs are
# expanded by the tests: `editions/*/README.md` is four files and
# `reports/diffs/*/report.md` is four, so the twenty patterns cover
# twenty-six files. `data/raw/repo/CONVENTIONS.md` is hand-maintained and is
# listed in `HAND_MAINTAINED_DOCS` instead.
GENERATED_MARKDOWN = (
    "README.md",
    "data/README.md",
    "data/raw/README.md",
    "data/raw/print/README.md",
    "data/raw/repo/README.md",
    "data/raw/print/rp2005/README.md",
    "data/raw/print/rp2018/README.md",
    "data/raw/repo/rp2005-2019/README.md",
    "data/raw/repo/rp2018-2023/README.md",
    "docs/EDITIONS.md",
    "docs/HISTORY.md",
    "docs/DATA_CONTRACT.md",
    "docs/PROVENANCE.md",
    "editions/*/README.md",
    "reports/baseline/summary.md",
    "reports/baseline/decision-log.md",
    "reports/reconciliation/summary.md",
    "reports/reconciliation/decision-log.md",
    "reports/diffs/README.md",
    "reports/diffs/*/report.md",
)

# Hand-maintained files that live next to generated ones. In particular
# `data/provenance/pdfs.toml` is written by no script and must never receive a
# banner or be listed as generated. The root README is generated from the
# template listed here; edit the template, never the rendered file.
HAND_MAINTAINED = (
    "data/provenance/pdfs.toml",
    "src/byz/curate/README.template.md",
    "SPECS/*.md",
    "data/raw/repo/CONVENTIONS.md",
    "docs/BUILD.md",
    "essay/README.md",
    "docs/COLLATEX.md",
)

# The hand-written Markdown files under `docs/`. The generated-file
# classification test treats the rest of `docs/` as generated, so these are
# listed explicitly instead of relaxing the test.
HAND_MAINTAINED_DOCS = (
    "data/raw/repo/CONVENTIONS.md",
    "docs/BUILD.md",
    "docs/COLLATEX.md",
)

# One row per generated artifact family, rendered as the `## Generated files`
# table in the root README. `patterns` is used by the classification tests, so
# the table and the banner scope cannot disagree.
GENERATED_FILES = (
    {
        "label": "`docs/EDITIONS.md`",
        "command": "`PYTHONPATH=src python3 -m byz.build`",
        "patterns": ("docs/EDITIONS.md",),
    },
    {
        "label": (
            "`data/raw/repo/rp2005-2019/`, "
            "`data/provenance/rp2005-2019.toml`"
        ),
        "command": "`PYTHONPATH=src python3 -m byz.materialise`",
        "patterns": (
            "data/raw/repo/rp2005-2019/textonly-beta-code/**",
            "data/raw/repo/rp2005-2019/parsed/**",
            "data/provenance/rp2005-2019.toml",
        ),
    },
    {
        "label": (
            "`data/README.md`, `data/raw/README.md`, "
            "`data/raw/print/README.md`, `data/raw/repo/README.md`, "
            "`data/raw/print/<edition>/README.md`, "
            "`data/raw/repo/<edition>/README.md`, "
            "`data/provenance/rp2018-2023.toml`"
        ),
        "command": "`PYTHONPATH=src python3 -m byz.build`",
        "patterns": (
            "data/README.md",
            "data/raw/README.md",
            "data/raw/print/README.md",
            "data/raw/repo/README.md",
            "data/raw/print/rp2005/README.md",
            "data/raw/print/rp2018/README.md",
            "data/raw/repo/rp2005-2019/README.md",
            "data/raw/repo/rp2018-2023/README.md",
            "data/provenance/rp2018-2023.toml",
        ),
    },
    {
        "label": "`editions/<edition>/README.md`",
        "command": "`PYTHONPATH=src python3 -m byz.build`",
        "patterns": ("editions/*/README.md",),
    },
    {
        "label": "`editions/<edition>/manifest.json`, `csv/`, `tei/`",
        "command": "`PYTHONPATH=src python3 -m byz.build`",
        "patterns": (
            "editions/*/manifest.json",
            "editions/*/csv/**",
            "editions/*/tei/**",
        ),
    },
    {
        "label": "`README.md`",
        "command": "`PYTHONPATH=src python3 -m byz.build`",
        "patterns": ("README.md",),
    },
    {
        "label": (
            "`reports/diffs/README.md`, "
            "`reports/diffs/<left>--<right>/report.md`"
        ),
        "command": "`PYTHONPATH=src python3 -m byz.diff`",
        "patterns": (
            "reports/diffs/README.md",
            "reports/diffs/*/report.md",
        ),
    },
    {
        "label": "`docs/HISTORY.md`",
        "command": (
            "`PYTHONPATH=src python3 -m byz.contract`, then "
            "`PYTHONPATH=src python3 -m byz.reconcile`"
        ),
        "patterns": ("docs/HISTORY.md",),
    },
    {
        "label": "`docs/DATA_CONTRACT.md`",
        "command": "`PYTHONPATH=src python3 -m byz.contract`",
        "patterns": ("docs/DATA_CONTRACT.md",),
    },
    {
        "label": (
            "`docs/contract/*.json`, `reports/baseline/summary.md`, "
            "`reports/baseline/decision-log.md`, `reports/baseline/*.csv`"
        ),
        "command": "`PYTHONPATH=src python3 -m byz.contract`",
        "patterns": (
            "docs/contract/*.json",
            "reports/baseline/*.md",
            "reports/baseline/*.csv",
        ),
    },
    {
        "label": "`docs/PROVENANCE.md`",
        "command": "`PYTHONPATH=src python3 -m byz.reconcile`",
        "patterns": ("docs/PROVENANCE.md",),
    },
    {
        "label": (
            "`reports/reconciliation/summary.md`, "
            "`reports/reconciliation/decision-log.md`, "
            "`reports/reconciliation/*.csv`"
        ),
        "command": "`PYTHONPATH=src python3 -m byz.reconcile`",
        "patterns": (
            "reports/reconciliation/*.md",
            "reports/reconciliation/*.csv",
        ),
    },
    {
        "label": "`data/provenance/rp2005.toml`, `data/provenance/rp2018.toml`",
        "command": (
            "`PYTHONPATH=src python3 -m byz.fetch` (offline re-record) or "
            "`--force` (re-download and re-extract)"
        ),
        "patterns": (
            "data/provenance/rp2005.toml",
            "data/provenance/rp2018.toml",
        ),
    },
)


def markdown(text: str) -> str:
    """Return `text` with exactly one banner prepended.

    A banner previously inserted by this function is removed first, so
    `markdown(markdown(text)) == markdown(text)`. The body is not otherwise
    touched and no trailing newline is added.
    """
    prefix = "\n".join(MARKDOWN_BANNER) + "\n\n"
    if text.startswith(prefix):
        text = text[len(prefix) :]
    return prefix + text


def write_markdown(path, text: str) -> Path:
    """Write generated Markdown with the banner; return the path."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown(text), encoding="utf-8")
    return path


def toml_header() -> list:
    """The banner lines for the generated provenance TOMLs."""
    return list(TOML_BANNER)

