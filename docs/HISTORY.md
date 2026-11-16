# Internal history map

This map is derived from git history only. It does not prove which official archive any file came from; that is the job of the external reconciliation cycle.

## Current HEAD

`c62a53d|2026-11-16|Reorder milestones around existing corpus contract`

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

## Edition mapping (internal evidence)

| Claim | Evidence |
| --- | --- |
| RP2005 is best approximated by the release 2.0.3 Unicode files | `README.md` (Versions section); tag `v2.0.3` |
| Release 3.0.0 introduced RP2018 | `README.md` (Versions section); tags `v3.0.0`..`v3.3.4` |
| The text claims to be up to date as of 2023-07-20 | `README.md`; commits `16859b2`, `18ea8e9`, `a6d4c1e` (all 2023-07-20) |

## Dataset history

| Dataset | First added | Last changed |
| --- | --- | --- |
| `source/CCAT` | `97371d7` (2023-05-31) Update source files and Unicode CSVs | `16859b2` (2023-07-20) Add Pericope Adulterae and Acts 24 beta code |
| `source/Strongs` | `97371d7` (2023-05-31) Update source files and Unicode CSVs | `b7485a3` (2026-11-11) Fix morphology tags per Dr. Robinson (issue #43, partial) |
| `csv-unicode/ccat` | `97371d7` (2023-05-31) Update source files and Unicode CSVs | `27a45ff` (2024-12-31) Clearly mark new paragraphs with a pilcrow sign |
| `csv-unicode/strongs` | `97371d7` (2023-05-31) Update source files and Unicode CSVs | `97371d7` (2023-05-31) Update source files and Unicode CSVs |
| `tei-xml-unicode` | `e9ce9bf` (2022-08-24) Create TEI-XML version | `f2a0cc1` (2023-07-19) Correct edition number in TEI XML |
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
