# Decision log - baseline contract

Every row is a conflict or ambiguity found in the current corpus. The pipeline
only flags; the maintainer decides.

| ID | Affected paths | Evidence | Options | Maintainer decision |
| --- | --- | --- | --- | --- |
| D1 | `source/CCAT/04a_PA.TXT`, `05a_ACT24.TXT`, `csv-unicode/ccat/*/PA.csv`, `ACT24.csv` | The section files are Byzantine expansions/alternatives that overlap John 8 and Acts 24; they exist only in the CCAT/CSV-CCAT datasets. | (a) Keep as separate pseudo-books. (b) Fold into John/Acts. (c) Treat as apparatus-only. | pending |
| D2 | `tei-xml-unicode/*` | `scripts/tei_xml_converter.py` reads `csv-unicode/strongs/no-parsing`, so the TEI is unaccented and drops parsing. | (a) Intended. (b) TEI should use the CCAT text instead. | pending |
| D3 | `source/`, `csv-unicode/`, `tei-xml-unicode/` | `README.md` claims RP2018 updated 2023-07-20; git history alone may not prove it. | (a) Model as `rp2018`. (b) Model as `rp2018@2023-07-20`. | pending |
| D4 | generated CSV/TEI | They may be stale relative to `source/`. Exact regeneration is deferred to the pipeline cycle. | (a) Treat as current. (b) Regenerate before trusting. | pending |
| D5 | all datasets | Which dataset is authoritative when views disagree. | (a) Source wins. (b) Generated view wins. (c) Maintainer decides per case. | pending |
| D6 | CI | Whether the baseline contract is enforced now or only reported. | (a) Enforce in CI. (b) Report only until external reconciliation. | pending |
| D7 | `source/CCAT/03_LUK.TXT:794`, `source/CCAT/05_ACT.TXT:290,553`; same refs in `source/Strongs` | Verse references have no text (LUK 17:36, ACT 8:37, ACT 15:34). They are not covered by a section file. | (a) Intentional omission. (b) Missing text. (c) Should move to apparatus. | pending |
