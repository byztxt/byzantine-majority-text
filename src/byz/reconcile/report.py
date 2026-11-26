"""Deterministic reconciliation reports and provenance documents."""

import csv
from collections import Counter, defaultdict
from datetime import datetime

from .. import generated
from . import archive, historical, sources

CYCLE2_BEGIN = "<!-- cycle2:begin -->"
CYCLE2_END = "<!-- cycle2:end -->"


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0].keys()),
            lineterminator="\n",
        )
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


def _retrieval_window() -> tuple:
    """Return (month, first_stamp, last_stamp) from the provenance files.

    Derived from the `downloaded` fields, never hard-coded: a later `--force`
    rewrites those timestamps, and the generated prose must follow them rather
    than go stale.
    """
    from . import fetch

    stamps = []
    for edition in sorted({spec["edition"] for spec in sources.ARCHIVES}):
        path = sources.PROVENANCE_DIR / f"{edition}.toml"
        for record in fetch._existing_records(path).values():
            stamp = record.get("downloaded", "")
            if stamp:
                stamps.append(stamp)
    if not stamps:
        return "", "", ""
    first, last = min(stamps), max(stamps)
    month = datetime.strptime(first, "%Y-%m-%dT%H:%M:%SZ").strftime("%B %Y")
    return month, first, last


