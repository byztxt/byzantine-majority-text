# Validation - Documentation clarity, linkable references, and a Unicode apparatus diff

A change is complete only when every item below is checked against the actual
files, and command output or observed diffs are recorded in this document. The
authoritative checklist is `requirements.md` (R1-R7) and `plan.md` (phases 0-6).

## 0. Amendments recorded during implementation (2026-11-20)

This spec was written before `SPECS/2026-11-19-retire-legacy-unicode-trees/`
landed. The following changes are recorded here rather than applied silently.

### R4 is superseded and closed, not implemented

`csv-unicode/` and `tei-xml-unicode/` no longer exist in the working tree, and
`scripts/csv_converter.py` / `scripts/tei_xml_converter.py` were retired. The R4
deliverables that assumed a live working-tree counterpart (the
`## Working-tree paths and the curated editions` table, the two folder READMEs,
the root README paragraph, and the byte-identity test over the live trees)
cannot be implemented as written and were **not** implemented.

The same information landed in the retirement change, in post-removal form:

- `docs/EDITIONS.md` carries `## Where the old working-tree paths went`, whose
  table maps every retired path to `editions/rp2018-2023/` (or `docs/assets/`,
  `docs/COLLATEX.md`) and points at `docs/RELEASE-NOTES.md`;
- `docs/RELEASE-NOTES.md` records the breaking change;
- `tests/curate/test_editions.py::DocsTests` and
  `tests/curate/test_current_pipeline.py::LegacyTreesAreGoneTests` lock the
  absence and the mapping.

R4 is therefore closed as satisfied by the retirement change, not by this one.
Its remaining intent - that no reader-facing reference implies the trees still
exist - holds: a sweep of `docs/`, `reports/`, `scripts/README.md`, and the root
README finds the retired names only inside the old-to-new mapping tables and the
release note, and
`LegacyTreesAreGoneTests.test_no_tracked_file_reads_a_retired_path` enforces
that allowlist.

### R5 targets the post-removal dataset names

The datasets in `docs/DATA_CONTRACT.md` are
`editions/rp2018-2023/csv/...` and `editions/rp2018-2023/tei/...`. The retired
`csv-unicode/` paths are named nowhere in the document. `csv/unaccented` was
**not** added as a separate dataset, as decided.

### R6: `apparatus.diff` holds apparatus-only rows

`R6.4` says "one hunk per row with `apparatus_changed == "true"`", while the
preamble it mandates says "for every apparatus-only change" and the R6 check
below expects `rp2005--rp2018` to have hunks only for the 7 apparatus-only rows
with a Unicode difference. The literal "every row" reading would also include
main-text rows (for `rp2005--rp2018` that is most of the 55 source-tier rows),
contradicting both. It is implemented as the coherent reading:
`apparatus.diff` contains only apparatus-only rows (`text_changed == "false"`)
whose apparatus also differs in Unicode, matching the report's
`Apparatus-only changes` section.

Consequently the expected line count for
`rp2005-2019--rp2018/apparatus.diff` is **7**, not 1: the file always carries
the 6-line preamble plus the title. There are no hunks for that pair, because it
has no apparatus-only change.

### R7: the literal `provenance-unknown` is gone from generated output

`R7.2` prescribed a decision-log row whose option (b) reads "Keep
provenance-unknown". That would leave the retired status string in a generated
file, contradicting the acceptance criterion that no generated output calls the
Strong's files unknown. Option (b) was reworded to "Leave the files labelled
unknown"; the row, its evidence, and its `resolved (2026-11-19)` decision are
otherwise unchanged. The negative assertions in
`tests/reconciliation/test_integration.py` and `test_offline.py` keep the
literal as the guard that prevents its return.

### R1: the `Basis` tag is linkified at render time

The earlier amendment narrowed R1 to backticked tags, but the `Basis` column of
the four-editions table renders the manifest value "Recovered from git tag
v2.0.3 (textonly-beta-code + parsed)" as plain prose. That left the reader with
an unlinked tag and the test unable to see it. The generator now runs the
`Basis` cell through `docs._link_bare_tags`, so any `vX.Y.Z` in that value
becomes a `releases/tag/` link without editing `manifest.json`.
`test_every_release_tag_is_a_link` now strips every Markdown link and asserts no
`vX.Y.Z` remains anywhere, so the narrowed rule cannot return.

## 1. Preconditions

