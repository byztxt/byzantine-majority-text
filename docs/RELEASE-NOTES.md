# Release notes

Hand-maintained. Generated-file changes are described in
[`EDITIONS.md`](EDITIONS.md); this page records changes a reader needs to act
on.

## 2026-11-19 - the legacy Unicode trees were removed

The working-tree convenience trees `csv-unicode/` and `tei-xml-unicode/` were
deleted, together with the two scripts that wrote them
(`scripts/csv_converter.py` and `scripts/tei_xml_converter.py`). They duplicated
the current text that now lives in `editions/rp2018-2023/`, and the edition used
to be copied out of them instead of generated from `source/`.

The old URLs return **404** by design. There are no redirect stubs and no
symlinks. The bytes did not change: only the paths did, and
`editions/rp2018-2023/manifest.json` records the same hashes as before the move.

| Old path | New path |
| --- | --- |
| `csv-unicode/ccat/no-variants/` | `editions/rp2018-2023/csv/accented/no-variants/` |
| `csv-unicode/ccat/with-variants/` | `editions/rp2018-2023/csv/accented/with-variants/` |
| `csv-unicode/strongs/with-parsing/` | `editions/rp2018-2023/csv/strongs/with-parsing/` |
| `csv-unicode/strongs/no-parsing/` | `editions/rp2018-2023/csv/strongs/no-parsing/` |
| `tei-xml-unicode/no-accents/` | `editions/rp2018-2023/tei/unaccented/` |
| `tei-xml-unicode/no-accents/BYZ/byz.xml` | `editions/rp2018-2023/tei/unaccented/BYZ/byz.xml` |
| `tei-xml-unicode/assets/coll.png` | `docs/assets/coll.png` |
| `tei-xml-unicode/assets/demo_collation.xlsx` | `docs/assets/demo_collation.xlsx` |
| `tei-xml-unicode/assets/demo_john_1.xml` | `docs/assets/demo_john_1.xml` |

The three CollateX demo assets moved byte-for-byte to `docs/assets/`, and their
walkthrough is now [`COLLATEX.md`](COLLATEX.md).

The unaccented TEI for `2TI` and `PHP` keeps the inherited titles
`Second Timoty` and `Phillipians`. They are misspellings carried over from the
retired tree; preserving them keeps the edition's TEI bytes unchanged. See
[`EDITIONS.md`](EDITIONS.md) for the note.

The authoritative old-to-new table, including the two removed folder READMEs,
is in [`EDITIONS.md`](EDITIONS.md#where-the-old-working-tree-paths-went).
