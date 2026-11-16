# Decision log - official archive reconciliation

The pipeline flags; the maintainer decides. No source file was changed.

| ID | Question | Evidence | Options | Maintainer decision |
| --- | --- | --- | --- | --- |
| R1 | Which archive is canonical for each edition? | Current `source/CCAT` is closest to 2018; 2005 differs in more verses. | (a) `rp2018` canonical. (b) 2005 canonical. (c) per-file. | pending |
| R2 | Apparatus codes differ from official 2018 (e.g. `C` vs `N` in Acts). | `reports/reconciliation/verses.csv` (category `variant-code`). | (a) Keep current 2023 codes. (b) Adopt official 2018 codes. (c) per-book. | pending |
| R3 | Word segmentation differs (`mhti` vs `mh ti` in 1CO/2CO). | `verses.csv` (category `word-segmentation`). | (a) Keep current. (b) Adopt archive. | pending |
| R4 | Strong's/BP5 provenance. | Status `provenance-unknown`; no parsed archive in the six zips. | (a) Find an official parsed archive. (b) Keep provenance-unknown. | pending |
| R5 | `GREEK.CCT` is documentation, not text. | Inventory shows it is a transliteration key. | (a) Auxiliary. (b) Map elsewhere. | pending |
| R6 | Formatting-only differences (`*[` vs `[*`, dash/ellipsis spacing). | Treated as normalization-only. | (a) Accept as equivalent. (b) Preserve exactly. | pending |
| R7 | Should official 2018 files replace current `source/`? | Current includes post-2018 changes (e.g. apparatus codes). | (a) Keep current. (b) Adopt official. (c) merge per decision R1/R2. | pending |
| R8 | Commit original zips? | They live under gitignored `data/raw/_archives/`; checksums recorded. | (a) Keep out of git. (b) Commit them. | pending |
