# Plan - Existing corpus contract & matrix (Cycle 1)

Red/green TDD throughout. This cycle is read-only: no external archives, no data
changes. We document and validate what is already here.

## Task group 1 - Branch, skeleton, and test harness

- [ ] Create branch `feature/2026-11-16-existing-corpus-contract` off `master`.
- [ ] Prefer the standard library (`hashlib`, `csv`, `tomllib`, `xml.etree`,
      `difflib`) over new dependencies. If a dependency is genuinely needed, add
      it to `pyproject.toml` and state why.
- [ ] Create `src/byz/contract/` with modules: `inventory.py`, `encoding.py`,
      `ccat.py`, `bp5.py`, `csv_view.py`, `tei_view.py`, `coverage.py`,
      `invariants.py`, `history.py`, `report.py`.
- [ ] Create `tests/contract/`; write the first failing test before each module
      (RED), then implement (GREEN).

## Task group 2 - Complete inventory

- [ ] Inventory every tracked file in `source/`, `csv-unicode/`,
      `tei-xml-unicode/`, `essay/`, `scripts/`, and root docs.
- [ ] Record path, size, SHA-256, line count, encoding, line endings, format
      class, git blob hash, and last-touching commit.
- [ ] Test completeness (file count equals disk count) and determinism.
- [ ] Emit `reports/baseline/files.csv`.

## Task group 3 - Discover and document the record grammars

- [ ] Read `source/README.md`, `scripts/README.md`, `csv-unicode/README.md`,
      `tei-xml-unicode/README.md`, and the converter scripts.
- [ ] Write the CCAT grammar: `chapter:verse` prefix, `? ` paragraph marker,
      Beta code, `{CODE OLD > NEW}` variants, `|`, brackets, multi-word forms.
- [ ] Write the BP5 grammar: `chapter.verse` prefix, `word strongs {parsing}`
      triplets, multi-parsing alternatives.
- [ ] Write the CSV grammars for the four views and the TEI structure (including
      `byz.xml`).
- [ ] Capture the allowed variant codes, parsing-code grammar, and Strong's
      number rules.
- [ ] Encode each grammar as a machine-readable contract in `docs/contract/`.
- [ ] Test the contracts against valid and deliberately invalid fixtures.

## Task group 4 - Coverage matrix

- [ ] Determine book coverage per dataset/view, including `04a_PA` and
      `05a_ACT24`.
- [ ] For each book: chapter count, verse count, min/max chapter and verse, blank
      records, duplicate `(chapter,verse)` keys, and numbering gaps/overlaps.
- [ ] Map `04a_PA` into John and `05a_ACT24` into Acts; confirm whether the main
      files omit those verses (observed: `05_ACT.TXT` leaves 24:7 blank).
- [ ] Build the cross-dataset coverage comparison:
      CCAT ↔ CSV-CCAT, Strongs ↔ CSV-Strongs, Strongs-no-parsing ↔ TEI.
- [ ] Emit `reports/baseline/books.csv` and a table in `summary.md`.
- [ ] Test the coverage logic on fixtures with missing, extra, blank, and
      duplicate verses.

## Task group 5 - Invariants and internal consistency

- [ ] Implement CCAT validators (prefix, braces, variant codes, line structure)
      and tests for each failure mode.
- [ ] Implement BP5 validators (prefix, triplet structure, Strong's integer,
      parsing grammar, multi-parsing) and tests.
- [ ] Implement CSV validators (`chapter,verse,text`, integer types, no NaN/empty
      text, no duplicate keys, no Beta-code leftovers) and tests.
- [ ] Implement TEI validators (well-formedness, expected elements, unique verse
      anchors, `byz.xml` coverage, no empty `<w>`) and tests.
- [ ] Implement cross-dataset checks (sibling book presence, documented absences).
- [ ] Run all validators over the real corpus and emit
      `reports/baseline/invariants.csv`.
- [ ] Every violation is either fixed (only if it is a reporting/doc bug) or
      recorded as a known exception with a reason and decision field. Never
      weaken a check to hide a violation.

## Task group 6 - Derivation map

- [ ] Trace `scripts/csv_converter.py` and `scripts/tei_xml_converter.py` to
      determine input → output relationships.
- [ ] Confirm the observed relationships (e.g. TEI reads
      `csv-unicode/strongs/no-parsing`).
- [ ] Verify coarse derivability: expected output files exist for every input
      book; auxiliary files are documented.
- [ ] Record which relationships require running the converters (deferred to
      Cycle 3) and do not claim correctness without evidence.
- [ ] Add the map to `docs/DATA_CONTRACT.md`.

## Task group 7 - Internal history

- [ ] List tags/releases and map them to RP2005/RP2018 using release notes and
      README statements.
- [ ] For each dataset, find the introduction and last-change commit
      (`git log --follow`, `git log --diff-filter`).
- [ ] Investigate the July 20, 2023 update claim and record supporting commits or
      the absence of evidence.
- [ ] Write `docs/HISTORY.md` with hash/date/message/file-hash evidence.
- [ ] State explicitly where history is insufficient.

## Task group 8 - Reports and decision log

- [ ] Generate `reports/baseline/summary.md` with a plain-language state of the
      corpus, top inconsistencies, and open questions.
- [ ] Generate the machine-readable contract under `docs/contract/`.
- [ ] Build the decision log (internal ambiguities, evidence, options, empty
      maintainer decision field).
- [ ] Ensure deterministic ordering and no timestamps.

## Task group 9 - Validation and handoff

- [ ] Run the full validator suite twice and prove identical reports (hash them).
- [ ] Confirm `git status` shows no changes under `source/`, `csv-unicode/`,
      `tei-xml-unicode/`, or `essay/`.
- [ ] Run the tests; all green.
- [ ] Walk `validation.md` item by item.
- [ ] Present `summary.md` and the decision log to the maintainer.
- [ ] Do not commit; leave the reports/spec for the user to review and commit.

## Explicitly deferred to Cycle 2

- Downloading the official 2005/2018 archives.
- Comparing the current corpus against them.
- Deciding whether changes need to be made.
