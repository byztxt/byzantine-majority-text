# Validation - Retire the legacy Unicode trees: sources -> pipeline -> editions

A change is complete only when every item below is checked against the actual
files, and the command output or observed diff is recorded here. The
authoritative checklist is `requirements.md` (R1-R10) and `plan.md` (phases
0-6).

The single non-negotiable gate is §3: **the text did not change**. If the
regenerated `rp2018-2023` differs by one byte, stop and report; do not adjust the
edition.

## 1. Preconditions

- [x] Branch is `feature/2026-11-16-edition-recovery-curation`. Do not switch
      branches and do not commit.
- [x] The previous change's uncommitted edits are present and untouched
      (`src/byz/generated.py` banners, `data/provenance/*.toml`,
      `SPECS/TECH.md` §2). Record the starting state:
      `git status --porcelain > /tmp/byz-retire-before.txt`. *(Recorded at
      `/tmp/opencode/byz-review-before.txt`.)*
- [x] Python with `beta-code` importable:
      `python3 -c "import beta_code; print(beta_code.__version__)"`. If 3.10 +
      `scripts/requirements.txt` is unavailable, use a 3.12 venv with
      `beta-code==1.0.0` and record it in §11. *(Python 3.12.3 venv at
      `/tmp/opencode/venv-byz`; the package has no `__version__`, so the pin is
      asserted through `scripts/requirements.txt` and the green suites.)*
- [x] Full git history and tags: `git tag --list v2.0.3 v3.3.4` prints both.
- [x] The six committed archives exist:
      `ls data/raw/_archives/rp2005 data/raw/_archives/rp2018` shows three ZIPs
      each.
- [ ] Snapshot the edition before touching anything:

```bash
find editions/rp2018-2023/source editions/rp2018-2023/csv editions/rp2018-2023/tei \
  -type f -print0 | sort -z | xargs -0 sha256sum > /tmp/byz-edition-before.sha256
sha256sum editions/rp2018-2023/manifest.json | tee /tmp/byz-manifest-before.sha256
git ls-files csv-unicode tei-xml-unicode | wc -l     # expect 145
```

  *(Not repeated in the review pass because the implementation already landed;
  the post-change evidence is `git status --porcelain -- editions` showing only
  the four READMEs and `git ls-files csv-unicode tei-xml-unicode` printing 0.
  Byte identity is re-locked by `test_current_pipeline`.)*
- [x] Move pre-existing untracked files aside only if a generator would copy
      them. After `recover_current()` is inverted (phase 1) nothing copies whole
      legacy directories any more, so
      `csv-unicode/ccat/with-variants/variant_analysis.py` is harmless and will
      be deleted with the tree (record it in §11). The five untracked files
      under `essay/` still enter `reports/baseline/files.csv` if they exist;
      move them aside for the determinism check and restore them afterwards, as
      the previous change did. *(The five `essay/` files were left in place in
      the review pass: the B1 inventory fix excludes untracked files, so they no
      longer enter `files.csv`; see §11.5.)*

## 2. Red phase

Write the tests from `plan.md` phases 1a, 2a, 3, 4a, 5 before changing
production code. Confirm each fails **for the intended reason**, not from an
import error or a typo in the test.

- [ ] `tests/curate/test_current_pipeline.py` fails with `TypeError:
      build_current() got an unexpected keyword argument 'edition_dir'`.
- [ ] After the parameter exists but before the views are written, the gate
      fails on the first missing CSV file (`csv/accented/no-variants/MAT.csv`),
      not on a stray file.
- [ ] `tests/contract/test_integration.py::test_dataset_set` fails with the old
      dataset names in the actual set.
- [ ] `tests/contract/test_coverage.py` fails because `diff_rows` finds no
      `COMPARISONS` rows for the synthetic names.
- [ ] `test_contract_json_matches_the_dataset_names` fails because the six
      legacy-named JSON files are still there.
- [ ] `tests/curate/test_generated.py` fails on the 13-row registry and on the
      two unclassified hand-written docs.
- [ ] The phase 3 doc tests fail on missing files.
- [ ] `LegacyTreesAreGoneTests` fails because both directories still exist.

Record the failing command and the first failing assertion for each.

