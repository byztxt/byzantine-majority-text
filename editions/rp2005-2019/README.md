# rp2005-2019 - Robinson-Pierpont 2005 lineage, 2019 repo revision

- **Status:** released
- **Basis:** Recovered from git tag v2.0.3 (textonly-beta-code + parsed)
- **Repo releases:** `v1.0.0` to `v2.0.3`

## Layout

- `source/` - frozen source files
- `csv/` - generated Unicode CSV
- `tei/` - generated TEI-XML
- `manifest.json` - provenance and hashes

Accented with/without variants, unaccented, Strong's with/no parsing, and accented/unaccented TEI are recovered or generated from `v2.0.3`. The historical `parsed` source includes apparatus markup; the Strong's views use the main text only.

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

`textonly-beta-code`, `parsed`, the accented CSV (both views), the unaccented CSV, and the unaccented TEI are recovered byte-identically from git tag `v2.0.3`. The accented TEI (from the recovered accented CSV) and the Strong's views (from `parsed`) are generated here; `v2.0.3` itself has no accented TEI. The accented CSV (7968 rows), unaccented CSV (7953 rows), and unaccented TEI **omit** LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7: the rows are absent and there is no empty `<ab/>`, even though the `textonly-beta-code` and `parsed` files in that tag do contain the blank verse lines. The generated accented TEI inherits that omission, while the generated Strong's views include the four verses as empty rows (7957 rows). The recovered artifacts must stay byte-identical, so the rows are deliberately not added back. The other three curated editions keep the verses as empty rows and empty `<ab/>` elements.
