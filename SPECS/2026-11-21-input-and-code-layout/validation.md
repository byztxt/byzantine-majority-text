# Validation - Inputs under `data/`, code under `src/`, outputs under `editions/`

A change is complete only when every item below is checked against the actual
files, and the command output or observed result is recorded here. The
authoritative checklist is `requirements.md` (`R1`-`R8`) and `plan.md`
(phases 0-6).

The non-negotiable gate is §3: **the editions did not change**. If a
regenerated CSV, TEI, or source snapshot differs by one byte, or a manifest hash
entry differs at all, stop and report; do not adjust the edition to match the
new pipeline.

## 1. Preconditions and the before-snapshot

- [x] Branch is `feature/2026-11-16-edition-recovery-curation`; the base commit
      is `9a5a9d1`. The before-snapshot is `git show HEAD:...`, so the diff is
      measured against that commit.
- [x] `python3 -c "import beta_code"` succeeds. Interpreter
      `/tmp/opencode/venv-byz/bin/python3` (Python 3.12.3), `beta-code==1.0.0`
      (recorded in §11).
- [x] `git tag --list v2.0.3 v3.3.4` prints both tags.
- [x] Byte snapshot of every edition artifact. `wc -l` was **844** files under
      `editions/*/{source,csv,tei}` (the remaining 8 of the 852 tracked
      `editions` files are the four manifests and four READMEs):

```bash
find editions -type f \
  \( -path 'editions/*/source/*' -o -path 'editions/*/csv/*' \
     -o -path 'editions/*/tei/*' \) -print0 \
  | sort -z | xargs -0 sha256sum > /tmp/opencode/byz-layout-editions-before.sha256
wc -l /tmp/opencode/byz-layout-editions-before.sha256
```

  Record the line count. It must be the same after the change.

- [x] Manifest snapshot, one file per edition, from `HEAD` (`9a5a9d1`):

```bash
for id in rp2005 rp2005-2019 rp2018 rp2018-2023; do
  git show "HEAD:editions/$id/manifest.json" \
    > "/tmp/opencode/manifest-$id-before.json"
done
```

- [x] Tracked inventory at `HEAD`: `git ls-files scripts | wc -l` → **9**,
      `git ls-files source | wc -l` → **57**, `wc -l reports/baseline/files.csv`
      → **219** (218 data rows plus the header).
- [x] The untracked `scripts/beta_to_unicode_custom/__pycache__/` was removed
      before the move.

## 2. Red phase

Write the tests from `plan.md` phases 1a, 2a, 3a, 4a, 5a before changing
production code. Confirm each fails **for the intended reason**, not from an
import error or a typo.

- [x] `tests/curate/test_layout.py` fails because `data/text` does not exist and
      `source/` does.
- [x] `tests/contract/test_integration.py::test_dataset_set` fails with
      `source/CCAT`/`source/Strongs` in the actual set.
- [x] `tests/contract/test_integration.py::test_contract_json_matches_the_dataset_names`
      fails while `docs/contract/source__*.json` exist.
- [x] `tests/curate/test_build.py::ConverterPackageTests` fails with
      `ModuleNotFoundError: byz.beta` and on `sys.path` in `build.py`/`recover.py`.
- [x] `tests/curate/test_layout.py::EntryPointTests` fails because `scripts/`
      still exists and `byz.build` does not import.
- [x] `RootReadmeTests` fails on `docs.render_root_readme` (block markers
      expected) and on the missing template.
- [x] `tests/curate/test_generated.py` fails on 17 banner files and
      `test_block_banner…`.
- [x] The phase 5 doc tests fail on missing `MOVED_PATHS`, the release-note
      entry, `docs/BUILD.md`, and the TECH.md assertions.

The red phase was run when the tests were added, before the move. It cannot be
replayed in the finished tree without reverting the move; the failure reasons
above are the ones the tests assert. The equivalent final evidence is the
worktree failure at commits A and B in §9, which proves the tests still fail
when `HEAD` is not converged.

## 3. The byte-identity gate

### 3.1 Edition artifacts

- [x] After the full regeneration (`§8`), re-run the phase 1 `find … sha256sum`
      into `/tmp/opencode/byz-layout-editions-after.sha256` and:

```bash
diff /tmp/opencode/byz-layout-editions-before.sha256 \
     /tmp/opencode/byz-layout-editions-after.sha256
```

  Result: no output; `wc -l` stayed **844**. No file was added or removed under
  `editions/*/{source,csv,tei}`.

- [x] `git status --porcelain -- editions` lists only `editions/*/README.md` and
      `editions/*/manifest.json`. Any `csv/`, `tei/`, or `source/` path fails
      this gate. Result: empty.
- [x] `git diff --stat -- 'editions/*/csv' 'editions/*/tei' 'editions/*/source'`
      is empty. Result: empty.
- [x] Prove the gate can fail: appended one byte to
      `editions/rp2018-2023/csv/accented/no-variants/MAT.csv` in the scratch
      clone; `git status` named that file (`1 file changed, 1 insertion(+)`),
      then it was restored byte-for-byte from a copy and `git status` was
      empty again.

### 3.2 Manifest hash lists (the only permitted metadata diff)

- [x] Run:

```bash
python3 - <<'PY'
import glob, json
for path in sorted(glob.glob("editions/*/manifest.json")):
    edition = path.split("/")[1]
    old = json.load(open(f"/tmp/opencode/manifest-{edition}-before.json"))
    new = json.load(open(path))
    for key in ("source_files", "artifact_files"):
        assert old[key] == new[key], f"{edition}: {key} changed"
    changed = sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k))
    print(edition, changed)
PY
```

  Expected output, and nothing else:

```
rp2005 ['generated_by']
rp2005-2019 ['generated_by']
rp2018 ['generated_by']
rp2018-2023 ['generated_by', 'source_commit', 'strongs_commit']
```

  This delta is measured against `HEAD` **after the move commit**. Before the
  move lands, only `generated_by` differs: `source_commit` / `strongs_commit`
  still resolve to the last pre-move commit because the renamed paths are not in
  git history yet. Regenerating after the move commit moves them to that commit.

- [x] `generated_by` is `"PYTHONPATH=src python3 -m byz.build"` in all four; the
      command exists (§4).
- [x] Recorded the before/after values of the three keys in §11. `source_commit`
      and `strongs_commit` are new commit hashes (the move commit); that is
      intended and documented in `docs/EDITIONS.md`.
- [x] `tests/curate/test_fidelity.py::ManifestIntegrityTests` passes, so every
      `sha256`/`size` in every manifest still matches its file (part of the
      green `tests/curate` suite, §9).

### 3.3 No text or input change

- [x] `git diff HEAD --stat -- data/raw data/provenance` is empty.
- [x] `git diff --cached --summary -M` records all 56 data files as
      `rename {source => data/text}/... (100%)`; `source/README.md ->
      data/text/README.md` is `RM` (the path is corrected and one sentence is
      added), as expected.
- [x] The `sha256` of `CCAT/01_MAT.TXT` is
      `0de6c3ca28ea270a8902414b95df2a95d259c092e2cc37a0a39aeabad1373e29`
      before and after (also visible as the unchanged `git_blob` in
      `files.csv`).

## 4. Layout gates

- [x] `test -e source` and `test -e scripts` both fail; `ls -ld source scripts`
      reports "No such file or directory".
- [x] `git ls-files source scripts` prints nothing.
- [x] `git status --porcelain | grep -E '^.. (source|scripts)/'` prints nothing
      in the converged tree (no stub or symlink left behind). In the
      uncommitted tree the same grep only matches the staged `R  source/... ->
      data/text/...` renames, which are the move itself.
- [x] `data/text/CCAT` has **29** `.TXT`, `data/text/Strongs` **27** `.BP5`,
      `data/text/README.md` exists.
- [x] `requirements.txt` is exactly `beta-code==1.0.0`:

```bash
python3 -c "print(sorted(l for l in open('requirements.txt').read().splitlines() if l.strip()))"
```

- [x] The four entry points exist and expose `main` (`['main', 'main',
      'main', 'main']`):

```bash
PYTHONPATH=src python3 -c "import byz.fetch, byz.recover, byz.build, byz.diff; print([m.main.__name__ for m in (byz.fetch, byz.recover, byz.build, byz.diff)])"
PYTHONPATH=src python3 -m byz.fetch --help
```

