# Plan - The two source classes

Red/green TDD throughout (`SPECS/TECH.md` §10). Read `requirements.md` first;
`R1`-`R10` are the numbered requirements, "The chosen tree" is the target
layout, "README content model" is the renderer's contract, and `validation.md`
is the merge gate.

This is a layout, provenance, and documentation change. **No edition byte may
change**: all 672 files under `editions/*/{csv,tei}` stay identical, and every
`artifact_files` entry keeps its `path`, `sha256`, and `size`. If any of them
differs, stop and report; the input path, a reader, or a book map is wrong.

The normal build becomes (unchanged commands, new side effects):

```bash
PYTHONPATH=src python3 -m byz.fetch --verify
PYTHONPATH=src python3 -m byz.build          # also writes the 8 input READMEs + rp2018-2023 provenance
PYTHONPATH=src python3 -m byz.diff
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m byz.reconcile
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m byz.verify
```

`byz.fetch` (record mode) is run **once** in phase 2 to re-record the two
official provenance files against the new extract paths. `byz.materialise` is
run **once** in phase 2 to re-record the 2019 lineage's `extracted` path. Neither
is part of the normal rebuild.

## Phase 0 - Preconditions and the before-snapshot

- [ ] Save the superseded draft's wording, then restore a committed base. The
      working tree at `a811b8c` has six superseded paths (requirements,
      "Superseded work in the working tree"):

```bash
cp data/README.md /tmp/opencode/data-README-draft.md
rm data/README.md
git checkout -- data/text/README.md reports/baseline/files.csv \
  src/byz/contract/inventory.py src/byz/generated.py \
  tests/curate/test_layout.py
git status --porcelain          # empty
```

- [ ] Stay on `feature/2026-11-16-edition-recovery-curation`. Do not switch
      branches or commit. Record `git rev-parse HEAD` (the spec was written at
      `a811b8c`) and `python3 --version` (3.12.3) and confirm
      `python3 -c "import beta_code"`.
- [ ] The history and tags are present: `git tag --list v2.0.3 v3.3.4` prints
      both, and `git rev-parse v2.0.3^{commit}` prints
      `8ec95671e463030347c2c643358eb56e58235b19`.
- [ ] Snapshot every edition CSV/TEI (672 files):

```bash
find editions -type f \
  \( -path 'editions/*/csv/*' -o -path 'editions/*/tei/*' \) -print0 \
  | sort -z | xargs -0 sha256sum \
  > /tmp/opencode/byz-classes-editions-before.sha256
wc -l /tmp/opencode/byz-classes-editions-before.sha256    # 672
```

- [ ] Snapshot the manifests, the reports, and the whole input tree:

```bash
for id in rp2005 rp2005-2019 rp2018 rp2018-2023; do
  git show "HEAD:editions/$id/manifest.json" \
    > "/tmp/opencode/classes-manifest-$id-before.json"
done
find reports docs -type f -print0 | sort -z | xargs -0 sha256sum \
  > /tmp/opencode/byz-classes-docs-before.sha256
find data -type f -print0 | sort -z | xargs -0 sha256sum \
  > /tmp/opencode/byz-classes-data-before.sha256
```

- [ ] Record the inventory: `git ls-files data | wc -l` -> **293**,
      `git ls-files editions | wc -l` -> **680**, `git ls-files | wc -l` ->
      **1154**, and the per-directory counts from requirements' "Verified
      inventory" (29/27, 29/27/27/1, 30/27/27/1, 6, 57).
- [ ] Extract the six archives so the moved trees can be proved to be their
      content:

```bash
rm -rf /tmp/opencode/classes-zips && mkdir -p /tmp/opencode/classes-zips
python3 - <<'PY'
import pathlib, zipfile
for archive in sorted(pathlib.Path("data/raw/_archives").glob("*/*")):
    target = pathlib.Path("/tmp/opencode/classes-zips") / archive.stem
    target.mkdir(parents=True, exist_ok=True)
    zipfile.ZipFile(archive).extractall(target)
PY
find /tmp/opencode/classes-zips -type f | wc -l    # 167 (29+27+27+30+27+27)
```

  (`Path.stem` strips either `.zip` or `.ZIP`, so the 2018 CCAT archive lands in
  `rp2018-ccat/`.)

## Phase 1 - Move the trees and switch the path constants (R1, R2, R4)

### 1a. Red

