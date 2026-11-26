# Validation - Diff categories: rename `variant-code`, document every category, show the tag change

Authoritative checklist: `requirements.md` R1-R8 and `plan.md` phases 0-7.
Record the commands run and the observed output in §8; the boxes are the
implementation-time checklist.

## 1. Preconditions

- [ ] Branch is `feature/2026-11-16-edition-recovery-curation`; do not switch
      branches and do not commit as part of this change.
- [ ] `git rev-parse --short HEAD` is `9a5a9d1` (or the immediate parent of the
      implementation commit, if the maintainer commits in between), and
      `git status --porcelain` shows only this spec folder before work starts.
      Record the starting state: `git status --porcelain > /tmp/byz-categories-before.txt`.
      *Implementation ran at `fc71f28`; only this spec folder was untracked.*
- [ ] Python 3.10 with `pip install -r requirements.txt`; if unavailable,
      use the existing Python 3.12 environment with only `beta-code==1.0.0` and
      record it in §7. *Used Python 3.12.3 in `/tmp/opencode/venv-byz` with `beta-code==1.0.0`.*
- [ ] Full history and tags: `git tag --list v2.0.3 v3.3.4` prints both (the
      edition recovery needs them).
- [ ] The six committed archives exist:
      `ls data/raw/_archives/rp2005 data/raw/_archives/rp2018` shows three
      ZIPs each.
- [ ] No untracked file is inside `data/text/` or an edition directory; if there
      is, move it aside before regenerating (recovery copies whole directories)
      and restore it in §6.
- [ ] Baseline counts recorded (Phase 0 of `plan.md`): 161 / 3 / 54 / 55
      source-tier rows and 156 / 0 / 8 / 8 apparatus-only rows for
      `rp2005--rp2005-2019`, `rp2005-2019--rp2018`, `rp2018--rp2018-2023`,
      `rp2005--rp2018`.

## 2. Red phase

Write the tests from `plan.md` phases 1a, 2a, 3a, 4a before changing production
code. Confirm each fails for the intended reason, not an import error in the
test itself.

- [ ] `tests/reconciliation/test_compare.py` fails: the classifier returns
      `variant-code`, and `compare.CATEGORY_MEANINGS` /
      `compare.APPARATUS_CODE_NAMES` do not exist.
- [ ] `tests/curate/test_diff.py::TagChangeTests` fails with
      `AttributeError: module ... has no attribute 'tag_change'`.
- [ ] `tests/curate/test_diff.py::ReadmeCategoryTests` fails: `README_TEXT`
      has no `## Categories`.
- [ ] `tests/curate/test_integration.py` fails on the committed
      `rp2018--rp2018-2023/report.md`: no ``### ACT 1:15 · `apparatus-code` ``,
      no `Apparatus code:` line, still `variant-code`.
- [ ] `tests/reconciliation/test_integration.py` fails: the summary has no
      reading/code split, R2 still says `variant-code`.
- [ ] `tests/reconciliation/test_offline.py::CommittedReportTests` fails: the
      rename guard finds `variant-code` in `reports/reconciliation/`.
- [ ] The guard deliberately excludes `bad-variant-code`:
      `grep -rn "bad-variant-code" reports/` is empty today, so a bare
      substring guard would still pass; add the exclusion comment so a future
      contract violation does not fail this unrelated test.

Record the exact failing command and first failing assertion per group in §8.

## 3. Green phase: regeneration sequence

Run from the repository root, in this order:

```bash
# 1. Provenance: validate the committed archives; no network, no writes.
PYTHONPATH=src python3 -m byz.fetch --verify

# 2. Record mode reuses the committed archives; no downloads.
PYTHONPATH=src python3 -m byz.fetch

# 3. Curated editions and diffs.
PYTHONPATH=src python3 -m byz.recover
PYTHONPATH=src python3 -m byz.build
PYTHONPATH=src python3 -m byz.diff

# 4. Reports. Contract first, reconciliation second (docs/BUILD.md).
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m byz.reconcile
```

