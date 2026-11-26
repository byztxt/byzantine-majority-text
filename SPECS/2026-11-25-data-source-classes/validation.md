# Validation - The two source classes

A change is complete only when every item below is checked against the actual
files, and the command output or observed result is recorded in §12. The
authoritative checklist is `requirements.md` (`R1`-`R10`); `plan.md` phases 0-6
are the task order.

The non-negotiable gate is §3: **no edition byte changed**. All 672 files under
`editions/*/{csv,tei}` must be byte identical, and every manifest's
`artifact_files` entry must keep its `path`, `sha256`, and `size`. If a single
file differs, stop and report; the cause is a wrong input path, a reader, or a
book map, never an edition to adjust.

## 1. Preconditions and the before-snapshot

- [ ] The superseded uncommitted work is gone and the tree is clean. At the
      time of writing `git status --porcelain` showed `data/text/README.md`,
      `reports/baseline/files.csv`, `src/byz/contract/inventory.py`,
      `src/byz/generated.py`, and `tests/curate/test_layout.py` modified plus
      untracked `data/README.md`. They are reverted (`rm` for the untracked
      draft after copying it to `/tmp/opencode/data-README-draft.md`) before the
      snapshot.
- [ ] Branch is `feature/2026-11-16-edition-recovery-curation`; the base commit
      is recorded (the spec was written at `a811b8c`), Python is 3.12.3, and
      `python3 -c "import beta_code"` succeeds (`beta-code==1.0.0`).
- [ ] `git tag --list v2.0.3 v3.3.4` prints both;
      `git rev-parse v2.0.3^{commit}` is
      `8ec95671e463030347c2c643358eb56e58235b19`.
- [ ] Edition CSV/TEI snapshot (672 files):

```bash
find editions -type f \
  \( -path 'editions/*/csv/*' -o -path 'editions/*/tei/*' \) -print0 \
  | sort -z | xargs -0 sha256sum \
  > /tmp/opencode/byz-classes-editions-before.sha256
wc -l /tmp/opencode/byz-classes-editions-before.sha256    # 672
```

- [ ] Manifest snapshot:

```bash
for id in rp2005 rp2005-2019 rp2018 rp2018-2023; do
  git show "HEAD:editions/$id/manifest.json" \
    > "/tmp/opencode/classes-manifest-$id-before.json"
done
```

- [ ] Docs/reports and input snapshots:

```bash
find reports docs -type f -print0 | sort -z | xargs -0 sha256sum \
  > /tmp/opencode/byz-classes-docs-before.sha256
find data -type f -print0 | sort -z | xargs -0 sha256sum \
  > /tmp/opencode/byz-classes-data-before.sha256
```

- [ ] Inventory: `git ls-files data | wc -l` -> **293**,
      `git ls-files editions | wc -l` -> **680**,
      `git ls-files | wc -l` -> **1154**.
- [ ] Per-directory counts: `data/text/CCAT` 29, `data/text/Strongs` 27,
      `rp2005` 29/27/27/1, `rp2018` 30/27/27/1, `_archives` 6,
      `rp2005-2019` 30/27.
- [ ] Archive extracts for the equality check:

```bash
rm -rf /tmp/opencode/classes-zips && mkdir -p /tmp/opencode/classes-zips
python3 - <<'PY'
import pathlib, zipfile
for archive in sorted(pathlib.Path("data/raw/_archives").glob("*/*")):
    target = pathlib.Path("/tmp/opencode/classes-zips") / archive.stem
    target.mkdir(parents=True, exist_ok=True)
    zipfile.ZipFile(archive).extractall(target)
PY
find /tmp/opencode/classes-zips -type f | wc -l     # 167 (29+27+27+30+27+27)
```

## 2. Red phase

Write the tests from `plan.md` phases 1a, 2a, 3a, 4a, and 5a before the
production change, and confirm each fails **for the intended reason**.

- [ ] `tests/curate/test_layout.py::InputTreeTests` fails because
      `data/raw/repo/rp2018-2023/ccat` and `data/raw/print` do not exist (not an
      import error).
- [ ] `tests/curate/test_input_provenance.py` fails with
      `FileNotFoundError: data/provenance/rp2018-2023.toml`.
- [ ] `tests/curate/test_data_docs.py` fails with
      `FileNotFoundError: data/README.md`.
- [ ] `tests/curate/test_generated.py` classification fails and names the eight
      unlisted `data/**/README.md` files.
- [ ] `tests/curate/test_editions.py::DocsTests` fails on the missing
      `## Where the inputs moved into the print and repo classes (2026-11-25)`
      section and the missing `INPUT_CLASS_MOVES` rows.
- [ ] `tests/reconciliation/test_fetch.py` fails on the extraction directory
      name, and `tests/contract/test_integration.py` on the dataset names.

