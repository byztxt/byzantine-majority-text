<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

# Decision log - baseline contract

Adopted by the maintainer on 2026-11-16. The pipeline flags; the maintainer decides.

| ID | Question | Decision | Next step |
| --- | --- | --- | --- |
| D1 | What are `PA` and `ACT24`? | Keep them as separate pseudo-books linked to John 7:53-8:11 and Acts 24:6-8. | Revisit the TEI representation in Cycle 6. |
| D2 | Is the TEI intentionally unaccented? | Yes. `editions/rp2018-2023/tei/unaccented` is the plain unaccented main-text export from `csv/unaccented`. | Add an accented/apparatus TEI from CCAT in Cycle 6. |
| D3 | How is the current text labelled? | A separate curated edition, `rp2018-2023`, based on the 2018 edition with the `2023-07-20` revision. | Recorded in `docs/EDITIONS.md`; confirm against the official archive in Cycle 2. |
| D4 | Are the generated CSV/TEI trustworthy? | The source files are authoritative. The generated artifacts were stale in 2TI 2:22 and ACT 4:9 and have been regenerated. | Full byte-for-byte pipeline check in Cycle 3. |
| D5 | Which view wins on disagreement? | The source files win; divergence is a bug to flag. | Enforce in the validators and the pipeline. |
| D6 | Enforce the baseline contract in GitHub CI? | No GitHub CI. Run the contract validators/tests locally. Do not enforce artifact equality until Cycle 3. | Local test command documented; no workflow. |
| D7 | What about LUK 17:36, ACT 8:37, ACT 15:34? | Intentional: these verses are not part of the Byzantine tradition. | The official archives should confirm this in Cycle 2. |
| D8 | Should blank verses be dropped from generated artifacts? | No. They are preserved as empty records: empty CSV text and empty `<ab/>` in TEI. | Implemented 2026-11-16; artifacts regenerated. |

Note: Acts 24:7 is a separate intentional blank; the Byzantine expansion is in
`05a_ACT24.TXT`. The PA/ACT24 section files are the only pseudo-books without a
Strong's/TEI counterpart.
