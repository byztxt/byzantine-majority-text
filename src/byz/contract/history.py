"""Internal (git-only) history map. No external archives are consulted."""

import subprocess

from . import paths

DATASETS = [
    ("source/CCAT", "source/CCAT"),
    ("source/Strongs", "source/Strongs"),
    ("csv-unicode/ccat", "csv-unicode/ccat"),
    ("csv-unicode/strongs", "csv-unicode/strongs"),
    ("tei-xml-unicode", "tei-xml-unicode"),
    ("essay", "essay"),
]


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


def _first_add(root, path):
    out = _git(
        root, ["log", "--diff-filter=A", "--format=%h|%cs|%s", "--", path]
    )
    lines = out.splitlines()
    return lines[-1] if lines else ""


def _last_change(root, path):
    return _git(root, ["log", "-1", "--format=%h|%cs|%s", "--", path])


def collect(root=paths.ROOT):
    rows = []
    for label, path in DATASETS:
        rows.append(
            {
                "dataset": label,
                "first_added": _first_add(root, path),
                "last_changed": _last_change(root, path),
            }
        )
    return {
        "head": _git(root, ["log", "-1", "--format=%h|%cs|%s"]),
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
                "source",
                "csv-unicode",
                "tei-xml-unicode",
                "essay",
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
        "## Current HEAD",
        "",
        f"`{data['head']}`",
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