Record the exact failure messages in §12. The red phase cannot be replayed in
the finished tree; the worktree failure before the follow-up commits (§9) is the
final proof that the tests still bite.

## 3. Gates

### 3.1 The artifact byte-identity gate

- [ ] After the full regeneration (§8), re-run the phase 0 snapshot into
      `/tmp/opencode/byz-classes-editions-after.sha256` and diff:

```bash
diff /tmp/opencode/byz-classes-editions-before.sha256 \
     /tmp/opencode/byz-classes-editions-after.sha256
wc -l /tmp/opencode/byz-classes-editions-after.sha256    # 672
```

  Expected: **no output**. No file added, removed, or changed under
  `editions/*/{csv,tei}`, including `rp2005-2019`.
- [ ] `git status --porcelain -- 'editions/*/csv' 'editions/*/tei'` is empty.
- [ ] Prove the gate can fail: in a scratch clone, append one byte to
      `editions/rp2018-2023/csv/accented/no-variants/MAT.csv`; the snapshot diff
      names it; restore it and the diff is silent again.

### 3.2 The manifest gate

```bash
python3 - <<'PY'
import json
for edition in ("rp2005", "rp2005-2019", "rp2018", "rp2018-2023"):
    old = json.load(open(f"/tmp/opencode/classes-manifest-{edition}-before.json"))
    new = json.load(open(f"editions/{edition}/manifest.json"))
    assert old["artifact_files"] == new["artifact_files"], edition
    changed = sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k))
    print(edition, changed)
    for group_old, group_new in zip(old["inputs"], new["inputs"]):
        assert [f["sha256"] for f in group_old["files"]] \
            == [f["sha256"] for f in group_new["files"]], edition
        old_paths = [f["path"] for f in group_old["files"]]
        new_paths = [f["path"] for f in group_new["files"]]
        if edition == "rp2018-2023":
            # The group root is now the snapshot directory, so the first path
            # segment changes case (`CCAT/` -> `ccat/`, `Strongs/` ->
            # `strongs/`); the file set is unchanged.
            assert [p.lower() for p in old_paths] \
                == [p.lower() for p in new_paths], edition
        else:
            assert old_paths == new_paths, edition
        print("  root", group_old["root"], "->", group_new["root"])
PY
```

- [ ] `artifact_files` is equal for all four editions.
- [ ] The changed top-level keys are exactly:
      - `rp2005`, `rp2018`: `inputs`, `pdf`, `ascii_source`,
        `preformatted_source`;
      - `rp2005-2019`: `inputs`, `note`;
      - `rp2018-2023`: `inputs`, `note`, `source_commit`, `strongs_commit`.
      Any other key is a failure (R5.4).
- [ ] The input `files[].sha256`/`size` lists are equal per group; only the
      group `root`, the current edition's two `include` globs, and (for
      `rp2018-2023`) the first path segment's case differ.
      The new roots are `data/raw/print/rp2005/{ccat,ascii}`,
      `data/raw/print/rp2018/{ccat,ascii}`,
      `data/raw/repo/rp2005-2019`, and `data/raw/repo/rp2018-2023`.
- [ ] `pdf_sha256` and `pdf_size` are unchanged for `rp2005`/`rp2018`;
      `tag`/`commit` unchanged; `generated_by` still
      `"PYTHONPATH=src python3 -m byz.build"` in all four.
- [ ] `tests/curate/test_fidelity.py::ManifestIntegrityTests` passes.

### 3.3 The input byte gate

- [ ] Re-run the data snapshot into
      `/tmp/opencode/byz-classes-data-after.sha256` and diff. Expected
      differences only:
      - the path names of the 289 moved files (their hashes are unchanged);
      - `data/provenance/rp2005.toml`, `rp2018.toml`, `rp2005-2019.toml`
        (`extracted` only);
      - the new `data/provenance/rp2018-2023.toml`;
      - `data/text/README.md` -> `data/raw/repo/CONVENTIONS.md` (content
        rewritten);
      - the eight new READMEs.
      No archive, PDF, `.CCT`, `.TXT`, `.BP5`, `.ASC`, or `*_Byz.txt` hash
      changes.