> Evidence (review pass, 2026-11-20): the implementation predates this review
> pass, so the red phase was not re-run and these boxes stay unchecked. The
> final tests named here exist and are green in `tests/curate` and
> `tests/contract` (with the 3 known pre-commit worktree failures noted in §8).

## 3. The byte-identity gate

### 3.1 Without running a generator (in-memory facts)

Re-confirm the two facts the port relies on, before writing any code:

- [ ] `diff -rq csv-unicode/ccat/no-variants editions/rp2018-2023/csv/accented/no-variants`
      prints nothing (and the same for `with-variants`, `strongs/with-parsing`,
      `strongs/no-parsing`, `strongs/no-parsing` vs `csv/unaccented`, and
      `tei-xml-unicode/no-accents` vs `tei/unaccented`). *(Not runnable in the
      review pass: the left-hand trees are deleted. The equivalent identity is
      now locked by `BuildCurrentByteIdentityTests`.)*
- [ ] `git ls-files csv-unicode tei-xml-unicode | wc -l` is 145. *(It is now 0,
      as intended by §4; the pre-change count was 145.)*

### 3.2 The automated gate

- [x] `PYTHONPATH=src python3 -m unittest tests.curate.test_current_pipeline -v`
      passes, in particular
      `BuildCurrentByteIdentityTests.test_build_current_reproduces_the_committed_views`
      and `test_build_current_is_idempotent` (11 tests, OK).
- [ ] Prove the gate can fail. Temporarily corrupt one thing in a scratch copy
      (for example pass `edition_label` to the unaccented `write_tei`, or change
      one byte of `editions/rp2018-2023/source/CCAT/01_MAT.TXT` in the
      temporary copy the test builds), rerun, and record that the test names the
      offending file. Restore the code afterwards. *(Not repeated in the review
      pass.)*
- [x] The test leaves the repository untouched: `git status --porcelain editions/`
      is unchanged before and after running it (`diff` of the two saved status
      files was silent).

### 3.3 The manual gate, immediately after phase 1 and before any deletion

- [x] `python3 scripts/build_editions.py` completes.
- [ ] `git status --porcelain -- editions/` prints **nothing**. *(It prints the
      four regenerated `editions/*/README.md` files, which `build_editions.py`
      owns; no `source/`, `csv/`, `tei/`, or `manifest.json` path appears.)*
- [ ] `find editions/rp2018-2023/source editions/rp2018-2023/csv editions/rp2018-2023/tei -type f -print0 | sort -z | xargs -0 sha256sum | diff /tmp/byz-edition-before.sha256 -`
      prints nothing. *(No pre-change snapshot was taken in the review pass;
      see the manifest and identity checks instead.)*
- [ ] `sha256sum editions/rp2018-2023/manifest.json` equals
      `/tmp/byz-manifest-before.sha256`. *(Same reason.)*
- [x] `git diff --stat -- editions/rp2018-2023/manifest.json` is empty, so
      every per-file `sha256`/`size` in the manifest is unchanged.
- [x] Spot-check one verse by hand against the frozen book:
      `sed -n '2p' editions/rp2018-2023/csv/accented/with-variants/MAT.csv`
      is still `1,1,"Βίβλος γενέσεως ...`.
- [x] Record the exact commands and the empty output in this document. This
      section is the merge evidence for "no edition byte changed" (see the
      commands in §3.2 above).

## 4. Deletion

- [x] `test -e csv-unicode` and `test -e tei-xml-unicode` both fail (no such
      path); `ls -ld csv-unicode tei-xml-unicode` reports "No such file or
      directory".
- [x] `git ls-files csv-unicode tei-xml-unicode` prints nothing (0 lines).
- [ ] No stub replaced them:
      `git status --porcelain | grep -E 'csv-unicode|tei-xml-unicode'` prints
      nothing, and no untracked file exists at either path. *(The paths are
      gone and there are no untracked files there; `git status` still lists the
      staged `D` rows for the tracked files that were deleted, and the three
      `R` rows for the assets moved to `docs/assets/`.)*
- [x] `test -e scripts/csv_converter.py` and `test -e scripts/tei_xml_converter.py`
      both fail.
- [x] `scripts/requirements.txt` is exactly one line: `beta-code==1.0.0`.
- [x] `grep -rn "import pandas\|import numpy" --include='*.py' .` finds nothing
      outside `.git/`.
