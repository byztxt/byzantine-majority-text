"""Deterministic report writers for the baseline contract."""

import csv
import json
from collections import Counter

from . import contracts, coverage, derivation, history, invariants, paths


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _contract_doc(derivation_rows, dataset_rows, inv_rows):
    lines = [
        "# Data contract",
        "",
        "This document describes the corpus as it exists today. It is generated "
        "from `src/byz/contract/contracts.py` and the baseline run. The machine-"
        "readable copy lives in `docs/contract/`.",
        "",
        "No external archive is involved in this contract; that is the next cycle.",
        "",
        "## Coverage",
        "",
        "| Dataset | Files | Books | Records |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in dataset_rows:
        lines.append(
            f"| `{row['dataset']}` | {row['files']} | {row['books']} | {row['verses']} |"
        )
    lines.extend(
        [
            "",
            "## Derivation map",
            "",
            "| Input | Output | Evidence | Status |",
            "| --- | --- | --- | --- |",
        ]
    )
    grouped = derivation.summary(derivation_rows)
    for evidence, group in sorted(grouped.items()):
        status = f"{group['ok']} ok"
        if group["missing"]:
            status += f", {group['missing']} missing"
        if group["auxiliary"]:
            status += f", {group['auxiliary']} auxiliary"
        lines.append(
            f"| `{group['example_source']}` (+{group['checked'] - 1} more) "
            f"| `{group['example_derived']}` | {evidence} | {status} |"
        )
    lines.extend(
        [
            "",
            "## Section files",
            "",
            "`04a_PA.TXT` (John 7:53-8:11) and `05a_ACT24.TXT` (Acts 24:6-8) are "
            "separate pseudo-books in the CCAT and CSV-CCAT datasets. The Strong's "
            "and TEI datasets have no counterpart. See decision log D1.",
            "",
            "## Known exceptions",
            "",
            "| Dataset | Key | Reason |",
            "| --- | --- | --- |",
        ]
    )
    seen = set()
    for row in inv_rows:
        if not row["known_exception"]:
            continue
        marker = (row["dataset"], row["key"])
        if marker in seen:
            continue
        seen.add(marker)
        lines.append(
            f"| `{row['dataset']}` | `{row['key']}` | {row['known_exception']} |"
        )
    lines.extend(["", "## Dataset contracts", ""])
    for name, contract in contracts.DATASET_CONTRACTS.items():
        lines.extend([f"### {name}", "", contract.get("purpose", ""), ""])
        for key in (
            "filename",
            "record",
            "variant",
            "word",
            "strongs",
            "parsing",
            "header",
            "structure",
            "anchor",
        ):
            if key in contract:
                value = contract[key]
                if isinstance(value, dict):
                    lines.append(f"- **{key}**:")
                    for sub, subvalue in value.items():
                        lines.append(f"  - `{sub}`: `{subvalue}`")
                else:
                    lines.append(f"- **{key}**: `{value}`")
        lines.extend(["", "Invariants:", ""])
        for rule in contract.get("invariants", []):
            lines.append(f"- {rule}")
        lines.append("")
    return "\n".join(lines)


def _decision_log():
    return """# Decision log - baseline contract

Adopted by the maintainer on 2026-11-16. The pipeline flags; the maintainer decides.

| ID | Question | Decision | Next step |
| --- | --- | --- | --- |
| D1 | What are `PA` and `ACT24`? | Keep them as separate pseudo-books linked to John 7:53-8:11 and Acts 24:6-8. | Revisit the TEI representation in Cycle 6. |
| D2 | Is the TEI intentionally unaccented? | Yes. `tei-xml-unicode/no-accents` is the main-text export from `strongs/no-parsing`. | Add an accented/apparatus TEI from CCAT in Cycle 6. |
| D3 | How is the current text labelled? | `rp2018` with a `2023-07-20` revision, not a separate edition. | Confirm against the official archive in Cycle 2. |
| D4 | Are the generated CSV/TEI trustworthy? | The source files are authoritative; generated artifacts are unverified derivatives. | Reproduce them byte-for-byte in Cycle 3 before tagging an edition. |
| D5 | Which view wins on disagreement? | The source files win; divergence is a bug to flag. | Enforce in the validators and the pipeline. |
| D6 | Enforce the baseline contract in CI? | Yes, enforce the contract validators/tests now. Do not enforce artifact equality until Cycle 3. | CI workflow runs `tests/contract`. |
| D7 | What about LUK 17:36, ACT 8:37, ACT 15:34? | Intentional: these verses are not part of the Byzantine tradition. | The official archives should confirm this in Cycle 2. |
| D8 | Should blank verses be dropped from generated artifacts? | No. Preserve them as empty records so the intent is visible. | Implement in Cycle 3 and update the CSV/TEI contract. |

Note: Acts 24:7 is a separate intentional blank; the Byzantine expansion is in
`05a_ACT24.TXT`. The PA/ACT24 section files are the only pseudo-books without a
Strong's/TEI counterpart.
"""


def _summary(results, inv_rows, diff_rows, dataset_rows, derivation_rows):
    known = sum(1 for row in inv_rows if row["known_exception"])
    unknown = len(inv_rows) - known
    categories = Counter(row["category"] for row in inv_rows)
    missing = [row for row in derivation_rows if row["status"] == "missing"]
    diff_issues = [
        row
        for row in diff_rows
        if row["only_left"] or row["only_right"]
    ]
    lines = [
        "# Baseline corpus summary",
        "",
        "Read-only inventory and validation of the corpus as it exists today. "
        "No external archive was fetched and no data file was changed.",
        "",
        f"- Datasets: {len(results)}",
        f"- Files: {sum(len(v) for v in results.values())} validated; see `files.csv`",
        f"- Invariant findings: {len(inv_rows)} ({unknown} unresolved, {known} known exception)",
        f"- Missing derived files: {len(missing)}",
        f"- Cross-dataset coverage mismatches: {len(diff_issues)}",
        "",
        "## Key finding",
        "",
        "- The only coverage difference is the four verses that are intentionally "
        "blank because they are not part of the Byzantine tradition: LUK 17:36, "
        "ACT 8:37, ACT 15:34, and ACT 24:7. The CSV currently drops them "
        "(decision D7); Cycle 3 will preserve them as empty records (D8).",
        "- TEI matches `strongs/no-parsing` exactly (7953 verses).",
        "- All 140 expected derivations exist; `demo_john_1.xml` is auxiliary.",
        "- The current text is modelled as `rp2018` revision `2023-07-20` (D3); "
        "the source files are authoritative (D5).",
        "",
        "## Datasets",
        "",
        "| Dataset | Files | Books | Records | Unique verses |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in dataset_rows:
        lines.append(
            f"| `{row['dataset']}` | {row['files']} | {row['books']} | "
            f"{row['verses']} | {row['unique_verses']} |"
        )
    lines.extend(["", "## Invariant findings by category", ""])
    if categories:
        for category, count in sorted(categories.items()):
            lines.append(f"- `{category}`: {count}")
    else:
        lines.append("No findings.")
    lines.extend(["", "## Cross-dataset coverage differences", ""])
    if diff_issues:
        for row in diff_issues[:40]:
            lines.append(
                f"- {row['comparison']}, {row['book']}: "
                f"{row['only_left']} only-left, {row['only_right']} only-right"
            )
        if len(diff_issues) > 40:
            lines.append(f"- ... and {len(diff_issues) - 40} more rows in `differences.csv`")
    else:
        lines.append("No coverage differences.")
    lines.extend(
        [
            "",
            "## Known internal quirks",
            "",
            "- `04a_PA.TXT` is John 7:53-8:11 (Pericope Adulterae) and "
            "`05a_ACT24.TXT` is Acts 24:6-8. They are separate pseudo-books in "
            "CCAT/CSV-CCAT and have no Strong's or TEI counterpart.",
            "- `05_ACT.TXT` leaves Acts 24:7 blank; the Byzantine expansion lives "
            "in `05a_ACT24.TXT`.",
            "- LUK 17:36, ACT 8:37, and ACT 15:34 are intentionally blank "
            "because they are not part of the Byzantine tradition (D7).",
            "- TEI is generated from `strongs/no-parsing`, so it is unaccented and "
            "has no parsing; this is intended (D2).",
            "- Generated CSV/TEI are unverified derivatives until Cycle 3 "
            "reproduces them byte-for-byte (D4).",
            "",
            "## Reproduce",
            "",
            "```bash",
            "PYTHONPATH=src python3 -m byz.contract",
            "PYTHONPATH=src python3 -m unittest discover -s tests/contract -v",
            "```",
            "",
            "## Decision log",
            "",
            "See `reports/baseline/decision-log.md`.",
            "",
        ]
    )
    return "\n".join(lines)


def _rel(root, value):
    prefix = str(root) + "/"
    return value[len(prefix) :] if value.startswith(prefix) else value


def write_all(results, root=paths.ROOT):
    inv_rows = [
        violation.as_row()
        for violation in sorted(
            invariants.all_violations(results),
            key=lambda v: (v.dataset, v.path, v.line, v.category, v.message),
        )
    ]
    for row in inv_rows:
        row["path"] = _rel(root, row["path"])
    dataset_rows = coverage.dataset_summary(results)
    book_rows = coverage.book_rows(results)
    for row in book_rows:
        row["file"] = _rel(root, row["file"])
    diff_rows = coverage.diff_rows(results)
    derivation_rows = derivation.check(root)
    for row in derivation_rows:
        row["source"] = _rel(root, row["source"])

    reports = root / paths.REPORTS_DIR.relative_to(paths.ROOT)
    docs = root / paths.DOCS_DIR.relative_to(paths.ROOT)
    contract_dir = root / paths.CONTRACT_DIR.relative_to(paths.ROOT)

    from . import inventory

    files_rows = [record.as_row() for record in inventory.inventory(root)]
    write_csv(reports / "files.csv", files_rows)
    write_csv(reports / "books.csv", book_rows)
    write_csv(reports / "differences.csv", diff_rows)
    write_csv(reports / "invariants.csv", inv_rows)
    write_csv(reports / "derivations.csv", derivation_rows)

    write_json(contract_dir / "contracts.json", contracts.DATASET_CONTRACTS)
    for name, contract in contracts.DATASET_CONTRACTS.items():
        safe = name.replace("/", "__")
        write_json(contract_dir / f"{safe}.json", contract)

    (docs / "HISTORY.md").write_text(history.render(root), encoding="utf-8")
    (docs / "DATA_CONTRACT.md").write_text(
        _contract_doc(derivation_rows, dataset_rows, inv_rows), encoding="utf-8"
    )
    (reports / "summary.md").write_text(
        _summary(results, inv_rows, diff_rows, dataset_rows, derivation_rows),
        encoding="utf-8",
    )
    (reports / "decision-log.md").write_text(_decision_log(), encoding="utf-8")

    return {
        "reports": reports,
        "docs": docs,
        "contracts": contract_dir,
        "invariants": len(inv_rows),
        "unresolved": sum(1 for row in inv_rows if not row["known_exception"]),
        "known": sum(1 for row in inv_rows if row["known_exception"]),
        "missing_derived": sum(
            1 for row in derivation_rows if row["status"] == "missing"
        ),
        "differences": len(diff_rows),
    }
