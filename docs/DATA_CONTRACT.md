# Data contract

This document describes the corpus as it exists today. It is generated from `src/byz/contract/contracts.py` and the baseline run. The machine-readable copy lives in `docs/contract/`.

No external archive is involved in this contract; that is the next cycle.

## Coverage

| Dataset | Files | Books | Records |
| --- | ---: | ---: | ---: |
| `csv-unicode/ccat/no-variants` | 29 | 29 | 7968 |
| `csv-unicode/ccat/with-variants` | 29 | 29 | 7968 |
| `csv-unicode/strongs/no-parsing` | 27 | 27 | 7953 |
| `csv-unicode/strongs/with-parsing` | 27 | 27 | 7953 |
| `source/CCAT` | 29 | 29 | 7972 |
| `source/Strongs` | 27 | 27 | 7957 |
| `tei-xml-unicode/BYZ` | 1 | 27 | 7953 |
| `tei-xml-unicode/no-accents` | 27 | 27 | 7953 |

## Derivation map

| Input | Output | Evidence | Status |
| --- | --- | --- | --- |
| `n/a` (+0 more) | `tei-xml-unicode/assets/demo_john_1.xml` | hand-prepared demo asset (see tei-xml-unicode/README.md) | 0 ok, 1 auxiliary |
| `source/CCAT/01_MAT.TXT` (+57 more) | `csv-unicode/ccat/no-variants/MAT.csv` | scripts/csv_converter.py: path_ccat_no_variants / path_ccat_with_variants, convert_book(drop_variants=...) | 58 ok |
| `source/Strongs/01_MAT.BP5` (+53 more) | `csv-unicode/strongs/no-parsing/MAT.csv` | scripts/csv_converter.py: path_strongs_with_parsing / path_strongs_no_parsing, convert_book(drop_parsing=...) | 54 ok |
| `csv-unicode/strongs/no-parsing/*.csv` (+27 more) | `tei-xml-unicode/no-accents/BYZ/byz.xml` | scripts/tei_xml_converter.py: path_no_accents_csv = '../csv-unicode/strongs/no-parsing'; convert_byz()/convert_book() | 28 ok |

## Section files

`04a_PA.TXT` (John 7:53-8:11) and `05a_ACT24.TXT` (Acts 24:6-8) are separate pseudo-books in the CCAT and CSV-CCAT datasets. The Strong's and TEI datasets have no counterpart. See decision log D1.

## Known exceptions

| Dataset | Key | Reason |
| --- | --- | --- |
| `source/CCAT` | `LUK 17:36` | The verse reference is present with no text in the base file. The reading is not in the main text here; needs maintainer confirmation (decision log D7). |
| `source/CCAT` | `ACT 8:37` | The verse reference is present with no text in the base file. The reading is not in the main text here; needs maintainer confirmation (decision log D7). |
| `source/CCAT` | `ACT 15:34` | The verse reference is present with no text in the base file. The reading is not in the main text here; needs maintainer confirmation (decision log D7). |
| `source/CCAT` | `ACT 24:7` | Acts 24:6-8 Byzantine expansion lives in 05a_ACT24.TXT; 05_ACT.TXT leaves 24:7 blank by design. |
| `source/Strongs` | `LUK 17:36` | The verse reference is present with no text in the base file. The reading is not in the main text here; needs maintainer confirmation (decision log D7). |
| `source/Strongs` | `ACT 8:37` | The verse reference is present with no text in the base file. The reading is not in the main text here; needs maintainer confirmation (decision log D7). |
| `source/Strongs` | `ACT 15:34` | The verse reference is present with no text in the base file. The reading is not in the main text here; needs maintainer confirmation (decision log D7). |
| `source/Strongs` | `ACT 24:7` | Acts 24:6-8 Byzantine expansion lives in 05a_ACT24.TXT; 05_ACT.TXT leaves 24:7 blank by design. |

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

### csv-unicode/ccat/no-variants

Unicode CSV of CCAT with variants removed.

- **header**: `['chapter', 'verse', 'text']`

Invariants:

- header is chapter,verse,text
- chapter and verse are integers
- text is non-empty
- no duplicate (chapter, verse) keys
- no Beta-code backslashes

### csv-unicode/ccat/with-variants

Unicode CSV of CCAT with variants retained.

- **header**: `['chapter', 'verse', 'text']`

Invariants:

- header is chapter,verse,text
- chapter and verse are integers
- text is non-empty
- no duplicate (chapter, verse) keys
- no Beta-code backslashes

### csv-unicode/strongs/no-parsing

Unicode CSV of the Strong's text with parsing dropped.

- **header**: `['chapter', 'verse', 'text']`

Invariants:

- header is chapter,verse,text
- chapter and verse are integers
- text is non-empty
- no duplicate (chapter, verse) keys

### csv-unicode/strongs/with-parsing

Unicode CSV of the Strong's text with parsing retained.

- **header**: `['chapter', 'verse', 'text']`

Invariants:

- header is chapter,verse,text
- chapter and verse are integers
- text is non-empty
- no duplicate (chapter, verse) keys

### tei-xml-unicode/no-accents

Unaccented TEI-XML export generated from strongs/no-parsing.

- **structure**: `TEI/teiHeader/text/body/div[@type=book]/div[@type=chapter]/ab/w`
- **anchor**: `^B(\d{2})K(\d+)V(\d+)$`

Invariants:

- XML is well-formed
- each file has book divisions with known Bxx ids
- verse anchors are unique and match BxxKxVx
- no empty <w> elements

### tei-xml-unicode/BYZ

Combined TEI-XML of all 27 books.

- **structure**: `same as per-book TEI, with 27 book divisions`
- **anchor**: `^B(\d{2})K(\d+)V(\d+)$`

Invariants:

- covers the same books as the per-book files