- [ ] `grep -rn "csv_converter\|tei_xml_converter" --include='*.py' src scripts tests`
      finds nothing. *(Only the allowlisted absence checks remain:
      `tests/curate/test_current_pipeline.py` and
      `tests/curate/test_editions.py`. `src/` and `scripts/` have none; the
      allowlist is exercised by the R9.3 sweep test.)*
- [x] The three moved assets exist under `docs/assets/` and their SHA-256 equals
      the values recorded from the old paths before the move
      (`sha256sum docs/assets/*`; git records the three as `R` renames, so the
      content is unchanged).
- [x] No content was lost from the two deleted READMEs: the CollateX URLs,
      command, and screenshot reference are in `docs/COLLATEX.md`; the
      multi-parsing note is in `docs/EDITIONS.md`.

## 5. Repointed consumers

- [x] `PYTHONPATH=src python3 -m byz.contract` and
      `PYTHONPATH=src python3 -m byz.reconcile` both exit 0.
- [x] `reports/baseline/files.csv` has no `csv-unicode/` or `tei-xml-unicode/`
      row; it has rows named `editions/rp2018-2023/csv/...`,
      `editions/rp2018-2023/tei/...`, and `docs/assets/...`.
- [x] `docs/contract/` contains `contracts.json` plus exactly one JSON per
      dataset, with names like
      `editions__rp2018-2023__csv__accented__no-variants.json`; the six
      `csv-unicode__*` / `tei-xml-unicode__*` files are gone (9 files total).
- [x] `docs/DATA_CONTRACT.md` Coverage table lists the six new dataset names and
      the same figures as before (29/29/7972/7972 for the two accented views,
      27/27/7957/7957 for the two Strong's views, 27 and 1/27 for the two TEI
      views). `csv/unaccented` is deliberately absent (R5.3); it is validated by
      the identity test instead.
- [ ] `reports/baseline/files.csv` has exactly two fewer rows than before (the
      two deleted folder READMEs in `DOC_FILES`), the same three `docs/assets`
      rows under the new dataset name, and no other change. `summary.md`'s
      "Datasets: 8" and "Invariant findings: 0" are unchanged. *(The two README
      rows are gone and the three `docs/assets` rows are present; the review's
      B1 fix also removes the five untracked `essay/` rows, so the count is 218
      rows rather than the seven-row reduction alone.)*
- [x] `docs/HISTORY.md` dataset table labels are
      `editions/rp2018-2023/csv` and `editions/rp2018-2023/tei`, and their
      "First added" values still include the 2022 TEI and 2023 CSV commits
      (`e9ce9bf`, `97371d7`). No retired working-tree path appears in the
      document.
- [x] Open `reports/reconciliation/summary.md` in a Markdown preview and read
      the per-format tables: the dataset column reads
      `editions/rp2018-2023/csv/strongs/no-parsing` and
      `editions/rp2018-2023/tei/unaccented`, row counts and percentages are
      unchanged (7951/7957, 7953/7957), and the banner is still the first thing
      in the file. *(Checked by reading the file, not by a GUI preview.)*
- [x] `reports/reconciliation/files.csv` and `verses.csv` use only the new
      dataset names; the totals (`7769/7972`, `7811/7972`, the history rows
      7918/7969/7754/7796) are unchanged.
- [x] `tests/reconciliation/test_offline.py::CommittedReportTests` passes, so
      the stable totals are still the stable totals.

## 6. Docs, mapping, and the retired-name rule

- [x] `docs/EDITIONS.md` contains `## Where the old working-tree paths went`,
      the `| Retired path | Now |` table with every row of
      `docs.RETIRED_PATHS`, and the sentence that the bytes did not change.
- [x] `docs/RELEASE-NOTES.md` exists, is banner-free, names the six data paths,
      says the old URLs now 404, and links `EDITIONS.md`.
- [x] `docs/EDITIONS.md` and `docs/RELEASE-NOTES.md` are the only `.md` files
      under `docs/` that contain `csv-unicode/` or `tei-xml-unicode/`.
- [x] The whole-tree check (this is the R9.3 sweep):