> **Note (2026-11-20):** the `csv-unicode/` and `tei-xml-unicode/` checks in
> this section are obsolete; the retirement change deleted those trees. See
> amendment §0. No untracked file needed moving aside for this change: the only
> untracked paths were this spec folder and the generated `apparatus.diff`
> files, none of which `recover_editions.py` copies.

- [ ] Branch is `feature/2026-11-16-edition-recovery-curation`. Do not switch
      branches and do not commit.
- [ ] The previous change's uncommitted edits are present and untouched:
      `git status --porcelain` lists the 29 modified files already in the tree
      before this change. Record the starting state:
      `git status --porcelain > /tmp/byz-docs-before.txt`.
- [ ] Python 3.10 with `pip install -r scripts/requirements.txt`. If that
      environment is unavailable, record the workaround in §9 (the previous
      change used a Python 3.12 venv with only `beta-code==1.0.0`, which is all
      the regeneration sequence and the tests import).
- [ ] Full git history and tags: `git tag --list v2.0.3 v3.3.4` prints both.
- [ ] The six committed archives exist:
      `ls data/raw/_archives/rp2005 data/raw/_archives/rp2018` shows three ZIPs
      each.
- [ ] Pre-existing untracked files are recorded and moved aside **before any
      regeneration**, because `recover_editions.py` copies whole directories and
      would otherwise copy `csv-unicode/ccat/with-variants/variant_analysis.py`
      into `editions/rp2018-2023/csv/accented/with-variants/`, changing
      `editions/rp2018-2023/manifest.json`:

```bash
git ls-files --others --exclude-standard > /tmp/byz-untracked.txt
mkdir -p /tmp/byz-untracked
git ls-files --others --exclude-standard -z | xargs -0 -r -I{} \
  mv {} /tmp/byz-untracked/
```

  Restore them byte-for-byte in §8 and confirm the file list is unchanged.
- [ ] Confirm the five overlapping views are byte-identical **before** starting,
      so a later diff is attributable to this change:
      `diff -rq csv-unicode/ccat/no-variants editions/rp2018-2023/csv/accented/no-variants`
      etc. (five pairs; no output expected).

## 2. Red phase

Write the tests from `plan.md` phases 1a, 2a, 2b, 3a, 4a, 5a, and 5b before
changing production code. Confirm each fails for the intended reason, not an
import error in the test itself.

- [ ] `tests/curate/test_generated.py::ReportingDocsTests` fails: the
      "Report generation order" text has no `stale`, has
      `owns the baseline document`, and `SPECS/MISSION.md` has `why category`.
- [ ] `tests/curate/test_editions.py::EditionsDocLinkTests` fails on
      `test_every_release_tag_is_a_link` (0 tag links) and on the commit link.
      At this point `test_relative_markdown_links_resolve` still passes.
- [ ] `tests/reconciliation/test_integration.py` fails on
      `official-source-files` (actual `provenance-unknown`), and
      `test_decision_log_row_r4_is_resolved` fails on `pending`.
- [ ] `tests/reconciliation/test_offline.py::test_provenance_doc_does_not_call_strongs_unknown`
      fails on the committed `docs/PROVENANCE.md`.
- [ ] `tests/curate/test_generated.py::test_tech_doc_calls_strongs_official`
      fails: `SPECS/TECH.md` §2 still says `must be established separately`.
- [x] `WorkingTreeViewTests` does not exist: R4 was superseded by the
      retirement change (amendment §0), so it is not part of this red phase.
      The post-removal facts it would have locked are covered by
      `tests/curate/test_editions.py::DocsTests` and
      `tests/curate/test_current_pipeline.py::LegacyTreesAreGoneTests`, which
      pass at `HEAD`.
- [ ] `tests/contract/test_integration.py::BaselineCsvTests` fails:
      `reports/baseline/invariants.csv` is 0 bytes, so it has no header.
      `DataContractDocTests` fails on `How to read this document` and `## Terms`.
- [ ] `tests/curate/test_diff.py` fails on `load_text("rp2018", "with-variants")`
      (`TypeError`) and on the variant word-diff assertion.
- [ ] `tests/curate/test_integration.py` fails on the file list (`apparatus.diff`
      missing) and on the appended CSV fields.
- [ ] `tests/curate/test_reproducible.py` still passes at HEAD (it builds a
      worktree at `HEAD`, which does not contain this change); it becomes the
      lock after the change is committed.

Record the failing command and the first failing assertion for each group.

