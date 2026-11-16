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

## Cycle 1 - Provenance & reconciliation

**Goal:** establish exactly what each existing file is, where it came from, and
how it relates to the official archives.

**Deliverables**

- Download and checksum all official archives listed in `TECH.md` (2005:
  preformatted, ascii, ccat; 2018: ascii, ascii-one-line-per-verse, ccat).
- Store extracted, immutable inputs under `data/raw/<edition>/` and write
  `data/provenance/<edition>.toml` (URLs, SHA-256, dates, notes).
- Determine the provenance of the existing `source/Strongs/*.BP5` separately.
- A reconciliation report comparing official inputs with the current
  `source/CCAT`, `source/Strongs`, `csv-unicode`, and `tei-xml-unicode`, with
  per-file/per-book/per-verse differences and categories.
- A git-history map (`docs/HISTORY.md`): which commits/tags correspond to which
  edition/revision, with evidence.

**Acceptance**

- The maintainer has reviewed the reconciliation report and recorded, per edition,
  which state is canonical (the pipeline flags; the maintainer decides).
- Every input file has a provenance record and a checksum.
- No file was overwritten silently.

**Risks:** the Dropbox archives may not match the repo at all; the Strong's/BP5
files may have no listed archive; 2005/2018 may differ by more than expected.

---

## Cycle 2 - Pipeline skeleton & test harness

**Goal:** turn the existing converters into a reproducible, tested package
without changing the current output.

**Deliverables**

- `pyproject.toml` with pinned dependencies; `src/byz/` package with parse,
  validate, normalize, transform, and render stages.
- Thin `scripts/` wrappers: `test`, `lint`, `build`, `verify`, `diff`.
- A pytest suite covering Beta-code standardization, parsing, variant extraction,
  and golden output for a small real pericope.
- Determinism check: build twice, compare hashes.
- Baseline: regenerate the current RP2018 CSV and TEI outputs and prove they are
  byte-identical to the committed artifacts (or document every intended
  difference).

**Acceptance**

- `pytest` is green; tests were written first for each behaviour.
- A clean build reproduces the committed artifacts with no diff.
- Invalid input fails loud with edition/book/chapter/verse context.

---

## Cycle 3 - Edition slots, snapshots & layout migration

**Goal:** make editions symmetric and navigable, and move to the target layout.

**Deliverables**

- Restructure to `data/raw/<edition>/` and `editions/<edition>/{csv,tei}/` with
  manifests and checksums.
- Freeze `rp2005` and `rp2018` with tags and a `README` download guide.
- Best-effort path compatibility for the current `csv-unicode/` and
  `tei-xml-unicode/` paths; document every move and deprecation.
- Migration spec capturing old-to-new path mapping.

**Acceptance**

- Each edition can be downloaded/checked out and rebuilt.
- Every artifact is listed in a manifest with its hash.
- READMEs and release notes describe the new layout and any path changes.

---

## Cycle 4 - Delta engine

**Goal:** make edition differences readable and trustworthy.

**Deliverables**

- Verse alignment, then word alignment, then categorization.
- `reports/diff/rp2005--rp2018/` with `report.md` (human) and `changes.csv`
  (machine), grouped by book and category (letters, accents/breathings,
  punctuation, capitalization, apparatus, parsing, Strong's, normalization).
- Tests over known differences plus synthetic edge cases (insertions, deletions,
  split words, variant-only changes).

**Acceptance**

- Deltas are deterministic and committed.
- A reviewer can explain each category from the report alone.
- No normalization-only change is misreported as a textual change.

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
