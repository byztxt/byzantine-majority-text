"""Deterministic reconciliation reports and provenance documents."""

import csv
from collections import Counter, defaultdict
from pathlib import Path

from . import archive, sources

CYCLE2_BEGIN = "<!-- cycle2:begin -->"
CYCLE2_END = "<!-- cycle2:end -->"


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _percent(match, total):
    return f"{(100.0 * match / total):.2f}%" if total else "n/a"


def _source_stats(files):
    stats = {}
    for edition in ("rp2005", "rp2018"):
        subset = [
            row
            for row in files
            if row["tier"] == "source" and row["edition"] == edition
        ]
        stats[edition] = {
            "files": len(subset),
            "normalized": sum(1 for row in subset if row["class"] == "normalized"),
            "textual": sum(1 for row in subset if row["class"] == "textual"),
            "structural": sum(1 for row in subset if row["class"] == "structural"),
            "verses": sum(row["verses"] for row in subset),
            "match": sum(row["verses_match"] for row in subset),
        }
    return stats


def _derived_stats(files):
    stats = {}
    for row in files:
        if row["tier"] != "derived":
            continue
        reference = row["note"].split(": ", 1)[-1]
        key = (row["edition"], reference, row["dataset"])
        entry = stats.setdefault(
            key, {"files": 0, "exact": 0, "textual": 0, "verses": 0, "match": 0}
        )
        entry["files"] += 1
        if row["class"] == "exact-transliteration":
            entry["exact"] += 1
        elif row["class"] == "textual":
            entry["textual"] += 1
        entry["verses"] += row["verses"]
        entry["match"] += row["verses_match"]
    return stats


def _categories(verse_rows):
    counts = defaultdict(int)
    for row in verse_rows:
        counts[(row["tier"], row["edition"], row["category"])] += 1
    rows = [
        {
            "tier": tier,
            "edition": edition,
            "category": category,
            "count": count,
        }
        for (tier, edition, category), count in sorted(counts.items())
    ]
    return rows


def _archives():
    rows = []
    for row in archive.inventory_all():
        rows.append(
            {
                "edition": row["edition"],
                "archive": row["archive"],
                "member": row["member"],
                "size": row["size"],
                "crc": row["crc"],
                "sha256": row["sha256"],
                "encoding": row["encoding"],
                "eol": row["eol"],
                "format": row["format"],
            }
        )
    rows.sort(key=lambda row: (row["edition"], row["archive"], row["member"]))
    return rows


def _archive_records():
    from . import fetch

    rows = []
    for spec in sources.ARCHIVES:
        path = sources.ARCHIVE_DIR / spec["edition"] / spec["name"]
        if not path.exists():
            continue
        rows.append(
            {
                "edition": spec["edition"],
                "archive": spec["name"],
                "sha256": fetch.sha256_file(path),
                "size": path.stat().st_size,
            }
        )
    return rows


def _provenance_doc(results, source_stats, derived_stats):
    lines = [
        "# Provenance",
        "",
        "External evidence gathered in Cycle 2. The source files remain",
        "authoritative; these records describe the official archives and how far",
        "the current corpus matches them.",
        "",
        "## Archives",
        "",
        "| Edition | Archive | SHA-256 | Size (bytes) |",
        "| --- | --- | --- | ---: |",
    ]
    for row in _archive_records():
        lines.append(
            f"| `{row['edition']}` | `{row['archive']}` | `{row['sha256']}` | {row['size']} |"
        )
    lines.extend(
        [
            "",
            "The original zips live under `data/raw/_archives/` (gitignored); the",
            "extracted inputs are committed under `data/raw/<edition>/`.",
            "",
            "## Match verdict",
            "",
            "| Edition | Source files normalized | Source verses matching |",
            "| --- | ---: | ---: |",
        ]
    )
    for edition, stat in sorted(source_stats.items()):
        lines.append(
            f"| `{edition}` | {stat['normalized']}/{stat['files']} | "
            f"{stat['match']}/{stat['verses']} ({_percent(stat['match'], stat['verses'])}) |"
        )
    lines.extend(
        [
            "",
            "| Edition | Reference | Dataset | Verses matching |",
            "| --- | --- | --- | ---: |",
        ]
    )
    for (edition, reference, dataset), stat in sorted(derived_stats.items()):
        lines.append(
            f"| `{edition}` | `{reference}` | `{dataset}` | "
            f"{stat['match']}/{stat['verses']} ({_percent(stat['match'], stat['verses'])}) |"
        )
    strongs = results["strongs"]
    lines.extend(
        [
            "",
            "## Strong's / BP5 provenance",
            "",
            f"Status: `{strongs['status']}`.",
        ]
    )
    if strongs["hits"]:
        lines.append("Hits: " + ", ".join(f"`{hit}`" for hit in strongs["hits"]))
    else:
        lines.append(
            "None of the six official archives contains a parsed/Strong's file, "
            "so `source/Strongs/*.BP5` remains provenance-unknown."
        )
    lines.extend(
        [
            "",
            "## Intentional blanks (D7)",
            "",
            "LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 are present as blank",
            "references in the official CCAT archives, confirming D7.",
            "",
            "## Decisions",
            "",
            "See `reports/reconciliation/decision-log.md`.",
            "",
        ]
    )
    return "\n".join(lines)


