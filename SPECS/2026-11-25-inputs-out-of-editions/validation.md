# Validation - Inputs out of the editions

A change is complete only when every item below is checked against the actual
files, and the command output or observed result is recorded here. The
authoritative checklist is `requirements.md` (`R1`-`R9`) and `plan.md`
(phases 0-6).

The non-negotiable gate is §3: **`rp2005`, `rp2018`, and `rp2018-2023` did not
change**. `rp2005-2019` is regenerated from its 2019 sources by the current
pipeline (requirements Correction 2) and is expected to change: the release's
`{Ν`/`{Β` apparatus codes become `{NA`/`{Byz`, typography is normalised, and
the four blank verses are emitted. If a non-historical CSV/TEI differs by one
byte, or its `artifact_files` entry differs at all, stop and report.

## 1. Preconditions and the before-snapshot

- [ ] Branch is `feature/2026-11-16-edition-recovery-curation`; the base commit
      is recorded (`git rev-parse HEAD`). The spec was written at `7fb28fe`.
- [ ] `git status --porcelain` is empty. If the working tree still has the
      documentation edits that existed when this spec was written, they are
      committed or stashed first; the snapshot is measured against a clean
      baseline.
- [ ] `python3 -c "import beta_code"` succeeds. Record the interpreter and
      `beta-code==1.0.0`.
- [ ] `git tag --list v2.0.3 v3.3.4` prints both;
      `git rev-parse v2.0.3^{commit}` is
      `8ec95671e463030347c2c643358eb56e58235b19`.
- [ ] Byte snapshot of every edition CSV/TEI (**not** `source/`, which is
      deleted):

```bash
find editions -type f \
  \( -path 'editions/*/csv/*' -o -path 'editions/*/tei/*' \) -print0 \
  | sort -z | xargs -0 sha256sum \
  > /tmp/opencode/byz-inputs-editions-before.sha256
wc -l /tmp/opencode/byz-inputs-editions-before.sha256    # 672
```

- [ ] Manifest snapshot, one per edition:

```bash
for id in rp2005 rp2005-2019 rp2018 rp2018-2023; do
  git show "HEAD:editions/$id/manifest.json" \
    > "/tmp/opencode/manifest-$id-before.json"
done
```

- [ ] Diff-report snapshot:

```bash
find reports/diffs -type f -print0 | sort -z | xargs -0 sha256sum \
  > /tmp/opencode/byz-inputs-diffs-before.sha256
```

- [ ] Input/provenance snapshot:

```bash
find data/text data/raw/rp2005 data/raw/rp2018 data/raw/_archives \
     data/provenance -type f -print0 \
  | sort -z | xargs -0 sha256sum \
  > /tmp/opencode/byz-inputs-data-before.sha256
```

- [ ] Inventory: `git ls-files editions | wc -l` → **852**;
      `git ls-files 'editions/*/source/*' | wc -l` → **172**;
      CSV/TEI count → **672**; `git ls-files data/text | wc -l` → **57**.
- [ ] Tag extract for the historical comparison:

```bash
rm -rf /tmp/opencode/v203 && mkdir -p /tmp/opencode/v203
git archive --format=tar v2.0.3 \
  textonly-beta-code parsed \
  csv-unicode/accents/no-variants csv-unicode/accents/with-variants \
  csv-unicode/no-accents tei-xml-unicode/no-accents \
  | tar -x -C /tmp/opencode/v203
find /tmp/opencode/v203 -type f | wc -l    # 170 (57 inputs, 113 outputs)
```

## 2. Red phase

Write the tests from `plan.md` phases 1a, 2a, 3a, 4a, 5a before the production
changes. Confirm each fails **for the intended reason**, not from an import
error or a typo.

- [ ] `tests/curate/test_materialise.py` fails because
      `data/raw/rp2005-2019` does not exist (not `ModuleNotFoundError`).
- [ ] `tests/curate/test_build.py::BuildTests` and
      `tests/curate/test_current_pipeline.py` fail because `build_current` still
      raises `missing CCAT source directory: editions/rp2018-2023/source/CCAT`,
      and `build._input_groups` does not exist.
- [ ] `tests/curate/test_fidelity.py::ManifestIntegrityTests` fails with
      `KeyError: 'inputs'` (the manifests still have `source_files`).
- [ ] `tests/curate/test_verify.py` fails with `ModuleNotFoundError: byz.verify`.
- [ ] `tests/curate/test_layout.py::EditionLayoutTests` fails because
      `editions/<id>/source` still exists.
- [ ] The phase 5 doc tests fail on the missing snapshot section, the missing
      `byz.verify` prose, and the old recover sequence.

Record the exact failure messages here. The red phase cannot be replayed in the
finished tree without reverting; the final proof that the tests still bite is the
worktree failure before the follow-up commits (§9).

## 3. The byte-identity gate

### 3.1 Edition CSV/TEI

- [ ] After the full regeneration (§8), re-run the phase 0 snapshot into
      `/tmp/opencode/byz-inputs-editions-after.sha256` and:

```bash
diff /tmp/opencode/byz-inputs-editions-before.sha256 \
     /tmp/opencode/byz-inputs-editions-after.sha256
```

  Expected: the 477 lines for `rp2005`, `rp2018`, and `rp2018-2023` are
  unchanged; the 195 `rp2005-2019` lines differ. `wc -l` stayed **672**; no
  file was added or removed under `editions/*/{csv,tei}`.

- [ ] `git status --porcelain -- 'editions/rp2005/csv' 'editions/rp2005/tei'
      'editions/rp2018/csv' 'editions/rp2018/tei' 'editions/rp2018-2023/csv'
      'editions/rp2018-2023/tei'` is empty.
