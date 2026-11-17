# Baseline corpus summary

Inventory and validation of the corpus as it currently exists. No external archive was fetched. The generated CSV/TEI were regenerated from source for D8 and the stale parsing artifacts were corrected.

- Datasets: 8
- Files: 196 validated; see `files.csv`
- `files.csv` records, for each file, the last commit that touched it. Because the working tree has not been committed yet, that column lags by one commit until the next commit lands.
- Invariant findings: 0 (0 unresolved, 0 known exception)
- Missing derived files: 0
- Cross-dataset coverage mismatches: 0

## Key finding

- The four verses that are intentionally blank because they are not part of the Byzantine tradition (LUK 17:36, ACT 8:37, ACT 15:34, ACT 24:7) are preserved as explicit empty records in CSV and TEI (D7/D8).
- Source and generated coverage now match; TEI matches `strongs/no-parsing` exactly.
- Regeneration also corrected two stale parsing artifacts: 2TI 2:22 (`A-APF-C` -> `A-APF`) and ACT 4:9 (duplicate `5101 {I-DSN}` removed).
- All 140 expected derivations exist; `demo_john_1.xml` is auxiliary.
- The current text is modelled as `rp2018` revision `2023-07-20` (D3); the source files are authoritative (D5).

## Datasets

| Dataset | Files | Books | Records | Unique verses |
| --- | ---: | ---: | ---: | ---: |
| `csv-unicode/ccat/no-variants` | 29 | 29 | 7972 | 7972 |
| `csv-unicode/ccat/with-variants` | 29 | 29 | 7972 | 7972 |
| `csv-unicode/strongs/no-parsing` | 27 | 27 | 7957 | 7957 |
| `csv-unicode/strongs/with-parsing` | 27 | 27 | 7957 | 7957 |
| `source/CCAT` | 29 | 29 | 7972 | 7972 |
| `source/Strongs` | 27 | 27 | 7957 | 7957 |
| `tei-xml-unicode/BYZ` | 1 | 27 | 7957 | 7957 |
| `tei-xml-unicode/no-accents` | 27 | 27 | 7957 | 7957 |

## Invariant findings by category

No findings.

## Cross-dataset coverage differences

No coverage differences.

## Known internal quirks

- `04a_PA.TXT` is John 7:53-8:11 (Pericope Adulterae) and `05a_ACT24.TXT` is Acts 24:6-8. They are separate pseudo-books in CCAT/CSV-CCAT and have no Strong's or TEI counterpart.
- `05_ACT.TXT` leaves Acts 24:7 blank; the Byzantine expansion lives in `05a_ACT24.TXT`.
- LUK 17:36, ACT 8:37, and ACT 15:34 are intentionally blank because they are not part of the Byzantine tradition; they are kept as empty records (D7/D8).
- TEI is generated from `strongs/no-parsing`, so it is unaccented and has no parsing; this is intended (D2).
- Generated CSV/TEI were unverified derivatives until this regeneration; source remains authoritative (D4/D5).

## Reproduce

```bash
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m unittest discover -s tests/contract -v
```

## Decision log

See `reports/baseline/decision-log.md`.
