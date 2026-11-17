# rp2018 - Robinson-Pierpont 2018, official print edition

- **Status:** official
- **Basis:** Published in print by VTR, Nuremberg
- **Repo releases:** none (official print edition)
- **Official PDF:** [`robinson-pierpont-2018-gnt-edition.pdf`](https://byzantinetext.com/wp-content/uploads/2021/03/robinson-pierpont-2018-gnt-edition.pdf)

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

The official `.CCT` archive is the accented source; the official ASCII archive supplies the unaccented text. The archive does not contain LUK 17:36, ACT 8:37, ACT 15:34, or ACT 24:7 at all, because those verses are not part of the Byzantine tradition; this is expected, not a conversion loss. The other three curated editions keep those verses as empty CSV rows and empty `<ab/>` TEI elements.
