# Plan - Inputs out of the editions

Red/green TDD throughout (`SPECS/TECH.md` §10). Read `requirements.md` first;
`R1`-`R9` are the numbered requirements and `validation.md` is the merge gate.

This is a layout, provenance, and manifest change. `rp2005`, `rp2018`, and
`rp2018-2023` must stay byte-identical. `rp2005-2019` is **regenerated** from
its 2019 sources by the current pipeline (requirements Correction 2) and is
expected to change: the release's `{Ν`/`{Β` apparatus codes become
`{NA`/`{Byz`, typography is normalised, and the four blank verses are emitted.
If a non-historical CSV or TEI differs by one byte, stop and report; do not
adjust the edition.

The normal build becomes:

```bash
PYTHONPATH=src python3 -m byz.fetch --verify
PYTHONPATH=src python3 -m byz.build
PYTHONPATH=src python3 -m byz.diff
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m byz.reconcile
PYTHONPATH=src python3 -m byz.verify
```

`byz.materialise` is an ingest command, run only to restore the 57 source files
under `data/raw/rp2005-2019/` from tag `v2.0.3`. It is not in the normal
sequence and `byz.build` does not call it.

## Phase 0 - Preconditions and the before-snapshot

- [ ] Stay on `feature/2026-11-16-edition-recovery-curation`. Do not switch
      branches, commit, or revert.
- [ ] `git status --porcelain` is empty. At the time of writing the working tree
      had uncommitted documentation edits (`README.md`, `data/text/README.md`,
      `docs/EDITIONS.md`, `src/byz/curate/docs.py`, `src/byz/generated.py`, and
      four tests; `docs/RELEASE-NOTES.md` deleted). Commit or stash them first;
      the byte snapshot is meaningless against a dirty tree.
- [ ] Record the base commit:
      `git rev-parse HEAD` (the spec was written at `7fb28fe`) and the
      interpreter (`python3 --version`, `python3 -c "import beta_code"`).
- [ ] The history and tags are present:
      `git tag --list v2.0.3 v3.3.4` prints both, and
      `git rev-parse v2.0.3^{commit}` prints
      `8ec95671e463030347c2c643358eb56e58235b19`.
- [ ] Snapshot the edition outputs (672 files; **not** `source/`, which will be
      deleted). After the change, the 477 files of `rp2005`, `rp2018`, and
      `rp2018-2023` must match this snapshot; `rp2005-2019` is expected to
      differ:

```bash
find editions -type f \
  \( -path 'editions/*/csv/*' -o -path 'editions/*/tei/*' \) -print0 \
  | sort -z | xargs -0 sha256sum \
  > /tmp/opencode/byz-inputs-editions-before.sha256
wc -l /tmp/opencode/byz-inputs-editions-before.sha256    # 672
```

- [ ] Snapshot the manifests and the diff reports:

```bash
for id in rp2005 rp2005-2019 rp2018 rp2018-2023; do
  git show "HEAD:editions/$id/manifest.json" \
    > "/tmp/opencode/manifest-$id-before.json"
done
find reports/diffs -type f -print0 | sort -z | xargs -0 sha256sum \
  > /tmp/opencode/byz-inputs-diffs-before.sha256
```

- [ ] Snapshot every existing input and provenance file (the new historical tree
      must be the only addition):

```bash
find data/text data/raw/rp2005 data/raw/rp2018 data/raw/_archives \
     data/provenance -type f -print0 \
  | sort -z | xargs -0 sha256sum \
  > /tmp/opencode/byz-inputs-data-before.sha256
```

- [ ] Record the inventory: `git ls-files editions | wc -l` → **852**,
      `git ls-files 'editions/*/source/*' | wc -l` → **172**,
      `find editions -type f \( -path 'editions/*/csv/*' -o -path
      'editions/*/tei/*' \) | wc -l` → **672**,
      `git ls-files data/text | wc -l` → **57**.
- [ ] Capture the tag's prefixes for the later comparison (the input gate
      compares the two source prefixes; the four released prefixes are only
      checked against the edition's artifacts):

```bash
rm -rf /tmp/opencode/v203
mkdir -p /tmp/opencode/v203
git archive --format=tar v2.0.3 \
  textonly-beta-code parsed \
  csv-unicode/accents/no-variants csv-unicode/accents/with-variants \
  csv-unicode/no-accents tei-xml-unicode/no-accents \
  | tar -x -C /tmp/opencode/v203
find /tmp/opencode/v203 -type f | wc -l    # 170 (57 inputs, 113 outputs)
```

## Phase 1 - Materialise the 2019 source files (R2, D2/D7)

This phase only adds data. It does not change any edition byte. The 57
`textonly-beta-code` and `parsed` files are the inputs; the tag's 113 released
CSV/TEI are neither inputs nor the edition's outputs (Correction 2).

### 1a. Red

