# Plan - Inputs under `data/`, code under `src/`, outputs under `editions/`

Red/green TDD throughout (`SPECS/TECH.md` §10). This is a move plus generated
documentation: no text, archive, PDF, CSV, TEI, or manifest-hash change.
`requirements.md` `R1`-`R8` are the numbered requirements; `validation.md` is the
merge gate.

Read `requirements.md` first. The only hand edits are `data/text/README.md`,
`docs/BUILD.md` (new), `docs/RELEASE-NOTES.md`, `SPECS/TECH.md`,
`src/byz/curate/README.template.md` (new), and `.opencode/**`. Everything else
under `docs/`, `reports/`, `editions/`, and `README.md` is written by its own
generator.

## The move table

Every row is a `git mv` unless it says otherwise. Bytes are unchanged except
where "content edit" is noted.

| From | To | Count | Content change |
| --- | --- | ---: | --- |
| `source/CCAT/*.TXT` | `data/text/CCAT/*.TXT` | 29 | none |
| `source/Strongs/*.BP5` | `data/text/Strongs/*.BP5` | 27 | none |
| `source/README.md` | `data/text/README.md` | 1 | links `../../`, converter pointer, snapshot distinction (R1.7) |
| `scripts/fetch_official.py` | `src/byz/fetch.py` | 1 | rewritten as a module entry point |
| `scripts/recover_editions.py` | `src/byz/recover.py` | 1 | rewritten as a module entry point |
| `scripts/build_editions.py` | `src/byz/build.py` | 1 | rewritten as a module entry point |
| `scripts/diff_editions.py` | `src/byz/diff.py` | 1 | rewritten as a module entry point |
| `scripts/beta_to_unicode_custom/beta_to_unicode_custom.py` | `src/byz/beta/converter.py` | 1 | logic identical; shebang dropped |
| `scripts/beta_to_unicode_custom/__init__.py` | `src/byz/beta/__init__.py` | 1 | one-line package docstring |
| `scripts/tei_xml_header.xml` | `src/byz/curate/tei_xml_header.xml` | 1 | none |
| `scripts/requirements.txt` | `requirements.txt` | 1 | none (`beta-code==1.0.0`) |
| `scripts/README.md` | `docs/BUILD.md` | 1 | rewritten for the new commands and layout (R5.1) |
| `README.md` (hand-written body) | `src/byz/curate/README.template.md` | — | **new file**; `README.md` is regenerated from it (D3) |
| — | `src/byz/curate/README.template.md` | 1 | new |
| `docs/contract/source__CCAT.json` | `docs/contract/data__text__CCAT.json` | 1 | regenerated (name derives from the dataset) |
| `docs/contract/source__Strongs.json` | `docs/contract/data__text__Strongs.json` | 1 | regenerated |

Directories that disappear: `source/` and `scripts/` (the latter after all nine
tracked files move). Delete the untracked
`scripts/beta_to_unicode_custom/__pycache__/` with the directory; never move it.

Not moved, and this is the point of D1: `editions/<edition>/source/` stays.
Every manifest's `source_files[].path` is relative to the edition root
(`source/CCAT/01_MAT.TXT`), so those 56 strings are correct before and after.

## Files changed