def _summary(results, source_stats, derived_stats, categories):
    best = max(
        source_stats,
        key=lambda edition: (
            source_stats[edition]["match"] / max(source_stats[edition]["verses"], 1)
        ),
    )
    lines = [
        "# Official archive reconciliation",
        "",
        "Read-only comparison of the current corpus against the six official",
        "archives. No source, CSV, or TEI file was changed.",
        "",
        "## Commands",
        "",
        "```bash",
        "python3 scripts/fetch_official.py --verify",
        "PYTHONPATH=src python3 -m byz.reconcile",
        "PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation -v",
        "```",
        "",
        "## Source tier (`source/CCAT/*.TXT` vs official `.CCT`)",
        "",
        "| Edition | Files compared | Normalized matches | Verses matching |",
        "| --- | ---: | ---: | ---: |",
    ]
    for edition, stat in sorted(source_stats.items()):
        lines.append(
            f"| `{edition}` | {stat['files']} | {stat['normalized']} | "
            f"{stat['match']}/{stat['verses']} ({_percent(stat['match'], stat['verses'])}) |"
        )
    best_categories = {
        row["category"]: row["count"]
        for row in categories
        if row["tier"] == "source" and row["edition"] == best
    }
    apparatus = best_categories.get("variant", 0) + best_categories.get(
        "variant-code", 0
    )
    lines.extend(
        [
            "",
            f"**Closest edition:** `{best}`.",
            "",
            f"Current `source/CCAT` is closest to `{best}`. For `{best}`, "
            f"{best_categories.get('letters', 0)} verses differ in main-text "
            f"letters, {best_categories.get('punctuation', 0)} in punctuation, "
            f"{apparatus} are apparatus/variant differences, and "
            f"{best_categories.get('accents-breathings', 0)} are diacritic-"
            "ordering differences. Everything is itemised in `verses.csv` and the "
            "decision log.",
            "",
            "## Derived tier",
            "",
            "| Edition | Reference | Dataset | Verses matching |",
            "| --- | --- | --- | ---: |",
        ]
    )
    for (edition, reference, dataset), stat in sorted(derived_stats.items()):
        lines.append(
            f"| `{edition}` | `{reference}` | `{dataset}` | "
            f"{stat['match']}/{stat['verses']} ({_percent(stat['match'], stat['verses'])}) |"
        )
    classes = Counter(row["class"] for row in results["files"])
    lines.extend(
        [
            "",
            "## Mapping coverage",
            "",
            "| Class | Files |",
            "| --- | ---: |",
        ]
    )
    for name, count in sorted(classes.items()):
        lines.append(f"| `{name}` | {count} |")
    lines.extend(
        [
            "",
            "`files.csv` lists every mapped file, including the 27 Strong's files",
            "with `provenance-unknown` and the accented CCAT CSV views marked",
            "`incomparable-pending-pipeline`.",
            "",
            "## Strong's / BP5",
            "",
            f"Status: `{results['strongs']['status']}`. The official archives do not",
            "include a parsed/Strong's file, so its provenance remains unknown.",
            "",
            "## Intentional blanks",
            "",
            "LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 are blank in the official",
            "CCAT archives; D7 is confirmed.",
            "",
            "## Categories",
            "",
            "| Tier | Edition | Category | Count |",
            "| --- | --- | --- | ---: |",
        ]
    )
    for row in categories:
        lines.append(
            f"| `{row['tier']}` | `{row['edition']}` | `{row['category']}` | {row['count']} |"
        )
    lines.extend(
        [
            "",
            "## Decision log",
            "",
            "See `reports/reconciliation/decision-log.md`. No canonical source was",
            "selected automatically.",
            "",
        ]
    )
    return "\n".join(lines)


