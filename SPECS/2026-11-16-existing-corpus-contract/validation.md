# Validation - Existing corpus contract & matrix (Cycle 1)

**Status:** Complete and verified on 2026-11-16.

Evidence and commands:

```bash
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m unittest discover -s tests/contract -v
```

Result: 40 tests pass, 0 invariant findings, 0 cross-dataset coverage differences,
140 derivations present, 1 auxiliary asset, reports deterministic across two runs.

## 1. Inventory

- [x] Every tracked file in `source/`, `csv-unicode/`, `tei-xml-unicode/`,
      `essay/`, `scripts/`, and the root docs appears in
      `reports/baseline/files.csv`.
- [x] Inventory counts equal the files on disk (no silent omissions).
- [x] Encoding and line endings are recorded per file, not guessed.
- [x] Inventories are deterministic across two runs.
- [x] Each file has a git blob hash and last-touching commit.

## 2. Dataset contract

- [x] `docs/DATA_CONTRACT.md` covers every dataset and view:
      `source/CCAT`, `source/Strongs`, the four CSV views, TEI per-book,
      `BYZ/byz.xml`, the TEI asset, and the essay.
- [x] Each contract states purpose, claimed provenance, naming, encoding,
      grammar, allowed values, invariants, derivation, and exceptions.
- [x] The machine-readable contracts in `docs/contract/` are consumed by the
      validators (not dead documentation).
- [x] The CCAT and BP5 grammars are formal enough to reject malformed lines.
- [x] Allowed variant codes (N/B/C/M/S/E) and the parsing/Strong's rules are
      documented.

## 3. Coverage matrix

- [x] `reports/baseline/books.csv` lists every book and section for every
      dataset/view.
- [x] `04a_PA` and `05a_ACT24` are explicitly mapped into John and Acts, with
      their presence/absence in each dataset explained.
- [x] Per book: chapter count, verse count, min/max chapter and verse, blank
      records, duplicate keys, and gaps/overlaps are reported.
- [x] Cross-dataset comparisons (CCAT↔CSV-CCAT, Strongs↔CSV-Strongs,
      Strongs-no-parsing↔TEI) are present and explained.
- [x] Missing, extra, and single-dataset books are called out, not averaged away.

## 4. Invariants and internal consistency

- [x] CCAT, BP5, CSV, and TEI validators exist and are tested on valid and
      invalid fixtures for every invariant.
- [x] Every violation appears in `reports/baseline/invariants.csv` with
      `file:line` and a category. After D7/D8, intentional blanks are modeled as
      allowed, so the final report has 0 findings.
- [x] Every pre-D8 violation was resolved by the adopted decisions: the eight
      blank-record findings (four verses × CCAT/Strongs) are intentional and are
      now preserved as empty records in the generated outputs.
- [x] No check was weakened to hide a violation; the validators were tightened
      to allow exactly the four intentional blanks and to reject any other empty
      verse (including an unexpected empty `<ab>` in TEI).
- [x] The eight pre-D8 findings were spot-checked against the raw source lines
      (`LUK 17:36`, `ACT 8:37`, `ACT 15:34`, `ACT 24:7`) and confirmed.

## 5. Derivation map

- [x] The map in `docs/DATA_CONTRACT.md` cites the script code that establishes
      each input→output relationship.
- [x] The TEI source is confirmed (`csv-unicode/strongs/no-parsing`).
- [x] Coarse derivability is verified: all 140 expected files exist and
      `demo_john_1.xml` is documented as auxiliary.
- [x] The converters were run for the D8 regeneration. The outputs now match the
      source coverage; the full byte-for-byte pipeline reproduction remains a
      Cycle 3 task (D4).

## 6. Internal history

- [x] `docs/HISTORY.md` maps tags/releases and key commits to RP2005/RP2018 with
      hash/date/message evidence.
- [x] The introduction and last-change commits of each dataset are identified.
- [x] The July 20, 2023 update claim is tied to evidence (commits `16859b2`,
      `18ea8e9`, `a6d4c1e`) or explicitly marked unverified where history is
      silent.
- [x] Points where history is insufficient are stated (no guessing).

## 7. Determinism and safety

- [x] Two runs produce byte-identical reports.
- [x] No modifications were made to `source/` or `essay/`.
- [x] `csv-unicode/` and `tei-xml-unicode/` were regenerated from source for D8;
      the changes are committed and limited to the four intentional blanks plus
      the two stale parsing corrections.
- [x] No external archive was fetched.
- [x] No source file was moved, deleted, or normalized in place.
- [x] No canonical dataset was selected automatically.
- [x] Tests run offline and pass.

## 8. Decision log

- [x] Every internal ambiguity has a row with id, affected paths, evidence,
      options, and an adopted decision.
- [x] The decision log was presented to the maintainer and adopted (D1-D8).
- [x] Recorded decisions are added to `docs/DATA_CONTRACT.md`, `decisions.md`, and
      the contract files.

## 9. Definition of done

- [x] `docs/DATA_CONTRACT.md`, `docs/HISTORY.md`, and `docs/contract/` exist.
- [x] `reports/baseline/{summary.md,files.csv,books.csv,invariants.csv}` exist.
- [x] Test suite green; tooling deterministic; source untouched; no external fetch.
- [x] The maintainer has a plain-language summary of the corpus and the decision
      log.
- [x] The plan's task groups are complete; deviations are recorded here and in
      `decisions.md` (D8 was implemented during this cycle rather than deferred).

## Final verification result

- Tests: 40 passing.
- Invariant findings: 0.
- Cross-dataset coverage differences: 0.
- Derivations: 140 ok, 1 auxiliary.
- Determinism: identical report hashes across two runs.
- D8 regeneration: LUK 17:36, ACT 8:37, ACT 15:34, ACT 24:7 preserved as empty
  CSV rows and empty `<ab/>` TEI elements.
- Regeneration also corrected stale parsing artifacts in 2TI 2:22 and ACT 4:9 to
  match the source.
