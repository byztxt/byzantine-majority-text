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

## Source feature matrix

| Source | Provenance | Accents | Strong's | Apparatus | Parsing |
| --- | --- | --- | --- | --- | --- |
| Official 2005/2018 `ccat` (`.CCT`) | official archive | yes | no | yes | no |
| Official 2005/2018 ASCII / preformatted | official archive | no | no | no | no |
| Official 2005/2018 PDFs | published print | yes | no | yes | no |
| `source/CCAT` | repo 2018+2023 | yes | no | yes | no |
| `source/Strongs` | repo lineage, not in the six ZIPs | no | yes | no | yes |
| `textonly-beta-code` (v2.0.3) | repo 2005 lineage, 2019 | yes | no | yes | no |
| `parsed` (v2.0.3) | repo parsed lineage | no | yes | yes | yes |
| `textonly-online-bible` (v2.0.3) | repo 2005 lineage | no | no | no | no |

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

- Official editions: accented CSV (with/without variants) and accented
  TEI are generated from the official `.CCT`; unaccented CSV/TEI are
  generated from the official ASCII. Strong's/parsing are absent because
  the official URL files do not contain them.
- `rp2005-2019`: accented with/without variants, unaccented, Strong's
  with/no parsing, and accented/unaccented TEI are recovered or generated
  from `v2.0.3`.
- `rp2018-2023`: the same views are copied or generated from the current
  working tree.

## Blank verses and omitted rows

LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 are not part of the
Byzantine tradition. The official `.CCT` and ASCII archives do not
contain them, so `rp2005` and `rp2018` have no row for them at all;
that is expected, not a conversion loss. `rp2018-2023` keeps them as
explicit empty rows (empty CSV text and empty `<ab/>` in TEI).
`rp2005-2019` inherits the same omission from tag `v2.0.3`: its
unaccented CSV has 7953 rows instead of 7957 and its TEI has no empty
`<ab/>` for those verses. Those historical artifacts must stay
byte-identical to `v2.0.3`, so the rows are deliberately not added
back; the edition README records the omission.

## TEI punctuation

Generated TEI wraps each whitespace-separated token in `<w>`. A
standalone `-` (the official text's dash and deletion marks) is
emitted as `<pc>-</pc>`, and a leading `¶` becomes
`<milestone unit="paragraph" type="start"/>` instead of being glued to
the following word. Punctuation attached to a word stays inside its
`<w>`. Only the accented TEI contains these two markers; the unaccented
TEI has neither, so its markup is unchanged.

## Derived artifacts by edition

| Edition | Accented no-variants | Accented with-variants | Unaccented | Strong's with-parsing | Strong's no-parsing | Accented TEI | Unaccented TEI |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `rp2005` | yes | yes | yes | no | no | yes | yes |
| `rp2005-2019` | yes | yes | yes | yes | yes | yes | yes |
| `rp2018` | yes | yes | yes | no | no | yes | yes |
| `rp2018-2023` | yes | yes | yes | yes | yes | yes | yes |

Where a source carries accents, Strong's, apparatus, or parsing, the
edition provides the corresponding derived view. Official editions
have no Strong's/parsing view because those data are not in the official
URL files.

Accented CSV also includes the `PA` and `ACT24` section files where the
source provides them. TEI is the 27-book main text.

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

Successive diffs compare the **source-tier main text** (official `.CCT`,
historical `textonly-beta-code`, or current `source/CCAT`), not the
generated CSV/TEI views.

## Source of truth

If a PDF, an archive, and the curated source disagree, the PDF wins and
the conflict must be flagged to the maintainer. Do not silently choose.
