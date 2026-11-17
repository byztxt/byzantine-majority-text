# rp2018-2023 - Robinson-Pierpont 2018 with 2023 adjustments (repo release)

- **Status:** released
- **Basis:** Current maintained source; 2018 edition plus 2023 adjustments
- **Repo releases:** `v3.0.0` to `v3.3.4`

## Layout

- `source/` - frozen source files
- `csv/` - generated Unicode CSV
- `tei/` - generated TEI-XML
- `manifest.json` - provenance and hashes

Accented with/without variants, unaccented, Strong's with/no parsing, and accented/unaccented TEI are copied or generated from the current working tree.

Curated CSV/TEI filenames use the current book abbreviations
(`MAT`, `MAR`, ...). Historical source files may use the older
official codes (`MT`, `MR`, ...).

## Derived artifacts

- `csv/accented`
- `csv/accented/no-variants`
- `csv/accented/with-variants`
- `csv/strongs`
- `csv/strongs/no-parsing`
- `csv/strongs/with-parsing`
- `csv/unaccented`
- `tei/accented`
- `tei/accented/BYZ`
- `tei/unaccented`
- `tei/unaccented/BYZ`

## Notes

The manifest separates the Greek-text commit (`source_commit`, from `source/CCAT`) from the Strong's/parsing commit (`strongs_commit`, from `source/Strongs`). LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 are not part of the Byzantine tradition but are present in `source/CCAT`/`source/Strongs` as blank verse lines. This edition emits them as explicit empty records: 7972 accented CSV rows and 7957 unaccented/Strong's CSV rows, each with four empty rows, and empty `<ab/>` elements in both TEI views.