- [ ] Create `tests/curate/test_materialise.py` and delete the snapshot-only
      `tests/curate/test_recover.py`. The first tests:
      - `materialise_historical(dest_root=tmp)` creates exactly 57 files under
        `tmp/data/raw/rp2005-2019/` with the two source-prefix counts (30/27);
      - every file's SHA-256 equals `git archive v2.0.3` at the same path;
      - `tmp/data/provenance/rp2005-2019.toml` starts with
        `generated.toml_header()`, contains the tag and commit, `method`, two
        `[[prefixes]]` blocks, and one `[[files]]` block per file, sorted by
        `path`;
      - a second run writes no byte and exits 0;
      - a destination file with different bytes raises `SystemExit` naming the
        path and both hashes, and is not overwritten;
      - a stray extra file under `data/raw/rp2005-2019/` raises `SystemExit`;
      - a failed `git archive` leaves an existing tree untouched.
- [ ] Add the real-tree assertion in the same red step (it fails until the data
      exists): `data/raw/rp2005-2019/` has 57 files and
      `data/provenance/rp2005-2019.toml` exists.
- [ ] Confirm the failure is "No such file or directory" for
      `data/raw/rp2005-2019`, not an import error.

### 1b. Green

- [ ] Rename `src/byz/curate/recover.py` to `materialise.py` and add:

```python
HISTORICAL_TAG = "v2.0.3"
HISTORICAL_COMMIT = "8ec95671e463030347c2c643358eb56e58235b19"
# tag prefix -> data path under data/raw/rp2005-2019/, expected file count.
# Only the two source prefixes are inputs. The tag's released CSV/TEI are not
# read by any build path; `byz.build` regenerates the edition from these files.
PREFIX_MAP = (
    ("textonly-beta-code/", "textonly-beta-code/", 30),
    ("parsed/", "parsed/", 27),
)
HISTORICAL_INPUT_ROOT = "data/raw/rp2005-2019"
HISTORICAL_PROVENANCE = "data/provenance/rp2005-2019.toml"
```

  `_git_archive(tag, prefixes)` already exists and returns `{name: bytes}`.
  Add `materialise_historical(dest_root: Path | None = None)` that:
  - asserts the expected count for every `(tag_prefix, data_prefix, count)`
    and fails if a count is wrong;
  - computes the data-relative path by replacing the tag prefix with the data
    prefix;
  - writes each file with `Path.write_bytes` under
    `dest_root / HISTORICAL_INPUT_ROOT`, creating parents;
  - before writing, compares every existing file byte-for-byte and raises
    `SystemExit(f"{relpath}: existing bytes differ from {HISTORICAL_TAG}")`
    instead of overwriting; a stray extra file raises before any write; only
    after the whole destination validates are missing files written;
  - writes the provenance TOML (minimal writer, `method`, two `[[prefixes]]`
    blocks with `path`/`files`, sorted `[[files]]`, no timestamp) after the
    tree matches;
  - returns the destination path.
- [ ] Add `src/byz/curate/files.py` with `sha256_file(path)` (streamed) now;
      phase 2/3 extend it with `matching_files`. Switch the materialiser and
      `build._hash_tree` to it; do not duplicate the hash loop.
- [ ] Replace `src/byz/recover.py` with `src/byz/materialise.py`:

```python
def main() -> int:
    from .curate import materialise

    materialise.materialise_historical()
    print(f"materialised {materialise.HISTORICAL_INPUT_ROOT} (57 files)")
    print(f"wrote {materialise.HISTORICAL_PROVENANCE}")
    return 0
```

  Delete `src/byz/recover.py` and the old `recover_all` snapshot behaviour.
- [ ] Green: `PYTHONPATH=src python3 -m unittest tests.curate.test_materialise -v`.
- [ ] Run the real command:
      `PYTHONPATH=src python3 -m byz.materialise`.
- [ ] Prove the tree:

```bash
for p in textonly-beta-code parsed; do
  diff -r "/tmp/opencode/v203/$p" "data/raw/rp2005-2019/$p"
done
find data/raw/rp2005-2019 -type f | wc -l          # 57
```

- [ ] `git status --porcelain -- editions` is still empty (no edition changed).
- [ ] Do **not** add `data/raw/rp2005-2019/` to `reports/baseline/files.csv`; the
      contract inventories `data/text/`, not `data/raw/`.

## Phase 2 - Build from `data/` only (R3, D5/D9)

### 2a. Red

- [ ] `tests/curate/test_build.py`:
      - `build._input_groups(edition)` (to be added) returns roots under
        `data/` and never under `editions/` for all four editions;
      - the `_check_source_books` error message test names
        `data/text/CCAT`, not `editions/rp2018-2023/source/CCAT`
        (lines 88-104; replace `build.SNAPSHOT_DIR`).
- [ ] `tests/curate/test_current_pipeline.py`:
      - `BuildCurrentByteIdentityTests` (lines 39-57) creates a temp
        `csv/`/`tei/` target and calls `build.build_current(edition,
        edition_dir=target)` **without** copying a `source/` tree;
      - `test_build_current_is_idempotent` (58-75) does the same;
      - delete `SourceSnapshotFileSetTests` (100-157) and
        `test_edition_source_snapshot_equals_repository_source` (168-176);
      - keep `ViewCountTests` and the other `IdentityTests`.