- [x] `src/byz/beta/converter.py` imports and the two helpers return it;
      `grep -rn "sys.path" src/ --include='*.py'` finds nothing (0 hits).
- [x] `src/byz/curate/tei_xml_header.xml` exists, and the behaviour test
      `test_tei_header_is_package_data` builds a book and finds the header in
      the TEI (`<teiHeader>`, the Robinson/Pierpont statement, and no
      `BOOK_METADATA_PLACEHOLDER`).
- [x] `tests/curate/test_layout.py` and `tests/curate/test_current_pipeline.py`
      pass (part of §9).

## 5. The retired-layout sweep (R8)

Run all four, from the repository root:

```bash
git grep -n -E '(^|[^[:alnum:]_./-])source/(CCAT|Strongs|README\.md)' \
  -- ':!SPECS' ':!editions'

git grep -n -E 'python3 scripts/|scripts/(requirements\.txt|beta_to_unicode_custom|tei_xml_header\.xml|README\.md)' \
  -- ':!SPECS' ':!editions'

git grep -n -E '`source/`|\(source/\)|\(\.\./source/\)' \
  -- ':!SPECS' ':!editions'

git grep -n -E '(^|[^[:alnum:]_./-])(fetch_official|recover_editions|build_editions|diff_editions)\.py' \
  -- ':!SPECS' ':!editions'
```

Expected offenders, and nothing else. The allowlist has 13 entries (the
implementation widened it from the six entries first drafted here; see §11):

| File | Why it is allowed |
| --- | --- |
| `docs/EDITIONS.md` | renders the `MOVED_PATHS` / `RETIRED_PATHS` tables |
| `docs/RELEASE-NOTES.md` | the dated breaking-change entries |
| `docs/HISTORY.md` | keeps the pre-move paths as historical tag labels |
| `docs/PROVENANCE.md` | names paths inside the historical tags |
| `reports/reconciliation/history.csv` | the same historical tag labels |
| `reports/reconciliation/summary.md` | the same historical tag labels |
| `src/byz/curate/docs.py` | holds the authoritative mapping constants |
| `src/byz/contract/history.py` | holds the git pathspecs for pre-move history |
| `src/byz/reconcile/historical.py` | reads paths inside tags `v2.0.3` / `v3.0.0` |
| `src/byz/reconcile/report.py` | renders the archive prose from those labels |
| `tests/contract/test_integration.py` | asserts the retired datasets are gone |
| `tests/curate/test_editions.py` | asserts the retired tree is gone |
| `tests/curate/test_layout.py` | contains this sweep's own needles |

- [x] Anything else fails: especially `README.md`,
      `src/byz/curate/README.template.md`, `data/text/README.md`,
      `docs/BUILD.md`, reports outside the two allowlisted reconciliation
      files, `.opencode/**`, and the root `requirements.txt` (no pattern
      applies, checked for completeness). In particular
      `reports/reconciliation/decision-log.md` must not name the retired
      entry point: R8 now reads `PYTHONPATH=src python3 -m byz.fetch --verify`.
      Result: the sweep's only offenders are the 13 allowlisted files above;
      `reports/reconciliation/decision-log.md` is clean.
- [x] `SPECS/TECH.md` has no `scripts/` and no `source/CCAT`:

```bash
grep -n -E 'scripts/|source/CCAT|source/Strongs|source/README' SPECS/TECH.md
```

  Expected: no output.
- [x] `editions/**` is excluded because `editions/<id>/source/…` is the
      edition's own snapshot, but the one repository-level sentence is locked
      separately:

```bash
grep -n 'data/text/' editions/rp2018-2023/README.md
grep -n 'repository `source/`' editions/rp2018-2023/README.md
```

  The first printed ``duplicates the repository `data/text/`.``; the second
  printed nothing.
- [x] `tests/curate/test_layout.py::test_no_tracked_file_names_the_removed_layout`
      is green. Mutation check for the new entry-point pattern: appending
      `` An old command: `fetch_official.py --verify`. `` to `docs/BUILD.md` in
      the scratch clone made the test fail with
      `"docs/BUILD.md: 'fetch_official.py'"`; restoring the file made it green.
      This is exactly the B2 class of bug the pattern exists to catch.