| File | Change |
| --- | --- |
| `src/byz/contract/paths.py` | `DATA_TEXT`, `CCAT_DIR`, `BP5_DIR`, `CCAT_DATASET`, `BP5_DATASET`; drop `SOURCE` and `SCRIPTS_DIR`; `DERIVATION_EVIDENCE` prose (R1.2, R3.2) |
| `src/byz/contract/inventory.py` | `_specs()` dataset names from `paths`; drop the `scripts` row (line 44); `DOC_FILES` (lines 112-118) (R1.3, R3.2) |
| `src/byz/contract/contracts.py` | `DATASET_CONTRACTS` keys at lines 37, 53 use the dataset constants (R1.3) |
| `src/byz/contract/coverage.py` | `COMPARISONS` left-hand names (lines 7-24) (R1.3) |
| `src/byz/contract/invariants.py` | invariant table keys (lines 27, 32) (R1.3) |
| `src/byz/contract/bp5.py`, `ccat.py` | default `dataset=` arguments use the constants (R1.2) |
| `src/byz/contract/history.py` | `DATASETS` labels + dual pathspecs; `CORPUS_PATHSPECS` (lines 12-36) (R1.6) |
| `src/byz/contract/derivation.py` | source globs use `paths.CCAT_DIR` / `paths.BP5_DIR` (lines 27, 36) (R1.2) |
| `src/byz/contract/report.py` | `_contract_doc` prose (lines 75-76, 92, 127) names `data/text/` and `src/byz/`; no `scripts/` (R1.3, R7.4) |
| `src/byz/curate/build.py` | `_buc()` loses the `sys.path` hack (197-200); TEI header via `Path(__file__)` (518); `_last_commit` pathspecs (715, 722, 873-874); `generated_by` (861); `_readme`/`EXPORT_NOTES`/docstrings (R1.8, R2.3, R6.3) |
| `src/byz/curate/recover.py` | `_beta_converter()` loses the hack (35-39); `recover_current()` reads `paths.CCAT_DIR`/`BP5_DIR` (271-286) (R1.4, R2.3) |
| `src/byz/curate/docs.py` | template renderer replaces `BEGIN`/`END`/`root_readme_block`/`replace_block`; `MOVED_PATHS` section; four command strings (9-10, 375-383, 493-568) (R4, R5.2) |
| `src/byz/curate/diff.py` | `README_TEXT` command (527) (R5.4) |
| `src/byz/curate/editions.py` | the `rp2018-2023` note's path names (102-106) (R1.8) |
| `src/byz/generated.py` | drop `BLOCK_MARKER`/`block_banner()`; `README.md` into `GENERATED_MARKDOWN`; `HAND_MAINTAINED`; all `GENERATED_FILES` commands (R3.2, R4.4, R4.5) |
| `src/byz/fetch.py`, `recover.py`, `build.py`, `diff.py` | **new** entry points (R2.1) |
| `src/byz/beta/__init__.py`, `converter.py` | **new** home of the converter (R2.2) |
| `src/byz/curate/tei_xml_header.xml` | **moved** byte-for-byte (R2.4) |
| `src/byz/curate/README.template.md` | **new** template (R4.1) |
| `requirements.txt` | **moved** from `scripts/` (R2.5) |
| `data/text/**` | **moved** from `source/`; `README.md` content edit (R1.1, R1.7) |
| `docs/BUILD.md` | **new** hand-written build reference (R5.1) |
| `docs/RELEASE-NOTES.md` | one new dated entry (R5.3) |
| `docs/EDITIONS.md` | generated: `MOVED_PATHS` section, `data/text/` prose, new commands (R1.8, R5.2, R5.4) |
| `docs/DATA_CONTRACT.md`, `docs/HISTORY.md`, `docs/PROVENANCE.md` | regenerated (R1.3) |
| `docs/contract/*.json` | two stale files deleted, two new written (R1.3) |
| `editions/*/README.md` | `rp2018-2023`: one sentence now names `data/text/`; the other three unchanged (R6.4) |
| `editions/*/manifest.json` | `generated_by` in all four; `source_commit`/`strongs_commit` in `rp2018-2023` (R6.3) |
| `reports/baseline/*`, `reports/reconciliation/*`, `reports/diffs/*` | regenerated (R1.3, R5.4) |
| `README.md` | regenerated from the template (R4.2) |
| `source/`, `scripts/` | **deleted** (R1.1, R3.1) |
| `SPECS/TECH.md` | §2, §5, §7, §9, §11 (R7.1, R7.2) |
| `.opencode/**` (10 files) | input tree, entry points, docs paths (R7.3) |
| `tests/curate/test_layout.py` | **new**: layout locks + sweep (R3.3, R8.2) |
| `tests/curate/test_editions.py` | `ROOT_ITEMS`; `RootReadmeTests`; `DocsTests`; `PdfLinkTests._user_docs` (R3, R4.7, R5) |
| `tests/curate/test_generated.py` | 17 → 18 banner files; `HAND_MAINTAINED`; drop `test_block_banner…`; `ReportingDocsTests` reads `docs/BUILD.md` (R4.4, R5.1) |
| `tests/curate/test_reproducible.py` | `GENERATORS` become `-m byz.*` (R3.4) |
| `tests/curate/test_current_pipeline.py` | `ROOT/"source"` → `paths.CCAT_DIR`/`BP5_DIR`; scripts deletion test; requirements path (R3.5) |
| `tests/curate/test_fidelity.py` | `ROOT/"source"` → constants (lines 168-172); comments (R1) |
| `tests/curate/test_build.py` | converter import test (R2.2, R2.3) |
| `tests/contract/test_integration.py` | dataset literals, `data/text/` prefix, state fixtures (R1.3) |
| `tests/contract/test_coverage.py` | fixture dataset names (R1.3) |
| `tests/reconciliation/test_integration.py` | `current` path, `--force` message, history labels (R1.5) |