## 3. Green phase: regeneration routine

Run from the repository root, in this order:

```bash
# 1. Provenance: validate the committed archives; no writes, no network.
python3 scripts/fetch_official.py --verify

# 2. Curated editions and diffs.
python3 scripts/recover_editions.py
python3 scripts/build_editions.py
python3 scripts/diff_editions.py

# 3. Reports. Contract first, reconciliation second (scripts/README.md).
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m byz.reconcile
```

- [ ] `--verify` exits 0 and prints `verified 6 archives`.
- [ ] `--force` is **not** used. If it was used by accident, restore the
      provenance TOMLs with `git checkout -- data/provenance/` and re-run
      `--verify`; record it in §9.
- [ ] After step 2, `git diff --stat -- data/raw source csv-unicode tei-xml-unicode editions/*/csv editions/*/tei editions/*/source editions/*/manifest.json`
      is empty. This is the "no data change" gate; a non-empty result means the
      untracked-file hazard in §1 fired, or a converter was run unnecessarily.
- [ ] `docs/HISTORY.md` still ends with exactly one `<!-- cycle2:begin -->` block
      and starts with exactly one banner after contract then reconciliation.

## 4. Item checks

> **Bookkeeping note (2026-11-20):** the boxes in this section are the
> implementation-time checklist. The authoritative results - the commands run
> and the observed values - are recorded in §12, and §11 states the overall
> outcome. The boxes were not re-ticked after the fact; §12 is the evidence of
> record.

### R1 - `docs/EDITIONS.md` links

- [ ] `grep -o '](https://github.com/byztxt/byzantine-majority-text/releases/tag/' docs/EDITIONS.md | wc -l`
      equals
      ``grep -o '`v[0-9]*\.[0-9]*\.[0-9]*`' docs/EDITIONS.md | wc -l``; no tag is
      left unlinked. Expected tags: `v1.0.0`, `v2.0.3`, `v3.0.0`, `v3.3.4`
      (repeated in the ranges, the prose, and the feature matrix).
- [ ] `grep -n '97371d7' docs/EDITIONS.md` shows exactly one line, and the hash
      is inside a `.../commit/97371d7` link.
- [ ] The four diff bullets (lines 240-243) read
      ``- `rp2005` -> `rp2005-2019` ([`reports/diffs/rp2005--rp2005-2019/`](../reports/diffs/rp2005--rp2005-2019/))``.
- [ ] `PdfLinkTests.test_relative_markdown_links_resolve` passes, proving the
      `../reports/diffs/...` targets exist from `docs/`.
- [ ] `git diff -- docs/EDITIONS.md` contains no other wording change in the
      sections this item does not touch; every changed line is a tag, commit, or
      diff-path substitution.

### R2 - `scripts/README.md`

- [ ] The "Report generation order" section names `docs/HISTORY.md`, the two
      markers, both commands, the required order, the three failure modes, and
      the idempotence sentence.
- [ ] It contains neither `owns the baseline document` nor
      `leaves exactly one block and one heading`.
- [ ] The commands in the section still match the ones in the root README's
      "Reproducing the curated data" block (`git diff` on the two files shows no
      command change).

### R3 - `SPECS/MISSION.md`

- [ ] Line 73 reads `and *what category* of change it is.`; `git diff` on the
      file is exactly that one-word change.

### R4 - Working-tree paths vs curated editions

> **Closed by `SPECS/2026-11-19-retire-legacy-unicode-trees/`.** See amendment
> §0. The trees are gone, the old-to-new mapping and the release note are
> generated, and the deletion is locked by tests. No item below is implemented
> in this change.

- [x] `docs/EDITIONS.md` contains `## Where the old working-tree paths went`,
      the retired-path table mapping each path to `editions/rp2018-2023/`, and
      the pointer to `docs/RELEASE-NOTES.md`.
- [x] The folder READMEs no longer exist, so there is nothing to update.
- [x] The root README contains no retired path
      (`DocsTests.test_root_readme_has_no_retired_tree`); the generated block
      still matches its generator.
- [x] `LegacyTreesAreGoneTests.test_no_tracked_file_reads_a_retired_path` passes,
      so no tracked file outside the allowlist names a retired path.
- [x] `editions/rp2018-2023/csv/**` contains no non-`.csv` file.

### R5 - `docs/DATA_CONTRACT.md` and `invariants.csv`

