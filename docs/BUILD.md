# Building the repository

This is the build and run reference for the `byz` package. The package lives
under `src/byz/`, and its runnable entry points are modules, invoked from the
repository root as `PYTHONPATH=src python3 -m byz.<verb>`.

The package has one dependency, `beta-code`, pinned at `beta-code==1.0.0` in
`requirements.txt` at the repository root. Python 3.10 or newer is
recommended. Install it with `pip install -r requirements.txt` (run from the
repository root).

## The input tree

Every input a build reads lives under `data/`, in one of two source classes:

| Class | Source folder | Holds | Edition |
| --- | --- | --- | --- |
| print | `data/raw/print/rp2005/{ccat,ascii,preformatted,official-pdf}/` | the published 2005 extracts and PDF | `rp2005` |
| print | `data/raw/print/rp2018/{ccat,ascii,preformatted,official-pdf}/` | the published 2018 extracts and PDF | `rp2018` |
| print | `data/raw/print/_archives/{rp2005,rp2018}/` | the six committed original ZIPs | `byz.fetch` |
| repo | `data/raw/repo/rp2005-2019/{textonly-beta-code,parsed}/` | the 2019 lineage, materialised from tag `v2.0.3` | `rp2005-2019` |
| repo | `data/raw/repo/rp2018-2023/{ccat,strongs}/` | the maintained current text | `rp2018-2023` |

`data/provenance/*.toml` records archive, PDF, tag, revision, and per-file
hashes. `data/raw/repo/CONVENTIONS.md` is the hand-maintained authority for the
Beta-code, variant, parsing, and Strong's conventions of the two repo sources;
the print extracts use the publisher's own conventions.

Each of `data/`, `data/raw/`, the two class folders, and the four source folders
has a generated `README.md`; `byz.build` writes them. An edition under
`editions/<edition>/` contains outputs only: `csv/`, `tei/`, `manifest.json`, and
`README.md`. Its `manifest.json` pins each input by repository-relative path and
SHA-256, so the edition records its provenance without carrying a second copy of
the input tree.

## The pipeline

The model is **sources -> pipeline -> editions**. The two source classes under
`data/raw/` are the sources; `byz.build` is the only producer of the curated
edition CSV/TEI.

- `byz.fetch` - checksum, extract, and (re)fetch the official ZIP archives. The
  six original zips are committed under `data/raw/print/_archives/`, so `--verify`
  checks them against the pinned digests with no network access and no writes.
  Record mode (no flag) reuses the committed archives and preserves the recorded
  `downloaded`, `final_url`, and `http_status` values, rewriting only
  `data/provenance/*.toml` (it downloads only if an archive is missing or fails
  its digest). `--force` always re-downloads and re-extracts the archives and
  rewrites the provenance TOMLs, replacing the recorded timestamps and final
  Dropbox URLs. `--verify` and `--force` cannot be combined.
- `PYTHONPATH=src python3 -m byz.materialise` - restore the historical 2005-2019 inputs from tag `v2.0.3`
  into `data/raw/repo/rp2005-2019/` and write `data/provenance/rp2005-2019.toml`. It
  is an ingest command, not part of the normal rebuild: the tree is committed,
  so run it only when that tree is missing. It writes nothing under `editions/`
  and refuses to overwrite a conflicting file.
- `byz.build` - generate every curated CSV/TEI view from the committed `data/`
  inputs, then write manifests, per-edition READMEs, the eight input-tree
  READMEs, `docs/EDITIONS.md`, the root `README.md`, and
  `data/provenance/rp2018-2023.toml`. It renders the root README from
  `src/byz/curate/README.template.md`. `rp2005-2019` is generated from its 2019
  sources under `data/raw/repo/rp2005-2019/` exactly like the other editions;
  the build never reads a git tag.
- `byz.diff` - write the successive edition diffs under `reports/diffs/`.
- `byz.contract` - write `docs/DATA_CONTRACT.md`, `docs/HISTORY.md`,
  `docs/contract/*.json`, and `reports/baseline/`.
- `byz.reconcile` - write `docs/PROVENANCE.md` and `reports/reconciliation/`.
- `byz.verify` - check every manifest against the inputs under `data/` and the
  committed `csv/`/`tei/`. See "Verifying the editions" below.

The shared Beta-code converter lives at `src/byz/beta/converter.py`, and the
TEI header template at `src/byz/curate/tei_xml_header.xml`. The build uses
both.

Run the pipeline from the repository root:

```bash
PYTHONPATH=src python3 -m byz.fetch --verify
PYTHONPATH=src python3 -m byz.build
PYTHONPATH=src python3 -m byz.diff
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m byz.reconcile
PYTHONPATH=src python3 -m byz.verify
```

