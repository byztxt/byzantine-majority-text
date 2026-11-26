# Validation - Provenance source page and generated-file banners

A change is complete only when every item below is checked against the actual
files. Record command output excerpts and the observed diff in this document.
Do not run `--force`; it replaces the 2026-11-16 retrieval timestamps and the
recorded final Dropbox URLs.

## 1. Preconditions

- [x] Branch is `feature/2026-11-16-edition-recovery-curation`; do not switch or
      commit.
- [ ] Python 3.10 with `pip install -r scripts/requirements.txt`. *(Not met:
      Python 3.10 is unavailable and pandas does not build on 3.12. Ran in
      `/tmp/opencode/venv-byz` with Python 3.12 and `beta-code==1.0.0`; see
      §12.1.)*
- [x] Full git history and tags, at least `v2.0.3`
      (`git tag --list v2.0.3` prints `v2.0.3`).
- [x] The six committed archives are present:
      `ls data/raw/_archives/rp2005 data/raw/_archives/rp2018` shows three ZIPs
      each.
- [x] Record any pre-existing untracked files before starting, for example
      `git status --porcelain > /tmp/byz-before.txt`. The tree may contain
      unrelated untracked essay/CSV files; the clean-tree checks below apply to
      tracked files and to generated paths, not to those pre-existing entries.
      *(Recorded at `/tmp/opencode/byz-review-before.txt`; the five untracked
      `essay/` files were left in place, see §12.2.)*

## 2. Red phase

Write the tests from `plan.md` task groups 1, 2, 6, 7, and 9 before changing
production code. Confirm each fails for the intended reason, not an import
error in the test itself:

- [ ] `tests/curate/test_generated.py` fails because `byz.generated` does not
      exist.
- [ ] `tests/reconciliation/test_fetch.py::test_write_provenance_puts_source_page_on_every_record`
      fails with a missing-key/`KeyError` or a TOML without `source_page`.
- [ ] `test_existing_records_ignores_comment_lines_even_with_equals` fails
      because a `# note = value` line is parsed as a record field.
- [ ] `test_record_mode_adds_source_page_and_preserves_previous_metadata` fails
      because the rewritten TOML has no `source_page`.
- [ ] The banner presence tests fail on the first unmodified generated file.
- [ ] `tests/curate/test_reproducible.py` still passes at this point; it becomes
      the lock after implementation.

Record the failing command and the first failing assertion for each.

> Evidence (review pass, 2026-11-20): the implementation predates this review
> pass, so the red phase was not re-run. The red-phase checks are therefore
> left unchecked here. The tests named above exist and are green in the current
> tree (§9); `tests/curate/test_reproducible.py` passes and is the lock.

## 3. Green phase and regeneration routine

Run from the repository root, in this order:

```bash
# 1. Provenance: validate, then re-record offline from the committed zips.
python3 scripts/fetch_official.py --verify
python3 scripts/fetch_official.py

# 2. Curated editions and diffs.
python3 scripts/recover_editions.py
python3 scripts/build_editions.py
python3 scripts/diff_editions.py

# 3. Reports. Contract first, reconciliation second (scripts/README.md).
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m byz.reconcile
```

- [x] `--verify` exits 0 before and after record mode.
- [x] Record mode performs no network access because `--verify` just passed. If
      it ever calls `download`, stop: the archives are missing or corrupt. The
      unit test mocks `download` to raise if called in the matching-archive
      case.
- [x] Record mode leaves `data/raw/` unchanged (the extracted trees already
      exist, so nothing is re-extracted). `git status --porcelain -- data/raw`
      prints nothing.
- [x] `docs/HISTORY.md` ends with exactly one `<!-- cycle2:begin -->` block and
      begins with exactly one banner (`grep -c` gives 1/1/1).
- [ ] The root README's hand-written prose above and below
      `<!-- editions:begin -->` is unchanged; only the block content changed.
      *(Not true after the review's N4 fix: the runbook comment and the
      paragraph after it were updated to say `recover_editions.py` only freezes
      inputs. The generated block itself still round-trips:
      `docs.render_root_readme(readme_text) == readme_text`.)*

## 4. Expected diff shape

Inspect, do not just trust the exit code:

```bash
git diff --stat
git diff data/provenance/rp2005.toml data/provenance/rp2018.toml
git diff -- docs/PROVENANCE.md SPECS/TECH.md README.md
```