- [ ] `wc -c reports/baseline/invariants.csv` is 55 (the header plus its
      newline) and `cat` prints exactly
      `dataset,path,line,category,message,key,known_exception`.
- [ ] `wc -l reports/baseline/invariants.csv` is 1.
- [ ] `head -1 reports/baseline/invariants.csv` equals
      `",".join(byz.contract.model.VIOLATION_FIELDS)`.
- [ ] `docs/DATA_CONTRACT.md` has `## How to read this document`, `## Terms`,
      `## Coverage` with a `What it holds` column, `## Derivation map` with its
      two explanatory sentences, `## Invariant results (reports/baseline/invariants.csv)`,
      and `## Baseline report files`.
- [ ] `grep -n 'that is the next cycle' docs/DATA_CONTRACT.md` finds nothing;
      `grep -n 'Cycle 2' docs/DATA_CONTRACT.md` finds the replacement sentence
      and it points at `docs/PROVENANCE.md`.
- [ ] Every `What it holds` cell equals the matching
      `contracts.DATASET_CONTRACTS[...]["purpose"]` string (the generated doc
      test asserts this).
- [ ] `reports/baseline/summary.md` gained the "header with no data rows is the
      clean result" sentence and still reads
      `Invariant findings: 0 (0 unresolved, 0 known exception)`.
- [ ] `git diff -- reports/baseline/files.csv` changes only the two
      `scripts/README.md` rows (the `scripts` and `docs` datasets); it does
      **not** change the `README.md` row, because R4 was superseded and the root
      README was not edited. It does **not** gain a row for
      `reports/baseline/invariants.csv`; nothing under `reports/` is inventoried.

### R6 - Unicode apparatus diff

- [ ] Every `reports/diffs/<pair>/` contains `apparatus.diff`:
      `ls reports/diffs/*/apparatus.diff` lists four files.
- [ ] `changes.csv` header ends
      `...,text_left,text_right,text_changed,apparatus_word_diff,apparatus_changed`
      for all four pairs.
- [ ] `apparatus_changed` is `"true"` for `ROM 1:27` in `rp2005--rp2018` and
      `"false"` for `MAT 11:23` in `rp2018--rp2018-2023`.
- [ ] `apparatus.diff` for `rp2005--rp2018` has hunks only for the 7 rows whose
      Unicode apparatus differs; the 8th (`2PE 1:12`) is absent and is named in
      `report.md` as encoding-only.
- [x] `wc -l reports/diffs/rp2005-2019--rp2018/apparatus.diff` is **7** (the
      6-line preamble plus the title, and no hunks because that pair has no
      apparatus-only change). See amendment §0: the original "1" assumed the
      file had no preamble.
- [ ] Report counters: for `rp2018--rp2018-2023`, `shown + no Unicode difference
      == 156`; for `rp2005--rp2018`, `7 + 1 == 8`; for `rp2005--rp2005-2019`,
      `8 + 0 == 8`.
- [ ] `reports/diffs/README.md` documents `apparatus.diff`, the
      `apparatus_word_diff`/`apparatus_changed` columns, and the Apparatus
      notation bullet with the `{+{Byz τε > δε }+}` example.
- [ ] `docs/EDITIONS.md` lists `apparatus.diff` and describes the Unicode-first
      apparatus rendering.
- [ ] The extended
      `test_word_diffs_reconstruct_the_reference_text` passes for all three
      word-diff columns (`source_`, `text_`, `apparatus_`) over all four pairs.

### R7 - Strong's/BP5 provenance

- [x] `grep -rn 'provenance-unknown' docs reports` finds nothing. The generator
      in `src/byz/reconcile/report.py` no longer contains it either; the only
      remaining occurrences are the two negative assertions in the
      reconciliation tests (`test_strongs_rows_are_not_unknown`,
      `test_provenance_doc_does_not_call_strongs_unknown`), which are the guard.
      Historical specs keep their original wording.
- [ ] `docs/PROVENANCE.md` §"Strong's / BP5 provenance" reads
      ``Status: `official-source-files` (delivery route: `not-recorded`).`` and the
      three-sentence paragraph naming Dr. Maurice A. Robinson.
- [ ] `reports/reconciliation/summary.md` mapping-coverage table has a
      `` `official-source` | 27 `` row and no `provenance-unknown` row; its
      `## Strong's / BP5` section uses the new wording.
- [ ] `reports/reconciliation/decision-log.md` R4 contains
      `resolved (2026-11-19)` and does not end `| pending |`.