## Phase 0 - Preconditions and the before-snapshot

- [ ] Stay on `feature/2026-11-16-edition-recovery-curation`. Do not switch
      branches, commit, or revert.
- [ ] `git status --porcelain` is empty; record it:
      `git status --porcelain > /tmp/opencode/byz-layout-before.txt`.
- [ ] Python environment with `beta-code` importable:
      `python3 -c "import beta_code"`. Record the interpreter in
      `validation.md` §11.
- [ ] Full history and tags: `git tag --list v2.0.3 v3.3.4` prints both.
- [ ] Snapshot the edition bytes:

```bash
find editions -type f \
  \( -path 'editions/*/source/*' -o -path 'editions/*/csv/*' \
     -o -path 'editions/*/tei/*' \) -print0 \
  | sort -z | xargs -0 sha256sum > /tmp/opencode/byz-layout-editions-before.sha256
```

- [ ] Snapshot the manifest **hash lists**, which is the gate R6.2 compares:

```bash
for id in rp2005 rp2005-2019 rp2018 rp2018-2023; do
  git show "HEAD:editions/$id/manifest.json" > "/tmp/opencode/manifest-$id-before.json"
done
```

- [ ] Record the three keys that R6.3 allows to change, per edition:

```bash
git show HEAD:editions/rp2018-2023/manifest.json | grep -E 'generated_by|source_commit|strongs_commit'
```

  Expected today: `"generated_by": "python3 scripts/build_editions.py"`,
  `source_commit = 16859b2…` (last commit touching `source/CCAT`),
  `strongs_commit = b7485a3…` (last commit touching `source/Strongs`).
- [ ] Record the tracked inventory:
      `git ls-files scripts | wc -l` → 9, `git ls-files source | wc -l` → 57,
      `wc -l reports/baseline/files.csv` → 219 (218 rows + header).
- [ ] Remove the untracked `scripts/beta_to_unicode_custom/__pycache__/` before
      the move so it cannot travel with the directory.

## Phase 1 - `source/` → `data/text/` (R1)

This phase changes no edition artifact. If `git status -- editions` shows
anything but generated READMEs, stop.

### 1a. Red: layout and dataset tests

- [ ] Create `tests/curate/test_layout.py` with the R1 locks first:

```python
class InputTreeTests(unittest.TestCase):
    def test_repository_inputs_live_under_data_text(self):
        self.assertTrue((ROOT / "data" / "text").is_dir())
        self.assertFalse((ROOT / "source").exists())
        self.assertEqual(len(list((ROOT / "data" / "text" / "CCAT").glob("*.TXT"))), 29)
        self.assertEqual(len(list((ROOT / "data" / "text" / "Strongs").glob("*.BP5"))), 27)

    def test_contract_uses_the_data_text_dataset_names(self):
        self.assertEqual(paths.CCAT_DATASET, "data/text/CCAT")
        self.assertEqual(paths.BP5_DATASET, "data/text/Strongs")
        self.assertEqual(set(contracts.DATASET_CONTRACTS) & {"data/text/CCAT", "data/text/Strongs"},
                         {"data/text/CCAT", "data/text/Strongs"})

    def test_history_keeps_the_pre_move_evidence(self):
        labels = dict(history.DATASETS)
        self.assertIn("data/text/CCAT", labels)
        self.assertIn("source/CCAT", labels["data/text/CCAT"])
```

- [ ] Update `tests/contract/test_integration.py` in the same red step:
      `"source/CCAT"` → `"data/text/CCAT"`, `"source/Strongs"` →
      `"data/text/Strongs"` (lines 33-34, 46, 62-63, 106-107), and
      `test_dataset_names_live_in_the_current_edition`'s skip prefix becomes
      `"data/text/"`.
- [ ] Update `tests/contract/test_coverage.py:22`'s fixture name.
- [ ] Update `tests/reconciliation/test_integration.py:37` to
      `data/text/CCAT/01_MAT.TXT` and the history fixtures at lines 216-237:
      `"current data/text/CCAT"` for the two current rows; keep
      `"v3.0.0 source/CCAT"` (path inside the tag).
- [ ] Confirm the failures: `data/text` missing, `KeyError: 'data/text/CCAT'`,
      dataset set mismatch.

### 1b. Green: move and repoint

