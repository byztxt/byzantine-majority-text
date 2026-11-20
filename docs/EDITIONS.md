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
`source/` are the authoritative machine-readable text for the
derivatives.

For where everything lives in the repository, see the layout table in
the [root README](../README.md#repository-layout).

## The four editions

| Edition | Status | Basis | Repo releases | PDF (committed) |
| --- | --- | --- | --- | --- |
| `rp2005` | official | Published in print by Chilton Book Publishing, Southborough, Massachusetts | none | [`rp2005 PDF`](../data/raw/rp2005/official-pdf/editions-rp2.pdf) (`ccf5bb5467408fdd44a362764dc93383ddb5d5579c6601fac0ec0b83a095ecce`) |
| `rp2005-2019` | released | Recovered from git tag v2.0.3 (textonly-beta-code + parsed) | `v1.0.0`-`v2.0.3` | none |
| `rp2018` | official | Published in print by VTR, Nuremberg | none | [`rp2018 PDF`](../data/raw/rp2018/official-pdf/robinson-pierpont-2018-gnt-edition.pdf) (`00303ddc443816d363ccca8c3882ce83f4ecb858fa52d0313b80f445d263852c`) |
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
- `rp2018-2023`: every view is generated from the edition's own
  `source/` snapshot.

`rp2018-2023` also has a frozen `source/` snapshot, which intentionally
duplicates the repository `source/` so the edition can be downloaded and
verified on its own.

See [`COLLATEX.md`](COLLATEX.md) for using the unaccented TEI with
CollateX.

## Where the old working-tree paths went

`csv-unicode/` and `tei-xml-unicode/` were removed on 2026-11-19. The
current text is `editions/rp2018-2023/`; the retired paths return 404 by
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
| csv-unicode/README.md (multi-parsing note) | `docs/EDITIONS.md` and `source/README.md` |

The bytes did not change: the files moved, and the edition's
`manifest.json` records the same hashes as before the change. See
[`RELEASE-NOTES.md`](RELEASE-NOTES.md) for the breaking-change note.

## Blank verses and omitted rows

LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 are not part of the
Byzantine tradition. The official `.CCT` and ASCII archives contain
them as **blank verse lines**, so they are real data, not conversion
losses. `rp2005` and `rp2018` therefore emit explicit empty records:
7972 accented CSV rows (four empty), 7957 unaccented CSV rows (four
empty), and empty `<ab/>` elements in both TEI views.
`rp2018-2023` behaves the same way (7972 / 7957 rows plus empty
`<ab/>` elements).

The recovered `rp2005-2019` edition is the exception. Its
`textonly-beta-code`, `parsed`, accented no-variants CSV, unaccented
CSV, and unaccented TEI are recovered byte-identically from `v2.0.3`.
The accented with-variants derivative differs from `v2.0.3` only at
MAR 16:8, where the apparatus literal is corrected. The accented TEI
(from the recovered accented CSV) and the Strong's
views (from `parsed`) are generated here, and `v2.0.3` itself has no
accented TEI. The accented CSV (7968 rows), unaccented CSV (7953
rows), and unaccented TEI **omit** the four verses: the rows are
absent and there is no empty `<ab/>`, even though the source files in
that tag do contain the blank verse lines. The generated accented TEI
inherits the omission; the generated Strong's views include the four
verses as empty rows (7957 rows). The recovered rows are deliberately
not added back; the edition README records the omission.

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
`rp2018` therefore show `[[ "shorter ending" ]]` from the official
`.CCT` archives, while `rp2018-2023` shows `[["SHORTER ENDING"]]`
because `source/CCAT` is upper-case with no spaces inside the
brackets. Before this fix the historical converter transliterated the
notes (`σηορτερ ενδινγ`) and rendered `"+"` as `" ̈"`.

All curated editions now preserve the literals. The recovered
`rp2005-2019` with-variants view is the `v2.0.3` artifact with exactly
one corrected row: MAR 16:8, where `[[ "σηορτερ ενδινγ" ]]` and
`" ̈"` are restored to `[[ "shorter ending" ]]` and `"+"`. The
recovered source files and the other historical views remain
byte-identical to `v2.0.3`.

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

The unaccented TEI for `2TI` and `PHP` in `rp2018-2023` and
`rp2005-2019` titles the books `Second Timoty` and `Phillipians`.
Both spellings are inherited, not introduced here: `rp2018-2023`
copies the retired `tei-xml-unicode/` convenience tree, and
`rp2005-2019` recovers the same titles from the `v2.0.3` artifacts
that tree held. They are preserved deliberately so the editions'
TEI bytes stay unchanged. Every other title, and the whole
accented TEI (in both editions), uses the corrected spellings.
Do not "fix" them without a new edition release.

In the `csv/strongs/with-parsing/` view a word may be followed by two
sets of Strong's number and parsing code. These are alternative
parsings of the same word (for example, a neuter form that can be
either nominative or accusative), not two separate words; either
parsing is applicable. The convention is explained in
`source/README.md`.

### Rebuilding the curated editions

The official `.CCT` archives also contain the `PA` (Pericope Adulterae)
and `ACT24` (Acts 24 appendix) sections, which are exported as separate
accented CSV files; the TEI exports are the 27-book main text.

To rebuild every curated edition from the committed archives,
`source/`, and git tag `v2.0.3`, run these from the repository root
(no network is needed):

```bash
python3 scripts/fetch_official.py --verify
python3 scripts/recover_editions.py
python3 scripts/build_editions.py
python3 scripts/diff_editions.py
```

## Successive diffs

- `rp2005` -> `rp2005-2019` (`reports/diffs/rp2005--rp2005-2019/`)
- `rp2005-2019` -> `rp2018` (`reports/diffs/rp2005-2019--rp2018/`)
- `rp2018` -> `rp2018-2023` (`reports/diffs/rp2018--rp2018-2023/`)
- `rp2005` -> `rp2018` (`reports/diffs/rp2005--rp2018/`)

Each directory contains:

- `report.md` - Unicode-first human-readable report.
  `Main-text changes` lists the verses whose normalised Unicode text
  changes, with the Text word diff (`[-removed-]{+added+}`, in the
  style of `git diff --word-diff`) first and the Beta-code Source
  second. `Apparatus-only changes` compacts the remaining
  source-tier differences into one line per verse. The Text diff is
  normalised: paragraph markers (`¶`), apostrophe typography,
  and whitespace are omitted.
- `changes.csv` - machine-readable rows with the category, both word
  diffs, the full source/text left and right, and a `text_changed`
  flag. `text_word_diff` is normalised; `text_left`/`text_right` are
  exact.
- `source.diff` - word-diff style, one line per verse, for the
  Beta-code source tier.
- `text.diff` - the same word-diff view for the exact derived
  Unicode accented main text (`csv/accented/no-variants`). It
  includes formatting-only changes such as a `¶` edit;
  paragraph markers and apostrophes are shown as stored.
- `derived.diff` - the word diff of the normalised Unicode main
  text for every differing verse.

The source-tier comparison canonicalises dash spacing (`-` ↔ ` - `), so raw
dash-spacing differences are invisible there but survive in the derived
text. All current derived-only cases are attached-vs-spaced dashes.

The `.diff` files are word-diff style, with one
`@@ BOOK CHAPTER:VERSE [category] @@` hunk and one marked line per
verse, not patchable line-based diffs: they have no line ranges and
no `-`/`+` whole-verse lines.

**Source** is the edition's Beta-code source tier: the official
`.CCT` archive for `rp2005`/`rp2018`, the recovered
`textonly-beta-code` for `rp2005-2019`, and `source/CCAT` for
`rp2018-2023`. **Text** is the derived Unicode accented main text.

`[-removed-]{+added+}` wraps changed words; unchanged text is
context. Beta-code apparatus braces (`{N ... }`) remain part of the
source text.

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
