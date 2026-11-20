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

The published PDFs are committed in the repository: the
[2005 PDF](data/raw/rp2005/official-pdf/editions-rp2.pdf) and the
[2018 PDF](data/raw/rp2018/official-pdf/robinson-pierpont-2018-gnt-edition.pdf).
Their publisher URLs and SHA-256 hashes are recorded in
[`data/provenance/pdfs.toml`](data/provenance/pdfs.toml). The 2005 edition is
also available from
[The Internet Archive](https://archive.org/details/newtestamentrobinsonpierpontbyzantine/),
and the 2018 edition from
[its Internet Archive record](https://archive.org/details/robinson-pierpont-2018-gnt-edition).
RP2018 is recommended over RP2005 for all practical purposes (read the details
below). Additional resources are available at
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
| Read or download the current text as CSV or TEI | [`editions/rp2018-2023/`](editions/rp2018-2023/) |
| Use the official 2018 print edition | [`editions/rp2018/`](editions/rp2018/) and the [2018 PDF](data/raw/rp2018/official-pdf/robinson-pierpont-2018-gnt-edition.pdf) |
| Use the official 2005 print edition | [`editions/rp2005/`](editions/rp2005/) and the [2005 PDF](data/raw/rp2005/official-pdf/editions-rp2.pdf) |
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
<!-- generated-block: do not edit by hand -->
> **Generated section. Do not edit by hand.**
> This block is produced by `python3 scripts/build_editions.py`; the rest of
> this README is hand-written.

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

## Generated files

| Generated path | Regenerate with |
| --- | --- |
| `docs/EDITIONS.md` | `python3 scripts/build_editions.py` |
| `editions/<edition>/source/` | `python3 scripts/recover_editions.py` (`build_editions.py` re-runs it) |
| `editions/<edition>/README.md` | `python3 scripts/build_editions.py` |
| `editions/<edition>/manifest.json`, `csv/`, `tei/` | `python3 scripts/build_editions.py` |
| this README's generated editions block | `python3 scripts/build_editions.py` |
| `reports/diffs/README.md`, `reports/diffs/<left>--<right>/report.md` | `python3 scripts/diff_editions.py` |
| `docs/HISTORY.md` | `PYTHONPATH=src python3 -m byz.contract`, then `PYTHONPATH=src python3 -m byz.reconcile` |
| `docs/DATA_CONTRACT.md` | `PYTHONPATH=src python3 -m byz.contract` |
| `docs/contract/*.json`, `reports/baseline/summary.md`, `reports/baseline/decision-log.md`, `reports/baseline/*.csv` | `PYTHONPATH=src python3 -m byz.contract` |
| `docs/PROVENANCE.md` | `PYTHONPATH=src python3 -m byz.reconcile` |
| `reports/reconciliation/summary.md`, `reports/reconciliation/decision-log.md`, `reports/reconciliation/*.csv` | `PYTHONPATH=src python3 -m byz.reconcile` |
| `data/provenance/rp2005.toml`, `data/provenance/rp2018.toml` | `python3 scripts/fetch_official.py` (offline re-record) or `--force` (re-download and re-extract) |

Do not edit any file in this table by hand; the next run overwrites
it. The rest of this README is hand-written.
`data/provenance/pdfs.toml` is hand-maintained and is **not**
generated.

<!-- editions:end -->

## Repository layout

| Path | What it holds |
| --- | --- |
| `editions/` | The four curated editions, each self-contained (source, CSV, TEI, manifest, README). Start here for a complete text. |
| `source/` | The official Beta-code source files for the current text: accented `CCAT/` and parsed `Strongs/`. |
| `data/` | Official ZIP archives (`raw/_archives/`, committed), extracted archive trees (`raw/<edition>/`), the published PDFs, and `provenance/` hashes and URLs. |
| `docs/` | `EDITIONS.md`, `PROVENANCE.md`, `HISTORY.md`, `DATA_CONTRACT.md`, `COLLATEX.md`, `RELEASE-NOTES.md`, `assets/`, and `contract/`. |
| `reports/` | `baseline/` (contract snapshot), `reconciliation/` (official-archive comparison), and `diffs/` (successive edition diffs). |
| `scripts/` | The build, recovery, diff, and fetch entry points, plus the shared Beta-code converter module. |
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
the curated source disagree, the PDF wins and the conflict is recorded for the
maintainer instead of being resolved automatically.

## Which text should I use?

- `rp2018-2023` for current work. It is the current text described by
  `source/` and exported under `editions/rp2018-2023/`.
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
system, so recovering the exact wordings of those editions from the Git
history alone is not straightforward; they are curated from the official
archives instead.

It is strongly recommended that versions `3.x.x` be used instead of previous
ones, for at least the following reasons:

* Previous to release 1.0.0 there was *no* Unicode version of the files. The source files (which were in a custom flavor of Beta code) *were* however in the repository and can be accessed by browsing the Git history.

* A Unicode converter was added in release 1.0.0, but its output unfortunately produced various misspellings. The errors were successfully fixed in release 2.0.3. That tag is preserved as the curated `rp2005-2019` edition. The Unicode files of releases before 2.0.3 contain conversion errors and should not be used (the source Beta code files, however, did not change between releases 1.0.0 and 2.0.3 and are official as they came directly from Professor Robinson).

* Release 3.0.0 introduced the text of the RP2018 edition, with minor updates to the apparatus. By direct recommendation of professor Robinson, *the use of the RP2005 is discouraged in favor of RP2018*, as RP2005 had "numerous accent, breathing, and punctuation errors (caused by porting over an NA27 file, and then altering only where the Byz text differed)". Additionally, "the 2018 edition should be used, since those errors were corrected". The text was updated "in a very few places", and the apparatus was updated as well in order to "to reflect NA28 and ECM differences in the general epistles and Acts". Note that the *unaccented* text remained highly stable between RP2005 and RP2018.

## Reproducing the curated data

Run the generators from the repository root; they need no network access (only
`--force` downloads). The recovery and the tests also need the full git history
and tags, at least `v2.0.3`, so they fail in a shallow clone. `byz.contract`
additionally requires a git checkout: it inventories only tracked files, so
`git` must be installed and `git ls-files` must work.

```bash
python3 scripts/fetch_official.py --verify   # validate the committed archives; no network, no writes
python3 scripts/fetch_official.py            # re-record provenance from the committed archives; offline after --verify
python3 scripts/recover_editions.py          # freeze edition inputs only; build_editions.py writes the views
python3 scripts/build_editions.py            # CSV, TEI, manifests, per-edition READMEs, docs/EDITIONS.md, this README
python3 scripts/diff_editions.py             # reports/diffs/
PYTHONPATH=src python3 -m byz.contract       # reports/baseline/
PYTHONPATH=src python3 -m byz.reconcile      # reports/reconciliation/ and docs/PROVENANCE.md
```

`recover_editions.py` only freezes the inputs (the current edition's `source/`
snapshot and the historical artifacts recovered from git); it does not write the
CSV/TEI views. Running it alone leaves every `editions/<edition>/csv/` and
`tei/` empty, so always follow it with `build_editions.py`, which also re-runs
the recovery before building.

Record mode (`python3 scripts/fetch_official.py`, no flag) reuses the committed
archives and preserves the recorded `downloaded`, `final_url`, and
`http_status` values; it downloads only if an archive is missing or fails its
digest. `python3 scripts/fetch_official.py --force` always re-downloads the six
archives, re-extracts them, and rewrites `data/provenance/*.toml`, replacing the
recorded timestamps and final Dropbox URLs.

Tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests/contract
PYTHONPATH=src python3 -m unittest discover -s tests/curate
PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation
```

See [`scripts/README.md`](scripts/README.md) for the build details.

## Archiving

A mirror of this repository is available at the [Software Heritage Archive](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/byztxt/byzantine-majority-text).

## Copyright

All the code and text contained in this folder is in the Public Domain.
