# Validation - Edition recovery, curation & successive diffs (Cycle 3)

**Status:** Verified 2026-11-16, with two non-blocking follow-ups noted below.

## 1. Terminology and metadata

- [x] `docs/EDITIONS.md` defines **official** (print by Dr. Robinson) and
      **released** (repo artifact) exactly, and never blurs them.
- [x] The registry lists all four editions with id, status, basis, source
      locations, release range, and latest release.
- [x] Release numbers are read from git tags and match the repo:
      `rp2005-2019` = `v1.0.0`-`v2.0.3`; `rp2018-2023` = `v3.0.0`-`v3.3.4`.
- [x] The official editions are explicitly marked as having no repo release
      number.

## 2. `rp2005-2019` recovery

- [x] The source is recovered from `v2.0.3` (`textonly-beta-code` and `parsed`).
- [x] Every recovered file's SHA-256 matches the corresponding git blob.
- [x] The manifest records the tag `v2.0.3` and commit
      `8ec95671e463030347c2c643358eb56e58235b19`, plus path and hash for every
      recovered file.
- [x] The edition is labelled "2019 repo revision of the 2005 lineage", not the
      official 2005 print edition.
- [x] The recovery report records the comparison: 99.32% vs official 2005,
      99.96% vs official 2018 (`reports/reconciliation/history.csv`,
      `summary.md`, and `docs/PROVENANCE.md`).
- [x] `v2016-07-28` is documented as an earlier, superseded snapshot rather than
      a separate curated edition.

## 3. Official editions

- [x] The official PDFs exist at `data/raw/<edition>/official-pdf/` and their
      SHA-256 matches `data/provenance/pdfs.toml`.
- [x] `docs/EDITIONS.md` and the edition READMEs link to the official PDFs.
- [ ] Any disagreement between an archive/output and a PDF is flagged.
      **Non-blocking:** the PDF-first policy is documented and checksums match,
      but no automated PDF-vs-archive text comparison was performed.
- [x] `rp2005/source/` is byte-identical to `data/raw/rp2005/editions-rp2-ccat`.
- [x] `rp2018/source/` is byte-identical to `data/raw/rp2018/rp2018-ccat`.
- [x] Archive URL, SHA-256, extraction date, and per-file hashes are recorded.
- [x] ASCII/preformatted cross-check material is referenced and documented.
- [x] The docs state that these are official print editions.

## 4. `rp2018-2023`

- [x] The source matches the current tree and the choice is recorded.
- [x] The manifest records first release `v3.0.0`, the latest release, and the
      2023/2026 basis.
- [x] The docs call it a released/unofficial revision, not the official 2018
      print edition.

## 5. Layout and manifests

- [x] All four editions exist under `editions/` with `README.md`,
      `manifest.json`, `source/`, `csv/`, and `tei/`.
- [x] `manifest.json` includes edition id, status, basis, source provenance,
      release range, generation command, and per-file SHA-256; the historical
      edition also records tag and commit.
- [x] No edition writes generated output back into `source/`.

## 6. CSV and TEI generation

- [x] Each edition has a usable main-text CSV and well-formed TEI.
- [x] Variant/parsing views are present where the source supports them:
      official editions have accented with/without variants, unaccented, and
      accented/unaccented TEI; released editions add Strong's with/no parsing.
- [x] The official `.CCT`/ASCII parser is faithful and tested. Production
      conversion uses `official_ccat_line(..., reorder_iota=False)`; the
      comparison normalizer keeps the iota reorder for diff alignment.
- [x] The historical `rp2005-2019` conversion is documented and verified. All
      recovered accented/unaccented CSV and TEI artifacts match `v2.0.3`; the
      generated Strong's/parsing views use the correct UB5 mapping (`q`=θ,
      `y`=ψ), drop TVM numbers, keep the word once for multi-parse entries, and
      strip apparatus markup. They differ from the historical unaccented text in
      only 4 verses (`μητι` vs `μη τι`), matching the known segmentation
      difference.
- [x] A golden `MAT 1:1` test exists for every edition.
- [x] A clean rebuild produces identical output hashes.
- [x] Conversion failures are loud and name the book/verse: unmatched `.CCT`
      lines raise, and unexpected UB5 tokens or unparsed apparatus markup raise.

