# Requirements - The two source classes: `data/raw/print/` and `data/raw/repo/`

## Context

After `SPECS/2026-11-25-inputs-out-of-editions/` every input a build reads lives
under `data/`, and every edition under `editions/` is outputs only. The shape is
right, but the **input tree still hides what kind of source each tree is**:

```
today
  data/
    text/CCAT, text/Strongs          <- the current text (a repo lineage source)
    text/README.md                   <- Beta-code and parsing conventions
    raw/rp2005/                      <- published print-edition extracts + PDF
    raw/rp2018/                      <- published print-edition extracts + PDF
    raw/_archives/                   <- the six published ZIPs
    raw/rp2005-2019/                 <- the 2019 repo lineage, from tag v2.0.3
    provenance/*.toml
```

Five problems:

1. **The current text is not a source snapshot like the others.** It sits at
   `data/text/`, outside `data/raw/`, so it is the only input tree with a
   special path and the only one that is not a per-edition snapshot. Every other
   edition's inputs are `data/raw/<something>/`; the current text is
   `data/text/`. The asymmetry is historical, not meaningful: `byz.build` reads
   it exactly like `data/raw/rp2005-2019/`.
2. **Print and repository material are indistinguishable.** `raw/rp2005/` and
   `raw/rp2018/` come from the publisher; `raw/rp2005-2019/` comes from this
   repository's own history. They are siblings with no label, and the only place
   that says which is which is prose in three different documents.
3. **The conventions are stranded in a folder README.** `data/text/README.md`
   holds Dr Robinson's Beta-code, variant-code, parsing, and Strong's
   conventions. Moving the folder would bury them at
   `data/raw/repo/rp2018-2023/README.md`, which is also where the (generated)
   description of the snapshot belongs, and it would imply that a single
   edition's folder owns the conventions both repo trees use.
4. **The current text has no provenance record.** `data/provenance/` has records
   for the two official editions (archives + PDFs) and for the 2019 lineage
   (tag + commit + 57 hashes). The current text — the maintained text the
   repository exists for — has none: its revision date and per-file hashes are
   only in `editions/rp2018-2023/manifest.json`.
5. **The input tree has no READMEs.** There is no `data/README.md` (only an
   uncommitted draft), no `data/raw/README.md`, no README in any source folder.
   A reader who opens `data/raw/` sees four opaque directory names. The edition
   folders and `docs/` are documented; the inputs are not.

This change splits `data/raw/` into two source classes, turns the current text
into a source snapshot under `data/raw/repo/`, moves the conventions into a
hand-maintained document owned by the repo class, gives the current text a
provenance record, and generates a README for `data/` and for every input
folder.

```
after
  data/
    README.md                        <- generated index of the input tree
    raw/
      README.md                      <- generated: print vs repo
      print/                         <- published print-edition material
        _archives/{rp2005,rp2018}/   <- the six published ZIPs
        rp2005/{ccat,ascii,preformatted,official-pdf}/
        rp2018/{ccat,ascii,preformatted,official-pdf}/
      repo/                          <- this repository's own lineage
        CONVENTIONS.md               <- hand-maintained: Beta code, variants, parsing
        rp2005-2019/{textonly-beta-code,parsed}/
        rp2018-2023/{ccat,strongs}/
    provenance/*.toml
```

There is no top-level `data/text/` afterwards.

## Goal

1. Move the print-edition extracts and PDFs under `data/raw/print/`, and the two
   repository lineages under `data/raw/repo/`, so the kind of source is visible
   from the path (D1).
2. Move `data/text/` to `data/raw/repo/rp2018-2023/{ccat,strongs}/`, so the
   current text is a source snapshot like `data/raw/repo/rp2005-2019/` (D2).
3. Move the conventions into one hand-maintained `data/raw/repo/CONVENTIONS.md`
   with Dr Robinson's prose intact, and have both repo source READMEs link to
   it (D3).
4. Generate `data/README.md`, `data/raw/README.md`, `data/raw/print/README.md`,
   `data/raw/repo/README.md`, and one README in each of the four source folders
   from `byz.build`, with counts, provenance, the consuming edition, the
   command, and links (D4).
5. Add `data/provenance/rp2018-2023.toml` recording the revision (2023-07-20),
   the commit(s) that last touched the sources, and a SHA-256 per file (D5).
6. Keep every `editions/*/csv/**` and `editions/*/tei/**` byte identical, and
   give the repository a regression guard that no tracked file names the retired
   `data/text/` (or the four retired `data/raw/` roots).
7. Keep the pipeline deterministic: a second full regeneration is byte
   identical, and no generated file carries a timestamp, hostname, or absolute
   path.

## Non-goals

- **No change to any edition artifact.** All 672 files under
  `editions/*/{csv,tei}` keep their SHA-256, and no file is added or removed.
  Every `artifact_files` entry in every manifest keeps its `path`, `sha256`, and
  `size`. This is the hard gate, and it is stronger than the 2026-11-25 change's
  (which regenerated `rp2005-2019`).
- **No change to any source byte.** Every `.CCT`, `.TXT`, `.BP5`, `.ASC`,
  `*_Byz.txt`, ZIP, and PDF keeps its content. The change is `git mv` plus
  directory names, code, docs, and one new provenance record. No converter,
  reader, book map, or view definition changes.
- **No source-correction or reconciliation work.** Nothing is compared,
  re-downloaded, or re-decided. `byz.fetch --force` is not used; the two official
  provenance records are re-recorded offline with their `downloaded`,
  `final_url`, and `http_status` values preserved.
- **No compatibility shims.** No `data/text` symlink, no stub README, no
  `.gitkeep`, no duplicate tree. Retired paths are documented, not aliased.
- **No new command.** The data READMEs are rendered by `byz.build` (D4), not by
  a new `byz.docs`. `byz.fetch`, `byz.materialise`, `byz.build`, `byz.diff`,
  `byz.contract`, `byz.reconcile`, and `byz.verify` keep their roles.
- **No new dependency.** `beta-code==1.0.0` stays the only one. The README
  renderer and the provenance writer use the standard library.
- **No packaging.** Commands stay `PYTHONPATH=src python3 -m byz.<verb>`.
- **No change to the edition model, dataset set, diff categories, or diff
  figures.** `csv/unaccented` stays outside the contract. The diff reports keep
  their data: the only report change is the one-line "Source"/Notation prose that
  names the current source path, in `reports/diffs/README.md` and in each
  `reports/diffs/<pair>/report.md`.
- **No new README for `data/provenance/` or `data/raw/print/_archives/`.**
  D4 names the folders that get one; `data/README.md` and `print/README.md`
  describe those two. Adding more is scope creep.
- **No edit to a frozen `SPECS/` folder.** Only this folder and `SPECS/TECH.md`
  change.

## Affected scope

