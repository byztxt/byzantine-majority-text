<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

# Internal history map

This map is derived from git history only. It does not prove which official archive any file came from; that is the job of the external reconciliation cycle.

## Last corpus commit

`636160f` (2026-11-26) Add official archive reconciliation and curated RP editions

## Tags

- `v1.0.0`
- `v1.0.1`
- `v2.0.0`
- `v2.0.1`
- `v2.0.2`
- `v2.0.3`
- `v2016-07-28`
- `v3.0.0`
- `v3.1.0`
- `v3.2.0`
- `v3.3.0`
- `v3.3.1`
- `v3.3.2`
- `v3.3.3`
- `v3.3.4`

`v2016-07-28` is an earlier 2005-lineage snapshot (2017-05-23). It is not
curated as a separate edition: `v2.0.3` is the last pre-2023 release and
supersedes it. The curated `rp2005-2019` source is the `textonly-beta-code`
and `parsed` tree at `v2.0.3` (commit
`8ec95671e463030347c2c643358eb56e58235b19`).

## Edition mapping (internal evidence)

| Claim | Evidence |
| --- | --- |
| RP2005 is best approximated by the release 2.0.3 Unicode files | `README.md` (Versions section); tag `v2.0.3` |
| Release 3.0.0 introduced RP2018 | `README.md` (Versions section); tags `v3.0.0`..`v3.3.4` |
| The text claims to be up to date as of 2023-07-20 | `README.md`; commits `16859b2`, `18ea8e9`, `a6d4c1e` (all 2023-07-20) |

## Dataset history

| Dataset | First added | Last changed |
| --- | --- | --- |
| `data/raw/repo/rp2018-2023/ccat` | `97371d7` (2023-05-31) Update source files and Unicode CSVs | `636160f` (2026-11-26) Add official archive reconciliation and curated RP editions |
| `data/raw/repo/rp2018-2023/strongs` | `97371d7` (2023-05-31) Update source files and Unicode CSVs | `636160f` (2026-11-26) Add official archive reconciliation and curated RP editions |
| `editions/rp2018-2023/csv` | `97371d7` (2023-05-31) Update source files and Unicode CSVs | `636160f` (2026-11-26) Add official archive reconciliation and curated RP editions |
| `editions/rp2018-2023/tei` | `e9ce9bf` (2022-08-24) Create TEI-XML version | `636160f` (2026-11-26) Add official archive reconciliation and curated RP editions |
| `essay` | `e8e5189` (2023-09-03) Add Robinson's Case for Byz Priority essay | `d84f8e7` (2023-09-06) Update README |

## June-September 2023 commits touching the corpus

- `d84f8e7` (2023-09-06) Update README
- `0709c3f` (2023-09-06) Add Spanish translation
- `168284c` (2023-09-05) Add author's name
- `e8e5189` (2023-09-03) Add Robinson's Case for Byz Priority essay
- `18ea8e9` (2023-07-20) Update B to Byz in apparatuses
- `a6d4c1e` (2023-07-20) Rename files
- `16859b2` (2023-07-20) Add Pericope Adulterae and Acts 24 beta code
- `161a821` (2023-07-19) Add documentation
- `f2a0cc1` (2023-07-19) Correct edition number in TEI XML
- `a14f9b9` (2023-07-19) Replace apostrophes with right quotation marks

## What this does not establish

- Which official archive (2005 vs 2018) each source file came from.
- Whether the committed CSV/TEI outputs match the current source.
- Whether the current text is RP2018, RP2018 plus July 2023 fixes, or a mix.

These are open questions for the maintainer and the external reconciliation cycle.

<!-- cycle2:begin -->
## External archive evidence (Cycle 2)

| Edition | Source verses matching official CCAT |
| --- | ---: |
| `rp2005` | 7769/7972 (97.45%) |
| `rp2018` | 7811/7972 (97.98%) |

| State | Compared to | Verses matching |
| --- | --- | ---: |
| `v2.0.3 textonly-beta-code` | `rp2005` | 7918/7972 (99.32%) |
| `v2.0.3 textonly-beta-code` | `rp2018` | 7969/7972 (99.96%) |
| `v3.0.0 source/CCAT` | `rp2005` | 7754/7957 (97.45%) |
| `v3.0.0 source/CCAT` | `rp2018` | 7796/7957 (97.98%) |
| `current data/raw/repo/rp2018-2023/ccat` | `rp2005` | 7769/7972 (97.45%) |
| `current data/raw/repo/rp2018-2023/ccat` | `rp2018` | 7811/7972 (97.98%) |

Closest official edition for the current source: `rp2018`.
The current `data/raw/repo/rp2018-2023/ccat` was first added in `97371d7` (2023-05-30, merged in `v3.0.0`). The 2005-lineage text is in `textonly-beta-code` at `v2.0.3` and earlier, last updated 2019. See `docs/PROVENANCE.md`.
<!-- cycle2:end -->
