<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

# Data contract

This document describes the corpus as it exists today. It is generated from `src/byz/contract/contracts.py` and the baseline run. The machine-readable copy lives in `docs/contract/`.

No external archive is involved in this contract; that is the next cycle.

## Coverage

| Dataset | Files | Books | Records |
| --- | ---: | ---: | ---: |
| `editions/rp2018-2023/csv/accented/no-variants` | 29 | 29 | 7972 |
| `editions/rp2018-2023/csv/accented/with-variants` | 29 | 29 | 7972 |
| `editions/rp2018-2023/csv/strongs/no-parsing` | 27 | 27 | 7957 |
| `editions/rp2018-2023/csv/strongs/with-parsing` | 27 | 27 | 7957 |
| `editions/rp2018-2023/tei/unaccented` | 27 | 27 | 7957 |
| `editions/rp2018-2023/tei/unaccented/BYZ` | 1 | 27 | 7957 |
| `source/CCAT` | 29 | 29 | 7972 |
| `source/Strongs` | 27 | 27 | 7957 |

## Derivation map

| Input | Output | Evidence | Status |
| --- | --- | --- | --- |
| `n/a` (+0 more) | `docs/assets/demo_john_1.xml` | hand-prepared demo asset (see docs/COLLATEX.md) | 0 ok, 1 auxiliary |
| `source/CCAT/01_MAT.TXT` (+57 more) | `editions/rp2018-2023/csv/accented/no-variants/MAT.csv` | src/byz/curate/build.py: build_all -> recover.recover_all copies source/CCAT into the editions/rp2018-2023/source snapshot, then build_current -> parse_cct_current(drop_variants=...) -> write_csv | 58 ok |
| `source/Strongs/01_MAT.BP5` (+53 more) | `editions/rp2018-2023/csv/strongs/no-parsing/MAT.csv` | src/byz/curate/build.py: build_all -> recover.recover_all copies source/Strongs into the editions/rp2018-2023/source snapshot, then build_current -> parse_bp5_strongs -> write_csv | 54 ok |
| `editions/rp2018-2023/csv/strongs/no-parsing/*.csv` (+27 more) | `editions/rp2018-2023/tei/unaccented/BYZ/byz.xml` | src/byz/curate/build.py: build_current -> write_tei() from csv/strongs/no-parsing | 28 ok |

## Section files

`04a_PA.TXT` (John 7:53-8:11) and `05a_ACT24.TXT` (Acts 24:6-8) are separate pseudo-books in the CCAT and CSV-CCAT datasets. The Strong's and TEI datasets have no counterpart. See decision log D1.

## Known exceptions

| Dataset | Key | Reason |
| --- | --- | --- |
| - | - | None |

## Intentional blank verses

These verses are not part of the Byzantine tradition. They are kept as empty CSV rows and empty `<ab/>` TEI elements (D7/D8).

| Book | Chapter | Verse |
| --- | ---: | ---: |
| `ACT` | 8 | 37 |
| `ACT` | 15 | 34 |
| `ACT` | 24 | 7 |
| `LUK` | 17 | 36 |

## Dataset contracts

### source/CCAT

Official accented Byzantine text in Beta code, with variants.

- **filename**: `^(\d{2}a?)_([A-Z0-9]+)\.TXT$`
- **record**:
  - `prefix`: `chapter:verse`
  - `line`: `^(\d{2}):(\d{2})(?:\s(.*))?$`
- **variant**:
  - `syntax`: `{CODE OLD > NEW}`
  - `codes`: `['N', 'B', 'C', 'M', 'S', 'E']`
  - `prefix`: `^[NBCMSE]\s`

Invariants:

- every non-blank line starts with chapter:verse
- variant braces are balanced and not nested
- variant content starts with a known code and contains '>'
- blank records are allowed only for the intentional blank verses

### source/Strongs

Official unaccented text with Strong's numbers and parsing.

- **filename**: `^(\d{2})_([A-Z0-9]+)\.BP5$`
- **record**:
  - `prefix`: `chapter.verse`
  - `line`: `^(\d{2})\.(\d{2})(?:\s(.*))?$`
- **word**:
  - `syntax`: `word strongs {parsing} [strongs {parsing}]`
- **strongs**: `^\d+$`
- **parsing**: `^\{[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\}$`

Invariants:

- every non-blank line starts with chapter.verse
- every word is followed by a positive Strong's number and parsing code
- multi-parsing alternatives are allowed after the first pair
- blank records are allowed only for the intentional blank verses

### editions/rp2018-2023/csv/accented/no-variants

Unicode CSV of CCAT with variants removed.

- **header**: `['chapter', 'verse', 'text']`

Invariants:

- header is chapter,verse,text
- chapter and verse are integers
- text is non-empty except for the intentional blank verses
- no duplicate (chapter, verse) keys
- no Beta-code backslashes

### editions/rp2018-2023/csv/accented/with-variants

Unicode CSV of CCAT with variants retained.

- **header**: `['chapter', 'verse', 'text']`

Invariants:

- header is chapter,verse,text
- chapter and verse are integers
- text is non-empty except for the intentional blank verses
- no duplicate (chapter, verse) keys
- no Beta-code backslashes

### editions/rp2018-2023/csv/strongs/no-parsing

Unicode CSV of the Strong's text with parsing dropped.

- **header**: `['chapter', 'verse', 'text']`

Invariants:

- header is chapter,verse,text
- chapter and verse are integers
- text is non-empty except for the intentional blank verses
- no duplicate (chapter, verse) keys

### editions/rp2018-2023/csv/strongs/with-parsing

Unicode CSV of the Strong's text with parsing retained.

- **header**: `['chapter', 'verse', 'text']`

Invariants:

- header is chapter,verse,text
- chapter and verse are integers
- text is non-empty except for the intentional blank verses
- no duplicate (chapter, verse) keys

### editions/rp2018-2023/tei/unaccented

Unaccented TEI-XML export generated from strongs/no-parsing.

- **structure**: `TEI/teiHeader/text/body/div[@type=book]/div[@type=chapter]/ab/w`
- **anchor**: `^B(\d{2})K(\d+)V(\d+)$`

Invariants:

- XML is well-formed
- each file has book divisions with known Bxx ids
- verse anchors are unique and match BxxKxVx
- no empty <w> elements
- intentional blank verses are empty <ab> elements

### editions/rp2018-2023/tei/unaccented/BYZ

Combined TEI-XML of all 27 books.

- **structure**: `same as per-book TEI, with 27 book divisions`
- **anchor**: `^B(\d{2})K(\d+)V(\d+)$`

Invariants:

- covers the same books as the per-book files