```bash
# every moved file keeps its hash
python3 - <<'PY'
import hashlib
import pathlib

before = {}
for line in pathlib.Path(
    "/tmp/opencode/byz-classes-data-before.sha256"
).read_text().splitlines():
    digest, path = line.split("  ", 1)
    before[path] = digest

moves = {
    "data/text/CCAT/": "data/raw/repo/rp2018-2023/ccat/",
    "data/text/Strongs/": "data/raw/repo/rp2018-2023/strongs/",
    "data/raw/rp2005/editions-rp2-ccat/": "data/raw/print/rp2005/ccat/",
    "data/raw/rp2005/editions-rp2-ascii/": "data/raw/print/rp2005/ascii/",
    "data/raw/rp2005/editions-rp2-preformatted/": "data/raw/print/rp2005/preformatted/",
    "data/raw/rp2005/official-pdf/": "data/raw/print/rp2005/official-pdf/",
    "data/raw/rp2018/rp2018-ccat/": "data/raw/print/rp2018/ccat/",
    "data/raw/rp2018/rp2018-ascii-one-line-per-verse/": "data/raw/print/rp2018/ascii/",
    "data/raw/rp2018/rp2018-ascii/": "data/raw/print/rp2018/preformatted/",
    "data/raw/rp2018/official-pdf/": "data/raw/print/rp2018/official-pdf/",
    "data/raw/_archives/": "data/raw/print/_archives/",
    "data/raw/rp2005-2019/": "data/raw/repo/rp2005-2019/",
}

checked = 0
skipped = []
for old, digest in sorted(before.items()):
    for src, dst in moves.items():
        if old.startswith(src):
            new = pathlib.Path(dst + old[len(src):])
            assert new.is_file(), new
            actual = hashlib.sha256(new.read_bytes()).hexdigest()
            assert actual == digest, old
            checked += 1
            break
    else:
        skipped.append(old)
print("checked", checked)      # 289
print("not moved", skipped)    # only the files this change edits or adds
PY
```

- [ ] `sha256sum data/raw/repo/rp2018-2023/ccat/01_MAT.TXT` is
      `0de6c3ca28ea270a8902414b95df2a95d259c092e2cc37a0a39aeabad1373e29` (the
      value the 2026-11-25 validation recorded for `data/text/CCAT/01_MAT.TXT`).
- [ ] `git diff --stat -- data/provenance/rp2005.toml
      data/provenance/rp2018.toml` shows 3 changed lines each;
      `git diff data/provenance/rp2005-2019.toml` shows 1.
- [ ] The moved extract trees equal the archive content:

```bash
diff -r /tmp/opencode/classes-zips/editions-rp2-ccat \
        data/raw/print/rp2005/ccat
diff -r /tmp/opencode/classes-zips/editions-rp2-ascii \
        data/raw/print/rp2005/ascii
diff -r /tmp/opencode/classes-zips/editions-rp2-preformatted \
        data/raw/print/rp2005/preformatted
diff -r /tmp/opencode/classes-zips/rp2018-ccat \
        data/raw/print/rp2018/ccat
diff -r /tmp/opencode/classes-zips/rp2018-ascii-one-line-per-verse \
        data/raw/print/rp2018/ascii
diff -r /tmp/opencode/classes-zips/rp2018-ascii \
        data/raw/print/rp2018/preformatted
```

  Expected: no output for all six. (If a zip extracts a nested directory, `diff
  -r` names it; adapt the target in the comparison, not the tree.)

### 3.4 The diff-report gate

- [ ] Re-run `PYTHONPATH=src python3 -m byz.diff`, then the phase 0 docs
      snapshot diff. Expected:
      - for each pair, `changes.csv`, `source.diff`, `text.diff`,
        `apparatus.diff`, and `derived.diff` are byte identical;
      - each pair's `report.md` changes on one line (the Notation bullet naming
        the current source path);
      - `reports/diffs/README.md` changes only in its "Source and text" prose.

```bash
git diff --stat -- reports/diffs
git diff -- reports/diffs | grep '^[-+]' | grep -v '^[-+][-+]'
```

- [ ] The four pair directories still have the same file sets and the same row
      counts in `changes.csv`; no category moved.

- [ ] The other regenerated reports change only where a dataset name or the
      current-state label is rendered: `reports/baseline/{summary.md,
      books.csv,differences.csv,derivations.csv,files.csv}`,
      `reports/reconciliation/{summary.md,decision-log.md,files.csv,
      history.csv,verses.csv}`, `docs/contract/*.json`,
      `docs/DATA_CONTRACT.md`, `docs/HISTORY.md`, and `docs/PROVENANCE.md`.
      Confirm no numeric figure (verse count, match count, percent) moved:

```bash
git diff -- reports/baseline reports/reconciliation \
  | grep -E '^[-+]\|' | grep -v 'data/raw/repo\|data/text\|current '
```

- [ ] `docs/contract/` contains no `data__text__*.json`; it contains
      `data__raw__repo__rp2018-2023__ccat.json`,
      `...__strongs.json`, the six edition documents, and `contracts.json`.

```bash
ls docs/contract
test ! -e docs/contract/data__text__CCAT.json
test ! -e docs/contract/data__text__Strongs.json
```

## 4. Provenance gate

### 4.1 `data/provenance/rp2018-2023.toml`

