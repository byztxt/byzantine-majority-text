# Requirements - Retire the legacy Unicode trees: sources -> pipeline -> editions

## Context

The repository has one obvious model and one leftover that contradicts it.

The model is **sources -> pipeline -> editions**: `source/` (and the committed
archives in `data/raw/`) are the authoritative inputs, `editions/<id>/` holds
every derived view for every edition, and a single pipeline
(`scripts/recover_editions.py` -> `scripts/build_editions.py`) produces them.

The leftover is the pair of legacy convenience trees, `csv-unicode/` and
`tei-xml-unicode/`, plus the two top-level scripts that once wrote them
(`scripts/csv_converter.py`, `scripts/tei_xml_converter.py`). They describe the
current text only, they duplicate the same bytes as
`editions/rp2018-2023/`, and nothing says which of the two copies a reader is
supposed to use.

Worse, the dependency runs the wrong way. The curated edition is not built from
`source/`; it is **copied out of** the legacy trees:

```
today
  source/CCAT, source/Strongs
        |                                   csv-unicode/  (converter output)
        |                                        |
        v                                        v
  scripts/csv_converter.py  ------------>  csv-unicode/ccat, /strongs
        |                                        |
        |                                        |  recover.py copies
        v                                        v
  (nothing)                            editions/rp2018-2023/csv/*
  scripts/tei_xml_converter.py -------> tei-xml-unicode/no-accents
                                                 |
                                                 v
                                       editions/rp2018-2023/tei/unaccented
```

So the "convenience mirror" is an **input** to the curated edition, and the
edition is a copy of it. That is backwards: a mirror is a copy of the canonical
artifact, never its source.

```
after
  source/CCAT, source/Strongs
        |
        v
  scripts/recover_editions.py   (snapshot source/ into editions/<id>/source/)
        |
        v
  editions/rp2018-2023/source/  ->  scripts/build_editions.py
        |
        v
  editions/rp2018-2023/{csv,tei,manifest.json,README.md}
        |
        +--> reports/baseline/        (byz.contract)
        +--> reports/reconciliation/  (byz.reconcile)
        +--> docs/EDITIONS.md         (build_editions.py)
```

