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

The recovered source and artifacts are byte-identical to git tag `v2.0.3`. That release's published accented CSV (7968 rows), unaccented CSV (7953 rows), and TEI **omit** LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7: the four rows are absent and no empty `<ab/>` exists for them, even though the `textonly-beta-code` and `parsed` source files in that tag do contain the blank verse lines. The generated Strong's views are built from `parsed`, so they do include the four verses as empty rows (7957 rows). The rows are deliberately **not** added to the recovered accented/unaccented artifacts, because those must stay byte-identical. The other three curated editions keep the verses as empty rows and empty `<ab/>` elements.