- [ ] `git mv source data/text`.
- [ ] `src/byz/contract/paths.py`:

```python
# The authoritative Beta-code inputs, beside the official archive inputs.
DATA_TEXT = ROOT / "data" / "text"
CCAT_DIR = DATA_TEXT / "CCAT"
BP5_DIR = DATA_TEXT / "Strongs"
CCAT_DATASET = "data/text/CCAT"
BP5_DATASET = "data/text/Strongs"
```

  Delete `SOURCE` and `SCRIPTS_DIR`. Update `DERIVATION_EVIDENCE` (lines 96-110)
  to say `data/text/CCAT` / `data/text/Strongs`, and the "Number ->
  abbreviation" comment stays pointing at `build.py`.
- [ ] `inventory._specs()` (lines 14-15): `(paths.CCAT_DATASET, paths.CCAT_DIR,
      "*.TXT", "ccat")` and `(paths.BP5_DATASET, paths.BP5_DIR, "*.BP5", "bp5")`.
- [ ] `contracts.DATASET_CONTRACTS` (lines 37, 53), `coverage.COMPARISONS`
      (7, 12, 17, 22), `invariants` (27, 32), `bp5.validate` default (20),
      `ccat.validate` default (62) use the two constants.
- [ ] `derivation.py` (27, 36): `sorted(paths.CCAT_DIR.glob("*.TXT"))` and
      `sorted(paths.BP5_DIR.glob("*.BP5"))`.
- [ ] `recover.recover_current()` (271-286): `paths.CCAT_DIR` / `paths.BP5_DIR`
      instead of `editions.ROOT / "source" / …`.
- [ ] `reconcile/compare.py` `source_rows()` (148-159) and the Strong's rows
      (343-351) use `paths.CCAT_DIR` / `paths.BP5_DIR`; `compare.py` already
      imports `from byz.contract import paths`.
- [ ] `reconcile/historical.py`:

```python
# State labels shown in docs/PROVENANCE.md and reports/reconciliation/.
# The historical label names the path as it exists inside tag v3.0.0; the
# current label names the working-tree path after the 2026-11-21 move.
V3_STATE = "v3.0.0 source/CCAT"
CURRENT_STATE = "current data/text/CCAT"
```

  `STATE_SPECS[1]["state"] = V3_STATE`, `_load_source()` keeps
  `f"source/CCAT/{num}_{abbr}.TXT"` (inside the tag), `_load_current()` uses
  `paths.CCAT_DIR`, `evidence()` sets `states[CURRENT_STATE]`.
- [ ] `reconcile/report.py` (294-295) looks up `historical.CURRENT_STATE`; the
      prose at 167, 237-238, 357, 380, 425, 486, 531 names `data/text/`; the
      sentence at 299 says "the current text (`data/text/CCAT`) was first added
      in commit `97371d7` as `source/CCAT`" using
      `historical.V3_STATE`'s path segment, not a new literal.
- [ ] `contract/history.py`: labels and dual pathspecs per R1.6; add
      `data/text` to `CORPUS_PATHSPECS` and keep `source`.
- [ ] `contract/report.py` prose (75-76, 92, 127) names `data/text/` and
      `src/byz/`.
- [ ] `curate/build.py` `_last_commit("source/CCAT")` (873) →
      `_last_commit("source/CCAT", "data/text/CCAT")`; same for `Strongs` (874);
      update the comment at 871-872 and the `build_current` docstring (693-696).
      Source labels at 715/722 are only error context for the edition snapshot;
      leave them naming the snapshot (`source/CCAT` inside the edition) and add
      a comment that these are the edition's own paths.
- [ ] `curate/docs.py` prose (6 sites) and `editions.py:102-106` note.
- [ ] `data/text/README.md`: links `../../editions`, `../../docs/EDITIONS.md`;
      add the snapshot-distinction sentence (D1, R1.7).
- [ ] `src/byz/generated.py` `HAND_MAINTAINED`: `source/README.md` →
      `data/text/README.md`.
- [ ] Tests: `test_fidelity.py` (168-172) and `test_current_pipeline.py`
      (104-118) use `paths.CCAT_DIR`/`paths.BP5_DIR` or
      `ROOT/"data"/"text"`.
- [ ] Green: `PYTHONPATH=src python3 -m unittest tests.contract.test_integration
      tests.contract.test_coverage tests.curate.test_layout -v`.

### 1c. Regenerate and check