This change finishes the migration that `SPECS/TECH.md` §5 anticipated ("The
migration from the current `source/`, `csv-unicode/`, and `tei-xml-unicode/`
layout is a spec of its own"). It is structure, pipeline, docs, and tests only:
no text, archive, PDF, manifest hash, or edition byte changes.

## Goal

1. Invert the dependency: `build_current()` generates all five CSV views and
   both TEI views of `rp2018-2023` from that edition's own `source/` snapshot;
   `recover_current()` copies only `source/`.
2. Prove with a hard gate that the regenerated edition is **byte-identical** to
   the committed one.
3. Delete `csv-unicode/` and `tei-xml-unicode/` entirely, and retire the two
   converters, so one pipeline remains.
4. Repoint every consumer (contract, reconciliation, registry, tests, docs,
   agent instructions) at `editions/rp2018-2023/`.
5. Relocate the only content that exists nowhere else: the CollateX walkthrough
   and its three demo assets.
6. Keep the two *intentional* duplications and document them so nobody
   "de-duplicates" them later.

## Non-goals

- No change to any source file under `source/`, any archive under `data/raw/`,
  any PDF, any `editions/*/source/`, `editions/*/csv/`, `editions/*/tei/`, or
  any `editions/*/manifest.json` hash. The CSVs and TEI must keep the exact
  bytes they have today.
- No new output format, no new edition, no renaming of an existing view
  directory, no `apparatus.diff`-style new artifact.
- No redirect stubs, placeholder READMEs, symlinks, or compatibility shims for
  the removed paths.
- No change to the reconciliation numbers, the diff reports' content, or the
  baseline invariant results. Only dataset *names* and *paths* move.
- No work from `SPECS/2026-11-19-docs-clarity/` beyond recording that this
  change is its prerequisite (see "Sequencing").
- No `fetch_official.py --force`, no re-download, no re-extraction.
- No new dependency. This change *removes* two.

## Affected scope

- **Editions:** `rp2018-2023` only, and only in *how* its artifacts are
  produced. Its `source/`, `csv/`, `tei/`, and `manifest.json` are byte-identical
  afterwards. Its `README.md` gains one sentence (generated) and is the only
  edition file whose text changes.
- **Inputs touched:** none. `source/CCAT`, `source/Strongs`, and the six
  archives are read exactly as today.
- **Outputs touched:** `docs/EDITIONS.md`, `docs/HISTORY.md`,
  `docs/DATA_CONTRACT.md`, `docs/PROVENANCE.md`, `docs/contract/*.json`,
  `reports/baseline/*`, `reports/reconciliation/*`, `editions/*/README.md`,
  the root `README.md` (hand-written parts), `scripts/README.md`,
  `scripts/requirements.txt`, `SPECS/TECH.md` §5, and the agent instructions
  under `.opencode/`.
- **Deleted:** `csv-unicode/`, `tei-xml-unicode/`, `scripts/csv_converter.py`,
  `scripts/tei_xml_converter.py`.
- **New:** `docs/COLLATEX.md`, `docs/RELEASE-NOTES.md`, `docs/assets/`, and one
  test module `tests/curate/test_current_pipeline.py`.

## Verified inventory

Every claim below was checked against the working tree on
`feature/2026-11-16-edition-recovery-curation`, 2026-11-19. Byte comparisons were
done in memory (or under `/tmp/opencode`) without writing to the repository; no
generator was run.

### The dependency that must be inverted

| Fact | Check |
| --- | --- |
| `recover_current()` copies five legacy directories into six edition paths | `src/byz/curate/recover.py:249-280`, `_copy_tree` calls at 255-278 |
| `csv-unicode/ccat/no-variants` -> `csv/accented/no-variants` | `recover.py:255-258` |
| `csv-unicode/ccat/with-variants` -> `csv/accented/with-variants` | `recover.py:259-262` |
| `csv-unicode/strongs/with-parsing` -> `csv/strongs/with-parsing` | `recover.py:263-266` |
| `csv-unicode/strongs/no-parsing` -> `csv/strongs/no-parsing` | `recover.py:267-270` |
| `csv-unicode/strongs/no-parsing` -> `csv/unaccented` | `recover.py:271-274` |
| `tei-xml-unicode/no-accents` -> `tei/unaccented` | `recover.py:275-278` |
| `build_current()` does nothing but the accented TEI | `src/byz/curate/build.py:536-537` |

### Byte identity today (`diff -rq`, no differences)

| Left | Right | Files |
| --- | --- | ---: |
| `csv-unicode/ccat/no-variants` | `editions/rp2018-2023/csv/accented/no-variants` | 29 |
| `csv-unicode/ccat/with-variants` | `editions/rp2018-2023/csv/accented/with-variants` | 29 `.csv` |
| `csv-unicode/strongs/with-parsing` | `editions/rp2018-2023/csv/strongs/with-parsing` | 27 |
| `csv-unicode/strongs/no-parsing` | `editions/rp2018-2023/csv/strongs/no-parsing` | 27 |
| `csv-unicode/strongs/no-parsing` | `editions/rp2018-2023/csv/unaccented` | 27 |
| `tei-xml-unicode/no-accents` | `editions/rp2018-2023/tei/unaccented` | 27 + `BYZ/byz.xml` |

The one entry on the left that is not on the right is
`csv-unicode/ccat/with-variants/variant_analysis.py`, an **untracked** stray
script that is not part of any view.

### The port is a port, not a rewrite (verified in memory)

`scripts/beta_to_unicode_custom/beta_to_unicode_custom.py` already holds every
conversion rule. `src/byz/curate/build.py` already imports it (`_buc`,
lines 134-140) and already has `parse_cct_accented()`, `write_csv()`,
`write_tei()`, `write_accented_tei()`, and `_read_csv_verses()`. Three
verification runs were made against the committed files:

> **Correction (implementation).** An earlier draft of this section claimed
> that `parse_cct_accented()` alone reproduced the current accented views. That
> is wrong: it is the *official-archive* reader and runs
> `normalize.production_ccat_line`, which upper-cases the text, so on
> `source/CCAT` it yields `Βίβλος ΓΕΝΈΣΕΩΣ ... ΥἹΟΥ ͂ ...` instead of the
> committed `Βίβλος γενέσεως ... υἱοῦ ...`. The current views need a dedicated
> reader for the all-lowercase `source/CCAT` dialect, `parse_cct_current()`
> (a port of the retired converter's reader, including the `? ` paragraph
> rewrite). The two readers are deliberately separate and labelled by source
> dialect; see `build.py`.

1. `build.parse_cct_current(path, drop_variants=True/False)` for all 29
   `source/CCAT/*.TXT` files reproduces **every row** of both accented CSV views
   (0 differing books, 0 differing rows).
2. `buc.convert_beta_to_unicode_strongs(body, drop_parsing=False/True)` with the
   `NN.NN` prefix split reproduces **every row** of `strongs/with-parsing` and
   `strongs/no-parsing` for all 27 `source/Strongs/*.BP5` files.
3. Writing those rows with `build.write_csv()` into a temporary directory
   reproduces **all 139 CSV files byte-for-byte** (29 + 29 + 27 + 27 + 27),
   including quoting, `\n` line endings, and the empty intentional-blank rows.
4. `build.write_tei()` over `csv/unaccented` in `paths.CANONICAL_BOOKS` order,
   **without** an `edition_label`, reproduces
   `tei/unaccented/MAT.xml` and `tei/unaccented/BYZ/byz.xml` byte-for-byte.

So the only capability that lives *only* in `scripts/csv_converter.py` is the
`.BP5` reader (`extract_verse_chapter` for the `XX.XX` format,
`read_book_lines`, the drop-parsing token loop, and the pandas
filter/cast/`to_csv` layer). That is a port of roughly 40 lines.

### Consumers that must be repointed

| Consumer | What it does today |
| --- | --- |
| `src/byz/contract/paths.py:11-23` | `CSV_DIR = ROOT/"csv-unicode"`, `TEI_DIR = ROOT/"tei-xml-unicode"/"no-accents"`, `TEI_ASSETS` |
| `src/byz/contract/inventory.py:11-44` | seven dataset rows named `csv-unicode/...`, `tei-xml-unicode/...` |
| `src/byz/contract/inventory.py:61-69` | `DOC_FILES` lists the two folder READMEs |
| `src/byz/contract/coverage.py:3-29` | five `COMPARISONS` keyed by the legacy dataset names |
| `src/byz/contract/contracts.py:65-124` | six `DATASET_CONTRACTS` entries named by the legacy paths |
| `src/byz/contract/derivation.py:23-66` | targets built from `paths.CSV_*` / `paths.TEI_*`; the `TEI_BYZ` source label at line 52; the demo asset row at 57-66 |
| `src/byz/contract/invariants.py:10-52` | dataset names built as `f"csv-unicode/{key}"`; TEI datasets literal |
| `src/byz/contract/history.py:7-14, 59-87` | dataset labels and the three git pathspecs |
| `src/byz/contract/report.py:52-159, 162-181` | `_contract_doc`, and decision D2 naming `tei-xml-unicode/no-accents` |
| `src/byz/reconcile/compare.py:228-259` | `_load_current_csv` / `_load_current_tei` hardcode the legacy paths |
| `src/byz/reconcile/compare.py:278-281, 354-395` | dataset labels and mapping rows |
| `src/byz/generated.py:57-66, 169-178` | `HAND_MAINTAINED` and the last `GENERATED_FILES` row |
| `scripts/README.md:52-56` | "Csv converter" section |
| `src/byz/curate/docs.py:114-118, 129-143` | prose that says the current views are "copied ... from the current working tree" |
| `src/byz/curate/build.py:53-57` | `EXPORT_NOTES["current"]` |
| `README.md` | "Start here", "Generated files" row, "Repository layout", "Which text should I use?" |
| `docs/contract/*.json` | six filenames derived from the dataset names |
| `.opencode/agents/{build,plan,verifier,code-reviewer,spec-implementer}.md`, `.opencode/skills/{investigate-bug,fix-typing-linting-issues,feature-specification}/SKILL.md`, `.opencode/commands/read-conventions.md` | describe the legacy trees and the two converters as the working pipeline |
| Tests | `tests/curate/test_fidelity.py`, `test_editions.py`, `tests/contract/test_integration.py`, `test_coverage.py`, `test_generated.py` |

### Content that exists only in the legacy trees

| Content | Where it goes |
| --- | --- |
| `tei-xml-unicode/assets/coll.png` | `docs/assets/coll.png` |
| `tei-xml-unicode/assets/demo_collation.xlsx` | `docs/assets/demo_collation.xlsx` |
| `tei-xml-unicode/assets/demo_john_1.xml` | `docs/assets/demo_john_1.xml` |
| `tei-xml-unicode/README.md` CollateX walkthrough (INTF P66 URL, `java -jar collatex-tools-1.7.1.jar -xp '//w' ...` command, screenshot) | `docs/COLLATEX.md` |
| `csv-unicode/README.md` "words with more than one parsing" note | one sentence in `docs/EDITIONS.md` (it already points at `source/README.md`, which explains the convention in full) |

### Corrections to the brief, and things it does not mention

1. **`.opencode/` also consumes the legacy paths.** Eight files under
   `.opencode/` tell agents to regenerate `csv-unicode/` and
   `tei-xml-unicode/`, to run `csv_converter.py` / `tei_xml_converter.py`, and to
   read their READMEs. If they are not updated they will instruct future agents
   to recreate the retired trees. They are in scope (R10).
2. **`src/byz/contract/history.py` is a consumer the brief does not name.**
   Its `DATASETS` rows and the `head` / `july_2023` git pathspecs produce the
   `csv-unicode/ccat`, `csv-unicode/strongs`, and `tei-xml-unicode` rows of
   `docs/HISTORY.md`. Repointing `docs/HISTORY.md` means changing `history.py`.
3. **`docs/contract/*.json` filenames change with the dataset names.** Six stale
   files (`csv-unicode__*.json`, `tei-xml-unicode__*.json`) must be deleted, or
   `docs/contract/` keeps documents for datasets that no longer exist.
4. **The contract inventories the demo assets.** `inventory._specs()` has a
   `tei-xml-unicode/assets` row (3 files, `format_class="asset"`) and
   `derivation.check()` records `demo_john_1.xml` as `auxiliary`. Moving the
   assets means deciding what happens to those two records (R7.3).
5. **There is no release-note file.** `SPECS/TECH.md` §5 says a move must be
   documented "in the README and release notes", but the repository has no
   release-notes document. This change creates `docs/RELEASE-NOTES.md`.
6. **`BYZ/byz.xml` book order differs between the two TEI views.** The accented
   combined file starts at `B07` (alphabetical, produced by
   `write_accented_tei`), the unaccented one starts at `B01` (canonical,
   produced by the legacy converter). The port must keep both orders exactly as
   they are; normalising either would change edition bytes.
7. **`pandas` and `numpy` are used only by the two retired converters.** No
   module under `src/`, `scripts/` (after deletion), or `tests/` imports them.
   `beta_code` is imported by `beta_to_unicode_custom` and is required.
8. **"No `csv-unicode/` string survives" cannot be literal.** `docs/EDITIONS.md`
   is generated, so its old-to-new mapping table must exist as a constant in
   `src/byz/curate/docs.py`; `recover.py` and `test_fidelity.py` name paths
   *inside git tag `v2.0.3`* (`csv-unicode/accents/...`), which are not
   working-tree paths. The rule is restated precisely in R9.3.
9. **The generated-Markdown classification test forbids new hand-written docs
   in `docs/`.** `tests/curate/test_generated.py:101-108` asserts that every
   `.md` under `docs/`, `editions/`, and `reports/` is generated. Adding
   `docs/COLLATEX.md` and `docs/RELEASE-NOTES.md` therefore needs an explicit
   hand-maintained allowlist (R6.4).
10. **`reports/baseline/summary.md` hardcodes "All 140 expected derivations
    exist".** The demo asset is the 141st row and is counted separately as
    `auxiliary`; keeping it as an auxiliary row (R7.3) keeps that sentence true.

## Definitions

- **Legacy tree** - `csv-unicode/` or `tei-xml-unicode/` in the working tree,
  as distinct from the identically named directories *inside git tag `v2.0.3`*,
  which the historical recovery still reads.
- **View** - one derived directory of an edition: `csv/accented/no-variants`,
  `csv/accented/with-variants`, `csv/unaccented`, `csv/strongs/with-parsing`,
  `csv/strongs/no-parsing`, `tei/accented`, `tei/unaccented`.
- **Current edition** - `rp2018-2023`, the only edition whose `source_kind` is
  `current`.
- **Source snapshot** - `editions/<id>/source/`, a copy of the inputs frozen
  inside the edition so the edition can be downloaded on its own.
- **Pipeline** - `scripts/recover_editions.py` + `scripts/build_editions.py`
  (`byz.curate.recover` + `byz.curate.build`). After this change it is the only
  producer of edition CSV/TEI.
- **Byte-identity gate** - the check that regenerating `rp2018-2023` leaves
  `editions/rp2018-2023/{source,csv,tei,manifest.json}` byte-identical.

## Maintainer decisions (fixed requirements)

1. **Delete both folders entirely.** Data, READMEs, and assets all go. No
   redirect README stubs, no symlinks. Every old path becomes a 404; that is
   accepted. The mapping is documented in `docs/EDITIONS.md` and in the release
   note only.
2. **Retire `scripts/csv_converter.py` and `scripts/tei_xml_converter.py`.** One
   pipeline. Their conversion logic already lives in
   `scripts/beta_to_unicode_custom/beta_to_unicode_custom.py`.
3. **Keep both `csv/unaccented/` and `csv/strongs/no-parsing/`** inside each
   edition. They are distinct user-facing views that happen to be byte-identical
   today; document the identity, do not collapse it.
4. **Keep `editions/<id>/source/`** as self-contained snapshots. For
   `rp2018-2023` that duplicates `source/` on purpose; document it as
   intentional, not redundancy.

Decisions this spec finalises (because the brief left them open):

5. **Asset location:** `docs/assets/` (a plain move, names unchanged) and
   `docs/COLLATEX.md` for the walkthrough. `docs/` is where a reader looks for
   documentation, and the screenshot's relative link then works from one file.
6. **Release note:** a new hand-maintained `docs/RELEASE-NOTES.md` carries the
   breaking-change entry and a short old-to-new table. It is listed in
   `generated.HAND_MAINTAINED`, is banner-free, and is linked from
   `docs/EDITIONS.md` and the root `README.md`.
7. **Contract treatment of the demo assets:** they stay inventoried, under the
   dataset name `docs/assets`, with `format_class="asset"`; the derivation row
   stays `auxiliary` with evidence `docs/COLLATEX.md`. Dropping them would
   silently shrink `reports/baseline/files.csv` for no user benefit.
8. **Dependencies:** drop `pandas` and `numpy` from `scripts/requirements.txt`,
   keep `beta-code==1.0.0`. After R4 nothing imports pandas or numpy; `beta_code`
   remains required by the shared converter module, and pinning it is what makes
   the text reproducible.
9. **`docs/HISTORY.md` keeps its pre-2026 history.** `history.DATASETS` grows an
   explicit git-pathspec tuple so the labels become
   `editions/rp2018-2023/csv` and `editions/rp2018-2023/tei` while the dated
   evidence still comes from the retired directories' commits (`e9ce9bf` 2022
   TEI, `97371d7` 2023 CSV, and so on). Losing those dates would hide when the
   CSV and TEI data actually last changed.