- [ ] `docs/EDITIONS.md` source feature matrix row for `source/Strongs` reads
      `official files, not in the six ZIPs`.
- [ ] `SPECS/TECH.md` §2 has the new sentence and no longer says
      `must be established separately`.
- [ ] `compare.run()["strongs"]` returns `status == "official-source-files"`,
      `delivery == ("recorded" if hits else "not-recorded")`, and `hits == []`
      today.

## 5. Document-level checks

- [ ] All 17 generated Markdown files still start with
      `<!-- generated-file: do not edit by hand -->` and the root README block
      still starts with `<!-- editions:begin -->` followed by
      `<!-- generated-block: do not edit by hand -->`.
- [ ] `grep -c 'editions:begin' README.md` and `grep -c 'editions:end' README.md`
      are both 1.
- [ ] No generated prose contains `<!-- editions:begin -->` or
      `<!-- editions:end -->` outside the block:
      `grep -n 'editions:' docs/EDITIONS.md docs/DATA_CONTRACT.md docs/PROVENANCE.md reports/**/*.md README.md`
      shows only the two README markers.
- [ ] `docs/EDITIONS.md`, `docs/DATA_CONTRACT.md`, `docs/PROVENANCE.md`,
      `reports/diffs/README.md`, and both decision logs contain no timestamp,
      hostname, or absolute path (`grep -nE '/home/|/tmp/|2026-11-19T' ...` is
      empty; the only dates are the existing editorial dates).

## 6. Test suites

```bash
PYTHONPATH=src python3 -m unittest discover -s tests/contract
PYTHONPATH=src python3 -m unittest discover -s tests/curate
PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation
```

- [ ] All three suites pass with 0 failures and no unplanned skips.
- [x] Every new test from `plan.md` is present and green: `ReportingDocsTests`
      (4), `EditionsDocLinkTests` (6), `BaselineCsvTests` (6),
      `DataContractDocTests` (8), four Strong's tests in
      `tests/reconciliation/test_integration.py`, one in `test_offline.py`, one
      in `test_generated.py`, five in `tests/curate/test_diff.py`, and four new
      methods (`test_encoding_only_rows_say_so`,
      `test_apparatus_counters_add_up`, `test_readme_documents_apparatus_diff`,
      `test_editions_doc_lists_apparatus_diff`) plus extensions to the existing
      report/CSV/reconstruction tests in `tests/curate/test_integration.py`.
      The R4 byte-identity tests are excluded because R4 was superseded
      (amendment §0). The counts were re-checked by the verifier on 2026-11-20;
      the review-fix round added three header tests to `BaselineCsvTests`
      and a fourth Strong's test.
- [ ] No test performs network access. Link checking is static: exact URL
      strings, plus the existing on-disk relative-link test.
- [ ] `tests/curate/test_reproducible.py` and
      `tests/contract/test_integration.py::ContractWorktreeTests` create a
      worktree at `HEAD`, so before this change is committed they exercise the
      old commit. Treat §7 as the authoritative pre-commit determinism evidence
      and re-run both after committing (or in a throwaway committed copy under
      `/tmp/opencode/`). Record which was done in §9.

## 7. Determinism: byte-identical second run

- [ ] After the first full run, snapshot the diff against `HEAD`:
      `git diff --binary > /tmp/byz-docs-run1.diff`.
- [ ] Run the entire §3 sequence a second time.
- [ ] `git diff --binary > /tmp/byz-docs-run2.diff` and
      `cmp /tmp/byz-docs-run1.diff /tmp/byz-docs-run2.diff` reports no
      difference. (The diff against `HEAD` is non-empty; this compares run 1 to
      run 2, not the tree to `HEAD`.)
- [ ] `git status --porcelain` after the second run equals the state after the
      first (apart from the moved untracked files from §1).
- [ ] Hash both snapshots of the generated files:
      `find docs editions reports -type f \( -name '*.md' -o -name '*.csv' -o -name '*.diff' -o -name '*.json' \) -print0 | sort -z | xargs -0 sha256sum`
      before and after the second run; every hash matches, including the four new
      `apparatus.diff` files and the one-line `invariants.csv`.
- [ ] `git diff -- docs/EDITIONS.md` is stable across the two runs, so no
      tag-derived value (for example `latest_release`) changed between them.

## 8. Restore untracked files and confirm scope

