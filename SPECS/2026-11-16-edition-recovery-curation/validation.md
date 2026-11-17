# Validation - Edition recovery, curation & successive diffs (Cycle 3)

**Status:** Verified 2026-11-16; review fixes implemented and verified
2026-11-17 on `feature/2026-11-16-edition-recovery-curation` (PR #46). The final
verifier pass on 2026-11-17 passed every regeneration, determinism, historical
fidelity, manifest, and test-suite check; its one blocking fidelity finding
(dash spacing after final sigma in the two official editions) was fixed and is
recorded as resolved below. Two non-blocking maintainer-review items remain.

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
      conversion goes through `normalize.production_ccat_line()`, which reads
      capitalisation from the original mixed-case token (so glued apparatus
      codes such as `.{B` are not treated as capitals), renders all-uppercase
      apparatus abbreviations such as `_DAD` as Greek capitals (`—ΔΑΔ`), and
      rewrites the official iota-before-accent ordering (`mimnh|/skh|`) to the
      ordering the beta-code library needs (`μιμνῄσκῃ`). `official_ccat_line()`
      keeps its comparison-only default behaviour, including the iota reorder,
      so the committed reconciliation reports stay valid.
- [x] The historical `rp2005-2019` conversion is documented and verified. All
      recovered accented/unaccented CSV and TEI artifacts match `v2.0.3`; the
      generated Strong's/parsing views use the correct UB5 mapping (`q`=θ,
      `y`=ψ), drop TVM numbers, skip the historical `0` spurious-Strong's
      placeholder, keep the word once for multi-parse entries, and strip
      apparatus markup. They differ from the historical unaccented text in only
      4 verses (`μητι` vs `μη τι`), matching the known segmentation difference.
- [x] A golden `MAT 1:1` test exists for every edition.
- [x] A clean rebuild produces identical output hashes.
- [x] Generated CSV uses Unix (LF) line endings even where the copied
      historical/current views keep their original line endings.
- [x] Accented TEI emits a standalone `-` as `<pc>-</pc>` and a leading `¶` as
      `<milestone unit="paragraph" type="start"/>`; the unaccented TEI has neither
      token and is unaffected.
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

- 24 curate tests pass (one accented-conversion test runs under the pinned
  Python 3.10 environment), plus 40 contract and 25 reconciliation tests.
  *(2026-11-17 correction: the "25 reconciliation tests pass" claim does not
  reproduce in a clean clone. Six of those tests call `compare.run()`, which
  needs the git-ignored `data/raw/_archives/**/*.zip`, so a fresh clone gets six
  `FileNotFoundError`s. They are now skipped with a loud message, and offline
  replacements were added; see the 2026-11-17 run below.)*
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

- Swapped θ/ψ, spurious `0` Strong's placeholders, and malformed historical
  Strong's tokens: fixed; no stray numbers/braces, no apparatus markup,
  multi-parse word appears once.
- Official accented iota-subscript corruption: fixed in production via
  `normalize.production_ccat_line()` (2026-11-17; the earlier
  `reorder_iota=False` call was incomplete and produced `μιμνῃ ́σκῃ`).
- Manifest tag/commit: added; the current-edition `source_commit` now comes from
  `source/CCAT` (with `strongs_commit` from `source/Strongs`) so a README-only
  commit cannot masquerade as a text change.
- Golden and parser regression tests: added.
- Loud conversion failures: added.

## Verification run - 2026-11-17 (PR #46 review fixes)

Commands, run from the repository root with the pinned Python 3.10 environment:

```bash
python3 scripts/recover_editions.py
python3 scripts/build_editions.py
python3 scripts/diff_editions.py
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m unittest discover -s tests/curate
PYTHONPATH=src python3 -m unittest discover -s tests/contract
PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation
```

### Tests

- `tests/curate`: 58 tests pass.
- `tests/contract`: 44 tests pass.
- `tests/reconciliation`: 41 tests run (35 pass, 6 skipped), with the six
  archive-dependent integration tests skipped with `official archives not
  fetched: run python3 scripts/fetch_official.py --verify`. The offline
  replacements cover the six pinned SHA-256 values and the committed report
  totals.
- The legacy `scripts/csv_converter.py` and `scripts/tei_xml_converter.py` were
  re-run and `csv-unicode/` and `tei-xml-unicode/` are byte-identical to
  `HEAD`.

### Blast radius of the production-conversion fix

Compared with the previously committed `editions/rp2005` and `editions/rp2018`
(`csv/accented/no-variants` and `csv/accented/with-variants`), the only verse
texts that changed are:

- `rp2005`, no-variants: MAR 14:65, LUK 9:22.
- `rp2005`, with-variants: the same two verses plus the 18 Revelation apparatus
  verses (REV 3:7, 4:4, 4:10, 5:5, 5:8, 7:5, 7:6, 7:7, 7:8, 11:2, 11:16, 13:18,
  14:1, 14:3, 14:20, 19:4, 21:17, 22:16).