- [ ] `PYTHONPATH=src python3 -m byz.contract`; it writes the two new
      `docs/contract/data__text__*.json` files. Delete the two stale
      `docs/contract/source__*.json`.
- [ ] `PYTHONPATH=src python3 -m byz.reconcile`.
- [ ] `git status -- editions` shows only `editions/*/README.md` and
      `editions/*/manifest.json`.
- [ ] `git diff -- editions/rp2018-2023/manifest.json` shows only
      `source_commit`/`strongs_commit` (and `generated_by` once phase 3 lands).
      Every `path`/`sha256`/`size` pair is unchanged; compare with
      `/tmp/opencode/manifest-rp2018-2023-before.json`.

## Phase 2 - The converter moves into the package (R2.2, R2.3)

### 2a. Red

- [ ] `tests/curate/test_build.py`:

```python
class ConverterPackageTests(unittest.TestCase):
    def test_converter_lives_in_the_package(self):
        from byz.beta import converter
        self.assertTrue(hasattr(converter, "convert_beta_to_unicode_strongs"))

    def test_build_and_recover_use_the_package_converter(self):
        self.assertEqual(build._buc().__name__, "byz.beta.converter")
        self.assertEqual(recover._beta_converter().__name__, "byz.beta.converter")

    def test_no_library_module_manipulates_sys_path(self):
        for path in sorted((ROOT / "src").rglob("*.py")):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("sys.path", text, str(path))
```

- [ ] Confirm it fails with `ModuleNotFoundError: byz.beta` and on `sys.path`
      in `build.py`/`recover.py`.

### 2b. Green

- [ ] `mkdir -p src/byz/beta`; `git mv
      scripts/beta_to_unicode_custom/beta_to_unicode_custom.py
      src/byz/beta/converter.py`; `git mv
      scripts/beta_to_unicode_custom/__init__.py src/byz/beta/__init__.py`.
- [ ] Write `src/byz/beta/__init__.py` as `"""Beta-code to Unicode conversion."""`
      (replace the 1-byte file).
- [ ] Drop the shebang from `converter.py`; do not touch any other line.
- [ ] `build.py`:

```python
def _buc():
    """Return the package's Beta-code converter (imported lazily)."""
    from byz.beta import converter
    return converter
```

  Remove `import sys` from `build.py` and `recover.py` if it becomes unused
  (it is used only by the deleted hacks in both files; confirm with
  `grep -n 'sys\.' src/byz/curate/build.py src/byz/curate/recover.py`).
  `recover.py` `_beta_converter()` gets the same body.
- [ ] Update the docstring at `build.py:300` ("`beta_to_unicode_custom` module")
      and `recover.py:35`.
- [ ] Green: the three new tests, then `tests.curate.test_build`,
      `tests.curate.test_recover`, `tests.curate.test_current_pipeline`.
- [ ] Prove the outputs are untouched: no generator has run yet; the unit tests
      convert in memory.

## Phase 3 - Entry points, root files, and deleting `scripts/` (R2, R3)

### 3a. Red

- [ ] Extend `tests/curate/test_layout.py`:

```python
class EntryPointTests(unittest.TestCase):
    def test_scripts_directory_is_gone(self):
        self.assertFalse((ROOT / "scripts").exists())
        self.assertEqual(subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "scripts"],
            capture_output=True, text=True, check=True).stdout.strip(), "")

    def test_entry_points_are_modules_with_main(self):
        for name in ("fetch", "recover", "build", "diff"):
            module = importlib.import_module(f"byz.{name}")
            self.assertTrue(callable(module.main), name)

    def test_root_files_moved(self):
        self.assertTrue((ROOT / "requirements.txt").is_file())
        self.assertFalse((ROOT / "scripts" / "requirements.txt").exists())
        self.assertTrue((ROOT / "docs" / "BUILD.md").is_file())
        self.assertFalse((ROOT / "scripts" / "README.md").exists())

    def test_tei_header_is_package_data(self):
        self.assertTrue((ROOT / "src" / "byz" / "curate" / "tei_xml_header.xml").is_file())
```

- [ ] `tests/curate/test_reproducible.py` `GENERATORS` → the five `-m` entries
      (R3.4). It will fail until the modules exist.
- [ ] `tests/curate/test_generated.py`: 18 banner files; `HAND_MAINTAINED_DOCS`
      three entries; delete `test_block_banner_names_the_command_and_partial_generation`;
      `ReportingDocsTests.setUp` reads `docs/BUILD.md`.
