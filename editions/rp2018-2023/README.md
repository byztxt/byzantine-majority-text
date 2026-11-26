<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

# rp2018-2023 - Robinson-Pierpont 2018 with 2023 adjustments (repo release)

- **Status:** released
- **Basis:** Current maintained source; 2018 edition plus 2023 adjustments
- **Repo releases:** `v3.0.0` to `v3.3.4`

## Layout

- `csv/` - generated Unicode CSV
- `tei/` - generated TEI-XML
- `manifest.json` - provenance and hashes

Accented with/without variants, unaccented, Strong's with/no parsing, and accented/unaccented TEI are generated from the committed `data/raw/repo/rp2018-2023/` inputs. `csv/strongs/with-parsing` keeps the Strong's numbers and morphology, `csv/strongs/no-parsing` keeps the numbers and drops the morphology (collapsing consecutive identical numbers for one word), and `csv/unaccented` is plain text with neither.

Curated CSV/TEI filenames use the current book abbreviations
(`MAT`, `MAR`, ...). Historical source files may use the older
official codes (`MT`, `MR`, ...).

This edition contains outputs only. `manifest.json` pins every
input under `data/` by repository-relative path and SHA-256, and
`PYTHONPATH=src python3 -m byz.verify` checks both the inputs and
these artifacts.

`csv/unaccented/` is the plain unaccented text with no
Strong's numbers and no parsing. `csv/strongs/no-parsing/`
keeps the Strong's numbers and drops the `{...}` morphology;
consecutive identical numbers for one word collapse to one,
while distinct alternative numbers stay. `csv/strongs/with-
parsing/` keeps both. The unaccented TEI is generated from
`csv/unaccented/`. The plain-text view and the numbers-only
view were one alias before 2026-11-26; they are now distinct.

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

The manifest separates the Greek-text commit (`source_commit`, from `data/raw/repo/rp2018-2023/ccat`) from the Strong's/parsing commit (`strongs_commit`, from `data/raw/repo/rp2018-2023/strongs`). A pure move updates the recorded commit and no hash. LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 are not part of the Byzantine tradition but are present in `data/raw/repo/rp2018-2023/ccat`/`.../strongs` as blank verse lines. This edition emits them as explicit empty records: 7972 accented CSV rows and 7957 unaccented/Strong's CSV rows, each with four empty rows, and empty `<ab/>` elements in both TEI views.
