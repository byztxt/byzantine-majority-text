<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

# `rp2018` sources

## What this folder holds

The published sources of the Robinson-Pierpont 2018, official print edition. The `.CCT`
extract supplies the accented text, the ASCII extract the
unaccented text, and the published PDF is the ultimate source
of truth. The files are the publisher's own format; the
repository conventions in `data/raw/repo/CONVENTIONS.md` are
not asserted for them.

## Contents

| Folder | Files | Contents | Feeds |
| --- | --- | --- | --- |
| `ccat/` | 30 `.CCT` | Accented Beta-code with apparatus | Accented CSV and TEI |
| `ascii/` | 27 `*_Byz.txt` | One line per verse, unaccented | Unaccented CSV and TEI |
| `preformatted/` | 27 `.ASC` | The publisher's preformatted ASCII; not a build input | Archived reference |
| `official-pdf/` | 1 PDF | The published print edition | Source of truth |

`GREEK.CCT`, when the archive publishes it, is Dr Robinson's
alphabet/transliteration key, not a book. The manifest pins it
as part of the source snapshot, but `byz.build` skips it: the
exports are the 27 books plus the PA and ACT24 sections.

## Edition

- Folder: `data/raw/print/rp2018/`.
- Edition: `editions/rp2018/` (Robinson-Pierpont 2018, official print edition).
- Publisher: Published in print by VTR, Nuremberg.
- Published PDF: `data/raw/print/rp2018/official-pdf/robinson-pierpont-2018-gnt-edition.pdf`.
- PDF SHA-256: `00303ddc443816d363ccca8c3882ce83f4ecb858fa52d0313b80f445d263852c`.
- Archive `rp2018-ascii.zip` (`preformatted`) extracts to `preformatted/`.
- Archive `rp2018-ascii-one-line-per-verse.zip` (`ascii-one-line`) extracts to `ascii/`.
- Archive `rp2018-ccat.ZIP` (`ccat`) extracts to `ccat/`.

## Provenance

- `data/provenance/rp2018.toml` - the archive hashes and downloads.
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
- [Edition `rp2018`](../../../../editions/rp2018/README.md)
- [Provenance record](../../../../data/provenance/rp2018.toml)
