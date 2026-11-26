# Requirements - Inputs under `data/`, code under `src/`, outputs under `editions/`

## Context

The repository says its model is **sources -> pipeline -> editions**, and after
`SPECS/2026-11-19-retire-legacy-unicode-trees/` the pipeline really is one chain.
The *folder layout* is still the old one, and it tells three different stories
about where an input lives:

```
today
  source/            <- the authoritative Beta-code inputs
  data/raw/          <- the same kind of thing: official inputs
  data/provenance/   <- metadata about inputs
  scripts/           <- entry points; the library imports *from here*
  src/byz/           <- the library
  editions/          <- outputs
```

Three problems:

1. **Two homes for inputs.** `source/` sits beside `data/` although it is one
   more input tree. A reader has to learn that `data/raw/` is input, `source/` is
   input, and that the difference is historical rather than meaningful.
2. **The dependency points the wrong way.** `src/byz/curate/build.py` and
   `src/byz/curate/recover.py` rewrite `sys.path` so they can import a module
   that lives in `scripts/`. The library depends on the CLI directory, which is
   the exact inversion this repository removed once already for the edition
   views. `scripts/*.py` compensate by inserting `src/` into `sys.path`.
3. **The root README is only half generated.** Its `<!-- editions:begin -->` …
   `<!-- editions:end -->` block is rendered; everything around it is
   hand-written prose that names `source/`, `scripts/`, and the old commands. The
   banner has to say "the rest of this README is hand-written", and no test can
   prove that the prose describes the tree it ships with.

This change moves the folders so the layout matches the model, and makes the
README a first-class generated artifact:

```
after
  data/
    text/CCAT/*.TXT          <- accented Beta-code inputs (was source/CCAT)
    text/Strongs/*.BP5       <- parsed inputs           (was source/Strongs)
    text/README.md           <- the conventions          (was source/README.md)
    raw/...                  <- official archives and extracts
    provenance/*.toml
  src/byz/
    beta/converter.py        <- the Beta-code wrapper   (was scripts/beta_to_unicode_custom/)
    curate/tei_xml_header.xml<- TEI header template     (was scripts/tei_xml_header.xml)
    fetch.py recover.py build.py diff.py                <- entry points (was scripts/*.py)
  editions/<id>/source/      <- per-edition frozen snapshot (unchanged)
  requirements.txt           <- beta-code==1.0.0        (was scripts/requirements.txt)
  README.md                  <- rendered from src/byz/curate/README.template.md
```

This is a move/rename of code and inputs plus generated documentation. No text,
archive, PDF, CSV, TEI, or manifest *hash* changes. The one place where the
"no manifest content change" rule and the move are in direct conflict is
recorded in **R6** and **"Decision required: manifest metadata"** below.

## Goal

1. One input tree: `data/`, with `data/text/` for the authoritative Beta-code
   files and `data/raw/` for the official archive inputs. No top-level `source/`.
2. One Python package: `src/byz/`, with entry points as
   `PYTHONPATH=src python3 -m byz.<verb>` and no `scripts/` directory. The
   library imports nothing from a CLI directory.
3. One generated README: the whole file is rendered from a template owned by the
   generator, carries the full-file generated banner, and cannot drift from the
   registry and the manifests.
4. Prove with a hard gate that every edition artifact is unchanged, and that a
   second full regeneration is byte-identical.
5. Leave no tracked file that tells a reader to use a path that no longer
   exists, except the documented old-to-new table and the git-history pathspecs.

## Non-goals

- No change to any file under `data/raw/`, `data/provenance/`, `essay/`, any
  PDF, or any archive.
- No change to `editions/*/csv/**`, `editions/*/tei/**`, or
  `editions/*/source/**` bytes. The edition CSV/TEI remain byte-identical, and
  every `source_files` / `artifact_files` entry in every manifest keeps the same
  `path`, `sha256`, and `size`.
- No renaming of `editions/<edition>/source/`. It is a different thing from the
  repository input tree (see D1) and renaming it would rewrite 852 manifest
  entries and every edition README for no user benefit.
- No new packaging (`pyproject.toml`, `pip install -e .`, console scripts). The
  `PYTHONPATH=src` prefix already used by `byz.contract` and `byz.reconcile` is
  the documented mechanism for all six commands. Installable packaging is a
  separate change.
- No shim scripts, symlinks, redirect READMEs, or `.gitkeep` for `source/` or
  `scripts/`. Both directories are gone.
- No change to the `editions/` edition model, dataset set, or report figures.
  `csv/unaccented` remains outside the contract (`SPECS/2026-11-19-…` R5.3).
- No edit to `SPECS/2026-11-21-diff-categories/` (a concurrent spec) or to any
  other `SPECS/` folder except this one and `SPECS/TECH.md`.
- No re-download (`byz.fetch --force` is not used) and no change to
  `data/provenance/`.
- No reflow or content rewrite of the README prose beyond the path and command
  corrections this change requires.

## Affected scope

- **Editions:** all four, but only through generated documentation. Their
  `csv/`, `tei/`, and `source/` bytes and their manifest hash lists are
  unchanged; `editions/rp2018-2023/README.md` changes one sentence (it names the
  repository input tree), and three manifest keys change (R6).
- **Inputs touched:** `source/` is moved to `data/text/`. Its 57 files are read
  exactly as today. `data/text/README.md` gets path corrections only.