- [ ] Restore the untracked files moved in §1:
      `cd /tmp/byz-untracked && find . -type f -print0 | xargs -0 -r -I{} cp --parents {} "$OLDPWD"/`
      (or move them back individually), then confirm
      `git ls-files --others --exclude-standard` matches
      `/tmp/byz-untracked.txt`.
- [ ] `git status --porcelain` shows only intended changes: source modules,
      tests, the hand-edited docs, and regenerated outputs. No file under
      `data/raw/`, `source/`, `csv-unicode/**/*.csv`,
      `tei-xml-unicode/**/*.xml`, `editions/*/source/`, `editions/*/csv/`,
      `editions/*/tei/`, or `editions/*/manifest.json`.
- [ ] `git diff --stat` on `editions/` is **empty**: this change does not touch
      `editions/*/README.md`, `manifest.json`, `csv/`, `tei/`, or `source/`. If
      anything under `editions/` changed, the untracked-file hazard in §1 fired
      or a converter ran unnecessarily.

## 9. Deviations log

Record every deviation from `plan.md` here with its reason. Known candidates:

1. Python/pinned-package environment differences (see §1).
2. Pre-existing untracked files moved aside for the determinism run (the
   `variant_analysis.py` and `essay/` files), and whether `recover_editions.py`
   needed them absent.
3. Pre-commit worktree tests exercising `HEAD`; where the green run was done
   instead.
4. Any line-number drift in `docs/EDITIONS.md`, `src/byz/curate/docs.py`, or
   `src/byz/curate/diff.py` relative to `plan.md` (the previous change shifted
   lines), recorded per task group.
5. Any difference between the documented path table and the tree, for example a
   sixth overlapping view discovered while implementing R4.

The deviations actually observed are recorded in §0 (R4 supersession, the R6
apparatus-only scope, the R7 wording change, and the `Basis`-cell
linkification), §12 (the review-fix round), and §13 (the verifier pass,
including the two minor plan deviations there).

## 10. Manual inspection

- [ ] Open `docs/EDITIONS.md` in a Markdown preview (or on GitHub): the "Repo
      releases" cells show clickable tag pairs, the commit hash in "Why the
      history looks messy" is clickable, the four "Successive diffs" bullets link
      to the diff directories, and the retired-path table points at
      `editions/rp2018-2023/`.
- [ ] Open **a regenerated diff report** and confirm an apparatus-only entry now
      shows a readable Unicode line. Specifically:

```bash
sed -n '/## Apparatus-only changes/,/## Derived-only/p' \
  reports/diffs/rp2005--rp2018/report.md | head -20
```

  Expected: for `ROM 1:27`, a first line
  ``- `ROM 1:27` · `variant` `` followed by
  ``  - Apparatus (Unicode): `...{+{Byz τε > δε }+}...` `` in Greek, then
  ``  - Apparatus (Beta code): `...O(MOI/WS TE {+{B TE > DE }+}...` ``.
  Then confirm `1CO 3:14` reads `{+{Byz ME/NEI > MENEI= }+}` (or the archive's
  exact Greek apparatus) and that the Beta-code line is still present.
- [ ] Open `reports/diffs/rp2018--rp2018-2023/report.md` at `MAT 11:23` and
      confirm it says
      `no difference after conversion to Unicode (Beta-code encoding only)`
      instead of an empty code span.
- [ ] Open `reports/diffs/README.md`: the Files list includes `apparatus.diff`,
      the Notation section defines Apparatus and shows the doubled-brace example,
      and the `changes.csv` bullet names the two new columns.
- [ ] Open `reports/baseline/invariants.csv` in a spreadsheet or editor: it shows
      one header row and no data rows. Read `docs/DATA_CONTRACT.md` from the top
      with no prior knowledge: the purpose, the section guide, the terms, the
      "header with no rows is clean" statement, and the per-file table are all
      understandable without opening the source.
- [ ] Open `docs/PROVENANCE.md`: "Strong's / BP5 provenance" states
      `official-source-files` and the delivery-route caveat, and the document no
      longer calls the parsed files unknown.
- [ ] Open `scripts/README.md` at "Report generation order" and follow it as a
      first-time user: the reason for the order and the three failure modes are
      clear without reading `src/byz/contract/report.py`.
- [ ] Open `docs/RELEASE-NOTES.md`: the removal is explained and points at the
      retired-path table in `docs/EDITIONS.md`.

## 11. Definition of done