## 6. Generated documentation

- [x] `docs/EDITIONS.md` contains `## Where the code and inputs moved
      (2026-11-21)`, every `docs.MOVED_PATHS` row, the "bytes and hashes did not
      change" sentence, and a link to `RELEASE-NOTES.md`.
- [x] `docs/EDITIONS.md`'s "Rebuilding the curated editions" block contains the
      four new commands and no `scripts/` command.
- [x] `docs/RELEASE-NOTES.md` has the 2026-11-21 entry, lists the removed
      commands and doc paths, says there are no shims, and links the canonical
      table.
- [x] `docs/DATA_CONTRACT.md` names `data/text/CCAT`, `data/text/Strongs`,
      `src/byz/`, and no `scripts/`.
- [x] `docs/contract/` contains `contracts.json`, the six
      `editions__rp2018-2023__*.json`, `data__text__CCAT.json`, and
      `data__text__Strongs.json` — and no `source__*.json`:

```bash
ls docs/contract
python3 -m unittest tests.contract.test_integration.IntegrationTests.test_contract_json_matches_the_dataset_names -v
```

- [x] `reports/baseline/files.csv` has no `scripts` dataset row (0), has one
      `data/text/README.md` row and one `docs/BUILD.md` row, and names
      `data/text/CCAT` (29 rows) / `data/text/Strongs` (27 rows).
- [x] `reports/reconciliation/{files,history}.csv` use
      `current data/text/CCAT`; the history rows `v2.0.3 textonly-beta-code`
      and `v3.0.0 source/CCAT` (path inside the tag) are unchanged, with the
      same figures (7918/7969/7754/7796).
- [x] `docs/HISTORY.md` labels the input rows `data/text/CCAT` /
      `data/text/Strongs`. The *First added* dates and the tag-labelled
      historical evidence stay pre-move, but the input rows' *Last changed*
      moves to the move commit: their pathspec pair lists both the old and the
      new location (`src/byz/contract/history.py`).
- [x] `README.md` is byte-identical to the render (the command printed
      `True`):

```bash
PYTHONPATH=src python3 -c "
from pathlib import Path
from byz import generated
from byz.curate import docs
template = Path('src/byz/curate/README.template.md').read_text(encoding='utf-8')
print(Path('README.md').read_text(encoding='utf-8') == generated.markdown(docs.render_root_readme(template)))
"
```

  Prints `True`.

- [x] `README.md` starts with the banner, contains no `editions:begin` /
      `editions:end` (count 0), and renders twice identically:

```bash
head -2 README.md
grep -c 'editions:begin' README.md   # 0
```

- [x] `docs/BUILD.md` contains the six module commands, the install line, the
      pipeline notes, the report-generation order, and "Editing the root
      README".

## 7. Links

- [x] `python3 -m unittest tests.curate.test_editions.PdfLinkTests -v` passes
      with the extended `_user_docs()` (README, the four edition READMEs,
      `docs/{EDITIONS,COLLATEX,RELEASE-NOTES,BUILD}.md`, `data/text/README.md`).
- [x] `data/text/README.md` links resolve from one directory deeper
      (`../../editions/`, `../../docs/EDITIONS.md`).
- [x] `docs/BUILD.md` carries no Markdown links; it names `data/text/`,
      `README.md`, `docs/EDITIONS.md`, and `docs/RELEASE-NOTES.md` as code
      spans, and those targets exist.
- [x] The root README's `` [`data/text/`](data/text/) `` and
      `` [`docs/BUILD.md`](docs/BUILD.md) `` targets exist.

## 8. Regeneration and determinism (new commands)

Run from the repository root, in this order:

```bash
PYTHONPATH=src python3 -m byz.fetch --verify
PYTHONPATH=src python3 -m byz.recover
PYTHONPATH=src python3 -m byz.build
PYTHONPATH=src python3 -m byz.diff
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m byz.reconcile
PYTHONPATH=src python3 -m byz.contract
```

- [x] `byz.fetch --verify` exits 0 with no network access and writes nothing
      (`git diff HEAD -- data/provenance` empty).