- [ ] `tests/curate/test_integration.py`:
      - `test_edition_layout` (18-22) is covered by phase 4; for now assert the
        build reads `data/`;
      - `test_historical_recovery_matches_git` (55-77) reads
        `data/raw/rp2005-2019/textonly-beta-code/MT.CCT`;
      - `test_official_source_counts` (79-83) reads
        `editions.ROOT / edition["source_dir"]`;
      - delete `test_current_source_matches_working_tree` (85-95); it becomes a
        manifest assertion in phase 3.
- [ ] `tests/curate/test_current_pipeline.py` (retired-path sweep): allowlist
      `tests/curate/test_materialise.py` because it records the tag prefix
      mapping, and assert the sweep stays green with no `csv-unicode/` or
      `tei-xml-unicode/` in `editions/`, `data/`, or the manifests.
- [ ] Confirm the failures: `build_current` still raises
      `missing CCAT source directory: editions/rp2018-2023/source/CCAT`, and the
      diff loaders still read the snapshots.

### 2b. Green: registry and build paths

- [ ] `src/byz/curate/editions.py`:
      - `rp2005-2019` gains
        `"source_dir": "data/raw/rp2005-2019/textonly-beta-code"` and
        `"parsed_dir": "data/raw/rp2005-2019/parsed"`;
      - `rp2018-2023` gains
        `"source_dir": "data/text/CCAT"`,
        `"strongs_dir": "data/text/Strongs"`;
      - add a comment that every `source_dir` is an input under `data/`.
- [ ] `src/byz/curate/build.py`:
      - delete `SNAPSHOT_DIR = "source"` (line 72) and every use;
      - `EXPORT_NOTES["current"]` (lines 122-126) says "generated from the
        committed `data/text/` inputs";
      - `build_official` (616): `ccat_dir = editions.ROOT / edition["source_dir"]`,
        `ascii_dir = editions.ROOT / edition["ascii_dir"]`; add
        `edition_dir: Path | None = None`, resolve it once like
        `build_current` (713), and pass `edition_dir=target` to
        `write_accented_tei` (line 673);
      - `build_historical` (676): regenerate every view from
        `data/raw/rp2005-2019/` (requirements Correction 2):
        `csv/accented/{no-variants,with-variants}` from
        `textonly-beta-code/*.CCT` with `parse_cct_accented`;
        `csv/strongs/{with-parsing,no-parsing}` and `csv/unaccented` from
        `parsed/*.UB5` with `parse_parsed_ub5`; `tei/unaccented` from the
        unaccented text; `tei/accented` from `write_accented_tei`. Derive the
        `.UB5` segmentation reference from the accent-free, punctuation-free
        accented view generated from the same `.CCT`, not from a released
        `csv/unaccented`. Read no tag, copy no released CSV/TEI, and apply no
        MAR 16:8 correction; add `edition_dir`;
      - delete `_git_archive`, `HISTORICAL_ARTIFACT_PREFIXES`,
        `HISTORICAL_ARTIFACT_MAPPING`, `_copy_historical_artifacts`,
        `_correct_historical_apparatus_literals`, `SOURCE_VERSE_RE`, and
        `SOURCE_LITERAL_RE`; `write_manifest` takes the tag and commit from the
        registry (`editions.EDITIONS["rp2005-2019"]`), not `git rev-parse`;
      - `build_current` (703): `ccat_source = editions.ROOT /
        edition["source_dir"]`, `strongs_source = editions.ROOT /
        edition["strongs_dir"]`; labels are `data/text/CCAT` and
        `data/text/Strongs`; delete the `source/` docstring paragraphs
        (704-712, 722-725);
      - `_readme` (793): drop the `source/` layout row (820) and the "frozen
        copy" paragraph (831-833); replace the current-edition snapshot
        paragraph (835-847) with one sentence that `manifest.json` pins the
        inputs under `data/`;
      - `build_all` (908): remove `recover.recover_all()` (909) and
        `from . import recover` (14).
- [ ] Add view staging to `build_all`:
      - `_staging_views(edition_id)` creates
        `editions/.<id>.staging/{csv,tei}`;
      - build the edition into the staging dir;
      - `_swap_views(staging, final)` replaces `final/csv` and `final/tei`
        atomically enough: rename the old subdirectory to `.old`, `os.replace`
        the new one, remove `.old`; on failure restore the old;
      - remove the staging dir on any failure;
      - then `write_manifest` (which also writes the edition README).
      Add a test: a build that raises (for example a missing input directory)
      leaves the committed `csv/`/`tei/` hashes unchanged and no
      `.staging`/`.old` directory behind.
- [ ] `src/byz/curate/diff.py`:
      - `_load_official` (150): `editions.ROOT /
        editions.EDITIONS[edition_id]["source_dir"]`;
      - `_load_historical` (160): the same, with `source_dir` =
        `data/raw/rp2005-2019/textonly-beta-code`;
      - `_load_current` (170): `editions.ROOT /
        editions.EDITIONS[edition_id]["source_dir"]`.