- [x] Each provenance TOML diff adds exactly three banner lines at the top and
      exactly one `source_page = "https://byzantinetext.com/study/editions/robinson-pierpont/"`
      line after each `format` line (3 per file, 6 total). `git diff --stat`
      shows `7 +++++++` per file (three banner lines, one blank, three
      `source_page` lines).
- [x] No `sha256`, `size`, `http_status`, `downloaded`, `final_url`,
      `requested_url`, `download_url`, or `extracted` value changed.
- [x] `data/provenance/pdfs.toml` is not in the diff.
- [x] `docs/PROVENANCE.md` adds the listing page and the derived month
      (`November 2026`, from the recorded `downloaded` values) as generated
      prose; it is not hand-edited afterwards.
- [x] `SPECS/TECH.md` §2 names the listing page in addition to the Dropbox URLs.
- [ ] No file under `data/raw/`, `source/`, `csv-unicode/`,
      `tei-xml-unicode/`, `editions/*/source/`, `editions/*/csv/`,
      `editions/*/tei/`, or `editions/*/manifest.json` appears in the diff.
      *(`data/raw/` and every edition artifact directory are clean;
      `source/README.md` is modified by the companion retire change, not by
      this provenance change.)*

## 5. Banner checks

- [x] Exactly 17 generated Markdown files start with
      `<!-- generated-file: do not edit by hand -->`:

```bash
find docs editions reports -name '*.md' | sort | while read -r f; do
  head -1 "$f"
done
```

  Expected: 4 generated `docs/*.md`, 4 `editions/*/README.md`, 5
  `reports/diffs/**/*.md`, 2 `reports/baseline/*.md`, 2
  `reports/reconciliation/*.md`. After the companion retire change, `docs/`
  holds **6** `.md` files: the four generated ones above plus the two
  hand-maintained docs (`COLLATEX.md`, `RELEASE-NOTES.md`) that deliberately
  carry no banner. The `head -1` sweep prints 17 marker lines plus
  `# Release notes` and `# Using CollateX with the Byzantine text`.
- [x] Each file's second line is `> **Generated file. Do not edit by hand.**`,
      and the original first line (for example `# Editions`) is separated from
      the banner by one blank line.
- [x] The banner renders as a visible blockquote on GitHub and in a Markdown
      preview, not only as an HTML comment (`tests/curate/test_generated.py`
      asserts the marker plus the blockquote line).
- [x] Root `README.md`: `<!-- editions:begin -->` is immediately followed by
      `<!-- generated-block: do not edit by hand -->`, then the blockquote
      containing `hand-written` and `python3 scripts/build_editions.py`.
- [x] `data/provenance/rp2005.toml` and `rp2018.toml` start with
      `# generated-file: do not edit by hand`; `data/provenance/pdfs.toml` does
      not start with it.
- [x] No banner appears in `changes.csv`, `source.diff`, `text.diff`,
      `derived.diff`, `manifest.json`, CSV, or TEI files.

## 6. Root README generated-files section

- [x] `## Generated files` appears exactly once, inside the
      `<!-- editions:begin -->` ... `<!-- editions:end -->` block.
- [x] The table has one row for each of the registry rows in `plan.md`
      task group 8, including `editions/<edition>/source/`, the individual
      `docs/*.md` outputs, the `reports/baseline/` and `reports/reconciliation/`
      Markdown and CSV families, `editions/<edition>/manifest.json`, `csv/`,
      `tei/`, `docs/contract/*.json`, and `reports/diffs/`. After the companion
      retire change the registry has **12** rows: the two `csv-unicode/` and
      `tei-xml-unicode/` rows were removed with the trees.
- [x] `docs/HISTORY.md` is listed with both commands in the documented order.
- [x] The blockquote contains the phrase `hand-written` (it wraps across two
      lines) and `data/provenance/pdfs.toml` appears only in the hand-maintained
      sentence, never as a generated table row.
- [x] `docs.render_root_readme(readme_text) == readme_text` for the committed
      README (the existing `RootReadmeTests.test_generated_block_matches_the_generator`).
- [x] The root README contains exactly one `<!-- editions:begin -->` and one
      `<!-- editions:end -->`; neither literal appears in the generated-files
      table or prose (`RootReadmeTests.test_has_exactly_one_generated_block`).