```bash
head -12 data/provenance/rp2018-2023.toml
grep -c '^\[\[prefixes\]\]' data/provenance/rp2018-2023.toml   # 2
grep -c '^\[\[files\]\]' data/provenance/rp2018-2023.toml      # 56
grep -n -E 'https?://|downloaded|/home/' data/provenance/rp2018-2023.toml  # none
```

- [ ] `edition = "rp2018-2023"`, `revision = "2023-07-20"`,
      `extracted = "data/raw/repo/rp2018-2023"`, `generated_by =
      "PYTHONPATH=src python3 -m byz.build"`.
- [ ] The two prefix blocks are `ccat/` 29 and `strongs/` 27, sorted.
- [ ] The 56 file blocks are sorted by `path`; a script (or
      `tests/curate/test_input_provenance.py`) verifies every hash and size and
      that the set equals `editions/rp2018-2023/manifest.json`'s first input
      group.
- [ ] `ccat_commit`/`strongs_commit` name real commits once the move commit
      exists (`git log -1 --format=%h -- data/raw/repo/rp2018-2023/ccat`); before
      that commit they name the last commit that touched the old selectors, and
      after the follow-up they name the move commit. Empty is accepted only in a
      shallow checkout, and §9 records the lag.
- [ ] A second `byz.build` changes no byte of the file (the one-commit lag of
      §9 is the only allowed move after a commit).

### 4.2 The two ingest commands

- [ ] `PYTHONPATH=src python3 -m byz.materialise` prints
      `materialised data/raw/repo/rp2005-2019 (57 files)`; the second run
      produces no `git status` change and exits 0.
- [ ] `data/provenance/rp2005-2019.toml` has 2 prefix blocks and 57 sorted file
      blocks, no URL, no timestamp; the tag and commit are unchanged.
- [ ] `PYTHONPATH=src python3 -m byz.fetch --verify` exits 0 with no network and
      no writes (`git diff -- data/provenance/rp2005.toml
      data/provenance/rp2018.toml` empty).
- [ ] `PYTHONPATH=src python3 -m byz.fetch` (record mode) rewrites only the
      `extracted` lines; run it twice and confirm the second run is a no-op.
- [ ] A conflicting file is still refused: in a temp `dest_root`, change one
      byte under the materialised tree and assert `SystemExit` names the path
      and both hashes (covered by `tests/curate/test_materialise.py`).

### 4.3 `byz.verify`

- [ ] Clean run:

```bash
PYTHONPATH=src python3 -m byz.verify
```

  Expected: four `OK` lines, `rp2005` 56/141, `rp2005-2019` 57/195, `rp2018`
  57/141, `rp2018-2023` 56/195; summary
  `verified 4 editions (226 inputs, 672 artifacts)`; exit 0.
- [ ] `PYTHONPATH=src python3 -m byz.verify rp2018-2023` exits 0 and prints
      `OK rp2018-2023: 56 inputs, 195 artifacts`.
- [ ] In a scratch clone (`git clone --no-hardlinks .`), corrupt one byte of
      `data/raw/repo/rp2018-2023/ccat/01_MAT.TXT`; verify exits 1 and prints
      `FAIL rp2018-2023: data/raw/repo/rp2018-2023/ccat/01_MAT.TXT: sha256
      expected …, actual …`; restore with `git checkout --`.
- [ ] In the same clone, add `data/raw/repo/rp2018-2023/ccat/99_ZZZ.TXT`;
      verify reports it as `unexpected` (it matches `ccat/*.TXT`); remove it.
- [ ] In the same clone, change a manifest input `root` to
      `data/text` (the retired path, still under `data/`); verify reports the
      group's files as `missing`, which proves the manifest and the tree are
      tied to the new root, not to the old one. Restore the manifest.
- [ ] `PYTHONPATH=src python3 -m byz.verify rp1999` exits 2.
- [ ] `--edition-dir` on a copied edition still verifies artifacts and says
      inputs were skipped.
- [ ] `tests/curate/test_verify.py` is green; its fixture roots are updated from
      `data/text` to `data/raw/repo/rp2018-2023` where it names the real tree
      (lines 54-56, 94, 104, 114).

## 5. The generated README gate

- [ ] The eight files exist and are the only `README.md` in their folder:

```bash
for p in data/README.md data/raw/README.md data/raw/print/README.md \
         data/raw/repo/README.md data/raw/print/rp2005/README.md \
         data/raw/print/rp2018/README.md \
         data/raw/repo/rp2005-2019/README.md \
         data/raw/repo/rp2018-2023/README.md; do
  printf '%s: ' "$p"; head -1 "$p"
done
```

  Expected: every line is `<!-- generated-file: do not edit by hand -->`.
- [ ] `data/raw/repo/CONVENTIONS.md` is the **only** Markdown under `data/`
      without that first line:

```bash
find data -name '*.md' | sort
find data -name '*.md' -exec head -1 {} \; | sort | uniq -c
```

- [ ] Counts in the READMEs match the manifests and the tree:

| README | Must state |
| --- | --- |
| `data/README.md` | two classes; 226 pinned inputs (113 print, 113 repo); the conventions path; the four commands |
| `data/raw/README.md` | the print/repo definitions; the four source folders and `_archives/`; the edition each feeds |
| `data/raw/print/README.md` | 6 archives (3+3); 29/27/27/1 and 30/27/27/1; `byz.fetch` |
| `data/raw/repo/README.md` | `rp2005-2019` (tag `v2.0.3`, 30/27) and `rp2018-2023` (29/27, revision 2023-07-20); `CONVENTIONS.md`; `byz.materialise`, `byz.build`, `byz.verify` |
| `.../print/rp2005/README.md` | 29/27/27/1; its three archives; the PDF; `editions/rp2005/`; `data/provenance/{rp2005,pdfs}.toml` |
| `.../print/rp2018/README.md` | 30/27/27/1; its three archives; the PDF; `editions/rp2018/`; `data/provenance/{rp2018,pdfs}.toml` |
| `.../repo/rp2005-2019/README.md` | 30/27; tag `v2.0.3`, commit; `byz.materialise`; `data/provenance/rp2005-2019.toml`; link to `../CONVENTIONS.md` |
| `.../repo/rp2018-2023/README.md` | 29/27; revision 2023-07-20; `byz.build`/`byz.verify`; `data/provenance/rp2018-2023.toml`; link to `../CONVENTIONS.md` |

- [ ] Every relative Markdown link in the eight READMEs and in
      `CONVENTIONS.md` resolves. `tests/curate/test_editions.py::PdfLinkTests`
      covers them; spot-check manually:

```bash
PYTHONPATH=src python3 -m unittest tests.curate.test_editions.PdfLinkTests -v
```

- [ ] No README prints a build time, a host name, or an absolute path; the only
      date is `2023-07-20` (and historical tag names).
- [ ] A print README never says the repository conventions govern its files;
      the two repo READMEs link `CONVENTIONS.md`.
- [ ] Determinism: `PYTHONPATH=src python3 -m byz.build` twice, then
      `git diff --stat -- data` is empty.
- [ ] An untracked file does not change a pinned count: create
      `data/raw/print/rp2005/preformatted/untracked.ASC`, run `byz.build`, and
      confirm `git diff` is empty (auxiliary counts come from `git ls-files`);
      delete it.
- [ ] The registry and classification agree:
      `PYTHONPATH=src python3 -m unittest tests.curate.test_generated -v` is
      green, `len(generated.GENERATED_MARKDOWN)` expands to 26 files,
      `len(generated.GENERATED_FILES) == 13`, and
      `data/raw/repo/CONVENTIONS.md` matches no registry pattern.
- [ ] `reports/baseline/files.csv` has doc rows for all 13 `DOC_FILES` entries
      (including the eight READMEs and `CONVENTIONS.md`) and no
      `data/text/README.md` row.

## 6. The conventions document gate

- [ ] `data/raw/repo/CONVENTIONS.md` has no banner and is hand-maintained (see
      §5).
- [ ] The preamble says the document covers the repository-lineage sources, is
      not asserted for the print extracts under `data/raw/print/`, and is the
      authority referenced by `src/byz/beta/converter.py`.
- [ ] Dr Robinson's prose is intact. The exact diff from the pre-change body
      (run in phase 4b) shows only the two `ccat/`/`strongs/` directory-name
      lines:

```bash
git show HEAD:data/text/README.md \
  | sed -n '/^## Variant codes$/,$p' > /tmp/opencode/conventions-body-before.md
sed -n '/^## Variant codes$/,$p' data/raw/repo/CONVENTIONS.md \
  > /tmp/opencode/conventions-body-after.md
diff -u /tmp/opencode/conventions-body-before.md \
        /tmp/opencode/conventions-body-after.md
```

  Paste the diff (or "no output") in §12. If a content line changed, restore
  it; do not "improve" the text.
- [ ] `data/text/README.md` does not exist; `git ls-files data/text` is empty.
- [ ] The variant-code list, the tense/voice/mood/person/number/gender/case
      tables, the James 4:5 two-parsing example, the Strong's notes, and the
      sample table are all present (anchors asserted by
      `tests/curate/test_layout.py::ConventionsDocumentTests`).

## 7. The retired-path gate

- [ ] The five roots do not exist and are not tracked:

```bash
for p in data/text data/raw/rp2005 data/raw/rp2018 \
         data/raw/rp2005-2019 data/raw/_archives; do
  test ! -e "$p" || echo "STILL EXISTS: $p"
done
git ls-files data/text data/raw/rp2005 data/raw/rp2018 \
              data/raw/rp2005-2019 data/raw/_archives     # no output
```

