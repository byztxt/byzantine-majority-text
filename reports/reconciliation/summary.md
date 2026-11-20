<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

# Official archive reconciliation

Read-only comparison of the current corpus against the six official
archives. No source, CSV, or TEI file was changed.

## Commands

```bash
python3 scripts/fetch_official.py --verify
PYTHONPATH=src python3 -m byz.reconcile
PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation -v
```

## Source tier (`source/CCAT/*.TXT` vs official `.CCT`)

| Edition | Files compared | Normalized matches | Verses matching |
| --- | ---: | ---: | ---: |
| `rp2005` | 29 | 7 | 7769/7972 (97.45%) |
| `rp2018` | 29 | 11 | 7811/7972 (97.98%) |

**Closest edition:** `rp2018`.

Current `source/CCAT` is closest to `rp2018`. For `rp2018`, 0 verses differ in main-text letters, 2 in punctuation, 134 are apparatus/variant differences, and 23 are diacritic-ordering differences. Everything is itemised in `verses.csv` and the decision log.


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

## Derived tier

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

## Mapping coverage

| Class | Files |
| --- | ---: |
| `auxiliary` | 3 |
| `exact-transliteration` | 196 |
| `incomparable-pending-pipeline` | 58 |
| `normalized` | 18 |
| `provenance-unknown` | 27 |
| `textual` | 60 |

`files.csv` lists every mapped file, including the 27 Strong's files
with `provenance-unknown` and the accented CCAT CSV views marked
`incomparable-pending-pipeline`.

## Strong's / BP5

Status: `provenance-unknown`. The official archives do not
include a parsed/Strong's file, so its provenance remains unknown.

## Intentional blanks

LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 are blank in the official
CCAT archives; D7 is confirmed.

## Categories

| Tier | Edition | Category | Count |
| --- | --- | --- | ---: |
| `derived` | `rp2005` | `letters` | 8 |
| `derived` | `rp2005` | `word-segmentation` | 16 |
| `derived` | `rp2018` | `word-segmentation` | 16 |
| `source` | `rp2005` | `accents-breathings` | 28 |
| `source` | `rp2005` | `capitalization` | 7 |
| `source` | `rp2005` | `letters` | 2 |
| `source` | `rp2005` | `punctuation` | 26 |
| `source` | `rp2005` | `variant` | 91 |
| `source` | `rp2005` | `variant-code` | 45 |
| `source` | `rp2005` | `word-segmentation` | 4 |
| `source` | `rp2018` | `accents-breathings` | 23 |
| `source` | `rp2018` | `capitalization` | 2 |
| `source` | `rp2018` | `punctuation` | 2 |
| `source` | `rp2018` | `variant` | 89 |
| `source` | `rp2018` | `variant-code` | 45 |

## Decision log

See `reports/reconciliation/decision-log.md`. No canonical source was
selected automatically.
