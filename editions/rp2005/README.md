# rp2005 - Robinson-Pierpont 2005, official print edition

- **Status:** official
- **Basis:** Published in print by Chilton Book Publishing, Southborough, Massachusetts
- **Repo releases:** none (official print edition)
- **Official PDF:** [`editions-rp2.pdf`](https://byzantinetext.com/wp-content/uploads/2016/11/editions-rp2.pdf)

## Layout

- `source/` - frozen source files
- `csv/` - generated Unicode CSV
- `tei/` - generated TEI-XML
- `manifest.json` - provenance and hashes

Accented CSV (with/without variants) and accented TEI are generated from the official `.CCT` source. Unaccented CSV and TEI are generated from the official ASCII. Strong's and parsing are not included because the official archives do not contain them.

Curated CSV/TEI filenames use the current book abbreviations
(`MAT`, `MAR`, ...). Historical source files may use the older
official codes (`MT`, `MR`, ...).

## Derived artifacts

- `csv/accented`
- `csv/accented/no-variants`
- `csv/accented/with-variants`
- `csv/unaccented`
- `tei/accented`
- `tei/accented/BYZ`
- `tei/unaccented`
- `tei/unaccented/BYZ`

## Notes

The official `.CCT` archive is the accented source; the official ASCII archive supplies the unaccented text. Both archives contain LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 as **blank verse lines**, because those verses are not part of the Byzantine tradition. This edition therefore emits them as explicit empty records: the accented CSV has 7972 rows and the unaccented CSV 7957, each with four empty rows, and both TEI views contain empty `<ab/>` elements for the four verses.
