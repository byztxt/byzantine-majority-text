# Decisions - Existing corpus contract (Cycle 1)

Adopted by the maintainer on 2026-11-16. These decisions close the open questions
in `requirements.md` and are reflected in `reports/baseline/decision-log.md`.

| ID | Question | Decision | Next step |
| --- | --- | --- | --- |
| D1 | What are `PA` and `ACT24`? | Keep them as separate pseudo-books linked to John 7:53-8:11 and Acts 24:6-8. | Revisit the TEI representation in Cycle 6. |
| D2 | Is the TEI intentionally unaccented? | Yes. `tei-xml-unicode/no-accents` is the main-text export from `strongs/no-parsing`. | Add an accented/apparatus TEI from CCAT in Cycle 6. |
| D3 | How is the current text labelled? | `rp2018` with a `2023-07-20` revision, not a separate edition. | Confirm against the official archive in Cycle 2. |
| D4 | Are the generated CSV/TEI trustworthy? | The source files are authoritative; generated artifacts are unverified derivatives. | Reproduce them byte-for-byte in Cycle 3 before tagging an edition. |
| D5 | Which view wins on disagreement? | The source files win; divergence is a bug to flag. | Enforce in the validators and the pipeline. |
| D6 | Enforce the baseline contract in CI? | Yes, enforce the contract validators/tests now. Do not enforce artifact equality until Cycle 3. | The workflow is prepared at `.github/workflows/baseline-contract.yml`; commit it with a `workflow`-scoped token. |
| D7 | What about LUK 17:36, ACT 8:37, ACT 15:34? | Intentional: these verses are not part of the Byzantine tradition. They are not missing. | The official archives should confirm this in Cycle 2. |
| D8 | Should blank verses be dropped from generated artifacts? | No. Preserve them as empty records so the intent is visible to users. | Implement in Cycle 3 and update the CSV/TEI contract. |

## Notes

- Acts 24:7 is a separate intentional blank; the Byzantine expansion is in
  `05a_ACT24.TXT`.
- D7 means the four blank verse references (`LUK 17:36`, `ACT 8:37`,
  `ACT 15:34`, `ACT 24:7`) must not be treated as missing data. The current
  generated CSV silently drops them; Cycle 3 will keep them as explicit empty
  records.
- For D8, an empty CSV row is straightforward. In TEI, represent an intentionally
  blank verse as an empty `<ab n="..."/>` (or a documented marker), never as an
  empty `<w>`; the TEI contract and validator must be updated to allow it.