- [x] R1: every tag (including the `Basis` cell) and the commit in
      `docs/EDITIONS.md` are links, and no bare `vX.Y.Z` remains outside a link;
      the four diff bullets are relative links that resolve.
- [x] R2: the report-order section is explained in plain language with the
      failure modes; the jargon phrases are gone.
- [x] R3: the typo is fixed and nothing else in `SPECS/MISSION.md` changed.
- [x] R4: closed as satisfied by the retirement change (amendment §0); the
      relationship now lives in `docs/EDITIONS.md`'s retired-path table and
      `docs/RELEASE-NOTES.md`, and the deletion is locked by tests.
- [x] R5: `docs/DATA_CONTRACT.md` is self-contained, `invariants.csv` always has
      its seven-column header, and an empty file can no longer be mistaken for a
      broken run.
- [x] R6: every apparatus-only change shows a Unicode line and a Beta-code line;
      the 37 encoding-only rows say so; `apparatus.diff` and the two CSV columns
      exist and are documented; the Beta-code view is intact.
- [x] R7: no generated file calls `source/Strongs` provenance-unknown; R4 is
      resolved; `SPECS/TECH.md` §2 agrees.
- [x] The full regeneration runs twice with no diff; all three suites pass; no
      corpus, archive, CSV, TEI, manifest, or checksum changed.
- [x] Every deviation is recorded in §0 (post-retirement amendments) and §9.

## 12. Recorded results (2026-11-20)

Branch `feature/2026-11-16-edition-recovery-curation`, HEAD `47d664a`.
Environment: Python 3.12.3 in `/tmp/opencode/venv-byz`, with only
`beta-code==1.0.0` (all the regeneration and tests import).

- **Regeneration twice.** `fetch_official.py --verify`, record-mode
  `fetch_official.py`, `recover_editions.py`, `build_editions.py`,
  `diff_editions.py`, `byz.contract`, `byz.reconcile` ran twice.
  `cmp /tmp/byz-docs-run1.diff /tmp/byz-docs-run2.diff` reports no difference,
  and the two `git status --porcelain` snapshots are identical. No timestamps,
  hostnames, or absolute paths were introduced.
- **No corpus drift.** `git status --porcelain -- editions/` is empty and
  `git status --porcelain -- data/ source/` is empty. 37 tracked files changed,
  all generators, tests, hand-written docs, and generated reports; four new
  `reports/diffs/*/apparatus.diff`.
- **`invariants.csv`.** 55 bytes: the header
  `dataset,path,line,category,message,key,known_exception` and no data rows.
