<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

# Provenance

External evidence gathered in Cycle 2. The published PDFs are the
ultimate source of truth for the printed editions, and `source/` is the
authoritative machine-readable text for the derivatives. These records
describe the official archives and how far the current corpus matches
them.

## Archives

All six archives were initially obtained from the Byzantine Text editions
listing page <https://byzantinetext.com/study/editions/robinson-pierpont/> in November 2026.
The recorded download timestamps are `2026-11-16T18:37:00Z` through `2026-11-16T18:37:10Z`.
Each `[[archives]]` record in `data/provenance/rp2005.toml` and
`data/provenance/rp2018.toml` carries the listing page as `source_page`,
alongside the per-file Dropbox URL and SHA-256.

| Edition | Archive | SHA-256 | Size (bytes) |
| --- | --- | --- | ---: |
| `rp2005` | `editions-rp2-preformatted.zip` | `e8719d9eafa4239fb5131e80cc1b5584915ad2efd37aac2783fcc484e438f3a3` | 336188 |
| `rp2005` | `editions-rp2-ascii.zip` | `c85ccdcbccee55fbb0ca7744352330806f505514b28a6ae02302843f65a86a2a` | 324893 |
| `rp2005` | `editions-rp2-ccat.zip` | `d172e27a6adf77459cb08c2dc67a57b69239bb27605791c3d1cfaadcda97e2e2` | 471157 |
| `rp2018` | `rp2018-ascii.zip` | `cd8634562b6c8ae77fb04c2045e306fb7bd3a1870944bb569926d6d94dc3991c` | 325063 |
| `rp2018` | `rp2018-ascii-one-line-per-verse.zip` | `5ea075d9d52d85511ce627be258fcc78e901d08e8a912dda96dffe977add7fb6` | 324888 |
| `rp2018` | `rp2018-ccat.ZIP` | `55eae8ffc5679fc740318e7b520b283393ca09c66b7a6c1934336d54eca3a394` | 469973 |

The original zips are committed under `data/raw/_archives/` and are
pinned by SHA-256 in `data/provenance/*.toml`. The extracted inputs
under `data/raw/<edition>/` are produced from those zips; they are not
separately hashed in the provenance files.

## Match verdict

| Edition | Source files normalized | Source verses matching |
| --- | ---: | ---: |
| `rp2005` | 7/29 | 7769/7972 (97.45%) |
| `rp2018` | 11/29 | 7811/7972 (97.98%) |

| Edition | Reference | Dataset | Verses matching |
| --- | --- | --- | ---: |
| `rp2005` | `ascii-one-line` | `editions/rp2018-2023/csv/strongs/no-parsing` | 7951/7957 (99.92%) |
| `rp2005` | `ascii-one-line` | `editions/rp2018-2023/tei/unaccented` | 7951/7957 (99.92%) |
| `rp2005` | `preformatted` | `editions/rp2018-2023/csv/strongs/no-parsing` | 7951/7957 (99.92%) |
| `rp2005` | `preformatted` | `editions/rp2018-2023/tei/unaccented` | 7951/7957 (99.92%) |
| `rp2018` | `ascii-one-line` | `editions/rp2018-2023/csv/strongs/no-parsing` | 7953/7957 (99.95%) |
| `rp2018` | `ascii-one-line` | `editions/rp2018-2023/tei/unaccented` | 7953/7957 (99.95%) |
| `rp2018` | `preformatted` | `editions/rp2018-2023/csv/strongs/no-parsing` | 7953/7957 (99.95%) |
| `rp2018` | `preformatted` | `editions/rp2018-2023/tei/unaccented` | 7953/7957 (99.95%) |

## Historical lineage

| State | Compared to | Files fully matching | Verses matching |
| --- | --- | ---: | ---: |
| `v2.0.3 textonly-beta-code` | `rp2005` | 13/29 | 7918/7972 (99.32%) |
| `v2.0.3 textonly-beta-code` | `rp2018` | 26/29 | 7969/7972 (99.96%) |
| `v3.0.0 source/CCAT` | `rp2005` | 5/27 | 7754/7957 (97.45%) |
| `v3.0.0 source/CCAT` | `rp2018` | 9/27 | 7796/7957 (97.98%) |
| `current source/CCAT` | `rp2005` | 7/29 | 7769/7972 (97.45%) |
| `current source/CCAT` | `rp2018` | 11/29 | 7811/7972 (97.98%) |

- The current `source/CCAT` was first added in commit `97371d7` (2023-05-30) and merged in `v3.0.0` (2023-05-31, PR #25 'update_to_2023'). It is the 2018 edition with 2023 adjustments.
- The 2005-lineage text lives in `textonly-beta-code` at `v2.0.3` and earlier; it was last updated in 2019.
- `v2.0.3` matches official 2018 in 7969/7972 verses (99.96%) but official 2005 in 7918/7972 (99.32%). It is therefore a 2019 revision of the 2005 edition, not the official 2005 archive itself.
- The current source matches official 2018 in 7811/7972 (97.98%) and official 2005 in 7769/7972 (97.45%).
- So the current tree does **not** contain the 2005 text. Comparing it with the official 2005 archive is a cross-check, not an identification.


## Strong's / BP5 provenance

Status: `provenance-unknown`.
None of the six official archives contains a parsed/Strong's file, so `source/Strongs/*.BP5` remains provenance-unknown.

## Intentional blanks (D7)

LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 are present as blank
references in the official CCAT archives, confirming D7.

## Decisions

See `reports/reconciliation/decision-log.md`.