- [ ] No tracked text file names a retired root outside the allowlist:

```bash
git grep -n -E 'data/text/|data/raw/_archives/|data/raw/rp2005/|data/raw/rp2018/|data/raw/rp2005-2019/' \
  -- ':!SPECS' ':!docs/EDITIONS.md' ':!docs/HISTORY.md' \
     ':!src/byz/curate/docs.py' ':!src/byz/contract/history.py' \
     ':!src/byz/reconcile/report.py' ':!src/byz/reconcile/historical.py' \
     ':!tests'
```

  Expected: no output. (`data/raw/repo/rp2005-2019/` and
  `data/raw/print/rp2005/` do not match these patterns; verify with
  `git grep -c` on one of the new paths if the patterns are edited.)
- [ ] `tests/curate/test_layout.py::RetiredLayoutSweepTests` and
      `test_current_pipeline.py::LegacyTreesAreGoneTests` are green, including
      the new five-root absence test.
- [ ] No compatibility shim exists: `find data -maxdepth 4 -type l` prints
      nothing, and no `*.gitkeep` is under `data/`.

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

- [ ] `byz.fetch --verify` exits 0, no network, no writes.
- [ ] `byz.build` prints `built 4 editions`, `wrote docs/EDITIONS.md`,
      `updated README.md`, and `updated 8 input-tree READMEs`; it writes the
      manifests, the edition READMEs, the eight input READMEs, and
      `data/provenance/rp2018-2023.toml`.
- [ ] `byz.diff` writes the four reports; against the before snapshot, only each
      pair's `report.md` Notation line and `reports/diffs/README.md`'s Source
      prose move (§3.4).
- [ ] `byz.contract`, then `byz.reconcile`, then `byz.contract` leaves
      `docs/HISTORY.md` with one banner, one `# Internal history map`, and one
      `<!-- cycle2:begin -->` block.
- [ ] `byz.verify` exits 0 with `226 inputs, 672 artifacts`.
- [ ] Snapshot run 1:

```bash
find README.md docs reports editions data -type f -print0 \
  | sort -z | xargs -0 sha256sum \
  > /tmp/opencode/byz-classes-run1.sha256
```

- [ ] Run the whole sequence a second time; snapshot run 2; `diff` the two files
      is silent, and `git status --porcelain` is identical after run 1 and run 2.
- [ ] No `editions/.rp*` or `editions/.*.staging` directory remains; no
      `data/.tmp` directory remains:

```bash
ls -a editions data
```

- [ ] No wall-clock timestamp, host name, or absolute path in generated output:

```bash
git grep -n -E '/home/|localhost|/tmp/opencode' -- README.md docs reports editions data
```

  Expected: no output. (`2023-07-20`, commit hashes, and the recorded
  `downloaded` timestamps in `rp2005.toml`/`rp2018.toml` are history, not run
  metadata; the `downloaded` timestamps are pre-existing and unchanged.)

## 9. The suites

```bash
PYTHONPATH=src python3 -m unittest discover -s tests/contract
PYTHONPATH=src python3 -m unittest discover -s tests/curate
PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation
```

- [ ] All three pass with 0 failures and 0 unplanned skips. Record the counts
      (the 2026-11-25 baseline was contract 64, curate 247, reconciliation 80;
      this change adds `test_data_docs` and `test_input_provenance` and extends
      several files).
- [ ] `tests/curate/test_reproducible.py` passes after the change commit and the
      follow-up regeneration commits. Before the change it fails for the known
      reason (it builds a worktree at `HEAD`); the §8 two-run check is the
      authoritative pre-commit evidence.
- [ ] `tests/contract::ContractWorktreeTests` pass after the follow-ups.
      Because the change touches `editions/*/manifest.json` (`editions` is in
      `CORPUS_PATHSPECS`), adds `data/raw/repo` to `CORPUS_PATHSPECS`, and writes
      `data/provenance/rp2018-2023.toml` whose `ccat_commit`/`strongs_commit`
      change once the move commit exists, the first follow-up rewrites the
      manifests and the provenance and `docs/HISTORY.md`; a second follow-up
      should touch only `docs/HISTORY.md` and converge. Record the actual number
      and hashes.
- [ ] No test touches the network; no test writes to the repository. The
      materialise, provenance, and README tests use temporary roots or
      read-only assertions.
- [ ] A shallow clone still cannot run the worktree tests; that is documented
      behaviour, not a regression.

Convergence table:

| Commit | Contents | `tests/contract` | `tests/curate` | `tests/reconciliation` |
| --- | --- | --- | --- | --- |
| A (the change) | 13 moves, provenance, READMEs, code/tests/docs | | | |
| B (first follow-up) | manifests, provenance commits, baseline, `docs/HISTORY.md` | | | |
| C (second follow-up, if any) | `docs/HISTORY.md` only | | | |