- [ ] `--verify` exits 0 and prints `verified 6 archives`.
- [ ] `--force` is **not** used. If it was used by accident, restore
      `data/provenance/` with `git checkout -- data/provenance/` and re-run
      `--verify`; record it in §7.
- [ ] After step 3, `git status --porcelain -- data/ editions/` is
      empty. This is the "no corpus change" gate.
- [ ] `git diff --stat -- editions/` is empty: no edition README, manifest,
      CSV, TEI, or source snapshot changed.
- [ ] `docs/HISTORY.md` still has exactly one `<!-- cycle2:begin -->` block, and
      the contract-then-reconcile order leaves it with one banner.

## 4. Item checks

### R1 - classifier rename and vocabulary

- [ ] `PYTHONPATH=src python3 -c "from byz.reconcile import compare; print(compare.classify_diff('text {C x > y }','text {N x > y }'))"`
      prints `apparatus-code`.
- [ ] `PYTHONPATH=src python3 -c "from byz.reconcile import compare; print(list(compare.CATEGORY_MEANINGS))"`
      prints, in order:
      `['missing', 'variant', 'apparatus-code', 'capitalization', 'word-segmentation', 'whitespace', 'punctuation', 'accents-breathings', 'letters']`.
- [ ] `PYTHONPATH=src python3 -c "from byz.reconcile import compare; print(compare.APPARATUS_CODE_NAMES)"`
      prints the six letters `N B C M S E` and no others.
- [ ] `grep -rn "variant-code" src/` finds only the contract's
      `bad-variant-code` at `src/byz/contract/ccat.py:111`;
      `grep -rn "variant-code" src/ | grep -v bad-variant-code` is empty.
- [ ] `grep -rn "bad-variant-code" src/byz/contract/ tests/contract/` is
      unchanged.

### R2 - tag line and evidence

- [ ] `grep -c "Apparatus code: " reports/diffs/rp2018--rp2018-2023/report.md`
      is **45**.
- [ ] This command prints `29 N -> C` and `16 N -> S` (the one two-position
      row, `2PE 2:6`, is deduplicated; see §10.5):

```bash
grep -o 'Apparatus code: `[NBCMSE]` -> `[NBCMSE]`' \
  reports/diffs/rp2018--rp2018-2023/report.md | sort | uniq -c
```

- [ ] The apparatus-only entry for `ACT 1:10` is:

```
- `ACT 1:10` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `...`
  - Apparatus (Beta code): `...`
```

- [ ] The `1CO 3:14` `variant` entry in `rp2005--rp2018` has no
      `Apparatus code:` line and still shows `{+{NA μένει > μενεῖ }+}`.
- [ ] The direction is not hard-coded: the reconciliation R2 row keeps
      `C` vs `N`, the diff report renders `N -> C`.

### R3 - honest rendering at ACT 1:15

- [ ] `sed -n '/### ACT 1:15/,/^### /p' reports/diffs/rp2018--rp2018-2023/report.md`
      shows, in order:
      1. ``### ACT 1:15 · `apparatus-code` ``
      2. ``Apparatus code: `N` -> `C` (the reading is unchanged)``
      3. `Text (derived; typographic only, not part of the source-tier change):`
      4. a Text block containing `[-εἶπεν --]{+εἶπεν-+}`
      5. `Source (Beta code):` and a block containing `[-{N-]{+{C+}`
      6. `Apparatus (Unicode):` and a block containing `[-{NA-]{+{NA27/28+}`
- [ ] The Text block is still present: the dash difference is visible, not
      suppressed (`text.diff` and `changes.csv` also keep it).
- [ ] `## Main-text changes (derived text differs)` and its lead sentence are
      present; `## Apparatus-only changes` has its lead sentence.
- [ ] The source-tier counts did not move: the `## Main-text changes` section
      still has five `###` entries for this pair, and
      `**Apparatus-only changes (source differs, main text identical):** 156`.
- [ ] The per-pair category table has the header `| Category | Meaning | Count |`,
      includes an `apparatus-code` row, and is followed by the
      `../README.md#categories` pointer.

### R4 - generated README glossary