- [x] `git diff --binary > /tmp/opencode/byz-layout-run1.diff`; ran the sequence
      a second time; wrote `run2.diff`; the two diffs are identical, and a
      914-file sha256 snapshot of `README.md docs reports editions
      data/provenance` is identical too. (The diff against `HEAD` is expected
      to be non-empty; this compares the two runs.)
- [x] `git status --porcelain` after run 2 equals the state after run 1.
- [x] `ls -a editions/` has no `.rp*` staging directory.
- [x] `docs/HISTORY.md` has exactly one generated banner and exactly one
      `<!-- cycle2:begin -->` block after the two report commands.
- [x] No wall-clock timestamp, hostname, or absolute path in generated output:

```bash
git grep -n -E '/home/|localhost|/tmp/opencode' -- README.md docs reports editions
```

  Expected: no output. (The repository's own `.opencode/` directory is named in
  the README and is not a temp path; the pattern targets an absolute `/tmp`
  path. Git commit dates in `docs/HISTORY.md` and
  `editions/*/manifest.json`'s commit hashes are stable history, not run
  metadata.)

## 9. The suites

```bash
PYTHONPATH=src python3 -m unittest discover -s tests/contract
PYTHONPATH=src python3 -m unittest discover -s tests/curate
PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation
```

- [x] All three pass with 0 failures and 0 unplanned skips. At the converged
      scratch commit C: `tests/contract` **64**, `tests/curate` **181**,
      `tests/reconciliation` **69**, all `OK`. The live uncommitted tree cannot
      pass the two worktree classes (see below).
- [x] `tests/curate/test_reproducible.py` passes after the change commit and the
      **two** follow-up regeneration commits; before the change it fails for the
      known reason (it builds a worktree at `HEAD`). The §8 two-run check is the
      authoritative pre-commit evidence.
- [x] `tests/contract` `ContractWorktreeTests` pass after the **two** follow-up
      regeneration commits (they compare `HEAD` with a fresh run). One follow-up
      is not enough: the first touches `editions/*/manifest.json`, and
      `editions` is in `CORPUS_PATHSPECS`, so "Last corpus commit" moves; the
      second records it in `docs/HISTORY.md`.
- [x] No test touches the network; no test writes to the repository.

Recorded convergence (scratch clone of the same working tree):

| Commit | Contents | `tests/contract` | `tests/curate` | `tests/reconciliation` |
| --- | --- | --- | --- | --- |
| A (the change) | move + code + regenerated docs | 2 failures | 1 failure | OK |
| B (first follow-up) | manifests + `files.csv` + `docs/HISTORY.md` | 2 failures | 1 failure | OK |
| C (second follow-up) | `docs/HISTORY.md` only | **OK** | **OK** | **OK** |

At A and B exactly three tests fail: `ContractWorktreeTests` (2) and
`RegenerationDeterminismTests::test_committed_outputs_match_a_fresh_run` (1).
The live uncommitted tree shows the same pre-commit failures (contract 1,
curate 1 error) and `tests/reconciliation` passes. The failure at A/B is not a
bug: the committed `HEAD` is not yet the converged output.

## 10. Manual inspection

- [ ] Read the rendered `README.md` start to finish. "Start here", the layout
      table, "Source of truth and provenance", and "Which text should I use?"
      send a reader to `data/text/`, `src/byz/`, `docs/BUILD.md`, and
      `editions/rp2018-2023/`; nothing points at `source/` or `scripts/`.
- [ ] Read `src/byz/curate/README.template.md`. Its first line says it is the
      file to edit, and the two `{{…}}` lines sit exactly where the generated
      sections belong.
- [ ] Read `docs/BUILD.md` as a first-time contributor: install, the six
      commands, why `byz.recover` alone leaves the views empty, the report
      order, how to edit the README, how to run the tests.
- [ ] Read `docs/EDITIONS.md`'s new section: an old command or path can be
      found and mapped in one step, and the "bytes and hashes did not change"
      sentence is unambiguous.
- [ ] Read `docs/RELEASE-NOTES.md`: the breaking change is dated, complete, and
      does not promise a shim.