- [ ] `git status --porcelain -- 'editions/rp2005-2019/csv'
      'editions/rp2005-2019/tei'` lists the regenerated views.
- [ ] Prove the gate can fail: in a scratch clone, append one byte to
      `editions/rp2018-2023/csv/accented/no-variants/MAT.csv`; `git status`
      names it; restore it byte-for-byte and `git status` is empty again.

### 3.2 Manifest artifact lists

- [ ] Run the comparison for the three unchanged editions:

```bash
python3 - <<'PY'
import json
for edition in ("rp2005", "rp2018", "rp2018-2023"):
    old = json.load(open(f"/tmp/opencode/manifest-{edition}-before.json"))
    new = json.load(open(f"editions/{edition}/manifest.json"))
    assert old["artifact_files"] == new["artifact_files"], edition
    assert "source_files" not in new, edition
    assert new["inputs"], edition
    changed = sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k))
    print(edition, changed)
PY
```

  Expected output, and nothing else:

```
rp2005 ['inputs', 'source_files']
rp2018 ['inputs', 'source_files']
rp2018-2023 ['inputs', 'source_files']
```

  (`source_files` is present only in the old manifest, `inputs` only in the new;
  every other key is identical.)

- [ ] For `rp2005-2019`, assert `source_files` is absent, `inputs` pins the 57
      sources, and `artifact_files` has 195 regenerated entries whose hashes
      match the working tree. `basis` and `note` also change.

- [ ] The old `source_files` hashes are a subset of the new `inputs` hashes for
      the same underlying files:
      - `rp2018-2023`: the 56 `source/CCAT|Strongs` paths map to
        `CCAT|Strongs` under `data/text`; every hash is equal.
      - `rp2005`/`rp2018`: the 29/30 `source/ccat` paths map to the archive
        `.CCT` files; every hash is equal.
      - `rp2005-2019`: the 57 `source/{textonly-beta-code,parsed}` paths map to
        the same paths under `data/raw/rp2005-2019`; every hash is equal. The
        113 released CSV/TEI are not inputs and are not read by `byz.build`.

- [ ] `generated_by` is still `"PYTHONPATH=src python3 -m byz.build"` in all
      four; `tag`/`commit`, `source_commit`/`strongs_commit`, `pdf_sha256`/
      `pdf_size`, `ascii_source`/`preformatted_source` are unchanged.
- [ ] `tests/curate/test_fidelity.py::ManifestIntegrityTests` passes.

### 3.3 No text or input change

- [ ] Re-run the phase 0 data snapshot into
      `/tmp/opencode/byz-inputs-data-after.sha256` and:

```bash
diff /tmp/opencode/byz-inputs-data-before.sha256 \
     /tmp/opencode/byz-inputs-data-after.sha256
```

  The only differences are the edited `data/text/README.md` and additions
  under `data/raw/rp2005-2019/` and
  `data/provenance/rp2005-2019.toml`. No `.TXT`/`.BP5` line appears, and no
  `data/raw/rp2005/`, `data/raw/rp2018/`, `data/raw/_archives/`,
  `rp2005.toml`, or `rp2018.toml` line appears.

- [ ] `git diff --stat -- data/text/CCAT data/text/Strongs data/raw/rp2005
      data/raw/rp2018 data/raw/_archives data/provenance/rp2005.toml
      data/provenance/rp2018.toml` is empty. (The only `data/text` change is
      `data/text/README.md`, a documentation edit.)
- [ ] `sha256sum data/text/CCAT/01_MAT.TXT` is unchanged
      (`0de6c3ca28ea270a8902414b95df2a95d259c092e2cc37a0a39aeabad1373e29`).

### 3.4 Diff reports

- [ ] Re-run the phase 0 diff snapshot and `diff` it against
      `byz-inputs-diffs-before.sha256`; expected: only
      `rp2005--rp2005-2019/**` and `rp2005-2019--rp2018/**` differ.
- [ ] `git diff --stat -- reports/diffs/rp2005--rp2018
      reports/diffs/rp2018--rp2018-2023` is empty.
- [ ] The source-tier counts in the two changed reports are unchanged; only the
      exact Unicode text (apparatus codes, `¶`, apostrophes) changes.

## 4. Historical input gate

The only historical inputs are the 57 `textonly-beta-code`/`parsed` files.
`rp2005-2019` is **regenerated** from them; the 113 released CSV/TEI are
evidence of the 2019 converter's output and are not read by any build path.

- [ ] `data/raw/rp2005-2019/` exists and has exactly **57** files with the
      source-prefix counts **30 / 27**:

```bash
for p in textonly-beta-code parsed; do
  printf '%s ' "$p"
  find "data/raw/rp2005-2019/$p" -type f | wc -l
done
```

- [ ] The tree is byte-identical to the tag at the same paths:

```bash
for p in textonly-beta-code parsed; do
  diff -r "/tmp/opencode/v203/$p" "data/raw/rp2005-2019/$p"
done
```

  Expected: no output, and no `released/` directory under
  `data/raw/rp2005-2019/`.

- [ ] `data/provenance/rp2005-2019.toml` starts with the generated TOML banner,
      has `tag = "v2.0.3"`, `commit = "8ec95671e463030347c2c643358eb56e58235b19"`,
      `extracted = "data/raw/rp2005-2019"`, `generated_by =
      "PYTHONPATH=src python3 -m byz.materialise"`, no `downloaded`, no URL, two
      `[[prefixes]]` blocks, and 57 `[[files]]` blocks sorted by `path`:

```bash
head -10 data/provenance/rp2005-2019.toml
grep -c '^\[\[prefixes\]\]' data/provenance/rp2005-2019.toml  # 2
grep -c '^\[\[files\]\]' data/provenance/rp2005-2019.toml     # 57
grep -n -E 'downloaded|https?://' data/provenance/rp2005-2019.toml  # no output
```