- [ ] `reports/diffs/README.md` has `## Categories`.
- [ ] The table has nine rows in precedence order:
      `missing`, `variant`, `apparatus-code`, `capitalization`,
      `word-segmentation`, `whitespace`, `punctuation`, `accents-breathings`,
      `letters`.
- [ ] Each row has a non-empty meaning; `missing` and `whitespace` say
      `none in the current reports`.
- [ ] The apparatus-code example is `ACT 1:15` in `rp2018--rp2018-2023`,
      `N -> C`, reading unchanged.
- [ ] The variant example is `1CO 3:14` in `rp2005--rp2018`.
- [ ] The `variant` vs `apparatus-code` paragraph is present and distinguishes
      reading from label.
- [ ] The apparatus-code names sentence lists `Nestle-Aland`, `Byzantine`,
      `NA27/28`, `ECM`, `NA27`, `NA28`, and explains that `{NA-]{+{NA27/28+}`
      is the Unicode spelling of `{N-]{+{C+}`.
- [ ] `grep -n "variant-code" reports/diffs/README.md` finds nothing.
- [ ] Each `CATEGORY_EXAMPLES` reference resolves:
      `test_glossary_examples_are_real` passes.

### R5 - reconciliation

- [ ] `grep -n "variant-code" reports/reconciliation/*` finds nothing.
- [ ] `grep -n "apparatus-code" reports/reconciliation/categories.csv` shows
      `source,rp2005,apparatus-code,45` and `source,rp2018,apparatus-code,45`.
- [ ] `reports/reconciliation/decision-log.md` R2 contains
      ``category `apparatus-code` `` and still ends `| pending |`.
- [ ] `reports/reconciliation/summary.md` states the reading/code split and
      links `../diffs/README.md#categories`.
- [ ] `reports/reconciliation/verses.csv` has 45 `apparatus-code` rows per
      edition and no `variant-code` row:
      `awk -F, '$8=="apparatus-code"' reports/reconciliation/verses.csv | wc -l` is 90.

### R6 - CSV schema and migration

- [ ] All four `changes.csv` headers are exactly:

```
book,chapter,verse,category,source_word_diff,text_word_diff,source_left,source_right,text_left,text_right,text_changed,apparatus_word_diff,apparatus_changed
```

- [ ] No `changes.csv` row has `category == "variant-code"`.
- [ ] `ACT,1,15,...` has `category` `apparatus-code`, `text_changed` `true`,
      `apparatus_changed` `true`, `{N` on the left, `{C` on the right.
- [ ] `docs/RELEASE-NOTES.md` has the `2026-11-21` section: old value, new
      value, affected files, no alias, the `variant` vs `apparatus-code`
      distinction, and the migration instruction.