## Requirements

### R1 - Invert the dependency

`src/byz/curate/recover.py` `recover_current()` (lines 249-280) keeps only the
two `_copy_tree` calls that snapshot `source/CCAT` and `source/Strongs` into
`editions/rp2018-2023/source/`. The six calls at lines 255-278 go away.

`src/byz/curate/build.py` `build_current()` (lines 536-537) becomes the single
producer of the seven views, in this order:

1. `csv/accented/no-variants` and `csv/accented/with-variants` from
   `source/CCAT/*.TXT` via `parse_cct_current(drop_variants=...)` +
   `write_csv` (the official-archive `parse_cct_accented` reader is not
   interchangeable: it upper-cases the text);
2. `csv/strongs/with-parsing`, `csv/strongs/no-parsing`, and `csv/unaccented`
   from `source/Strongs/*.BP5` via a new `parse_bp5_strongs()` that delegates to
   `buc.convert_beta_to_unicode_strongs`, writing the *same dict* to
   `strongs/no-parsing` and `unaccented`;
3. `tei/unaccented` per book and combined, from `csv/unaccented`, iterating
   `paths.CANONICAL_BOOKS` and **without** `edition_label`;
4. `tei/accented` via the existing `write_accented_tei()`.

R1.1 `build_current()` accepts an optional target directory
(`build_current(edition, edition_dir=None)`), and `write_accented_tei()` accepts
the same, so the generator can be exercised against a temporary tree without
touching the repository. `build_all()` passes nothing and keeps today's
behaviour.

