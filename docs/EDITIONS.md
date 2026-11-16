# Editions

This repository curates four Robinson-Pierpont texts. Two are **official**
and two are **released**.

- **Official** means published in print by Dr. Maurice A. Robinson.
- **Released** means published as an artifact in this repository.

The official PDFs are the ultimate source of truth. The ZIP archives and
the source files here are machine-readable companions.

## The four editions

| Edition | Status | Basis | Repo releases | PDF |
| --- | --- | --- | --- | --- |
| `rp2005` | official | Published in print by Chilton Book Publishing, Southborough, Massachusetts | none | [`rp2005 PDF`](https://byzantinetext.com/wp-content/uploads/2016/11/editions-rp2.pdf) (`ccf5bb5467408fdd44a362764dc93383ddb5d5579c6601fac0ec0b83a095ecce`) |
| `rp2005-2019` | released | Recovered from git tag v2.0.3 (textonly-beta-code + parsed) | `v1.0.0`-`v2.0.3` | none |
| `rp2018` | official | Published in print by VTR, Nuremberg | none | [`rp2018 PDF`](https://byzantinetext.com/wp-content/uploads/2021/03/robinson-pierpont-2018-gnt-edition.pdf) (`00303ddc443816d363ccca8c3882ce83f4ecb858fa52d0313b80f445d263852c`) |
| `rp2018-2023` | released | Current maintained source; 2018 edition plus 2023 adjustments | `v3.0.0`-`v3.3.4` | none |

## What each edition is

### `rp2005` - official 2005

The published 2005 print edition (Chilton Book Publishing, Southborough,
Massachusetts). The PDF is the ultimate source of truth. The machine-
readable source is the official `.CCT` archive. It has no repo release
number.

### `rp2005-2019` - released 2019 revision of the 2005 lineage

The repo's last pre-2023 text, recovered from tag `v2.0.3`
(`textonly-beta-code` and `parsed`). It was updated in 2019 and is not
the official 2005 print edition. It matches the official 2018 archive in
99.96% of verses and the official 2005 archive in 99.32%, which is why
calling it simply "2005" is misleading. Repo releases: `v1.0.0`-`v2.0.3`.

### `rp2018` - official 2018

The published 2018 print edition (VTR, Nuremberg). The PDF is the
ultimate source of truth. The machine-readable source is the official
`.CCT` archive. It has no repo release number.

### `rp2018-2023` - released 2018 with 2023 adjustments

The current maintained text: the 2018 edition plus the 2023 adjustments
and later minor fixes. It was first released in `v3.0.0` and continues
to receive releases. Repo releases: `v3.0.0`-`v3.3.4` (and later tags).

## Why the history looks messy

- The 2005 lineage lived in `textonly-beta-code`, `parsed`, and
  `csv-unicode` until 2023. It was last updated in 2019.
- Commit `97371d7` (2023-05-30), merged as `v3.0.0`, switched the repo to
  the 2018 edition with 2023 adjustments and introduced `source/`.
- The current tree therefore contains only the 2018+2023 text. The 2005
  lineage is curated here so that nobody has to use `git show` to find it.

## Layout, exports, and verification

Each edition has `source/`, `csv/`, `tei/`, `manifest.json`, and
`README.md`. The manifest records source and artifact SHA-256 hashes.

- Official editions: `csv/` and `tei/` are unaccented main-text exports
  generated from the official ASCII. `source/ccat` holds the official
  `.CCT` source; the PDF is the ultimate source of truth.
- `rp2005-2019`: `csv/main` and `tei/no-accents` are the historical
  released artifacts recovered from `v2.0.3`.
- `rp2018-2023`: `csv/main` and `tei/no-accents` are copied from the
  current working tree (accented CCAT no-variants CSV, unaccented TEI).

```bash
python3 scripts/recover_editions.py
python3 scripts/build_editions.py
python3 scripts/diff_editions.py
```

## Successive diffs

- `rp2005` -> `rp2005-2019`: `reports/diffs/rp2005--rp2005-2019/report.md`
- `rp2005-2019` -> `rp2018`: `reports/diffs/rp2005-2019--rp2018/report.md`
- `rp2018` -> `rp2018-2023`: `reports/diffs/rp2018--rp2018-2023/report.md`
- `rp2005` -> `rp2018`: `reports/diffs/rp2005--rp2018/report.md`

## Source of truth

If a PDF, an archive, and the curated source disagree, the PDF wins and
the conflict must be flagged to the maintainer. Do not silently choose.
