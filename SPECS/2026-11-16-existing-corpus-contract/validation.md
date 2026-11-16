# Validation - Existing corpus contract & matrix (Cycle 1)

A cycle is complete only when every item below is verified against the actual
files and reports, not against intent. Attach evidence (paths, hashes, commands,
report excerpts) to each check.

## 1. Inventory

- [ ] Every tracked file in `source/`, `csv-unicode/`, `tei-xml-unicode/`,
      `essay/`, `scripts/`, and the root docs appears in
      `reports/baseline/files.csv`.
- [ ] Inventory counts equal the files on disk (no silent omissions).
- [ ] Encoding and line endings are recorded per file, not guessed.
- [ ] Inventories are deterministic across two runs.
- [ ] Each file has a git blob hash and last-touching commit.

## 2. Dataset contract

- [ ] `docs/DATA_CONTRACT.md` covers every dataset and view:
      `source/CCAT`, `source/Strongs`, the four CSV views, TEI per-book,
      `BYZ/byz.xml`, the TEI asset, and the essay.
- [ ] Each contract states purpose, claimed provenance, naming, encoding,
      grammar, allowed values, invariants, derivation, and known exceptions.
- [ ] The machine-readable contracts in `docs/contract/` are consumed by the
      validators (not dead documentation).
- [ ] The CCAT and BP5 grammars are formal enough to reject malformed lines.
- [ ] Allowed variant codes (N/B/C/M/S/E) and the parsing/Strong's rules are
      documented.

## 3. Coverage matrix

- [ ] `reports/baseline/books.csv` lists every book and section for every
      dataset/view.
- [ ] `04a_PA` and `05a_ACT24` are explicitly mapped into John and Acts, with
      their presence/absence in each dataset explained.
- [ ] Per book: chapter count, verse count, min/max chapter and verse, blank
      records, duplicate keys, and gaps/overlaps are reported.
- [ ] Cross-dataset comparisons (CCAT↔CSV-CCAT, Strongs↔CSV-Strongs,
      Strongs-no-parsing↔TEI) are present and explained.
- [ ] Missing, extra, and single-dataset books are called out, not averaged away.

## 4. Invariants and internal consistency

- [ ] CCAT, BP5, CSV, and TEI validators exist and are tested on valid and
      invalid fixtures for every invariant.
- [ ] Every violation appears in `reports/baseline/invariants.csv` with
      `file:line` and a category.
- [ ] Every violation is either fixed (reporting/doc only) or recorded as a known
      exception with a reason and an empty maintainer decision.
- [ ] No check was weakened to hide a violation; the diff of validator rules
      shows only additions/clarifications.
- [ ] Spot-check at least five reported violations against the raw files and
      confirm them.

## 5. Derivation map

- [ ] The map in `docs/DATA_CONTRACT.md` cites the script code that establishes
      each input→output relationship.
- [ ] The TEI source is confirmed (observed: `csv-unicode/strongs/no-parsing`).
- [ ] Coarse derivability is verified (expected files exist for every input book;
      auxiliary files are documented).
- [ ] Relationships that require running the converters are explicitly deferred
      to Cycle 3 and not asserted as correct.

## 6. Internal history

- [ ] `docs/HISTORY.md` maps tags/releases and key commits to RP2005/RP2018 with
      hash/date/message evidence.
- [ ] The introduction and last-change commits of each dataset are identified.
- [ ] The July 20, 2023 update claim is tied to evidence or explicitly marked
      unverified.
- [ ] Points where history is insufficient are stated (no guessing).

## 7. Determinism and safety

- [ ] Two runs produce byte-identical reports.
- [ ] `git status` shows no modifications under `source/`, `csv-unicode/`,
      `tei-xml-unicode/`, or `essay/`.
- [ ] No external archive was fetched.
- [ ] No file was moved, deleted, or normalized in place.
- [ ] No canonical dataset was selected automatically.
- [ ] Tests run offline and pass.

## 8. Decision log

- [ ] Every internal ambiguity has a row with: id, affected paths, evidence,
      options, and an empty "maintainer decision" field.
- [ ] The decision log is presented to the maintainer.
- [ ] Recorded decisions are added to `docs/DATA_CONTRACT.md` and the relevant
      contract files.

## 9. Definition of done

- [ ] `docs/DATA_CONTRACT.md`, `docs/HISTORY.md`, and `docs/contract/` exist.
- [ ] `reports/baseline/{summary.md,files.csv,books.csv,invariants.csv}` exist.
- [ ] Test suite green; tooling deterministic; data untouched; no external fetch.
- [ ] The maintainer has a plain-language summary of the corpus and the decision
      log.
- [ ] The plan's task groups are complete, or every deviation is recorded here.
