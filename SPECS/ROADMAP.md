# Roadmap

The roadmap is organised as **cycles**. Each cycle is delivered through one or
more specs under `SPECS/`, using red/green TDD. A cycle is complete when its
acceptance criteria pass in CI and its artifacts are committed.

The overriding goal: clean, provenance-tracked editions (RP2005, RP2018, and
later RP2026), with readable deltas and reproducible CSV/TEI-XML exports.

---

## Cycle 0 - Project setup (complete)

- [x] Project-specific opencode configuration under `.opencode/`.
- [x] Constitution: `SPECS/MISSION.md`, `SPECS/TECH.md`, `SPECS/ROADMAP.md`.
- [x] Record the key decisions: artifacts live in git (`TECH.md` §8), the
  maintainer decides source conflicts (§4), path compatibility is best-effort
  (§5), and RP2026 is deferred to Cycle 7.

---

## Cycle 1 - Existing corpus contract & matrix

**Spec:** `SPECS/2026-11-16-existing-corpus-contract/`.
**Decisions:** `SPECS/2026-11-16-existing-corpus-contract/decisions.md`
(D1-D8, adopted 2026-11-16).
**Status:** Complete (2026-11-16). Verified in `validation.md`; generated
artifacts were regenerated for D8.

**Goal:** get clarity on what is already in the repository before bringing in any
external data. Establish a precise, testable contract and matrix for the current
`source/`, `csv-unicode/`, `tei-xml-unicode/`, and `essay/` contents: formats,
invariants, coverage, derivation relationships, internal inconsistencies, and the
edition/revision the repo currently claims. No external archives are fetched.

**Deliverables**

- Complete inventory of every dataset file (hash, encoding, line endings, last
  commit).
- Machine-readable contract for each dataset/view (CCAT, BP5, four CSV views,
  TEI, `byz.xml`, essay) plus `docs/DATA_CONTRACT.md`.
- Coverage matrix covering every book and section, including `04a_PA` and
  `05a_ACT24`, with chapter/verse counts, gaps, blanks, and duplicates.
- Internal consistency report: every invariant violation with `file:line` and a
  known-exception/decision entry.
- Derivation map (input → output) evidenced by the scripts; the converters were
  run for D8, with the full byte-for-byte reproduction deferred to Cycle 4.
- Internal history map (`docs/HISTORY.md`) for the claimed RP2005/RP2018 and the
  July 2023 update.
- A maintainer decision log for internal ambiguities, now adopted as D1-D8.
- Local test command documented; no GitHub CI (D6).
- D8 implemented: intentionally blank verses are preserved as empty CSV rows and
  empty `<ab/>` TEI elements; the stale 2TI 2:22 and ACT 4:9 outputs were
  corrected during regeneration.

**Acceptance**

- Every dataset is documented and machine-validated.
- Every book/section is accounted for; every violation is visible, not silenced.
- Reports are deterministic; source files are unchanged; generated artifacts were
  regenerated for D8; no external fetch.
- The maintainer can understand the corpus from `reports/baseline/summary.md`
  alone.

**Risks:** source and generated outputs may have silently drifted; `PA`/`ACT24`
semantics may be ambiguous; git history may not establish provenance.

---

## Cycle 2 - Official archive reconciliation

**Spec:** `SPECS/2026-11-16-official-archive-reconciliation/`.
**Status:** Implementation complete on
`feature/2026-11-16-official-archive-reconciliation`; maintainer decisions
R1-R8 pending.

**Goal:** add the official archives and determine, quantitatively, to what extent
the current corpus matches them.

**Inputs:** the official archives recorded in `TECH.md` §2 (2005: preformatted,
ascii, ccat; 2018: ascii, ascii-one-line-per-verse, ccat).

**Deliverables**

- Fetch and checksum every archive; store immutable inputs under
  `data/raw/<edition>/`; write `data/provenance/<edition>.toml`.
