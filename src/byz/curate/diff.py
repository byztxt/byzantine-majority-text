"""Successive edition diffs."""

import csv
from collections import Counter, defaultdict
from pathlib import Path

from byz.contract import paths
from byz.reconcile import compare, normalize, sources

from . import editions

PAIRS = [
    ("rp2005", "rp2005-2019"),
    ("rp2005-2019", "rp2018"),
    ("rp2018", "rp2018-2023"),
    ("rp2005", "rp2018"),
]


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


def _write_changes(path: Path, rows: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "book",
                "chapter",
                "verse",
                "category",
                "left_text",
                "right_text",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def _report(left_id: str, right_id: str, rows: list, path: Path) -> None:
    left = editions.metadata(left_id)
    right = editions.metadata(right_id)
    categories = Counter(row["category"] for row in rows)
    books = Counter(row["book"] for row in rows)
    lines = [
        f"# Diff: {left_id} -> {right_id}",
        "",
        f"- **Left:** `{left_id}` ({left['status']}; {left['basis']})",
        f"- **Right:** `{right_id}` ({right['status']}; {right['basis']})",
        f"- **Differing verses:** {len(rows)}",
        "",
        "## Categories",
        "",
        "| Category | Count |",
        "| --- | ---: |",
    ]
    for category, count in sorted(categories.items()):
        lines.append(f"| `{category}` | {count} |")
    lines.extend(
        [
            "",
            "## Books",
            "",
            "| Book | Differing verses |",
            "| --- | ---: |",
        ]
    )
    for book, count in sorted(books.items()):
        lines.append(f"| `{book}` | {count} |")
    lines.extend(["", "## Examples", ""])
    for category in sorted(categories):
        examples = [row for row in rows if row["category"] == category][:3]
        lines.append(f"### {category}")
        lines.append("")
        for row in examples:
            lines.append(
                f"- `{row['book']} {row['chapter']}:{row['verse']}`"
            )
            lines.append(f"  - left: `{row['left_text'][:160]}`")
            lines.append(f"  - right: `{row['right_text'][:160]}`")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def diff_pair(left_id: str, right_id: str) -> Path:
    left = load_source(left_id)
    right = load_source(right_id)
    rows = []
    for abbr in sorted(set(left) | set(right)):
        metrics = compare.compare_maps(left.get(abbr, {}), right.get(abbr, {}))
        for difference in metrics["differences"]:
            rows.append(
                {
                    "book": abbr,
                    "chapter": difference["chapter"],
                    "verse": difference["verse"],
                    "category": difference["category"],
                    "left_text": difference["current"],
                    "right_text": difference["official"],
                }
            )
    rows.sort(key=lambda row: (row["book"], row["chapter"], row["verse"]))
    out = editions.DIFFS_DIR / f"{left_id}--{right_id}"
    _write_changes(out / "changes.csv", rows)
    _report(left_id, right_id, rows, out / "report.md")
    return out


def diff_all() -> list:
    return [diff_pair(left, right) for left, right in PAIRS]
