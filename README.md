<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

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
PDFs are the ultimate source of truth for the printed editions, and
[`data/`](data/) is the index of their authoritative machine-readable sources.
`data/raw/` splits them into two source classes: `print/` for the published
editions and `repo/` for this repository's own lineage.

The published PDFs are committed in the repository: the
[2005 PDF](data/raw/print/rp2005/official-pdf/editions-rp2.pdf) and the
[2018 PDF](data/raw/print/rp2018/official-pdf/robinson-pierpont-2018-gnt-edition.pdf).
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
| Use the official 2018 print edition | [`editions/rp2018/`](editions/rp2018/) and the [2018 PDF](data/raw/print/rp2018/official-pdf/robinson-pierpont-2018-gnt-edition.pdf) |
| Use the official 2005 print edition | [`editions/rp2005/`](editions/rp2005/) and the [2005 PDF](data/raw/print/rp2005/official-pdf/editions-rp2.pdf) |
| Use the 2019 revision of the 2005 lineage | [`editions/rp2005-2019/`](editions/rp2005-2019/) |
| Edit or convert the text | [`data/`](data/) and [`docs/BUILD.md`](docs/BUILD.md) |
| Check provenance and checksums | [`data/provenance/`](data/provenance/) and [`docs/PROVENANCE.md`](docs/PROVENANCE.md) |
| Understand the edition model and its history | [`docs/EDITIONS.md`](docs/EDITIONS.md) and [`docs/HISTORY.md`](docs/HISTORY.md) |

## Official vs released

- **Official** means published in print by Dr. Maurice A. Robinson.
- **Released** means published as an artifact in this repository.

`rp2005` and `rp2018` are therefore official editions; `rp2005-2019` and
`rp2018-2023` are released editions.

## Curated editions

Four editions are curated under [`editions/`](editions/), each with its
own generated `csv/`, `tei/`, `manifest.json`, and `README.md`. Every
edition is outputs only; its inputs live under `data/` and are pinned in
the manifest. `rp2018-2023` is the current text, `rp2018` and `rp2005` are
the official print editions, and `rp2005-2019` is the historical 2019
revision of the 2005 lineage.

| Edition | Status | Repo releases |
| --- | --- | --- |
| `rp2005` | official | none |
| `rp2005-2019` | released | `v1.0.0`-`v2.0.3` |
| `rp2018` | official | none |
| `rp2018-2023` | released | `v3.0.0`-`v4.0.0` |

See [`docs/EDITIONS.md`](docs/EDITIONS.md) and the
[`editions/`](editions/) directory for the full explanation, PDF
links, provenance, manifests, and checksums.

## Generated files

| Generated path | Regenerate with |
| --- | --- |
| `docs/EDITIONS.md` | `PYTHONPATH=src python3 -m byz.build` |
| `data/raw/repo/rp2005-2019/`, `data/provenance/rp2005-2019.toml` | `PYTHONPATH=src python3 -m byz.materialise` |
| `data/README.md`, `data/raw/README.md`, `data/raw/print/README.md`, `data/raw/repo/README.md`, `data/raw/print/<edition>/README.md`, `data/raw/repo/<edition>/README.md`, `data/provenance/rp2018-2023.toml` | `PYTHONPATH=src python3 -m byz.build` |
| `editions/<edition>/README.md` | `PYTHONPATH=src python3 -m byz.build` |
| `editions/<edition>/manifest.json`, `csv/`, `tei/` | `PYTHONPATH=src python3 -m byz.build` |
| `README.md` | `PYTHONPATH=src python3 -m byz.build` |
| `reports/diffs/README.md`, `reports/diffs/<left>--<right>/report.md` | `PYTHONPATH=src python3 -m byz.diff` |
| `docs/HISTORY.md` | `PYTHONPATH=src python3 -m byz.contract`, then `PYTHONPATH=src python3 -m byz.reconcile` |
| `docs/DATA_CONTRACT.md` | `PYTHONPATH=src python3 -m byz.contract` |
| `docs/contract/*.json`, `reports/baseline/summary.md`, `reports/baseline/decision-log.md`, `reports/baseline/*.csv` | `PYTHONPATH=src python3 -m byz.contract` |
| `docs/PROVENANCE.md` | `PYTHONPATH=src python3 -m byz.reconcile` |
| `reports/reconciliation/summary.md`, `reports/reconciliation/decision-log.md`, `reports/reconciliation/*.csv` | `PYTHONPATH=src python3 -m byz.reconcile` |
| `data/provenance/rp2005.toml`, `data/provenance/rp2018.toml` | `PYTHONPATH=src python3 -m byz.fetch` (offline re-record) or `--force` (re-download and re-extract) |