- Determine the provenance of `source/Strongs/*.BP5` (none of the listed archives
  is obviously a parsed/Strong's archive).
- A match matrix per edition and format: exact / normalized-only / textual /
  structural / missing / extra, at file, verse, and word level.
- Categorized differences and a plain-language verdict for each edition.
- Updated `docs/PROVENANCE.md` and `docs/HISTORY.md` with external evidence.
- Confirmation that LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 are absent
  from the Byzantine tradition in the official archives (D7), and whether the
  official 2018 archive matches the `2023-07-20` revision (D3).
- A maintainer decision log for every conflict (the pipeline flags; the
  maintainer decides).

**Acceptance**

- Every archive is hashed and recorded; no file is overwritten silently.
- The match extent for the current `source/CCAT`, `source/Strongs`,
  `csv-unicode`, and `tei-xml-unicode` is stated with evidence.
- The maintainer has recorded which state is canonical per edition.
- No source data changed without an explicit decision.

**Risks:** the archives may not match the repo; the 2018 archive may or may not
be the July 2023 revision; Strong's provenance may be unknown; Dropbox links may
expire.

---

## Cycle 3 - Edition recovery, curation & successive diffs

**Spec:** `SPECS/2026-11-16-edition-recovery-curation/`.
**Status:** Complete (2026-11-16). Review fixes implemented on
`feature/2026-11-16-edition-recovery-curation` (PR #46). Verification is
recorded in `validation.md`.
**Note:** moved ahead of the pipeline skeleton because users need stable editions
now. The pipeline refactor follows in Cycle 4.

**Goal:** recover the 2005-lineage text from git, freeze the four editions
(official 2005, released 2005+2019, official 2018, released 2018+2023),
generate CSV and TEI for each, explain the history in docs, and produce
successive-edition diffs.

**Deliverables**

- `editions/{rp2005,rp2005-2019,rp2018,rp2018-2023}/` with `source/`, `csv/`,
  `tei/`, `manifest.json`, and `README.md`.
- `rp2005-2019` recovered from `v2.0.3` (`textonly-beta-code` + `parsed`),
  labelled as the 2019 repo revision of the 2005 lineage.
- Official `rp2005` and `rp2018` frozen from the official PDFs and archives;
  official `rp2018` distinguished from released `rp2018-2023`.
- Official PDFs committed under `data/raw/<edition>/official-pdf/` and recorded
  in `data/provenance/pdfs.toml`; the PDFs are the ultimate source of truth.
- Successive diffs: `rp2005--rp2005-2019`, `rp2005-2019--rp2018`,
  `rp2018--rp2018-2023`, and `rp2005--rp2018`, each with `report.md` and
  `changes.csv`.
- `docs/EDITIONS.md`, root README "Editions" section, per-edition READMEs, and
  updated script/folder READMEs.
- Recovery, build, and diff scripts under `scripts/`, with tests.

**Acceptance**

- All four editions are curated and directly usable without git archaeology.
- Official PDFs are committed, checksummed, and linked; any PDF/archive conflict
  is flagged.
- Release numbers are recorded: `rp2005-2019` = `v1.0.0`-`v2.0.3`;
  `rp2018-2023` = `v3.0.0`-`v3.3.4` (and future tags).
- Every edition has deterministic CSV/TEI and a manifest with hashes.
- Successive diffs are categorized and deterministic.
- The authoritative files under `source/`, `csv-unicode/`,
  `tei-xml-unicode/`, and `essay/` are unchanged. `data/raw/` is additive: this
  cycle commits the official PDFs and the extracted archive inputs under
  `data/raw/<edition>/` (the Cycle 2 deliverables), without modifying the
  existing corpus datasets.

**Risks:** the historical converter may not reproduce old artifacts exactly; the
official `.CCT` parser is new; curated artifacts increase repo size.

---

## Cycle 4 - Pipeline skeleton & test harness

**Goal:** turn the existing converters into a reproducible, tested package
without changing the current output.

**Deliverables**

- `pyproject.toml` with pinned dependencies; `src/byz/` package with parse,
  validate, normalize, transform, and render stages.
- Thin `scripts/` wrappers: `test`, `lint`, `build`, `verify`, `diff`.
- A pytest suite covering Beta-code standardization, parsing, variant extraction,
  and golden output for a small real pericope.
- Determinism check: build twice, compare hashes.
- Baseline: regenerate the current `rp2018-2023` CSV and TEI outputs and prove they are
  byte-identical to the committed artifacts (or document every intended
  difference). Treat the source files as authoritative and flag divergence (D5).
- Keep the D8 empty-record behavior (already implemented: intentional blank
  verses kept as empty CSV rows and empty `<ab/>` TEI elements) in the rewritten
  pipeline.
- Add the local artifact-equality check once the rebuild is proven (D6).

**Acceptance**

- `pytest` is green; tests were written first for each behaviour.
- A clean build reproduces the committed artifacts with no diff.
- Invalid input fails loud with edition/book/chapter/verse context.

---

## Cycle 5 - TEI-XML apparatus

**Goal:** produce a standards-compliant apparatus export.

**Deliverables**

- `<listWit>` witnesses mapped from the variant codes (N/B/C/M/S/E).
- `<app>`, `<lem>`, `<rdg>` with `@wit` and stable `@n` anchors, following TEI P5
  and IGNTP guidelines; the Byzantine text is the lemma witness.
- Validation against the TEI RelaxNG schema in tests.
- A human-readable apparatus view alongside the TEI and CSV outputs.

**Acceptance**

- TEI with apparatus validates against the schema.
- The apparatus round-trips against the CSV with-variants output.
- Coverage tests prove every recorded variant appears exactly once.

---

## Cycle 6 - Release automation & committed artifacts

**Goal:** make every edition easy to download and verify.

**Deliverables**

- Artifacts committed to git per edition, plus release bundles (zip + checksums).
- CI that builds, tests, and asserts `git diff --exit-code` (no drift between a
  clean rebuild and committed artifacts).
- Hardware-independent, timestamp-free builds (`SOURCE_DATE_EPOCH`).
- Release notes generated from manifests and deltas.

**Acceptance**

- Tags/releases exist for `rp2005` and `rp2018` with checksums.
- CI fails on any uncommitted artifact drift.
- A user can download an edition and verify its checksum.

---

## Cycle 7 - RP2026 (future)

**Goal:** add the 2026 edition through the same pipeline, without special cases.

**Prerequisites:** official 2026 source files and their provenance. Do not invent
or extrapolate 2026 data before the files exist.

**Deliverables**

- `data/raw/rp2026/` + provenance record.
- Committed CSV/TEI artifacts and a `rp2026` tag.
- `reports/diff/rp2018--rp2026/` deltas.
- A note in the release history describing what is known about the edition.

**Acceptance**

- RP2026 is reproducible from its official inputs.
- Deltas against RP2018 are committed and categorized.
- No existing edition changes as a side effect.

---

## Cross-cutting backlog

- Documentation of Beta code, variant codes, parsing, and Strong's (consolidate
  from the folder READMEs into `docs/` while keeping the folder READMEs).
- Path-compatibility notes and redirects.
- Software Heritage / archival considerations when paths move.
- A `CHANGELOG.md` driven by manifests and deltas.
- Performance: full-build time and diff time for the whole New Testament.