R1.2 The new `.BP5` reader validates its input: a line that does not start with
`NN.NN`, a book abbreviation that is not in `paths.ABBR_TO_BOOK_ID`, or a
missing `source/Strongs` directory raises with the file name and the offending
line/abbreviation. It does not silently skip.

R1.3 `EXPORT_NOTES["current"]` and the `rp2018-2023` prose in
`src/byz/curate/docs.py` say the views are generated from the edition's own
`source/` snapshot, not "copied ... from the current working tree".

### R2 - The byte-identity gate (hard)

R2.1 Regenerating `rp2018-2023` must leave
`editions/rp2018-2023/{source,csv,tei,manifest.json}` byte-identical to the
committed files: 29 + 29 + 27 + 27 + 27 CSV, 28 unaccented TEI files, 28
accented TEI files, and `manifest.json` including every `sha256` and `size`.

R2.2 If any file differs, stop and report. Never "fix" the edition to match the
new pipeline. The committed edition is the reference; a difference means the
port is wrong.

R2.3 The gate is automated as a hermetic test that builds into a temporary
directory from the edition's own `source/` and compares every file's SHA-256
(and the file-set equality) with the committed tree. It uses only committed
inputs and needs no network.

### R3 - Delete the legacy trees

R3.1 `csv-unicode/` and `tei-xml-unicode/` are removed from the working tree and
the index. 145 tracked files disappear:

| Path | Tracked files |
| --- | ---: |
| `csv-unicode/README.md` | 1 |
| `csv-unicode/ccat/no-variants/*.csv` | 29 |
| `csv-unicode/ccat/with-variants/*.csv` | 29 |
| `csv-unicode/strongs/with-parsing/*.csv` | 27 |
| `csv-unicode/strongs/no-parsing/*.csv` | 27 |
| `tei-xml-unicode/README.md` | 1 |
| `tei-xml-unicode/no-accents/*.xml` | 27 |
| `tei-xml-unicode/no-accents/BYZ/byz.xml` | 1 |
| `tei-xml-unicode/assets/{coll.png,demo_collation.xlsx,demo_john_1.xml}` | 3 (moved, not lost) |

R3.2 No stub, no `.gitkeep`, no symlink, no README pointing at the new path.
The directories do not exist.

R3.3 The untracked stray `csv-unicode/ccat/with-variants/variant_analysis.py` is
not part of any view and is not restored anywhere. It disappears with the
directory; that is acceptable and must be recorded in the change's validation
log.

R3.4 `tests/curate/test_editions.py` `ROOT_ITEMS` no longer lists the two names,
and a test asserts that neither directory exists.

### R4 - One pipeline, one converter module

R4.1 `scripts/csv_converter.py` and `scripts/tei_xml_converter.py` are deleted.
Nothing imports them; the shared module
`scripts/beta_to_unicode_custom/beta_to_unicode_custom.py` and
`scripts/tei_xml_header.xml` stay.