- **Inputs moved:** 13 directories / 289 tracked files (see "Verified
  inventory"), plus `data/text/README.md` becoming
  `data/raw/repo/CONVENTIONS.md`.
- **Inputs added:** `data/provenance/rp2018-2023.toml` (generated) and eight
  generated READMEs under `data/`.
- **Pipeline:** `src/byz/contract/paths.py`, `src/byz/reconcile/sources.py`,
  `src/byz/reconcile/fetch.py`, `src/byz/contract/history.py`,
  `src/byz/curate/editions.py`, `src/byz/curate/materialise.py`,
  `src/byz/curate/build.py`, `src/byz/curate/docs.py`, `src/byz/curate/diff.py`,
  new `src/byz/curate/data_docs.py`, `src/byz/curate/files.py`,
  `src/byz/generated.py`, `src/byz/build.py`, and the prose strings in
  `src/byz/contract/report.py`, `src/byz/reconcile/{compare,historical,report}.py`,
  `src/byz/beta/converter.py`.
- **Generated documentation:** `README.md`, `docs/EDITIONS.md`,
  `docs/DATA_CONTRACT.md`, `docs/PROVENANCE.md`, `docs/HISTORY.md`,
  `docs/contract/*.json`, `reports/baseline/*`, `reports/reconciliation/*`,
  `reports/diffs/README.md`, `editions/*/manifest.json`, `editions/*/README.md`,
  and the eight new input READMEs.
- **Hand-written files edited directly:** `data/raw/repo/CONVENTIONS.md`
  (moved and re-scoped), `docs/BUILD.md`, `data/provenance/pdfs.toml`,
  `src/byz/curate/README.template.md`, `SPECS/TECH.md`, `.opencode/**`, and the
  tests.
- **Retired paths:** `data/text/`, `data/raw/rp2005/`, `data/raw/rp2018/`,
  `data/raw/rp2005-2019/`, and `data/raw/_archives/`.

## Superseded work in the working tree

At `a811b8c` the working tree has an uncommitted, **now superseded** partial
attempt at D4 only:

| Path | State | Superseded by |
| --- | --- | --- |
| `data/README.md` | untracked, hand-written | generated by `byz.build` (R6) |
| `data/text/README.md` | modified | `data/raw/repo/CONVENTIONS.md` (R7) |
| `src/byz/generated.py` | modified: `data/README.md` added to `HAND_MAINTAINED` | generated classification: `GENERATED_MARKDOWN` + `GENERATED_FILES` (R6) |
| `src/byz/contract/inventory.py` | modified: `data/README.md` added to `DOC_FILES` | the 13-entry `DOC_FILES` (R6.6) |
| `tests/curate/test_layout.py` | modified: new hand-written `DataReadmeTests` | generated-README tests (R6.7) |
| `reports/baseline/files.csv` | modified | regenerated by `byz.contract` (R9) |

The hand-written `data/README.md` is useful as **wording input** for the
renderer; it is not the committed artifact. The implementation starts from a
committed base: those six paths are reverted (`git checkout --` for the five
tracked ones, `rm` for the untracked draft after copying it to
`/tmp/opencode/data-README-draft.md`), and phase 0's before-snapshot is taken on
that clean tree. Nothing in this change depends on them.

## Verified inventory

Checked against the working tree at `a811b8c` on 2026-11-25 with Python 3.12.3.
No generator was run. `data/` has **293** tracked files, `editions/` **680**,
the repository **1154**.

### The trees being moved

| Today | Destination | Files | Bytes |
| --- | --- | ---: | ---: |
| `data/text/CCAT/*.TXT` | `data/raw/repo/rp2018-2023/ccat/` | 29 | 1,374,605 |
| `data/text/Strongs/*.BP5` | `data/raw/repo/rp2018-2023/strongs/` | 27 | 2,744,993 |
| `data/text/README.md` | `data/raw/repo/CONVENTIONS.md` (rewritten) | 1 | 14,205 |
| `data/raw/rp2005/editions-rp2-ccat/` | `data/raw/print/rp2005/ccat/` | 29 | 1,400,061 |
| `data/raw/rp2005/editions-rp2-ascii/` | `data/raw/print/rp2005/ascii/` | 27 | 879,851 |
| `data/raw/rp2005/editions-rp2-preformatted/` | `data/raw/print/rp2005/preformatted/` | 27 | 931,153 |
| `data/raw/rp2005/official-pdf/` | `data/raw/print/rp2005/official-pdf/` | 1 | 6,156,568 |
| `data/raw/rp2018/rp2018-ccat/` | `data/raw/print/rp2018/ccat/` | 30 | 1,401,158 |
| `data/raw/rp2018/rp2018-ascii-one-line-per-verse/` | `data/raw/print/rp2018/ascii/` | 27 | 879,847 |
| `data/raw/rp2018/rp2018-ascii/` | `data/raw/print/rp2018/preformatted/` | 27 | 931,149 |
| `data/raw/rp2018/official-pdf/` | `data/raw/print/rp2018/official-pdf/` | 1 | 2,161,630 |
| `data/raw/_archives/{rp2005,rp2018}/` | `data/raw/print/_archives/{rp2005,rp2018}/` | 6 | 2,252,162 |
| `data/raw/rp2005-2019/` | `data/raw/repo/rp2005-2019/` | 57 | 4,426,583 |
| **Total** | | **289** | |

(The 289 includes the four `official-pdf`/`_archives` groups; the manifest input
count stays 226 because the PDFs and the `preformatted/` trees are named, not
hashed, in the manifests.)

### What the current tree says today

| Fact | Check |
| --- | --- |
| The current text is the only input outside `data/raw/` | `data/text/{CCAT,Strongs}`; every other input is `data/raw/...` |
| Four manifests pin 226 inputs and 672 artifacts | `rp2005` 56/141, `rp2005-2019` 57/195, `rp2018` 57/141, `rp2018-2023` 56/195 |
| The current manifest group is `root = "data/text"`, `include = ["CCAT/*.TXT", "Strongs/*.BP5"]` | `editions/rp2018-2023/manifest.json` |
| The current text has no provenance TOML | `data/provenance/` has `pdfs.toml`, `rp2005.toml`, `rp2005-2019.toml`, `rp2018.toml` |
| `pdfs.toml` is hand-maintained and stores local `path` values | `data/provenance/pdfs.toml` (`data/raw/rp2005/official-pdf/...`) |
| The conventions live only in `data/text/README.md` | 168 lines, one file |
| There is no README under `data/` except that one | `git ls-files 'data/**/README.md'` |

### Consumers that name the moved paths (the sweep)

| Consumer | What it does today |
| --- | --- |
| `src/byz/contract/paths.py` 10-14, 100-113 | `DATA_TEXT`, `CCAT_DIR`, `BP5_DIR`, the two dataset names, and the derivation evidence |
| `src/byz/reconcile/sources.py` 7-11 | `ARCHIVE_DIR = data/raw/_archives`, `RAW_DIR = data/raw` |
| `src/byz/reconcile/fetch.py` 271-274, 287 | extraction path from the archive stem; the recorded `extracted` field |
| `src/byz/contract/history.py` 16-32, 37-44, 50-51 | dataset labels, corpus pathspecs, the two commit pathspecs (all `data/text/...`) |
| `src/byz/contract/inventory.py` 111-118 | `DOC_FILES` lists `data/text/README.md` |
| `src/byz/contract/report.py` 75-78, 92-93, 127, 509-512 | `docs/DATA_CONTRACT.md` prose; `data/text/...` in the contract JSON filenames |
| `src/byz/curate/editions.py` 25-28, 55-56, 80-83, 103-104, 107-118 | the registry's input directories and the `rp2018-2023` note |
| `src/byz/curate/materialise.py` 33-39 | `HISTORICAL_INPUT_ROOT = data/raw/rp2005-2019` |
| `src/byz/curate/build.py` 67-71, 77-113, 121-129, 246-283, 725-800, 801-873, 884-950, 953-978, 994-1021, 1024-1067 | reader docstrings, `EXPORT_NOTES`, `build_historical`, `build_current`, `_readme`, `_input_groups`, `_input_tree`, `write_manifest` |
| `src/byz/curate/diff.py` 472, 720 | the `Source` prose in `reports/diffs/README.md` |
| `src/byz/curate/docs.py` 73-86, 118-151, 159-180, 187-204, 247-249, 297-317, 402-410, 426, 474-489, 519, 580, 599, 669-670 | `docs/EDITIONS.md` mapping tables and prose |
| `src/byz/reconcile/compare.py` 18, 179, 362, 374 | comments and the current-text and Strong's readers |
| `src/byz/reconcile/historical.py` 18, 67 | `CURRENT_STATE = "current data/text/CCAT"` and the reader |
| `src/byz/reconcile/report.py` 113, 167, 196-198, 237-239, 300, 306, 365, 388, 434, 495, 498, 501-502, 544 | `docs/PROVENANCE.md` and `reports/reconciliation/*` prose |
| `src/byz/beta/converter.py` 111 | points at `data/text/README.md` for the variant codes |
| `src/byz/generated.py` 41-54, 60-69, 82-182 | the banner lists and the 12-row registry |
| `src/byz/curate/verify.py` 122 | the "root must be under data/" check (unchanged, but re-tested) |
| `data/provenance/rp2005.toml`, `rp2018.toml` | `extracted = "data/raw/<edition>/<stem>"` |
| `data/provenance/rp2005-2019.toml` | `extracted = "data/raw/rp2005-2019"` |
| `data/provenance/pdfs.toml` | the two hand-written `path` values |
| `docs/BUILD.md` 12-28, 30-61, 67-85, 95-126 | the input tree and pipeline sections |
| `README.md` (from `src/byz/curate/README.template.md` 17-23, 43-47, 67-93, 147-163) | layout table, "Which text", "Source of truth", the sequence |
| `SPECS/TECH.md` §2 (80-96), §3 (100-109), §5 (143-190), §7 (222), §9 (280), §11 (320-322) | layout tree, provenance kinds, the parsing pointer |
| `.opencode/**` (10 files: `agents/{build,code-reviewer,plan,spec-implementer,verifier}.md`, `commands/read-conventions.md`, `skills/{feature-specification,fix-typing-linting-issues,investigate-bug,write-tests}/SKILL.md`) | "the source files are `data/text/CCAT`/`Strongs`" |
| `tests/curate/{test_build,test_current_pipeline,test_editions,test_fidelity,test_generated,test_historical_pipeline,test_integration,test_layout,materialise,test_verify}.py`, `tests/contract/{test_coverage,test_integration}.py`, `tests/reconciliation/{test_compare,test_fetch,test_integration,test_offline}.py` | path literals, dataset names, layout sweeps, doc assertions |

### Why the byte gate can be met

Nothing the build reads changes value: the same 56 files, same bytes, read by
`parse_cct_current`/`parse_bp5_strongs`; the same 30+27 and 29+30+27+27 files
for the other editions; the same readers. Only the directory names in the
registry change. `build_current` uses `path.name` and the file contents only, so
a directory rename cannot alter an output byte. `build_official`'s `.CCT` and
ASCII readers likewise. The four `rp2018-2023` `source_commit`/`strongs_commit`
values and the two `pdf` strings are metadata, not text.

## Definitions

- **Source class** - one of the two top-level kinds of input: `print` (published
  by the publisher) and `repo` (this repository's own lineage). Every source tree
  under `data/raw/` belongs to exactly one class.
- **Source snapshot** - one edition's input tree, complete enough that the
  manifest can pin every file: `print/rp2005/`, `print/rp2018/`,
  `repo/rp2005-2019/`, `repo/rp2018-2023/`.
- **Source folder README** - the generated `README.md` inside a source snapshot
  (four files), or the generated class/tree README above it (four more).
- **Input-tree documentation** - the eight generated READMEs plus the
  hand-maintained `data/raw/repo/CONVENTIONS.md`. Nine files.
- **Conventions document** - `data/raw/repo/CONVENTIONS.md`, the single
  hand-maintained authority for Beta code, variant codes (`N/B/C/M/S/E`),
  parsing codes, and Strong's numbers.
- **Artifact byte-identity gate** - the proof that all 672 files under
  `editions/*/{csv,tei}` are unchanged and no file is added or removed.
- **Retired path** - a working-tree path this change removes: `data/text/`,
  `data/raw/rp2005/`, `data/raw/rp2018/`, `data/raw/rp2005-2019/`,
  `data/raw/_archives/`.
- **Input class move** - one row of the old -> new mapping that
  `docs/EDITIONS.md` renders for readers (`docs.INPUT_CLASS_MOVES`).

## Maintainer decisions (fixed requirements)

**D1 - two source classes.** Under `data/raw/`:
`data/raw/print/` holds material from the published print editions
(`rp2005/`, `rp2018/`, each with its CCAT/ASCII extracts and PDF, plus the
committed `_archives/` ZIPs); `data/raw/repo/` holds material from this
repository's own lineage (`rp2005-2019/`, `rp2018-2023/`). Subfolders are named
consistently in lower case: `ccat/`, `strongs/`, `ascii/`, `preformatted/`,
`textonly-beta-code/`, `parsed/`. Exact placement and justification: D7.

**D2 - the current text becomes a source snapshot.** `data/text/CCAT` and
`data/text/Strongs` move to `data/raw/repo/rp2018-2023/ccat/` and
`.../strongs/`, so the current text is treated exactly like
`data/raw/rp2005-2019/`. There is no top-level `data/text/` afterwards.

**D3 - shared conventions live with the repository lineage.** The Beta-code,
variant-code, parsing, and Strong's conventions in `data/text/README.md` move
into one hand-maintained document inside `data/raw/repo/`
(`data/raw/repo/CONVENTIONS.md`). The maintainer does not assume these
conventions describe the print sources, so the document belongs to the `repo`
class and both `rp2005-2019/` and `rp2018-2023/` link to it. Dr Robinson's prose
stays intact; links are adjusted for the new depth.

**D4 - generated READMEs for `data/` and every subfolder.** `data/README.md`,
`data/raw/README.md`, `data/raw/print/README.md`, `data/raw/repo/README.md`,
and a README in each source folder (`print/rp2005/`, `print/rp2018/`,
`repo/rp2005-2019/`, `repo/rp2018-2023/`) are generated by extending
`byz.build`. Each states what the folder holds, file counts and where they come
from, which edition consumes the source, the provenance record, the relevant
command, and links to sibling/parent docs. They carry the generated-file banner
and are covered by the classification/registry machinery in `src/byz/generated.py`.
The hand-maintained `CONVENTIONS.md` is the exception: no banner.

**D5 - provenance for `rp2018-2023`.** Add `data/provenance/rp2018-2023.toml`
with the same shape as `rp2005-2019.toml`: it is repo lineage (no external
archive), and it records the revision (2023-07-20), the commit(s) that last
touched the sources, and a SHA-256 per file.

## Decisions this spec finalises

The brief leaves these open. They are adopted throughout; the maintainer may
reject any of them, in which case the referenced requirements change (see
"Open questions" at the end).

**D6 - the exact tree.** Adopt the tree in "The chosen tree" below. `data/raw/`
contains exactly two class directories, `print/` and `repo/`. Rationale: the
first level under `data/raw/` answers the only question a reader has - "is this
published, or ours?" - and every source tree keeps its edition id directly under
its class.

**D7 - placement of `_archives/` and the PDFs.** Both belong to the print class.

- `data/raw/print/_archives/{rp2005,rp2018}/` keeps the six published ZIPs. All
  six are published print-edition material; they are the download source for
  `print/rp2005/` and `print/rp2018/`, and `repo/` contains no download at all.
  Keeping them under `print/` is what makes the class boundary true rather than
  decorative.
- `data/raw/print/<edition>/official-pdf/` keeps each PDF beside the extracts of
  the same printed edition. The folder name is unchanged; only the `print/`
  segment is inserted. `docs/PROVENANCE.md`, `docs/EDITIONS.md`, and the edition
  READMEs already link these files, and `data/provenance/pdfs.toml` already
  records their local paths - so this is one path segment, not a new concept.

**D8 - subfolder naming.** Every source folder uses the lower-case names in
D1: `ccat/` for accented Beta-code with variants (`.CCT` and `.TXT`), `strongs/`
for parsed Strong's/BP5, `ascii/` for the official one-line-per-verse ASCII
(`*_Byz.txt`), `preformatted/` for the official preformatted ASCII (`.ASC`), and
the tag names `textonly-beta-code/` and `parsed/` unchanged for the 2019
lineage. This renames six extract directories and the current text's two
directories. File names keep their case (`01_MAT.TXT`, `01_MAT.BP5`,
`MR.CCT`); only directories change. D2's parenthetical "its `CCAT/` and
`Strongs/` directories" identifies *which* directories move; D1's naming rule
fixes their names.

**D9 - archive extraction is mapped by format, not by archive stem.** Because
the extract directories no longer carry the archive names, `sources.ARCHIVES`
gains one canonical mapping `FORMAT_DIRS = {"ccat": "ccat",
"ascii-one-line": "ascii", "preformatted": "preformatted"}` and
`fetch.run()` extracts to `PRINT_DIR / edition / FORMAT_DIRS[spec["format"]]`.
It asserts the mapping is unambiguous per `(edition, format)`. The recorded
`extracted` value in `rp2005.toml`/`rp2018.toml` follows. No per-archive literal
is added.

**D10 - `byz.build` writes the input READMEs and the current-text provenance.**
`src/byz/build.py::main` calls a new renderer after `build.build_all()` and
`docs.write_editions_doc()`, because the counts come from the manifests that run
just produced. The `rp2018-2023` provenance TOML is written by
`build.write_manifest` (it already hashes every input and looks up the commits),
so the manifest and the provenance cannot disagree. `byz.materialise` keeps
writing the 2019 record from the tag; no command gains a new role.

**D11 - the retired-path guard.** `tests/curate/test_layout.py`'s
`RetiredLayoutSweepTests` gains patterns for the five retired roots and an
explicit allowlist (the mapping table, the git pathspecs, and the tests that
assert absence). A second test asserts the five retired directories do not
exist.

**D12 - the migration mapping lives in `docs/EDITIONS.md`.** The existing
2026-11-21 and 2026-11-25 mapping sections stay as history. A new section
`## Where the inputs moved into the print and repo classes (2026-11-25)`
renders `docs.INPUT_CLASS_MOVES` (the 13 move rows plus the two consequences:
the `pdfs.toml` `path` and the manifest `pdf` key). No reader-facing doc sends a
user to a retired path; no compatibility shim is added.

## The chosen tree

```
data/
├── README.md                              generated
├── provenance/
│   ├── pdfs.toml                           hand-maintained (path values edited)
│   ├── rp2005.toml                         generated by byz.fetch
│   ├── rp2005-2019.toml                    generated by byz.materialise
│   ├── rp2018.toml                         generated by byz.fetch
│   └── rp2018-2023.toml                    NEW, generated by byz.build
└── raw/
    ├── README.md                          generated
    ├── print/
    │   ├── README.md                      generated
    │   ├── _archives/
    │   │   ├── rp2005/{editions-rp2-ccat,editions-rp2-ascii,editions-rp2-preformatted}.zip
    │   │   └── rp2018/{rp2018-ccat.ZIP,rp2018-ascii.zip,rp2018-ascii-one-line-per-verse.zip}
    │   ├── rp2005/
    │   │   ├── README.md                  generated
    │   │   ├── ccat/*.CCT                 29
    │   │   ├── ascii/*_Byz.txt            27
    │   │   ├── preformatted/*.ASC         27
    │   │   └── official-pdf/editions-rp2.pdf
    │   └── rp2018/
    │       ├── README.md                  generated
    │       ├── ccat/*.CCT                 30
    │       ├── ascii/*_Byz.txt            27
    │       ├── preformatted/*.ASC         27
    │       └── official-pdf/robinson-pierpont-2018-gnt-edition.pdf
    └── repo/
        ├── README.md                      generated
        ├── CONVENTIONS.md                 HAND-MAINTAINED, no banner
        ├── rp2005-2019/
        │   ├── README.md                  generated
        │   ├── textonly-beta-code/*.CCT   30
        │   └── parsed/*.UB5               27
        └── rp2018-2023/
            ├── README.md                  generated
            ├── ccat/*.TXT                 29
            └── strongs/*.BP5              27
```

Tracked totals: `data/` goes from 293 to **302** (`+8` READMEs `+1` provenance
TOML; the moved `data/text/README.md` becomes `CONVENTIONS.md`, a rename).
`editions/` stays 680 and the repository becomes **1163**.

## Requirements

### R1 - The print class (D1, D6, D7, D8)

1. `data/raw/print/` exists with exactly `_archives/`, `rp2005/`, `rp2018/`,
   `README.md`. `data/raw/rp2005/`, `data/raw/rp2018/`, and
   `data/raw/_archives/` do not exist.
2. The moves in "Verified inventory" are `git mv` operations: every moved file
   keeps its bytes and its git history. Directory names are the ones in D8; no
   file is renamed.
3. `data/raw/print/rp2005/` contains `ccat/` (29 `.CCT`), `ascii/` (27
   `*_Byz.txt`), `preformatted/` (27 `.ASC`), `official-pdf/` (one PDF), and the
   generated README. `data/raw/print/rp2018/` is the same with `ccat/` = 30.
4. `data/raw/print/_archives/{rp2005,rp2018}/` holds the six committed ZIPs
   under their published names. `byz.fetch --verify` passes with no network and
   no writes.
5. `src/byz/reconcile/sources.py` gains `PRINT_DIR = ROOT/"data"/"raw"/"print"`
   and `REPO_DIR = ROOT/"data"/"raw"/"repo"`, redefines
   `ARCHIVE_DIR = PRINT_DIR/"_archives"`, keeps `ROOT`, and owns `FORMAT_DIRS`
   (D9). No module outside `sources.py` builds a print path by hand.
6. `src/byz/reconcile/fetch.py` extracts to
   `PRINT_DIR / edition / FORMAT_DIRS[spec["format"]]`, asserts the mapping is
   unique per `(edition, format)`, and records that path in `extracted`.
7. Re-running `byz.fetch` in record mode changes **only** the `extracted` lines
   of `data/provenance/rp2005.toml` and `rp2018.toml`; `downloaded`,
   `final_url`, `http_status`, `sha256`, and `size` are unchanged. `--force` is
   not run.

### R2 - The repo class and the current text (D2, D6, D8)

1. `data/raw/repo/` exists with exactly `CONVENTIONS.md`, `README.md`,
   `rp2005-2019/`, `rp2018-2023/`. `data/text/` and
   `data/raw/rp2005-2019/` do not exist; `git ls-files data/text` is empty.
2. `data/raw/repo/rp2018-2023/ccat/` has 29 `.TXT` and `strongs/` has 27
   `.BP5`, byte identical to the pre-change `data/text/CCAT`/`Strongs`.
3. `data/raw/repo/rp2005-2019/` has 30 `textonly-beta-code/*.CCT` and 27
   `parsed/*.UB5`, byte identical to the pre-change tree and to
   `git archive v2.0.3`.
4. `src/byz/curate/editions.py` registers the new directories for all four
   editions, adds `"input_class"` (`"print"` for `rp2005`/`rp2018`, `"repo"`
   for `rp2005-2019`/`rp2018-2023`), and adds
   `"revision": "2023-07-20"` to `rp2018-2023`. A test asserts each
   registration is inside its class directory.
5. `src/byz/curate/materialise.py` writes
   `HISTORICAL_INPUT_ROOT = "data/raw/repo/rp2005-2019"` and records it as
   `extracted`; the tag, commit, `method`, the two prefix names, the 57
   `[[files]]` blocks, and their hashes are unchanged. A second run writes no
   byte.

### R3 - Provenance for `rp2018-2023` (D5, D10)

1. `data/provenance/rp2018-2023.toml` exists, starts with
   `generated.toml_header()`, and contains:
   - `edition = "rp2018-2023"`;
   - `revision = "2023-07-20"`;
   - `method = "working-tree snapshot"`;
   - `extracted = "data/raw/repo/rp2018-2023"`;
   - `generated_by = "PYTHONPATH=src python3 -m byz.build"`;
   - `ccat_commit` and `strongs_commit`: the full 40-hex hash of the last
     commit touching `data/raw/repo/rp2018-2023/ccat` and `.../strongs`
     respectively, looked up with the pre-move pathspecs as well (R4.4);
   - one `[[prefixes]]` block per directory (`ccat/` 29, `strongs/` 27), sorted
     by `path`;
   - one `[[files]]` block per file, sorted by `path`, with `path`, `sha256`,
     and `size`.
2. It has no URL, no `downloaded` field, no timestamp, and no absolute path.
3. Every `sha256` and `size` equals `src/byz/curate/files.py`'s hash of the
   committed file, and the file set equals the `rp2018-2023` manifest's input
   files. A test asserts both directions.
4. `build.write_manifest` writes it for the `current` edition only, from the
   same input groups it just pinned, and from `history.CCAT_COMMIT_PATHSPECS`
   / `STRONGS_COMMIT_PATHSPECS`. It is written after the manifest, so a failed
   build cannot leave a provenance record for a manifest that was not written.
5. A second `byz.build` writes no byte. The recorded commits may move once when
   the move commit lands (exactly as the manifest's `source_commit` does); this
   is the known one-commit lag, recorded in `validation.md`, not a determinism
   failure.

### R4 - Path constants and the consumer sweep (D6)

1. `src/byz/contract/paths.py` derives every current-text path from one pair:

   ```python
   REPO_DIR = ROOT / "data" / "raw" / "repo"
   CURRENT_INPUT_DIR = REPO_DIR / "rp2018-2023"
   CCAT_DIR = CURRENT_INPUT_DIR / "ccat"
   BP5_DIR = CURRENT_INPUT_DIR / "strongs"
   CCAT_DATASET = "data/raw/repo/rp2018-2023/ccat"
   BP5_DATASET = "data/raw/repo/rp2018-2023/strongs"
   ```

   `DATA_TEXT` is deleted. `DERIVATION_EVIDENCE` names the new directories. No
   module outside `paths.py` builds a current-text dataset name by hand.
2. The two dataset names change everywhere they are derived: the contract
   dataset set, `reports/baseline/{files,books,differences,derivations}.csv`,
   `reports/reconciliation/{files,verses,history}.csv`, `docs/DATA_CONTRACT.md`,
   `docs/HISTORY.md`, `docs/PROVENANCE.md`, and the `docs/contract/*.json`
   filenames (`data__text__CCAT.json`/`data__text__Strongs.json` are deleted;
   `data__raw__repo__rp2018-2023__ccat.json` and `...__strongs.json` appear).
3. `src/byz/contract/history.py` keeps the pre-move git selectors and adds the
   new ones, so pre-move history stays visible:
   `CCAT_COMMIT_PATHSPECS = ("source/CCAT", "data/text/CCAT",
   "data/raw/repo/rp2018-2023/ccat")`, the same for Strong's, and
   `CORPUS_PATHSPECS` gains `data/raw/repo`. `DATASETS` labels follow
   `paths.CCAT_DATASET` / `paths.BP5_DATASET`. A comment says these are git
   selectors, not working-tree paths.
4. `src/byz/reconcile/historical.py`'s `CURRENT_STATE` and every consumer that
   looks it up by string change together (one constant pair, no duplicated
   literals): `"current data/raw/repo/rp2018-2023/ccat"`.
5. `src/byz/curate/build.py`: the reader docstrings, `EXPORT_NOTES["current"]`,
   `build_current`'s labels, and `_check_source_books` messages name the new
   directories. `_input_groups` keeps its shape: the current group's root becomes
   `data/raw/repo/rp2018-2023` with includes `ccat/*.TXT`, `strongs/*.BP5`; the
   historical root becomes `data/raw/repo/rp2005-2019`; the official roots gain
   `print/`.
6. `src/byz/curate/diff.py`, `src/byz/curate/docs.py`,
   `src/byz/contract/report.py`, `src/byz/reconcile/{compare,report}.py`, and
   `src/byz/beta/converter.py` follow the sweep table above. No behavioural
   change: labels, comments, and generated prose only.

### R5 - Manifests and `byz.verify`

1. `byz.build` writes the four manifests with the new `inputs` roots. For
   `rp2005` and `rp2018` the group roots are
   `data/raw/print/<edition>/{ccat,ascii}`; for `rp2005-2019`
   `data/raw/repo/rp2005-2019`; for `rp2018-2023`
   `data/raw/repo/rp2018-2023` with the two new includes.
2. The same 226 input files are pinned, with the same `sha256` and `size`. The
   only input-side differences are `root`, the `files[].path` prefix for
   `rp2018-2023` (`CCAT/…` -> `ccat/…`, `Strongs/…` -> `strongs/…`, because
   that group's root is now the snapshot directory), and, for `rp2018-2023`,
   the two `include` globs.
3. `artifact_files` is byte-for-byte the same list in all four manifests.
4. The only other manifest keys allowed to change are: `pdf` for `rp2005` and
   `rp2018` (one `print/` segment), `ascii_source`/`preformatted_source` for
   the two official editions (those keys record the moved extract
   directories), `note` for `rp2005-2019` and `rp2018-2023` (they name the
   input paths), and `source_commit`/`strongs_commit` for `rp2018-2023` (new
   pathspecs; the recorded commit moves to the move commit until the next
   content edit). `pdf_sha256`, `pdf_size`, `tag`, `commit`, `generated_by`,
   `basis`, `status`, `release_range`, and every other key are unchanged.
5. `byz.verify` needs no logic change: its `data/`-prefix and
   `editions/`-exclusion checks already cover the new roots. It must exit 0 and
   print `verified 4 editions (226 inputs, 672 artifacts)`.
6. `editions/rp2005/README.md` and `editions/rp2018/README.md` link their PDF at
   the new path; the `pdf` key and the link must agree (a test compares them).

### R6 - Generated input-tree READMEs (D4, D10)

1. `byz.build` writes exactly these eight Markdown files, each with the
   full-file banner from `generated.write_markdown`:
   `data/README.md`, `data/raw/README.md`, `data/raw/print/README.md`,
   `data/raw/repo/README.md`, `data/raw/print/rp2005/README.md`,
   `data/raw/print/rp2018/README.md`,
   `data/raw/repo/rp2005-2019/README.md`,
   `data/raw/repo/rp2018-2023/README.md`. Each is the only `README.md` in its
   folder.
2. The renderer is a new module `src/byz/curate/data_docs.py` called from
   `src/byz/build.py::main` after `build_all()`; it never reads the filesystem
   for counts except through the two helpers below, and it never formats a date,
   a host name, or a path with `str(ROOT)`.
3. The content model ("README content model" below) is implemented by four
   render functions - `render_data_readme`, `render_raw_readme`,
   `render_class_readme(kind)`, `render_source_readme(edition_id)` - plus shared
   helpers `_group_count(manifest, root)` and `_tracked_count(relative_dir,
   pattern)`. Every list and table is sorted; the same manifests produce the same
   bytes.
4. `src/byz/curate/files.py` gains `tracked_count(relative_dir, pattern="*")`,
   implemented over `git ls-files -z -- <relative_dir>` (it raises a
   `RuntimeError` naming the command when git is unavailable, like
   `contract.inventory.tracked_paths`). It is used only for the directories the
   manifests do not pin (`preformatted/`, `official-pdf/`); every pinned count
   comes from the manifest, so an untracked file cannot change a generated
   count.
5. `src/byz/generated.py`:
   - `GENERATED_MARKDOWN` gains the eight README patterns (18 -> 26 files);
   - `GENERATED_FILES` gains one row for the input-tree READMEs and the new
     provenance record, and the existing materialiser row's label/patterns move
     to `data/raw/repo/rp2005-2019/` (registry 12 -> 13 rows);
   - `HAND_MAINTAINED` drops `data/README.md` and `data/text/README.md` and gains
     `data/raw/repo/CONVENTIONS.md`;
   - `HAND_MAINTAINED_DOCS` gains `data/raw/repo/CONVENTIONS.md`.
6. `src/byz/contract/inventory.py` `DOC_FILES` becomes: `README.md`, `LICENSE`,
   `data/README.md`, `data/raw/README.md`, `data/raw/print/README.md`,
   `data/raw/repo/README.md`, `data/raw/print/rp2005/README.md`,
   `data/raw/print/rp2018/README.md`,
   `data/raw/repo/rp2005-2019/README.md`,
   `data/raw/repo/rp2018-2023/README.md`, `data/raw/repo/CONVENTIONS.md`,
   `essay/README.md`, `docs/BUILD.md`. (`data/text/README.md` is gone.)
7. `BannerScopeTests.test_every_markdown_under_generated_trees_is_classified`
   scans `data/` as well as `docs/`, `editions/`, and `reports/`, and still
   asserts that the found set equals `GENERATED_MARKDOWN ∪
   HAND_MAINTAINED_DOCS`. `tests/curate/test_layout.py::DataReadmeTests`
   (uncommitted draft) is deleted and replaced by the generated-README tests.
8. A new `tests/curate/test_data_docs.py` asserts, for all eight files: the
   banner is the first line; the required skeleton headings are present; the
   folder's own path appears; the consuming edition id, the provenance record
   path, and the relevant command appear where the content model requires them;
   every relative Markdown link resolves; regenerating twice is byte identical;
   no timestamp, host name, or absolute path appears; and dropping an untracked
   file into an auxiliary directory does not change a pinned count.

### R7 - The conventions document (D3)

1. `data/raw/repo/CONVENTIONS.md` exists and is hand-maintained: it is listed in
   `generated.HAND_MAINTAINED` and `HAND_MAINTAINED_DOCS`, carries no
   generated-file banner, and is not matched by any `GENERATED_FILES` pattern.
2. Its body keeps Dr Robinson's prose intact. Every line from the pre-change
   `data/text/README.md`'s `## Variant codes` heading onwards appears unchanged,
   except the directory names in prose (`CCAT`/`Strongs` -> `ccat/`/`strongs/`).
   The proof is a diff in `validation.md`, not a paraphrase.
3. It gains a short preamble that says: this document holds the conventions for
   the repository-lineage Beta-code sources
   (`data/raw/repo/rp2018-2023/`, `data/raw/repo/rp2005-2019/`); it is not
   asserted for the print-edition `.CCT`/ASCII extracts under
   `data/raw/print/`, whose own conventions are the publisher's; and it is the
   authority for variant codes, parsing codes, and Strong's numbers referenced by
   `src/byz/beta/converter.py`.
4. The maintainer-authored framing of `data/text/README.md` (which text the
   folder holds, "not a copy of the official files", the input/output rule, the
   PDFs-are-truth sentence) moves into the generated
   `data/raw/repo/rp2018-2023/README.md`; it is not duplicated in
   `CONVENTIONS.md`.
5. The moved body carries no relative link to rewrite: its only link is the
   external 2009 parsing document (`https://github.com/byztxt/...`), which stays
   exactly as it is. Any relative link the new preamble adds is written from
   `data/raw/repo/` (`../README.md` for the `data/raw/` index, `rp2018-2023/`,
   `rp2005-2019/`, and `../../../docs/EDITIONS.md` for the repository docs), and
   `tests/curate/test_editions.py`'s link check covers the file.
6. `data/text/README.md` does not exist. No tracked file points at it except the
   mapping table and the retired-path test.

### R8 - Public docs, `SPECS/TECH.md`, and agent instructions

1. `src/byz/curate/README.template.md`: the layout table's `data/` row names
   `raw/print/` and `raw/repo/`; the intro, "Start here", "Source of truth and
   provenance", "Which text should I use?", and the command block use the new
   paths; the paragraph on `byz.materialise` names
   `data/raw/repo/rp2005-2019/`; a new sentence explains the print/repo split
   and links to the generated `data/README.md`.
2. `docs/BUILD.md`: "The input tree" becomes a print/repo table with the new
   paths and the eight READMEs; "The pipeline" says `byz.build` also writes the
   input READMEs and `data/provenance/rp2018-2023.toml`; "Verifying the
   editions" keeps its text (inputs still 226); "Report generation order" names
   `data/raw/print/_archives/`.
3. `data/provenance/pdfs.toml` (hand-maintained): the two `path` values gain
   `print/`. Nothing else changes; the hashes and sizes are unchanged.
4. `src/byz/curate/docs.py`: the existing `MOVED_PATHS` and `SNAPSHOT_MOVES`
   stay as history (the `data/text/` row now points at
   `data/raw/repo/rp2018-2023/`); a new `INPUT_CLASS_MOVES` renders
   `## Where the inputs moved into the print and repo classes (2026-11-25)`;
   the source feature matrix, the "Source" prose, the layout section, the
   rebuild block, and the curated-editions section name the new paths. The
   section links `editions/<id>/manifest.json` roots, not the retired ones.
5. `docs/EDITIONS.md` is regenerated with that section, every
   `INPUT_CLASS_MOVES` row, and the note that no compatibility shim exists.
6. `SPECS/TECH.md`: §2's `data/text/...` references become the repo paths and
   §2 gains the print/repo split; §3 records two repo provenance records and the
   provenance kinds (`official archive`, `published PDF`, `git tag`,
   `working-tree snapshot`); §5's layout tree is replaced by "The chosen tree"
   above plus a print/repo paragraph; §7's parsing-code pointer names
   `data/raw/repo/CONVENTIONS.md`; §9 keeps `byz.verify`; §11 states that the
   input tree has two classes and that `byz.build` writes the input READMEs and
   the current-text provenance.
7. `.opencode/**` (the ten files listed in the sweep table): every
   `data/text/CCAT`/`data/text/Strongs`/`data/text/README.md` reference becomes
   `data/raw/repo/rp2018-2023/{ccat,strongs}` and
   `data/raw/repo/CONVENTIONS.md`; `read-conventions.md` names the new
   conventions document first; `build.md` states that `byz.build` writes the
   edition outputs and the input-tree READMEs; no agent instruction claims the
   print extracts follow the repo conventions.
8. `src/byz/beta/converter.py:111` points at `data/raw/repo/CONVENTIONS.md`.

### R9 - The retired-path guard and the migration mapping (D11, D12)

1. `tests/curate/test_layout.py::RetiredLayoutSweepTests` gains narrow patterns
   for `data/text/`, `data/raw/rp2005/`, `data/raw/rp2018/`,
   `data/raw/rp2005-2019/`, and `data/raw/_archives/`, with a lookbehind so the
   new paths (`data/raw/repo/rp2005-2019/`, `data/raw/print/rp2005/`) do not
   match. `RETIRED_ALLOWED` gains exactly the files that must name them:
   - `docs/EDITIONS.md` - renders the mapping;
   - `docs/HISTORY.md` - prints historical commit subjects, which may name the
     old path;
   - `src/byz/curate/docs.py` - holds the mapping constants;
   - `src/byz/contract/history.py` - holds the git selectors;
   - `src/byz/reconcile/historical.py`, `src/byz/reconcile/report.py` - paths
     inside tags and the generated decision log;
   - `tests/curate/test_layout.py`, `tests/curate/test_current_pipeline.py`,
     `tests/curate/test_editions.py` - the guard's own needles and the absence
     assertions.

   A generated report that still names a retired path is a generator bug: fix
   the renderer and regenerate; do not add the report to the allowlist.
2. A new test asserts the five retired directories do not exist and that
   `git ls-files data/text data/raw/rp2005 data/raw/rp2018
   data/raw/rp2005-2019 data/raw/_archives` is empty.
3. `docs/EDITIONS.md` renders `INPUT_CLASS_MOVES` with one row per moved tree
   plus the two consequences (`pdfs.toml` `path`, the manifest `pdf` key), and
   one sentence that paths were not aliased.
4. `tests/curate/test_editions.py::DocsTests` asserts the new section, every
   row, and the absence of a compatibility claim, plus the new PDF link paths in
   `PdfLinkTests`.

### R10 - Byte identity, determinism, and tests

1. All 672 files under `editions/*/{csv,tei}` are byte identical to the
   pre-change tree; no file is added or removed. This includes `rp2005-2019`.
2. Every `artifact_files` entry in every manifest keeps `path`, `sha256`, and
   `size`; the allowed manifest differences are exactly R5.4's list.
3. The diff reports' data files are byte identical:
   `reports/diffs/<pair>/{changes.csv,source.diff,text.diff,apparatus.diff,
   derived.diff}` for all four pairs, with the same row counts and categories.
   The prose changes are confined to one line: every
   `reports/diffs/<pair>/report.md` Notation bullet and `reports/diffs/README.md`
   name the current source path (R4.6), so the five `report.md`/`README.md`
   files differ in that sentence only.
4. No input byte changes: the 289 moved files, the six archives, the two PDFs,
   and the three existing provenance records keep their SHA-256 except the
   `extracted` lines of `rp2005.toml`/`rp2018.toml` and the `extracted` line of
   `rp2005-2019.toml`.
5. A second full regeneration is byte identical: no timestamp, host name, or
   absolute path appears in any generated file (including the eight READMEs and
   `data/provenance/rp2018-2023.toml`).
6. The three suites pass, including the worktree-based
   `tests/curate/test_reproducible.py` after the change commit and the usual
   regeneration follow-up(s). The one-commit lag for the recorded commit values
   is expected and recorded.
7. New tests are red before their phase and green after; no test touches the
   network; no test writes to the repository (temporary roots only).

## README content model

Every generated README uses the same skeleton, in this order. Optional rows are
marked; the required set is asserted per file.

```
# <Title>                                   <- plain H1 naming the folder
## What this folder holds                    <- 1-3 sentences
## Contents                                  <- table: Folder | Files | Contents | Feeds
## <Edition | Classes>                        <- one class section
## Provenance                                 <- record path + recorded facts
## Commands                                   <- fenced bash block
## Related                                    <- relative links
```

| README | What it says | Facts and their source |
| --- | --- | --- |
| `data/README.md` | `data/` is every input; it has two classes and `provenance/`; editions contain outputs only; the conventions live in `data/raw/repo/CONVENTIONS.md` | class table static; per-class file totals from the manifests' `inputs` counts (226 inputs: 113 print, 113 repo); provenance rows static + `data/provenance/` listing by name; commands `fetch`, `materialise`, `build`, `verify` |
| `data/raw/README.md` | what distinguishes `print/` (published, downloaded, checksummed) from `repo/` (this repository's lineage); which edition each class feeds | class definitions static; child table (4 source folders + `_archives/`) with counts from the manifests and `sources.ARCHIVES`; edition ids from `editions.EDITIONS[*]["input_class"]` |
| `data/raw/print/README.md` | print material: two editions, the six published ZIPs, which archive produced which folder, the PDFs | counts: `ccat`/`ascii` from the manifests, `preformatted` from `files.tracked_count`, `_archives` from `sources.ARCHIVES` per edition, `official-pdf` = 1 from the registry's `pdf`; archive names from `sources.ARCHIVES`; command `byz.fetch --verify` / `byz.fetch` |
| `data/raw/repo/README.md` | repository lineage: the 2019 tag snapshot and the current text; both are inputs to `byz.build`; the conventions document is shared | counts from the manifests; `rp2005-2019` tag/commit from `editions.EDITIONS`; `rp2018-2023` revision from the registry; commands `byz.materialise`, `byz.build`, `byz.verify`; link to `CONVENTIONS.md` |
| `data/raw/print/rp2005/README.md` | the 2005 print sources; what each subfolder is; which archive it came from; the PDF | counts from the `rp2005` manifest for `ccat`/`ascii`; `preformatted` by `tracked_count`; `official-pdf` = 1; archives for `rp2005` from `sources.ARCHIVES`; PDF path from the registry's `pdf`, `pdf_sha256` from the manifest just written, publisher from the registry's `basis`; provenance `data/provenance/{rp2005,pdfs}.toml`; consumer `editions/rp2005/` |
| `data/raw/print/rp2018/README.md` | the same for 2018 (the 2018 `_Byz.txt` comes from `rp2018-ascii-one-line-per-verse.zip`; the `.ASC` from `rp2018-ascii.zip`) | as above; the archive-to-folder row makes the two 2018 ASCII archives explicit |
| `data/raw/repo/rp2005-2019/README.md` | the 2019 lineage restored from tag `v2.0.3`; it is an input, and the edition is regenerated from it, not copied from the release | counts from the manifest (30/27); tag, commit, `method`, `generated_by` from `editions.EDITIONS`/`materialise` constants; provenance `data/provenance/rp2005-2019.toml`; command `byz.materialise`; link to `../CONVENTIONS.md` |
| `data/raw/repo/rp2018-2023/README.md` | the maintained current text (RP2018 + 2023 adjustments); the repository's own input; its conventions link | counts from the manifest (29/27); `revision` 2023-07-20, `ccat_commit`/`strongs_commit` from the registry/provenance writer; provenance `data/provenance/rp2018-2023.toml`; commands `byz.build`, `byz.verify`; link to `../CONVENTIONS.md` |

Rules for the renderer:

1. **Counts are never scraped from a directory.** A pinned count is
   `len(group["files"])` from the manifest this run wrote; an auxiliary count is
   `files.tracked_count(...)`; an archive count is `len(sources.ARCHIVES)` for
   that edition. This is why D4's counts cannot drift from `byz.verify`.
2. **Facts are read from the registry, not parsed from a TOML.** The provenance
   TOMLs are written by three different commands; the README states the path and
   the facts the registry already knows (tag, commit, revision, PDF name/hash).
   It never claims to have validated a TOML.
3. **No dates but the recorded revision.** The only date a README may print is
   `2023-07-20` (the registry's `revision`) and, where it is a historical fact,
   the tag name. No build time.
4. **Links are relative and checked.**
   `tests/curate/test_editions.py::PdfLinkTests._user_docs` gains the eight
   READMEs and `CONVENTIONS.md`.
5. **Uniform skeleton, level-specific content.** `## Edition` appears in a source
   README; `## Classes` in `data/raw/README.md`; both `data/README.md` and the
   class READMEs use `## Contents`. Tests assert the skeleton per file rather
   than a single global template, so a level can add a row without a false
   failure.

## Breaking changes

| Retired | Replacement |
| --- | --- |
| `data/text/CCAT/`, `data/text/Strongs/` | `data/raw/repo/rp2018-2023/{ccat,strongs}/` |
| `data/text/README.md` | `data/raw/repo/CONVENTIONS.md` |
| `data/raw/rp2005/` | `data/raw/print/rp2005/{ccat,ascii,preformatted,official-pdf}/` |
| `data/raw/rp2018/` | `data/raw/print/rp2018/{ccat,ascii,preformatted,official-pdf}/` |
| `data/raw/rp2005-2019/` | `data/raw/repo/rp2005-2019/` |
| `data/raw/_archives/` | `data/raw/print/_archives/` |
| manifest `inputs[].root` `data/text` | `data/raw/repo/rp2018-2023` with `ccat/*.TXT`, `strongs/*.BP5` |
| `pdfs.toml` `path` `data/raw/<edition>/official-pdf/` | `data/raw/print/<edition>/official-pdf/` |
| dataset names `data/text/CCAT`, `data/text/Strongs` | `data/raw/repo/rp2018-2023/ccat`, `.../strongs` |
| the contract JSON files `data__text__CCAT.json`, `data__text__Strongs.json` | `data__raw__repo__rp2018-2023__ccat.json`, `...__strongs.json` |
| no README in `data/` | eight generated READMEs (one hand-maintained `CONVENTIONS.md`) |

No shims, no symlinks, no duplicated trees. The mapping is rendered in
`docs/EDITIONS.md`.

## Acceptance criteria

- `data/raw/` contains exactly `README.md`, `print/`, `repo/`; `print/`
  contains `README.md`, `_archives/`, `rp2005/`, `rp2018/`; `repo/` contains
  `README.md`, `CONVENTIONS.md`, `rp2005-2019/`, `rp2018-2023/`. None of
  `data/text/`, `data/raw/rp2005/`, `data/raw/rp2018/`,
  `data/raw/rp2005-2019/`, or `data/raw/_archives/` exists.
- The 289 moved files are byte identical to their pre-change counterparts and to
  the archive extracts; `git ls-files data` is 302 and the repository 1163.
- The eight generated READMEs and `data/provenance/rp2018-2023.toml` exist,
  carry the banner (except the hand-maintained `CONVENTIONS.md`), contain the
  content model's sections, resolve every relative link, and a second build
  leaves them byte identical.
- `data/provenance/rp2018-2023.toml` records `revision = "2023-07-20"`, the two
  source commits, two prefix blocks (29/27), and 56 sorted file blocks whose
  hashes match `byz.files.sha256_file`.
- Every manifest's `inputs` roots are under `data/` and resolve; every
  `files[].path`/`sha256`/`size` is unchanged; `artifact_files` is byte
  identical to the pre-change list in all four editions; the only other changed
  keys are R5.4's.
- `byz.verify` exits 0 and reports `verified 4 editions (226 inputs, 672
  artifacts)`; passing `rp2018-2023` alone also exits 0.
- All 672 `editions/*/{csv,tei}` files are byte identical; no file added or
  removed. Every pair's `reports/diffs/<pair>/{changes.csv,*.diff}` is byte
  identical, and the only report prose that changes is the current-source line
  in each `report.md` and in `reports/diffs/README.md`.
- No tracked text file names `data/text/`, `data/raw/rp2005/`,
  `data/raw/rp2018/`, `data/raw/rp2005-2019/`, or `data/raw/_archives/` outside
  the documented allowlist; `docs/EDITIONS.md` renders every
  `INPUT_CLASS_MOVES` row.
- The full sequence runs twice with no diff; no generated file has a timestamp,
  host name, or absolute path; the three suites pass after the change commit and
  the regeneration follow-up.
- `README.md`, `docs/BUILD.md`, `docs/EDITIONS.md`, `docs/PROVENANCE.md`,
  `docs/DATA_CONTRACT.md`, `SPECS/TECH.md`, and `.opencode/**` describe the two
  classes and never send a reader to a retired path.

## Risks

- **The byte gate is the honest seam.** A one-byte change in any of the 672
  files means a path or reader changed behaviour. Stop and report; do not
  regenerate until it looks right.
- **`git mv` and history.** Using `cp`/`rm` instead of `git mv` loses the rename
  detection and changes `last_commit` in ways that are hard to reason about; the
  plan uses `git mv` only. `reports/baseline/files.csv` still records new
  `last_commit` values for the 57 current-text files (the move commit), which is
  expected churn.
- **Two `ccat` meanings.** `print/<edition>/ccat` holds `.CCT` (mixed-case,
  apparatus) while `repo/rp2018-2023/ccat` holds `.TXT` (all-lowercase). They
  are not interchangeable: `parse_cct_accented` and `parse_cct_current` are
  different readers. The READMEs and `CONVENTIONS.md` must say which reader
  serves which tree, or a future contributor will "unify" them.
- **Conventions scope.** D3 exists because the repo conventions are not asserted
  for the print sources. Any generated README that says "the conventions" next
  to a print folder contradicts the maintainer's decision.
- **Counts from git.** `files.tracked_count` requires a git checkout and staged
  moves; a plain `mv` before `byz.build` would print 0 for `preformatted/`.
  `git mv` stages, and `validation.md` checks the counts against known values.
- **One-commit lag.** `source_commit`/`strongs_commit` in the manifest and
  `ccat_commit`/`strongs_commit` in the new provenance cannot name a commit
  that does not exist yet. The first build before the move commit records the
  last pre-move commit (or empty); the follow-up records the move commit. This
  is the same lag the 2026-11-21 and 2026-11-25 changes had; the follow-up count
  is recorded.
- **Report churn.** Dataset names change, so `reports/baseline/*.csv`,
  `reports/reconciliation/*.csv`, `docs/contract/*.json` (two deleted, two
  added), and `docs/{DATA_CONTRACT,HISTORY,PROVENANCE}.md` change. None of it is
  a text change; record the row deltas in `validation.md`.
- **PDFs are hand-pinned twice.** `pdfs.toml` and the manifests both name the
  PDF path; a test must compare them so one cannot move alone.
- **Agent instructions are executable documentation.** Leaving `.opencode/`
  unchanged would have future agents edit `data/text/`, recreate it, or assume
  the print extracts follow the repo conventions.

## Open questions (maintainer may overrule)

1. **Directory case (D2 vs D8).** D2's parenthetical says "its `CCAT/` and
   `Strongs/` directories"; D1 says to name subfolders lower-case. This spec
   adopts `ccat/`/`strongs/` for the directories and keeps file names
   (`01_MAT.TXT`, `01_MAT.BP5`). Keeping `CCAT/`/`Strongs/` would cost one
   exception to the naming rule and leave the two repo trees inconsistent.
2. **`preformatted/` name.** The official archives call this content
   "preformatted" (`*.ASC`); the repository reads it only as
   `preformatted_source`, never as a build input. The spec keeps the
   publisher's word rather than inventing `asc/`.
3. **Where the current-text provenance is written (D10).** `byz.build` writes
   it because it already has the hashes and commits. The alternative is to make
   `byz.materialise` the single provenance writer for both repo trees; that
   would give `byz.materialise` a second, unrelated input and make a normal
   rebuild unable to refresh the record.
4. **No README for `data/provenance/`.** D4 names the folders; if the
   maintainer wants one, it is a one-line addition to the renderer and the
   registry.

## Sequencing

- Independent of any concurrent spec. Edit only this folder and `SPECS/TECH.md`.
- The change is self-contained on
  `feature/2026-11-16-edition-recovery-curation`.
- Phase order is mandatory: move the trees and the constants first (phase 1),
  then the provenance records and the fetch/materialise paths (phase 2), then the
  generated READMEs and the registry (phase 3), then the conventions document
  (phase 4), then docs/`TECH.md`/`.opencode` (phase 5), then the gates (phase 6).
  Writing the READMEs before the tree exists produces counts for missing
  folders; moving the trees before the constants breaks every reader.
