<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

# `rp2005-2019` sources

## What this folder holds

The 2019 lineage, restored from git tag `v2.0.3` by
`byz.materialise`. It is an input: `byz.build` regenerates
the edition from these 57 files; it does not copy the
release's CSV/TEI. The files follow the repository
conventions in [`../CONVENTIONS.md`](../CONVENTIONS.md).

## Contents

| Folder | Files | Contents | Feeds |
| --- | --- | --- | --- |
| `textonly-beta-code/` | 30 `.CCT` | Mixed-case Beta-code with apparatus | Accented CSV and TEI |
| `parsed/` | 27 `.UB5` | Parsed text with Strong's numbers | Unaccented CSV, Strong's views, TEI |

## Edition

- Folder: `data/raw/repo/rp2005-2019/`.
- Edition: `editions/rp2005-2019/` (Robinson-Pierpont 2005 lineage, 2019 repo revision).
- Tag: `v2.0.3` (commit `8ec95671e463030347c2c643358eb56e58235b19`).
- Method: `git archive v2.0.3`.
- Written by `PYTHONPATH=src python3 -m byz.materialise`.

## Provenance

- `data/provenance/rp2005-2019.toml` - the tag, commit, and file hashes.

## Commands

```bash
PYTHONPATH=src python3 -m byz.materialise
PYTHONPATH=src python3 -m byz.build
PYTHONPATH=src python3 -m byz.verify
```

## Related

- [Class README](../README.md)
- [Conventions](../CONVENTIONS.md)
- [Edition `rp2005-2019`](../../../../editions/rp2005-2019/README.md)
- [Provenance record](../../../../data/provenance/rp2005-2019.toml)
