# Requirements - Existing corpus contract & matrix (Cycle 1)

## Context

Before touching the official archives, we need clarity on what is already in this
repository. The repo contains authoritative-looking source files, generated CSV,
generated TEI-XML, an essay, and converter scripts, but there is no explicit
contract describing each dataset, its format, its coverage, or which outputs are
supposed to derive from which inputs. There are also internal oddities: the CCAT
source has `04a_PA` and `05a_ACT24` section files, while the Strong's and TEI
datasets do not; `05_ACT.TXT` leaves Acts 24:7 blank while `05a_ACT24.TXT`
supplies the Byzantine expansion; the TEI is generated (per `scripts/`) from the
unaccented `strongs/no-parsing` CSV, not from the accented CCAT. None of this is
written down as a testable contract.

This cycle establishes that contract and an internal matrix. It does **not**
fetch or compare the external official archives; that is the next cycle.

## Goal

Produce a precise, testable contract and matrix for the corpus as it exists
today: what each dataset is, what its format and invariants are, how the datasets
relate, what is covered, what is inconsistent, and what edition/revision the repo
currently claims. No data is changed and no external source is used.

## Non-goals

- Fetching, unzipping, or diffing the official 2005/2018 archives (Cycle 2).
- Building the full parse/render pipeline (Cycle 3).
- Restructuring or moving `source/`, `csv-unicode/`, or `tei-xml-unicode/`.
- Fixing data inconsistencies. We document and flag them; the maintainer decides.
- Deciding which external edition is canonical.
- Ingesting RP2026.

## Inputs

The current tracked working tree and its git history, specifically:

- `source/CCAT/*.TXT`, `source/Strongs/*.BP5`, `source/README.md`
- `csv-unicode/ccat/{no-variants,with-variants}/*.csv`
- `csv-unicode/strongs/{no-parsing,with-parsing}/*.csv`
- `csv-unicode/README.md`
- `tei-xml-unicode/no-accents/*.xml`, `tei-xml-unicode/no-accents/BYZ/byz.xml`,
  `tei-xml-unicode/assets/*`, `tei-xml-unicode/README.md`
- `essay/*.qmd`, `essay/README.md`
- `scripts/*.py`, `scripts/beta_to_unicode_custom/`, `scripts/README.md`,
  `scripts/requirements.txt`, `scripts/tei_xml_header.xml`
- `README.md`, `LICENSE`
- git tags, releases, and commit history

## Definitions

- **Dataset**: a group of files with one format and one purpose, e.g.
  `source/CCAT`, `csv-unicode/strongs/with-parsing`, `tei-xml-unicode/no-accents`.
- **View**: a variant of a dataset (with/without variants, with/without parsing).
- **Record**: a verse (CCAT/BP5/CSV) or a TEI `<ab>`.
- **Unit**: a file, a book, a chapter, a verse, a word, a variant marker, a parsing
  code, or a Strong's number.
- **Invariant**: a rule that every record in a dataset must satisfy.
- **Known exception**: a documented, maintainer-visible violation that is not
  silently ignored.
- **Coverage**: which books/chapters/verses and section files exist in a dataset.
- **Internal evidence**: READMEs, scripts, release notes, and git history. Not
  external archives.

## Functional requirements

### R1 - Complete repository inventory

- Inventory every tracked file in `source/`, `csv-unicode/`, `tei-xml-unicode/`,
  `essay/`, `scripts/`, plus the root docs.
- For each: path, size, SHA-256, line count, detected encoding, line endings,
  format class, git blob hash, and last-touching commit.
- The inventory must be complete (counts equal files on disk) and deterministic.

### R2 - Dataset contract

For every dataset and view, document:

- purpose and claimed provenance (from the READMEs), and whether that claim is
  internally verifiable;
- file naming scheme and book ids;
- encoding and line endings;
- the record grammar (for CCAT and BP5), including the `NN:NN` / `NN.NN`
  prefixes, `{...}` variant syntax, word/Strong's/parsing triplets, and
  multi-parsing alternatives;
- CSV columns and types; TEI elements/attributes and their expected structure;
- allowed values: variant codes (N/B/C/M/S/E), parsing codes, Strong's numbers;
- invariants (see R4);
- derivation relationships: which outputs are produced from which inputs
  (evidenced by `scripts/`);
- known exceptions.

The contract must be machine-readable (`docs/contract/`), consumed by the
validators, not just prose.

### R3 - Coverage matrix

Build a matrix that answers, at file/book/chapter/verse level:

- which books and section files are present in each dataset;
- how `04a_PA` and `05a_ACT24` map into John and Acts, and why they exist only in
  the CCAT/CSV-CCAT datasets;
- per book: chapter count, verse count, min/max chapter and verse, blank records,
  duplicate verse keys, and non-contiguous numbering;
- cross-dataset coverage: `source/CCAT` vs `csv-unicode/ccat`,
  `source/Strongs` vs `csv-unicode/strongs`,
  `csv-unicode/strongs/no-parsing` vs TEI;
- what is missing, extra, or only present in one dataset.

Output both a human-readable table and a machine-readable CSV.

### R4 - Internal consistency and invariants

Validate and report every violation, with `file:line` and a category. At minimum:

- **CCAT source**: every non-blank line starts with a valid `chapter:verse`
  reference; variant braces are balanced; variant codes are in the allowed set;
  no unmapped artefacts; books and sections are accounted for.
- **BP5 source**: every non-blank line starts with `chapter.verse`; each word is
  followed by a Strong's number and a parsing code; parsing codes are structurally
  valid; multi-parsing alternatives are well formed; no orphan tokens.
- **CSV**: parses; header is exactly `chapter,verse,text`; chapter/verse are
  integers; no NaN/empty text except documented exceptions; no duplicate
  `(chapter,verse)` keys; no stray Beta code in Unicode outputs.
- **TEI**: well-formed XML; expected book/chapter/`ab`/`w` structure; verse anchors
  unique and consistent with the CSV source; `byz.xml` covers the same books as
  the per-book files; no empty `<w>`.
- **Cross-dataset**: every book in one view has the expected counterpart in its
  sibling views, or is documented as intentionally absent (e.g. PA/ACT24).

Each violation is either fixed (only if it is a read-only documentation/report
bug) or recorded as a known exception with a reason and a maintainer decision
field. Do not hide violations by weakening a check.

### R5 - Derivation map

- Document, with script evidence, which outputs derive from which inputs.
- Verify coarse derivability now: every input book has its expected output files,
  and every output file traces to an input or is documented as auxiliary
  (e.g. `assets/demo_john_1.xml`).
- State which relationships can only be verified by running the converters, and
  defer that exact check to Cycle 3. Do not claim a derivation is correct without
  evidence.

### R6 - Internal edition/revision history

- Map tags/releases and key commits to the claimed editions (RP2005, RP2018) using
  release notes, README statements, and commit messages.
- Locate the commits that introduced and last changed each dataset.
- Investigate the claim in `README.md` that the text is the 2018 edition updated
  as of July 20, 2023, and record the supporting (or missing) evidence.
- Write `docs/HISTORY.md` with commit hashes, dates, messages, and file hashes.
- State explicitly where internal evidence is insufficient.

### R7 - Reports and decision log

- `docs/DATA_CONTRACT.md` - the human-readable contract.
- `docs/HISTORY.md` - internal history map.
- `docs/contract/<dataset>.json` - machine-readable contract.
- `reports/baseline/summary.md` - plain-language state of the corpus, including
  the most important inconsistencies and open questions.
- `reports/baseline/files.csv` - inventory.
- `reports/baseline/books.csv` - coverage matrix.
- `reports/baseline/invariants.csv` - every violation and known exception.
- A decision log listing every internal ambiguity with evidence, options, and an
  empty "maintainer decision" field.

### R8 - Tests and validators (red/green TDD)

- Write the failing test first for every validator.
- Test each validator against valid and invalid fixtures for every invariant.
- Run the validators over the real corpus; record known exceptions explicitly.
- Reports must be deterministic (stable ordering, no timestamps).
- Tests run offline and use no external data.

### R9 - Safety

- Do not fetch external archives in this cycle.
- Do not modify, move, normalize, or delete any file under `source/`,
  `csv-unicode/`, `tei-xml-unicode/`, or `essay/`.
- Do not silently normalize data to make a check pass.
- Do not select canonical datasets automatically.

## Deliverable layout

```
docs/
  DATA_CONTRACT.md
  HISTORY.md
  contract/<dataset>.json
reports/baseline/
  summary.md
  files.csv
  books.csv
  invariants.csv
src/byz/contract/...
tests/contract/...
```

## Acceptance criteria

- Every dataset and view has a documented, machine-readable contract.
- The coverage matrix accounts for every file, book, and section, including
  `04a_PA` and `05a_ACT24`.
- Every internal inconsistency is listed with `file:line`, a category, and a
  known-exception/decision entry. Nothing is silently ignored.
- The derivation map is documented with script evidence, with unverifiable
  relationships explicitly deferred.
- `docs/HISTORY.md` maps the internal edition history with commit evidence, and
  states where evidence is missing.
- Validators and tests are green; reports are deterministic.
- No data file changed and no external archive was fetched.
- The maintainer can read `reports/baseline/summary.md` and understand the state
  of the corpus without reading code.

## Open questions (resolved in `decisions.md`)

All questions below were adopted on 2026-11-16; see `decisions.md` for D1-D8.



1. What is the intended semantic contract for `04a_PA` and `05a_ACT24`? Are they
   Byzantine expansions intentionally omitted from the main CCAT line, and why do
   they have their own CSV files but no Strong's/TEI counterparts?
2. Which dataset is authoritative when views disagree: the source, or the
   generated CSV/TEI?
3. Is the TEI intentionally unaccented because it derives from
   `strongs/no-parsing`? Confirm the intended relationship.
4. Is the current corpus RP2018, or RP2018 plus the July 2023 corrections, or a
   mix? Which files carry the corrections?
5. Are the committed CSV/TEI artifacts actually in sync with the current source,
   or are some stale?
6. Should the baseline contract be enforced in CI from now on, or only reported
   until the external reconciliation is done?

## Risks

- The corpus may contain silent drift between source and generated outputs.
- `PA`/`ACT24` semantics may be ambiguous; misclassifying them would corrupt the
  contract.
- Encoding/line-ending differences may create noise; treat these as their own
  category.
- Git history may be insufficient to establish provenance; unresolved points must
  be stated, not guessed.