- [ ] `tests/curate/test_layout.py` `InputTreeTests` (lines 120-192):
      - replace `test_repository_inputs_live_under_data_text` with
        `test_input_tree_has_the_two_classes`: `data/raw/print` and
        `data/raw/repo` are directories, `data/text` is not, the counts are 29
        `.TXT` in `data/raw/repo/rp2018-2023/ccat` and 27 `.BP5` in
        `.../strongs`, and `data/raw/repo/CONVENTIONS.md` exists;
      - add `test_print_trees_are_under_the_print_class`: for each edition, the
        `ccat`/`ascii`/`preformatted` counts are 29/27/27 and 30/27/27 and the
        PDF is in `official-pdf/`;
      - replace `test_contract_uses_the_data_text_dataset_names` with
        `test_contract_uses_the_repo_dataset_names`:
        `paths.CCAT_DATASET == "data/raw/repo/rp2018-2023/ccat"`, the same for
        Strong's, and `paths.CCAT_DIR`/`BP5_DIR` resolve under it;
      - `test_history_keeps_the_pre_move_evidence` (143-147) keeps
        `source/CCAT` and adds `data/text/CCAT` as selectors and the new dataset
        label;
      - add `test_retired_input_roots_do_not_exist` (the five roots) and
        `test_no_tracked_file_under_a_retired_input_root`
        (`git ls-files data/text data/raw/rp2005 data/raw/rp2018
        data/raw/rp2005-2019 data/raw/_archives` is empty).
- [ ] `tests/curate/test_integration.py`:
      - `test_current_manifest_pins_the_current_inputs` (~95-110): root
        `data/raw/repo/rp2018-2023`, includes `["ccat/*.TXT", "strongs/*.BP5"]`,
        and the sample path `ccat/01_MAT.TXT`;
      - the historical group assertion (~60-80) keeps `textonly-beta-code/MT.CCT`
        and reads the new root.
- [ ] `tests/curate/test_historical_pipeline.py` (226-231): root
      `data/raw/repo/rp2005-2019`.
- [ ] `tests/curate/test_build.py` (105-110, 155): the labels are
      `data/raw/repo/rp2018-2023/ccat`; the official reader test reads
      `data/raw/print/rp2018/ccat/MR.CCT`.
- [ ] `tests/contract/test_integration.py` (33-34, 44-51, 62-63, 105-107,
      230, 237) and `tests/contract/test_coverage.py` (22): dataset names and
      the current-state label.
- [ ] `tests/reconciliation/test_integration.py` (8, 22-23, 40, 79, 128,
      156-157): archive helper path, skip message, the current row path, and the
      `current ...` label.
- [ ] Confirm the failure reason: `KeyError`/`AssertionError` on the missing new
      directories and on `paths.CCAT_DATASET`, not an import error.

### 1b. Green: the moves

- [ ] Create the class roots, then `git mv` (no `cp`, no `rm`):

```bash
# `git mv` does not create missing destination parents, so make the class and
# edition directories first.
mkdir -p data/raw/print/rp2005 data/raw/print/rp2018 \
         data/raw/repo/rp2018-2023

# print class
git mv data/raw/_archives data/raw/print/_archives
git mv data/raw/rp2005/editions-rp2-ccat         data/raw/print/rp2005/ccat
git mv data/raw/rp2005/editions-rp2-ascii        data/raw/print/rp2005/ascii
git mv data/raw/rp2005/editions-rp2-preformatted data/raw/print/rp2005/preformatted
git mv data/raw/rp2005/official-pdf              data/raw/print/rp2005/official-pdf
git mv data/raw/rp2018/rp2018-ccat               data/raw/print/rp2018/ccat
git mv data/raw/rp2018/rp2018-ascii-one-line-per-verse \
       data/raw/print/rp2018/ascii
git mv data/raw/rp2018/rp2018-ascii              data/raw/print/rp2018/preformatted
git mv data/raw/rp2018/official-pdf              data/raw/print/rp2018/official-pdf

# repo class
git mv data/raw/rp2005-2019 data/raw/repo/rp2005-2019
git mv data/text/CCAT        data/raw/repo/rp2018-2023/ccat
git mv data/text/Strongs     data/raw/repo/rp2018-2023/strongs
git mv data/text/README.md   data/raw/repo/CONVENTIONS.md
rmdir data/text
```

  (`data/raw/print/_archives` already contains `rp2005/` and `rp2018/`; no
  second level is needed. `data/raw/rp2005` and `data/raw/rp2018` disappear once
  their last child is moved; remove them with `rmdir` if empty.)

- [ ] Prove every move kept its bytes:

```bash
git status --porcelain -- data | grep -v '^R '    # only the new/modified docs
for d in data/raw/repo/rp2018-2023/ccat data/raw/repo/rp2018-2023/strongs \
         data/raw/repo/rp2005-2019/textonly-beta-code \
         data/raw/repo/rp2005-2019/parsed; do
  find "$d" -type f | wc -l
done
```

### 1c. Green: the constants and the sweep

- [ ] `src/byz/contract/paths.py` (10-14): replace `DATA_TEXT`/`CCAT_DIR`/
      `BP5_DIR`/the two dataset names per R4.1 and update
      `DERIVATION_EVIDENCE` (100-113). Keep `CURRENT_EDITION`/`CURRENT_PREFIX`
      below it unchanged.
