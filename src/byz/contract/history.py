"""Internal (git-only) history map. No external archives are consulted."""

import subprocess

from . import paths

# Each row is (label, git pathspecs). The retired `csv-unicode` and
# `tei-xml-unicode` pathspecs are git history selectors, not working-tree
# paths: they keep the pre-2026 evidence (2022 TEI, 2023 CSV) visible after the
# curated edition became the only home of those bytes. See
# `SPECS/2026-11-19-retire-legacy-unicode-trees/` decision 9.
DATASETS = [
    ("source/CCAT", ("source/CCAT",)),
    ("source/Strongs", ("source/Strongs",)),
    (
        "editions/rp2018-2023/csv",
        (
            "csv-unicode/ccat",
            "csv-unicode/strongs",
            "editions/rp2018-2023/csv",
        ),
    ),
    (
        "editions/rp2018-2023/tei",
        ("tei-xml-unicode", "editions/rp2018-2023/tei"),
    ),
    ("essay", ("essay",)),
]

# Repository history selectors for the corpus-wide rows. The retired paths are
# included so the June-September 2023 evidence does not disappear.
CORPUS_PATHSPECS = (
    "source",
    "csv-unicode",
    "tei-xml-unicode",
    "editions",
    "essay",
)


def _fmt(value):
    if not value:
        return "unknown"
    parts = value.split("|")
    if len(parts) >= 3:
        return f"`{parts[0]}` ({parts[1]}) {parts[2]}"
    return value


def _git(root, args):
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


def _first_add(root, *pathspecs):
    out = _git(
        root,
        ["log", "--diff-filter=A", "--format=%h|%cs|%s", "--", *pathspecs],
    )
    lines = out.splitlines()
    return lines[-1] if lines else ""


def _last_change(root, *pathspecs):
    return _git(
        root, ["log", "-1", "--format=%h|%cs|%s", "--", *pathspecs]
    )


def collect(root=paths.ROOT):
    rows = []
    for label, pathspecs in DATASETS:
        rows.append(
            {
                "dataset": label,
                "first_added": _first_add(root, *pathspecs),
                "last_changed": _last_change(root, *pathspecs),
            }
        )
    return {
        "head": _git(
            root,
            [
                "log",
                "-1",
                "--format=%h|%cs|%s",
                "--",
                *CORPUS_PATHSPECS,
            ],
        ),
        "tags": _git(root, ["tag", "--list"]).splitlines(),
        "datasets": rows,
        "july_2023": _git(
            root,
            [
                "log",
                "--since=2023-06-01",
                "--until=2023-10-01",
                "--format=%h|%cs|%s",
                "--",
                *CORPUS_PATHSPECS,
            ],
        ).splitlines(),
    }


def render(root=paths.ROOT) -> str:
    data = collect(root)
    lines = [
        "# Internal history map",
        "",
        "This map is derived from git history only. It does not prove which "
        "official archive any file came from; that is the job of the external "
        "reconciliation cycle.",
        "",
        "## Last corpus commit",
        "",
        f"{_fmt(data['head'])}",
        "",
        "## Tags",
        "",
    ]
    if data["tags"]:
        lines.extend(f"- `{tag}`" for tag in data["tags"])
    else:
        lines.append("No tags in the repository.")
    lines.extend(
        [
            "",
            # Static text: this is a documented git fact (tag date and commit),
            # not data read from the archives, so it is safe to emit verbatim
            # even when the baseline contract is regenerated offline.
            "`v2016-07-28` is an earlier 2005-lineage snapshot (2017-05-23). It is not",
            "curated as a separate edition: `v2.0.3` is the last pre-2023 release and",
            "supersedes it. The curated `rp2005-2019` source is the `textonly-beta-code`",
            "and `parsed` tree at `v2.0.3` (commit",
            "`8ec95671e463030347c2c643358eb56e58235b19`).",
            "",
            "## Edition mapping (internal evidence)",
            "",
            "| Claim | Evidence |",
            "| --- | --- |",
            "| RP2005 is best approximated by the release 2.0.3 Unicode files | "
            "`README.md` (Versions section); tag `v2.0.3` |",
            "| Release 3.0.0 introduced RP2018 | `README.md` (Versions section); "
            "tags `v3.0.0`..`v3.3.4` |",
            "| The text claims to be up to date as of 2023-07-20 | `README.md`; "
            "commits `16859b2`, `18ea8e9`, `a6d4c1e` (all 2023-07-20) |",
            "",
            "## Dataset history",
            "",
            "| Dataset | First added | Last changed |",
            "| --- | --- | --- |",
        ]
    )
    for row in data["datasets"]:
        lines.append(
            f"| `{row['dataset']}` | {_fmt(row['first_added'])} "
            f"| {_fmt(row['last_changed'])} |"
        )
    lines.extend(
        [
            "",
            "## June-September 2023 commits touching the corpus",
            "",
        ]
    )
    if data["july_2023"]:
        lines.extend(f"- {_fmt(commit)}" for commit in data["july_2023"])
    else:
        lines.append(
            "No commits in this window in the available history, so the "
            "July 20, 2023 update claim cannot be confirmed from git alone."
        )
    lines.extend(
        [
            "",
            "## What this does not establish",
            "",
            "- Which official archive (2005 vs 2018) each source file came from.",
            "- Whether the committed CSV/TEI outputs match the current source.",
            "- Whether the current text is RP2018, RP2018 plus July 2023 fixes, "
            "or a mix.",
            "",
            "These are open questions for the maintainer and the external "
            "reconciliation cycle.",
            "",
        ]
    )
    return "\n".join(lines)