- [ ] `src/byz/curate/files.py`: extend the phase 1 helper with
      `matching_files(root, includes)`; switch `build._hash_tree` and the
      materialiser to `sha256_file`.
- [ ] Remove `from . import recover` from `build.py`; the deleted MAR helper is
      gone, and `build.py` imports nothing from `materialise`.

### 2c. Regenerate and check

- [ ] `PYTHONPATH=src python3 -m byz.build`.
- [ ] `git status --porcelain -- editions` shows `manifest.json` and
      `README.md`, the regenerated `rp2005-2019` views, and no other edition
      CSV/TEI (the old `source/` is still present, untouched).
- [ ] Byte gate: re-run the phase 0 `find … sha256sum` and diff against
      `byz-inputs-editions-before.sha256`. The 477 files of `rp2005`, `rp2018`,
      and `rp2018-2023` are silent; the 195 `rp2005-2019` files differ.
- [ ] `reports/diffs` changes only for `rp2005--rp2005-2019` and
      `rp2005-2019--rp2018` after `PYTHONPATH=src python3 -m byz.diff`; the
      source-tier counts are unchanged.
- [ ] `byz.verify` does not exist yet; use
      `tests/curate/test_fidelity.py::ManifestIntegrityTests` (it still reads
      `source_files` at this point, so it will fail until phase 3; that is
      expected and is the phase 3 red).

## Phase 3 - Manifest `inputs` and `byz.verify` (R4, R5, D3/D4/D8)

### 3a. Red

- [ ] Rewrite `tests/curate/test_fidelity.py::ManifestIntegrityTests` (208-229):
      - `source_files` is absent; `inputs` is present;
      - each group's actual `matching_files(ROOT / root, include)` equals its
        `files` set;
      - each file's `sha256`/`size` matches;
      - `artifact_files` resolves against the edition directory, and the actual
        `csv/`+`tei/` set equals the manifest set.
- [ ] Add `tests/curate/test_verify.py`:
      - clean tree: `verify.verify_all()` returns no errors, and
        `verify.main([]) == 0`;
      - a tiny temporary root with one input and one artifact verifies clean;
      - corrupting the input file's hash yields an error containing the
        edition, the path, `sha256 expected`, and the actual hash;
      - corrupting an artifact file yields the same for the artifact;
      - deleting an artifact yields a `missing` error; adding an extra file
        under `csv/` yields an `unexpected` error;
      - adding an extra matching input file yields an `unexpected` error;
      - a manifest with `source_files` and no `inputs` is rejected;
      - `../` or an absolute path in `root`/`path` is rejected;
      - `main(["no-such-edition"]) == 2`;
      - `--edition-dir` on a copied edition verifies artifacts and says inputs
        were skipped;
      - the command writes nothing (hash the temp tree before and after).
- [ ] Confirm the failures: `KeyError: 'inputs'` / `ModuleNotFoundError:
      byz.verify`.

### 3b. Green: manifest

- [ ] `src/byz/curate/build.py` add `_input_groups(edition)` returning
      `(root, includes)` pairs per "Manifest schema":
      - official: `(source_dir, ("*.CCT",))`,
        `(ascii_dir, ("*_Byz.txt",))`;
      - historical: `("data/raw/rp2005-2019", ("textonly-beta-code/*.CCT",
        "parsed/*.UB5"))`;
      - current: `(parent of source_dir, (f"{source_dir.name}/*.TXT",
        f"{strongs_dir.name}/*.BP5"))`.
- [ ] Add `_input_tree(edition)`:
      - for each group, `matching_files(ROOT / root, include)`;
      - fail if a group matches no file;
      - fail if `root` is absolute, contains `..`, is not under `data/`, or is
        under `editions/`;
      - build `{"root": root, "include": sorted(includes),
        "files": [{"path": rel, "sha256": …, "size": …} for rel in sorted(...)]}`;
      - sort groups by `(root, include)`.
- [ ] `write_manifest` (864): replace `"source_files": _hash_tree(root /
      "source", root)` (877) with `"inputs": _input_tree(edition)`; keep
      `artifact_files` unchanged.
- [ ] Inspect one manifest:
      `python3 -m json.tool editions/rp2005-2019/manifest.json | head -60` and
      confirm `root` is `data/raw/rp2005-2019`, the include list has two
      globs, and the 57 paths are `textonly-beta-code/...` or `parsed/...`.

### 3c. Green: `byz.verify`