## 7. Parser and `--verify` behaviour

- [x] `python3 scripts/fetch_official.py --verify` exits 0 with the banner
      present (`verified 6 archives`, exit 0).
- [x] Hash both TOMLs before and after `--verify`; they are identical:
      `sha256sum data/provenance/rp2005.toml data/provenance/rp2018.toml`
      (`sha256sum -c` reports OK for both).
- [x] `fetch._existing_records` on each committed TOML returns three records per
      edition, each with `source_page` equal to `sources.SOURCE_PAGE`
      (`rp2005 3 True`, `rp2018 3 True`).
- [x] A synthetic TOML whose banner line contains `=` (for example
      `# note = not a field`) still parses; the comment is ignored
      (`tests/reconciliation/test_fetch.py::test_existing_records_ignores_comment_lines_even_with_equals`).
- [x] `python3 scripts/fetch_official.py --verify --force` still exits non-zero
      ("mutually exclusive", exit 1).
- [x] In `--force` output, `downloaded` is the only clock-dependent field;
      record order, keys, `source_page`, `sha256`, and all other values are fixed
      by `sources.ARCHIVES`
      (`test_force_output_is_deterministic_when_the_clock_is_fixed`).

## 8. Determinism

- [x] After the first full run, save the working-tree diff:
      `git diff --binary > /tmp/byz-run1.diff`. Run the entire §3 routine a
      second time, then `git diff --binary > /tmp/byz-run2.diff` and
      `cmp /tmp/byz-run1.diff /tmp/byz-run2.diff`. They must be identical. (The
      diff against `HEAD` is expected to be non-empty after the first run; this
      check compares run 1 with run 2, not the working tree with `HEAD`.)
      *(Ran with `/tmp/opencode/byz-review-run1.diff` and
      `/tmp/opencode/byz-review-run2.diff`; `cmp` was silent.)*
- [x] `git status --porcelain` after the second run equals the state after the
      first run (apart from the pre-existing untracked entries recorded in §1).
      *(`diff` of the two saved status files was silent.)*
- [x] Compare the first run's hash list with the second run's:
      `find docs editions reports -type f -name '*.md' -print0 | sort -z | xargs -0 sha256sum`
      plus the two TOMLs; every hash matches. *(The run-2 list has 19
      Markdown files: 17 generated plus the two hand-maintained docs.)*
- [x] `tests/curate/test_reproducible.py` now covers `byz.contract` **and**
      `byz.reconcile`, and both `test_committed_outputs_match_a_fresh_run` and
      `test_two_runs_are_byte_identical` pass (`tests/curate`, 141 tests, OK on
      2026-11-20; the 134 in the implementation pass predates the retire tests).
- [x] `--force` was not used. If it was accidentally used, record the resulting
      `downloaded`/`final_url` changes here and restore the originals with
      `git checkout -- data/provenance/`, then re-run record mode.

## 9. Test suites

```bash
PYTHONPATH=src python3 -m unittest discover -s tests/contract
PYTHONPATH=src python3 -m unittest discover -s tests/curate
PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation
```

- [ ] All three suites pass with 0 failures and 0 unplanned skips. *(Not in the
      live uncommitted tree: `tests/contract` is 50 tests with the 3 known
      `ContractWorktreeTests` failures described below. `tests/curate` is 141
      tests OK and `tests/reconciliation` is 64 tests OK; both have 0 failures
      and 0 unplanned skips. Verified 2026-11-20.)*
- [x] New tests from `plan.md` task groups 1, 2, 6, 7, and 9 are present and
      green.
- [x] `tests/curate/test_integration.py:396` compares
      `reports/diffs/README.md` with `generated.markdown(diff.README_TEXT)`, not
      with the raw constant (`test_readme_is_generated_from_the_module_constant`).
- [x] `tests/curate/test_editions.py` still passes
      `test_generated_block_matches_the_generator` and
      `test_has_exactly_one_generated_block`.
- [x] `tests/contract/test_integration.py` asserts one banner and one Cycle 2
      block after contract and after `_update_history` (the assertions run in
      the worktree tests; see the pre-commit caveat below).
- [x] `tests/curate/test_reproducible.py` creates a worktree at `HEAD`, so before
      this change is committed it exercises the old commit. Treat §8 as the
      authoritative pre-commit determinism check, and re-run this test after the
      change is committed (or in a worktree that contains it). *(The test
      passes because it compares the worktree against `HEAD`; the live change
      is covered by §8.)*
