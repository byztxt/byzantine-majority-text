<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

# Inputs (`data/`)

## What this folder holds

`data/` holds every input an edition is built from. It has two source classes
under `data/raw/`: `print/` for the published print editions
and `repo/` for this repository's own lineage. `data/provenance/`
records where each input came from and what its files hash to.

Nothing here is a build output: the curated editions live under
`editions/` and contain outputs only. The Beta-code, variant, parsing,
and Strong's conventions are in `data/raw/repo/CONVENTIONS.md`.

## Contents

| Folder | Files | Contents | Feeds |
| --- | --- | --- | --- |
| `raw/print/` | 113 pinned inputs | Published print-edition extracts, preformatted ASCII, the 6 ZIP archives, and the 2 PDFs | `rp2005`, `rp2018` |
| `raw/repo/` | 113 pinned inputs | The 2019 lineage, the current text, and the shared conventions | `rp2005-2019`, `rp2018-2023` |
| `provenance/` | 5 records | SHA-256, download, tag, and revision facts for every source tree | `byz.fetch`, `byz.materialise`, `byz.build`, `byz.verify` |

## Classes

| Class | Holds | Origin | Editions |
| --- | --- | --- | --- |
| `print` | Published print-edition material | Downloaded and checksummed from the publisher | `rp2005`, `rp2018` |
| `repo` | This repository's own lineage | Committed to this repository and pinned by tag or revision | `rp2005-2019`, `rp2018-2023` |

## Provenance

Every record lives in `data/provenance/`:

- `pdfs.toml` - hand-maintained: publisher URLs and local PDF paths
- `rp2005.toml` - official 2005 archive hashes and downloads
- `rp2018.toml` - official 2018 archive hashes and downloads
- `rp2005-2019.toml` - the `v2.0.3` tag snapshot and its file hashes
- `rp2018-2023.toml` - the current text's revision and file hashes

## Commands

```bash
PYTHONPATH=src python3 -m byz.fetch --verify  # validate the 6 committed archives
PYTHONPATH=src python3 -m byz.fetch           # re-record the print-class downloads
PYTHONPATH=src python3 -m byz.materialise     # restore the 2019 lineage from tag v2.0.3
PYTHONPATH=src python3 -m byz.build           # CSV, TEI, manifests, and these READMEs
PYTHONPATH=src python3 -m byz.verify          # check inputs and artifacts against the manifests
```

## Related

- [Source classes](raw/README.md)
- [Published print-edition sources](raw/print/README.md)
- [Repository-lineage sources](raw/repo/README.md)
- [Conventions](raw/repo/CONVENTIONS.md)
- [Edition model](../docs/EDITIONS.md)
- [Build details](../docs/BUILD.md)
