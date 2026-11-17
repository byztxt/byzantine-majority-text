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

The source and every recovered artifact are byte-identical to git tag `v2.0.3`. That release predates the intentional blank verses, so it omits LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 entirely: the unaccented CSV has 7953 rows instead of 7957 and the TEI has no empty `<ab/>` for them. The rows are deliberately **not** added here, because the historical artifacts must stay byte-identical. The other three curated editions preserve those verses as empty rows and empty `<ab/>` elements.
