# Requirements - Documentation clarity, linkable references, and a Unicode apparatus diff

## Context

The corpus is now stable: four curated editions under `editions/`, generated CSV
and TEI for the current text, successive-edition diffs under `reports/diffs/`,
a baseline contract under `reports/baseline/`, and an archive reconciliation
under `reports/reconciliation/`. The generated Markdown that describes all of
this has accumulated jargon, stale sentences, and plain-text references that a
reader cannot follow:

- `docs/EDITIONS.md` cites commit hashes, release tags, and diff directories as
  plain code spans. A reader on GitHub cannot click any of them.
- `scripts/README.md` explains the report-generation order in the vocabulary of
  the implementation ("owns the baseline document", "leaves exactly one block
  and one heading"). A first-time user does not learn why the order matters or
  what a wrong order looks like.
- `SPECS/MISSION.md` has a typo in a success criterion.
- The relationship between `csv-unicode/`, `tei-xml-unicode/`, and `editions/`
  is undocumented at the point of use. The overlapping views are byte-identical
  duplicates, but nothing says so, so readers cannot tell whether the
  duplication is deliberate.
- `docs/DATA_CONTRACT.md` opens with "This document describes the corpus as it
  exists today" and then presents four tables of undefined terms. One of its
  sentences ("No external archive is involved in this contract; that is the next
  cycle") is stale: Cycle 2 is complete. `reports/baseline/invariants.csv` is a
  **0-byte file**, which looks like a broken run even though it means "no
  violations".
- `reports/diffs/<pair>/report.md` renders apparatus-only changes in Beta code
  only. Most readers cannot read Beta code, and an accented Unicode view of the
  apparatus exists in every edition.
- `source/Strongs/*.BP5` is labelled `provenance-unknown` throughout the
  generated reports, although these are Dr Robinson's official parsed files. The
  only real gap is that the six published ZIP archives contain no parsed file,
  so the *delivery route* is not recorded.

This change fixes the seven items below. It changes documentation, report
generation, one CSV schema (adding columns and a header), and the diff
generators. It does not change any text, source file, edition CSV/TEI byte, PDF,
archive, or checksum.

## Scope

- **Editions:** all four curated editions are affected only through
  `docs/EDITIONS.md` and through the diff reports that compare them. Their
  `source/`, `csv/`, `tei/`, `manifest.json`, and `README.md` are byte-identical
  afterwards (the edition READMEs are regenerated but their text does not
  change, because this change edits `docs.py`, not `build.py`'s `_readme`).
- **Inputs touched:** none. No source file, archive, or PDF is read differently;
  the new apparatus diff reads `editions/<id>/csv/accented/with-variants/`, which
  already exists for all four editions.
- **Outputs touched:** `docs/EDITIONS.md`, `docs/DATA_CONTRACT.md`,
  `docs/PROVENANCE.md`, `reports/baseline/invariants.csv`,
  `reports/baseline/{summary,decision-log}.md`, `reports/baseline/files.csv`,
  `reports/diffs/README.md`, `reports/diffs/<pair>/{report.md,changes.csv,
  apparatus.diff}`, `reports/reconciliation/{summary,decision-log}.md`.
  Hand-written files edited directly: `SPECS/MISSION.md`, `scripts/README.md`,
  the root `README.md` (outside the generated block), `csv-unicode/README.md`,
  `tei-xml-unicode/README.md`, `SPECS/TECH.md` §2.
- **Not touched:** any file under `data/raw/`, `source/`, `editions/*/source/`,
  `editions/*/csv/`, `editions/*/tei/`, `editions/*/manifest.json`,
  `csv-unicode/**/*.csv`, `tei-xml-unicode/**/*.xml`.

## Verified inventory (2026-11-19, branch `feature/2026-11-16-edition-recovery-curation`)

Every claim below was checked against the working tree before this spec was
written.

| Fact | Check |
| --- | --- |
| `csv-unicode/ccat/no-variants` == `editions/rp2018-2023/csv/accented/no-variants` | `diff -rq`, 29 files, no differences |
| `csv-unicode/ccat/with-variants` == `editions/rp2018-2023/csv/accented/with-variants` | `diff -rq`: identical except the untracked `variant_analysis.py` (30 entries on the left, 29 `.csv` on the right) |
| `csv-unicode/strongs/with-parsing` == `editions/rp2018-2023/csv/strongs/with-parsing` | `diff -rq`, 27 files, no differences |
| `csv-unicode/strongs/no-parsing` == `editions/rp2018-2023/csv/strongs/no-parsing` | `diff -rq`, 27 files, no differences |
| `tei-xml-unicode/no-accents` == `editions/rp2018-2023/tei/unaccented` | `diff -rq`, 28 files (27 books + `BYZ/byz.xml`), no differences |
| `editions/rp2018-2023/csv/unaccented` == `csv-unicode/strongs/no-parsing` | `diff -rq`, 27 files, no differences; also identical to `editions/rp2018-2023/csv/strongs/no-parsing` (see R4.4) |
| `editions/rp2018-2023/tei/accented` has no working-tree counterpart | `csv-unicode/` has only `ccat/` and `strongs/`; `tei-xml-unicode/` has only `no-accents/`, `BYZ/`, `assets/` |
| All four editions have `csv/accented/with-variants/` | `editions/{rp2005,rp2005-2019,rp2018,rp2018-2023}/csv/accented/with-variants/` |
| `docs/EDITIONS.md` line numbers | tags at 26, 28, 39-41, 54, 58, 69-70, 76, 92, 141-145, 177, 181, 208, 228; commit at 76; diff directories at 240-243 |
| `reports/baseline/invariants.csv` | `wc -c` = 0; `reports/baseline/*.csv` inventory in `files.csv` does **not** include it (see R5.10 and "Corrections" 1) |
| `changes.csv` schema test | `tests/curate/test_integration.py:157-182`, not `tests/curate/test_diff.py` (see R6.3) |
| Apparatus-only rows per pair | 8 (`rp2005`→`rp2005-2019`), 0 (`rp2005-2019`→`rp2018`), 156 (`rp2018`→`rp2018-2023`), 8 (`rp2005`→`rp2018`) |
| Apparatus-only rows with **no** Unicode difference | 37 total: 36 in `rp2018`→`rp2018-2023` (21 `accents-breathings`, 15 `variant`) and 1 in `rp2005`→`rp2018` (`2PE 1:12`) (see R6.2) |
| Canonical GitHub remote | `upstream` = `https://github.com/byztxt/byzantine-majority-text.git`; `origin` is a personal fork. The base URL used by R1 is the upstream URL, which also matches the root README badge |

### Corrections to the brief

1. **`invariants.csv` has no hash row in `files.csv`.** `files.csv` inventories
   `source/`, `csv-unicode/`, `tei-xml-unicode/`, `essay/`, `scripts/`, and the
   seven hand-written documents listed in `src/byz/contract/inventory.py:61-69`
   (`DOC_FILES`). Nothing under `reports/` is inventoried. Adding the header
   therefore changes `invariants.csv` but not any `files.csv` row. `files.csv`
   *does* change in this change, but because the hand-written documents it
   hashes changed (`README.md`, `scripts/README.md`).
   *Superseded (2026-11-20):* the retirement change removed `csv-unicode/` and
   `tei-xml-unicode/`, including the two folder READMEs this spec originally
   listed; the inventory names neither, `DOC_FILES` now lists five documents, and
   this change updates only the two `scripts/README.md` rows (`scripts` and
   `docs`).
2. **`editions/rp2018-2023/csv/unaccented` is not a curated-only view.** It is
   byte-identical to `csv-unicode/strongs/no-parsing`, because
   `src/byz/curate/recover.py:271-274` copies that directory into both
   `csv/strongs/no-parsing` and `csv/unaccented`. The documentation must state
   this rather than imply the view has no working-tree source.
3. **37 of the 172 apparatus-only changes have no Unicode apparatus difference.**
   They are Beta-code encoding-order differences in the main text (for example
   `*(/A|DOU` vs `*(/AD|OU` at MAT 11:23, or `_DAD` vs `_*D*A*D` at REV 3:7) that
   convert to the same Unicode. R6 therefore has to render them explicitly; a
   blank Unicode line would look like a bug.
4. **The CSV schema is pinned in `tests/curate/test_integration.py:157-182`.**
   `tests/curate/test_diff.py` only tests `word_diff` and `normalize_text`.
5. **`docs/PROVENANCE.md` and `reports/reconciliation/` also cite
   `97371d7`, `v2.0.3`, and `v3.0.0` as plain text.** R1 is scoped to
   `docs/EDITIONS.md`; the other documents are a follow-up (see non-goals).

## Functional requirements

### R1 - `docs/EDITIONS.md`: link paths, commits, and tags

Generated by `src/byz/curate/docs.py` `write_editions_doc`.

1. A single module-level constant defines the base repository URL:
   `REPO_URL = "https://github.com/byztxt/byzantine-majority-text"` in
   `src/byz/curate/docs.py`. No other literal copy of that URL exists in Python
   code, and no test hard-codes it twice.
2. Four helpers render the links, so every site has the same shape:
   - `_tag(tag)` -> `` [`v2.0.3`](https://github.com/byztxt/byzantine-majority-text/releases/tag/v2.0.3) ``
   - `_commit(sha)` -> `` [`97371d7`](https://github.com/byztxt/byzantine-majority-text/commit/97371d7) ``
   - `_diff_dir(left, right)` ->
     `` [`reports/diffs/rp2005--rp2005-2019/`](../reports/diffs/rp2005--rp2005-2019/) ``
     (a relative link: `docs/EDITIONS.md` is one level below the repository root,
     so the target must start with `../` for GitHub to resolve it);
   - `_tag_range(first, last)` -> `_tag(first)` + `-` + `_tag(last)`.
3. Tag ranges link **both endpoints** and leave the hyphen as plain text:
   `` [`v1.0.0`](.../releases/tag/v1.0.0)-[`v2.0.3`](.../releases/tag/v2.0.3) ``.
   Justification: a range has no single canonical URL, and linking the whole
   label to the newest tag would send a reader who clicked "v1.0.0-v2.0.3" to
   `v3.3.4`, which is false. Linking each endpoint keeps the range readable and
   both targets reachable.
4. Every place the document names a release tag becomes a link: the
   "Repo releases" column (lines 26, 28), the `(v2.0.3)` qualifiers in the source
   feature matrix (`textonly-beta-code`, `parsed`, `textonly-online-bible`), and
   the prose mentions at lines 54, 58, 69-70, 92, 109-111, 113, 145, 149, 172.
   The only exception is `docs/EDITIONS.md`'s fenced `bash` block, which contains
   no tags.
5. The commit hash at line 76 becomes a link via `_commit("97371d7")`.
6. The four diff bullets at lines 184-187 become
   `- `rp2005` -> `rp2005-2019` (<link>)`, preserving the existing text and
   parentheses shape so the change is easy to review.
7. `none` for the two official editions stays plain text.
8. Rendered links must survive GitHub from `docs/`: the relative diff links are
   validated on disk by the existing
   `tests/curate/test_editions.py::PdfLinkTests.test_relative_markdown_links_resolve`,
   and new tests assert the exact `https://github.com/byztxt/...` strings.

### R2 - `scripts/README.md`: rewrite "Report generation order" for humans

Hand-written; edit directly. Keep the section heading.

1. The rewrite explains, in plain order:
   - both commands write the same file, `docs/HISTORY.md`;
   - `byz.contract` regenerates the whole document from git but first saves and
     re-appends the "External archive evidence (Cycle 2)" section, if present,
     which it finds by the `<!-- cycle2:begin -->` / `<!-- cycle2:end -->`
     markers;
   - `byz.reconcile` rebuilds that section from the committed archives;
   - therefore run contract first and reconciliation second, so the archive
     numbers are the last thing written and match `data/raw/_archives/`;
   - both commands are safe to re-run; a second run of either produces no diff.
2. It states what a wrong order looks like, which the current text omits:
   - contract only -> the archive section keeps its previous numbers, or
     disappears entirely if its markers were removed by hand;
   - reconciliation only -> the rest of `docs/HISTORY.md` is stale relative to
     git;
   - a hand-edited or deleted marker -> the next contract run silently drops the
     section; a reconciliation run restores it.
3. It keeps the factual content that is already there (the two commands, the
   `data/raw/_archives/` dependency, exactly one block and one heading, "a second
   run produces no diff") and drops the implementation vocabulary. No new
   commands, no new files.

### R3 - Typo in `SPECS/MISSION.md`

Line 73: `and *why category* of change it is.` becomes
`and *what category* of change it is.` Nothing else in the file changes.

### R4 - Document the working-tree paths vs the curated editions

> **Superseded by `SPECS/2026-11-19-retire-legacy-unicode-trees/`.** That change
> deletes `csv-unicode/` and `tei-xml-unicode/` and retires
> `scripts/csv_converter.py` and `scripts/tei_xml_converter.py`, so there is no
> working-tree copy left to describe. Do not implement R4. Its factual content
> (byte identity, the `csv/unaccented` duplicate) moves into the old-to-new path
> table in `docs/EDITIONS.md`. R5 must still be written against the
> post-removal layout.

The overlapping views are byte-identical duplicates, and the documentation must
say so where readers meet them.

1. **Generated section in `docs/EDITIONS.md`.** Add a new section
   `## Working-tree paths and the curated editions`, emitted by
   `write_editions_doc` and placed after the "four editions" table (before
   `## Source feature matrix`). It contains:
   - one paragraph: `csv-unicode/` and `tei-xml-unicode/` are the original
     convenience paths, produced by `scripts/csv_converter.py` and
     `scripts/tei_xml_converter.py` from `source/`, and they describe the
     **current text only** (`rp2018-2023`); `editions/` holds all four editions,
     each with `manifest.json` and per-file SHA-256 hashes;
   - a table `| Working-tree path | Curated equivalent |` with five rows:
     `csv-unicode/ccat/no-variants` -> `editions/rp2018-2023/csv/accented/no-variants`;
     `csv-unicode/ccat/with-variants` -> `editions/rp2018-2023/csv/accented/with-variants`;
     `csv-unicode/strongs/with-parsing` -> `editions/rp2018-2023/csv/strongs/with-parsing`;
     `csv-unicode/strongs/no-parsing` -> `editions/rp2018-2023/csv/strongs/no-parsing`;
     `tei-xml-unicode/no-accents` -> `editions/rp2018-2023/tei/unaccented`;
   - a sentence: the overlapping files are **byte-identical**: the curated copy
     is made by copying the working-tree output, not by converting the source a
     second time, and a test asserts the bytes so the two paths cannot silently
     diverge;
   - a sentence for R4.4 (the `csv/unaccented` duplication) and one for
     `tei/accented` having no working-tree counterpart;
   - a closing sentence: `source/` remains the source of truth for both trees;
     an edit belongs in `source/`, after which both are regenerated.
2. **Single source of truth for the table.** The five pairs are a module-level
   constant in `src/byz/curate/docs.py`, for example
   `WORKING_TREE_VIEWS = ((left, right), ...)`. The generated table is rendered
   from it and the byte-identity test imports it, so the table and the test
   cannot disagree. The duplication in R4.4 gets its own one-entry constant
   `CURATED_DUPLICATE_VIEWS = (("editions/rp2018-2023/csv/strongs/no-parsing",
   "editions/rp2018-2023/csv/unaccented"),)`, tested the same way, so that prose
   claim is locked too.
3. **Folder READMEs (hand-written).** `csv-unicode/README.md` and
   `tei-xml-unicode/README.md` each gain a short subsection
   `## Working-tree paths and the curated editions` (replacing the current
   one-line blockquote) with: what this folder is, that it covers the current
   text only, the path to the curated equivalent, that the overlapping files are
   byte-identical, and that `source/` is the source of truth. Keep both files
   banner-free.
4. **`csv/unaccented` accuracy.** State that
   `editions/rp2018-2023/csv/unaccented` holds the same bytes as
   `editions/rp2018-2023/csv/strongs/no-parsing`, because
   `recover_editions.py` copies `csv-unicode/strongs/no-parsing` into both views;
   the two names describe two views of one text. Do not describe it as a view
   with no working-tree source.
5. **Root `README.md` (hand-written, outside the generated block).** After the
   "Repository layout" table, add a short paragraph: the two path families hold
   the same bytes for the current text; `editions/` is the complete, manifest-
   backed view of all four editions; `source/` is the source of truth. Do not
   add prose inside the `<!-- editions:begin -->` / `<!-- editions:end -->` block;
   the generated block must stay byte-identical.
6. **The stray file.** `csv-unicode/ccat/with-variants/variant_analysis.py` is
   untracked and is not part of the pipeline. It is not documented as a member of
   any view, and the byte-identity test compares `*.csv` names only. It is moved
   aside before regeneration (see `validation.md` §1) because
   `recover_editions.py` copies whole directories.

### R5 - `docs/DATA_CONTRACT.md`: readable without prior context, and `invariants.csv`

Generated by `src/byz/contract/report.py` `_contract_doc` (lines 52-159).

1. **Opening.** Replace the current three paragraphs with: what the repository
   ships (four editions of the Robinson-Pierpont Byzantine textform; Beta-code
   sources; generated Unicode CSV and TEI); what this document is for (the shape
   of the corpus: datasets, records, invariants, derivations); that it is
   generated by `PYTHONPATH=src python3 -m byz.contract` from
   `src/byz/contract/contracts.py` and the baseline run, so it always describes
   the tree it was generated from; that the machine-readable copy is
   `docs/contract/` (one JSON per dataset plus `contracts.json`); and that it
   covers the working-tree corpus, while `editions/`, the archive comparison, and
   the edition history are in `docs/EDITIONS.md`, `docs/PROVENANCE.md`, and
   `docs/HISTORY.md`.
2. **`## How to read this document`.** A bullet per section, in document order,
   saying what question the section answers and how to read its table.
3. **`## Terms`.** Short definitions of: dataset, file, record, key, invariant,
   violation, known exception, contract, derivation, evidence, auxiliary,
   intentional blank verse, section file (`04a_PA`, `05a_ACT24`).
4. **`## Coverage`** keeps its heading and gains a `What it holds` column,
   rendered from `contracts.DATASET_CONTRACTS[dataset]["purpose"]` so the
   description is not a second copy of the contracts. Header becomes
   `| Dataset | What it holds | Files | Books | Records |`. This doubles as the
   dataset-name glossary the brief asks for.
5. **`## Derivation map`** gains two sentences before the table: a derivation is
   one source file (or the grouped `*.csv` set) producing one derived file; the
   `Evidence` column names the converter and the exact variable or function that
   writes it; `(+N more)` groups rows that share one evidence string; `Status`
   counts `ok`, `missing`, and `auxiliary` files.
6. **`## Known exceptions`, `## Intentional blank verses`, and
   `## Dataset contracts`** each gain one or two sentences on how to read them,
   in particular that an empty "Known exceptions" table means none, and that each
   dataset subsection lists the regexes/shapes a file must satisfy followed by
   the invariant list the validator enforces.
7. **Stale sentence.** Replace "No external archive is involved in this
   contract; that is the next cycle." with a statement of the current state: the
   working-tree contract does not depend on the external archives; the archive
   comparison is Cycle 2, and its results are in `docs/PROVENANCE.md`,
   `reports/reconciliation/`, and the "External archive evidence" section of
   `docs/HISTORY.md`.
8. **New `## Baseline report files`.** A table of the five CSVs and two Markdown
   files in `reports/baseline/`, one row each, naming what one row per file
   means and the columns. The column lists must match the generated headers
   exactly: `files.csv` (`dataset,path,size,sha256,lines,encoding,eol,
   format_class,git_blob,last_commit`), `books.csv` (`dataset,book,file,
   chapters,verses,min_chapter,max_chapter,min_verse,max_verse,blank`),
   `differences.csv` (`comparison,left,right,book,left_verses,right_verses,
   only_left,only_right,examples_only_left,examples_only_right`),
   `derivations.csv` (`source,derived,evidence,status`), and `invariants.csv`
   (seven columns, R5.9).
9. **New `## Invariant results (reports/baseline/invariants.csv)`.** Explain that
   the baseline run writes one row per finding; a header with no data rows is the
   clean result ("no validator found a violation"); an empty or missing file
   would mean the generator did not run. Then a column table for the seven
   columns. Also state that the file always carries its header.
10. **`invariants.csv` gets a header row even when there are no violations.**
    `write_csv` in `src/byz/contract/report.py:17-29` currently writes `""` for
    an empty row list. It gains an optional declared field list
    (`write_csv(path, rows, fields=None)`), and only the `invariants.csv` call
    site passes it. The header is
    `dataset,path,line,category,message,key,known_exception`: exactly
    `Violation.as_row()`'s keys (`src/byz/contract/model.py:44-53`), declared
    once as `VIOLATION_FIELDS` next to `Violation` so the header and the rows
    cannot drift. `status` and `detail` from the brief are deliberately not added:
    every row *is* a violation (the status is implied by the file and mirrored in
    `summary.md`), and `message` is the detail.
11. **`reports/baseline/summary.md`** gains one sentence after the
    "Invariant findings" line: `invariants.csv` has a header and no data rows
    when there are no findings, which is the clean result. Its existing
    "Invariant findings: 0 (0 unresolved, 0 known exception)" line stays.

### R6 - Unicode apparatus diffs in the successive-edition reports

Generated by `src/byz/curate/diff.py`. This is a separate phase of work because
it touches the diff engine and the `changes.csv` schema.

1. **Variants-aware loader.** `load_text(edition_id)` (lines 105-116) hardcodes
   `csv/accented/no-variants`. It becomes
   `load_text(edition_id, view="no-variants")`, with the directory built as
   `csv/accented/<view>`. The apparatus view is
   `load_text(edition_id, "with-variants")`. All four editions have that
   directory.
2. **Apparatus word diff.** `_add_text` (lines 212-232) additionally computes,
   per source-tier row:
   - `apparatus_word_diff` = `word_diff(normalize_text(with_variants_left),
     normalize_text(with_variants_right))`;
   - `apparatus_changed` = `"true"` when those normalised strings differ, else
     `"false"`.
   `normalize_text` (lines 119-129) is reused unchanged: the same paragraph-
   marker/apostrophe/whitespace conventions apply to both views.
3. **`changes.csv` gains two columns**, appended at the end so every existing
   column keeps its position and readers that select by name are unaffected:
   `...,text_changed,apparatus_word_diff,apparatus_changed`. The schema is pinned
   by `tests/curate/test_integration.py:157-182`; that list is updated in the
   same commit. `apparatus_left`/`apparatus_right` are **not** added: the
   with-variants text is already stored in `editions/.../with-variants/` and
   `apparatus.diff` shows the marked line, so duplicating the whole verse in the
   CSV would double its size for no new information.
4. **New per-view artefact `apparatus.diff`**, written by `diff_pair` next to
   `source.diff`, `text.diff`, and `derived.diff`:
   - one hunk per row with `apparatus_changed == "true"`, using the existing
     `_verse_diff` writer, title
     `# Word diff: <left> -> <right> (Unicode accented text with apparatus)`;
   - preamble lines stating that this is the Unicode accented text from
     `csv/accented/with-variants`, that variant readings stay inside `{...}`
     braces, that the braces are literal text inside the markers, and that
     `source.diff` is the Beta-code view of the same verses.
   Rows with `apparatus_changed == "false"` are omitted from the file, because a
   hunk with no marker would be noise; the report names them (R6.6).
5. **`report.md`, "Apparatus-only changes" section.** Rewrite the rendering
   (lines 394-415). Each entry keeps the existing first line so the section stays
   a compact list and the existing assertions keep working:

   ```
   - `ROM 1:27` · `variant`
     - Apparatus (Unicode): `...{+{Byz τε > δε }+}...`
     - Apparatus (Beta code): `...O(MOI/WS TE {+{B TE > DE }+} KAI\...`
   ```

   Rules:
   - the Unicode line comes first (the report is Unicode-first elsewhere);
   - the Beta-code line is kept for scholars, indented as a sub-item;
   - when `apparatus_changed == "false"` the Unicode sub-item reads
     ``Apparatus (Unicode): no difference after conversion to Unicode
     (Beta-code encoding only)`` and no code span is emitted;
   - the existing formatting-only suffix
     (`` — formatting-only (normalised text identical; see `text.diff`) ``) stays
     after the category when `text_left != text_right`;
   - nothing else in the section changes; the "None: every source-tier
     difference also changes the normalised main text." case stays.
6. **Counters and self-description in `report.md`.**
   - After the existing "Apparatus-only changes (source differs, main text
     identical)" line, add two lines:
     `- **Apparatus-only changes shown in Unicode:** {n}` and
     `- **Apparatus-only changes with no Unicode difference (Beta-code encoding
     only):** {m}`, where `n + m` equals the existing total.
   - In `## Notation`, add a bullet defining **Apparatus** as the Unicode
     accented text with variants from `editions/<id>/csv/accented/with-variants/`,
     and a paragraph (new subsection `### Why the main text can be unchanged
     while the apparatus changes`) explaining that variant readings live inside
     `{...}` braces, the main text drops the braces, and an added variant
     therefore renders as `{+{Byz τε > δε }+}` (outer markers = the diff, inner
     braces = the reading).
   - The module docstring ("three word-diff views") is updated to four.
7. **`reports/diffs/README.md`** (`README_TEXT`, lines 445-529):
   - the `report.md` bullet describes the new apparatus rendering;
   - the file list gains `apparatus.diff` (R6.4 wording);
   - `## Notation` gains the **Apparatus** bullet and the doubled-brace example;
   - the `changes.csv` bullet names the two new columns.
8. **`docs/EDITIONS.md`** (generated, `src/byz/curate/docs.py:262-283`): the
   "Each directory contains" bullet for `report.md` says the apparatus section
   now shows the Unicode apparatus word diff first and the Beta-code diff second;
   the list gains an `apparatus.diff` bullet with the same facts as R6.7.
9. **Beta code is not removed.** `source.diff`, `source_word_diff`,
   `source_left`/`source_right`, and the report's Source lines are unchanged in
   content and order; the Unicode apparatus view is additive.

### R7 - `source/Strongs/*.BP5` is official Robinson material, not unknown

`source/README.md` states that the `CCAT` and `Strongs` folders are the files
created and maintained by Dr. Maurice A. Robinson, and that the `Strongs` folder
holds Strong's numbers and parsing codes. The only gap is that the six published
ZIP archives contain no parsed/Strong's file, so the file-level delivery route is
not recorded.

1. `src/byz/reconcile/compare.py`:
   - `strongs_provenance()` (lines 322-334): the status is no longer
     `"provenance-unknown"`/`"found"`. It returns
     `status = "official-source-files"` (the files are Dr Robinson's official
     parsed files) plus `delivery = "recorded" if hits else "not-recorded"` (no
     parsed archive among the six ZIPs today). The `hits` scan of the archives is
     kept: if a future archive ever contains a parsed file, `hits` lists it and
     `delivery` follows it.
   - `mapping_rows()` (lines 339-353): the 27 `source/Strongs/*.BP5` rows use
     `"class": "official-source"` and the note
     `"Dr Robinson's parsed/Strong's files; not in the six ZIPs"`. The rows stay
     one per file so the mapping coverage table still counts them.
2. `src/byz/reconcile/report.py`:
   - `_provenance_doc` (lines 185-200), section
     `## Strong's / BP5 provenance`: status line
     ``Status: `official-source-files` (delivery route: `not-recorded`).`` with a
     paragraph saying `source/Strongs/*.BP5` are Dr Robinson's official parsed
     files, the same official material as `source/CCAT` (see `source/README.md`).
     When `hits` is empty it adds that none of the six published ZIP archives
     contains a parsed/Strong's file, so the delivery route is not recorded (a
     gap in the archive evidence, not a doubt about the files' origin); when
     `hits` is non-empty it says the route is recorded and names the hit(s).
   - `_summary` (lines 350-358): the mapping-coverage sentence names the new
     class, and the `## Strong's / BP5` section follows the same
     hits-versus-empty distinction.
   - `_decision_log` R4 (line 398): the row changes from `pending` to a resolved
     decision on this basis; it is not deleted. Its evidence and decision text
     follow the same distinction, and the row keeps `resolved (2026-11-19)`:

     ```
     | R4 | Strong's/BP5 provenance. | `source/Strongs/*.BP5` are Dr Robinson's official parsed files (`source/README.md`); no parsed archive is among the six ZIPs, so the delivery route is not recorded. | (a) Find an official parsed archive. (b) Leave the files labelled unknown. | resolved (2026-11-19): the files are official Robinson material; only the delivery route for the parsed files is unrecorded. |
     ```
3. `docs/EDITIONS.md` source feature matrix (line 38): the `source/Strongs`
   provenance cell becomes `official files, not in the six ZIPs`.
4. `docs/PROVENANCE.md` (generated) follows from R7.2; no hand edit.
5. `SPECS/TECH.md` §2, last paragraph: replace "The provenance of the existing
   `source/Strongs/*.BP5` (parsing and Strong's numbers) must be established
   separately during the reconciliation cycle; it is not assumed to come from the
   archives listed above." with: `source/Strongs/*.BP5` are Dr Robinson's official
   parsed files (see `source/README.md`); none of the six archives listed above
   contains a parsed/Strong's file, so the delivery route for the parsed files is
   not recorded.
6. Tests asserting the old string are updated, not deleted:
   `tests/reconciliation/test_integration.py:48-59` (`test_strongs_provenance_unknown`
   becomes `test_strongs_provenance_is_official_source`, assertive of
   `official-source-files` and `delivery == "recorded" if hits else "not-recorded"`;
   `test_mapping_classes_present` expects `official-source`). A companion
   `test_strongs_delivery_follows_the_hits` simulates an archive member and
   asserts `delivery == "recorded"`.

## Decisions (fixed by the maintainer, plus the ones this spec finalises)

1. One spec folder covers all seven items, with the diff-engine work (R6) as its
   own phase.
2. `invariants.csv` always has a header, so an empty result reads as "clean", not
   "broken". **Finalised:** the header is the seven `Violation` fields
   (`dataset,path,line,category,message,key,known_exception`), not the
   `status`/`detail` sketched in the brief, because those would either be
   constant or duplicate `message`; see R5.10.
3. Strong's/BP5 provenance is resolved as official Robinson material, and
   decision-log row R4 is resolved on that basis rather than deleted.
4. R1 scope is `docs/EDITIONS.md` only. `docs/PROVENANCE.md`,
   `docs/HISTORY.md`, and the reconciliation decision log keep plain-text
   commits and tags; linking them is a separate, mechanical follow-up and would
   widen this change's review surface.
5. R1 links both endpoints of a tag range rather than the whole label; see R1.3.
6. R4 documents the relationship in `docs/EDITIONS.md` (generated, the reference
   document), the two folder READMEs (hand-written, where the folders are met),
   and one paragraph in the root README's hand-written layout section. The root
   README's generated block is not touched.
7. R6 adds both a column pair and a per-view file, because the report needs the
   former for `report.md` and the latter for auditing; it keeps the Beta-code
   view.
8. Determinism is a hard requirement: no timestamps, hostnames, absolute paths,
   or run-dependent ordering; a second full regeneration is byte-identical.

## Non-goals

- No text, source, CSV, TEI, PDF, archive, manifest, or checksum change.
- No new dependency, no network access in tests, no docs site, no CI workflow.
- No re-download (`fetch_official.py --force` is not used).
- No restructuring of `docs/`; no renaming of generated files except the new
  `apparatus.diff`.
- No change to the root README's generated block, so no risk to the
  `<!-- editions:begin -->` / `<!-- editions:end -->` block detection.
- No re-categorisation of the 37 Beta-code encoding-only diffs in `diff.py`'s
  category classifier: R6.6 names them in the report, it does not reclassify
  them.
- No linkifying of commits/tags outside `docs/EDITIONS.md` (decision 4).
- No general "every generated CSV declares its fields" refactor; only
  `invariants.csv` gains a declared header (R5.10). The risk of another empty CSV
  is covered by a test instead (see `plan.md` phase 4).

## Acceptance criteria

- `docs/EDITIONS.md` contains no unlinked release tag and no unlinked commit
  hash: every `` `v<major>.<minor>.<patch>` `` occurrence sits inside a
  `releases/tag/` link, and `97371d7` appears only inside a `commit/` link. The
  four diff bullets are relative links that resolve from `docs/`.
- `scripts/README.md`'s "Report generation order" section explains the shared
  file, the preserved evidence block, the required order, what a wrong order
  produces, and that both commands are idempotent, without the phrases "owns the
  evidence block" or "leaves exactly one block and one heading".
- `SPECS/MISSION.md` line 73 reads `what category`.
- `docs/EDITIONS.md` has the `## Working-tree paths and the curated editions`
  section with the five-row table; `csv-unicode/README.md` and
  `tei-xml-unicode/README.md` explain the relationship and the byte identity;
  the root README has the paragraph; a test asserts the five overlapping views
  are byte-identical for every `*.csv`/`*.xml` file.
- `docs/DATA_CONTRACT.md` explains its purpose, defines dataset/record/
  invariant/derivation, has a "How to read this document" section, a `Terms`
  section, a `What it holds` column in Coverage rendered from the contracts, a
  `Baseline report files` table, and an `Invariant results` section; the stale
  "next cycle" sentence is gone.
- `reports/baseline/invariants.csv` is
  `dataset,path,line,category,message,key,known_exception\n` and nothing else
  when there are no findings; the header equals `Violation.as_row()`'s keys.
- Every `reports/diffs/<pair>/` has `apparatus.diff`; `changes.csv` has the two
  new columns; `report.md`'s "Apparatus-only changes" entries show a Unicode
  line, and the 37 encoding-only rows say so explicitly instead of showing an
  unchanged line.
- No generated file claims `provenance-unknown` for `source/Strongs`; `R4` is
  `resolved (2026-11-19)`; `SPECS/TECH.md` §2 and `docs/EDITIONS.md` say
  `official` with the archives caveat.
- The full regeneration runs twice with no diff; all three test suites pass; no
  file under `data/raw/`, `source/`, `csv-unicode/**/*.csv`,
  `tei-xml-unicode/**/*.xml`, `editions/*/{source,csv,tei,manifest.json}` changed.

## Risks

- **Byte-identity test brittle against the untracked `.py`.** Compare `*.csv`
  names only, and state in the test name that the stray script is not part of the
  view; also move the file aside before regenerating, or
  `recover_editions.py` will copy it into `editions/` and change the manifest.
- **`changes.csv` schema drift.** The schema is asserted in the integration
  suite, not in `test_diff.py`; update both the writer and the assertion in the
  same step, and keep the new columns last so downstream selections by position
  keep working.
- **Empty-looking apparatus entries.** 37 rows have no Unicode difference. If
  they render as an empty code span, a reader will read the report as broken;
  R6.5 requires the explicit encoding-only sentence.
- **Report size.** `rp2018--rp2018-2023` has 156 apparatus-only entries. The
  sub-item form adds one line per entry (~312 lines), which is acceptable; do not
  expand each into headings plus fenced blocks.
- **Generated-block markers.** No new generated prose may contain the literal
  `<!-- editions:begin -->` or `<!-- editions:end -->`; the root README block is
  unchanged, and `RootReadmeTests.test_has_exactly_one_generated_block` guards it.
- **Tag links depend on local tags.** `editions.metadata` derives
  `latest_release` from `git tag`, so `docs/EDITIONS.md` already depends on the
  clone having tags; linking does not change that, but a shallow clone produces a
  different document, which the existing release-range tests already cover.
- **Two writers of `docs/HISTORY.md`.** R2's rewrite must describe the actual
  behaviour of `_render_history` and `_update_history`; do not promise an
  ordering guarantee the code does not make (both orders are safe today, but
  contract-last is documented as the supported order).