## 10. Manual inspection

- [ ] Open `editions/rp2018-2023/manifest.json`: `inputs[0].root` is
      `data/raw/repo/rp2018-2023`, `include` is `ccat/*.TXT` and
      `strongs/*.BP5`, 56 files, and `artifact_files` is 195 entries with the
      same hashes as before.
- [ ] Open `editions/rp2005/manifest.json`: the two groups point at
      `data/raw/print/rp2005/{ccat,ascii}`; `pdf` is
      `data/raw/print/rp2005/official-pdf/editions-rp2.pdf`;
      `pdf_sha256` is unchanged.
- [ ] Open `editions/rp2005-2019/manifest.json`: the root is
      `data/raw/repo/rp2005-2019`, the two includes are `parsed/*.UB5` and
      `textonly-beta-code/*.CCT`, `tag`/`commit` unchanged.
- [ ] Open `data/provenance/rp2018-2023.toml` and read it start to finish: it
      looks like `rp2005-2019.toml` with `revision` and two commit keys instead
      of `tag`/`commit`.
- [ ] Read `data/README.md`, `data/raw/README.md`, `data/raw/print/README.md`,
      and `data/raw/repo/README.md` as a first-time reader: each answers "what
      is here", "which edition uses it", "where is its provenance", and "what
      do I run".
- [ ] Read one print source README and one repo source README: the first never
      claims the repo conventions; the second links `CONVENTIONS.md`.
- [ ] Read `data/raw/repo/CONVENTIONS.md`: the preamble scopes it to the repo
      class, and Dr Robinson's text reads as it did.
- [ ] Read `docs/EDITIONS.md`'s new section: every retired path maps to its new
      home, and it says the bytes did not change and no shim exists.
- [ ] Read `docs/BUILD.md` as a first-time contributor: install, the two
      classes, the commands, the verify section, the report order, the tests.
- [ ] Read `SPECS/TECH.md` §5 and compare it with `find data -maxdepth 4 -type
      d`; the tree matches.
- [ ] Read `.opencode/commands/read-conventions.md` and one agent file: the
      commands run as written, and no file says `data/text/`.
- [ ] Run `PYTHONPATH=src python3 -m byz.verify` and the scratch-clone
      corrupted-input check (§4.3) once more against the committed tree.

## 11. Definition of done

- [ ] `data/raw/{print,repo}/` exist with the chosen tree; the five retired
      roots are gone; `data/` is 302 tracked files and the repository 1163.
- [ ] The 289 moved files are byte identical; the six archives and two PDFs are
      unchanged; `01_MAT.TXT` keeps `0de6c3ca…`.
- [ ] Eight generated READMEs + hand-maintained `CONVENTIONS.md`;
      `data/provenance/rp2018-2023.toml` records revision, commits, 56 hashes;
      both ingest commands are idempotent.
- [ ] All 672 edition CSV/TEI files and all four `artifact_files` lists are
      unchanged; the only manifest differences are R5.4's.
- [ ] `byz.verify` exits 0 with `226 inputs, 672 artifacts`; each diff pair's
      `changes.csv` and `*.diff` files are unchanged, and the only report prose
      that moved is the current-source line.
- [ ] The sequence runs twice with no diff; no timestamp/host/absolute path; the
      three suites pass after the follow-ups.
- [ ] No tracked file names a retired root outside the allowlist; the mapping is
      rendered in `docs/EDITIONS.md`.
- [ ] Every deviation from `plan.md` is recorded in §12 below.

## 12. Verification record (to fill in)

### 12.1 Red-phase messages

| Test | Exact failure | Intended? |
| --- | --- | --- |
| `test_layout.InputTreeTests` | `data/raw/print`, `data/raw/repo`, and `data/raw/repo/rp2018-2023/ccat` did not exist; `paths.CCAT_DATASET` was still `data/text/CCAT`. | yes |
| `test_input_provenance` | `FileNotFoundError: data/provenance/rp2018-2023.toml`. | yes |
| `test_data_docs` | `FileNotFoundError: data/README.md` and the other seven. | yes |
| `test_generated.BannerScopeTests` | the eight `data/**/README.md` files were unclassified; the count was 18, not 26. | yes |
| `test_editions.DocsTests` | missing `## Where the inputs moved into the print and repo classes (2026-11-25)` and its rows. | yes |
| `tests.reconciliation.test_fetch` | extraction still used the archive stem (`data/raw/rp2018/fixture`), not `FORMAT_DIRS`. | yes |

### 12.2 Gate results