`byz.materialise` is not in this sequence. It restores the 57 source files
under `data/raw/repo/rp2005-2019/` from git tag `v2.0.3` when that tree is missing;
only it extracts the tag's files into `data/`, and the build reads `data/` only.
(`byz.reconcile` reads the tag with `git show` for historical comparison, and
`byz.build` lists tags for the release ranges, but neither uses the tag's files
as build inputs.) `byz.build` regenerates `rp2005-2019` from those sources with
the current pipeline, so the published CSV/TEI are not a copy of the tag's
artifacts. The worktree-based tests still need the full history and tags.

Regenerating `rp2005-2019` changes it relative to the artifacts released as
`v2.0.3`: the 2019 converter's malformed apparatus codes (`{Ν` for NA and `{Β`
for Byz) become `{NA`/`{Byz`, typography is normalised (`¶` paragraph markers,
curly apostrophes), and the four intentional blank verses are emitted as empty
records. The main text keeps the same words.

See `docs/EDITIONS.md` for the edition model and release numbers.

## Verifying the editions

`editions/<edition>/manifest.json` carries:

- `inputs` - one `{root, include, files}` group per input directory. `root` is a
  repository-relative path under `data/`; `include` lists the globs the build
  reads; `files` lists each match with its `path` (relative to `root`),
  `sha256`, and `size`.
- `artifact_files` - every committed `csv/` and `tei/` file, relative to the
  edition, with its `sha256` and `size`.

Check the clean tree with:

```bash
PYTHONPATH=src python3 -m byz.verify
```

It prints one `OK <edition>: <n> inputs, <m> artifacts` line per edition and a
`verified 4 editions (226 inputs, 672 artifacts)` summary. A mismatch prints
`FAIL <edition>: <path>: sha256 expected <hex>, actual <hex>` (or `missing`,
`unexpected`, or a size mismatch) and the command exits `1`. An unknown edition
exits `2`.

A downloaded edition ships its artifacts but not the inputs, so verify it with:

```bash
PYTHONPATH=src python3 -m byz.verify --edition-dir path/to/rp2018
```

That checks the `csv/`/`tei/` files against the manifest and states that the
inputs were skipped. It cannot prove the artifacts were built from the pinned
inputs, because the inputs are not shipped.

## Editing the root README

`README.md` is generated. Do not edit it by hand: edit
`src/byz/curate/README.template.md`, then run

```bash
PYTHONPATH=src python3 -m byz.build
```

The template's first line marks it as the edit point; the renderer strips that
line and replaces the `{{CURATED_EDITIONS}}` and `{{GENERATED_FILES}}` lines
with sections rendered from the manifests and the generated-file registry. The
rendered README carries the full-file generated banner. Commit both files.

`data/provenance/pdfs.toml` is hand-maintained and is not generated; it never
receives a banner.

### Report generation order

`docs/HISTORY.md` is written by two commands, so run them in this order:

```bash
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m byz.reconcile   # reads data/raw/print/_archives/
```

`byz.contract` rebuilds the whole history document from git. Before it writes,
it takes a copy of the "External archive evidence (Cycle 2)" section if that
section is present, and puts it back at the end afterwards; it finds the section
by the `<!-- cycle2:begin -->` and `<!-- cycle2:end -->` markers.
`byz.reconcile` rebuilds that section from the archives committed under
`data/raw/print/_archives/`.

Running the contract first and the reconciliation second means the archive
section is written last, so the finished document carries both the current
history and the current archive numbers. After the supported order the file has
exactly one generated-file banner, one `# Internal history map` heading, and
one evidence section.

If the order or the run goes wrong, this is what you see:

- contract only: the archive section keeps its previous numbers, or disappears
  entirely if its markers were removed by hand;
- reconciliation only: the rest of `docs/HISTORY.md` is stale relative to git;
- a hand-edited or deleted marker: the next contract run drops the section
  silently. Run the reconciliation to put it back.

Both commands are safe to re-run: a second run of either produces no diff.

`byz.contract` requires a git checkout: it inventories only tracked files, so
`git` must be installed and `git ls-files` must work under the repository root.
Without a usable `git` binary it raises a clear `RuntimeError` rather than
describing an untracked working tree.

## Tests

Run the three `unittest` suites from the repository root:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests/contract
PYTHONPATH=src python3 -m unittest discover -s tests/curate
PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation
```

The materialisation and the worktree-based tests need the full git history and
tags, at least `v2.0.3`, so they fail in a shallow clone.
