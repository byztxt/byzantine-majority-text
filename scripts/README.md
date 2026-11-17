# Scripts to convert the files to Unicode

The scripts have dependencies, which are listed in the `requirements.txt` file. To install them, you can run `pip install -r requirements.txt`.

## Curated editions and reconciliation

Python 3.10 is recommended. Install the converter dependencies with
`pip install -r requirements.txt` (run from this folder).

- `fetch_official.py` - checksum, extract, and (re)fetch the official ZIP
  archives. The six original zips are committed under `data/raw/_archives/`,
  so `--verify` checks them against the pinned digests with no network access
  and no writes. `--force` is the only mode that downloads: it re-downloads and
  re-extracts the archives and rewrites `data/provenance/*.toml`. The two modes
  cannot be combined.
- `recover_editions.py` - recover the 2005 lineage from git and freeze the four
  curated editions under `editions/`.
- `build_editions.py` - build curated CSV/TEI, manifests, per-edition READMEs,
  `docs/EDITIONS.md`, and the generated editions block in the root `README.md`.
- `diff_editions.py` - write the successive edition diffs under `reports/diffs/`.

Run them from the repository root:

```bash
python3 scripts/fetch_official.py --verify
python3 scripts/recover_editions.py
python3 scripts/build_editions.py
python3 scripts/diff_editions.py
```

See `docs/EDITIONS.md` for the edition model and release numbers.

### Report generation order

`docs/HISTORY.md` is written by two steps. Regenerate them in this order:

```bash
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m byz.reconcile   # reads data/raw/_archives/
```

`byz.contract` owns the baseline document but preserves the
`<!-- cycle2:begin -->` ... `<!-- cycle2:end -->` evidence block if it exists,
and `byz.reconcile` rebuilds that block from the archives. Running the contract
first and the reconciliation second leaves exactly one block and one heading,
and a second run of either step produces no diff.

## Csv converter

You call it using `python3 csv_converter.py` (or `python csv_converter.py`
depending on your particular settings.) It has been tested on Ubuntu 22.04 and
Python 3.10.
