# Provenance

External evidence gathered in Cycle 2. The source files remain
authoritative; these records describe the official archives and how far
the current corpus matches them.

## Archives

| Edition | Archive | SHA-256 | Size (bytes) |
| --- | --- | --- | ---: |
| `rp2005` | `editions-rp2-preformatted.zip` | `e8719d9eafa4239fb5131e80cc1b5584915ad2efd37aac2783fcc484e438f3a3` | 336188 |
| `rp2005` | `editions-rp2-ascii.zip` | `c85ccdcbccee55fbb0ca7744352330806f505514b28a6ae02302843f65a86a2a` | 324893 |
| `rp2005` | `editions-rp2-ccat.zip` | `d172e27a6adf77459cb08c2dc67a57b69239bb27605791c3d1cfaadcda97e2e2` | 471157 |
| `rp2018` | `rp2018-ascii.zip` | `cd8634562b6c8ae77fb04c2045e306fb7bd3a1870944bb569926d6d94dc3991c` | 325063 |
| `rp2018` | `rp2018-ascii-one-line-per-verse.zip` | `5ea075d9d52d85511ce627be258fcc78e901d08e8a912dda96dffe977add7fb6` | 324888 |
| `rp2018` | `rp2018-ccat.ZIP` | `55eae8ffc5679fc740318e7b520b283393ca09c66b7a6c1934336d54eca3a394` | 469973 |

The original zips live under `data/raw/_archives/` (gitignored); the
extracted inputs are committed under `data/raw/<edition>/`.

## Match verdict

| Edition | Source files normalized | Source verses matching |
| --- | ---: | ---: |
| `rp2005` | 7/29 | 7769/7972 (97.45%) |
| `rp2018` | 11/29 | 7811/7972 (97.98%) |

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

## Strong's / BP5 provenance

Status: `provenance-unknown`.
None of the six official archives contains a parsed/Strong's file, so `source/Strongs/*.BP5` remains provenance-unknown.

## Intentional blanks (D7)

LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 are present as blank
references in the official CCAT archives, confirming D7.

## Decisions

See `reports/reconciliation/decision-log.md`.