- [ ] `src/byz/reconcile/sources.py` (7-11): `PRINT_DIR`, `REPO_DIR`,
      `ARCHIVE_DIR = PRINT_DIR / "_archives"`, and
      `FORMAT_DIRS = {"ccat": "ccat", "ascii-one-line": "ascii",
      "preformatted": "preformatted"}` with a comment that a format names one
      folder per edition.
- [ ] `src/byz/reconcile/fetch.py` (271-274): replace the archive-stem path with
      `extract_path = sources.PRINT_DIR / edition / sources.FORMAT_DIRS[...]`;
      fail loud on an unknown format and on a duplicate `(edition, format)`.
      Line 287's `extracted` follows automatically.
- [ ] `src/byz/curate/editions.py`: the registry entries (18-120) get the new
      `source_dir`/`ascii_dir`/`preformatted_dir`/`parsed_dir`/`strongs_dir`/
      `pdf` values, plus `"input_class"` on all four and
      `"revision": "2023-07-20"` on `rp2018-2023`. Rewrite the two notes that
      name paths (`rp2005-2019` 59-71, `rp2018-2023` 107-118).
- [ ] `src/byz/curate/materialise.py` (33-39): `HISTORICAL_INPUT_ROOT =
      "data/raw/repo/rp2005-2019"`. The tag, commit, `PREFIX_MAP`, and the
      writer are unchanged.
- [ ] `src/byz/contract/history.py` (16-51): the two pathspec tuples gain
      `data/raw/repo/rp2018-2023/{ccat,strongs}`; `CORPUS_PATHSPECS` gains
      `data/raw/repo`; comments say selectors, not paths.
- [ ] `src/byz/curate/build.py`: the current-text docstrings (67-71, 77-113,
      246-283), `EXPORT_NOTES["current"]` (124-128), the `build_current` labels
      (801-830), and `_check_source_books` calls; `_input_groups` (953-978) needs
      no logic change (it derives from the registry), but its docstring example
      does; `_readme` (884-950) names `data/` generically, so it is unchanged.
- [ ] `src/byz/curate/diff.py` (465-475, 715-722): the two `Source` prose
      strings name `data/raw/repo/rp2018-2023/ccat`.
- [ ] Delete the two contract JSON files whose names derive from the retired
      dataset names (they are regenerated under the new names in phase 5):
      `git rm docs/contract/data__text__CCAT.json
      docs/contract/data__text__Strongs.json`. `byz.contract` writes only the
      current names and never removes a stale file, so
      `tests/contract/test_integration.py::test_contract_json_matches_the_dataset_names`
      fails until they are gone.
- [ ] `src/byz/reconcile/historical.py` (18): `CURRENT_STATE =
      "current data/raw/repo/rp2018-2023/ccat"`. `_load_current` (67) uses the
      constants and needs no change.
- [ ] `src/byz/reconcile/compare.py` (18, 179, 362, 374) and
      `src/byz/curate/docs.py` (73-86, 118-151, 159-180, 187-204, 297-317,
      402-410, 426, 474-489, 519, 580, 599, 669-670): comments and paths only;
      the mapping tables are finished in phase 5.
- [ ] Green: `tests.curate.{test_layout,test_integration,test_build,
      test_historical_pipeline,test_current_pipeline,test_fidelity,test_materialise}`
      (the materialise real-tree test may still fail if it asserts the old
      root; update it in phase 2), `tests.contract.test_coverage`,
      `tests.contract.test_integration`, `tests.reconciliation.test_integration`.

### 1d. Regenerate and gate

- [ ] `PYTHONPATH=src python3 -m byz.build`.
- [ ] `git status --porcelain -- editions` shows only `manifest.json` and
      `README.md` for the four editions; **no** CSV/TEI.
- [ ] Byte gate: re-run the phase 0 snapshot into
      `/tmp/opencode/byz-classes-editions-after.sha256` and diff. Expected:
      silent, 672 lines both sides.
- [ ] Manifest gate: for each edition compare
      `artifact_files` with `/tmp/opencode/classes-manifest-<id>-before.json`
      (must be equal) and list the changed keys (expected: `inputs`, `pdf` for
      the two official editions, `note` for the two repo editions,
      `source_commit`/`strongs_commit` for `rp2018-2023`).
- [ ] `PYTHONPATH=src python3 -m byz.verify` exits 0 with
      `verified 4 editions (226 inputs, 672 artifacts)`.
- [ ] Do not run `byz.diff`/`byz.contract`/`byz.reconcile` yet; they are phase 6
      (their prose references are still being edited).

## Phase 2 - Provenance records and the ingest commands (R1.7, R2.5, R3)

