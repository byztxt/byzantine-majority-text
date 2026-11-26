<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

# `rp2005` sources

## What this folder holds

The published sources of the Robinson-Pierpont 2005, official print edition. The `.CCT`
extract supplies the accented text, the ASCII extract the
unaccented text, and the published PDF is the ultimate source
of truth. The files are the publisher's own format; the
repository conventions in `data/raw/repo/CONVENTIONS.md` are
not asserted for them.

## Contents

| Folder | Files | Contents | Feeds |
| --- | --- | --- | --- |
| `ccat/` | 29 `.CCT` | Accented Beta-code with apparatus | Accented CSV and TEI |
| `ascii/` | 27 `*_Byz.txt` | One line per verse, unaccented | Unaccented CSV and TEI |
| `preformatted/` | 27 `.ASC` | The publisher's preformatted ASCII; not a build input | Archived reference |
| `official-pdf/` | 1 PDF | The published print edition | Source of truth |

## Edition

- Folder: `data/raw/print/rp2005/`.
- Edition: `editions/rp2005/` (Robinson-Pierpont 2005, official print edition).
- Publisher: Published in print by Chilton Book Publishing, Southborough, Massachusetts.
- Published PDF: `data/raw/print/rp2005/official-pdf/editions-rp2.pdf`.
- PDF SHA-256: `ccf5bb5467408fdd44a362764dc93383ddb5d5579c6601fac0ec0b83a095ecce`.
- Archive `editions-rp2-preformatted.zip` (`preformatted`) extracts to `preformatted/`.
- Archive `editions-rp2-ascii.zip` (`ascii-one-line`) extracts to `ascii/`.
- Archive `editions-rp2-ccat.zip` (`ccat`) extracts to `ccat/`.

## Provenance

- `data/provenance/rp2005.toml` - the archive hashes and downloads.
- `data/provenance/pdfs.toml` - the hand-maintained PDF URL and local path.

## Commands

```bash
PYTHONPATH=src python3 -m byz.fetch --verify
PYTHONPATH=src python3 -m byz.fetch
PYTHONPATH=src python3 -m byz.build
PYTHONPATH=src python3 -m byz.verify
```

## Related

- [Class README](../README.md)
- [Input index](../../../README.md)
- [Edition `rp2005`](../../../../editions/rp2005/README.md)
- [Provenance record](../../../../data/provenance/rp2005.toml)