Do not edit any file in this table by hand; the next run overwrites
it. `data/provenance/pdfs.toml` is hand-maintained and is **not**
generated.

## Repository layout

| Path | What it holds |
| --- | --- |
| `editions/` | The four curated editions, each outputs only (`csv/`, `tei/`, `manifest.json`, `README.md`). Start here for a complete text. |
| `data/` | The inputs, split into two source classes: `raw/print/` for the published print editions (archive extracts, preformatted ASCII, and PDFs) and `raw/repo/` for this repository's lineage (the 2019 snapshot and the current text). `provenance/` holds the hashes and URLs. Each folder has a generated README; `raw/repo/CONVENTIONS.md` holds the Beta-code, variant, parsing, and Strong's conventions. |
| `docs/` | `BUILD.md`, `EDITIONS.md`, `PROVENANCE.md`, `HISTORY.md`, `DATA_CONTRACT.md`, `COLLATEX.md`, `assets/`, and `contract/`. |
| `reports/` | `baseline/` (contract snapshot), `reconciliation/` (official-archive comparison), and `diffs/` (successive edition diffs). |
| `src/` | The `byz/` Python package and its module entry points (`byz/fetch.py`, `materialise.py`, `build.py`, `diff.py`, `verify.py`), plus `beta/` (the converter) and `contract/`, `curate/`, `reconcile/`. |
| `tests/` | The `contract/`, `curate/`, and `reconciliation/` suites. |
| `essay/` | Robinson's essay on Byzantine priority, in plain text and translations. |
| `SPECS/` | The mission, technical design, roadmap, and dated cycle specifications. |
| `.opencode/`, `opencode.json` | Configuration for the maintenance agents and commands; not part of the edition data. |
| `LICENSE`, `.gitignore`, `README.md`, `requirements.txt` | Licensing, repository plumbing, and the pinned `beta-code` dependency. |

## Source of truth and provenance

The published PDFs are the ultimate source of truth for the printed editions.
`data/raw/repo/rp2018-2023/{ccat,strongs}/` are the current text's authoritative
machine-readable sources, `data/raw/repo/rp2005-2019/` holds the materialised
2019 lineage, and `data/raw/print/_archives/` holds the committed official ZIP
archives from which the print sources were extracted. `data/provenance/*.toml` pin the SHA-256 of
each archive, PDF, and historical input, and `docs/PROVENANCE.md` records what
was compared and how far the current corpus matches. If a PDF, an archive, and
the curated source disagree, the PDF wins and the conflict is recorded for the
maintainer instead of being resolved automatically.

## Which text should I use?

- `rp2018-2023` for current work. It is the current text described by
  `data/raw/repo/rp2018-2023/` and exported under `editions/rp2018-2023/`.
- `rp2018` to cite or check the official 2018 print edition.
- `rp2005` to cite or check the official 2005 print edition.
- `rp2005-2019` for the repository's 2019 revision of the 2005 lineage. It is
  the 2019 sources rebuilt by the current pipeline, not a copy of the `v2.0.3`
  release's artifacts, and it is not the official 2005 print edition.

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