R4.2 `scripts/requirements.txt` contains exactly `beta-code==1.0.0`.
`scripts/README.md` loses the "Csv converter" section, describes
`recover_editions.py` + `build_editions.py` as the only producer, and keeps the
install instruction pointing at the now-single dependency.

R4.3 `src/byz/contract/paths.py` `DERIVATION_EVIDENCE` (lines 78-92) stops
naming the retired scripts. Each entry names the function in
`src/byz/curate/build.py` that now writes the view. The strings appear in
`docs/DATA_CONTRACT.md` and `reports/baseline/derivations.csv`, so they are part
of the repointing, not cosmetic.

### R5 - Repoint the contract and the reconciliation

R5.1 `src/byz/contract/paths.py` derives every current-text path from one
constant pair (`CURRENT_EDITION = "rp2018-2023"`,
`CURRENT_PREFIX = f"editions/{CURRENT_EDITION}"`). No module builds a legacy
path. A helper returns the dataset name for a view key so the path and the name
cannot drift.

R5.2 Dataset names follow the new paths everywhere:
`editions/rp2018-2023/csv/accented/no-variants`,
`.../csv/accented/with-variants`, `.../csv/strongs/with-parsing`,
`.../csv/strongs/no-parsing`, `editions/rp2018-2023/tei/unaccented`,
`editions/rp2018-2023/tei/unaccented/BYZ`, and `docs/assets`. They appear in
`reports/baseline/{files,books,differences,summary}.csv/.md`,
`docs/DATA_CONTRACT.md`, `docs/contract/*.json`, and
`reports/reconciliation/{files,verses,summary}`.

R5.3 The validated dataset set does not grow. `csv/unaccented` stays outside
`DATASET_CONTRACTS` and `inventory._specs()`, exactly as today: it is the same
bytes as `csv/strongs/no-parsing` and R8.3 locks that identity, so validating it
twice would add 27 `files.csv` rows, 27 `books.csv` rows, 27 derivation rows,
and falsify the "All 140 expected derivations exist" line in
`reports/baseline/summary.md` for no new information. `coverage.COMPARISONS`
keeps its five entries and its labels.

R5.4 `src/byz/reconcile/compare.py` loads the edition paths
(`_load_current_csv`, `_load_current_tei`) and emits the new dataset names in
`derived_rows()` and `mapping_rows()`. The reconciliation figures
(`7769/7972`, `7811/7972`, the 7951/7953 derived totals, the history rows) stay
identical, because the bytes are identical.

R5.5 `docs/contract/*.json` is exactly `contracts.json` plus one file per
dataset, named from the dataset name. The six stale legacy-named files are
deleted, and a test asserts the directory contains no extra file.

R5.6 `src/byz/contract/history.py` labels and git pathspecs follow decision 9 so
`docs/HISTORY.md` contains no retired working-tree path and keeps its dated
evidence.

### R6 - Registry, banners, and generated-file docs

R6.1 `src/byz/generated.py` drops the `csv-unicode/`, `tei-xml-unicode/` row
from `GENERATED_FILES` (13 rows become 12) and the two folder READMEs from
`HAND_MAINTAINED`.

R6.2 `HAND_MAINTAINED` gains `docs/COLLATEX.md` and `docs/RELEASE-NOTES.md`.
`GENERATED_MARKDOWN` is unchanged: the 17 generated Markdown files are the same
17.

R6.3 The two retired folder READMEs are gone, so no generated-file list may
mention them, and `tests/curate/test_generated.py` no longer asserts their
presence in `HAND_MAINTAINED`.