- [ ] `docs/EDITIONS.md` contains
      ``[`reports/diffs/README.md`](../reports/diffs/README.md#categories)`` and
      the relative link resolves (the link test strips the anchor and checks
      the file).

### R7 - tests and lock

- [ ] `grep -rn "variant-code" reports/ | grep -v bad-variant-code` prints
      nothing.
- [ ] The rename guard test exists and is not a bare substring test: it
      excludes `bad-variant-code` with an explanatory comment.
- [ ] The positive guard asserts `apparatus-code` at ACT 1:15, so a regression
      that deletes the category also fails.
- [ ] The pinned category test is renamed, not deleted:
      `grep -n "test_classify_apparatus_code" tests/reconciliation/test_compare.py`.

### R8 - determinism

See §5. No timestamps, hostnames, or absolute paths:

```bash
grep -nE '/home/|/tmp/|[0-9]{4}-[0-9]{2}-[0-9]{2}T' \
  reports/diffs/README.md reports/diffs/*/report.md reports/diffs/*/*.diff \
  reports/reconciliation/*.md docs/EDITIONS.md docs/PROVENANCE.md
```

Expected: no output. Fixed editorial dates in `docs/RELEASE-NOTES.md` and
`docs/EDITIONS.md` prose are not timestamps and are allowed.

## 5. Determinism: byte-identical second run

- [ ] After the first full §3 run, snapshot:
      `git diff --binary > /tmp/byz-categories-run1.diff`.
- [ ] Snapshot the generated files:
      `find docs editions reports -type f \( -name '*.md' -o -name '*.csv' -o -name '*.diff' -o -name '*.json' -o -name '*.xml' \) -print0 | sort -z | xargs -0 sha256sum > /tmp/byz-categories-hashes1.txt`.
- [ ] Run the entire §3 sequence a second time.
- [ ] `git diff --binary > /tmp/byz-categories-run2.diff` and
      `cmp /tmp/byz-categories-run1.diff /tmp/byz-categories-run2.diff`
      reports no difference. (The diff against `HEAD` is non-empty; this
      compares run 1 to run 2.)
- [ ] Re-hash as above to `/tmp/byz-categories-hashes2.txt` and
      `cmp /tmp/byz-categories-hashes1.txt /tmp/byz-categories-hashes2.txt`
      reports no difference.
- [ ] `git status --porcelain` after the second run equals the state after the
      first.
- [ ] `git diff --stat -- editions/ data/` is empty after both runs.

## 6. Test suites

```bash
PYTHONPATH=src python3 -m unittest discover -s tests/contract
PYTHONPATH=src python3 -m unittest discover -s tests/curate
PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation
```

- [ ] All three suites pass with 0 failures and no unplanned skips.
- [ ] Every new test from `plan.md` is present and green:
      `TagChangeTests` (4) and `ReadmeCategoryTests` in `tests/curate/test_diff.py`;
      the ACT 1:15 / ACT 1:10 / 1CO 3:14 assertions, the diff-directory rename
      guard, and `test_glossary_examples_are_real` in
      `tests/curate/test_integration.py`; `VocabularyTests` and the renamed
      classifier test in `tests/reconciliation/test_compare.py`; the summary/R2
      assertions in `tests/reconciliation/test_integration.py`; the
      `CommittedReportTests` additions in `tests/reconciliation/test_offline.py`.
- [ ] No test performs network access.
- [ ] `tests/curate/test_reproducible.py` and
      `ContractWorktreeTests` build a worktree at `HEAD`; before this change is
      committed they exercise the old commit. Record in §8 whether they were
      run in place or in a throwaway committed copy under `/tmp/opencode/`.
- [ ] Restore any untracked files moved in §1 and confirm
      `git ls-files --others --exclude-standard` matches the pre-change list.

## 7. Deviations log

Record every deviation from `plan.md` here with its reason. Known candidates:

1. Python/pinned-package environment differences.
2. Line-number drift in `compare.py`, `diff.py`, `report.py`, or `docs.py`
   relative to `plan.md`.
3. The `test_reproducible` / worktree-at-`HEAD` one-commit lag.
4. Any difference between the category examples in `CATEGORY_EXAMPLES` and the
   regenerated `changes.csv` (the test should have caught it; record why it did
   not if one slips through).
5. Any generated file that changes beyond the expected set in
   `plan.md` "Files changed" (for example an edition file, which is a failure,
   or `docs/HISTORY.md` prose).
6. Deliberate retention of the old value in `docs/RELEASE-NOTES.md` (migration
   history) and in
   `SPECS/2026-11-16-edition-recovery-curation/requirements.md:174` (dated
   spec). These are not generated output and must not be "fixed" to make
   `grep` quiet.

## 8. Manual inspection

- [ ] Open `reports/diffs/rp2018--rp2018-2023/report.md` at ACT 1:15 and read it
      as a first-time user. Confirm the answer to "what changed?" is immediate:
      the apparatus code went from `N` to `C`, the reading is unchanged, and the
      Text block is explicitly derived/typographic. Confirm the Text block still
      shows the dash difference, so nothing is hidden.
- [ ] In the same file, open `ACT 1:10` under `Apparatus-only changes` and
      confirm the tag line, the Unicode apparatus line, and the Beta-code line
      read together without inference.
- [ ] Open the `## Categories (source tier)` table: every count is unchanged
      from the baseline (the rename is a value change, not a reclassification),
      and the Meaning column explains each row.
- [ ] Open `reports/diffs/README.md`: read `## Categories` from top to bottom
      without opening the code and confirm every category, its meaning, the
      `variant`/`apparatus-code` distinction, and both worked examples are
      clear.
- [ ] Open `reports/reconciliation/decision-log.md` R2: the category is
      `apparatus-code`, the evidence still points at `verses.csv`, and the
      decision is still pending. Open `reports/reconciliation/summary.md` and
      confirm the reading/code split matches the category table.
- [ ] Open `docs/RELEASE-NOTES.md`: the migration note says exactly what a
      consumer of `category` values must change, and states that no alias is
      emitted.
- [ ] Open `docs/EDITIONS.md` at "Successive diffs": the glossary pointer is a
      working relative link.

## 9. Definition of done

- [ ] R1: the classifier returns `apparatus-code`; `CATEGORY_MEANINGS` and
      `APPARATUS_CODE_NAMES` are the single vocabulary; `src/` has no
      `variant-code` except `bad-variant-code`.
- [ ] R2: all 45 apparatus-code entries print the tag change in the report's
      direction; Beta-code and Unicode apparatus evidence is intact.
- [ ] R3: ACT 1:15 states the source-tier change, labels the Text block as
      derived, and keeps every piece of evidence; the counts are unchanged.
- [ ] R4: the generated README documents all nine categories with real examples
      and the two-category distinction.
- [ ] R5: reconciliation `categories.csv`, `verses.csv`, `summary.md`, and R2 use
      `apparatus-code`, and the summary distinguishes reading from code.
- [ ] R6: `changes.csv` schema is unchanged; the migration is documented in
      `docs/RELEASE-NOTES.md`; `docs/EDITIONS.md` links the glossary.
- [ ] R7: the red/green tests and both rename guards (negative and positive)
      are green.
- [ ] R8: the full regeneration runs twice with no diff; all three suites pass;
      no `data/`, `data/text/`, or `editions/` file changed; no timestamp,
      hostname, or absolute path was introduced.
- [ ] Every deviation is recorded in §7.

## 10. Implementation record (2026-11-23)

Implemented on branch `feature/2026-11-16-edition-recovery-curation`, HEAD
`fc71f28`, working tree clean apart from this spec folder. Section headings and
checkboxes above are the pre-implementation checklist; this section records what
actually ran and the amendments forced by the landed layout refactor.

### 10.1 Layout amendments

The spec was drafted after `9a5a9d1` and before
`SPECS/2026-11-21-input-and-code-layout/` landed at `1d39f3d`. Every command and
path was reconciled to the landed layout:

- `scripts/fetch_official.py` -> `PYTHONPATH=src python3 -m byz.fetch`
- `scripts/recover_editions.py` -> `PYTHONPATH=src python3 -m byz.recover`
- `scripts/build_editions.py` -> `PYTHONPATH=src python3 -m byz.build`
- `scripts/diff_editions.py` -> `PYTHONPATH=src python3 -m byz.diff`
- `scripts/requirements.txt` -> `requirements.txt` (repository root)
- `scripts/README.md` -> `docs/BUILD.md`
- `scripts/beta_to_unicode_custom/beta_to_unicode_custom.py` ->
  `src/byz/beta/converter.py`
- `source/CCAT`, `source/Strongs`, `source/README.md` ->
  `data/text/CCAT`, `data/text/Strongs`, `data/text/README.md`
- `editions/<id>/source/` is unchanged (the frozen per-edition snapshot); the
  "not touched" and corpus gates therefore read `data/` plus
  `editions/*/source|csv|tei|manifest.json`.

### 10.2 Red phase

Tests were written first and run against the unmodified code. Each failed for
the intended reason:

- `tests.reconciliation.test_compare`: `classify_apparatus_code` returned
  `variant-code`; `CATEGORY_MEANINGS` / `APPARATUS_CODE_NAMES` raised
  `AttributeError`.
- `tests.curate.test_diff`: `TagChangeTests` raised
  `AttributeError: module ... has no attribute 'tag_change'`;
  `ReadmeCategoryTests` failed because `README_TEXT` had no `## Categories`.
- `tests.curate.test_integration`: the committed report still said
  `### ACT 1:15 · `variant-code``, had no tag line and no Meaning column.
- `tests.reconciliation.test_integration`: the summary had no reading/code
  split and R2 still said `variant-code`.
- `tests.reconciliation.test_offline`: the rename guard found `variant-code` in
  `reports/`, and R2 had not been renamed.

### 10.3 Category inventory confirmed from the code

`compare.classify_diff` precedence order, with the counts regenerated from the
four `changes.csv` files:

| Category | Meaning | Occurrences |
| --- | --- | ---: |
| `missing` | The verse is present on one side only. | 0 |
| `variant` | The apparatus reading or note changed; the main text is identical. | 103 |
| `apparatus-code` | Only the apparatus code letters changed; the reading is identical. | 45 |
| `capitalization` | The main text differs only in capitalisation. | 12 |
| `word-segmentation` | The same letters are divided into words differently. | 8 |
| `whitespace` | Only whitespace differs. | 0 (unreachable: `_main_text` collapses whitespace first) |
| `punctuation` | The main text differs only in punctuation. | 50 |
| `accents-breathings` | The main text differs only in accents or breathings. | 51 |
| `letters` | The main text letters differ. | 4 |

`bad-variant-code` (contract validator) is a different vocabulary and is
unchanged.

### 10.4 ACT 1:15 before and after

Before:

```
### ACT 1:15 · `variant-code`

Text:

... [-εἶπεν --]{+εἶπεν-+} ...

Source (Beta code):

... [-{N-]{+{C+} ...
```

After:

```
### ACT 1:15 · `apparatus-code`

Apparatus code: `N` -> `C` (the reading is unchanged)

Text (derived; typographic only, not part of the source-tier change):

... [-εἶπεν --]{+εἶπεν-+} ...

Source (Beta code):

... [-{N-]{+{C+} ...

Apparatus (Unicode):

... [-{NA-]{+{NA27/28+} ...
```

The entry stays under `## Main-text changes (derived text differs)`; the dash
difference is still visible in the report, `text.diff`, and `changes.csv`.

### 10.5 Tag-line counts

`grep -c "Apparatus code: "` is **45** as expected. The distribution is
**29 `N -> C`** and **16 `N -> S`**. The initial draft predicted `30`/`15`;
`2PE 2:6` has two positions that dedupe to one line, so the count was corrected
to 29/16 in §4 R2 and `requirements.md`. That row is `2PE 2:6`
(`{N ... }{N ... }` -> `{S ... }{S ... }`), which renders once as `N -> S`:
29 `N -> C` rows and 15 single-change `N -> S` rows plus the deduplicated row =
16 `N -> S` lines. The old `variant-code` membership is unchanged at 45 and no
row was reclassified.

### 10.6 Green phase and regeneration

Run from the repository root with `PYTHONPATH=src` and
`/tmp/opencode/venv-byz/bin/python3`:

```
byz.fetch --verify   -> verified 6 archives
byz.fetch            -> rewrote data/provenance/rp2005.toml, rp2018.toml (bytes unchanged)
byz.recover          -> recovered 4 editions
byz.build            -> built 4 editions; docs/EDITIONS.md, README.md
byz.diff             -> wrote 4 report directories
byz.contract         -> wrote reports/baseline
byz.reconcile        -> wrote reports/reconciliation
```

Observed checks:

- `grep -rn "variant-code" reports/ | grep -v bad-variant-code` -> clean.
- `reports/reconciliation/decision-log.md` R2 contains
  ``category `apparatus-code` `` and ends `| pending |`.
- `summary.md` states `89 reading changes, 45 code-only changes` and links
  `../diffs/README.md#categories`.
- `categories.csv` has `source,rp2005,apparatus-code,45` and
  `source,rp2018,apparatus-code,45`; `verses.csv` has 90 `apparatus-code` rows.
- All four `changes.csv` files keep the 13-column schema and order.
- `docs/EDITIONS.md` has the glossary pointer at line 314.

### 10.7 Determinism and corpus gate

The complete sequence above was run twice. `git diff --binary`, the SHA-256 of
all 736 generated `.md`/`.csv`/`.diff`/`.json`/`.xml` files under
`docs/`, `editions/`, and `reports/`, and `git status --porcelain` were
byte-identical between runs.

`git status --porcelain -- 'editions/*/csv' 'editions/*/tei'
'editions/*/source' 'data/'` is empty: no text, archive, edition CSV/TEI,
manifest, or `data/` byte changed. `docs/HISTORY.md`,
`reports/baseline/files.csv`, and `docs/PROVENANCE.md` did not move (the
edition sources are unchanged, so the baseline hashes did not change), so the
known one-commit corpus lag did not occur here.

The only timestamp-looking hit is the pre-existing recorded retrieval window in
`docs/PROVENANCE.md` (`2026-11-16T18:37:00Z`..`18:37:10Z`), which is data, not a
run timestamp; this change does not touch it.

### 10.8 Migration note wording

`docs/RELEASE-NOTES.md`, section
`## 2026-11-21 - the diff category `variant-code` is now `apparatus-code``:
old value `variant-code`, new value `apparatus-code`; lists the affected
generated files; states **no alias is emitted**; states the 13-column schema is
unchanged; tells consumers filtering `category == "variant-code"` to switch to
`category == "apparatus-code"`; separates `bad-variant-code`; links
[`reports/diffs/README.md`](../reports/diffs/README.md#categories). A second
section dated 2026-11-21 is deliberate: the layout-move note already used that
date.

### 10.9 Suites

```
tests/contract        64 tests   OK
tests/curate         201 tests   OK
tests/reconciliation  80 tests   OK
```

No test was weakened. `test_reproducible` ran its detached worktree at HEAD
(the old commit) and passed, as expected before a commit is created.

### 10.10 Deviations log additions

1. The layout refactor landed; commands/paths updated throughout this spec.
2. Python 3.12.3 was used, not 3.10 (venv with the pinned `beta-code==1.0.0`).
3. Tag-line distribution is 29 `N -> C` / 16 `N -> S` (the initial draft
   predicted 30/15; corrected to 29/16 in §4 R2 and `requirements.md` because
   `2PE 2:6` has two positions that dedupe to one line; §10.5 has the details).
4. `docs/HISTORY.md`, `reports/baseline/*`, and `docs/PROVENANCE.md` did not
   move, so the noted one-commit corpus lag did not apply.
5. `SPECS/2026-11-16-edition-recovery-curation/requirements.md:174` keeps the
   old value as history, as this spec permits; `docs/RELEASE-NOTES.md` keeps it
   in the migration note. Generated output is clean.

### 10.11 Follow-up: comparison-only capitalisation from a glued apparatus code

`reports/diffs/rp2018--rp2018-2023/report.md` lists `MAR 14:65` and `LUK 9:22`
under `## Apparatus-only changes` as `capitalization`. The derived Unicode text
does not carry a case difference; the classification comes from the comparison
normaliser, not the production converter:

- at `MAR 14:65` the source token `e)/ballon.{B` (lowercase word glued to the
  `{B` apparatus code) and at `LUK 9:22` the token `a)nasth^nai.{B` are handled
  by `normalize.official_ccat_line` with its default comparison behaviour. Its
  `re.search(r"[A-Z]", token)` test sees the uppercase code letter `B` inside
  `{B`, prepends `*`, and treats the whole token as a capital;
- the production path (`faithful_capitals=True`, used by
  `normalize.production_ccat_line`) splits the token at `{` and marks a capital
  only from the word part, so it emits no `*`.

This is a pre-existing normaliser discrepancy, not a diff-category change and
not a bug in the report: the classifier compares the two layouts exactly as
`normalize.parse_cct` supplies them. The wording of the apparatus-only lead was
corrected to say only that "the derived Unicode text carries no corresponding
difference". The parser discrepancy should be investigated as a separate change
(and would reclassify those two rows); this change deliberately leaves the
comparison and normalisation logic untouched.