- [ ] The data tree, the manifest, and the provenance do not reintroduce the
      retired `csv-unicode/` or `tei-xml-unicode/` working-tree names:

```bash
git grep -n -E 'csv-unicode/|tei-xml-unicode/' -- data editions \
  ':!data/raw/rp2005-2019/**'
```

  Expected: no output. (The tag-prefix names remain only in the retired-paths
  documentation and the tests that record the tag's history, which the
  retired-path sweep allowlists.)

- [ ] Every `rp2005-2019` view is generated from the sources, not copied:

```bash
grep -L '{NA' editions/rp2005-2019/csv/accented/with-variants/*.csv  # no output
grep -rn '{Ν\|{Β' editions/rp2005-2019/csv/accented/with-variants/  # no output
find editions/rp2005-2019/csv editions/rp2005-2019/tei -type f | wc -l  # 195
```

- [ ] `tests/curate/test_historical_pipeline.py` rebuilds the edition into a
      temporary directory and compares it byte-for-byte; it also forbids any
      `{` + Greek capital, pins `{NA`/`{Byz` samples, checks the four blank
      verses, and compares the accented main text to the release's words after
      normalising `¶`/apostrophes.
- [ ] `python3 -m byz.materialise` is idempotent: run it twice; the second run
      produces no `git status` change and exits 0.
- [ ] A conflicting file is refused: in a temp `dest_root` (the test does this),
      change one byte and assert `SystemExit` naming the path and both hashes;
      the file is not overwritten.

## 5. Manifest and `byz.verify` tests

- [ ] Clean run:

```bash
PYTHONPATH=src python3 -m byz.verify
```

  Expected: four `OK` lines, `rp2005` 56 inputs/141 artifacts, `rp2005-2019`
  57/195, `rp2018` 57/141, `rp2018-2023` 56/195; summary
  `verified 4 editions (226 inputs, 672 artifacts)`; exit 0.

- [ ] Selected editions:
      `PYTHONPATH=src python3 -m byz.verify rp2018-2023` verifies only that
      edition and exits 0.
- [ ] Unknown edition:

```bash
PYTHONPATH=src python3 -m byz.verify rp1999; echo $?
```

  Expected: a message naming `rp1999` and the four valid ids; exit **2**.

- [ ] Corrupted input hash (scratch clone, never the working tree):

```bash
rm -rf /tmp/opencode/byz-verify-scratch
git clone --no-hardlinks . /tmp/opencode/byz-verify-scratch
cd /tmp/opencode/byz-verify-scratch
python3 - <<'PY'
import json
path = "editions/rp2018-2023/manifest.json"
manifest = json.load(open(path))
entry = manifest["inputs"][0]["files"][0]
entry["sha256"] = "0" * 64
with open(path, "w", encoding="utf-8") as handle:
    handle.write(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
PY
PYTHONPATH=src python3 -m byz.verify rp2018-2023; echo $?
```

  Expected: `FAIL rp2018-2023: data/text/CCAT/01_MAT.TXT: sha256 expected
  0000… actual 0de6…`; exit **1**. Restore with `git checkout -- <manifest>`.

- [ ] Corrupted artifact: in the same scratch clone, append a byte to
      `editions/rp2018-2023/csv/accented/no-variants/MAT.csv`; verify names that
      path with the expected/actual hash and exits 1; restore it.
- [ ] Missing artifact: delete a committed CSV in the scratch clone; verify says
      `missing` and names the path; restore it.
- [ ] Extra artifact: add `editions/rp2018-2023/csv/extra.csv`; verify says
      `unexpected` and names it; remove it.
- [ ] Extra input: add `data/text/CCAT/99_ZZZ.TXT` in the scratch clone; verify
      reports it as unexpected because it matches `CCAT/*.TXT`; remove it.
- [ ] Legacy manifest: add `"source_files": []` to a manifest; verify rejects it
      as invalid; restore.
- [ ] Path safety: change a `root` to `/etc` or `../data`; verify rejects it
      before hashing; restore.
- [ ] Downloaded edition:

```bash
rm -rf /tmp/opencode/rp2018-download
cp -r editions/rp2018 /tmp/opencode/rp2018-download
PYTHONPATH=src python3 -m byz.verify --edition-dir /tmp/opencode/rp2018-download
```

  Expected: `OK rp2018: 141 artifacts (external edition directory; inputs
  skipped)`; exit 0. Corrupt one CSV in the copy; exit 1.
- [ ] No writes: hash the scratch tree before and after a verify run; no change.
- [ ] `tests/curate/test_verify.py` covers all of the above in temp trees and is
      green.

## 6. Layout gates

- [ ] No snapshot exists:

```bash
test ! -e editions/rp2005/source
test ! -e editions/rp2005-2019/source
test ! -e editions/rp2018/source
test ! -e editions/rp2018-2023/source
git ls-files 'editions/*/source/*'    # no output
```

- [ ] Each edition has exactly four entries:

```bash
for d in editions/*/; do
  printf '%s: ' "$d"
  find "$d" -mindepth 1 -maxdepth 1 -printf '%f ' | sort
  echo
done
```

  Expected: `README.md csv manifest.json tei` for each.

- [ ] `editions/` is 680 tracked files: `git ls-files editions | wc -l`.
- [ ] `grep -R -n -E '"/source"|/ "source"|SNAPSHOT_DIR' src/byz` prints nothing.
- [ ] `grep -R -n 'editions/.*/source' src/byz tests --include='*.py'` prints
      only the tests/docs that assert the snapshot is gone and the docs mapping
      constant.
