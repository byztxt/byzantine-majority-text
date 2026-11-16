# Baseline corpus summary

Read-only inventory and validation of the corpus as it exists today. No external archive was fetched and no data file was changed.

- Datasets: 8
- Files: 196 validated; see `files.csv`
- Invariant findings: 8 (0 unresolved, 8 known exception)
- Missing derived files: 0
- Cross-dataset coverage mismatches: 8

## Key finding

- Source and generated coverage agree everywhere except LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7, which are blank in the source and therefore absent from the CSV (and consequently the TEI).
- TEI matches `strongs/no-parsing` exactly (7953 verses).
- All 140 expected derivations exist; `demo_john_1.xml` is auxiliary.

## Datasets

| Dataset | Files | Books | Records | Unique verses |
| --- | ---: | ---: | ---: | ---: |
| `csv-unicode/ccat/no-variants` | 29 | 29 | 7968 | 7968 |
| `csv-unicode/ccat/with-variants` | 29 | 29 | 7968 | 7968 |
| `csv-unicode/strongs/no-parsing` | 27 | 27 | 7953 | 7953 |
| `csv-unicode/strongs/with-parsing` | 27 | 27 | 7953 | 7953 |
| `source/CCAT` | 29 | 29 | 7972 | 7972 |
| `source/Strongs` | 27 | 27 | 7957 | 7957 |
| `tei-xml-unicode/BYZ` | 1 | 27 | 7953 | 7953 |
| `tei-xml-unicode/no-accents` | 27 | 27 | 7953 | 7953 |

## Invariant findings by category

- `blank-record`: 8

## Cross-dataset coverage differences

- CCAT source vs CSV no-variants, ACT: 3 only-left, 0 only-right
- CCAT source vs CSV no-variants, LUK: 1 only-left, 0 only-right
- CCAT source vs CSV with-variants, ACT: 3 only-left, 0 only-right
- CCAT source vs CSV with-variants, LUK: 1 only-left, 0 only-right
- Strong's source vs CSV no-parsing, ACT: 3 only-left, 0 only-right
- Strong's source vs CSV no-parsing, LUK: 1 only-left, 0 only-right
- Strong's source vs CSV with-parsing, ACT: 3 only-left, 0 only-right
- Strong's source vs CSV with-parsing, LUK: 1 only-left, 0 only-right

## Known internal quirks

- `04a_PA.TXT` is John 7:53-8:11 (Pericope Adulterae) and `05a_ACT24.TXT` is Acts 24:6-8. They are separate pseudo-books in CCAT/CSV-CCAT and have no Strong's or TEI counterpart.
- `05_ACT.TXT` leaves Acts 24:7 blank; the Byzantine expansion lives in `05a_ACT24.TXT`.
- LUK 17:36, ACT 8:37, and ACT 15:34 are also blank verse references with no section file (decision log D7).
- TEI is generated from `strongs/no-parsing`, so it is unaccented and has no parsing.

## Reproduce

```bash
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m unittest discover -s tests/contract -v
```

## Decision log

See `reports/baseline/decision-log.md`.
