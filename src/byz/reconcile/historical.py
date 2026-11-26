"""Compare historical repository tags with the official editions.

This answers the question "which state in git history is 2005, and which is
2018?" without trusting the README alone.
"""

import subprocess

from byz.contract import paths

from . import compare, normalize, sources

# State labels shown in docs/PROVENANCE.md and reports/reconciliation/.
# The historical label names the path as it exists *inside* tag `v3.0.0`; the
# current label names the working-tree path after the 2026-11-21 move. Both
# are single constants so a report lookup cannot drift from the row label.
V3_STATE = "v3.0.0 source/CCAT"
CURRENT_STATE = "current data/raw/repo/rp2018-2023/ccat"

STATE_SPECS = [
    {
        "state": "v2.0.3 textonly-beta-code",
        "tag": "v2.0.3",
        "kind": "textonly",
        "note": "last release before the 2023 update; README calls it the 2005 edition",
    },
    {
        "state": V3_STATE,
        "tag": "v3.0.0",
        "kind": "source",
        "note": "first release with source/CCAT (2023 update)",
    },
]


def _git_show(tag: str, path: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(sources.ROOT), "show", f"{tag}:{path}"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout if result.returncode == 0 else ""


def _load_textonly(tag: str) -> dict:
    rows = {}
    for abbr, code in sources.ABBR_TO_OFFICIAL.items():
        text = _git_show(tag, f"textonly-beta-code/{code}.CCT")
        if text:
            rows[abbr] = normalize.parse_cct(text)
    return rows


def _load_source(tag: str) -> dict:
    # `source/CCAT` is the path inside the tag, which is immutable history.
    rows = {}
    for abbr, num in paths.ABBR_TO_NUM.items():
        text = _git_show(tag, f"source/CCAT/{num}_{abbr}.TXT")
        if text:
            rows[abbr] = normalize.parse_current_ccat(text)
    return rows


def _load_current() -> dict:
    rows = {}
    for path in sorted(paths.CCAT_DIR.glob("*.TXT")):
        num = path.name.split("_", 1)[0]
        abbr = paths.NUM_TO_ABBR.get(num)
        if abbr is None:
            raise ValueError(
                f"current source has an unknown book number: {path.name}"
            )
        rows[abbr] = normalize.parse_current_ccat(
            path.read_text(encoding="utf-8")
        )
    expected = set(paths.CANONICAL_BOOKS) | set(paths.SECTION_ABBRS)
    missing = sorted(expected - set(rows))
    unexpected = sorted(set(rows) - expected)
    if missing or unexpected:
        details = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if unexpected:
            details.append("unexpected " + ", ".join(unexpected))
        raise ValueError(
            "current source does not contain the expected book set: "
            + "; ".join(details)
        )
    return rows


def _load_official(edition: str) -> dict:
    members = compare.ccat_members(edition)
    rows = {}
    for abbr, code in sources.ABBR_TO_OFFICIAL.items():
        text = members.get(f"{code}.CCT")
        if text:
            rows[abbr] = normalize.parse_cct(text)
    return rows


def _compare(state: str, compared_to: str, current: dict, official: dict) -> dict:
    files = 0
    full = 0
    verses = 0
    match = 0
    for abbr in sorted(set(current) & set(official)):
        metrics = compare.compare_maps(current[abbr], official[abbr])
        files += 1
        if metrics["verses_diff"] == 0 and not metrics["only_current"] and not metrics["only_official"]:
            full += 1
        verses += metrics["verses"]
        match += metrics["verses_match"]
    return {
        "state": state,
        "compared_to": compared_to,
        "files": files,
        "full_files": full,
        "verses": verses,
        "match": match,
        "percent": f"{(100.0 * match / verses):.2f}%" if verses else "n/a",
    }


def evidence() -> list:
    official = {
        "rp2005": _load_official("rp2005"),
        "rp2018": _load_official("rp2018"),
    }
    states = {}
    for spec in STATE_SPECS:
        if spec["kind"] == "textonly":
            states[spec["state"]] = _load_textonly(spec["tag"])
        else:
            states[spec["state"]] = _load_source(spec["tag"])
    states[CURRENT_STATE] = _load_current()

    rows = []
    for state, dataset in states.items():
        for edition in ("rp2005", "rp2018"):
            rows.append(_compare(state, edition, dataset, official[edition]))
    return rows