- [ ] Open `data/text/README.md`: it describes the input tree, distinguishes
      itself from `editions/<edition>/source/`, and its links work.
- [ ] Read `SPECS/TECH.md` §5 and §11: the layout block matches the physical
      tree, and §11 states the module-entry-point rule instead of "thin scripts
      in `scripts/`".
- [ ] Read one `.opencode` agent file and `read-conventions.md`: the commands
      they give run as written.
- [ ] `python3 -m byz.build` prints the three expected lines (`built 4
      editions`, `wrote …/docs/EDITIONS.md`, `updated …/README.md`).

## 11. Definition of done and deviations log

Definition of done:

- [x] `source/` and `scripts/` do not exist; `data/text/` holds the 57 input
      files (29 `.TXT` + 27 `.BP5` + `README.md`); `requirements.txt` is at the
      root.
- [x] All four entry points run as `PYTHONPATH=src python3 -m byz.<verb>`; no
      module manipulates `sys.path`; the converter and the TEI header live in
      `src/byz/`.
- [x] `README.md` is byte-identical to its template render, carries the
      full-file banner, and has no block markers; the template is the documented
      edit point.
- [x] Every edition artifact is byte-identical (§3.1); every manifest hash entry
      is identical (§3.2); only `generated_by`, `source_commit`, and
      `strongs_commit` changed, and they are recorded below.
- [x] `docs/EDITIONS.md`, `docs/RELEASE-NOTES.md`, `docs/BUILD.md`, and the
      regenerated contract/reconciliation docs name the new layout; the sweep
      (§5) has only the allowlisted offenders.
- [x] `SPECS/TECH.md` §2/§5/§7/§9/§11 and `.opencode/**` describe the real tree.
- [x] The sequence runs twice with no diff; the three suites pass; the **two**
      follow-up regeneration commits land (`reports/baseline/files.csv` then
      `docs/HISTORY.md`).
- [x] Every deviation from `plan.md` is recorded here with its reason.

Deviations log:

1. **Interpreter and `beta-code` version.** `/tmp/opencode/venv-byz/bin/python3`,
   Python **3.12.3**, `beta-code==1.0.0` (the packages target Python 3.10; no
   3.10-specific behaviour is used).

2. **Manifest metadata before → after.** Before is `HEAD` (`9a5a9d1`); after is
   the regenerated tree at the move commit (scratch **A** `7dbdd8e`). Important:
   in the *uncommitted* working tree only `generated_by` differs; the two commit
   fields move only after the move commit exists in git history.
   - `rp2005.generated_by`: `python3 scripts/build_editions.py` →
     `PYTHONPATH=src python3 -m byz.build`
   - `rp2005-2019.generated_by`: same change.
   - `rp2018.generated_by`: same change.
   - `rp2018-2023.generated_by`: same change.
   - `rp2018-2023.source_commit`: `16859b22c07f7d52b573fd3eab4919b1d7ddcbc1` →
     `7dbdd8e81c657428818e7b80a8e7d592bef637d7` (scratch A; the real move
     commit when this lands).
   - `rp2018-2023.strongs_commit`: `b7485a3dc4ef2d0436be2b9c47a1e386ed27db0d`
     → `7dbdd8e81c657428818e7b80a8e7d592bef637d7` (same).
   `source_files` and `artifact_files` are byte-identical in all four.

3. **`reports/baseline/files.csv` row delta.** 218 data rows → **209** (−9).
   The 9 `scripts` rows are gone; the `docs` row `source/README.md` is replaced
   by `data/text/README.md` (new hash/size: the path corrections and the one
   added sentence); `docs/BUILD.md` is a new `docs` row. The 56 moved input
   files keep their `git_blob`/`sha256`/`size` and appear under the new
   `data/text/{CCAT,Strongs}` dataset, and in the converged tree all 56
   `last_commit` values move to the move commit. Add the new
   `data/text/README.md` row (moved from `source/README.md`) and that is the
   **57** row churn the plan predicted; `docs/BUILD.md` replaces the removed
   `scripts/README.md` row.