- [ ] `src/byz/curate/verify.py`:
      - `class VerificationError(Exception)` carrying `edition`, `path`,
        `expected`, `actual`, `kind`;
      - `load_manifest(edition_dir)`: validate the shape (types, 64-hex
        `sha256`, non-negative `size`, relative POSIX paths, no `..`, no
        absolute, `source_files` absent, `inputs` non-empty,
        `artifact_files[].path` starts with `csv/` or `tei/`); reject a
        `root`/`include`/`path` containing `..`, an absolute prefix, or a
        backslash; do not require the directory basename to equal the manifest
        `edition` (that check is repo-mode only);
      - `verify_inputs(manifest, root=ROOT)`: for each group, resolve
        `root / group["root"]`, check it is under `data/` and not under
        `editions/`, compare `matching_files` to `files`, hash and size;
      - `verify_artifacts(manifest, edition_dir)`: compare
        `matching_files(edition_dir, ("csv/**/*", "tei/**/*"))` to
        `artifact_files`, hash and size;
      - `verify_pdf(manifest, root=ROOT)` when `pdf_sha256` is present;
      - `verify_edition(edition_id, *, edition_dir=None, root=None)` returns a
        list of `VerificationError` (empty on success);
      - `verify_all(edition_ids=None, *, edition_dir=None, root=None)` returns
        `(checked, failures)` and prints one `OK`/`FAIL` line per edition plus
        the summary;
      - `main(argv=None)` parses `editions` and `--edition-dir`, validates the
        ids against `editions.EDITIONS`, maps usage errors to exit 2, and
        returns 0/1.
- [ ] `src/byz/verify.py`:

```python
"""Verify the curated editions against their manifests.

run: PYTHONPATH=src python3 -m byz.verify [edition ...] [--edition-dir PATH]
"""

import sys


def main(argv=None) -> int:
    from .curate import verify

    return verify.main(argv)


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] `src/byz/generated.py`: add the materialiser row (phase 5, but do it now
      so the README registry test is green at the end of this phase):
      - remove the `editions/<edition>/source/` row (87-94);
      - add this row, keeping the registry at 12 rows:

```python
{
    "label": "`data/raw/rp2005-2019/`, `data/provenance/rp2005-2019.toml`",
    "command": "`PYTHONPATH=src python3 -m byz.materialise`",
    "patterns": (
        "data/raw/rp2005-2019/**",
        "data/provenance/rp2005-2019.toml",
    ),
},
```

- [ ] `PYTHONPATH=src python3 -m byz.build` (writes the new manifests).
- [ ] `PYTHONPATH=src python3 -m byz.verify`; expect exit 0 and
      `226 inputs, 672 artifacts`.
- [ ] Byte gate again (all 672 files unchanged). Manifest gate:
      `artifact_files` equal to the before snapshot for every edition; the only
      changed keys are `source_files` (removed) and `inputs` (added).
- [ ] Test a corrupted input without touching the repo:
      use the temp-tree test, and in `validation.md` §5 do the scratch-clone
      manual check.

## Phase 4 - Delete the snapshots and retire the old recovery code (R1, R6)

### 4a. Red

- [ ] `tests/curate/test_layout.py`:
      - add `EditionLayoutTests.test_editions_contain_only_outputs`: for each
        edition, `sorted(p.name for p in root.iterdir()) ==
        ["README.md", "csv", "manifest.json", "tei"]` and `source` is absent;
      - add `test_no_tracked_file_under_editions_source`:
        `git ls-files 'editions/*/source/*'` is empty;
      - update `InputTreeTests.test_current_edition_readme_names_the_repository
        _input_tree` (148-155) to assert the README names `data/` and
        `manifest.json`, not the snapshot;
      - `EntryPointTests.test_entry_points_are_modules_with_main` (169-172)
        adds `verify`;
      - `TechTests` (248-254) asserts `SPECS/TECH.md` has no
        `editions/<edition>/source` and no recovery-before-build wording.
- [ ] Confirm `tests/curate/test_recover.py` is gone (phase 1 replaced it with
      `test_materialise.py`). Keep the "failed archive keeps the existing tree"
      test; drop the official/current snapshot file-set tests and
      `_copy_data_files` tests.
- [ ] `tests/curate/test_integration.py`:
      - `test_edition_layout` (18-22) drops `"source"`;
      - `test_manifests` (24-31) asserts `manifest["inputs"]`;
      - `test_official_source_counts` (79-83) reads
        `editions.ROOT / edition["source_dir"]`;
      - `test_historical_recovery_matches_git` reads
        `data/raw/rp2005-2019/textonly-beta-code/MT.CCT`.
- [ ] Confirm the failures: `source` still exists; `manifest["inputs"]` raises
      KeyError; `byz.verify` import is fine but the layout tests fail.

### 4b. Green

- [ ] `git rm -r editions/rp2005/source editions/rp2005-2019/source
      editions/rp2018/source editions/rp2018-2023/source` (172 files).
- [ ] `src/byz/curate/materialise.py`: delete `_staging`, `_swap`, `_recover`,
      `recover_official`, `recover_current`, `recover_all`, and
      `_copy_data_files`. Keep `_git_archive`, the two source prefixes,
      `materialise_historical`, and the TOML writer. Delete
      `src/byz/recover.py`.
- [ ] `src/byz/curate/build.py` no longer imports the materialiser; it already has the
      moved MAR helper and reads `data/`.
- [ ] `tests/curate/test_fidelity.py::DashGuardTests`
      `test_official_ccat_main_text_has_no_attached_dashes` (182-192) reads
      `editions.ROOT / editions.EDITIONS[edition_id]["source_dir"]`.
- [ ] `tests/curate/test_fidelity.py::HistoricalArtifactTests` (426-546):
      - split the target helper: source names (`textonly-beta-code/...`,
        `parsed/...`) resolve under `ROOT/"data/raw/rp2005-2019"/name`; the
        artifact names keep the edition prefix-to-view mapping;
      - `test_bytes_match` compares the data tree for source names and the
        edition for artifact names;
      - add `test_manifest_pins_the_historical_inputs`: the manifest's
        historical `files` set equals the 57 source files and every hash
        matches.
- [ ] `tests/curate/test_build.py` message labels are `data/text/CCAT`.
- [ ] `tests/curate/test_current_pipeline.py` has no snapshot tests.
- [ ] `tests/curate/test_editions.py` `test_lists_every_root_directory`
      (130-138) keeps the `source/`/`scripts/` negative assertions.
- [ ] `tests/curate/test_generated.py`:
      - registry count stays 12;
      - rename `test_registry_lists_the_two_generated_tomls_and_not_pdfs` to
        `test_registry_lists_the_generated_tomls_and_not_pdfs` and assert
        `data/provenance/rp2005-2019.toml` is present.
- [ ] Green: `tests.curate.test_layout`, `test_materialise`, `test_fidelity`,
      `test_integration`, `test_build`, `test_current_pipeline`,
      `test_editions`, `test_generated`.
- [ ] `PYTHONPATH=src python3 -m byz.build`; confirm no `source/` reappears and
      the 672 CSV/TEI files are still unchanged.

## Phase 5 - Docs, TECH.md, and agent instructions (R7, R8, D10)

### 5a. Red

- [ ] `tests/curate/test_layout.py`:
      - `test_no_tracked_file_names_the_removed_layout` gains the needle
        `editions/<id>/source` (a regex such as
        `editions/[a-z0-9-]+/source/`) with `docs/EDITIONS.md`,
        `src/byz/curate/docs.py`, `tests/curate/test_layout.py`, and any test
        that asserts the snapshot is gone allowlisted;
      - `TechTests` asserts §5 has `data/raw/rp2005-2019/`, `byz.verify`, and
        no `editions/<edition>/source`.
- [ ] `tests/curate/test_editions.py::DocsTests`:
      - `docs/EDITIONS.md` contains
        `## Where the edition snapshots went (2026-11-25)`, every
        `docs.SNAPSHOT_MOVES` row, and the self-verification sentence;
      - the "Rebuilding" block has `byz.verify` and no recovery command;
      - `docs/BUILD.md` has `byz.verify`, `--edition-dir`, and the manifest
        schema explanation.