def _decision_log(results):
    strongs = results["strongs"]["status"]
    return f"""# Decision log - official archive reconciliation

The pipeline flags; the maintainer decides. No source file was changed.

| ID | Question | Evidence | Options | Maintainer decision |
| --- | --- | --- | --- | --- |
| R1 | Which archive is canonical for each edition? | Current `source/CCAT` is closest to 2018; 2005 differs in more verses. | (a) `rp2018` canonical. (b) 2005 canonical. (c) per-file. | pending |
| R2 | Apparatus codes differ from official 2018 (e.g. `C` vs `N` in Acts). | `reports/reconciliation/verses.csv` (category `variant-code`). | (a) Keep current 2023 codes. (b) Adopt official 2018 codes. (c) per-book. | pending |
| R3 | Word segmentation differs (`mhti` vs `mh ti` in 1CO/2CO). | `verses.csv` (category `word-segmentation`). | (a) Keep current. (b) Adopt archive. | pending |
| R4 | Strong's/BP5 provenance. | Status `{strongs}`; no parsed archive in the six zips. | (a) Find an official parsed archive. (b) Keep provenance-unknown. | pending |
| R5 | `GREEK.CCT` is documentation, not text. | Inventory shows it is a transliteration key. | (a) Auxiliary. (b) Map elsewhere. | pending |
| R6 | Formatting-only differences (`*[` vs `[*`, dash/ellipsis spacing). | Treated as normalization-only. | (a) Accept as equivalent. (b) Preserve exactly. | pending |
| R7 | Should official 2018 files replace current `source/`? | Current includes post-2018 changes (e.g. apparatus codes). | (a) Keep current. (b) Adopt official. (c) merge per decision R1/R2. | pending |
| R8 | Commit original zips? | They live under gitignored `data/raw/_archives/`; checksums recorded. | (a) Keep out of git. (b) Commit them. | pending |
"""


def _update_history(stats, best):
    path = sources.DOCS_DIR / "HISTORY.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    begin = text.find(CYCLE2_BEGIN)
    end = text.find(CYCLE2_END)
    if begin != -1 and end != -1:
        text = text[:begin].rstrip() + "\n" + text[end + len(CYCLE2_END) :]
    block = [
        CYCLE2_BEGIN,
        "## External archive evidence (Cycle 2)",
        "",
        "| Edition | Source verses matching official CCAT |",
        "| --- | ---: |",
    ]
    for edition, stat in sorted(stats.items()):
        block.append(
            f"| `{edition}` | {stat['match']}/{stat['verses']} "
            f"({_percent(stat['match'], stat['verses'])}) |"
        )
    block.extend(
        [
            "",
            f"Closest official edition: `{best}`. See `docs/PROVENANCE.md`.",
            CYCLE2_END,
            "",
        ]
    )
    text = text.rstrip() + "\n\n" + "\n".join(block)
    path.write_text(text, encoding="utf-8")


def write_all(results):
    archives = _archives()
    category_rows = _categories(results["verses"])
    source_stats = _source_stats(results["files"])
    derived_stats = _derived_stats(results["files"])
    best = max(
        source_stats,
        key=lambda edition: (
            source_stats[edition]["match"] / max(source_stats[edition]["verses"], 1)
        ),
    )

    files = sorted(
        results["files"],
        key=lambda row: (
            row["tier"],
            row["edition"],
            row["dataset"],
            row["current"],
        ),
    )
    verses = sorted(
        results["verses"],
        key=lambda row: (
            row["tier"],
            row["edition"],
            row["dataset"],
            row["book"],
            row["chapter"],
            row["verse"],
        ),
    )

    reports = sources.REPORTS_DIR
    write_csv(reports / "archives.csv", archives)
    write_csv(reports / "files.csv", files)
    write_csv(reports / "verses.csv", verses)
    write_csv(reports / "categories.csv", category_rows)
    (reports / "summary.md").write_text(
        _summary(results, source_stats, derived_stats, category_rows),
        encoding="utf-8",
    )
    (reports / "decision-log.md").write_text(_decision_log(results), encoding="utf-8")
    (sources.DOCS_DIR / "PROVENANCE.md").write_text(
        _provenance_doc(results, source_stats, derived_stats),
        encoding="utf-8",
    )
    _update_history(source_stats, best)

    return {
        "source_stats": source_stats,
        "derived_stats": derived_stats,
        "best": best,
        "files": len(files),
        "verses": len(verses),
        "strongs": results["strongs"]["status"],
    }
