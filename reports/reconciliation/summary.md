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

Current `source/CCAT` is closest to `rp2018`. For `rp2018`, 3 verses differ in main-text letters, 1 in punctuation, 134 are apparatus/variant differences, and 23 are diacritic-ordering differences. Everything is itemised in `verses.csv` and the decision log.

## Derived tier

| Edition | Reference | Dataset | Verses matching |
| --- | --- | --- | ---: |
| `rp2005` | `ascii-one-line` | `csv-unicode/strongs/no-parsing` | 7951/7957 (99.92%) |
| `rp2005` | `ascii-one-line` | `tei-xml-unicode/no-accents` | 7951/7957 (99.92%) |
| `rp2005` | `preformatted` | `csv-unicode/strongs/no-parsing` | 7951/7957 (99.92%) |
| `rp2005` | `preformatted` | `tei-xml-unicode/no-accents` | 7951/7957 (99.92%) |
| `rp2018` | `ascii-one-line` | `csv-unicode/strongs/no-parsing` | 7953/7957 (99.95%) |
| `rp2018` | `ascii-one-line` | `tei-xml-unicode/no-accents` | 7953/7957 (99.95%) |
| `rp2018` | `preformatted` | `csv-unicode/strongs/no-parsing` | 7953/7957 (99.95%) |
| `rp2018` | `preformatted` | `tei-xml-unicode/no-accents` | 7953/7957 (99.95%) |

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
| `source` | `rp2005` | `capitalization` | 1 |
| `source` | `rp2005` | `letters` | 17 |
| `source` | `rp2005` | `punctuation` | 21 |
| `source` | `rp2005` | `variant` | 91 |
| `source` | `rp2005` | `variant-code` | 45 |
| `source` | `rp2018` | `accents-breathings` | 23 |
| `source` | `rp2018` | `letters` | 3 |
| `source` | `rp2018` | `punctuation` | 1 |
| `source` | `rp2018` | `variant` | 89 |
| `source` | `rp2018` | `variant-code` | 45 |

## Decision log

See `reports/reconciliation/decision-log.md`. No canonical source was
selected automatically.