R6.4 `tests/curate/test_generated.py` grows an explicit hand-maintained
allowlist for these two docs, so
`test_every_markdown_under_generated_trees_is_classified` keeps its meaning
("every `.md` under `docs/`, `editions/`, `reports/` is either generated or
explicitly hand-maintained") without weakening to "anything goes".

R6.5 The root README's generated block lists only the surviving commands; the
`csv-unicode/` row disappears from the `## Generated files` table. The
hand-written layout table drops the legacy row and describes
`editions/rp2018-2023/` as the current text's CSV/TEI.

### R7 - Relocate the CollateX material

R7.1 The three assets move byte-for-byte to `docs/assets/` with the same names.
`docs/COLLATEX.md` carries the walkthrough: the CollateX download URL, the INTF
P66 transcription URL, the `demo_john_1.xml` link, the
`java -jar collatex-tools-1.7.1.jar -xp '//w' -xml -f csv -t demo_john_1.xml p66.xml > collation.csv`
command, and the `coll.png` screenshot. Relative links work from `docs/`.

R7.2 `docs/COLLATEX.md` states that `demo_john_1.xml` is a hand-prepared
single-chapter extract of `editions/rp2018-2023/tei/unaccented/JOH.xml`, not a
pipeline output, and that the collation exercise compares the Byzantine text
with an INTF manuscript transcription.

R7.3 `src/byz/contract/paths.py` `TEI_ASSETS` becomes
`ROOT/"docs"/"assets"`; `inventory._specs()` inventories it as
`docs/assets` (`format_class="asset"`); `derivation.check()` keeps the
`auxiliary` row for `demo_john_1.xml` with evidence naming `docs/COLLATEX.md`;
`compare.mapping_rows()` points its two auxiliary rows at
`editions/rp2018-2023/tei/unaccented/BYZ/byz.xml` and
`docs/assets/demo_john_1.xml`.

R7.4 `docs/EDITIONS.md` links `docs/COLLATEX.md` from its TEI section, and
`tests/curate/test_editions.py::PdfLinkTests.test_relative_markdown_links_resolve`
also checks `docs/COLLATEX.md` and `docs/RELEASE-NOTES.md` (it becomes "every
user-facing doc"), so a moved screenshot cannot leave a dead link.

### R8 - Keep and document the two intentional duplications

R8.1 `csv/unaccented/` and `csv/strongs/no-parsing/` stay separate directories
in every edition. `docs/EDITIONS.md` and `editions/<id>/README.md` state that
they hold the same bytes because they are two names for one text (the plain
Unicode text and the Strong's view with parsing dropped), that the duplication
is intentional, and that a test asserts the identity.

> **Superseded 2026-11-26:** the two directories are still separate, but they
> are no longer byte-identical. `csv/unaccented/` is plain text;
> `csv/strongs/no-parsing/` is the numbers-only view (Strong's numbers kept,
> morphology dropped, consecutive identical numbers collapsed). The identity
> test was replaced by shape and word-for-word TEI tests. See
> `SPECS/2026-11-26-pr46-review-fixes/`.

R8.2 `editions/<id>/source/` stays a self-contained snapshot. The edition
README's Layout section states that it is a frozen copy of the inputs so the
edition can be downloaded and verified on its own, and that for `rp2018-2023`
this intentionally duplicates `source/`.

R8.3 A test asserts (a) `editions/rp2018-2023/csv/unaccented` and
`csv/strongs/no-parsing` are byte-identical file for file, and (b)
`editions/rp2018-2023/source/CCAT` and `source/Strongs` are byte-identical to
`source/CCAT` and `source/Strongs`. Both are identity claims in the docs; both
get a lock so they cannot silently become false.

### R9 - Path mapping, breaking change, and the docs sweep

R9.1 `docs/EDITIONS.md` (generated) gains a section, after "Layout, exports, and
verification", titled `## Where the old working-tree paths went`. It holds:

- one paragraph: `csv-unicode/` and `tei-xml-unicode/` were removed on
  2026-11-19; the current text is `editions/rp2018-2023/`; the retired paths
  return 404 by design (no redirects, no stubs);
- a table `| Retired path | Now |` rendered from a module-level constant in
  `src/byz/curate/docs.py`, with one row per old path (the five CSV views, the
  two TEI paths, the three assets, the two READMEs — see `plan.md` for the exact
  rows);
- one sentence: the bytes did not change; the files moved, and the edition's
  `manifest.json` records the same hashes as before the change.

R9.2 `docs/RELEASE-NOTES.md` (new, hand-maintained, banner-free) carries one
entry for this change: what was removed, that every old URL now 404s, a compact
old-to-new table for the six data paths, and a pointer to the canonical table in
`docs/EDITIONS.md`.

R9.3 The documentation rule for the retired names is:

- **Allowed** in `docs/EDITIONS.md` (the mapping table), `docs/RELEASE-NOTES.md`,
  and `SPECS/**` (history).
- **Allowed in these Python locations only, each with a comment saying why:**
  `src/byz/curate/docs.py` (the mapping-table constant),
  `src/byz/curate/recover.py` (`ARTIFACT_PREFIXES`, paths inside tag `v2.0.3`),
  `src/byz/contract/history.py` (git pathspecs, decision 9), and
  `tests/curate/test_fidelity.py` (the same `v2.0.3` prefixes).
- **Forbidden** in every other tracked file: `README.md`, `scripts/README.md`,
  `source/README.md`, `docs/*.md` other than the two above, `reports/**`,
  `editions/**`, `.opencode/**`, and all other Python.

R9.4 Root `README.md` (hand-written parts): the "Start here" row, the layout
table, and "Which text should I use?" point at
`editions/rp2018-2023/`; the `docs/` row lists `COLLATEX.md`,
`RELEASE-NOTES.md`, and `assets/`.

R9.5 `SPECS/TECH.md` §5: the trailing paragraph that calls the migration "a spec
of its own" is replaced by a statement of the finished layout (sources ->
pipeline -> editions, one pipeline, no working-tree mirror) that references this
spec. §2 is untouched (the previous change's `source_page` text stays).

R9.6 `.opencode/` agent instructions describe the real pipeline: edit `source/`,
regenerate with `recover_editions.py` + `build_editions.py`, inspect
`editions/rp2018-2023/`; no reference to the retired trees or converters.

### R10 - Determinism and tests

R10.1 A second full regeneration is byte-identical: no timestamps, hostnames,
absolute paths, or run-dependent ordering.

R10.2 Every behaviour in R1-R9 has a failing test first (red) and a green test
after. The new test module is `tests/curate/test_current_pipeline.py`.

R10.3 No test touches the network, writes to the repository, or depends on a
machine-local absolute path. The byte-identity test builds into a temporary
directory from committed inputs.

R10.4 The three suites pass:
`tests/contract`, `tests/curate`, `tests/reconciliation`.

## Sequencing

`SPECS/2026-11-19-docs-clarity/` is written but not implemented. Two of its
items overlap this change:

- its **R4** ("document the relationship between `csv-unicode/`,
  `tei-xml-unicode/` and `editions/`") is **obsolete**: this change deletes the
  folders, so there is no relationship left to document. A "Superseded by" note
  is added under that heading in
  `SPECS/2026-11-19-docs-clarity/requirements.md`; that note is the only edit
  made outside this spec folder.
- its **R5** (`docs/DATA_CONTRACT.md` rewrite) must be written against the
  post-removal layout: the dataset glossary, the derivation map, and the
  baseline-report table all name the new paths.

Therefore **this change is a prerequisite of the docs-clarity work** and must be
implemented first. `docs/DATA_CONTRACT.md` is only repointed here; its rewrite
stays with docs-clarity.

## Acceptance criteria

- `csv-unicode/` and `tei-xml-unicode/` do not exist; `git ls-files` shows no
  path under either; no stub or symlink replaces them.
- `scripts/csv_converter.py` and `scripts/tei_xml_converter.py` do not exist;
  `scripts/requirements.txt` is exactly `beta-code==1.0.0`.
- `editions/rp2018-2023/{source,csv,tei,manifest.json}` are byte-identical to
  the pre-change tree; `git diff --stat` shows nothing under them (the edition
  README's new sentence is the only edition text change).
- `tests/curate/test_current_pipeline.py` passes and would fail if any view
  differed by one byte.
- `PYTHONPATH=src python3 -m byz.contract` and
  `PYTHONPATH=src python3 -m byz.reconcile` regenerate every report with dataset
  names under `editions/rp2018-2023/` and `docs/assets`, unchanged figures, and
  the six new `docs/contract/*.json` files only.
- `docs/EDITIONS.md` contains the `## Where the old working-tree paths went`
  section with the full mapping table; `docs/RELEASE-NOTES.md` carries the
  breaking change; the root README and `scripts/README.md` point at
  `editions/rp2018-2023/`.
- `docs/COLLATEX.md` and the three files in `docs/assets/` exist, the walkthrough
  text, URLs, command, and screenshot survive, and every relative link resolves.
- A test asserts `csv/unaccented` == `csv/strongs/no-parsing` and
  `editions/rp2018-2023/source` == `source/`.
- No tracked file outside the R9.3 allowlist contains a retired working-tree
  path or a retired converter name.
- The full regeneration runs twice with no diff; the three suites pass; no file
  under `data/raw/`, `source/`, or `editions/*/{source,csv,tei,manifest.json}`
  changed.

## Risks

- **The gate is the risk.** A "close enough" port that changes one byte in one
  verse silently changes an edition. The test compares hashes of every file and
  the file sets, and `validation.md` requires the manual `git status` proof
  before the deletion.
- **Order of operations.** If the trees are deleted before `build_current()`
  can generate all views, `recover_current()`'s remaining copies cannot fill the
  edition and every downstream report degrades. Phase order in `plan.md` is
  mandatory.
- **The unaccented TEI is order- and header-sensitive.** The legacy combined
  file is in canonical book order and carries the untouched
  `<edition n="2018">` header block; the accented one is alphabetical and
  carries the curated label. Passing `edition_label` or iterating a sorted glob
  for the unaccented view changes bytes.
- **Silent dataset-name drift.** Names are generated from `paths` in the
  contract but hard-coded in `coverage.COMPARISONS`, `contracts.DATASET_CONTRACTS`,
  and the reconciliation loaders. A test asserts the dataset set and that every
  name resolves to an existing directory.
- **Stale generated JSON.** `docs/contract/` keeps a file per contract name and
  never deletes one. Without the new "no extra file" test, six documents would
  describe datasets that no longer exist.
- **Agent instructions are executable documentation.** Leaving `.opencode/`
  unchanged would have future agents regenerate the retired trees.
- **Hand-written docs in `docs/`.** Two new banner-free Markdown files must be
  classified explicitly or the generated-file test fails for the wrong reason.
- **History evidence.** Repointing `history.py` carelessly would drop the 2022
  TEI and 2023 CSV commit dates from `docs/HISTORY.md`; decision 9 keeps them.
- **`docs/HISTORY.md` is written twice** (`byz.contract`, then `byz.reconcile`).
  Both must agree on the new dataset labels, as today.