- [ ] The `ContractWorktreeTests` in `tests/contract/test_integration.py` also
      build a worktree at `HEAD`; re-run them after committing the change.
      *(Known pre-commit artefact: `HEAD` predates the banner change, so
      `worktree/docs/HISTORY.md` has no banner and the three tests fail with
      `0 != 1` on `generated.MARKDOWN_MARKER`. Confirmed 2026-11-20 by
      committing the working tree in a scratch copy: the three banner failures
      disappear, and after one follow-up `byz.contract` + `byz.reconcile`
      regeneration commit, which updates `docs/HISTORY.md` and
      `reports/baseline/files.csv` for the new `HEAD`, all 50 contract tests
      pass. The branch therefore needs that regeneration commit immediately
      after the feature commit.)*
- [x] No test performs network access. `tests/reconciliation` uses only the
      committed archives and `fetch.run(verify=True)` / record mode with mocks.

## 10. Manual inspection

- [ ] Open each of the 17 generated Markdown files in a Markdown preview. The
      banner is the first thing a reader sees, and the document body is
      unchanged below it. *(Not previewed; the banner structure is asserted by
      `tests/curate/test_generated.py` and the `head -2` sweep in §5.)*
- [ ] Open the root README: the curated-editions section shows the "Generated
      section" note, the editions table, and the generated-files table. A reader
      can tell that the welcome text, "Start here", "Repository layout", and
      "Reproducing the curated data" are hand-written. *(Not previewed; the
      generated block round-trip is asserted in §6.)*
- [x] Open `data/provenance/rp2005.toml`: the banner is readable, then
      `edition = "rp2005"`, then three records each with `source_page`.
- [x] Open `docs/PROVENANCE.md`: the Archives section names the listing page and
      the November 2026 window before the checksum table.
- [x] Run `python3 scripts/fetch_official.py --verify` one final time; it
      validates the six committed zips and prints `verified 6 archives`.
- [x] Confirm `SPECS/TECH.md` §2 reads coherently: the listing page is the
      origin, the Dropbox URLs are the download targets, and `source_page`
      records the former.

## 11. Definition of done

- [x] `source_page` is present on all six `[[archives]]` records and is emitted
      by `_write_provenance` (not added by hand).
- [x] The listing page appears in `docs/PROVENANCE.md` and `SPECS/TECH.md` §2,
      with the November 2026 retrieval window.
- [x] All 17 generated Markdown files and both generated TOMLs carry the banner.
- [x] The root README lists every generated family with its command and states
      which parts are hand-written; `pdfs.toml` is excluded.
- [x] `docs/HISTORY.md` survives both writers with one banner and one Cycle 2
      block.
- [ ] A second full regeneration is byte-identical; the tracked tree is clean.
      *(Byte-identical yes (§8); the tracked tree necessarily still carries the
      uncommitted change, per the working rules.)*
- [ ] All three test suites pass. *(Curate and reconciliation pass; contract has
      the 3 known `ContractWorktreeTests` failures until the change is
      committed.)*
- [x] No corpus, archive, CSV, TEI, manifest, or checksum changed.
- [x] Every deviation from `plan.md` is recorded in §12 with its reason.

## 12. Deviations log

1. **Python version and pinned packages.** Python 3.10 is not installed in the
   implementation environment, and `pandas==1.4.2` / `numpy==1.23.5` do not
   build on the available Python 3.12. The regeneration sequence and all three
   test suites were run in a Python 3.12 virtual environment containing only
   `beta-code==1.0.0` (the only pinned package the sequence imports). The CSV
   and TEI converters were not run, as the plan's regeneration routine does not
   include them and no CSV/TEI output changed.
2. **Pre-existing untracked files.** Six unrelated untracked files predated this
   change (one under `csv-unicode/`, five under `essay/`). During the original
   implementation they were moved to a temporary directory for the two-run
   determinism check and restored byte-for-byte afterwards, because
   `recover_editions.py` then copied whole directories and would have copied
   `csv-unicode/ccat/with-variants/variant_analysis.py` into the edition,
   changing `manifest.json` and violating C3. In the review pass the five
   `essay/` files were **left in place**: `recover_current()` no longer copies
   whole trees, and the contract inventory now ignores untracked files (§12.6).
   Nothing was added, removed, or committed.
