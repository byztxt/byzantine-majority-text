<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

# Decision log - official archive reconciliation

The pipeline flags; the maintainer decides. No source file was changed.

| ID | Question | Evidence | Options | Maintainer decision |
| --- | --- | --- | --- | --- |
| R1 | Which archive is canonical for each edition? | Current `source/CCAT` is closest to 2018; 2005 differs in more verses. | (a) `rp2018` canonical. (b) 2005 canonical. (c) per-file. | pending |
| R2 | Apparatus codes differ from official 2018 (e.g. `C` vs `N` in Acts). | `reports/reconciliation/verses.csv` (category `variant-code`). | (a) Keep current 2023 codes. (b) Adopt official 2018 codes. (c) per-book. | pending |
| R3 | Word segmentation differs (`mhti` vs `mh ti` in 1CO/2CO). | `verses.csv` (category `word-segmentation`). | (a) Keep current. (b) Adopt archive. | pending |
| R4 | Strong's/BP5 provenance. | `source/Strongs/*.BP5` are Dr Robinson's official parsed files (`source/README.md`); no parsed archive is among the six ZIPs, so the delivery route is not recorded. | (a) Find an official parsed archive. (b) Leave the files labelled unknown. | resolved (2026-11-19): the files are official Robinson material; only the delivery route for the parsed files is unrecorded. |
| R5 | `GREEK.CCT` is documentation, not text. | Inventory shows it is a transliteration key. | (a) Auxiliary. (b) Map elsewhere. | pending |
| R6 | Formatting-only differences (`*[` vs `[*`, dash/ellipsis spacing). | Treated as normalization-only. | (a) Accept as equivalent. (b) Preserve exactly. | pending |
| R7 | Should official 2018 files replace current `source/`? | Current includes post-2018 changes (e.g. apparatus codes). | (a) Keep current. (b) Adopt official. (c) merge per decision R1/R2. | pending |
| R8 | Commit original zips? | They live under `data/raw/_archives/`; checksums are recorded in `data/provenance/*.toml`. | (a) Keep out of git. (b) Commit them. | adopted (2026-11-17): commit the six original zips under `data/raw/_archives/` for posterity and offline reproducibility; `fetch_official.py --verify` checks the committed copies. |
| R9 | Which historical state is the 2005 edition? | `v2.0.3 textonly-beta-code` is a 2019 revision of the 2005 edition; it matches official 2018 (99.96%) more closely than official 2005 (99.32%). The current source is the 2023 2018 text, first added in `97371d7` and merged in `v3.0.0`. | (a) Use the official 2005 archive as the 2005 edition. (b) Use `v2.0.3` (the repo's 2019 revision). (c) Keep both, clearly labelled. | pending |