- `rp2018`, no-variants: the same two verses plus HEB 2:6, HEB 13:3, 2TI 1:6,
  2PE 1:12, ROM 15:15.
- `rp2018`, with-variants: those seven plus the 18 Revelation verses.

`csv/unaccented` is unchanged for both editions; the only other CSV difference
is the generated line endings (LF).

### Dash analysis (review claim corrected; final-sigma regression resolved)

The review claim that the converter "adds spaces before dashes" is a false
positive: the official `.CCT` main text uses spaced dashes throughout (both
archives contain zero attached `word- ` dashes once apparatus blocks and
`GREEK.CCT` are excluded), and the converter never inserts a space before a
dash.

However, the inherited historical converter contains an unconditional
`ς -` -> `ς-` rewrite (present since `97371d7`). It affected every main-text
dash whose preceding word ends in final sigma. A genuinely attached source dash
renders with a medial sigma (`σ-`), never `ς-`, so every `ς-` in the generated
official text came from a spaced source dash. The production path in
`src/byz/curate/build.py::parse_cct_accented` now restores the source spacing
with `re.sub(r"ς-(?=\s|$)", "ς -", text)` after beta-code conversion. The
legacy converter, `csv-unicode/`, and the recovered `v2.0.3` artifacts are
untouched.

The fix changed 29 verses per official edition in both accented CSV views (and
the corresponding accented TEI `<ab>` elements), by inserting the missing space
and nothing else:

`MAT 9:6; MAR 2:10; LUK 5:24, 23:50; JOH 1:14, 1:42, 4:1, 7:50, 21:7; ACT 1:17,
1:19, 4:36, 10:36, 13:8; ROM 1:13; 2CO 2:5, 5:7, 6:1, 6:2, 9:4; GAL 2:7;
COL 2:21, 4:10; HEB 7:20, 10:8, 11:38; REV 16:14, 21:25`.

`2CO 9:4` has two dashes, so the 29 verses contain 30 dashes. The verifier's
count of "18 dashes" scanned `ς- ` followed by a space and therefore missed the
12 end-of-verse dashes (`1CO 16:15; 2CO 5:7, 6:1, 6:2; ACT 1:17, 1:19, 10:36;
COL 2:21; GAL 2:7; JOH 4:1; LUK 23:50; REV 16:14`), which the same source and
converter issue also affected. The `v2.0.3` accented CSV already keeps all of
them spaced (e.g. `ἑαυτούς -`), confirming the correct rendering.
`rp2005-2019`, `rp2018-2023`, `csv-unicode/`, and `tei-xml-unicode/` are
unchanged. New tests pin the 17 named verses plus the end-of-verse cases, a
corpus-wide "no attached main-text dash" invariant over both accented views, and
the TEI token split (`<w>πατρός</w>`, `<pc>-</pc>`, `<w>πλήρης</w>`).

### Determinism, history, and artifacts

- Two full runs of recover → build → diff → contract produce byte-identical
  `editions/`, `reports/diffs/`, `docs/EDITIONS.md`, `README.md`,
  `reports/baseline/`, and `docs/contract/`. A subprocess test enforces this.
- `python -m byz.contract` twice produces no diff. It now emits the static
  `v2016-07-28` paragraph itself and preserves the
  `<!-- cycle2:begin -->…<!-- cycle2:end -->` block verbatim; the duplicate
  "External archive evidence" stub was removed, so contract → reconcile keeps
  exactly one heading and one block.
- `reports/baseline/files.csv` was stale and has been regenerated; a second run
  produces no diff. `reports/baseline/summary.md` now states that the commit
  column lags by one commit.
- The historical artifacts remain byte-identical to tag `v2.0.3`: 30 `.CCT`,
  27 `.UB5`, 29+29 accented CSV, 27 unaccented CSV, and 27 unaccented TEI all
  match the tag (checked in `tests/curate/test_fidelity.py`). The 54 generated
  Strong's CSVs changed only in line endings (CRLF → LF).
- `rp2005-2019` still omits LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7
  (7953 unaccented rows vs 7957), matching `v2.0.3`; this is now documented in
  `docs/EDITIONS.md` and the edition README rather than "fixed" by adding rows.
- `manifest.json` hashes and sizes were checked against every listed file for
  all four editions.

### Safety and documentation

- `recover` builds into a hidden sibling staging tree and swaps it in only after
  recovery succeeds, so a failed `git archive` leaves the existing edition
  intact (tested).
- `fetch` rejects non-https and non-Dropbox URLs, caps downloads at 50 MB,
  rejects absolute/`..` zip members, and verifies every archive against the
  pinned SHA-256 (all tested).