- [ ] `tests/curate/test_generated.py` asserts the new registry row and the
      README render.
- [ ] `tests/curate/test_editions.py::RootReadmeTests` still compares
      `README.md` to the template render; it fails until the template and
      registry are updated.
- [ ] Confirm the failures: missing section/rows/commands.

### 5b. Green

- [ ] `src/byz/curate/docs.py`:
      - replace the snapshot prose (237-241) with the new section sentinel;
      - add `SNAPSHOT_MOVES` next to `MOVED_PATHS` with rows:
        | retired snapshot | now |
        | `editions/rp2005/source/ccat/` | `data/raw/rp2005/editions-rp2-ccat/` |
        | `editions/rp2005-2019/source/textonly-beta-code/` | `data/raw/rp2005-2019/textonly-beta-code/` |
        | `editions/rp2005-2019/source/parsed/` | `data/raw/rp2005-2019/parsed/` |
        | `editions/rp2018/source/ccat/` | `data/raw/rp2018/rp2018-ccat/` |
        | `editions/rp2018-2023/source/` | `data/text/` |
        | `manifest.json` `source_files` | `manifest.json` `inputs` |
        plus a sentence that the tag's released CSV/TEI are not inputs and are
        not read by the build: `rp2005-2019` is regenerated from the 57 sources,
        correcting the apparatus codes and typography. A sentence that an
        edition is outputs only and `byz.verify` checks it against `data/`;
      - "Layout, exports, and verification" (350-365): each edition has
        `csv/`, `tei/`, `manifest.json`, `README.md`; inputs under `data/`;
      - "Rebuilding" (474-489): drop the recovery command; add `byz.verify`;
        add the one-time `byz.materialise` note;
      - the 2026-11-21 moved-paths sentence (283-290): `artifact_files`
        unchanged; `source_files` replaced by `inputs` on 2026-11-25;
      - the source feature matrix (297-306): note the committed
        `data/raw/rp2005-2019/` copy;
      - `_curated_editions_section` (603-631): remove "own input snapshot" and
        say the manifest pins the `data/` inputs.
- [ ] `src/byz/generated.py`: ensure the phase 3 registry row is present; no
      other row names `source/`.
- [ ] `src/byz/curate/README.template.md`:
      - layout table rows `data/`, `editions/`, `src/` (67, 71);
      - sequence and prose (133-148, 180-191);
      - remove the old recovery command from the normal sequence;
      - add `byz.verify` to the sequence and the `src/` row.