def _provenance_doc(results, source_stats, derived_stats, history_rows):
    month, first, last = _retrieval_window()
    if first:
        obtained = f"in {month}."
        stamps = (
            f"The recorded download timestamp is `{first}`."
            if first == last
            else f"The recorded download timestamps are `{first}` through "
            f"`{last}`."
        )
    else:
        obtained = "at the recorded download time."
        stamps = ""
    lines = [
        "# Provenance",
        "",
        "External evidence gathered in Cycle 2. The published PDFs are the",
        "ultimate source of truth for the printed editions, and",
        "`data/raw/repo/rp2018-2023/` is the authoritative machine-readable",
        "text for the derivatives. `data/raw/` has two source classes:",
        "`data/raw/print/` holds the published print-edition material and",
        "`data/raw/repo/` holds this repository's own lineage. These records",
        "describe the official archives and how far the current corpus matches",
        "them.",
        "",
        "## Archives",
        "",
        "All six archives were initially obtained from the Byzantine Text editions",
        f"listing page <{sources.SOURCE_PAGE}> {obtained}",
    ]
    if stamps:
        lines.append(stamps)
    lines.extend(
        [
            "Each `[[archives]]` record in `data/provenance/rp2005.toml` and",
            "`data/provenance/rp2018.toml` carries the listing page as `source_page`,",
            "alongside the per-file Dropbox URL and SHA-256.",
            "",
            "| Edition | Archive | SHA-256 | Size (bytes) |",
            "| --- | --- | --- | ---: |",
        ]
    )
    for row in _archive_records():
        lines.append(
            f"| `{row['edition']}` | `{row['archive']}` | `{row['sha256']}` | {row['size']} |"
        )
    lines.extend(
        [
            "",
            "The original zips are committed under `data/raw/print/_archives/` and are",
            "pinned by SHA-256 in `data/provenance/*.toml`. The extracted inputs",
            "under `data/raw/print/<edition>/` are produced from those zips; they are",
            "not separately hashed in the provenance files.",
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
    lines.extend(_lineage_lines(history_rows))
    strongs = results["strongs"]
    hits = strongs["hits"]
    lines.extend(
        [
            "",
            "## Strong's / BP5 provenance",
            "",
            (
                f"Status: `{strongs['status']}` "
                f"(delivery route: `{strongs['delivery']}`)."
            ),
            "",
            "`data/raw/repo/rp2018-2023/strongs/*.BP5` are Dr. Maurice A. Robinson's parsed",
            "files, the same official material as `data/raw/repo/rp2018-2023/ccat` (see",
            "`data/raw/repo/CONVENTIONS.md`).",
        ]
    )
    if hits:
        lines.extend(
            [
                "The archive scan found a parsed/Strong's file, so the file-level",
                "delivery route is recorded: "
                + ", ".join(f"`{hit}`" for hit in hits)
                + ".",
            ]
        )
    else:
        lines.extend(
            [
                "None of the six published ZIP archives contains a parsed/Strong's",
                "file, so the file-level delivery route is not recorded. That is a gap",
                "in the archive evidence, not a doubt about the files' origin.",
            ]
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


def _lineage_lines(history_rows):
    lookup = {
        (row["state"], row["compared_to"]): row for row in history_rows
    }
    lines = [
        "",
        "## Historical lineage",
        "",
        "| State | Compared to | Files fully matching | Verses matching |",
        "| --- | --- | ---: | ---: |",
    ]
    for row in history_rows:
        lines.append(
            f"| `{row['state']}` | `{row['compared_to']}` | "
            f"{row['full_files']}/{row['files']} | "
            f"{row['match']}/{row['verses']} ({row['percent']}) |"
        )
    v203_05 = lookup.get(("v2.0.3 textonly-beta-code", "rp2005"), {})
    v203_18 = lookup.get(("v2.0.3 textonly-beta-code", "rp2018"), {})
    cur_05 = lookup.get((historical.CURRENT_STATE, "rp2005"), {})
    cur_18 = lookup.get((historical.CURRENT_STATE, "rp2018"), {})
    lines.extend(
        [
            "",
            "- The current `data/raw/repo/rp2018-2023/ccat` was first added in commit `97371d7` "
            "(2023-05-30) as `source/CCAT` and merged in `v3.0.0` (2023-05-31, "
            "PR #25 'update_to_2023'). It is the 2018 edition with 2023 "
            "adjustments.",
            "- The 2005-lineage text lives in `textonly-beta-code` at `v2.0.3` "
            "and earlier; it was last updated in 2019. Its `textonly-beta-code` "
            "and `parsed` inputs are committed at `data/raw/repo/rp2005-2019/`, with "
            "`data/provenance/rp2005-2019.toml` recording the tag, the commit, "
            "and every file hash. The curated `rp2005-2019` edition is the 2019 "
            "sources rebuilt by the current pipeline, not a copy of the release's "
            "artifacts: the malformed apparatus codes and the 2019 typography are "
            "corrected, while the main text keeps the same words.",
            f"- `v2.0.3` matches official 2018 in {v203_18.get('match', '?')}/"
            f"{v203_18.get('verses', '?')} verses ({v203_18.get('percent', '?')}) "
            f"but official 2005 in {v203_05.get('match', '?')}/"
            f"{v203_05.get('verses', '?')} ({v203_05.get('percent', '?')}). It is "
            "therefore a 2019 revision of the 2005 edition, not the official 2005 "
            "archive itself.",
            f"- The current source matches official 2018 in "
            f"{cur_18.get('match', '?')}/{cur_18.get('verses', '?')} "
            f"({cur_18.get('percent', '?')}) and official 2005 in "
            f"{cur_05.get('match', '?')}/{cur_05.get('verses', '?')} "
            f"({cur_05.get('percent', '?')}).",
            "- So the current tree does **not** contain the 2005 text. Comparing "
            "it with the official 2005 archive is a cross-check, not an "
            "identification.",
            "",
        ]
    )
    return lines


def _summary(results, source_stats, derived_stats, categories, history_rows):
    best = max(
        source_stats,
        key=lambda edition: (
            source_stats[edition]["match"] / max(source_stats[edition]["verses"], 1)
        ),
    )
    strongs = results["strongs"]
    if strongs["hits"]:
        strongs_body = [
            "Dr Robinson's official parsed files; the archive scan found "
            + ", ".join(f"`{hit}`" for hit in strongs["hits"])
            + ", so the delivery route is recorded."
        ]
    else:
        strongs_body = [
            "Dr Robinson's official parsed files; none of the six archives contains",
            "a parsed/Strong's file, so only the delivery route is unrecorded.",
        ]
    lines = [
        "# Official archive reconciliation",
        "",
        "Read-only comparison of the current corpus against the six official",
        "archives. No source, CSV, or TEI file was changed.",
        "",
        "## Commands",
        "",
        "```bash",
        "PYTHONPATH=src python3 -m byz.fetch --verify",
        "PYTHONPATH=src python3 -m byz.reconcile",
        "PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation -v",
        "```",
        "",
        "## Source tier (`data/raw/repo/rp2018-2023/ccat/*.TXT` vs official `.CCT`)",
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
    apparatus_reading = best_categories.get("variant", 0)
    apparatus_code = best_categories.get("apparatus-code", 0)
    apparatus = apparatus_reading + apparatus_code
    lines.extend(
        [
            "",
            f"**Closest edition:** `{best}`.",
            "",
            f"Current `data/raw/repo/rp2018-2023/ccat` is closest to `{best}`. For `{best}`, "
            f"{best_categories.get('letters', 0)} verses differ in main-text "
            f"letters, {best_categories.get('punctuation', 0)} in punctuation, "
            f"{apparatus} are apparatus differences ({apparatus_reading} reading "
            f"changes, {apparatus_code} code-only changes), and "
            f"{best_categories.get('accents-breathings', 0)} are diacritic-"
            "ordering differences. Everything is itemised in `verses.csv` and the "
            "decision log.",
            "",
        ]
    )
    lines.extend(_lineage_lines(history_rows))
    lines.extend(
        [
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
            "marked `official-source` and the accented CCAT CSV views marked",
            "`incomparable-pending-pipeline`.",
            "",
            "## Strong's / BP5",
            "",
            f"Status: `{strongs['status']}`. `data/raw/repo/rp2018-2023/strongs/*.BP5` are",
            *strongs_body,
            "",
            "## Intentional blanks",
            "",
            "LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 are blank in the official",
            "CCAT archives; D7 is confirmed.",
            "",
            "## Categories",
            "",
            "Category meanings and worked examples: "
            "[`reports/diffs/README.md`](../diffs/README.md#categories).",
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
    hits = results["strongs"]["hits"]
    if hits:
        route = (
            "the archive scan found "
            + ", ".join(f"`{hit}`" for hit in hits)
            + ", so the delivery route is recorded"
        )
        outcome = (
            "the files are official Robinson material, and the archive scan "
            "records their delivery route"
        )
    else:
        route = (
            "no parsed archive is among the six ZIPs, so the delivery route is "
            "not recorded"
        )
        outcome = (
            "the files are official Robinson material; only the delivery route "
            "for the parsed files is unrecorded"
        )
    return f"""# Decision log - official archive reconciliation

The pipeline flags; the maintainer decides. No source file was changed.

| ID | Question | Evidence | Options | Maintainer decision |
| --- | --- | --- | --- | --- |
| R1 | Which archive is canonical for each edition? | Current `data/raw/repo/rp2018-2023/ccat` is closest to 2018; 2005 differs in more verses. | (a) `rp2018` canonical. (b) 2005 canonical. (c) per-file. | pending |
| R2 | Apparatus codes differ from official 2018 (e.g. `C` vs `N` in Acts). | `reports/reconciliation/verses.csv` (category `apparatus-code`: the tag differs, the reading does not). | (a) Keep current 2023 codes. (b) Adopt official 2018 codes. (c) per-book. | pending |
| R3 | Word segmentation differs (`mhti` vs `mh ti` in 1CO/2CO). | `verses.csv` (category `word-segmentation`). | (a) Keep current. (b) Adopt archive. | pending |
| R4 | Strong's/BP5 provenance. | `data/raw/repo/rp2018-2023/strongs/*.BP5` are Dr Robinson's official parsed files (`data/raw/repo/CONVENTIONS.md`); {route}. | (a) Find an official parsed archive. (b) Leave the files labelled unknown. | resolved (2026-11-19): {outcome}. |
| R5 | `GREEK.CCT` is documentation, not text. | Inventory shows it is a transliteration key. | (a) Auxiliary. (b) Map elsewhere. | pending |
| R6 | Formatting-only differences (`*[` vs `[*`, dash/ellipsis spacing). | Treated as normalization-only. | (a) Accept as equivalent. (b) Preserve exactly. | pending |
| R7 | Should official 2018 files replace current `data/raw/repo/rp2018-2023/`? | Current includes post-2018 changes (e.g. apparatus codes). | (a) Keep current. (b) Adopt official. (c) merge per decision R1/R2. | pending |
| R8 | Commit original zips? | They live under `data/raw/print/_archives/`; checksums are recorded in `data/provenance/*.toml`. | (a) Keep out of git. (b) Commit them. | adopted (2026-11-17): commit the six original zips under `data/raw/print/_archives/` for posterity and offline reproducibility; `PYTHONPATH=src python3 -m byz.fetch --verify` checks the committed copies. |
| R9 | Which historical state is the 2005 edition? | `v2.0.3 textonly-beta-code` is a 2019 revision of the 2005 edition; it matches official 2018 (99.96%) more closely than official 2005 (99.32%). The current source is the 2023 2018 text, first added in `97371d7` and merged in `v3.0.0`. | (a) Use the official 2005 archive as the 2005 edition. (b) Use `v2.0.3` (the repo's 2019 revision). (c) Keep both, clearly labelled. | pending |
"""


def _update_history(stats, best, history_rows):
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
            "| State | Compared to | Verses matching |",
            "| --- | --- | ---: |",
        ]
    )
    for row in history_rows:
        block.append(
            f"| `{row['state']}` | `{row['compared_to']}` | "
            f"{row['match']}/{row['verses']} ({row['percent']}) |"
        )
    block.extend(
        [
            "",
            f"Closest official edition for the current source: `{best}`.",
            "The current `data/raw/repo/rp2018-2023/ccat` was first added in `97371d7` (2023-05-30, "
            "merged in `v3.0.0`). The 2005-lineage text is in `textonly-beta-code` "
            "at `v2.0.3` and earlier, last updated 2019. See `docs/PROVENANCE.md`.",
            CYCLE2_END,
            "",
        ]
    )
    text = text.rstrip() + "\n\n" + "\n".join(block)
    path.write_text(generated.markdown(text), encoding="utf-8")


def write_all(results):
    archives = _archives()
    category_rows = _categories(results["verses"])
    history_rows = historical.evidence()
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
    write_csv(reports / "history.csv", history_rows)
    generated.write_markdown(
        reports / "summary.md",
        _summary(results, source_stats, derived_stats, category_rows, history_rows),
    )
    generated.write_markdown(
        reports / "decision-log.md", _decision_log(results)
    )
    generated.write_markdown(
        sources.DOCS_DIR / "PROVENANCE.md",
        _provenance_doc(results, source_stats, derived_stats, history_rows),
    )
    _update_history(source_stats, best, history_rows)

    return {
        "source_stats": source_stats,
        "derived_stats": derived_stats,
        "best": best,
        "files": len(files),
        "verses": len(verses),
        "strongs": results["strongs"]["status"],
    }