- **`docs/EDITIONS.md`.** 23 backticked tag spans and 23 `releases/tag/` links
  (the extra one is the `Basis` cell's `v2.0.3`); stripping every Markdown link
  leaves no `vX.Y.Z`; one `commit/97371d7` link; four
  `../reports/diffs/<pair>/` links;
  `PdfLinkTests.test_relative_markdown_links_resolve` passes.
- **Apparatus.** `reports/diffs/*/apparatus.diff` hunk counts are 8, 0, 120, 7
  (`wc -l` 23, 7, 247, 21). `2PE 1:12` in `rp2005--rp2018` has no hunk and is
  rendered with the encoding-only sentence. Report counters are 8 = 8 + 0,
  156 = 120 + 36, and 8 = 7 + 1. All four `changes.csv` files end
  `apparatus_word_diff,apparatus_changed`.
- **Provenance.** `grep -rn 'provenance-unknown' docs reports` finds nothing;
  `docs/PROVENANCE.md` reads `official-source-files` with the delivery-route
  caveat; the reconciliation decision log's R4 row is `resolved (2026-11-19)`.
- **Suites.** contract 64, curate 161, reconciliation 69; all pass. (The
  review-fix round added the unlinked-tag assertion, the non-empty
  `invariants.csv` check, the Strong's delivery/hits check, two `load_text`
  rejection checks, the generated-prose assertions, the five-CSV header-field
  checks, and the report-prose hit simulation.)
- **Review-fix round (2026-11-20).** Fixed the R1 command above to compare link
  occurrences with backticked tags (23 each); aligned `requirements.md` and
  `plan.md` with the derived `delivery`; made the "None of the six archives"
  wording conditional on `hits` in `docs/PROVENANCE.md`,
  `reports/reconciliation/summary.md`, and the R4 decision-log row; reworded the
  diff report's apparatus-shape sentence; narrowed the `_link_bare_tags`
  docstring to what the regex guarantees; and passed `fields` for all five
  baseline CSVs (byte-identical output). See §4's bookkeeping note for why the
  item boxes are not re-ticked.
- **Worktree-at-`HEAD` checks.** `ContractWorktreeTests` (4 tests) and
  `RegenerationDeterminismTests` (2 tests) passed in the live tree rather than
  failing: `HEAD` is self-consistent because both its generator and its
  generated outputs predate this change, so the expected one-commit lag did not
  appear. They should still be re-run once the change is committed.
- **Documented output.** `reports/diffs/rp2005--rp2018/report.md` shows for
  `ROM 1:27` the Unicode line
  ``  - Apparatus (Unicode): `...{+{Byz τε > δε }+}...` `` followed by
  ``  - Apparatus (Beta code): `...O(MOI/WS TE {+{B TE > DE }+}...` ``; for
  `1CO 3:14` the Unicode apparatus is `{+{NA μένει > μενεῖ }+}`.

## 13. Verifier pass (2026-11-20)

Branch `feature/2026-11-16-edition-recovery-curation`, HEAD `47d664a`, using
`/tmp/opencode/venv-byz` (`beta-code==1.0.0`). This section records the
independent verification of the change against the working tree.

- **Regeneration twice.** The full §3 sequence ran twice; record-mode
  `fetch_official.py` rewrote the provenance TOMLs byte-identically.
  `git status --porcelain`, `git diff --binary`, and a SHA-256 snapshot of every
  generated `*.md`/`*.csv`/`*.diff`/`*.json` under `docs/`, `editions/`, and
  `reports/` were identical between the runs and matched the pre-run tree.
- **No data drift.** `git status --porcelain -- editions/ data/ source/` is
  empty.
- **Output inspection.** `reports/diffs/rp2005--rp2018/report.md` shows
  `ROM 1:27` with the Unicode line first and the Beta-code line second;
  `MAT 11:23` in `rp2018--rp2018-2023` carries the encoding-only sentence.
  `apparatus.diff` hunk counts are 8, 0, 120, 7 (23, 7, 247, 21 lines).
  `reports/baseline/invariants.csv` is 55 bytes and one header line, and
  `write_csv(..., fields=VIOLATION_FIELDS)` writes the header plus a synthetic
  violation row correctly.
- **CSV/TEI integrity.** All 448 edition CSVs parse with the
  `chapter,verse,text` header and unique integer keys; all 224 TEI files parse
  with `BxxKxVx` anchors.
- **Links.** All 23 backticked release tags are `releases/tag/` links, the one
  commit hash is a `commit/` link, the four diff links and the other relative
  links resolve from `docs/`, and the tags and commit exist in the clone.
- **Suites.** contract 64, curate 161, reconciliation 69; all pass.
  `ContractWorktreeTests` (4) and `RegenerationDeterminismTests` (2) are green.
- **Documentation sync.** No README edit was needed: `scripts/README.md` was
  already rewritten by this change, and the root `README.md` and
  `source/README.md` still describe the current tree. The root README's
  generated-files table is a summary, not an exhaustive file list, so it was
  left alone (the new `apparatus.diff` is documented in `docs/EDITIONS.md` and
  `reports/diffs/README.md`). The §6 test inventory above was corrected to the
  actual counts.

**Minor deviations from `plan.md`, none blocking.** `write_csv` receives
`fields` for all five baseline CSVs, not only `invariants.csv` (plan phase 4);
the output is byte-identical and the tests lock every header (§12).
`mapping_rows()` keeps `"edition": "unknown"` on the 27 BP5 rows rather than
changing it to `"source"` as plan phase 2d suggested; `requirements.md` R7.1
prescribes only the `official-source` class and the note, both present, and the
`edition` column means the source archive edition, which genuinely has no
mapping. `tests/curate/test_editions.py` carries one expected-URL constant for
its link assertions, so R1.1's "no other literal copy" holds for production
code but not for the test fixture.

After the commit: re-run `PYTHONPATH=src python3 -m byz.contract` and
`PYTHONPATH=src python3 -m byz.reconcile`, then commit the refreshed
`reports/baseline/files.csv` (its `last_commit` column lags by one commit until
that follow-up lands). Re-run `tests/curate/test_reproducible.py` and
`ContractWorktreeTests` against the new `HEAD` as the post-commit lock.
