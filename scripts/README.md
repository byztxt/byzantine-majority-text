# Scripts to convert the files to Unicode

The scripts have dependencies, which are listed in the `requirements.txt` file. To install them, you can run `pip install -r requirements.txt`.

## Csv converter

You call it using `python3 csv_converter.py` (or `python csv_converter.py` depending on your particular settings.) It has been tested on Ubuntu 22.04 and Python 3.10.

## Curated editions and reconciliation

Python 3.10 is recommended. Install the converter dependencies with
`pip install -r requirements.txt` (run from this folder).

- `fetch_official.py` - fetch, checksum, and extract the official ZIP archives.
- `recover_editions.py` - recover the 2005 lineage from git and freeze the four
  curated editions under `editions/`.
- `build_editions.py` - build curated CSV/TEI, manifests, per-edition READMEs,
  and `docs/EDITIONS.md`.
- `diff_editions.py` - write the successive edition diffs under `reports/diffs/`.

Run them from the repository root:

```bash
python3 scripts/fetch_official.py --verify
python3 scripts/recover_editions.py
python3 scripts/build_editions.py
python3 scripts/diff_editions.py
```

See `docs/EDITIONS.md` for the edition model and release numbers.

## Csv converter

You call it using `python3 csv_converter.py` (or `python csv_converter.py`
depending on your particular settings.) It has been tested on Ubuntu 22.04 and
Python 3.10.