- [ ] Confirm: `byz.fetch` etc. are missing, `scripts/` still exists,
      `requirements.txt` missing.

### 3b. Green: the four entry points

Each file follows `src/byz/contract/__main__.py`'s shape. Example
`src/byz/build.py`:

```python
"""Rebuild every curated edition. Run: PYTHONPATH=src python3 -m byz.build"""

import sys


def main() -> int:
    from .curate import build, docs

    manifests = build.build_all()
    print(f"built {len(manifests)} editions")
    print(f"wrote {docs.write_editions_doc()}")
    print(f"updated {docs.update_root_readme()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- `src/byz/recover.py` prints `recovered {path}` per edition.
- `src/byz/diff.py` prints `wrote {path}` per report.
- `src/byz/fetch.py`:

```python
"""Fetch and checksum the official archives. Run: PYTHONPATH=src python3 -m byz.fetch"""

import sys


def main(argv=None) -> int:
    from .reconcile.fetch import main as fetch_main

    return fetch_main(argv)


if __name__ == "__main__":
    sys.exit(main())
```

The lazy imports keep `beta_code` optional until a conversion runs, exactly as
`_buc()` does today.

### 3c. Green: the moves and the deletion

- [ ] `git mv scripts/tei_xml_header.xml src/byz/curate/tei_xml_header.xml`;
      `build.py:518` becomes
      `(Path(__file__).with_name("tei_xml_header.xml")).read_text(encoding="utf-8")`.
- [ ] `git mv scripts/requirements.txt requirements.txt`.
- [ ] `git mv scripts/README.md docs/BUILD.md` and rewrite per R5.1 in phase 5.
- [ ] `git rm scripts/fetch_official.py scripts/recover_editions.py
      scripts/build_editions.py scripts/diff_editions.py`.
- [ ] `rmdir scripts` (after the two subdirectories are empty) and delete the
      untracked `__pycache__`.
- [ ] `paths.SCRIPTS_DIR` removed; `inventory.py:44` row removed; `DOC_FILES`
      (112-118) becomes the five entries in R3.2.
- [ ] `generated.GENERATED_FILES`: update every `command` to the new module
      commands; replace the README-block row with the `README.md` row (R4.5).
- [ ] `curate/docs.py:375-383`: the four commands become
      `PYTHONPATH=src python3 -m byz.fetch --verify`, `… -m byz.recover`,
      `… -m byz.build`, `… -m byz.diff`.
- [ ] `curate/diff.py:527`, `reconcile/report.py:352`, `contract/report.py:92`,
      `reconcile/report.py`'s reproduce block → new commands.
- [ ] `tests/reconciliation/test_integration.py:24` message →
      `PYTHONPATH=src python3 -m byz.fetch --force`.
- [ ] Green: `test_layout`, `test_generated`, `test_reproducible` (the latter
      only after a clean worktree at `HEAD`; see `validation.md` §8).

## Phase 4 - The README becomes generated (R4)

### 4a. Red

- [ ] Rewrite `tests/curate/test_editions.py::RootReadmeTests` (R4.7). The new
      setUp reads both files:

```python
def setUp(self):
    self.path = editions.ROOT / "README.md"
    self.text = self.path.read_text(encoding="utf-8")
    self.template = (editions.ROOT / "src" / "byz" / "curate"
                     / "README.template.md").read_text(encoding="utf-8")

def test_readme_equals_the_template_render(self):
    self.assertEqual(
        self.text,
        generated.markdown(docs.render_root_readme(self.template)),
    )
```

- [ ] Add `test_readme_starts_with_the_generated_banner`,
      `test_readme_has_no_block_markers`, and the negative `source`/`scripts`
      assertions in `test_lists_every_root_directory`.
- [ ] `tests/curate/test_layout.py`:

```python
class ReadmeTemplateTests(unittest.TestCase):
    def setUp(self):
        self.template = (
            ROOT / "src" / "byz" / "curate" / "README.template.md"
        ).read_text(encoding="utf-8")

    def test_template_is_hand_maintained_and_banner_free(self):
        self.assertIn("src/byz/curate/README.template.md", generated.HAND_MAINTAINED)
        self.assertNotIn("README.md", generated.HAND_MAINTAINED)
        self.assertFalse(self.template.startswith(generated.MARKDOWN_MARKER))

    def test_template_tokens_are_known_and_used_once(self):
        tokens = re.findall(r"\{\{([A-Z_]+)\}\}", self.template)
        self.assertEqual(sorted(tokens), ["CURATED_EDITIONS", "GENERATED_FILES"])
        self.assertEqual(sorted(docs.TEMPLATE_TOKENS), sorted(tokens))