```bash
git ls-files | grep -v '^SPECS/' | grep -E '\.(py|md|txt|json|toml)$' |
  while read -r f; do
    grep -l -e 'csv-unicode/' -e 'tei-xml-unicode/' "$f"
  done
```

  Expected offenders, and nothing else:
  `docs/EDITIONS.md`, `docs/RELEASE-NOTES.md`,
  `src/byz/curate/docs.py` (mapping constant),
  `src/byz/curate/recover.py` (`v2.0.3` artifact prefixes),
  `src/byz/contract/history.py` (git pathspecs),
  `tests/curate/test_fidelity.py` (`v2.0.3` prefixes),
  `tests/curate/test_current_pipeline.py` (the allowlist itself).
  Anything else, especially under `.opencode/`, `reports/`, `editions/`, or the
  root `README.md`, fails this check. *(In the uncommitted review tree,
  `docs/RELEASE-NOTES.md` and `tests/curate/test_current_pipeline.py` are still
  untracked, so `git ls-files` lists only the first five; both are allowlisted
  and the sweep test sees them once they are staged. The same sweep now also
  locks the retired converter names; the only offender is the allowlisted
  `tests/curate/test_editions.py`, which asserts their absence.)*
- [x] `.opencode/` describes the real pipeline: no `csv-unicode`,
      `tei-xml-unicode`, `csv_converter.py`, or `tei_xml_converter.py` in any of
      its files.
- [x] `SPECS/TECH.md` §5 describes the finished layout and cites this spec; §2 is
      unchanged from the previous change (`source_page`, November 2026).
- [x] Root `README.md`: "Start here", the layout table, and "Which text should I
      use?" name `editions/rp2018-2023/`; the generated block lists 12 rows and
      no `csv-unicode/` row.
- [x] `scripts/README.md` has no "Csv converter" section and documents only
      `fetch_official.py`, `recover_editions.py`, `build_editions.py`,
      `diff_editions.py`.

## 7. Links

- [x] `python3 -m unittest tests.curate.test_editions.PdfLinkTests -v` passes,
      including the extended doc list (`docs/COLLATEX.md`,
      `docs/RELEASE-NOTES.md`) (2 tests, OK).
- [x] Every relative link in `docs/COLLATEX.md` resolves from `docs/`:
      `assets/coll.png`, `assets/demo_collation.xlsx`,
      `assets/demo_john_1.xml` (the link test resolves them).
- [x] The three external URLs in `docs/COLLATEX.md` are the originals
      (`collatex.net/download`, the INTF `ntvmr.uni-muenster.de` transcript API
      call for `docID=10066`, and the CollateX `-xp '//w'` command line).
- [x] `docs/assets/demo_john_1.xml` is well-formed:
      `python3 -c "import xml.etree.ElementTree as ET; ET.parse('docs/assets/demo_john_1.xml')"`
      (`xml ok`).

## 8. Determinism and the suites

Run the full routine from the repository root, in the documented order:

```bash
python3 scripts/fetch_official.py --verify
python3 scripts/recover_editions.py
python3 scripts/build_editions.py
python3 scripts/diff_editions.py
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m byz.reconcile
```

- [x] Record `git diff --binary > /tmp/byz-retire-run1.diff`; run the routine a
      second time; `git diff --binary > /tmp/byz-retire-run2.diff`;
      `cmp /tmp/byz-retire-run1.diff /tmp/byz-retire-run2.diff` is silent.
      (The diff against `HEAD` is expected to be non-empty; this compares run 1
      with run 2.) *(`/tmp/opencode/byz-review-run1.diff` and `-run2.diff`;
      `cmp` silent. The routine also ran `fetch_official.py` record mode.)*
- [x] `git status --porcelain` after run 2 equals the state after run 1
      (`diff` of the two saved status files was silent).
- [x] No staging directory survives: `ls -a editions/` has no `.rp*` entries.
- [x] `docs/HISTORY.md` has exactly one banner and exactly one
      `<!-- cycle2:begin -->` block after both report commands (`grep -c` gives
      1 and 1).
- [x] The full regeneration changes nothing under `editions/rp2018-2023/{source,csv,tei,manifest.json}`:
      `git status --porcelain editions | grep -v README.md` is empty (exit 1,
      no output).