- [ ] `PYTHONPATH=src python3 -m byz.build` does not recreate `source/`;
      `git status --porcelain -- editions` shows only manifests/READMEs.
- [ ] `tests/curate/test_layout.py` is green, including
      `EditionLayoutTests` and the retired-layout sweep.
- [ ] `SPECS/TECH.md` has no `editions/<edition>/source`:

```bash
grep -n 'editions/<edition>/source' SPECS/TECH.md    # no output
```

- [ ] No public doc sends a reader to a snapshot or to "recover before build":

```bash
git grep -n -E 'editions/[a-z0-9-]+/source' \
  -- ':!SPECS' ':!tests' ':!src/byz/curate/docs.py' ':!docs/EDITIONS.md'
```

  Expected: no output except the historical mapping table and the tests that
  assert the snapshot is gone (all allowlisted).

## 7. Generated documentation

- [ ] `docs/EDITIONS.md` contains
      `## Where the edition snapshots went (2026-11-25)`, every
      `docs.SNAPSHOT_MOVES` row, the released-artifact tag-to-edition mapping
      table, and the sentence that an edition is outputs only and `byz.verify`
      checks it against `data/`.
- [ ] `docs/EDITIONS.md`'s "Rebuilding the curated editions" block contains
      `byz.build`, `byz.diff`, and `byz.verify`, and no recovery command.
- [ ] `docs/EDITIONS.md` still contains the 2026-11-21 moved-paths table and the
      corrected note that `artifact_files` is unchanged while `source_files`
      became `inputs`.
- [ ] `README.md` is byte-identical to the template render:

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
- [ ] `README.md`'s generated-files table has no
      `editions/<edition>/source/` row and has the
      `data/raw/rp2005-2019/` / `data/provenance/rp2005-2019.toml` row.
- [ ] `README.md`'s sequence has `byz.verify` and no recovery step in the
      normal build; the prose explains the materialisation exception.
- [ ] `docs/BUILD.md` has "Verifying the editions", the manifest `inputs`
      schema, `--edition-dir`, the exit codes, and no "recover then build".
- [ ] `data/text/README.md` says `data/text/` is an input, editions are
      outputs, and `manifest.json` pins the inputs by path and hash; its links
      still resolve.
- [ ] Each `editions/<id>/README.md` has no `source/` layout row and no
      "downloaded and verified on its own" sentence; the `rp2018-2023` README
      no longer says the snapshot duplicates `data/text/`.
- [ ] `docs/DATA_CONTRACT.md` says the derivatives come from the committed
      `data/` inputs; no `recover.recover_all copies ... source snapshot` text.
- [ ] `docs/PROVENANCE.md` points at `data/raw/rp2005-2019/` and
      `data/provenance/rp2005-2019.toml`.
- [ ] `docs/contract/*.json` and `reports/baseline/derivations.csv` are
      regenerated; `reports/baseline/files.csv` changes only for the three
      documentation rows it inventories (`README.md`, `data/text/README.md`,
      `docs/BUILD.md`). Record the row delta; no snapshot or `data/raw/` row
      appears.
- [ ] `tests/curate/test_editions.py::PdfLinkTests` passes with the updated
      `_user_docs()`.
- [ ] `.opencode/**` and `SPECS/TECH.md` describe `byz.build` reading `data/`,
      `byz.verify` checking, and `byz.materialise` only restoring the historical
      inputs. No agent file says to run a recovery step before the build.

## 8. Regeneration and determinism

Run from the repository root, in this order:

```bash
PYTHONPATH=src python3 -m byz.fetch --verify
PYTHONPATH=src python3 -m byz.build
PYTHONPATH=src python3 -m byz.diff
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m byz.reconcile
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m byz.verify
```

- [ ] `byz.fetch --verify` exits 0 with no network access and writes nothing
      (`git diff -- data/provenance/rp2005.toml data/provenance/rp2018.toml`
      empty).
- [ ] `byz.build` prints `built 4 editions` and writes the manifests, edition
      READMEs, `docs/EDITIONS.md`, and the root README.
- [ ] `byz.diff` writes the four reports; `reports/diffs/**` is unchanged
      (§3.4).
- [ ] `byz.contract` then `byz.reconcile` then `byz.contract` leaves
      `docs/HISTORY.md` with one banner, one `# Internal history map`, and one
      `<!-- cycle2:begin -->` block.
- [ ] `byz.verify` exits 0 with `226 inputs, 672 artifacts`.
- [ ] Snapshot run 1:

```bash
find README.md docs reports editions data/provenance data/raw/rp2005-2019 \
  -type f -print0 | sort -z | xargs -0 sha256sum \
  > /tmp/opencode/byz-inputs-run1.sha256
```

- [ ] Run the whole sequence a second time; snapshot run 2 into
      `byz-inputs-run2.sha256`; `diff` the two files is silent. `git status
      --porcelain` is identical after run 1 and run 2.
- [ ] No `editions/.rp*` or `editions/.*.staging` directory remains:

```bash
ls -a editions
```

- [ ] No wall-clock timestamp, hostname, or absolute path in generated output:

```bash
git grep -n -E '/home/|localhost|/tmp/opencode' -- README.md docs reports editions data
```

  Expected: no output. (Git commit dates in `docs/HISTORY.md` and commit hashes
  in the manifests are stable history, not run metadata.)

## 9. The suites

```bash
PYTHONPATH=src python3 -m unittest discover -s tests/contract
PYTHONPATH=src python3 -m unittest discover -s tests/curate
PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation
```

- [ ] All three pass with 0 failures and 0 unplanned skips. Record the test
      counts (the 2026-11-21 baseline was contract 64, curate 181,
      reconciliation 69; this change adds tests).