* A Unicode converter was added in release 1.0.0, but its output unfortunately produced various misspellings. The errors were successfully fixed in release 2.0.3. That tag's text is preserved as the curated `rp2005-2019` edition, rebuilt from its 2019 sources by the current pipeline: the malformed apparatus codes and the typography of the 2019 converter are corrected, and the main text keeps the same words. The Unicode files of releases before 2.0.3 contain conversion errors and should not be used (the source Beta code files, however, did not change between releases 1.0.0 and 2.0.3 and are official as they came directly from Professor Robinson).

* Release 3.0.0 introduced the text of the RP2018 edition, with minor updates to the apparatus. By direct recommendation of professor Robinson, *the use of the RP2005 is discouraged in favor of RP2018*, as RP2005 had "numerous accent, breathing, and punctuation errors (caused by porting over an NA27 file, and then altering only where the Byz text differed)". Additionally, "the 2018 edition should be used, since those errors were corrected". The text was updated "in a very few places", and the apparatus was updated as well in order to "to reflect NA28 and ECM differences in the general epistles and Acts". Note that the *unaccented* text remained highly stable between RP2005 and RP2018.

## Reproducing the curated data

Install the pinned dependency from the repository root:

```bash
pip install -r requirements.txt
```

Run the generators from the repository root; they need no network access (only
`--force` downloads). The materialisation and the worktree-based tests need the
full git history and tags, at least `v2.0.3`, so they fail in a shallow clone.
`byz.contract` additionally requires a git checkout: it inventories only
tracked files, so `git` must be installed and `git ls-files` must work.

```bash
PYTHONPATH=src python3 -m byz.fetch --verify   # validate the committed archives; no network, no writes
PYTHONPATH=src python3 -m byz.fetch            # re-record provenance from the committed archives; offline after --verify
PYTHONPATH=src python3 -m byz.build            # CSV, TEI, manifests, input-tree READMEs, docs/EDITIONS.md, this README, data/provenance/rp2018-2023.toml
PYTHONPATH=src python3 -m byz.diff             # reports/diffs/
PYTHONPATH=src python3 -m byz.contract         # reports/baseline/
PYTHONPATH=src python3 -m byz.reconcile        # reports/reconciliation/ and docs/PROVENANCE.md
PYTHONPATH=src python3 -m byz.verify           # check inputs against data/ and artifacts against the editions
```

`byz.materialise` is an ingest command, not part of the normal rebuild: it
restores `data/raw/repo/rp2005-2019/` and its provenance from tag `v2.0.3`, and is
needed only when that committed tree is missing. `byz.build` reads `data/`
directly and never calls it; it regenerates `rp2005-2019` from the 57 committed
source files like every other edition. Only `byz.materialise` extracts the tag's
files into `data/`, and the build reads `data/` only. (`byz.reconcile` reads the
tag with `git show` for historical comparison, and `byz.build` lists tags for the
release ranges, but neither uses the tag's files as build inputs.)

`byz.build` needs a git checkout with the release tags (it lists them for the
release ranges) and it embeds each input's last commit in the manifests, the
current-text provenance record, the input-tree READMEs, and the baseline history.
A squash or rebase changes that metadata even when no input byte changes: rerun
the generators and commit the result.

Record mode (`PYTHONPATH=src python3 -m byz.fetch`, no flag) reuses the committed
archives and preserves the recorded `downloaded`, `final_url`, and
`http_status` values; it downloads only if an archive is missing or fails its
digest. `PYTHONPATH=src python3 -m byz.fetch --force` always re-downloads the six
archives, re-extracts them, and rewrites `data/provenance/*.toml`, replacing the
recorded timestamps and final Dropbox URLs.

Tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests/contract
PYTHONPATH=src python3 -m unittest discover -s tests/curate
PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation
```

See [`docs/BUILD.md`](docs/BUILD.md) for the build details.

## Archiving

A mirror of this repository is available at the [Software Heritage Archive](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/byztxt/byzantine-majority-text).

## Copyright

All the code and text contained in this folder is in the Public Domain.