- [ ] Suites:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests/contract
PYTHONPATH=src python3 -m unittest discover -s tests/curate
PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation
```

  All three pass with 0 failures and 0 unplanned skips. *(Curate: 141 tests OK;
  reconciliation: 64 tests OK; contract: 50 tests with the 3 known
  `ContractWorktreeTests` failures explained below. Counts verified
  2026-11-20.)*
- [x] No test performs network access. The byte-identity test and the contract
      suites read committed files only; `tests/reconciliation` uses the
      committed archives.
- [ ] `tests/curate/test_reproducible.py` and the three `ContractWorktreeTests`
      create a worktree at `HEAD`, so in the uncommitted working tree they
      exercise the old commit. Before committing, treat §8's two-run check as
      authoritative and re-run those two classes after the commit lands in a
      temporary copy (record that in §11). *(`test_reproducible` passes because
      it compares `HEAD` with itself; the three `ContractWorktreeTests` fail on
      the missing banner in the `HEAD` worktree until the change is committed.
      Confirmed 2026-11-20 in a scratch committed copy: the banner failures
      disappear, and one follow-up `byz.contract` + `byz.reconcile` commit
      updates `docs/HISTORY.md` and `reports/baseline/files.csv` for the new
      `HEAD`, after which all 50 contract tests pass.)*

## 9. Manual inspection

- [ ] Open `docs/EDITIONS.md` in a preview. A reader arriving from an old link
      sees "Where the old working-tree paths went" with a table that answers
      "where did my file go", and the links to the PDFs, the diffs, the
      release note, and `COLLATEX.md` all work. *(Read as text and link-checked;
      no GUI preview.)*
- [ ] Open `docs/COLLATEX.md`: the walkthrough still reads as instructions, the
      screenshot renders, and the demo extract is labelled as hand-prepared.
      *(Content and links checked; no GUI preview.)*
- [x] Open `docs/RELEASE-NOTES.md`: the breaking change is unmistakable, and the
      note does not claim anything the repository does not do (no redirects).
- [x] Open `docs/DATA_CONTRACT.md`: the Coverage table and the derivation map
      name the new paths; the "Section files", "Known exceptions", and
      "Intentional blank verses" sections are intact; the demo asset row still
      says `auxiliary` with `docs/COLLATEX.md` as evidence.
- [x] Open an edition README (`editions/rp2018-2023/README.md`): it says the
      views come from the edition's `source/` snapshot, that `source/`
      duplicates `source/` by design, and that `csv/unaccented` and
      `csv/strongs/no-parsing` are two views of one text.
- [x] Open `editions/rp2018-2023/tei/unaccented/MAT.xml` and
      `tei/accented/MAT.xml` side by side: only the accented one carries
      `<edition n="2018 (2023 revision)">Curated edition</edition>`; the
      unaccented one keeps the source header. Both remain well-formed.
- [x] Open the root `README.md`: "Start here" and the layout table no longer
      send a reader to a deleted directory.

## 10. Definition of done

- [x] `build_current()` generates all five `rp2018-2023` CSV views and both TEI
      views from the edition's own `source/`; `recover_current()` copies only
      `source/`.
- [x] The byte-identity gate passed (§3) and is locked by a test that fails when
      one byte changes (`BuildCurrentByteIdentityTests`; the "prove it can fail"
      sub-step was not repeated, see §3.2).
- [x] `csv-unicode/` and `tei-xml-unicode/` are gone, with no stubs or symlinks;
      the two converters are gone; `scripts/requirements.txt` pins only
      `beta-code==1.0.0`.
- [x] Contract, reconciliation, registry, tests, docs, and `.opencode/` all point
      at `editions/rp2018-2023/`; no report or document names a retired
      working-tree path except the allowlist in §6.
- [x] The CollateX material survives in `docs/COLLATEX.md` plus `docs/assets/`
      with working links.
- [x] The two intentional duplications are documented and locked by tests:
      `csv/unaccented` == `csv/strongs/no-parsing`, and
      `editions/rp2018-2023/source` == `source/`.
- [x] `docs/EDITIONS.md` carries the mapping table; `docs/RELEASE-NOTES.md`
      carries the breaking change.
- [ ] A second full regeneration is byte-identical; all three suites pass; no
      text, archive, PDF, manifest hash, or edition CSV/TEI byte changed.
      *(Byte identity holds and curate/reconciliation are green; contract has
      the 3 known pre-commit worktree failures, and nothing under the edition
      artifacts changed.)*
- [x] Every deviation from `plan.md` is recorded in §11 with its reason.

## 11. Deviations log

1. **Environment.** Python 3.10 and the pinned `pandas`/`numpy` are not
   available; the whole sequence and all suites ran in Python 3.12.3 with
   `beta-code==1.0.0` (`/tmp/opencode/venv-byz`). The two converters are gone,
   so nothing imports pandas/numpy any more.
2. **Untracked `essay/` files and `files.csv`.** During the original
   implementation the five untracked `essay/` files were moved aside for the
   determinism run. In the review pass they were left in place, because the
   blocking review finding B1 changed `src/byz/contract/inventory.py` to
   intersect its glob with `git ls-files`: only tracked files reach
   `reports/baseline/files.csv`. The five tracked essay rows remain and the
   five untracked files contribute none. The untracked
   `csv-unicode/ccat/with-variants/variant_analysis.py` disappeared with the
   tree; nothing was copied into an edition.
3. **Pre-commit worktree limitation.** `tests/curate/test_reproducible.py` and
   the three `ContractWorktreeTests` build a worktree at `HEAD`, so they
   exercise the committed text, not the uncommitted change. The two-run check
   in §8 is the authoritative pre-commit evidence; the three contract tests
   fail on the missing banner until the change is committed (the same known
   artefact recorded in the provenance validation).
4. **`parse_cct_accented` correction.** The spec's port section originally said
   the current accented views came from `parse_cct_accented`. That reader
   upper-cases the line through `production_ccat_line`, so the implementation
   added and uses `parse_cct_current` for the all-lowercase `source/CCAT`
   dialect. `requirements.md` and `plan.md` now record the correction and the
   reader's dialect, and `tests/curate/test_build.py` locks MAT 1:1, a blank
   verse, and a `? ` paragraph line.
5. **`files.csv` tracked-only fix (review finding B1).** The committed report
   previously gained five rows from untracked local files, which a clean
   worktree would never reproduce. `inventory.tracked_paths()` now feeds
   `iter_specs`, and `inventory()` passes the set down. Consequence: 218 rows
   including exactly five `essay` rows, and the three `docs/assets` rows.
6. **`recover_editions.py` only stages inputs (review finding N4).**
   `scripts/README.md` and the root README now say so explicitly; the script
   itself is unchanged (`build_editions.py` already re-runs recovery).
7. **Other review fixes.** `build_current()` asserts the canonical book set
   (27 + `PA`/`ACT24` for CCAT), `write_tei(combined=True)` rejects per-book
   titles, `docs/EDITIONS.md` renders multi-target retired rows as separate code
   spans and documents the inherited `Second Timoty`/`Phillipians` titles,
   `_retrieval_window()` derives the retrieval month and timestamps from the
   provenance records, and the doc/spec/`.opencode`/test nits from the review
   are fixed. `.opencode/agents/code-reviewer.md` and
   `.opencode/skills/write-tests/SKILL.md` were updated accordingly.

> **Superseded 2026-11-26:** `docs/EDITIONS.md` no longer documents the
> inherited `Second Timoty`/`Phillipians` titles. Those spellings were corrected
> in the unaccented TEI on 2026-11-26; every title now uses
> `editions.BOOK_NAMES`. See `SPECS/2026-11-26-pr46-review-fixes/`.

8. **Independent verification pass (2026-11-20).** The full sequence ran twice
   with byte-identical `git diff --binary` and status. The edition artifacts are
   unchanged (`git status --porcelain editions/` shows only the four
   `editions/*/README.md`), all 448 edition CSV files parse, and all 224 TEI
   files are well-formed. The deferred `SPECS/2026-11-19-docs-clarity/` items are
   not part of this change: `docs/EDITIONS.md` still renders tags, commits, and
   diff directories as plain code spans, `scripts/README.md` keeps the
   implementation vocabulary in "Report generation order", `SPECS/MISSION.md`
   still says "why category", and `source/Strongs` is still called
   `provenance-unknown` in generated output. Those are follow-ups for the
   docs-clarity spec, not failures of this change.