- **Outputs touched:** the root `README.md` (now fully generated),
  `docs/EDITIONS.md`, `docs/DATA_CONTRACT.md`, `docs/HISTORY.md`,
  `docs/PROVENANCE.md`, `docs/contract/*.json`, `reports/baseline/*`,
  `reports/reconciliation/*`, `reports/diffs/*`, `editions/*/README.md`, and
  every `editions/*/manifest.json`.
- **Hand-written files edited directly:** `data/text/README.md`,
  `docs/BUILD.md` (new), `docs/RELEASE-NOTES.md`, `SPECS/TECH.md`,
  `src/byz/curate/README.template.md` (new), `.opencode/**` (10 files).
- **Directories removed:** `scripts/` (9 tracked files, all relocated or
  deleted) and `source/` (57 tracked files, all relocated to `data/text/`). No
  stub remains.
- **Deleted files:** `docs/contract/source__CCAT.json`,
  `docs/contract/source__Strongs.json`, `scripts/README.md` (replaced by
  `docs/BUILD.md`).
- **New files:** `docs/BUILD.md`, `src/byz/curate/README.template.md`,
  `src/byz/{fetch,recover,build,diff}.py`, `src/byz/beta/{__init__,converter}.py`,
  `tests/curate/test_layout.py`. (The TEI header and `requirements.txt` are
  moves, not new files; see `plan.md`'s move table.)

## Verified inventory

Every fact below was checked against the working tree on
`feature/2026-11-16-edition-recovery-curation` at `9a5a9d1`, 2026-11-21. No
generator was run.

### The trees being moved

| Path | Tracked files | Size | Contents |
| --- | ---: | ---: | --- |
| `source/` | 57 | 4.2 MB | `CCAT/` 29 `.TXT` (27 books + `PA`/`ACT24`), `Strongs/` 27 `.BP5`, `README.md` |
| `data/` | 178 | 17 MB | `raw/_archives/` 6 ZIPs, `raw/<edition>/` extracts, `official-pdf/`, `provenance/*.toml` |
| `scripts/` | 9 | — | 4 entry points, `beta_to_unicode_custom/` (2 files), `tei_xml_header.xml`, `requirements.txt`, `README.md` |
| `editions/` | 852 | — | four editions; `rp2018-2023` has `source/` (56 files), `csv/`, `tei/`, `manifest.json`, `README.md` |

### The inverted dependency (must be removed)

| Fact | Check |
| --- | --- |
| `src/byz/curate/build.py` rewrites `sys.path` to import from `scripts/` | `build.py:197-200` (`_buc()`) |
| `src/byz/curate/recover.py` does the same | `recover.py:35-39` (`_beta_converter()`) |
| The TEI header is read through a `scripts/` path | `build.py:518`: `editions.ROOT / "scripts" / "tei_xml_header.xml"` |
| Each `scripts/*.py` inserts `src/` into `sys.path` | the four wrappers, one `sys.path.insert` each |
| One module lives only in `scripts/` | `scripts/beta_to_unicode_custom/beta_to_unicode_custom.py` (~6.2 KB, no module docstring) |
| The pin is only in `scripts/requirements.txt` | one line, `beta-code==1.0.0` |

### Consumers that name the repository input tree

| Consumer | What it does today |
| --- | --- |
| `src/byz/contract/paths.py:7-9` | `SOURCE = ROOT/"source"`, `CCAT_DIR`, `BP5_DIR` |
| `src/byz/contract/paths.py:35` | `SCRIPTS_DIR = ROOT/"scripts"` |
| `src/byz/contract/inventory.py:14-15,44,112-118` | `source/CCAT`, `source/Strongs` dataset names; a `scripts` dataset; `DOC_FILES` lists `source/README.md` and `scripts/README.md` |
| `src/byz/contract/contracts.py:37,53` | `DATASET_CONTRACTS` keys `source/CCAT`, `source/Strongs` |
| `src/byz/contract/coverage.py:7,12,17,22` | `COMPARISONS` left-hand dataset names |
| `src/byz/contract/invariants.py:27,32` | invariant table keyed by the two dataset names |
| `src/byz/contract/history.py:12-14,30-36` | history labels and git pathspecs (`source`, plus the retired trees) |
| `src/byz/contract/derivation.py:27,36` | reads `root/"source"/"CCAT"` and `root/"source"/"Strongs"` |
| `src/byz/curate/recover.py:271-286` | `recover_current()` copies `editions.ROOT/"source"/...` into the snapshot |
| `src/byz/curate/build.py:715,722,873-874` | source labels for the book check and `_last_commit("source/CCAT"/"source/Strongs")` |
| `src/byz/reconcile/compare.py:148-159,343-351` | `source_rows()` and the Strong's rows read `sources.ROOT/"source"/...` |
| `src/byz/reconcile/historical.py:51,59,111` | `_load_source()` reads the path *inside tag `v3.0.0`*; `_load_current()` reads the working tree; the current-state label |
| `src/byz/reconcile/report.py` (11 sites) | generated `docs/PROVENANCE.md` and `reports/reconciliation/` prose |
| `src/byz/curate/docs.py` (6 sites) | generated `docs/EDITIONS.md` prose |
| Generated reports | `reports/baseline/{files,books,differences,derivations}.csv`, `reports/reconciliation/{files,verses,history}.csv`, `docs/{DATA_CONTRACT,HISTORY,PROVENANCE,EDITIONS}.md`, `docs/contract/source__*.json`, `editions/rp2018-2023/manifest.json` (56 `source_files` entries, which are edition-relative and legal), `editions/rp2018-2023/README.md` (1 sentence) |

Re-verified count of `source/CCAT|source/Strongs|source/README.md` outside
`SPECS/`: **≈1,000 literal occurrences in 56 tracked files**, of which about 110
are in hand-edited Python/Markdown and the rest are generated reports that will
be regenerated. The brief's "roughly 126" understates the generated share;
`reports/reconciliation/verses.csv` alone has 364.

### Things the brief does not mention

1. **The manifest is not only hashes.** `editions/*/manifest.json` also stores
   `"generated_by": "python3 scripts/build_editions.py"`
   (`build.py:861`) and, for `rp2018-2023`, `source_commit` / `strongs_commit`
   computed from git pathspecs `source/CCAT` / `source/Strongs`
   (`build.py:873-874`). Deleting `scripts/` makes the first string false;
   moving `source/` changes what the pathspecs resolve to. See R6 and the
   decision box.
2. **The generated contract JSON filenames derive from the dataset names.**
   `src/byz/contract/report.py:509-512` writes `name.replace("/", "__")`, so
   `docs/contract/source__CCAT.json` becomes `data__text__CCAT.json`. The two
   stale files must be deleted or `tests/contract/test_integration.py`
   `test_contract_json_matches_the_dataset_names` fails.
3. **`data/text/README.md` has relative links.** It currently links
   `../editions` and `../docs/EDITIONS.md`; one directory deeper those become
   `../../`. `PdfLinkTests._user_docs()` does not include it today, so nothing
   would catch the break. It must be added.
4. **The current-state label is a working-tree path.** `historical.STATE_SPECS`
   has `"v3.0.0 source/CCAT"` (a path *inside tag `v3.0.0`*, which must stay) and
   `evidence()` sets `"current source/CCAT"` (a working-tree path, which must
   become `"current data/text/CCAT"`). `reconcile/report.py:294-295` looks both
   up by literal string; the two labels must come from one constant pair so they
   cannot drift.
5. **`reports/baseline/files.csv` has a `scripts` dataset.** `inventory._specs()`
   inventories 9 script files. After the move there is nothing there to
   inventory; the row disappears (−9 rows) and `docs/BUILD.md` /
   `data/text/README.md` replace the two folder README rows. This is the
   documented reason `files.csv` changes even though no edition changed.
6. **`README.md` is in `generated.HAND_MAINTAINED`.** Making it generated means
   moving it to `GENERATED_MARKDOWN` (17 → 18 files), deleting the
   partial-generation banner (`generated.BLOCK_MARKER`, `block_banner()`), and
   removing the entry from `HAND_MAINTAINED`.
7. **`docs/EDITIONS.md` is link-checked.** `PdfLinkTests` follows every relative
   link from the README, the edition READMEs, and the three `docs/` pages, so a
   template that links `(data/text/)` must point at a real directory.
8. **`tests/curate/test_reproducible.py` drives the four scripts by path.**
   `GENERATORS` (lines 19-25) must become `-m` entries, and it compares a
   worktree at `HEAD`, so it only passes after the change is committed.
9. **There is no CI.** Verification is the three `unittest` suites plus a
   twice-run pipeline with no diff, exactly as `README.md` and `TECH.md` §9 say.
10. **`SPECS/ROADMAP.md` names `scripts/` and `source/`.** It is a dated,
    historical roadmap. It is left untouched, like the other frozen specs; the
    live constitution (`SPECS/TECH.md`) is updated.

## Definitions

- **Repository input tree** - the Beta-code files at the repository root that
  feed the current edition: `data/text/CCAT` and `data/text/Strongs` after this
  change (`source/` before it). Dataset names are `data/text/CCAT` and
  `data/text/Strongs`.
- **Source snapshot** - `editions/<edition>/source/`, a frozen copy of that
  edition's inputs so the edition can be downloaded and verified on its own.
  Its internal layout is `source/CCAT` / `source/Strongs` (or `source/ccat` for
  the official editions) and it is **not** the repository input tree. This
  distinction is what removes the old `src/` vs `source/` confusion: `src/` is
  code, `data/text/` is input, `editions/<id>/source/` is a copy of input inside
  an output.
- **Entry point** - one of the four modules run with `python3 -m byz.<verb>`:
  `byz.fetch`, `byz.recover`, `byz.build`, `byz.diff`.
- **Byte-identity gate** - the check that `editions/*/{source,csv,tei}` are
  byte-identical to the pre-change tree, and that every manifest
  `source_files` / `artifact_files` entry is unchanged (R6).
- **Retired-layout reference** - a reference to a path or command that this
  change removes: `source/CCAT`, `source/Strongs`, `source/README.md`, a bare
  top-level `source/`, or `python3 scripts/…` / `scripts/requirements.txt` /
  `scripts/beta_to_unicode_custom/` / `scripts/tei_xml_header.xml` /
  `scripts/README.md`.

## Maintainer decisions (fixed requirements)

**D1 - fold `source/` into `data/`.** The repository input tree becomes
`data/text/`, so `data/text/CCAT/`, `data/text/Strongs/`, and
`data/text/README.md` sit beside `data/raw/` and `data/provenance/`. Do **not**
create a new top-level `raw_data/`. `editions/<edition>/source/` stays exactly
as it is: it is the per-edition snapshot, not the repository input tree, and
renaming it would churn every manifest and edition README. The distinction is
documented in `docs/EDITIONS.md`, `data/text/README.md`, and `docs/BUILD.md`.

**D2 - fold `scripts/` into `src/` and delete `scripts/`.** The four entry
points become `src/byz/{fetch,recover,build,diff}.py` and are invoked as
`PYTHONPATH=src python3 -m byz.fetch|recover|build|diff`, matching the existing
`byz.contract` / `byz.reconcile` pattern. `scripts/beta_to_unicode_custom/`
becomes `src/byz/beta/`, and the `sys.path` hacks in
`src/byz/curate/build.py:197-200` and `src/byz/curate/recover.py:35-39` are
deleted. `scripts/tei_xml_header.xml` moves next to the code that reads it
(`src/byz/curate/tei_xml_header.xml`, package data).
`scripts/requirements.txt` moves to the repository root as `requirements.txt`.
`scripts/README.md` becomes `docs/BUILD.md`. There is no `scripts/` directory
afterwards.

**D3 - the root `README.md` becomes fully machine-generated.** The hand-written
prose moves into `src/byz/curate/README.template.md`, which the generator owns.
The whole README is rendered from it, including the layout table, the
curated-editions table, and the generated-files table. The rendered file carries
the full-file "Generated file. Do not edit by hand." banner; the template
carries a note saying it is the file to edit. The contributor workflow is: edit
the template, run `PYTHONPATH=src python3 -m byz.build`, commit both.

Decisions this spec finalises (because the brief leaves them open):

4. **Entry-point shape.** Four thin modules, one per verb, each with
   `main()` (and `main(argv=None)` for `byz.fetch`) plus the
   `if __name__ == "__main__": sys.exit(main())` guard, exactly like
   `src/byz/contract/__main__.py`. They contain no logic; they call
   `byz.curate.{recover,build,diff}` and `byz.reconcile.fetch`.
5. **Converter package.** `src/byz/beta/__init__.py` (docstring only) and
   `src/byz/beta/converter.py` (the moved module, logic byte-identical). Callers
   import `from byz.beta import converter as buc` lazily inside the existing
   helper, so `beta_code` remains an optional import until a conversion runs
   (today's behaviour) and the error still names `beta_code`.
6. **Template mechanism.** Two placeholder lines, `{{CURATED_EDITIONS}}` and
   `{{GENERATED_FILES}}`, each on its own line and each used exactly once. The
   renderer raises `ValueError` naming the token when the template has an
   unknown token, a missing token, or a duplicated token. The template's first
   line is a note that the renderer strips (R4.3). The layout table stays as
   prose in the template: it documents structure, has no machine-readable
   source, and is already locked by `RootReadmeTests.test_lists_every_root_directory`.
7. **Docs home.** `docs/BUILD.md` is the single build/run reference (the content
   of `scripts/README.md`, rewritten for the new commands). `docs/RELEASE-NOTES.md`
   gains one dated entry for the breaking path/command change.
   `docs/EDITIONS.md` gains one section for the old-to-new mapping, rendered from
   a new `docs.MOVED_PATHS` constant (separate from `RETIRED_PATHS`, which
   records the 2026-11-19 removal).
8. **Old-path rule.** Retired-layout references are allowed only in
   `docs/EDITIONS.md` (the mapping table), `docs/RELEASE-NOTES.md`, `SPECS/**`
   (frozen history), `src/byz/curate/docs.py` (`MOVED_PATHS`),
   `src/byz/contract/history.py` (git pathspecs), and
   `src/byz/reconcile/historical.py` (paths inside tags `v2.0.3`/`v3.0.0`), plus
   the new `tests/curate/test_layout.py` that enforces the rule. Everywhere else
   a retired-layout reference fails a test with the file name.
9. **No packaging.** `PYTHONPATH=src` stays the documented prefix; `requirements.txt`
   at the root is installed with `pip install -r requirements.txt` from the
   repository root.

## Decision required: manifest metadata (needs maintainer sign-off)

The brief says "no change to any … manifest content". Two manifest values are
derived from the paths this change removes, so that constraint cannot be met
without keeping a false statement:

| Key | Today | Why it must change |
| --- | --- | --- |
| `generated_by` (all four editions) | `"python3 scripts/build_editions.py"` | `scripts/build_editions.py` will not exist |
| `source_commit` (`rp2018-2023`) | `git log -1 -- source/CCAT` | the path is now `data/text/CCAT` |
| `strongs_commit` (`rp2018-2023`) | `git log -1 -- source/Strongs` | the path is now `data/text/Strongs` |

Three options:

- **A (recommended, specified in R6).** Allow exactly these three keys to change,
  and gate everything else: `source_files` and `artifact_files` keep identical
  `path`/`sha256`/`size` for every entry, and a diff of `manifest.json` may show
  only these keys. `generated_by` becomes
  `"PYTHONPATH=src python3 -m byz.build"`; the commits are computed from both
  historical and current pathspecs (`_last_commit("source/CCAT", "data/text/CCAT")`),
  so future edits are still recorded. Cost: a one-time metadata diff in four
  manifests, and the recorded commit for `rp2018-2023` becomes the move commit
  until the next text change.
- **B (strict byte equality).** Freeze `generated_by` and the old pathspecs as
  constants in `build.py` with a comment. Cost: a committed artifact names a
  command that does not exist, and `source_commit` stops tracking future edits
  to `data/text/` forever.
- **C.** Keep `scripts/build_editions.py` as a shim so the string stays true.
  Rejected by D2 ("no shim scripts").

The rest of this spec is written for **A**; the gate in R6.2 is what makes it
safe. If the maintainer picks B, R6.2 is dropped and `build.py` keeps two
frozen literals, both added to the R8.4 allowlist with a comment.

## Requirements

### R1 - Fold `source/` into `data/text/` (D1)

1. `git mv source data/text` moves all 57 tracked files with their bytes and
   history. No `raw_data/`, no copy, no stub.
2. `src/byz/contract/paths.py` derives every input path and dataset name from
   one pair of constants:

   ```python
   DATA_TEXT = ROOT / "data" / "text"
   CCAT_DIR = DATA_TEXT / "CCAT"
   BP5_DIR = DATA_TEXT / "Strongs"
   CCAT_DATASET = "data/text/CCAT"
   BP5_DATASET = "data/text/Strongs"
   ```

   `SOURCE` is removed. No module outside `paths.py` builds `data/text/...` by
   hand: `inventory`, `contracts`, `coverage`, `invariants`, `bp5`, `ccat`,
   `derivation`, `compare`, and `historical` use the constants.
3. Dataset names change to `data/text/CCAT` and `data/text/Strongs` everywhere:
   `reports/baseline/{files,books,differences,derivations}.csv`,
   `reports/reconciliation/{files,verses,history}.csv`,
   `docs/DATA_CONTRACT.md`, `docs/HISTORY.md`, `docs/PROVENANCE.md`, and the
   JSON filenames in `docs/contract/`. The two stale
   `docs/contract/source__*.json` files are deleted.
4. `src/byz/curate/recover.py` `recover_current()` (lines 271-286) copies
   `paths.CCAT_DIR` / `paths.BP5_DIR` into `editions/rp2018-2023/source/`.
   `src/byz/reconcile/historical.py` `_load_current()` (line 59) reads the same
   constants.
5. `src/byz/reconcile/historical.py` keeps a single pair of state labels: the
   historical one names the path **inside tag `v3.0.0`** (`source/CCAT`, with a
   comment saying so) and the current one names the working-tree path
   (`current data/text/CCAT`). `reconcile/report.py` looks them up through the
   constants, not through duplicated literals. `_load_source()` keeps reading
   `source/CCAT` from the tag.
6. `src/byz/contract/history.py` labels the rows `data/text/CCAT` /
   `data/text/Strongs` and keeps the pre-move evidence by listing both
   pathspecs, e.g. `("data/text/CCAT", ("source/CCAT", "data/text/CCAT"))`,
   with a comment that these are git selectors, not working-tree paths.
   `CORPUS_PATHSPECS` gains `data/text` and keeps `source`.
7. `data/text/README.md` keeps its content and fixes only: the relative links
   (`../../editions`, `../../docs/EDITIONS.md`), the pointer to the converter
   (`src/byz/beta/converter.py`), and any `source/` self-reference. It gains one
   sentence distinguishing it from `editions/<edition>/source/`.
8. `root_readme` prose, `docs/EDITIONS.md`, `docs/DATA_CONTRACT.md`, and
   `editions/rp2018-2023/README.md` describe the repository input tree as
   `data/text/` and the edition snapshot as `editions/<edition>/source/`.

### R2 - Fold `scripts/` into `src/byz/` (D2)

1. The four entry points become `src/byz/fetch.py`, `src/byz/recover.py`,
   `src/byz/build.py`, and `src/byz/diff.py` (decision 4). Each is a thin
   `main()`; the existing printed output is preserved.
2. `scripts/beta_to_unicode_custom/beta_to_unicode_custom.py` becomes
   `src/byz/beta/converter.py` with its logic unchanged; its shebang line is
   dropped. `src/byz/beta/__init__.py` is a one-line package docstring.
3. `src/byz/curate/build.py` `_buc()` and `src/byz/curate/recover.py`
   `_beta_converter()` no longer touch `sys.path`; they return
   `byz.beta.converter` (imported inside the function). No module under `src/`
   contains `sys.path`.
4. `scripts/tei_xml_header.xml` becomes `src/byz/curate/tei_xml_header.xml`, and
   `build.py:518` reads it as `Path(__file__).with_name("tei_xml_header.xml")`,
   independent of the repository root.
5. `scripts/requirements.txt` becomes `requirements.txt` at the repository root
   with exactly `beta-code==1.0.0`. Every install instruction says
   `pip install -r requirements.txt` from the repository root.
6. All four `sys.path.insert(0, …/src)` blocks in the old wrappers disappear
   with the files.

### R3 - Delete `scripts/` and lock the layout

1. `scripts/` does not exist; `git ls-files scripts` is empty. No stub, symlink,
   or `.gitkeep`.
2. `src/byz/contract/paths.py` loses `SCRIPTS_DIR`;
   `src/byz/contract/inventory.py` loses the `("scripts", …)` spec row (line 44)
   and the `scripts/README.md` entry in `DOC_FILES` (line 117). `DOC_FILES`
   becomes `README.md`, `LICENSE`, `data/text/README.md`, `essay/README.md`,
   `docs/BUILD.md`. `requirements.txt` is deliberately **not** added to
   `DOC_FILES`.
3. `tests/curate/test_layout.py` (new) locks the layout: no `scripts/`
   directory, no top-level `source/` directory, `data/text` holds exactly the
   29 `.TXT` and 27 `.BP5` files, the four entry-point modules import and expose
   `main`, `requirements.txt` is at the root, the TEI header sits beside
   `build.py`, no Python module manipulates `sys.path`, and the sweep in R8.4.
4. `tests/curate/test_reproducible.py` `GENERATORS` (lines 19-25) lists
   `("-m", ["byz.recover"])`, `("-m", ["byz.build"])`, `("-m", ["byz.diff"])`,
   `("-m", ["byz.contract"])`, `("-m", ["byz.reconcile"])` and runs them all with
   `PYTHONPATH=<worktree>/src`.
5. `tests/curate/test_current_pipeline.py` drops
   `test_retired_converters_do_not_exist` (the directory is gone) and
   `test_requirements_pin_only_the_converter_dependency` reads
   `ROOT/"requirements.txt"`.

### R4 - The root README is fully generated (D3)

1. `src/byz/curate/README.template.md` holds all README prose: the title, the
   badge, the introduction, "Start here", "Official vs released", the
   placeholder lines for the two data sections, "Repository layout" (with the
   layout table), "Source of truth and provenance", "Which text should I use?",
   "Repo releases vs curated editions", "Reproducing the curated data", "Tests",
   "Archiving", and "Copyright". Path and command changes are applied here.
2. The rendered `README.md` is produced by
   `generated.write_markdown(editions.ROOT/"README.md", docs.render_root_readme(TEMPLATE))`:
   - one full-file banner (`generated.MARKDOWN_MARKER` plus the visible
     `> **Generated file. Do not edit by hand.**` line);
   - no `<!-- editions:begin -->` / `<!-- editions:end -->` markers;
   - `{{CURATED_EDITIONS}}` renders the `## Curated editions` section from the
     manifests (the current `root_readme_block()` table code, minus the banner
     and markers);
   - `{{GENERATED_FILES}}` renders the `## Generated files` section from
     `generated.GENERATED_FILES` (including the "do not edit" and
     `pdfs.toml`-is-hand-maintained sentences);
   - the render is deterministic and idempotent: rendering twice returns the
     same bytes.
3. The template's first line is
   `<!-- Template for README.md: edit this file, then run PYTHONPATH=src python3 -m byz.build. -->`.
   The renderer asserts it, strips it, and raises `ValueError` naming the file if
   it is missing. The template is banner-free and listed in
   `generated.HAND_MAINTAINED`.
4. `docs.render_root_readme`, `docs.update_root_readme`, `docs.BEGIN`,
   `docs.END`, `docs.replace_block`, `generated.BLOCK_MARKER`, and
   `generated.block_banner()` are deleted. `README.md` moves from
   `generated.HAND_MAINTAINED` to `generated.GENERATED_MARKDOWN` (18 files).
5. The `GENERATED_FILES` row for the README becomes label `` `README.md` ``,
   command `` `PYTHONPATH=src python3 -m byz.build` ``, patterns
   `("README.md",)`; the other rows' commands are updated to the new entry
   points.
6. The README states, in the "Reproducing the curated data" section, the new
   six commands and the `pip install -r requirements.txt` line, and points at
   `docs/BUILD.md` for details.
7. `tests/curate/test_editions.py::RootReadmeTests` becomes:
   - `test_readme_equals_the_template_render` (byte comparison);
   - `test_readme_starts_with_the_generated_banner`;
   - `test_readme_has_no_block_markers`;
   - `test_lists_every_root_directory` (with `source`/`scripts` removed from
     `ROOT_ITEMS` and a negative assertion for both);
   - `test_has_no_contradictory_version_wording` (unchanged);
   - `test_lists_generated_files_and_commands` (all 12 rows, whole file).
   `test_has_exactly_one_generated_block`, `test_generated_block_matches_the_generator`,
   and `test_generated_block_is_marked_and_says_the_rest_is_hand_written` are
   deleted, as is `test_generated.py::test_block_banner_names_the_command_and_partial_generation`.

### R5 - Build docs, release note, and the old-to-new table

1. `scripts/README.md` becomes `docs/BUILD.md`: install, the input tree,
   the six commands, what `byz.recover` stages, `byz.fetch`'s three modes, the
   report-generation order (the moved "Report generation order" section, with
   the same facts and the same failure modes), "Editing the root README" (D3
   workflow), `byz.contract`'s git requirement, and the test commands. It names
   `src/byz/beta/converter.py` and `src/byz/curate/tei_xml_header.xml` as the
   moved library files. It is banner-free, listed in `HAND_MAINTAINED` and in
   `HAND_MAINTAINED_DOCS`.
2. `docs/EDITIONS.md` (generated) gains `## Where the code and inputs moved
   (2026-11-21)`, after the 2026-11-19 section, rendered from
   `docs.MOVED_PATHS`: one row per old path or command (see the mapping table in
   `plan.md`), one sentence that the bytes and hashes did not change, and a link
   to `docs/RELEASE-NOTES.md`.
3. `docs/RELEASE-NOTES.md` gains one entry, "2026-11-21 - the inputs moved to
   `data/text/` and the scripts became modules": the old commands are removed
   (no shims), the old doc paths are gone, the new commands are listed, and the
   note links the canonical table in `docs/EDITIONS.md`.
4. `docs/EDITIONS.md`'s "Rebuilding the curated editions" code block and the
   report command blocks in `reports/reconciliation/summary.md` and
   `docs/DATA_CONTRACT.md`'s reproduce block use the new commands.

### R6 - Byte identity and manifest metadata

1. Every file under `editions/*/source`, `editions/*/csv`, and `editions/*/tei`
   is byte-identical to the pre-change tree. The tracked file count under
   `editions/` is unchanged (852) and no file is added or removed under those
   three directories.
2. Every `source_files` and `artifact_files` entry in every
   `editions/*/manifest.json` keeps its `path`, `sha256`, and `size`. The only
   manifest keys allowed to differ are `generated_by`, `source_commit`, and
   `strongs_commit` (decision A), and each difference is listed in
   `validation.md` with its before and after value.
3. `generated_by` becomes `"PYTHONPATH=src python3 -m byz.build"`. The commit
   fields are computed with both pathspecs
   (`_last_commit("source/CCAT", "data/text/CCAT")` and the same for `Strongs`)
   so the recorded commit follows future content changes. `build.py`'s comment
   and `editions/rp2018-2023`'s manifest note in `docs/EDITIONS.md` say that a
   pure move updates the recorded commit and no hash.
4. No other edition text changes except `editions/rp2018-2023/README.md`, whose
   one sentence about the repository input tree now names `data/text/`.
5. A test locks the invariant: `tests/curate/test_fidelity.py::ManifestIntegrityTests`
   already recomputes every manifest hash; it keeps passing, and
   `tests/curate/test_layout.py` asserts `generated_by` names an existing entry
   point (`(ROOT/"src"/"byz"/"build.py").is_file()`).

### R7 - TECH.md, `.opencode/`, and the prose sweep

1. `SPECS/TECH.md` §5 replaces the layout block and the "sources -> pipeline ->
   editions" paragraph: `data/text/` under `data/`, no `scripts/`, `src/byz/` as
   the package with `python -m byz.<verb>` entry points, `requirements.txt` at
   the root, and a reference to this spec.
2. `SPECS/TECH.md` §11 replaces "Keep the human-facing scripts in `scripts/`
   thin; logic lives in `src/byz/`" with the module-entry-point rule. §2's
   `scripts/fetch_official.py --verify`, `source/Strongs`, and
   `source/README.md` references become `python3 -m byz.fetch --verify`,
   `data/text/Strongs`, and `data/text/README.md`; §7's parsing-code pointer and
   §9's `scripts/requirements.txt` follow.
3. `.opencode/` describes the real layout: `data/text/` is the input,
   `editions/<id>/source/` is the snapshot, `python -m byz.<verb>` are the
   entry points, `docs/BUILD.md` is the build reference, and
   `src/byz/beta/converter.py` / `src/byz/curate/tei_xml_header.xml` are the
   moved library files. The ten files are
   `.opencode/agents/{build,code-reviewer,plan,spec-implementer,verifier}.md`,
   `.opencode/commands/read-conventions.md`, and
   `.opencode/skills/{feature-specification,fix-typing-linting-issues,investigate-bug,write-tests}/SKILL.md`.
   `investigate-bug/SKILL.md`'s suggested `scripts/check-output.py` becomes a
   check under `tests/`, and `fix-typing-linting-issues/SKILL.md`'s
   `py_compile scripts/*.py` becomes a `find src -name '*.py'` loop.

### R8 - The old-path rule, determinism, and red/green tests

1. The retired-layout rule in decision 8 holds. The enforced patterns are:
   `(?<![\w./-])source/(CCAT|Strongs|README\.md)`, a code-span or link to a bare
   `source/`, `python3 scripts/`, `scripts/requirements.txt`,
   `scripts/beta_to_unicode_custom`, `scripts/tei_xml_header.xml`,
   `scripts/README.md`, and a bare retired entry-point file name
   (`(?<![\w./-])(fetch_official|recover_editions|build_editions|diff_editions)\.py`).
   The last pattern catches an old command quoted without its `scripts/` prefix.
2. `tests/curate/test_layout.py::test_no_tracked_file_names_the_removed_layout`
   implements the rule over `git ls-files`, with an explicit allowlist (data,
   not a regex). The allowlist has 13 entries; each is here for one reason:
   - `docs/EDITIONS.md` - renders the `MOVED_PATHS` / `RETIRED_PATHS` tables.
   - `docs/RELEASE-NOTES.md` - the dated breaking-change entries.
   - `docs/HISTORY.md` - keeps the historical tag labels and names `data/text/CCAT`.
   - `docs/PROVENANCE.md` - names paths inside the historical tags.
   - `reports/reconciliation/history.csv` - the same historical tag labels.
   - `reports/reconciliation/summary.md` - the same historical tag labels.
   - `src/byz/curate/docs.py` - holds the authoritative mapping constants.
   - `src/byz/contract/history.py` - holds the git pathspecs for pre-move history.
   - `src/byz/reconcile/historical.py` - reads paths inside tags `v2.0.3` / `v3.0.0`.
   - `src/byz/reconcile/report.py` - renders the archive prose from those labels.
   - `tests/contract/test_integration.py` - keeps the historical tag labels `v3.0.0 source/CCAT`.
   - `tests/curate/test_editions.py` - asserts the retired tree is gone.
   - `tests/curate/test_layout.py` - contains this sweep's own needles.
   It skips `SPECS/` and `editions/` (an edition's `source/` is always its own
   snapshot). It also asserts `SPECS/TECH.md` specifically, so the constitution
   cannot regress.
3. Every behaviour has a failing test first and a green test after (R1-R7).
   New tests live in `tests/curate/test_layout.py` and the rewritten
   `RootReadmeTests`; no test touches the network; no test writes to the
   repository.
4. A second full regeneration is byte-identical: no timestamps, hostnames,
   absolute paths, or run-dependent ordering.
5. The three suites pass:
   `tests/contract`, `tests/curate`, `tests/reconciliation`, including the
   worktree-based `tests/curate/test_reproducible.py` after the change commit
   plus **two** follow-up regeneration commits. The first follow-up rewrites the
   manifests, `reports/baseline/files.csv`, and `docs/HISTORY.md`. Because it
   touches `editions/*/manifest.json` and `editions` is in `CORPUS_PATHSPECS`
   (`src/byz/contract/history.py`), the recorded "Last corpus commit" moves to
   that follow-up; a second regeneration commit updates only `docs/HISTORY.md`
   and then converges.

## Breaking changes (documented, no compatibility)

| Removed | Replacement |
| --- | --- |
| `python3 scripts/fetch_official.py [--verify\|--force]` | `PYTHONPATH=src python3 -m byz.fetch [--verify\|--force]` |
| `python3 scripts/recover_editions.py` | `PYTHONPATH=src python3 -m byz.recover` |
| `python3 scripts/build_editions.py` | `PYTHONPATH=src python3 -m byz.build` |
| `python3 scripts/diff_editions.py` | `PYTHONPATH=src python3 -m byz.diff` |
| `scripts/requirements.txt` | `requirements.txt` (repository root) |
| `scripts/README.md` | `docs/BUILD.md` |
| `scripts/beta_to_unicode_custom/` | `src/byz/beta/` |
| `scripts/tei_xml_header.xml` | `src/byz/curate/tei_xml_header.xml` |
| `source/CCAT`, `source/Strongs`, `source/README.md` | `data/text/CCAT`, `data/text/Strongs`, `data/text/README.md` |
| README's hand-written prose and `<!-- editions:begin -->` block | `src/byz/curate/README.template.md` |

No shims, no symlinks. The table is repeated in `docs/RELEASE-NOTES.md` and
`docs/EDITIONS.md` (decision 7).

## Acceptance criteria

- `source/` and `scripts/` do not exist; `git ls-files source scripts` is
  empty; no stub or symlink replaces them. `data/text/CCAT` has 29 `.TXT`,
  `data/text/Strongs` has 27 `.BP5`, `data/text/README.md` exists.
- `PYTHONPATH=src python3 -m byz.{fetch,recover,build,diff}` run; `byz.fetch
  --verify` exits 0 with no network access and no writes.
- No tracked Python module manipulates `sys.path`; `src/byz/beta/converter.py`
  is imported by `byz.curate.build` and `byz.curate.recover` without a path
  hack; the TEI header is read from beside `build.py`.
- `requirements.txt` is `beta-code==1.0.0`; `scripts/requirements.txt` is gone.
- `README.md` starts with the generated-file banner, contains no
  `editions:begin`/`editions:end` marker, and is byte-identical to
  `generated.markdown(docs.render_root_readme(TEMPLATE))`. Editing the template
  and re-rendering is the documented way to change it.
- `editions/*/{source,csv,tei}` are byte-identical to the pre-change tree; every
  manifest `source_files`/`artifact_files` entry is unchanged; the only
  manifest key differences are the three in R6.2 and they are recorded in
  `validation.md`.
- `docs/contract/` contains no `source__*.json`; it contains
  `data__text__CCAT.json` and `data__text__Strongs.json` plus the six edition
  documents and `contracts.json`.
- `docs/EDITIONS.md` contains `## Where the code and inputs moved (2026-11-21)`
  with every `MOVED_PATHS` row and the "bytes and hashes did not change"
  sentence; `docs/RELEASE-NOTES.md` carries the 2026-11-21 entry;
  `docs/BUILD.md` exists.
- No tracked file outside the allowlist in R8.2 references the retired layout;
  `SPECS/TECH.md` §5 and §11 describe the new layout.
- The full regeneration runs twice with no diff; all three suites pass; nothing
  under `data/raw/`, `data/provenance/`, or `editions/*/{source,csv,tei}`
  changed.

## Risks

- **The manifest gate is the honest seam.** R6.2 permits exactly three keys to
  differ. If a fourth key moves, the gate fails and the change is wrong. Record
  the before/after values; do not "regenerate until it looks right".
- **Order of operations.** `git mv source data/text` must happen before
  `byz.recover` runs, or the current edition's snapshot is built from a missing
  directory. Phase order in `plan.md` is mandatory.
- **Two `source/` meanings.** A careless sweep either misses the one sentence in
  `editions/rp2018-2023/README.md` or rewrites `editions/*/manifest.json`'s
  edition-relative `source_files` paths. The rule in R8.1 uses a lookbehind so
  `editions/<id>/source/CCAT` stays legal, and a targeted test asserts the
  current edition's README names `data/text/`.
- **`git log` pathspecs.** `_last_commit` with both pathspecs returns the move
  commit until the next content change; that is intended and documented. A test
  must not assert a fixed commit hash.
- **README idempotence.** `generated.markdown()` strips and re-adds one banner;
  the renderer must not add a second. The template's note line must be stripped
  exactly once, or the byte comparison fails.
- **Doc links.** `data/text/README.md` moves one level deeper; `docs/BUILD.md`
  is one level deep like `scripts/README.md` was, but a `../` link written for
  `scripts/` resolves differently from `docs/`. `PdfLinkTests` must cover both.
- **`files.csv` churn.** −9 `scripts` rows, −1 `source/README.md` row, +1
  `docs/BUILD.md` row, and 57 `last_commit` changes. The two follow-up
  regeneration commits are part of the change, not a surprise.
- **Agent instructions are executable documentation.** Leaving `.opencode/`
  unchanged would have future agents recreate `scripts/` and edit `source/`.

## Sequencing

- Independent of `SPECS/2026-11-21-diff-categories/` (a concurrent spec in a
  different folder). Do not touch that folder.
- `SPECS/2026-11-19-docs-clarity/` is already implemented; nothing in it
  overlaps beyond the general "docs clarity" goal.
- The previous change's regenerated baseline is committed at `9a5a9d1`, so this
  change starts from a clean, reproducible tree.