4. **Retired-layout offenders found outside the allowlist, and the fixes.**
   - **B1:** `docs/EDITIONS.md`'s 2026-11-19 table pointed at the deleted
     `source/README.md`. Fixed in `src/byz/curate/docs.py` (`RETIRED_PATHS`) to
     `data/text/README.md`, then regenerated.
   - **B2:** `reports/reconciliation/decision-log.md` (decision R8) told the
     reader to run `fetch_official.py --verify`. Fixed in
     `src/byz/reconcile/report.py` to
     `PYTHONPATH=src python3 -m byz.fetch --verify`, then regenerated.
   Both were fixed rather than allowlisted.

5. **Allowlist widening (deviation from R8.2 as first drafted).** The sweep's
   allowlist grew from the 6 entries first drafted to **13**. The extra entries
   are `docs/HISTORY.md`, `docs/PROVENANCE.md`,
   `reports/reconciliation/history.csv`, `reports/reconciliation/summary.md`,
   `src/byz/reconcile/report.py`, `tests/contract/test_integration.py`, and
   `tests/curate/test_editions.py`. They name historical tag paths or assert the
   retired trees are gone; they do not send a reader to a deleted working-tree
   path. Every entry has a one-line reason in the test comment and in
   `requirements.md` R8.2 / `validation.md` §5.

6. **Sweep pattern widening.** Added
   `(?<![\w./-])(fetch_official|recover_editions|build_editions|diff_editions)\.py`
   so a retired entry point quoted without its `scripts/` prefix (the B2 class)
   is caught. Mutation check: the test failed with
   `docs/BUILD.md: 'fetch_official.py'` and went green again when the line was
   removed.

7. **Test changes that deviate from the plan's letter.**
   - `tests/curate/test_reproducible.py` `GENERATORS` is now a list of argument
     lists (`[["byz.recover"], ...]`); the unreachable `str(worktree / script)`
     branch is gone.
   - The duplicated tests were collapsed: the `requirements.txt` pin test lives
     only in `tests/curate/test_layout.py`; the "no `sys.path`" test lives only
     in `tests/curate/test_layout.py` (it is a structural layout rule, scanned
     over all of `src/`), and `test_build.py`'s copy was deleted.
   - `test_tei_header_is_package_data` now builds a book and checks the built
     TEI carries `<teiHeader>` and the Robinson/Pierpont statement, instead of
     asserting the literal `Path(__file__).with_name(...)` implementation
     string.
   - Added `test_current_edition_readme_names_the_repository_input_tree`, the
     test the plan's risks section promised.

8. **Spec corrections made with this validation.** `validation.md` §3.2 now
   states that the three-key manifest delta is measured after the move commit;
   §6 no longer claims the *Last changed* column stays pre-move; §7 no longer
   claims `docs/BUILD.md` has Markdown links. `SPECS/TECH.md` §5 now lists the
   frozen `source/` snapshot. `docs/RELEASE-NOTES.md` quotes the real failure
   (`can't open file 'scripts/fetch_official.py' …`). The generated docs got a
   whitespace/reflow fix (`src/byz/contract/report.py`,
   `src/byz/reconcile/report.py`) and `MOVED_PATHS` now carries an explicit
   `code` flag, so the prose row is plain text. `src/byz/beta/converter.py`'s
   docstring is raw, removing a `SyntaxWarning` on `\+`.

9. **Pre-commit worktree limitation and the two-commit convergence.**
   `test_reproducible.py` and `ContractWorktreeTests` only pass after the commit
   plus **two** regeneration commits. In the scratch clone:
   - **A** (the change): contract 2 failures, curate 1, reconciliation OK;
   - **B** (manifests + `files.csv` + `docs/HISTORY.md`): still contract 2,
     curate 1, because B touches `editions/*/manifest.json` and `editions` is in
     `CORPUS_PATHSPECS`, so "Last corpus commit" moves to B;
   - **C** (`docs/HISTORY.md` only): contract 64 OK, curate 181 OK,
     reconciliation 69 OK, and a further regeneration leaves `git status`
     clean.
   The live uncommitted tree shows the same pre-commit failures; §8's two-run
   check is the authoritative pre-commit evidence. Scratch commit hashes for
   the record: A `7dbdd8e`, B `b6834d1`, C `c6a418e` (these are scratch-only;
   the real move commit will be whatever the build agent creates).