### 2a. Red

- [ ] New `tests/curate/test_input_provenance.py`:
      - `data/provenance/rp2018-2023.toml` exists; line 1 is
        `generated.TOML_MARKER` and the file has no `http` string and no
        absolute path;
      - it has `edition`, `revision = "2023-07-20"`, `method`, `extracted =
        "data/raw/repo/rp2018-2023"`, `generated_by =
        "PYTHONPATH=src python3 -m byz.build"`, and `ccat_commit` /
        `strongs_commit` (each a full 40-hex hash; empty is allowed only in a
        shallow checkout with no history for the paths);
      - two `[[prefixes]]` blocks (`ccat/` 29, `strongs/` 27) sorted by `path`;
      - 56 `[[files]]` blocks sorted by `path`, each `sha256`/`size` equal to
        `files.sha256_file`/`stat()` of the committed file;
      - the file set equals the manifest's `inputs[0].files` set;
      - `build.write_manifest(edition, inputs)` called twice writes identical
        bytes.
- [ ] Extend `tests/curate/test_materialise.py`: the real-tree assertion uses
      `data/raw/repo/rp2005-2019` (57 files) and
      `materialise.HISTORICAL_INPUT_ROOT`; the provenance `extracted` value is
      the new path. The prefix names and hashes are unchanged.
- [ ] `tests/reconciliation/test_fetch.py` (177-179, 295-300, 358-363, 423,
      447): patch `sources.PRINT_DIR` (and `sources.ARCHIVE_DIR` where it is
      already patched); add one assertion that the extraction directory comes
      from `FORMAT_DIRS[spec["format"]]` and that an unknown format fails loud.
- [ ] Confirm the failures: `FileNotFoundError` for the new TOML, and the old
      extraction names.

### 2b. Green

- [ ] `src/byz/curate/build.py`: add `_current_provenance_text(edition, inputs)`
      next to `write_manifest` (1024-1067). It writes the TOML with
      `generated.toml_header()`, one scalar per line, two sorted `[[prefixes]]`
      blocks, and 56 sorted `[[files]]` blocks (reuse the JSON string quoting
      the materialiser uses, `json.dumps(path)`), then returns the path.
      `write_manifest` calls it after writing `manifest.json`, only when
      `edition["source_kind"] == "current"`. The commit values come from
      `_last_commit(*history.CCAT_COMMIT_PATHSPECS)` /
      `(*history.STRONGS_COMMIT_PATHSPECS)`, already computed for the manifest
      (1052-1055) - compute once and pass the same values to both.
- [ ] `PYTHONPATH=src python3 -m byz.build`; inspect the new TOML (head, block
      counts, hashes) and re-run to confirm no byte changes.
- [ ] `PYTHONPATH=src python3 -m byz.materialise`: it validates the moved tree,
      writes nothing, and rewrites only the `extracted` line of
      `data/provenance/rp2005-2019.toml`. Prove:

```bash
git diff data/provenance/rp2005-2019.toml      # one changed line: extracted
PYTHONPATH=src python3 -m byz.materialise      # second run: no diff
```

- [ ] `PYTHONPATH=src python3 -m byz.fetch --verify` (no network, no writes),
      then `PYTHONPATH=src python3 -m byz.fetch` (record mode). Prove:

```bash
git diff --stat data/provenance/rp2005.toml data/provenance/rp2018.toml
git diff data/provenance/rp2005.toml | grep '^[-+]' | grep -v '^[-+][-+]'
```

  Expected: only the three `extracted` lines in each file move to
  `data/raw/print/<edition>/{ccat,ascii,preformatted}`; `downloaded`,
  `final_url`, `http_status`, `sha256`, and `size` are untouched.
- [ ] Confirm the extract trees equal the archives' content (phase 0 extraction)
      with `diff -r` for all six folders.

### 2c. Gate

- [ ] Byte gate again (unchanged).
- [ ] `byz.verify` still exits 0.
- [ ] `git status --porcelain -- data` lists only the two provenance edits, the
      new TOML, the moved files, and `CONVENTIONS.md`.

## Phase 3 - The generated input-tree READMEs (R6, D4/D10)

### 3a. Red

- [ ] `tests/curate/test_generated.py`:
      - `BannerScopeTests.test_every_generated_markdown_starts_with_the_banner`
        (82-89): `18` -> `26`;
      - `test_every_markdown_under_generated_trees_is_classified` (90-104):
        `for tree in ("data", "docs", "editions", "reports")`, and the
        `data/raw/repo/CONVENTIONS.md` exception through
        `HAND_MAINTAINED_DOCS`;
      - `RegistryTests.test_registry_has_one_row_per_generated_family` (128):
        `12` -> `13`;
      - `test_registry_lists_the_generated_tomls_and_not_pdfs` also asserts
        `data/provenance/rp2018-2023.toml`;
      - `test_generated_registry_covers_the_banner_scope` stays (it proves the
        eight new files are covered).