- [ ] `tests/curate/test_reproducible.py` passes after the change commit and the
      follow-up regeneration commits; before the change it fails for the known
      reason (it builds a worktree at `HEAD`). The §8 two-run check is the
      authoritative pre-commit evidence.
- [ ] `tests/contract` `ContractWorktreeTests` pass after the follow-up
      regeneration commits. Because the change touches
      `editions/*/manifest.json` and `editions` is in `CORPUS_PATHSPECS`, the
      first follow-up moves the recorded "Last corpus commit"; a second
      regeneration commit records it and converges. Record the actual number of
      follow-ups and the commit hashes.
- [ ] No test touches the network; no test writes to the repository. The
      materialise and verify tests use temporary roots.
- [ ] A shallow clone still cannot run the worktree tests; that is documented
      behaviour, not a regression.

Record the convergence table:

| Commit | Contents | `tests/contract` | `tests/curate` | `tests/reconciliation` |
| --- | --- | --- | --- | --- |
| A (the change) | snapshots deleted, data added, code/tests/docs |  |  |  |
| B (first follow-up) | manifests, baseline, `docs/HISTORY.md` |  |  |  |
| C (second follow-up) | `docs/HISTORY.md` only |  |  |  |

## 10. Manual inspection

- [ ] Open `editions/rp2018-2023/manifest.json` and confirm `inputs[0].root` is
      `data/text`, `include` is `CCAT/*.TXT` and `Strongs/*.BP5`, and every
      `path` starts with `CCAT/` or `Strongs/`; there is no `source_files` key.
- [ ] Open `editions/rp2005-2019/manifest.json` and confirm `inputs[0].root` is
      `data/raw/rp2005-2019`, the two `include` globs are present, and the
      57 `files` paths are tag-relative. Confirm `tag`/`commit`.
- [ ] Open `editions/rp2005/manifest.json` and confirm the two input groups
      (`.CCT` and `_Byz.txt`) point into `data/raw/rp2005/`; `artifact_files`
      still uses `csv/...`/`tei/...`.
- [ ] Run `PYTHONPATH=src python3 -m byz.verify` clean and read the report. Then
      run the scratch-clone corrupted-input check in §5 and read the failure.
- [ ] Read `README.md` start to finish: no "self-contained" edition claim, the
      sequence is `fetch`, `build`, `diff`, `contract`, `reconcile`, `verify`,
      and the `byz.materialise` exception is explained.
- [ ] Read `docs/BUILD.md` as a first-time contributor: install, the input tree
      (`data/raw/rp2005-2019/` included), the pipeline, the verify section, the
      report order, the tests.
- [ ] Read `docs/EDITIONS.md`'s new snapshot section: each retired path maps to
      a `data/` home, and the self-verification tradeoff is stated.
- [ ] Read `data/text/README.md`: it distinguishes input from output and points
      at `manifest.json`/`byz.verify`.
- [ ] Read `SPECS/TECH.md` §5 and §8: the layout block matches the physical
      tree, and the artifact section says editions contain only outputs.
- [ ] Read one `.opencode` agent file and `read-conventions.md`: the commands
      run as written, with no "recover before build".

## 11. Definition of done and deviations log

Definition of done:

- [x] `editions/<edition>/source/` is gone for all four; each edition has only
      `csv/`, `tei/`, `manifest.json`, `README.md`; `editions/` is 680 tracked
      files.
- [x] `data/raw/rp2005-2019/` has 57 source files matching `git archive
      v2.0.3`; `data/provenance/rp2005-2019.toml` records the tag, commit, and
      57 hashes/sizes with no timestamp. `rp2005-2019` is regenerated from
      those files; no release artifact is copied.
- [x] Every manifest has `inputs` and no `source_files`; every root is under
      `data/`; every input/artifact hash and set is verified.
- [x] `byz.verify` exits 0 clean, 1 on corrupted input/artifact, 2 on usage,
      and supports `--edition-dir`.
- [x] The 477 CSV/TEI files and `artifact_files` entries of `rp2005`,
      `rp2018`, and `rp2018-2023` are unchanged; `rp2005-2019` is regenerated
      (672 files before and after, 195 regenerated). No existing `.TXT`/`.BP5`,
      archive, PDF, or provenance file changed (the only existing data file
      edited is `data/text/README.md`). The two diff-report pairs that include
      `rp2005-2019` changed; the other two are unchanged.
- [x] No `rp2005-2019` with-variants file contains `{Ν`/`{Β` (or any `{` +
      Greek capital), and the view carries `{NA`/`{Byz`; the accented main text
      matches the release's words after normalising `¶`/apostrophes.
- [x] The sequence runs twice with no diff; the three suites pass; the
      follow-up commits land and converge. **See 12.2-12.4:** the two-run
      determinism passes; the retired-path allowlist fix is in place, and the
      committed copy converges after one regeneration follow-up with curate
      247/247.
- [x] `README.md`, `docs/EDITIONS.md`, `docs/BUILD.md`,
      `docs/DATA_CONTRACT.md`, `docs/PROVENANCE.md`, `data/text/README.md`,
      `editions/*/README.md`, `SPECS/TECH.md`, and `.opencode/**` describe the
      new model.
- [x] Every deviation from `plan.md` is recorded below with its reason.
      The verifier findings are recorded in 12.3 and deviation 15.

Deviations log:

1. **Baseline.** The implementation ran from `b5b8ba5` with a clean tracked
   tree (the only untracked path was this spec folder), so the snapshots were
   taken without stashing anything.
2. **Historical input count (corrected 2026-11-25).** The first draft proposed
   170 files. The maintainer corrected D2: only the 57
   `textonly-beta-code`/`parsed` files are inputs under `data/`. The 113
   released `v2.0.3` CSV/TEI are neither inputs nor published outputs here;
   Correction 2 regenerates every view from the 57 sources.
