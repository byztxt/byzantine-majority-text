<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

# Source classes (`data/raw/`)

## What this folder holds

`data/raw/` contains exactly two class directories. `print/` holds
published print-edition material that was downloaded and checksummed;
`repo/` holds material from this repository's own lineage. Every source
tree belongs to exactly one class, and each class keeps its per-edition
snapshots in named subfolders.

## Contents

| Folder | Files | Contents | Feeds |
| --- | --- | --- | --- |
| `data/raw/print/rp2005/` | 56 pinned inputs, 27 preformatted, 1 PDF | Print-edition extracts and the published PDF | `editions/rp2005/` |
| `data/raw/print/rp2018/` | 57 pinned inputs, 27 preformatted, 1 PDF | Print-edition extracts and the published PDF | `editions/rp2018/` |
| `data/raw/repo/rp2005-2019/` | 57 pinned inputs | Repository-lineage snapshot | `editions/rp2005-2019/` |
| `data/raw/repo/rp2018-2023/` | 56 pinned inputs | Repository-lineage snapshot | `editions/rp2018-2023/` |
| `print/_archives/` | 6 ZIPs | The published archives the print sources were extracted from | `byz.fetch` |

## Classes

**`print/`** is published material. The publisher's ZIP archives
are committed under `print/_archives/`, and the extracted `.CCT`,
ASCII, and preformatted folders sit beside the PDF of the same
edition. `byz.fetch` checks the pinned SHA-256 and extracts them;
`byz.verify` checks the manifest against the committed files.

**`repo/`** is this repository's lineage. `rp2005-2019/` is
restored from git tag `v2.0.3`, and `rp2018-2023/` is the
maintained current text snapshotted from the working tree. Both are
inputs to `byz.build`, and both use the conventions in
[`repo/CONVENTIONS.md`](repo/CONVENTIONS.md).

The print class feeds `rp2005` and `rp2018`; the repo class
feeds `rp2005-2019` and `rp2018-2023`. The print extracts are the
publisher's own format; the repository conventions are not asserted
for them.


## Provenance

- Print class: `data/provenance/rp2005.toml`, `data/provenance/rp2018.toml`, and the hand-maintained `data/provenance/pdfs.toml`.
- Repo class: `data/provenance/rp2005-2019.toml` and `data/provenance/rp2018-2023.toml`.

## Commands

```bash
PYTHONPATH=src python3 -m byz.fetch --verify
PYTHONPATH=src python3 -m byz.materialise
PYTHONPATH=src python3 -m byz.build
PYTHONPATH=src python3 -m byz.verify
```

## Related

- [Input index](../README.md)
- [Published print-edition sources](print/README.md)
- [Repository-lineage sources](repo/README.md)
- [Conventions](repo/CONVENTIONS.md)