- [ ] `data/text/README.md` (line 9): replace the snapshot-distinction
      paragraph.
- [ ] `docs/BUILD.md`: sections 12-56, 125-136 per R8.3; add "Verifying the
      editions".
- [ ] `SPECS/TECH.md`: §2, §3, §5, §8, §9, §11 per R8.6.
- [ ] `.opencode/agents/{build,code-reviewer,plan,spec-implementer,verifier}.md`,
      `.opencode/commands/read-conventions.md`, and
      `.opencode/skills/{feature-specification,fix-typing-linting-issues,
      investigate-bug,write-tests}/SKILL.md`: replace "recover then build" with
      "build reads data/; verify checks; materialise only restores the
      historical inputs".
- [ ] `src/byz/reconcile/report.py`: add the `docs/PROVENANCE.md` sentence
      pointing at `data/raw/rp2005-2019/` and its provenance.
- [ ] `src/byz/contract/paths.py` `DERIVATION_EVIDENCE` (100-115) and
      `src/byz/contract/report.py` (75-81): data-only wording.
- [ ] Regenerate the generated docs:
      `PYTHONPATH=src python3 -m byz.build`,
      `PYTHONPATH=src python3 -m byz.contract`,
      `PYTHONPATH=src python3 -m byz.reconcile`,
      `PYTHONPATH=src python3 -m byz.contract` (the history order).
- [ ] Green: `tests.curate.test_editions`, `test_generated`, `test_layout`,
      `tests.contract`, `tests.reconciliation`.

## Phase 6 - Regeneration, gates, determinism, and suites (R9)

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

- [ ] `git status --porcelain` before accepting: expected changes are the
      deleted `editions/*/source/`, the four manifests and READMEs, the
      regenerated `rp2005-2019` CSV/TEI, the new `data/raw/rp2005-2019/` and
      `data/provenance/rp2005-2019.toml`, the regenerated `README.md`,
      `docs/**`, `reports/**`, and the code/test edits. **Nothing** under the
      `csv/` or `tei/` of the other three editions.
- [ ] Byte gate (`validation.md` §3.1): re-run the phase 0 `find … sha256sum`
      and `diff` it against `byz-inputs-editions-before.sha256`. The 477
      non-historical files are silent; the 195 `rp2005-2019` files differ, as
      Correction 2 requires. 672 files before and after.
- [ ] Artifact gate (`§3.2`): compare the `artifact_files` list from
      `/tmp/opencode/manifest-<id>-before.json` with the regenerated manifest;
      equal for `rp2005`, `rp2018`, and `rp2018-2023`, regenerated for
      `rp2005-2019`. The only changed top-level keys are `source_files`
      (removed) and `inputs` (added); `rp2005-2019` also changes `basis` and
      `note`.
- [ ] Data gate (`§3.3`): re-run the data snapshot; the only differences are
      the edited `data/text/README.md` and the additions
      `data/raw/rp2005-2019/**` and `data/provenance/rp2005-2019.toml`. No
      existing `.TXT`/`.BP5` or archive/PDF/provenance file differs.
- [ ] Diff gate: only the two pairs that include `rp2005-2019` differ from
      `byz-inputs-diffs-before.sha256`.
- [ ] Historical gate: no with-variants file has a Greek code initial, the view
      carries `{NA`/`{Byz`, the accented main text matches the release's words
      after normalising `¶`/apostrophes, and the four blank verses are empty
      records.
- [ ] Historical input gate: compare each data prefix to its tag prefix as in
      phase 1; 57 files; provenance has 57 entries.
- [ ] `byz.verify` exits 0 and reports `verified 4 editions (226 inputs, 672
      artifacts)`.
- [ ] Run the whole sequence a second time; `git diff --binary` from run 1 and
      run 2 are identical (`cmp`), and `git status --porcelain` does not change.
- [ ] No generated file contains a timestamp, hostname, or absolute path:

```bash
git grep -n -E '/home/|localhost|/tmp/opencode' -- README.md docs reports editions data
```

  Expected: no output. (The generated `data/provenance/rp2005-2019.toml` has
  the commit and hashes, not a run time.)