3. **`byz.recover` role (corrected 2026-11-25).** D5 was amended: the command
   is renamed to `byz.materialise`, and the old `byz.recover` entry point and
   module are deleted with no alias.
4. **Manifest metadata.** For `rp2005`, `rp2018`, and `rp2018-2023` the only
   changed top-level keys are `source_files` (removed) and `inputs` (added);
   every `artifact_files` entry and edition-specific key is unchanged. For
   `rp2005-2019`, `inputs` is added, `source_files` is removed, `basis` and
   `note` are rewritten, and the 195 artifact hashes are regenerated.
   Input counts are `rp2005` 56, `rp2005-2019` 57, `rp2018` 57,
   `rp2018-2023` 56 (226 total); artifacts stay 672.
5. **Report churn.** `reports/baseline/files.csv` changed only the three
   documentation rows (`README.md`, `data/text/README.md`, `docs/BUILD.md`).
   `reports/baseline/derivations.csv` changed only the `evidence` strings for
   the `ccat` and `strongs` derivations. `docs/PROVENANCE.md` and
   `reports/reconciliation/summary.md` gained the historical-input sentence.
   `docs/HISTORY.md` is unchanged in the working tree, though it is expected to
   move once the change is committed because `editions` is in
   `CORPUS_PATHSPECS`. (The changed diff reports are recorded in deviation 10.)
6. **Test changes.** `tests/curate/test_recover.py` was replaced by
   `tests/curate/test_materialise.py`; the snapshot tests were deleted and
   materialise safety/idempotency/conflict coverage was added. Snapshot
   assertions were removed from `test_current_pipeline.py`, `test_integration.py`,
   `test_fidelity.py`, `test_build.py`, and `test_editions.py`; manifest tests
   now read `inputs`. `test_layout.py` gained outputs-only, no-source, and
   no-manifest-under-`editions/` checks. `test_verify.py` is new.
7. **Follow-up commits.** Not run: this implementation leaves the branch
   uncommitted. `tests/curate/test_reproducible.py` therefore fails at HEAD
   because its worktree runs the old `src/` and has no `byz.verify`; it will
   pass after the change commit. `tests/contract.ContractWorktreeTests` will
   need the usual regeneration follow-up because the change touches `editions`
   (a `CORPUS_PATHSPECS` entry).
8. **Historical regeneration (Correction 2, 2026-11-25).** `build_historical`
   was implemented to generate every view from `data/raw/rp2005-2019/`, as the
   maintainer's correction requires. All tag access was removed from
   `byz.build`: `_git_archive`, the artifact-prefix constants,
   `_copy_historical_artifacts`, `_correct_historical_apparatus_literals`, the
   MAR 16:8 post-correction, and the `git rev-parse` commit lookup are gone.
   The registry now carries the tag's commit, and `byz.materialise` imports it,
   so tag `v2.0.3` is read only by the materialiser. `rp2005-2019` now matches
   the other editions' blank-verse behaviour (7972/7957 rows, empty `<ab/>`)
   and has no Greek code initials.
9. **Segmentation reference (Correction 2).** The `.UB5` parenthetical-verse
   routing previously compared against the released `csv/unaccented`. It now
   derives a reference from the accented view generated from the same `.CCT`:
   lower-case, accent-free, punctuation-free words. That decides all nine
   parenthetical refs correctly and reproduces the release's segmentation. The
   regenerated `csv/unaccented` and `csv/strongs/no-parsing` are now the same
   bytes, as in `rp2018-2023`.
10. **Diff report churn (Correction 2).** `reports/diffs/rp2005--rp2005-2019/**`
    and `reports/diffs/rp2005-2019--rp2018/**` change because the historical
    edition's exact text changed; `rp2005--rp2018` and
    `rp2018--rp2018-2023` are byte-identical. The source-tier counts are
    unchanged. Three integration samples that depended on the removed `¶`-only
    differences were replaced by stronger checks: `text.diff` must reproduce
    the exact `text_left`/`text_right` for every block.
11. **Test additions (Correction 2).**
    `tests/curate/test_historical_pipeline.py` is new. It rebuilds the whole
    edition into a temp directory and compares it byte-for-byte, forbids any
    `{` + Greek capital, pins `{NA`/`{Byz` samples, checks the four blank verses,
    pins the 57 inputs, and compares the accented main text to the `v2.0.3`
    release's words after normalising `¶`/apostrophes (zero differences).
    `test_fidelity.py::ApparatusLiteralFidelityTests` now verifies the
    historical literal comes from regeneration, not a post-correction.
12. **Final runs.** The full sequence ran twice with no tracked diff on the
    second run; the three suites report contract 64, reconciliation 80, and
    curate 245 in the working tree, with the single pre-commit
    `test_reproducible` error expected from the one-commit lag. After the
    verifier fixes, the committed throwaway copy is contract 64, reconciliation
    80, curate 247/247 (see 12.2).
13. **Bracketed final sigma (observation, no behaviour change).** The shared
    converter has a pre-existing bracketed-final-sigma wart. It affects exactly
    five verses identically in all four editions (2PE 2:6, ACT 13:14,
    JOH 19:35, JOH 20:31, LUK 11:10). The `v2.0.3` release had these right, so
    this regeneration follows the current pipeline here rather than the release;
    fixing the converter is a separate change.
14. **Unaccented word spacing (observation, no behaviour change).** The
    regenerated `csv/unaccented` moves eight verses closer to the source on word
    spacing (for example 1CO 7:5 `μη τι` becomes `μητι`), consistent with
    `rp2018-2023`. `docs/EDITIONS.md` now states that word spacing in the
    unaccented view follows the parsed source.