```

- [ ] Confirm failures: `docs.render_root_readme` still expects the block
      markers, `README.md` still carries them, the template is missing, and
      `README.md` is still in `HAND_MAINTAINED`.

### 4b. Green: the template

- [ ] Copy the current hand-written README body into
      `src/byz/curate/README.template.md` with these changes:
      - first line the template note (R4.3);
      - `[`source/`](source/)` → `[`data/text/`](data/text/)` and the "Edit or
        convert the text" row points at `data/text/` and `docs/BUILD.md`;
      - layout table: drop `source/` and `scripts/`; `data/` and `src/`
        descriptions updated; `docs/` lists `BUILD.md`;
      - `source/CCAT`/`source/Strongs` → `data/text/…` (two places);
      - "Which text should I use?" → `data/text/`;
      - "Reproducing the curated data" → `pip install -r requirements.txt` and
        the six `PYTHONPATH=src python3 -m byz.*` commands;
      - `[`scripts/README.md`](scripts/README.md)` → `[`docs/BUILD.md`](docs/BUILD.md)`;
      - the two placeholder lines, each alone on a line, where the
        `## Curated editions` and `## Generated files` sections go.
- [ ] `src/byz/curate/docs.py`:

```python
TEMPLATE_PATH = editions.ROOT / "src" / "byz" / "curate" / "README.template.md"
TEMPLATE_NOTE = (
    "<!-- Template for README.md: edit this file, then run "
    "PYTHONPATH=src python3 -m byz.build. -->"
)
TEMPLATE_TOKENS = ("CURATED_EDITIONS", "GENERATED_FILES")
```

  `render_root_readme(template: str) -> str` asserts the first line is
  `TEMPLATE_NOTE`, drops it, replaces each `{{TOKEN}}` line with the
  rendered section, raises `ValueError` naming the offending token or the file
  on an unknown/duplicate/missing token, and returns the body **without** the
  banner. `update_root_readme()` writes it with `generated.write_markdown`.
- [ ] Reuse the existing table code: `root_readme_block()` becomes
      `_curated_editions_section()` and `_generated_files_section()`; delete
      `BEGIN`, `END`, `replace_block`, and the banner lines from the block.
- [ ] `generated.py`: delete `BLOCK_MARKER` (line 20) and `block_banner()`
      (206-213); add `README.md` to `GENERATED_MARKDOWN` (18 entries); remove
      it from `HAND_MAINTAINED` and add
      `src/byz/curate/README.template.md`; update the module docstring
      ("The root README is only partially generated" is no longer true).
- [ ] Green: `tests.curate.test_editions`, `tests.curate.test_generated`,
      `tests.curate.test_layout`.

## Phase 5 - Docs, `.opencode/`, TECH.md, release note (R5, R7)

### 5a. Red

- [ ] `tests/curate/test_editions.py::DocsTests`:

```python
def test_editions_doc_maps_every_moved_path(self):
    text = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
    self.assertIn("## Where the code and inputs moved (2026-11-21)", text)
    for old, new in docs.MOVED_PATHS:
        self.assertIn(old, text)
        self.assertIn(new, text)

def test_release_notes_document_the_move(self):
    text = (editions.DOCS_DIR / "RELEASE-NOTES.md").read_text(encoding="utf-8")
    self.assertIn("2026-11-21", text)
    self.assertIn("PYTHONPATH=src python3 -m byz.build", text)
    self.assertIn("no shim", text)

def test_build_doc_names_the_new_commands(self):
    text = (editions.DOCS_DIR / "BUILD.md").read_text(encoding="utf-8")
    for verb in ("fetch", "recover", "build", "diff", "contract", "reconcile"):
        self.assertIn(f"python3 -m byz.{verb}", text)
    self.assertIn("pip install -r requirements.txt", text)
```

- [ ] `test_layout.py`:

```python
def test_tech_md_describes_the_current_layout(self):
    text = (ROOT / "SPECS" / "TECH.md").read_text(encoding="utf-8")
    for needle in ("data/text/", "python -m byz.", "requirements.txt"):
        self.assertIn(needle, text)
    self.assertNotIn("scripts/", text)
    self.assertNotIn("source/CCAT", text)
```

- [ ] Delete `test_scripts_readme_has_no_retired_converter`; its replacement is
      `test_build_doc_has_no_retired_converter` over `docs/BUILD.md`.
