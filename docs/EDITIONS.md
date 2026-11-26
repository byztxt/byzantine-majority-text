<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

# Editions

This repository curates four Robinson-Pierpont texts. Two are **official**
and two are **released**.

- **Official** means published in print by Dr. Maurice A. Robinson.
- **Released** means published as an artifact in this repository.

The official PDFs are the ultimate source of truth. The ZIP archives and
`data/raw/repo/rp2018-2023/` are the authoritative machine-readable text for the
derivatives.

For where everything lives in the repository, see the layout table in
the [root README](../README.md#repository-layout).

## The four editions

| Edition | Status | Basis | Repo releases | PDF (committed) |
| --- | --- | --- | --- | --- |
| `rp2005` | official | Published in print by Chilton Book Publishing, Southborough, Massachusetts | none | [`rp2005 PDF`](../data/raw/print/rp2005/official-pdf/editions-rp2.pdf) (`ccf5bb5467408fdd44a362764dc93383ddb5d5579c6601fac0ec0b83a095ecce`) |
| `rp2005-2019` | released | The 2019 sources (textonly-beta-code + parsed), rebuilt by the current pipeline | [`v1.0.0`](https://github.com/byztxt/byzantine-majority-text/releases/tag/v1.0.0)-[`v2.0.3`](https://github.com/byztxt/byzantine-majority-text/releases/tag/v2.0.3) | none |
| `rp2018` | official | Published in print by VTR, Nuremberg | none | [`rp2018 PDF`](../data/raw/print/rp2018/official-pdf/robinson-pierpont-2018-gnt-edition.pdf) (`00303ddc443816d363ccca8c3882ce83f4ecb858fa52d0313b80f445d263852c`) |
| `rp2018-2023` | released | Current maintained source; 2018 edition plus 2023 adjustments | [`v3.0.0`](https://github.com/byztxt/byzantine-majority-text/releases/tag/v3.0.0)-[`v3.3.4`](https://github.com/byztxt/byzantine-majority-text/releases/tag/v3.3.4) | none |

## Source feature matrix

| Source | Provenance | Accents | Strong's | Apparatus | Parsing |
| --- | --- | --- | --- | --- | --- |
| Official 2005/2018 `ccat` (`.CCT`) | official archive | yes | no | yes | no |
| Official 2005/2018 ASCII / preformatted | official archive | no | no | no | no |
| Official 2005/2018 PDFs | published print | yes | no | yes | no |
| `data/raw/repo/rp2018-2023/ccat` | repo 2018+2023 | yes | no | yes | no |
| `data/raw/repo/rp2018-2023/strongs` | official files, not in the six ZIPs | no | yes | no | yes |
| `textonly-beta-code` (2019 sources) | `data/raw/repo/rp2005-2019/` | yes | no | yes | no |
| `parsed` (2019 sources) | `data/raw/repo/rp2005-2019/` | no | yes | yes | yes |

The `textonly-beta-code` and `parsed` sources are committed at
`data/raw/repo/rp2005-2019/`, with `data/provenance/rp2005-2019.toml`
recording tag [`v2.0.3`](https://github.com/byztxt/byzantine-majority-text/releases/tag/v2.0.3), its commit, and every file hash.
`byz.materialise` restores that tree from the tag. The tag's released
CSV/TEI are not inputs and are not used by the build.

## What each edition is

### `rp2005` - official 2005

The published 2005 print edition (Chilton Book Publishing, Southborough,
Massachusetts). The PDF is the ultimate source of truth. The machine-
readable source is the official `.CCT` archive. It has no repo release
number.

### `rp2005-2019` - released 2019 revision of the 2005 lineage

The repo's last pre-2023 text. Its 2019 `textonly-beta-code` and
`parsed` sources are committed at `data/raw/repo/rp2005-2019/`, and every
view is regenerated from them by the current pipeline. It was updated
in 2019 and is not the official 2005 print edition. It matches the
official 2018 archive in
99.96% of verses and the official 2005 archive in 99.32%, which is why
calling it simply "2005" is misleading. Repo releases: [`v1.0.0`](https://github.com/byztxt/byzantine-majority-text/releases/tag/v1.0.0)-[`v2.0.3`](https://github.com/byztxt/byzantine-majority-text/releases/tag/v2.0.3).

### `rp2018` - official 2018

The published 2018 print edition (VTR, Nuremberg). The PDF is the
ultimate source of truth. The machine-readable source is the official
`.CCT` archive. It has no repo release number.

### `rp2018-2023` - released 2018 with 2023 adjustments

The current maintained text: the 2018 edition plus the 2023 adjustments
and later minor fixes. It was first released in [`v3.0.0`](https://github.com/byztxt/byzantine-majority-text/releases/tag/v3.0.0) and continues
to receive releases. Repo releases: [`v3.0.0`](https://github.com/byztxt/byzantine-majority-text/releases/tag/v3.0.0)-[`v3.3.4`](https://github.com/byztxt/byzantine-majority-text/releases/tag/v3.3.4) (and later tags).

## Why the history looks messy

- The 2005 lineage lived in `textonly-beta-code`, `parsed`, and
  `csv-unicode` until 2023. It was last updated in 2019.
- Commit [`97371d7`](https://github.com/byztxt/byzantine-majority-text/commit/97371d7) (2023-05-30), merged as [`v3.0.0`](https://github.com/byztxt/byzantine-majority-text/releases/tag/v3.0.0), switched the repo to
  the 2018 edition with 2023 adjustments and introduced `source/`.
- The current tree therefore contains only the 2018+2023 text. The 2005
  lineage is curated here so that nobody has to use `git show` to find it.

Per-release change notes live in the repository's
[GitHub releases](https://github.com/byztxt/byzantine-majority-text/releases); this page describes the
editions themselves.

## Layout, exports, and verification

Each edition has `csv/`, `tei/`, `manifest.json`, and `README.md`.
The edition contains outputs only: its inputs live under `data/` and
are pinned in the manifest's `inputs` list by repository-relative
path and SHA-256. `PYTHONPATH=src python3 -m byz.verify` checks the
inputs against `data/` and the artifacts against the edition; a
downloaded edition can be checked for artifact integrity with
`--edition-dir`. An edition can no longer verify its own inputs:
`--edition-dir` checks the shipped artifacts only and cannot prove
they came from the pinned inputs.

- Official editions: accented CSV (with/without variants) and accented
  TEI are generated from the official `.CCT`; unaccented CSV/TEI are
  generated from the official ASCII. Strong's/parsing are absent because
  the official URL files do not contain them.
- `rp2005-2019`: accented with/without variants, unaccented,
  Strong's with/no parsing, and accented/unaccented TEI are generated
  from the 2019 sources committed at `data/raw/repo/rp2005-2019/`. Word
  spacing in the unaccented view follows the parsed source.
- `rp2018-2023`: every view is generated from the committed
  `data/raw/repo/rp2018-2023/` inputs.

## Where the edition snapshots went (2026-11-25)

Each edition used to carry a frozen copy of its inputs under `source/`.
That copy was removed on 2026-11-25: every input now lives under `data/`,
and `manifest.json` pins it by repository-relative path and SHA-256. An
edition is outputs only (`csv/`, `tei/`, `manifest.json`, `README.md`).
No `editions/<edition>/source/` directory remains.
`byz.verify` (run as `PYTHONPATH=src python3 -m byz.verify`) checks the
inputs against `data/` and the artifacts against the edition.

| Retired snapshot | Now |
| --- | --- |
| `editions/rp2005/source/ccat/` | `data/raw/print/rp2005/ccat/` |
| `editions/rp2018/source/ccat/` | `data/raw/print/rp2018/ccat/` |
| `editions/rp2018-2023/source/` | `data/raw/repo/rp2018-2023/` |
| `editions/rp2005-2019/source/` | `data/raw/repo/rp2005-2019/` |
| `manifest.json source_files` | `manifest.json inputs` |

The revision releasing this change replaces `source_files` with
`inputs`; `artifact_files` is unchanged for the three editions whose
text does not change. A manifest that still has `source_files`, or
lacks `inputs`, is invalid, and no input root may point under
`editions/`.

Only two [`v2.0.3`](https://github.com/byztxt/byzantine-majority-text/releases/tag/v2.0.3) prefixes are inputs: the 57
`textonly-beta-code` and `parsed` files committed at
`data/raw/repo/rp2005-2019/`. Only `byz.materialise` extracts the tag's
files into `data/`; the build reads `data/` only. (`byz.reconcile`
reads the tag with `git show` for historical comparison, and
`byz.build` lists tags for the release ranges, but neither uses the
tag's files as build inputs.)
`rp2005-2019` is **regenerated** from those sources by the same pipeline
as the other editions. Its released CSV/TEI are evidence of the 2019
converter's output, not what this repository publishes: regeneration
corrects the malformed apparatus codes (`{Ν`/`{Β` become
`{NA`/`{Byz`) and normalises typography, without changing the main
text's words.

The released-artifact prefixes of [`v2.0.3`](https://github.com/byztxt/byzantine-majority-text/releases/tag/v2.0.3) map to the
regenerated views as follows. Those outputs are now **regenerated**
from the same tag's 57 sources, so they are not byte-identical to the
release: the apparatus codes and the typography differ.

| Released [`v2.0.3`](https://github.com/byztxt/byzantine-majority-text/releases/tag/v2.0.3) prefix | Regenerated view |
| --- | --- |
| `csv-unicode/accents/no-variants/` | `editions/rp2005-2019/csv/accented/no-variants/` |
| `csv-unicode/accents/with-variants/` | `editions/rp2005-2019/csv/accented/with-variants/` |
| `csv-unicode/no-accents/` | `editions/rp2005-2019/csv/unaccented/` |
| `tei-xml-unicode/no-accents/` | `editions/rp2005-2019/tei/unaccented/` |

See [`COLLATEX.md`](COLLATEX.md) for using the unaccented TEI with
CollateX.

## Where the inputs moved into the print and repo classes (2026-11-25)

`data/raw/` has two source classes. `data/raw/print/` holds material
from the published print editions, including the six committed ZIP
archives; `data/raw/repo/` holds this repository's own lineage. Every
input tree belongs to exactly one class, and each source folder is named
after its edition id directly under its class.

The current text stopped being a special case: `data/text/` no longer
exists, and `data/raw/repo/rp2018-2023/{ccat,strongs}/` is a source
snapshot like the 2019 lineage. The Beta-code, variant, parsing, and
Strong's conventions moved to the hand-maintained
`data/raw/repo/CONVENTIONS.md`, inside the repo class.

| Retired input path | Now |
| --- | --- |
| `data/text/CCAT/` | `data/raw/repo/rp2018-2023/ccat/` |
| `data/text/Strongs/` | `data/raw/repo/rp2018-2023/strongs/` |
| `data/text/README.md` | `data/raw/repo/CONVENTIONS.md` |
| `data/raw/rp2005/editions-rp2-ccat/` | `data/raw/print/rp2005/ccat/` |
| `data/raw/rp2005/editions-rp2-ascii/` | `data/raw/print/rp2005/ascii/` |
| `data/raw/rp2005/editions-rp2-preformatted/` | `data/raw/print/rp2005/preformatted/` |
| `data/raw/rp2005/official-pdf/` | `data/raw/print/rp2005/official-pdf/` |
| `data/raw/rp2018/rp2018-ccat/` | `data/raw/print/rp2018/ccat/` |
| `data/raw/rp2018/rp2018-ascii-one-line-per-verse/` | `data/raw/print/rp2018/ascii/` |
| `data/raw/rp2018/rp2018-ascii/` | `data/raw/print/rp2018/preformatted/` |
| `data/raw/rp2018/official-pdf/` | `data/raw/print/rp2018/official-pdf/` |
| `data/raw/_archives/` | `data/raw/print/_archives/` |
| `data/raw/rp2005-2019/` | `data/raw/repo/rp2005-2019/` |
| `data/provenance/pdfs.toml path` | `data/raw/print/<edition>/official-pdf/` |
| `manifest pdf key` | `data/raw/print/<edition>/official-pdf/` |

Only the paths changed: every source byte and SHA-256 is unchanged, and
all 672 edition CSV/TEI artifacts keep their `artifact_files` hashes.
The two official `pdf` values in the manifests and in
`data/provenance/pdfs.toml` gained the `print/` segment so the hand-
maintained record and the generated manifest cannot disagree.
These paths are not aliased: no symlink, stub README, `.gitkeep`, or
duplicate tree exists, so a retired path simply fails.

## Where the old working-tree paths went

Earlier releases published the current text as `csv-unicode/` and
`tei-xml-unicode/`. Those paths are not present here; this table maps
them to the curated editions. The retired paths return 404 by
design, with no redirects and no stubs.

| Retired path | Now |
| --- | --- |
| `csv-unicode/ccat/no-variants` | `editions/rp2018-2023/csv/accented/no-variants` |
| `csv-unicode/ccat/with-variants` | `editions/rp2018-2023/csv/accented/with-variants` |
| `csv-unicode/strongs/with-parsing` | `editions/rp2018-2023/csv/strongs/with-parsing` |
| `csv-unicode/strongs/no-parsing` | `editions/rp2018-2023/csv/strongs/no-parsing` |
| csv-unicode/strongs/no-parsing (second view) | `editions/rp2018-2023/csv/unaccented` |
| `tei-xml-unicode/no-accents` | `editions/rp2018-2023/tei/unaccented` |
| `tei-xml-unicode/no-accents/BYZ/byz.xml` | `editions/rp2018-2023/tei/unaccented/BYZ/byz.xml` |
| `tei-xml-unicode/assets/coll.png` | `docs/assets/coll.png` |
| `tei-xml-unicode/assets/demo_collation.xlsx` | `docs/assets/demo_collation.xlsx` |
| `tei-xml-unicode/assets/demo_john_1.xml` | `docs/assets/demo_john_1.xml` |
| tei-xml-unicode/README.md (CollateX walkthrough) | `docs/COLLATEX.md` |
| csv-unicode/README.md (multi-parsing note) | `docs/EDITIONS.md` and `data/raw/repo/CONVENTIONS.md` |

Those `csv-unicode/` and `tei-xml-unicode/` views were the previous
release's `rp2018-2023` files. Their bytes changed only at the corrected
apparatus literal, the 2026-11-21 move kept every `artifact_files` hash,
and the 2026-11-25 change replaced `source_files` with `inputs`.

## Where the code and inputs moved

Earlier releases ran `scripts/*.py` and kept the inputs under
`source/`. Those paths are not present here; this table maps them to
the current layout. There are no shims, symlinks, or redirect files:
an old path or command fails.

| Old path or command | Now |
| --- | --- |
| `python3 scripts/fetch_official.py [--verify or --force]` | `PYTHONPATH=src python3 -m byz.fetch [--verify or --force]` |
| `python3 scripts/recover_editions.py` | `PYTHONPATH=src python3 -m byz.materialise` |
| `python3 scripts/build_editions.py` | `PYTHONPATH=src python3 -m byz.build` |
| `python3 scripts/diff_editions.py` | `PYTHONPATH=src python3 -m byz.diff` |
| `scripts/requirements.txt` | `requirements.txt` (repository root) |
| `scripts/README.md` | `docs/BUILD.md` |
| `scripts/beta_to_unicode_custom/` | `src/byz/beta/` |
| `scripts/tei_xml_header.xml` | `src/byz/curate/tei_xml_header.xml` |
| `source/CCAT` | `data/raw/repo/rp2018-2023/ccat` |
| `source/Strongs` | `data/raw/repo/rp2018-2023/strongs` |
| `source/README.md` | `data/raw/repo/CONVENTIONS.md` |
| the hand-written README body and its editions block | `src/byz/curate/README.template.md` |

The 2026-11-21 move changed only the paths and the commands; every
`artifact_files` hash stayed the same. The 2026-11-25 change replaced
`source_files` with `inputs` and regenerated `rp2005-2019` from its
committed sources, so that edition's artifact hashes changed (the other
three did not). Three metadata keys also changed (`generated_by`,
`source_commit`, and `strongs_commit`), because they name the command
and the git pathspecs that produce them. The `data/text/` targets in
that table were themselves moved on 2026-11-25 into the repository
source class, as the next section records.

See [Apparatus literals](#apparatus-literals) for the historical
converter's damaged notes and how the regenerated edition avoids them.

## Blank verses and omitted rows

LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 are not part of the
Byzantine tradition. The official `.CCT` and ASCII archives contain
them as **blank verse lines**, so they are real data, not conversion
losses. `rp2005` and `rp2018` therefore emit explicit empty records:
7972 accented CSV rows (four empty), 7957 unaccented CSV rows (four
empty), and empty `<ab/>` elements in both TEI views.
`rp2018-2023` behaves the same way (7972 / 7957 rows plus empty
`<ab/>` elements).

`rp2005-2019` now behaves the same way as well. Its 2019 sources
contain the four blank verse lines, and regeneration by the current
pipeline emits explicit empty records: 7972 accented CSV rows, 7957
unaccented/Strong's CSV rows, and empty `<ab/>` elements in both TEI
views. The artifacts released as [`v2.0.3`](https://github.com/byztxt/byzantine-majority-text/releases/tag/v2.0.3) omitted the four rows; that
omission is not reproduced.

## TEI punctuation

Generated TEI wraps each whitespace-separated token in `<w>`. A
standalone `-` (the official text's dash and deletion marks) is
emitted as `<pc>-</pc>`, and a leading `¶` becomes
`<milestone unit="paragraph" type="start"/>` instead of being glued to
the following word. Punctuation attached to a word stays inside its
`<w>`. Only the accented TEI contains these two markers; the unaccented
TEI has neither, so its markup is unchanged.

## Apparatus literals

Generated editions preserve apparatus literals verbatim: the quoted
English notes in `[[ "..." ]]` (for example
`[[ "shorter ending" ]]` in MAR 16:8) and the exact `"+"`
quotation mark keep the source's case and spacing. `rp2005` and
`rp2018` show `[[ "shorter ending" ]]` from the official `.CCT`
archives, `rp2018-2023` shows `[["SHORTER ENDING"]]` because
`data/raw/repo/rp2018-2023/ccat` is upper-case with no spaces inside the brackets,
and `rp2005-2019` takes the literal from its 2019 source.

Before the fix the historical converter transliterated the notes
(`σηορτερ ενδινγ`) and rendered `"+"` as `" ̈"`. The artifacts
released as [`v2.0.3`](https://github.com/byztxt/byzantine-majority-text/releases/tag/v2.0.3) still carry that damage; this repository
regenerates `rp2005-2019` from the sources, so the published view
needs no post-correction.

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

In `rp2018-2023`, `csv/unaccented/` and `csv/strongs/no-parsing/` hold
the same bytes: they are two names for one text (the plain Unicode
text and the Strong's view with parsing dropped). The duplication is
intentional, and a test asserts the identity.

### Inherited title quirks

The unaccented TEI for `2TI` and `PHP` in `rp2018-2023` titles the
books `Second Timoty` and `Phillipians`. Both spellings are inherited,
not introduced here: `rp2018-2023` preserves the titles of the earlier
`tei-xml-unicode/` outputs. They are preserved deliberately so the
edition's TEI bytes stay unchanged. Every other title, and the whole
accented TEI, uses the corrected spellings.

`rp2005-2019` uses the corrected titles. It is regenerated from its
2019 sources, so it does not inherit the released artifacts'
misspellings. Do not copy the quirk into other editions without a new
release.

In the `csv/strongs/with-parsing/` view a word may be followed by two
sets of Strong's number and parsing code. These are alternative
parsings of the same word (for example, a neuter form that can be
either nominative or accusative), not two separate words; either
parsing is applicable. The convention is explained in
`data/raw/repo/CONVENTIONS.md`.

### Rebuilding the curated editions

The official `.CCT` archives also contain the `PA` (Pericope Adulterae)
and `ACT24` (Acts 24 appendix) sections, which are exported as separate
accented CSV files; the TEI exports are the 27-book main text.

To rebuild every curated edition from the committed `data/` inputs,
run these from the repository root (no network is needed):

```bash
PYTHONPATH=src python3 -m byz.fetch --verify
PYTHONPATH=src python3 -m byz.build
PYTHONPATH=src python3 -m byz.diff
PYTHONPATH=src python3 -m byz.verify
```

`byz.materialise` is an ingest command, not part of this rebuild: run
it only to restore `data/raw/repo/rp2005-2019/` from tag [`v2.0.3`](https://github.com/byztxt/byzantine-majority-text/releases/tag/v2.0.3) when that
tree is missing.

## Successive diffs

- `rp2005` -> `rp2005-2019` ([`reports/diffs/rp2005--rp2005-2019/`](../reports/diffs/rp2005--rp2005-2019/))
- `rp2005-2019` -> `rp2018` ([`reports/diffs/rp2005-2019--rp2018/`](../reports/diffs/rp2005-2019--rp2018/))
- `rp2018` -> `rp2018-2023` ([`reports/diffs/rp2018--rp2018-2023/`](../reports/diffs/rp2018--rp2018-2023/))
- `rp2005` -> `rp2018` ([`reports/diffs/rp2005--rp2018/`](../reports/diffs/rp2005--rp2018/))

Each directory contains:

- `report.md` - Unicode-first human-readable report.
  `Main-text changes` lists the verses whose normalised Unicode text
  changes, with the Text word diff (`[-removed-]{+added+}`, in the
  style of `git diff --word-diff`) first and the Beta-code Source
  second. `Apparatus-only changes` compacts the remaining
  source-tier differences into one entry per verse, showing the
  Unicode apparatus word diff first and the Beta-code diff second;
  an entry whose only change is Beta-code encoding says so instead of
  printing an empty diff. The Text diff is
  normalised: paragraph markers (`¶`), apostrophe typography,
  and whitespace are omitted.
- `changes.csv` - machine-readable rows with the category, the
  Beta-code source word diff, the Unicode Text and Apparatus word
  diffs, the full source/text left and right, and the
  `text_changed` and `apparatus_changed` flags. The word diffs are
  normalised; `text_left`/`text_right` are exact.
- `source.diff` - word-diff style, one line per verse, for the
  Beta-code source tier.
- `text.diff` - the same word-diff view for the exact derived
  Unicode accented main text (`csv/accented/no-variants`). It
  includes formatting-only changes such as a `¶` edit;
  paragraph markers and apostrophes are shown as stored.
- `apparatus.diff` - the word diff of the normalised Unicode
  accented text with variants (`csv/accented/with-variants`) for
  every apparatus-only change that has a Unicode difference
  (encoding-only rows are named in `report.md`). Variant readings
  stay inside `{...}` braces, and the braces are literal text
  inside the diff markers. `source.diff` is the Beta-code view of
  the same verses.
- `derived.diff` - the word diff of the normalised Unicode main
  text for every differing verse.

The source-tier comparison canonicalises dash spacing (`-` ↔ ` - `), so raw
dash-spacing differences are invisible there but survive in the derived
text. All current derived-only cases are attached-vs-spaced dashes.

Category names, with worked examples (including the `variant` vs
`apparatus-code` distinction), are defined in
[`reports/diffs/README.md`](../reports/diffs/README.md#categories).

The `.diff` files are word-diff style, with one
`@@ BOOK CHAPTER:VERSE [category] @@` hunk and one marked line per
verse, not patchable line-based diffs: they have no line ranges and
no `-`/`+` whole-verse lines.

**Source** is the edition's Beta-code source tier: the official
`.CCT` archive for `rp2005`/`rp2018`, the 2019
`textonly-beta-code` sources at `data/raw/repo/rp2005-2019/` for
`rp2005-2019`, and `data/raw/repo/rp2018-2023/ccat` for `rp2018-2023`.
**Text** is the derived Unicode accented main text.
**Apparatus** is the Unicode accented text with variants, from
`editions/<id>/csv/accented/with-variants/`.

`[-removed-]{+added+}` wraps changed words; unchanged text is
context. Beta-code apparatus braces (`{N ... }`) remain part of the
source text. In the Unicode apparatus the same reading sits inside
literal `{...}` braces, so an added variant renders as
`{+{Byz τε > δε }+}`: the outer markers are the diff and the inner
braces are the reading.

The marker delimiters are the fixed strings `[-`, `-]`, `{+`, `+}`;
a literal `-` or `>` next to a delimiter is part of the text (for
example, a dash-spacing change can render as
`[-εἶπεν --]{+εἶπεν-+}`).

`@@ BOOK CHAPTER:VERSE [category] @@` opens a verse
hunk.
Text comparison removes paragraph markers (`¶`), maps curly
apostrophes (`’`/`‘`) to `'`, and collapses whitespace; the
word-diff shown omits those conventions. The exact text is in
`changes.csv` (`text_left`/`text_right`) and `text.diff`.
`reports/diffs/README.md` is generated by the same script.

## Source of truth

If a PDF, an archive, and the curated source disagree, the PDF wins and
the conflict is recorded for the maintainer instead of being resolved
automatically.