15. **Verifier findings (2026-11-25), fixed.** The verifier's review found
    seven issues, all fixed in this follow-up: the retired-path sweep allowlist
    now names `tests/curate/test_historical_pipeline.py`; `docs/EDITIONS.md`
    renders the released-artifact mapping table
    (`docs.RELEASED_ARTIFACT_MOVES`); the "only command that reads `v2.0.3`"
    claim is scoped to the tag's files as build inputs; `byz.verify` prints
    repo-relative manifest paths; `reports/diffs/README.md` no longer says
    "recovered"; and Correction 2 states the typography-only count as 1,920
    with its measurement basis. The `SPECS/ROADMAP.md` edit is recorded as a
    deliberate deviation in item 16. Details in 12.3.

16. **`SPECS/ROADMAP.md` edit (deliberate deviation).** The roadmap's Cycle 3
    follow-up gained a `(superseded 2026-11-25)` parenthetical after its stale
    claim that the historical views stay byte-identical to `v2.0.3`. The plan
    otherwise edits only this spec folder and `SPECS/TECH.md`; the parenthetical
    keeps a stale sentence honest and is recorded here rather than reverted.

## 12. Verification record (verifier, 2026-11-25)

Verified against the uncommitted working tree at
`feature/2026-11-16-edition-recovery-curation`, HEAD `b5b8ba5`, from the
repository root with Python 3.12.3
(`/tmp/opencode/venv-byz/bin/python3`) and `beta-code==1.0.0`.

### 12.1 Results by requirement

| Check | Result |
| --- | --- |
| No `editions/*/source`; each edition has exactly `README.md`, `csv`, `manifest.json`, `tei`; `git ls-files editions` = 680; `git ls-files 'editions/*/source/*'` empty | pass |
| No manifest input root under `editions/`; all four roots under `data/`; `byz.verify` rejects a root under `editions/`, an absolute root, a `../` root, and a `../` file path | pass (tested in a throwaway copy) |
| `byz.build` reads no tag content: instrumented run shows only `git tag --list` (release ranges) and `git log -1` (commit metadata), no `git archive`, no `git show`, no `v2.0.3` extraction | pass for tag content; see the wording finding in 12.3 |
| Byte identity: `rp2005`, `rp2018`, `rp2018-2023` CSV/TEI are byte-identical to HEAD (141 + 141 + 195 = 477 files); no file added or removed; 672 CSV/TEI total (448 CSV + 224 TEI) | pass |
| `rp2005-2019` regeneration: 195 files, 118 changed, 77 unchanged; 29/29/27/27/27 CSV views; 28 + 28 TEI files; `csv/unaccented` == `csv/strongs/no-parsing` byte-for-byte (27 books) | pass |
| Book guards: `build_historical` checks the 29 `.CCT` files against `CANONICAL_BOOKS + SECTION_ABBRS` (including `PA`/`ACT24`) and the 27 `.UB5` files against `CANONICAL_BOOKS`; `_historical_source_map` rejects an unknown or duplicate book | pass |
| Apparatus codes: 0 occurrences of `{` + Greek capital in the 29 with-variants files; `{NA` 6,816 and `{Byz` 666, exactly matching the old `{Ν` 6,816 and `{Β` 666 (7,482 total) | pass |
| Accented main text: 0 letter/word differences against the release after removing `¶` and normalising `’`/`‘` to `'`; 1,920 verses differ only in typography (measured with `¶` + apostrophe normalisation; see 12.3) | pass on the substantive criterion |
| Blank verses LUK 17:36, ACT 8:37, ACT 15:34, ACT 24:7: empty records in all five CSV views and `<ab n="..."/>` in both TEI views | pass |
| MAR 16:8: with-variants carries `{NA` literals rendered from `MR.CCT` (`{N ... }`), no-variants has the plain main text | pass |
| Manifest `artifact_files` for the three unchanged editions equals HEAD exactly; the only changed top-level keys are `source_files` (removed) and `inputs` (added); old `source_files` hashes are a subset of the new `inputs` hashes in all four editions | pass |
| `byz.verify` clean: `226 inputs, 672 artifacts`, exit 0; corrupted input hash, corrupted artifact, missing artifact, extra artifact, extra input, legacy `source_files`, path traversal all exit 1 with the path and expected/actual hash; unknown edition and `--edition-dir` + ids exit 2; `--edition-dir` reports `inputs skipped` and exits 0/1 | pass |
| `byz.materialise`: 57 files (30 `.CCT` + 27 `.UB5`), byte-identical to `git archive v2.0.3`; provenance has 2 prefix blocks and 57 sorted file blocks, tag, commit, no timestamp/URL; second run writes no byte; conflicting file and stray file refused without overwriting | pass |
| Full sequence twice (`materialise`, `fetch --verify`, `fetch`, `build`, `diff`, `contract`, `reconcile`, `verify`): 799-file snapshot and `git status` identical; no staging/`.old` directory; no absolute path, hostname, or timestamp in generated output | pass |
| Diff reports: 25 files before and after; only `rp2005--rp2005-2019` (4 files) and `rp2005-2019--rp2018` (3 files) changed; source-tier counts 54 and 3 are unchanged | pass |
| Inputs: `data/text/CCAT`, `data/text/Strongs`, `data/raw/rp2005`, `data/raw/rp2018`, `data/raw/_archives`, and the two official provenance TOMLs are unchanged; the only `data/text` edit is `README.md`; `01_MAT.TXT` keeps `0de6c3ca…` | pass |
| CSV parse (448 files), TEI well-formed (224 files), chapter/verse keys unique and sorted | pass |
| Spec corrections recorded: 57-file materialisation (Correction + D2/D7 + deviation 2) and regeneration-not-recovery (Correction 2 + D6 + deviations 8-11) | pass |

