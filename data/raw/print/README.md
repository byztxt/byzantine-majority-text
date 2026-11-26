<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

# Print sources (`data/raw/print/`)

## What this folder holds

`data/raw/print/` holds the published print-edition material: the
official `.CCT`, ASCII, and preformatted extracts, the
2 published PDFs, and the 6 committed ZIP
archives they came from. Everything here was published by the
publisher and downloaded, not authored in this repository.

## Contents

| Folder | Files | Contents | Feeds |
| --- | --- | --- | --- |
| `rp2005/` | 29 `.CCT`, 27 `*_Byz.txt`, 27 `.ASC`, 1 PDF | Print-edition extracts and PDF | `editions/rp2005/` |
| `rp2018/` | 30 `.CCT`, 27 `*_Byz.txt`, 27 `.ASC`, 1 PDF | Print-edition extracts and PDF | `editions/rp2018/` |
| `_archives/` | 6 ZIPs | The published archives, kept under their published names | `byz.fetch` |

## Editions

- `rp2005` - Robinson-Pierpont 2005, official print edition.
  Sources: `data/raw/print/rp2005/`; PDF: `data/raw/print/rp2005/official-pdf/editions-rp2.pdf`.
  Archive `editions-rp2-preformatted.zip` (`preformatted`) feeds `data/raw/print/rp2005/preformatted/`.
  Archive `editions-rp2-ascii.zip` (`ascii-one-line`) feeds `data/raw/print/rp2005/ascii/`.
  Archive `editions-rp2-ccat.zip` (`ccat`) feeds `data/raw/print/rp2005/ccat/`.
- `rp2018` - Robinson-Pierpont 2018, official print edition.
  Sources: `data/raw/print/rp2018/`; PDF: `data/raw/print/rp2018/official-pdf/robinson-pierpont-2018-gnt-edition.pdf`.
  Archive `rp2018-ascii.zip` (`preformatted`) feeds `data/raw/print/rp2018/preformatted/`.
  Archive `rp2018-ascii-one-line-per-verse.zip` (`ascii-one-line`) feeds `data/raw/print/rp2018/ascii/`.
  Archive `rp2018-ccat.ZIP` (`ccat`) feeds `data/raw/print/rp2018/ccat/`.

The archives are the download source; the extracts are
committed, so a rebuild needs no network.

## Provenance

- `data/provenance/rp2005.toml` and `data/provenance/rp2018.toml` - the archive hashes, downloads, and extraction paths.
- `data/provenance/pdfs.toml` - hand-maintained publisher URLs and the local PDF paths.

## Commands

```bash
PYTHONPATH=src python3 -m byz.fetch --verify  # validate the committed ZIPs; no network
PYTHONPATH=src python3 -m byz.fetch           # re-record provenance; no network after --verify
PYTHONPATH=src python3 -m byz.build           # build the official editions
PYTHONPATH=src python3 -m byz.verify          # check inputs and artifacts
```

## Related

- [Input index](../../README.md)
- [Source classes](../README.md)
- [Repository-lineage sources](../repo/README.md)
- [rp2005 sources](rp2005/README.md)
- [rp2018 sources](rp2018/README.md)