- [ ] The three suites pass:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests/contract
PYTHONPATH=src python3 -m unittest discover -s tests/curate
PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation
```

- [ ] Commit the change. Then regenerate and commit the follow-ups needed by
      the worktree tests: the first follow-up rewrites the manifests, the
      contract baseline, and `docs/HISTORY.md`; because `editions` is in
      `CORPUS_PATHSPECS`, the recorded "Last corpus commit" moves to that
      follow-up, so a second regeneration commit updates `docs/HISTORY.md` only
      and converges. Re-run the suites after the last commit; record the exact
      number of follow-ups in `validation.md`.
- [ ] Record every deviation from this plan in `validation.md` §10.

## Files changed

| File | Change |
| --- | --- |
| `src/byz/curate/editions.py` | input directories for all four editions; tag/commit registry metadata; regenerated `rp2005-2019` basis/note |
| `src/byz/curate/build.py` | data-only build paths; `_input_groups`, `_input_tree`; view staging; `build_historical` regenerates every view; tag/copy/MAR code deleted; README prose; no `recover` import |
| `src/byz/curate/materialise.py` | renamed from `recover.py`; `materialise_historical` + `_git_archive` + TOML writer; snapshot/copy functions deleted |
| `src/byz/curate/files.py` | **new**: `sha256_file`, `matching_files` |
| `src/byz/curate/verify.py` | **new**: manifest validation, input/artifact verification, CLI |
| `src/byz/curate/diff.py` | source tier from `editions.ROOT / edition["source_dir"]` |
| `src/byz/curate/docs.py` | `SNAPSHOT_MOVES`; layout/verification prose; rebuild block; curated section; 2026-11-21 note |
| `src/byz/generated.py` | replace the snapshot row with the materialiser row; registry stays 12 |
| `src/byz/materialise.py` | **new** entry point; prints the materialised data tree, not edition paths |
| `src/byz/verify.py` | **new** thin entry point |
| `src/byz/contract/paths.py` | data-only `DERIVATION_EVIDENCE` |
| `src/byz/contract/report.py` | `docs/DATA_CONTRACT.md` prose names `data/` inputs |
| `src/byz/reconcile/report.py` | `docs/PROVENANCE.md` historical-input pointer |
| `src/byz/curate/README.template.md` | layout, sequence, recover/verify prose |
| `data/text/README.md` | input-vs-output paragraph |
| `docs/BUILD.md` | input tree, pipeline, verify section, materialisation wording |
| `SPECS/TECH.md` | §2, §3, §5, §8, §9, §11 |
| `.opencode/**` (10 files) | build/verify/recover roles |
| `data/raw/rp2005-2019/**` | **new** 57 source files, generated by `byz.materialise` |
| `data/provenance/rp2005-2019.toml` | **new**, generated |
| `editions/*/source/**` | **deleted** (172 files) |
| `editions/*/manifest.json` | `source_files` → `inputs`; `artifact_files` unchanged for three editions and regenerated for `rp2005-2019` |
| `editions/*/README.md` | generated: outputs-only prose |
| `README.md`, `docs/EDITIONS.md`, `docs/DATA_CONTRACT.md`, `docs/PROVENANCE.md`, `docs/contract/*.json`, `reports/baseline/*` | regenerated |
| `reports/diffs/*` | regenerated; only the two pairs that include `rp2005-2019` change |
| `tests/curate/test_historical_pipeline.py` | **new**: regeneration byte identity, apparatus codes, blank verses, release-word regression, input pin |
| `tests/curate/test_materialise.py` | **new**, replaces `test_recover.py` |
| `tests/curate/test_recover.py` | **deleted**; materialiser coverage lives in `test_materialise.py` |
| `tests/curate/test_verify.py` | **new** |
| `tests/curate/test_fidelity.py` | manifest inputs; historical source paths from `data/`; blank verses and literals |
| `tests/curate/test_current_pipeline.py` | no snapshot; build reads `data/text` |
| `tests/curate/test_integration.py` | edition layout, manifest inputs, data source counts, historical identity, diff samples |
| `tests/curate/test_build.py` | `_input_groups`; data labels |
| `tests/curate/test_layout.py` | outputs-only editions; no `editions/*/source`; TECH/verify |
| `tests/curate/test_editions.py` | docs sections, rebuild block, README |
| `tests/curate/test_generated.py` | registry row; toml test rename |
| `tests/curate/test_reproducible.py` | drop the old recovery step from `GENERATORS`; add a `byz.verify` assertion |

## Guardrails

- Never recreate `editions/<edition>/source/`, not even empty, as a symlink, or
  as a `.gitkeep`.
- Never hand-edit `editions/*/manifest.json`, `editions/*/README.md`,
  `README.md`, `docs/EDITIONS.md`, `docs/DATA_CONTRACT.md`,
  `docs/PROVENANCE.md`, `docs/contract/*.json`, or `reports/**`. Edit the
  generator and regenerate.
- Never edit an edition CSV/TEI to make a gate pass. If a non-historical view
  differs, the input path is wrong; if `rp2005-2019` differs from a fresh
  `build_historical`, the reader, book mapping, or segmentation reference is
  wrong.
- Never read git tag `v2.0.3` outside `byz.materialise`. `byz.build` must not
  call `git archive` and must not copy a released artifact.
- Never overwrite a conflicting `data/raw/rp2005-2019/` file silently. The
  materialiser fails; the maintainer decides.
- Never add `source_files` back, and never write both `source_files` and
  `inputs`.
- Never let an `inputs[].root` be absolute, contain `..`, be under `editions/`,
  or be outside `data/`.
- Never add `byz.materialise` to the normal build sequence; `byz.build` must
  run without it.
- Never run `byz.fetch --force`; do not touch `data/provenance/rp2005.toml` or
  `rp2018.toml`.
- Never add a dependency; `byz.verify` is standard library only.
- Never touch `SPECS/` folders other than this one and `SPECS/TECH.md`.