- [ ] Confirm the doc tests fail on missing files/sections.

### 5b. Green

- [ ] `src/byz/curate/docs.py` `MOVED_PATHS` (separate from `RETIRED_PATHS`)
      with one row per line of the move table in `requirements.md`
      ("Breaking changes"), and `## Where the code and inputs moved
      (2026-11-21)` rendered after the 2026-11-19 section, with the "bytes and
      hashes did not change" sentence and the release-note link.
- [ ] `docs/RELEASE-NOTES.md`: one dated entry per R5.3, listing the old
      commands as removed with no shims, the new commands, the doc moves, and
      a link to the canonical table.
- [ ] `docs/BUILD.md`: the `scripts/README.md` content rewritten per R5.1, plus
      "Editing the root README" (D3) and the moved library files.
- [ ] `SPECS/TECH.md` §2, §5, §7, §9, §11 per R7.1-R7.2. In §5 the layout block
      gains `data/text/` under `data/`, drops `scripts/`, and lists
      `requirements.txt`; the trailing paragraph describes the module entry
      points and cites this spec.
- [ ] `.opencode/**` (10 files) per R7.3. Sweep with the same patterns as R8.1.
- [ ] `PdfLinkTests._user_docs()` gains `data/text/README.md` and
      `docs/BUILD.md`.
- [ ] Green: `tests.curate.test_editions`, `tests.curate.test_generated`,
      `tests.curate.test_layout`.

## Phase 6 - Full regeneration, byte identity, determinism (R6, R8)

Run from the repository root, in this order:

```bash
PYTHONPATH=src python3 -m byz.fetch --verify
PYTHONPATH=src python3 -m byz.recover
PYTHONPATH=src python3 -m byz.build
PYTHONPATH=src python3 -m byz.diff
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m byz.reconcile
PYTHONPATH=src python3 -m byz.contract     # history is written by two commands
```

- [ ] `git status --porcelain` before accepting: the expected changes are
      `README.md`, `data/text/README.md`, `docs/**`, `reports/**`,
      `editions/*/README.md`, the four `manifest.json`, the source tree rename,
      the deleted `scripts/`, and the code/test edits. **Nothing** under
      `editions/*/source`, `editions/*/csv`, `editions/*/tei`.
- [ ] Byte gate: re-run the phase 0 `find … sha256sum` and
      `diff /tmp/opencode/byz-layout-editions-before.sha256 -` is silent
      (`validation.md` §3).
- [ ] Hash-list gate: compare `source_files` + `artifact_files` from
      `/tmp/opencode/manifest-<id>-before.json` with the regenerated manifests;
      only `generated_by`, `source_commit`, `strongs_commit` may differ
      (`validation.md` §3.2).
- [ ] Run the whole sequence a second time; `git diff --binary` from run 1 and
      run 2 are identical (`cmp`), and `git status --porcelain` does not change.
- [ ] Three suites pass (`validation.md` §9).
- [ ] Commit the change, then regenerate and commit the known **first**
      follow-up: the regenerated manifests, `reports/baseline/files.csv`, and
      `docs/HISTORY.md`. Regenerate and commit the **second** follow-up for
      `docs/HISTORY.md` only. Two are needed because the first follow-up
      touches `editions/*/manifest.json`, and `editions` is in
      `CORPUS_PATHSPECS` (`src/byz/contract/history.py`), so the recorded
      "Last corpus commit" moves to that follow-up; the second regeneration
      records it and converges. Re-run the suites afterwards;
      `test_reproducible.py` and `ContractWorktreeTests` only pass against a
      committed `HEAD`.
- [ ] Record every deviation from this plan in `validation.md` §11.

## Guardrails

- Never edit `README.md` by hand after phase 4; edit the template and re-render.
- Never rewrite `editions/<edition>/source/` to `data/text/`. The edition
  snapshot is an output; the repository input tree is an input.
- Never hand-edit an edition CSV/TEI or a manifest hash to make a gate pass.
- Never add a shim for `scripts/…`, a symlink, or a `.gitkeep`.
- Never add a retired-layout reference outside the R8.2 allowlist, including in
  a comment or an f-string used as an error message.
- Never run `byz.fetch --force`; do not touch `data/provenance/`.
- Never touch `SPECS/2026-11-21-diff-categories/`.
- Never add `pandas`, `numpy`, or a packaging file; `beta-code==1.0.0` is the
  only dependency.