- `editions.release_range()` now raises a clear error if `git tag --list` fails
  or if a *released* edition has no matching tags; official editions still
  return `""`.
- Generated CSV uses LF; accented TEI emits `<pc>` for standalone punctuation
  and a paragraph `<milestone>` for `¶`.
- `SPECS/ROADMAP.md` marks Cycle 3 complete, and its acceptance wording now says
  that `data/raw/` is additive (Cycle 2 deliverables) while the existing
  corpus datasets stay unchanged.

## Final verifier pass - 2026-11-17

Worktree `/tmp/opencode/pr46`, HEAD `9b75447`, clean before and after; pinned
Python 3.10 (pandas 1.4.2, beta-code 1.0.0).

Commands, from the repository root:

```bash
python scripts/recover_editions.py
python scripts/build_editions.py
python scripts/diff_editions.py
PYTHONPATH=src python -m byz.contract
PYTHONPATH=src python -m unittest discover -s tests/curate
PYTHONPATH=src python -m unittest discover -s tests/contract
PYTHONPATH=src python -m unittest discover -s tests/reconciliation
```

### Regeneration and determinism

- Two complete recover -> build -> diff -> contract runs were compared by
  SHA-256 over every file under `editions/`, `reports/`, and `docs/`: 887 files
  were byte-identical, and `git status` stayed clean after both runs.
- `tests/curate`: 58 pass; `tests/contract`: 44 pass; `tests/reconciliation`:
  41 run, 6 skipped, 35 pass. The six skips are all in
  `tests/reconciliation/test_integration.py` and need the git-ignored
  `data/raw/_archives/**/*.zip` plus `scripts/fetch_official.py --verify`.
- The legacy `scripts/csv_converter.py` and `scripts/tei_xml_converter.py`
  were re-run in a throwaway copy of the worktree; `csv-unicode/` (113 files)
  and `tei-xml-unicode/` (32 files) were byte-identical to the committed tree.

### Output inspection

- `rp2005` and `rp2018` accented CSV: MAR 14:65 `ἔβαλλον`, LUK 9:22
  `ἀναστῆναι`; `rp2018` HEB 2:6 `μιμνῄσκῃ`; `rp2018`
  with-variants REV 3:7 `—ΔΑΔ`. No orphan combining mark after whitespace in
  any main text CSV or TEI; no apparatus markup in main-text views; no
  all-uppercase main-text runs.
- **Resolved (official-edition fidelity):** the historical converter's
  unconditional `ς -` -> `ς-` rewrite affected 29 verses per official edition in
  `csv/accented/{no-variants,with-variants}` and the corresponding accented TEI
  `<ab>` elements (30 dashes; the verifier's "18" counted only `ς- ` followed by
  a space). The production path now restores the source's spaced dash, and the
  corpus-wide invariant finds zero attached main-text dashes in either accented
  view. `rp2005-2019`, `rp2018-2023`, `csv-unicode/`, and `tei-xml-unicode/` are
  unchanged. See the dash analysis above.
- `editions/rp2005-2019`: 30 `.CCT`, 27 `.UB5`, 29+29 accented CSV, 27
  unaccented CSV, and all 27 unaccented TEI books plus `BYZ/byz.xml` are
  byte-identical to `v2.0.3`. The accented TEI and the Strong's views are
  generated here (`v2.0.3` has no accented TEI). The generated Strong's views
  have 7957 rows, no `0` placeholder, and include the four blank verses.
- `rp2005/source/ccat` and `rp2018/source/ccat` are byte-identical to their
  `data/raw/` archives; `rp2018-2023/source/` is byte-identical to the current
  `source/CCAT` and `source/Strongs`. PDF SHA-256 values match
  `data/provenance/pdfs.toml`.
- All 224 TEI files under `editions/` (and the 29 legacy TEI files) are
  well-formed. Manifest hashes and sizes match every listed file for all four
  editions; no absolute paths, hostnames, or timestamps were found in the
  manifests, reports, or generated docs.
- `docs/HISTORY.md` contains exactly one `<!-- cycle2:begin -->` block and one
  "External archive evidence (Cycle 2)" heading, plus the `v2016-07-28`
  paragraph; a second contract run produces no diff. `reports/baseline/*` is
  current (222 inventory rows; hashes and sizes match the tree).
- `source/`, `csv-unicode/`, `tei-xml-unicode/`, and `essay/` have no content
  changes versus `master` (only their README pointers changed); `data/raw/` is
  additive and unchanged.

### Remaining

- The maintainer has not yet reviewed `docs/EDITIONS.md`, the manifests, and the
  diff reports.
- The archive-dependent reconciliation checks cannot be re-run offline; the
  committed reports were produced with the archives present.