- [ ] New `tests/curate/test_data_docs.py`:
      - the eight paths exist and are the only `README.md` in their folder;
      - each starts with `generated.MARKDOWN_MARKER` and the visible banner;
      - the required skeleton headings per level (requirements' content model);
      - the folder's own repo path, the consumer edition id, the provenance
        record path(s), and the command appear where required;
      - every relative Markdown link resolves (reuse the resolver from
        `test_editions.PdfLinkTests`);
      - `data/raw/repo/rp2018-2023/README.md` names `revision` `2023-07-20` and
        links `../CONVENTIONS.md`; `data/raw/repo/rp2005-2019/README.md` names
        `v2.0.3` and `byz.materialise`;
      - no absolute path, `/home/`, `localhost`, or date other than `2023-07-20`;
      - counts: `data/raw/print/rp2005/README.md` says 29/27/27/1;
        `data/raw/repo/rp2018-2023/README.md` says 29/27;
        `data/raw/print/README.md` says 6 archives (3+3);
      - determinism: render twice, equal strings; and a temporary untracked file
        in `data/raw/print/rp2005/preformatted/` does not change a pinned count
        (auxiliary counts come from `git ls-files`, so the test asserts the
        pinned ones only; note this in the test docstring).
- [ ] `tests/curate/test_editions.py::PdfLinkTests._user_docs` (236-247) gains
      the eight READMEs and `CONVENTIONS.md`.
- [ ] Delete the uncommitted-draft `DataReadmeTests` (if it survived phase 0,
      it is already gone; do not recreate it).
- [ ] Confirm the failure: `FileNotFoundError` for `data/README.md`, and the
      classification test naming the unlisted files.

### 3b. Green

- [ ] `src/byz/curate/files.py`: add `tracked_count(relative_dir, pattern="*")`
      (git `ls-files -z -- <relative_dir>`, filter basenames with `fnmatch`,
      `RuntimeError` naming the command when git fails). Keep `sha256_file` and
      `matching_files` unchanged.
- [ ] New `src/byz/curate/data_docs.py`:
      - imports `editions`, `files`, `sources`, `generated`;
      - `SOURCE_READMES` maps each edition id to its source folder path;
      - `_group_count(manifest, root)` and `_tracked_count(path, pattern)`;
      - `render_data_readme(manifests)`, `render_raw_readme(manifests)`,
        `render_class_readme(kind, manifests)`,
        `render_source_readme(edition_id, manifest)`;
      - `write_data_docs(manifests) -> list[Path]`, which writes each with
        `generated.write_markdown`;
      - no `str(editions.ROOT)` in any output; no clock.
- [ ] `src/byz/build.py::main`: after `docs.write_editions_doc()`, call
      `data_docs.write_data_docs(manifests)` and print
      `updated 8 input-tree READMEs` (deterministic).
- [ ] `src/byz/generated.py` per R6.5: the eight patterns in
      `GENERATED_MARKDOWN`; one new `GENERATED_FILES` row whose patterns are the
      eight README paths plus `data/provenance/rp2018-2023.toml` and whose
      command is `` `PYTHONPATH=src python3 -m byz.build` ``; move the
      materialiser row's label/patterns to `data/raw/repo/rp2005-2019/` and
      narrow its patterns to the two source prefixes plus its TOML;
      `HAND_MAINTAINED` loses `data/README.md` and `data/text/README.md` and
      gains `data/raw/repo/CONVENTIONS.md`; `HAND_MAINTAINED_DOCS` gains it too.
- [ ] `src/byz/contract/inventory.py` (111-118): the 13-entry `DOC_FILES` per
      R6.6.
- [ ] `PYTHONPATH=src python3 -m byz.build`; read all eight READMEs by eye;
      confirm the counts and the links.
- [ ] Green: `tests.curate.test_generated`, `test_data_docs`, `test_editions`,
      `test_layout`.

## Phase 4 - The conventions document (R7, D3)

### 4a. Red

- [ ] `tests/curate/test_layout.py` new `ConventionsDocumentTests`:
      - `data/raw/repo/CONVENTIONS.md` is a file; `data/text/README.md` is not;
      - it is in `generated.HAND_MAINTAINED` and
        `generated.HAND_MAINTAINED_DOCS`, is not matched by any
        `GENERATED_FILES` pattern, and does not start with the banner;
      - the preamble names both repo trees and says the document is not
        asserted for the print extracts (`data/raw/print/`);
      - anchors from Dr Robinson's prose are present verbatim: the six variant
        codes `N`/`B`/`C`/`M`/`S`/`E` with their names, the tense/voice/mood
        tables' first rows, the James 4:5 two-parsing example,
        `It is ASSUMED that all Strong's numbers are correct`, and
        "The Analytical Greek Lexicon";
      - every relative link resolves from `data/raw/repo/`.
- [ ] Extend `tests/curate/test_editions.py::PdfLinkTests` coverage list with
      the file (phase 3 already added it; keep it).
- [ ] Confirm the failure: the anchors exist today only in the moved file with
      the old relative depth.

### 4b. Green

- [ ] Rewrite `data/raw/repo/CONVENTIONS.md`:
      - new preamble (3 short paragraphs): scope (repo class), the two source
        folders that use it, the print class is not covered, the converter
        pointer, and a link to `../README.md`;
      - copy every line from the pre-change `data/text/README.md` starting at
        `## Variant codes` **verbatim**, except:
        - `The files in the \`CCAT\` folder` -> `The files in the \`ccat/\`
          folder`, same for `strongs/`;
        - the body carries no relative link (only the external 2009 parsing
          document), so no link depth changes there;
      - the preamble's relative links are written from `data/raw/repo/`
        (`../README.md`, `rp2018-2023/`, `rp2005-2019/`,
        `../../../docs/EDITIONS.md`);
      - drop the maintainer-authored framing paragraphs (which text the folder
        holds, "not a copy of the official files", the input/output rule, the
        PDFs-are-truth sentence): they belong to the generated
        `data/raw/repo/rp2018-2023/README.md` from phase 3. If phase 3 ran
        first, compare the wording and keep it there rather than duplicating
        it.
- [ ] Prove the preservation with an exact diff:

```bash
git show HEAD:data/text/README.md \
  | sed -n '/^## Variant codes$/,$p' > /tmp/opencode/conventions-body-before.md
sed -n '/^## Variant codes$/,$p' data/raw/repo/CONVENTIONS.md \
  > /tmp/opencode/conventions-body-after.md
diff -u /tmp/opencode/conventions-body-before.md \
        /tmp/opencode/conventions-body-after.md
```

  Expected: only the two `ccat/`/`strongs/` directory-name lines. Paste the
  diff in `validation.md`.
- [ ] `src/byz/beta/converter.py:111` points at `data/raw/repo/CONVENTIONS.md`.
- [ ] Green: `tests.curate.test_layout`, `test_data_docs`, `test_editions`.

## Phase 5 - Docs, `TECH.md`, and agent instructions (R8, R9.3)

### 5a. Red

- [ ] `tests/curate/test_editions.py::DocsTests`: `docs/EDITIONS.md` contains
      `## Where the inputs moved into the print and repo classes (2026-11-25)`,
      every `docs.INPUT_CLASS_MOVES` row, the "no compatibility shim" sentence,
      and the updated source feature matrix (`ccat`/`strongs` under
      `data/raw/repo/rp2018-2023/`).
- [ ] `tests/curate/test_editions.py::PdfLinkTests`
      `test_official_pdf_links_point_at_the_committed_files` (262-283): the
      expected hrefs gain `print/`.
- [ ] `tests/curate/test_layout.py::TechTests` needles: `data/raw/repo/`,
      `data/raw/print/`, `data/raw/repo/CONVENTIONS.md`, and a negative
      assertion for `data/text`.
- [ ] `tests/curate/test_current_pipeline.py::LegacyTreesAreGoneTests` (136-168)
      and `test_layout.RetiredLayoutSweepTests` (346-371): the new patterns and
      allowlist per R9.1; add the five-root absence test (phase 1a wrote it).
- [ ] `tests/curate/test_editions.py::RootReadmeTests` still compares `README.md`
      to the template render; it fails until the template changes.
- [ ] Confirm the failures: missing section/rows/needles.

### 5b. Green

- [ ] `src/byz/curate/docs.py`:
      - add `INPUT_CLASS_MOVES` next to `SNAPSHOT_MOVES` (159-180): one row per
        moved tree (13) plus the two consequences (`pdfs.toml` `path`, the
        manifest `pdf` key), all as `(old, new)` with code spans;
      - render `## Where the inputs moved into the print and repo classes
        (2026-11-25)` after the snapshot section, with the table, the statement
        that `data/text/` and the four old `data/raw/` roots are gone, that the
        bytes and hashes did not change, and that no shim exists;
      - update the 2026-11-21 `MOVED_PATHS` targets (`source/CCAT` ->
        `data/text/CCAT` stays as the historical step; add a sentence that
        `data/text/` itself moved on 2026-11-25);
      - `RETIRED_PATHS` line 85 (`data/text/README.md`) ->
        `data/raw/repo/CONVENTIONS.md`;
      - `SNAPSHOT_MOVES` row `data/text/` -> `data/raw/repo/rp2018-2023/`;
      - the source feature matrix (402-410), the intro (247-249, 297-317), the
        rebuild block (474-489, 599), the apparatus/notation prose (519, 580),
        and the `Source` paragraph (669-670) name the new paths.
- [ ] `src/byz/curate/README.template.md` per R8.1 (lines 17-23, 43-47, 67-93,
      147-163).
- [ ] `docs/BUILD.md` per R8.2 (sections 12-28, 30-61, 145-159).
- [ ] `data/provenance/pdfs.toml`: two `path` values gain `print/`.
- [ ] `SPECS/TECH.md` per R8.6: §2 (80-96), §3 (100-109), §5 (133-190), §7
      (222), §9 (280-283), §11 (310-323).
- [ ] `.opencode/**` per R8.7; `grep -rn 'data/text' .opencode` must be empty.
- [ ] `src/byz/contract/report.py` (75-78, 92-93, 127) and
      `src/byz/reconcile/report.py` (167, 196-198, 237-239, 300, 306, 365, 388,
      434, 495, 498, 501-502, 544): new paths and the two repo provenance
      records. `report.py` also gains the "two source classes" sentence in
      `docs/PROVENANCE.md`.
- [ ] Regenerate in the canonical order:

```bash
PYTHONPATH=src python3 -m byz.build
PYTHONPATH=src python3 -m byz.diff
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m byz.reconcile
PYTHONPATH=src python3 -m byz.contract   # refresh the baseline against the reconciled HISTORY
PYTHONPATH=src python3 -m byz.verify
```

- [ ] Green: `tests.curate.{test_editions,test_generated,test_layout,
      test_current_pipeline,test_data_docs}`, `tests.contract`,
      `tests.reconciliation`.

## Phase 6 - Regeneration, gates, determinism, suites (R10)

Run the canonical sequence above twice.

- [ ] `git status --porcelain` before accepting: only the 13 moves, the two
      provenance `extracted` edits, the new provenance TOML, the eight new
      READMEs, the edited `CONVENTIONS.md`, `pdfs.toml`, and the regenerated
      docs/reports/manifests. **Nothing** under `editions/*/{csv,tei}`.
- [ ] Byte gate (`validation.md` §3.1): the 672-file snapshot diff is silent.
- [ ] Artifact gate (`§3.2`): every manifest's `artifact_files` equals
      `/tmp/opencode/classes-manifest-<id>-before.json`; enumerate the changed
      top-level keys and confirm they are R5.4's subset.
- [ ] Data gate (`§3.3`): the 289 moved files hash to the same values, the six
      archives and two PDFs are unchanged, and the only existing-data edits are
      the three `extracted` lines.
- [ ] Diff gate (`§3.4`): each pair's `changes.csv`/`*.diff` files are byte
      identical; only the Notation line of each `report.md` and the Source prose
      of `reports/diffs/README.md` changed.
- [ ] Provenance gate: `rp2018-2023.toml` shape/hashes; `rp2005-2019.toml` only
      `extracted`; materialise and fetch idempotent.
- [ ] README gate: the eight files carry the banner, the skeleton, the counts,
      the links; the second run is byte identical.
- [ ] Retired-path gate: the sweep is green; `git grep -n -E
      'data/text/|data/raw/_archives/|data/raw/rp2005/|data/raw/rp2018/|data/raw/rp2005-2019/'`
      outside the allowlist is empty.
- [ ] No generated file contains a timestamp, host name, or absolute path:

```bash
git grep -n -E '/home/|localhost|/tmp/opencode' -- README.md docs reports editions data
```

  Expected: no output. (`2023-07-20` and commit hashes are recorded history,
  not run metadata.)
- [ ] The two-run determinism check: snapshot `README.md docs reports editions
      data/provenance data/raw` after run 1 and run 2; `diff` is silent and
      `git status` does not change.
- [ ] The three suites pass:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests/contract
PYTHONPATH=src python3 -m unittest discover -s tests/curate
PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation
```

- [ ] Commit, then regenerate and commit the follow-ups needed by the worktree
      tests: the change touches `editions/*/manifest.json` and `data/raw/repo`
      (`editions` and `data/raw/repo` are both in `CORPUS_PATHSPECS`), so expect
      the first follow-up to rewrite the manifests'
      `source_commit`/`strongs_commit`, the new provenance's commit fields,
      `reports/baseline/files.csv`, and `docs/HISTORY.md`; a second follow-up
      should touch `docs/HISTORY.md` only and converge. Record the actual number
      of follow-ups and the commit hashes in `validation.md`.
- [ ] Record every deviation in `validation.md` §12.3.

## Files changed

| File | Change |
| --- | --- |
| `data/raw/**` (13 moves, 289 files) | into `print/` and `repo/`; directory names per D8; bytes unchanged |
| `data/text/README.md` | moved to `data/raw/repo/CONVENTIONS.md`; re-scoped, prose intact |
| `data/README.md`, `data/raw/README.md`, `data/raw/print/README.md`, `data/raw/repo/README.md`, `data/raw/{print/rp2005,print/rp2018,repo/rp2005-2019,repo/rp2018-2023}/README.md` | **new**, generated by `byz.build` |
| `data/provenance/rp2018-2023.toml` | **new**, generated by `byz.build` |
| `data/provenance/{rp2005,rp2018}.toml` | `extracted` lines, re-recorded by `byz.fetch` |
| `data/provenance/rp2005-2019.toml` | `extracted` line, re-recorded by `byz.materialise` |
| `data/provenance/pdfs.toml` | two hand-edited `path` values |
| `src/byz/contract/paths.py` | new repo-class constants, dataset names, evidence |
| `src/byz/contract/history.py` | pathspecs and labels |
| `src/byz/contract/inventory.py` | the 13-entry `DOC_FILES` |
| `src/byz/contract/report.py` | `docs/DATA_CONTRACT.md` prose and JSON filenames follow the datasets |
| `src/byz/reconcile/sources.py` | `PRINT_DIR`, `REPO_DIR`, `ARCHIVE_DIR`, `FORMAT_DIRS` |
| `src/byz/reconcile/fetch.py` | extraction dir from the format; `extracted` record |
| `src/byz/reconcile/historical.py` | `CURRENT_STATE` |
| `src/byz/reconcile/compare.py`, `src/byz/reconcile/report.py` | path prose and labels |
| `src/byz/curate/editions.py` | registry paths, `input_class`, `revision`, notes |
| `src/byz/curate/materialise.py` | `HISTORICAL_INPUT_ROOT` |
| `src/byz/curate/build.py` | labels, `EXPORT_NOTES`, `_input_groups` prose, `_current_provenance_text` |
| `src/byz/curate/data_docs.py` | **new**: the eight input READMEs |
| `src/byz/curate/files.py` | `tracked_count` |
| `src/byz/curate/docs.py` | `INPUT_CLASS_MOVES`, sections, matrix, rebuild block |
| `src/byz/curate/diff.py` | `Source` prose |
| `src/byz/beta/converter.py` | the conventions pointer |
| `src/byz/build.py` | calls `data_docs.write_data_docs` |
| `src/byz/generated.py` | 26 generated Markdown, 13 registry rows, hand-maintained list |
| `src/byz/curate/README.template.md` | layout and prose |
| `docs/contract/data__text__CCAT.json`, `docs/contract/data__text__Strongs.json` | **deleted**; the contract writes the two new-named files |
| `docs/BUILD.md` | input tree, pipeline, report order |
| `SPECS/TECH.md` | §2, §3, §5, §7, §9, §11 |
| `.opencode/**` (10 files) | the new paths and the two classes |
| `README.md`, `docs/EDITIONS.md`, `docs/DATA_CONTRACT.md`, `docs/PROVENANCE.md`, `docs/HISTORY.md`, `docs/contract/*.json`, `reports/baseline/*`, `reports/reconciliation/*`, `reports/diffs/README.md`, `editions/*/manifest.json`, `editions/*/README.md` | regenerated |
| `tests/curate/{test_layout,test_integration,test_build,test_historical_pipeline,test_current_pipeline,test_fidelity,test_materialise,test_editions,test_generated}.py`, new `tests/curate/{test_data_docs,test_input_provenance}.py`, `tests/contract/{test_integration,test_coverage}.py`, `tests/reconciliation/{test_fetch,test_integration}.py` | the new tree, counts, labels, and guards |

## Guardrails

- Never use `cp`/`rm` for a move; `git mv` keeps history and stages the paths
  that `files.tracked_count` reads.
- Never edit an edition CSV/TEI to make a gate pass. A one-byte difference means
  a reader or a path is wrong.
- Never hand-edit `data/**/README.md` (except `CONVENTIONS.md`), the manifests,
  `docs/{EDITIONS,HISTORY,PROVENANCE,DATA_CONTRACT}.md`, `docs/contract/*.json`,
  or `reports/**`. Edit the renderer/template and regenerate.
- Never re-create `data/text/`, the old `data/raw/<edition>/` trees, or
  `data/raw/_archives/`, not even empty or as a symlink.
- Never make the generated READMEs read counts from a directory glob; pinned
  counts come from the manifests, auxiliary counts from `git ls-files`.
- Never let a print source README claim the repo conventions apply to it.
- Never run `byz.fetch --force`; do not touch `downloaded`, `final_url`, or
  `http_status`.
- Never add a dependency; the renderer and the provenance writer are standard
  library.
- Never edit `SPECS/` folders other than this one and `SPECS/TECH.md`.