| Check | Result | Evidence |
| --- | --- | --- |
| 672 edition CSV/TEI byte identical | pass | `find` snapshot before/after, excluding the pre-existing ignored `editions/.rp2018.staging` tree: 672 paths, 0 missing, 0 extra, 0 changed. The raw `editions/*/{csv,tei}` glob was 734 because the stale staging tree held 62 ignored files; the first build removed it. Separately, all 672 `artifact_files` hashes match. |
| 4 manifests: `artifact_files` equal | pass | `old["artifact_files"] == new["artifact_files"]` for all four; file sets and hashes/sizes of every pinned input unchanged. |
| 226 inputs, 672 artifacts (`byz.verify`) | pass | `verified 4 editions (226 inputs, 672 artifacts)`; `byz.verify rp2018-2023` → `56 inputs, 195 artifacts`. |
| 289 moved files byte identical | pass | 288 files under the twelve moved prefixes hash identically; `data/text/README.md` is the 289th and was rewritten as `CONVENTIONS.md`. `01_MAT.TXT` is `0de6c3ca…`. |
| 6 extract trees equal the archives | pass | `diff -r /tmp/opencode/classes-zips/<archive> data/raw/print/...` silent for all six. |
| `rp2018-2023.toml` shape/hashes | pass | banner, `revision = "2023-07-20"`, 2 sorted prefixes (29/27), 56 sorted files; every hash/size equals `files.sha256_file`/`stat`. |
| `materialise`/`fetch` idempotent | pass | second `byz.materialise` prints the same 57 files and writes no byte; second record-mode `byz.fetch` writes no byte. Only the three `extracted` lines per official record changed; `downloaded`/`final_url`/`http_status` unchanged. |
| 8 READMEs: banner/skeleton/counts/links | pass | `tests/curate/test_data_docs.py` (21 tests, including the R6.8 untracked-file check) and `test_editions.PdfLinkTests`; second render byte-identical. |
| `CONVENTIONS.md` body diff | pass | `diff -u` shows only the `CCAT`→`ccat/` and `Strongs`→`strongs/` lines. |
| 5 retired roots absent; sweep green | pass | Python sweep over tracked + new files finds 0 offenders outside the allowlist; `test_layout.RetiredLayoutSweepTests` passes. |
| Two runs no diff | pass | snapshots of `README.md docs reports editions data` (1040 files) are identical after a second full sequence. |
| Suites (contract/curate/reconciliation) | partial | contract 64 (1 pre-commit worktree failure, see 12.3), curate 287 OK, reconciliation 84 OK. The two extra tests are the R6.8 untracked-file check and the duplicate `(edition, format)` guard. |
| Follow-up commits and convergence | pending | not committed by the implementer; the build agent commits and runs the follow-up. |

### 12.3 Deviations log

1. **Manifest path changes (R5.2/R5.4).** The chosen tree makes
   `rp2018-2023`'s group root `data/raw/repo/rp2018-2023`, so its input
   `files[].path` values are now `ccat/01_MAT.TXT`/`strongs/01_MAT.BP5`
   instead of `CCAT/01_MAT.TXT`/`Strongs/01_MAT.BP5`. The file set, hashes,
   and sizes are unchanged. `ascii_source`/`preformatted_source` also change
   for the two official editions because those keys record the moved source
   directories. Artifact lists are byte-identical. R5.2/R5.4 were amended to
   state these changes, so they are intended manifest differences rather than
   a deviation from the implemented tree. R3.1 now records that the two
   provenance commits use full 40-hex hashes, as written.
2. **Tracked totals.** `data/` is 302 tracked files as required, but the
   repository is 1166, not 1163: the spec's arithmetic omitted the new
   `src/byz/curate/data_docs.py` and the two new test modules
   (`test_data_docs.py`, `test_input_provenance.py`).
3. **Byte-gate denominator.** The `find editions/*/{csv,tei}` snapshot was 734
   paths, not 672, because `csv/unaccented` is outside the contract and an
   ignored `editions/.rp2018.staging` tree existed at the base commit. The
   contract's 672 `artifact_files` are the gate and are identical; the staging
   tree is gone.
4. **`materialise` and the generated README.** `data/raw/repo/rp2005-2019/`
   now contains the generated `README.md`, so `materialise_historical`
   excludes `GENERATED_NEIGHBOURS = ("README.md",)` from its unexpected-file
   check and its file count (still 57).
5. **Pre-commit worktree test.**
   `tests/contract/test_integration.py::ContractWorktreeTests.test_update_history_is_idempotent`
   fails before the change commit: the worktree is checked out at HEAD
   (`a811b8c`), whose `docs/HISTORY.md` still carries the `data/text/CCAT`
   label, while the new row fixtures name
   `data/raw/repo/rp2018-2023/ccat`. This is the documented one-commit lag; it
   converges after the change commit and the usual follow-up regeneration.
6. **`byz.fetch --force` was not run**, as required.
