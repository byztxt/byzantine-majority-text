# The New Testament in the original Greek: Byzantine textform

![GitHub release (latest by date)](https://img.shields.io/github/v/release/ByzTxt/byzantine-majority-text?style=for-the-badge)

Welcome to the official GitHub home of [Dr. Maurice A. Robinson](https://en.wikipedia.org/wiki/Maurice_A._Robinson)'s Greek
texts with variants, morphological parsing, and Strong's numbers.

This repository contains the Robinson-Pierpont edition of the Greek New
Testament in the Original Greek, Byzantine Majority Text: the Beta-code files
produced by Dr. Robinson, plus generated Unicode CSV and TEI-XML. The current
text (`rp2018-2023`) is the 2018 edition plus the 2023 adjustments; the parsing
tags received later minor corrections (2026). Both official print editions
(2005 and 2018) are also curated from their official archives. The published
PDFs are the ultimate source of truth for the printed editions, and `source/`
is their authoritative machine-readable companion.

The 2005 edition can be freely downloaded as a PDF from The Internet Archive
[here](https://archive.org/details/newtestamentrobinsonpierpontbyzantine/). The
2018 edition can be downloaded from
[this link](https://archive.org/details/robinson-pierpont-2018-gnt-edition).
RP2018 is recommended over RP2005 for all practical purposes (read the details
below). Additional resources can be downloaded from
[https://www.byzantinetext.com](https://www.byzantinetext.com).

You can read Professor Robinson's essay proposing the superiority of the
Byzantine textform
[here](https://byzantinetext.com/wp-content/uploads/2016/11/editions-rp-11-appendix.pdf)
(a Spanish translation is available for free download
[here](https://archive.org/details/libro-robinson-traducido/LIBRO%20ROBINSON%20TRADUCIDO/)).
The essay can be found in a plain text format inside the `essay` folder.

## Start here

| I want to... | Start here |
| --- | --- |
| Read or download the current text as CSV or TEI | [`editions/rp2018-2023/`](editions/rp2018-2023/), or `csv-unicode/` and `tei-xml-unicode/` for the working-tree outputs |
| Use the official 2018 print edition | [`editions/rp2018/`](editions/rp2018/) and the [2018 PDF](https://byzantinetext.com/wp-content/uploads/2021/03/robinson-pierpont-2018-gnt-edition.pdf) |
| Use the official 2005 print edition | [`editions/rp2005/`](editions/rp2005/) and the [2005 PDF](https://byzantinetext.com/wp-content/uploads/2016/11/editions-rp2.pdf) |
| Use the 2019 revision of the 2005 lineage | [`editions/rp2005-2019/`](editions/rp2005-2019/) |
| Edit or convert the text | [`source/`](source/) and [`scripts/`](scripts/) |
| Check provenance and checksums | [`data/provenance/`](data/provenance/) and [`docs/PROVENANCE.md`](docs/PROVENANCE.md) |
| Understand the edition model and its history | [`docs/EDITIONS.md`](docs/EDITIONS.md) and [`docs/HISTORY.md`](docs/HISTORY.md) |

## Official vs released

- **Official** means published in print by Dr. Maurice A. Robinson.
- **Released** means published as an artifact in this repository.

`rp2005` and `rp2018` are therefore official editions; `rp2005-2019` and
`rp2018-2023` are released editions.

<!-- editions:begin -->
## Curated editions

Four editions are curated under [`editions/`](editions/), each with its
own `source/`, `csv/`, `tei/`, `manifest.json`, and `README.md`.
`rp2018-2023` is the current text, `rp2018` and `rp2005` are the official
print editions, and `rp2005-2019` is the historical 2019 revision of the
2005 lineage.

| Edition | Status | Repo releases |
| --- | --- | --- |
| `rp2005` | official | none |
| `rp2005-2019` | released | `v1.0.0`-`v2.0.3` |
| `rp2018` | official | none |
| `rp2018-2023` | released | `v3.0.0`-`v3.3.4` |

See [`docs/EDITIONS.md`](docs/EDITIONS.md) and the
[`editions/`](editions/) directory for the full explanation, PDF
links, provenance, manifests, and checksums.
<!-- editions:end -->

## Repository layout

| Path | What it holds |
| --- | --- |
| `editions/` | The four curated editions, each self-contained (source, CSV, TEI, manifest, README). Start here for a complete text. |
| `source/` | The official Beta-code source files for the current text: accented `CCAT/` and parsed `Strongs/`. |
| `csv-unicode/`, `tei-xml-unicode/` | Generated Unicode CSV and TEI-XML for the current text. |
| `data/` | Official ZIP archives (`raw/_archives/`, committed), extracted archive trees (`raw/<edition>/`), the published PDFs, and `provenance/` hashes and URLs. |
| `docs/` | `EDITIONS.md`, `PROVENANCE.md`, `HISTORY.md`, `DATA_CONTRACT.md`, and `contract/`. |
| `reports/` | `baseline/` (contract snapshot), `reconciliation/` (official-archive comparison), and `diffs/` (successive edition diffs). |
| `scripts/` | Converters and the build, recovery, diff, and report entry points. |
| `src/` | The `byz/` Python package used by the scripts and tests (`contract/`, `curate/`, `reconcile/`). |
| `tests/` | The `contract/`, `curate/`, and `reconciliation/` suites. |
| `essay/` | Robinson's essay on Byzantine priority, in plain text and translations. |
| `SPECS/` | The mission, technical design, roadmap, and dated cycle specifications. |
| `.opencode/`, `opencode.json` | Configuration for the maintenance agents and commands; not part of the edition data. |
| `LICENSE`, `.gitignore`, `README.md` | Licensing and repository plumbing. |

## Source of truth and provenance

The published PDFs are the ultimate source of truth for the printed editions.
`source/CCAT` and `source/Strongs` are their authoritative machine-readable
companion, and `data/raw/_archives/` holds the committed official ZIP
archives from which the official sources were extracted. `data/provenance/*.toml`
pin the SHA-256 of each archive and PDF, and `docs/PROVENANCE.md` records what
was compared and how far the current corpus matches. If a PDF, an archive, and
the curated source disagree, the PDF wins and the conflict is flagged to the
maintainer rather than silently resolved.

## Which text should I use?

- `rp2018-2023` for current work. It is also the text described by `source/`,
  `csv-unicode/`, and `tei-xml-unicode/`.
- `rp2018` to cite or check the official 2018 print edition.
- `rp2005` to cite or check the official 2005 print edition.
- `rp2005-2019` for the repository's 2019 revision of the 2005 lineage (the
  `v2.0.3` text). It is not the official 2005 print edition.

RP2018 is recommended over RP2005, for the reasons given under repo releases
below.

## Repo releases vs curated editions

A **repo release** is a git tag. A **curated edition** is a stable view of one
text under `editions/`, with its own manifest and checksums, independent of the
commit you are on. `v3.x.x` is the current release line, and `v2.0.3` is
preserved as `rp2005-2019`.

The two official printed editions of the Byzantine Textform are those of the
years 2005 and 2018, both widely available as PDFs and in print. This repository
contains data from both. Prior to 2022 the repository had no formal versioning
system, so recuperating the exact wordings of those editions from the Git
history alone is not straightforward; they are curated from the official
archives instead.

It is strongly recommended that versions `3.x.x` be used instead of previous
ones, for at least the following reasons:

* Previous to release 1.0.0 there was *no* Unicode version of the files. The source files (which were in a custom flavor of Beta code) *were* however in the repository and can be accessed by browsing the Git history.

* A Unicode converter was added in release 1.0.0, but its output unfortunately produced various misspellings. The errors were successfully fixed in release 2.0.3. That tag is preserved as the curated `rp2005-2019` edition. Please do **not** use the Unicode files of releases prior to 2.0.3 as those contain conversion errors (the source Beta code files, however, did not change between releases 1.0.0 and 2.0.3 and are official as they came directly from Professor Robinson).

* Release 3.0.0 introduced the text of the RP2018 edition, with minor updates to the apparatus. By direct recommendation of professor Robinson, *the use of the RP2005 is discouraged in favor of RP2018*, as RP2005 had "numerous accent, breathing, and punctuation errors (caused by porting over an NA27 file, and then altering only where the Byz text differed)". Additionally, "the 2018 edition should be used, since those errors were corrected". The text was updated "in a very few places", and the apparatus was updated as well in order to "to reflect NA28 and ECM differences in the general epistles and Acts". Note that the *unaccented* text remained highly stable between RP2005 and RP2018.

## Reproducing the curated data

Run the generators from the repository root; they need no network access (only
`--force` downloads). The recovery and the tests also need the full git history
and tags, at least `v2.0.3`, so they fail in a shallow clone.

```bash
python3 scripts/fetch_official.py --verify   # validate the committed archives; no network, no writes
python3 scripts/recover_editions.py          # rebuild editions/ from data/raw/, git v2.0.3, and source/
python3 scripts/build_editions.py            # CSV, TEI, manifests, per-edition READMEs, docs/EDITIONS.md, this README
python3 scripts/diff_editions.py             # reports/diffs/
PYTHONPATH=src python3 -m byz.contract       # reports/baseline/
PYTHONPATH=src python3 -m byz.reconcile      # reports/reconciliation/ and docs/PROVENANCE.md
```

`python3 scripts/fetch_official.py --force` re-downloads the six archives,
re-extracts them, and rewrites `data/provenance/*.toml`.

Tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests/contract
PYTHONPATH=src python3 -m unittest discover -s tests/curate
PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation
```

See [`scripts/README.md`](scripts/README.md) for the converter details.

## Archiving

A mirror of this repository is available at the [Software Heritage Archive](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/byztxt/byzantine-majority-text).

## Copyright

All the code and text contained in this folder is in the Public Domain.
