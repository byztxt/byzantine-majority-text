# Validation - Edition recovery, curation & successive diffs (Cycle 3)

A cycle is complete only when every item below is verified against the actual
files, manifests, and reports.

## 1. Terminology and metadata

- [ ] `docs/EDITIONS.md` defines **official** (print by Dr. Robinson) and
      **released** (repo artifact) exactly, and never blurs them.
- [ ] The registry lists all four editions with id, status, basis, source
      locations, release range, and latest release.
- [ ] Release numbers are read from git tags and match the repo:
      `rp2005-2019` = `v1.0.0`-`v2.0.3`; `rp2018-2023` = `v3.0.0`-`v3.3.4`.
- [ ] The official editions are explicitly marked as having no repo release
      number.

## 2. `rp2005-2019` recovery

- [ ] The source is recovered from `v2.0.3` (`textonly-beta-code` and `parsed`).
- [ ] Every recovered file's SHA-256 matches the corresponding git blob.
- [ ] The manifest records tag, commit, path, and hash.
- [ ] The edition is labelled "2019 repo revision of the 2005 lineage", not the
      official 2005 print edition.
- [ ] The recovery report records the comparison: 99.32% vs official 2005,
      99.96% vs official 2018.
- [ ] If `v2016-07-28` is not preserved, the omission is documented.

## 3. Official editions

- [ ] The official PDFs exist at `data/raw/<edition>/official-pdf/` and their
      SHA-256 matches `data/provenance/pdfs.toml`.
- [ ] `docs/EDITIONS.md` and the edition READMEs link to the official PDFs.
- [ ] Any disagreement between an archive/output and a PDF is flagged, not
      resolved silently.
- [ ] `rp2005/source/` is byte-identical to `data/raw/rp2005/editions-rp2-ccat`.
- [ ] `rp2018/source/` is byte-identical to `data/raw/rp2018/rp2018-ccat`.
- [ ] Archive URL, SHA-256, extraction date, and per-file hashes are recorded.
- [ ] ASCII/preformatted cross-check material is referenced or retained and
      documented.
- [ ] The docs state that these are official print editions.

## 4. `rp2018-2023`

- [ ] The source matches the chosen current tree or latest release, and the
      choice is recorded.
- [ ] The manifest records first release `v3.0.0`, latest release, and the
      2023/2026 basis.
- [ ] The docs call it a released/unofficial revision, not the official 2018
      print edition.

## 5. Layout and manifests

- [ ] All four editions exist under `editions/` with `README.md`,
      `manifest.json`, `source/`, `csv/`, and `tei/`.
- [ ] `manifest.json` includes edition id, status, basis, source provenance,
      release range, generation command, and per-file SHA-256.
- [ ] No edition writes generated output back into `source/`.

## 6. CSV and TEI generation

- [ ] Each edition has a usable main-text CSV and a well-formed TEI main-text
      export.
- [ ] Variant/parsing views are present where the source supports them.
- [ ] The official `.CCT`/ASCII parser is faithful and tested; it is not the
      reconciliation normalizer.
- [ ] The historical `rp2005-2019` conversion method is documented and verified
      against the historical artifacts.
- [ ] A golden pericope test exists for every edition.
- [ ] A clean rebuild produces identical output hashes.
- [ ] Conversion failures are loud and name the edition/book/verse.

## 7. Successive diffs

- [ ] Diffs exist for:
      `rp2005--rp2005-2019`, `rp2005-2019--rp2018`, `rp2018--rp2018-2023`,
      `rp2005--rp2018`.
- [ ] Each diff has `report.md` and `changes.csv`.
- [ ] Changes are categorized and counted; examples are included.
- [ ] Encoding/normalization-only differences are not reported as textual
      change.
- [ ] Diffs are deterministic across two runs.
- [ ] Known changes are spot-checked and correct.

## 8. Documentation and discoverability

- [ ] `docs/EDITIONS.md` explains the four editions, the release numbers, and
      the messy-history story without requiring git archaeology.
- [ ] Root `README.md` has an "Editions" section linking to `docs/EDITIONS.md`
      and `editions/`.
- [ ] Each edition has its own `README.md`.
- [ ] `scripts/README.md` documents the recovery, build, and diff scripts.
- [ ] `source/README.md`, `csv-unicode/README.md`, and
      `tei-xml-unicode/README.md` point to the curated editions and explain the
      working-tree vs archive distinction.

## 9. Scripts and reproducibility

- [ ] `scripts/recover_editions.py`, `scripts/build_editions.py`, and
      `scripts/diff_editions.py` run from the repo root.
- [ ] They require no network once `data/raw/` is present.
- [ ] Commands and expected outputs are documented.
- [ ] Tests are red/green and run offline.

## 10. Safety and definition of done

- [ ] `git status` shows no changes under `source/`, `csv-unicode/`,
      `tei-xml-unicode/`, `essay/`, or `data/raw/`.
- [ ] Test suites pass (`tests/curate`, plus the existing suites).
- [ ] Manifests and reports are deterministic.
- [ ] The maintainer has reviewed `docs/EDITIONS.md`, the manifests, and the
      diff reports.
- [ ] Open questions in `requirements.md` are resolved and recorded.
- [ ] The plan's task groups are complete, or every deviation is recorded here.