## 7. Successive diffs

- [x] Diffs exist for:
      `rp2005--rp2005-2019`, `rp2005-2019--rp2018`,
      `rp2018--rp2018-2023`, and `rp2005--rp2018`.
- [x] Each diff has `report.md` and `changes.csv`.
- [x] Changes are categorized and counted; examples are included.
- [x] Encoding/normalization-only differences are not reported as textual
      change (the comparison reorder is applied only on the comparison side).
- [x] Diffs are deterministic across two runs.
- [x] Known changes were spot-checked.
- [x] The diff basis is recorded: source-tier main text, not generated CSV/TEI.

## 8. Documentation and discoverability

- [x] `docs/EDITIONS.md` explains the four editions, release numbers, PDFs, and
      the messy-history story without requiring git archaeology.
- [x] Root `README.md` has a "Curated editions" section linking to both
      `docs/EDITIONS.md` and `editions/`.
- [x] Each edition has its own `README.md`.
- [x] `scripts/README.md` documents the recovery, build, and diff scripts.
- [x] `source/README.md`, `csv-unicode/README.md`, and
      `tei-xml-unicode/README.md` point to the curated editions and explain the
      working-tree vs archive distinction.
- [x] The source feature matrix records that `parsed` (v2.0.3) contains
      apparatus markup; the derived Strong's views use the main text only.

## 9. Scripts and reproducibility

- [x] `scripts/recover_editions.py`, `scripts/build_editions.py`, and
      `scripts/diff_editions.py` run from the repo root.
- [x] They require no network once `data/raw/` is present.
- [x] Commands and expected outputs are documented.
- [x] Tests run offline (the accented `.CCT` test needs the pinned Python 3.10
      environment and is skipped otherwise).

## 10. Safety and definition of done

- [x] `git status` shows no changes under `source/`, `csv-unicode/`,
      `tei-xml-unicode/`, `essay/`, or `data/raw/` (only the folder README
      pointers are updated).
- [x] Test suites pass (`tests/curate`, `tests/contract`,
      `tests/reconciliation`).
- [x] Manifests and reports are deterministic.
- [ ] The maintainer has reviewed `docs/EDITIONS.md`, the manifests, and the
      diff reports. **Pending:** maintainer review.
- [x] Open questions in `requirements.md` are resolved and recorded; the diff
      basis is source-tier.
- [x] The plan's task groups are complete, or deviations are recorded here.

## Verification run - 2026-11-16

Commands:

```bash
/tmp/opencode/venv/bin/python scripts/build_editions.py
python3 scripts/diff_editions.py
PYTHONPATH=src python3 -m unittest discover -s tests/contract
PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation
PYTHONPATH=src python3 -m unittest discover -s tests/curate
```

Results:

- 22 curate tests pass (one accented-conversion test runs under the pinned
  Python 3.10 environment), plus 40 contract and 25 reconciliation tests.
- All 57 recovered `rp2005-2019` source files match `git show v2.0.3:...`.
- Official `.CCT` source counts: `rp2005` 29, `rp2018` 30; both match
  `data/raw/`.
- PDF SHA-256 values match `data/provenance/pdfs.toml`.
- Release ranges match git tags.
- Every edition has the expected derived views from the source feature matrix.
- The historical Strong's/parsing views differ from the historical unaccented
  text in only 4 `μητι` / `μη τι` verses.
- Diffs: 54, 3, 161, 55 verses for the four pairs; deterministic.
- A clean rebuild produced identical hashes.
- `source/`, `csv-unicode/`, `tei-xml-unicode/`, `essay/`, and `data/raw/`
  remain untouched (except README pointers).

### Resolved review findings

- Swapped θ/ψ and malformed historical Strong's tokens: fixed; no stray
  numbers/braces, no apparatus markup, multi-parse word appears once.
- Official accented iota-subscript corruption: fixed via
  `reorder_iota=False` for production conversion.
- Manifest tag/commit: added.
- Golden and parser regression tests: added.
- Loud conversion failures: added.