### 12.2 Suites

Working tree before the commit:

- `tests/contract`: 64 tests, OK.
- `tests/reconciliation`: 80 tests, OK.
- `tests/curate`: 245 tests run, 1 error:
  `test_reproducible.RegenerationDeterminismTests.setUpClass` fails with
  `No module named byz.verify` in the worktree at HEAD. This is the known
  one-commit lag, not a change defect.

After committing in a throwaway copy (change commit A, then one regeneration
commit B):

- `tests/contract`: 64, OK.
- `tests/reconciliation`: 80, OK.
- `tests/curate`: 247, OK, including
  `test_current_pipeline.LegacyTreesAreGoneTests` and
  `test_reproducible` 2/2 after B.

### 12.3 Verifier findings and their fixes (2026-11-25)

**Blocking - the retired-path sweep failed after the commit (fixed).**
`tests/curate/test_current_pipeline.py::LegacyTreesAreGoneTests`
`.test_no_tracked_file_reads_a_retired_path` passed now only because
`tests/curate/test_historical_pipeline.py` was untracked. Once the change was
committed the sweep read it and reported it as an offender: the new test
contains the tag selector `csv-unicode/accents/no-variants` and asserts the
retired `csv-unicode`/`tei-xml-unicode` names are gone. Reproduced in a
throwaway commit. The fix adds `tests/curate/test_historical_pipeline.py` to the
sweep's `allowed` set with a one-line reason; with that line the curate suite is
247/247 green in the committed copy. (`test_materialise.py`, the file named in
R2.7, contains neither retired name, so allowlisting it would not fix this.)

**Documentation - the R8.4 second mapping table was absent (fixed).**
`docs/EDITIONS.md`'s "Where the edition snapshots went" section had the
`SNAPSHOT_MOVES` table but not the requested second table mapping the `v2.0.3`
released prefixes (`csv-unicode/accents/no-variants`,
`csv-unicode/accents/with-variants`, `csv-unicode/no-accents`,
`tei-xml-unicode/no-accents`) to `editions/rp2005-2019/{csv,tei}/`. The
existing "Where the old working-tree paths went" table maps the 2026-11-19
working-tree paths to `rp2018-2023`, not the tag prefixes to the historical
edition. `src/byz/curate/docs.py` now holds `RELEASED_ARTIFACT_MOVES` and renders
the table, plus the sentence that those views are regenerated from the same
tag's sources and are therefore not byte-identical to the release.

**Documentation - "only command that reads `v2.0.3`" was too strong (fixed).**
`README.md`, `docs/EDITIONS.md`, `docs/BUILD.md`, `SPECS/TECH.md`, and the
`test_historical_pipeline.py` docstring said `byz.materialise` is the only
command that reads `v2.0.3` / every tag read belongs to it. That is false:
`byz.reconcile` reads `v2.0.3` with `git show` for its historical evidence,
and `byz.build` calls `git tag --list` to compute the release ranges (so a
tagless checkout cannot build). The prose now scopes the claim to the tag's
files as build inputs: only `byz.materialise` extracts them into `data/`, and
the build reads `data/` only.

**Minor - `byz.verify` manifest-load errors printed an absolute path (fixed).**
In repo mode a `source_files`/parse/shape error reported
`/home/.../editions/<id>/manifest.json`. `load_manifest` now takes a
`display_path`, and repository mode passes `editions/<id>/manifest.json`, so the
error is repo-relative as R5.3 requires.

**Minor - stale "recovered" wording (fixed).**
`reports/diffs/README.md` said "the recovered historical `textonly-beta-code`"
(rendered by `src/byz/curate/diff.py`); it now says "the historical
`textonly-beta-code` sources", and the report was regenerated.

**Minor - spec evidence count (resolved).**
The typography-only count is 1,920 verses, measured over the 29 accented
no-variants files after removing `¶` and normalising curly apostrophes to `'`;
letter/word differences are 0. Correction 2 now states that number and its
measurement basis. The 7,482 malformed-marker count reproduced exactly, and the
substantive acceptance criterion (zero word differences) holds.

**Minor - ROADMAP edited (recorded).**
`SPECS/ROADMAP.md` gained a one-word `(superseded 2026-11-25)` parenthetical,
although the sequencing says to edit only this spec and `SPECS/TECH.md`. The
edit keeps a stale byte-identity sentence honest; it is recorded as a deliberate
deviation in item 16 rather than reverted.


### 12.4 Post-commit regeneration sequence

The index currently has the 172 snapshot deletions staged and everything else
unstaged, so the change commit must start with `git add -A`.

```bash
git add -A
git commit -m "Take the edition inputs out of editions/"

# follow-up B (expected; verified in a throwaway copy)
PYTHONPATH=src python3 -m byz.build
PYTHONPATH=src python3 -m byz.diff
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m byz.reconcile
PYTHONPATH=src python3 -m byz.contract   # refresh baseline against the reconciled HISTORY
PYTHONPATH=src python3 -m byz.verify
git add -A
git commit -m "Regenerate the history map and baseline after the change"

# confirm convergence: run the same six commands again; `git status` must be
# empty. For this change one follow-up was enough (the throwaway copy was clean
# after B). The 2026-11-21 move needed two because its first follow-up changed
# a manifest under `editions/`, which is in CORPUS_PATHSPECS; this change's
# follow-up touches only docs/HISTORY.md and reports/baseline/files.csv.
# If a second follow-up diff appears, commit it the same way.

PYTHONPATH=src python3 -m unittest discover -s tests/contract
PYTHONPATH=src python3 -m unittest discover -s tests/curate
PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation
```

`byz.materialise` and `byz.fetch` are no-ops at this point; they stay out of the
follow-up sequence.
