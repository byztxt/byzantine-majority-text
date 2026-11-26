<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

# `rp2018-2023` sources

## What this folder holds

The maintained current text: the Byzantine Textform as
published in 2018 plus the 2023 adjustments, created and
maintained by Dr. Maurice A. Robinson. This is the repository's
own input, not a copy of the official printed editions' files,
and `byz.build` regenerates every view from it. It is an input
tree: the curated editions under `editions/` contain outputs
only and pin these files by path and SHA-256. The published
PDFs are the ultimate source of truth for the printed
editions. The files follow the repository conventions in
[`../CONVENTIONS.md`](../CONVENTIONS.md).

## Contents

| Folder | Files | Contents | Feeds |
| --- | --- | --- | --- |
| `ccat/` | 29 `.TXT` | All-lowercase accented Beta-code | Accented CSV and TEI |
| `strongs/` | 27 `.BP5` | Parsed text with Strong's numbers and morphology | Unaccented CSV, Strong's views, TEI |

## Edition

- Folder: `data/raw/repo/rp2018-2023/`.
- Edition: `editions/rp2018-2023/` (Robinson-Pierpont 2018 with 2023 adjustments (repo release)).
- Revision: `2023-07-20`.
- `ccat_commit`: `e7d19f40a9efb175b95a77d6697faa7062102a17`.
- `strongs_commit`: `e7d19f40a9efb175b95a77d6697faa7062102a17`.

## Provenance

- `data/provenance/rp2018-2023.toml` - the revision, the two source commits, and the file hashes.

## Commands

```bash
PYTHONPATH=src python3 -m byz.build
PYTHONPATH=src python3 -m byz.verify
```

## Related

- [Class README](../README.md)
- [Conventions](../CONVENTIONS.md)
- [Edition `rp2018-2023`](../../../../editions/rp2018-2023/README.md)
- [Provenance record](../../../../data/provenance/rp2018-2023.toml)
