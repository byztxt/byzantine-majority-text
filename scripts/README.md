# Scripts

The scripts have one dependency, listed in `requirements.txt` (`beta-code`, the
shared Beta-code converter used by the build). Python 3.10 is recommended.
Install it with `pip install -r requirements.txt` (run from this folder).

## The pipeline

The model is **sources -> pipeline -> editions**. `source/` and the committed
archives under `data/raw/` are the inputs; the only producer of the curated
edition CSV/TEI is `recover_editions.py` followed by `build_editions.py`.

- `fetch_official.py` - checksum, extract, and (re)fetch the official ZIP
  archives. The six original zips are committed under `data/raw/_archives/`,
  so `--verify` checks them against the pinned digests with no network access
  and no writes. Record mode (no flag) reuses the committed archives and
  preserves the recorded `downloaded`, `final_url`, and `http_status` values,
  rewriting only `data/provenance/*.toml` (it downloads only if an archive is
  missing or fails its digest). `--force` always re-downloads and re-extracts
  the archives and rewrites the provenance TOMLs, replacing the recorded
  timestamps and final Dropbox URLs. `--verify` and `--force` cannot be
  combined.
- `recover_editions.py` - recover the 2005 lineage from git and freeze the four
  curated editions under `editions/`, including each edition's `source/`
  snapshot. It only stages the inputs: it writes no CSV/TEI, so running it
  alone leaves every `editions/<edition>/csv/` and `tei/` empty. Always follow
  it with `build_editions.py` (which re-runs the recovery itself).
- `build_editions.py` - generate every curated CSV/TEI view from the edition
  `source/` snapshots, then write manifests, per-edition READMEs,
  `docs/EDITIONS.md`, and the generated editions block in the root `README.md`.
- `diff_editions.py` - write the successive edition diffs under `reports/diffs/`.

`beta_to_unicode_custom/beta_to_unicode_custom.py` is the shared conversion
module; `tei_xml_header.xml` is the TEI header template. Both are used by
`build_editions.py`.

Run the pipeline from the repository root:

```bash
python3 scripts/fetch_official.py --verify
python3 scripts/recover_editions.py
python3 scripts/build_editions.py
python3 scripts/diff_editions.py
```

See `docs/EDITIONS.md` for the edition model and release numbers.

### Report generation order

`docs/HISTORY.md` is written by two commands, so run them in this order:

```bash
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m byz.reconcile   # reads data/raw/_archives/
```

`byz.contract` rebuilds the whole history document from git. Before it writes,
it takes a copy of the "External archive evidence (Cycle 2)" section if that
section is present, and puts it back at the end afterwards; it finds the section
by the `<!-- cycle2:begin -->` and `<!-- cycle2:end -->` markers.
`byz.reconcile` rebuilds that section from the archives committed under
`data/raw/_archives/`.

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