3. **Pre-commit worktree tests.** The three `ContractWorktreeTests` create a
   worktree at `HEAD`, so in the uncommitted working tree they exercise the old
   commit and fail by design (see §9). All three suites, including those tests,
   were verified green in a temporary committed copy of the change under
   `/tmp/opencode/byz-verify`; that copy was deleted afterwards and the feature
   branch was not committed. The plan's §8 two-run check is the authoritative
   pre-commit determinism evidence and passed.
4. **`reports/baseline/files.csv`.** The plan lists only
   `reports/baseline/{summary.md,decision-log.md}` as changed. `files.csv` is a
   generated inventory and changed as well, because it hashes `README.md` and
   `scripts/README.md`, both edited by hand in task group 10. After the review
   fix in §12.6 it also has exactly the five tracked `essay/` rows; the five
   untracked `essay/` files contribute no rows.
5. **`parse_cct_accented` is not the current-source reader.** The retire spec
   (`requirements.md`, `plan.md`) claimed that `parse_cct_accented` reproduced
   the current accented views. It does not: it is the official-archive reader
   and upper-cases the text via `production_ccat_line`. The implementation added
   the separate `parse_cct_current` reader for the all-lowercase `source/CCAT`
   dialect, and the spec text now records the correction and the reader's
   dialect. `tests/curate/test_build.py` locks MAT 1:1, a blank verse, and a
   `? ` paragraph line.
6. **`files.csv` now inventories only tracked files (blocking review finding
   B1).** `inventory.iter_specs` intersects its glob with `git ls-files`, and
   `inventory.inventory` passes that set down. Previously five untracked
   `essay/` files appeared as rows with empty git columns; after commit the
   worktree determinism tests would have failed permanently and the committed
   report would have claimed files outside the corpus. The five tracked `essay/`
   rows remain, and `essay/README.md` is still inventoried once as an `essay`
   and once as a `doc` row.
7. **Root README hand-written prose changed (review finding N4).** The runbook
   comment and the paragraph after it now state that
   `recover_editions.py` only freezes inputs and must be followed by
   `build_editions.py`. This is why §3's "hand-written prose unchanged" item is
   not checked. The generated block still round-trips exactly.
8. **The retrieval window is derived, not hard-coded (review finding N5).**
   `reconcile.report._retrieval_window()` reads the `downloaded` values from
   `data/provenance/*.toml`; the generated prose now says "initially obtained"
   and prints the actual first/last timestamps, so a future `--force` cannot
   leave stale text.
9. **Other review fixes.** `build_current()` asserts the canonical 27 book set
   (plus `PA`/`ACT24` for CCAT) and names the edition and missing book;
   `write_tei(combined=True)` rejects per-book titles; the generated
   `docs/EDITIONS.md` renders the multi-target retired row as two code spans and
   documents the inherited `Second Timoty`/`Phillipians` titles; `scripts/README.md`
   and the root README document the recovery/build split; `.opencode` and the
   test nits from the review are updated.

> **Superseded 2026-11-26:** the inherited `Second Timoty`/`Phillipians` titles
> were corrected in the unaccented TEI on 2026-11-26; `docs/EDITIONS.md` now
> documents the corrected `Second Timothy`/`Philippians` titles. See
> `SPECS/2026-11-26-pr46-review-fixes/`.

10. **Independent verification pass (2026-11-20).** Re-ran the full sequence
    twice; `git diff --binary` and `git status --porcelain` from run 1 and run 2
    were byte-identical. All 448 edition CSV files parse and all 224 TEI files
    are well-formed. The three live `tests/contract` failures are only the
    missing banner at `HEAD`; the scratch-copy proof is in §9. The maintainer's
    asks that belong to `SPECS/2026-11-19-docs-clarity/` (hyperlinked tags and
    commits in `docs/EDITIONS.md`, the `scripts/README.md` report-order rewrite,
    the `SPECS/MISSION.md` "why category" typo, and the Strong's/BP5
    `official-source-files` wording) are still deferred: this branch does not
    implement that spec, so `provenance-unknown` remains in
    `docs/PROVENANCE.md` and in the reconciliation reports. That is a deferral,
    not a regression introduced by this change, but the Strong's wording ask is
    not met by this branch.
