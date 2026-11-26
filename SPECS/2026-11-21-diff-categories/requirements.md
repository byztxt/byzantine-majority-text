# Requirements - Diff categories: rename `variant-code`, document every category, show the tag change

Branch `feature/2026-11-16-edition-recovery-curation`, HEAD `9a5a9d1`, working
tree clean when this spec was written. This is a reporting and classification
change only: no text, source, archive, PDF, edition CSV/TEI/manifest, or
`data/` byte changes.

## Context

The maintainer read `reports/diffs/rp2018--rp2018-2023/report.md` and could not
tell what the category `variant-code` meant at **ACT 1:15**. The row is labelled
`variant-code`, and the Text block under it shows `εἶπεν --` -> `εἶπεν-`, which
is a dash-spacing difference in the derived Unicode text. Nothing tells the
reader that the source-tier difference is an apparatus code change, or that the
displayed Text difference is a conversion artefact.

The category name is opaque, the generated README does not define any category,
and `report.md` makes the reader infer the code change from Beta-code braces.
This spec fixes all three, and makes the evidence at ACT 1:15 honest.

## Verified inventory (2026-11-21, checked against the current tree)

Every claim below was checked before this spec was written.

| Fact | Evidence |
| --- | --- |
| `classify_diff` returns `variant-code` when the main text is identical, the code letters differ, and the apparatus is identical once the letters are stripped | `src/byz/reconcile/compare.py:35-53`, branch at 43-52; return at 51 |
| The classifier's complete category vocabulary is `""` (identical), `missing`, `variant`, `variant-code`, `capitalization`, `word-segmentation`, `whitespace`, `punctuation`, `accents-breathings`, `letters` | the `return` statements in `compare.py:35-73`; see the table below |
| `whitespace` is currently unreachable through `compare_maps`: `_main_text` collapses whitespace (line 20), a pure whitespace difference therefore reaches the apparatus branch, and `classify_diff("a b", "a  b")` returns `variant` | probe with `PYTHONPATH=src python3 -c "..."`; no generated row carries `whitespace` |
| At ACT 1:15 the current source (`rp2018-2023`) has `{C W(S > W(SEI\ }`; the official 2018 archive (`editions/rp2018/source/ccat/AC.CCT:17`) has `{N W(S > W(SEI\ }` | `data/text/CCAT/05_ACT.TXT` line `01:15`; `AC.CCT` line 17 |
| `C` = NA27/28 and `N` = Nestle-Aland, so the reading is unchanged and only its label moved | `data/text/README.md`, "Variant codes" |
| The Unicode apparatus spells the tags out: `N` -> `NA`, `B` -> `Byz`, `C` -> `NA27/28`, `M` -> `ECM`, `S` -> `NA27`, `E` -> `NA28` | `src/byz/beta/converter.py:116-121` |
| The ACT 1:15 row has `text_changed = true` only because the official source has `ei)^pen - ` while the current source has `EI)=PEN-`: a dash-spacing difference. The source-tier comparison canonicalises `\s*-\s*` to ` - `, so the source main text is identical | `changes.csv` row `ACT,1,15,...`; `normalize.normalize_spacing` at `src/byz/reconcile/normalize.py:63-70`; `compare._main_text` at line 19-20 |
| ACT 1:15 is the *only* apparatus-code row whose derived text also differs: 44 of the 45 apparatus-code rows have `text_changed = false`, and the one true row's text difference is dashes/whitespace only | probe over `reports/diffs/rp2018--rp2018-2023/changes.csv` |
| In this pair the source-tier tags change `N -> C` (29 rows) and `N -> S` (16 rows; `2PE 2:6` changes two positions and deduplicates to one `N -> S` line) | probe over the same CSV |
| The report's direction is left -> right: `rp2018` (official 2018, `N`) -> `rp2018-2023` (current, `C`). The reconciliation compares current vs official, so its row reads `C` vs `N`. Any rendered tag change must follow its document's direction | `diff._source_rows` calls `compare_maps(left, right)` (`diff.py:213-229`); reconciliation calls `compare_maps(current, official)` (`compare.py:169-172`) |
| `variant` currently means "the apparatus reading changed"; every generated `variant` row carries a `{...}` apparatus note | 103 `variant` rows across the four pairs, 0 without a brace |
| No generated file currently contains `bad-variant-code`, which is an unrelated contract-validator category | `grep -rn bad-variant-code reports/ docs/` |
| The reconciliation decision log names the category in row R2; the summary combines `variant` + `variant-code` | `src/byz/reconcile/report.py:372-374`, `:484`; `reports/reconciliation/decision-log.md:13` |

### The category vocabulary found in the code

The table is in classifier precedence order: when several descriptions fit,
`classify_diff` returns the first match. `""` is returned for an identical
verse and never appears as a `changes.csv` / `categories.csv` value.

| Category | Meaning | Emitted today |
| --- | --- | --- |
| `missing` | The verse exists on one side only. | no rows |
| `variant` | The apparatus reading or note changed; the main text is identical. | 103 rows |
| `variant-code` -> **`apparatus-code`** | Only the apparatus code letters changed; the reading is identical. | 45 rows (one pair) |
| `capitalization` | The main text differs only in capitalisation. | 12 rows |
| `word-segmentation` | The same letters are divided into words differently. | 8 rows |
| `whitespace` | Only whitespace differs. | unreachable today (see above) |
| `punctuation` | The main text differs only in punctuation. | 50 rows |
| `accents-breathings` | The main text differs only in accents or breathings. | 51 rows |
| `letters` | The main text letters differ. | 4 rows |

`bad-variant-code` (`src/byz/contract/ccat.py:111`) is a source-validation
violation, not a diff category, and is **not** renamed.

## Scope

- **Inputs touched:** none. The classifier reads the same parsed text; the
  report reads the same `changes.csv` rows.
- **Outputs touched (generated):** `reports/diffs/README.md`,
  `reports/diffs/<pair>/{report.md,changes.csv,source.diff,text.diff,
  apparatus.diff,derived.diff}`, `reports/reconciliation/{categories.csv,
  verses.csv,summary.md,decision-log.md}`, and the baseline contract files that
  hash the edited sources (`reports/baseline/*`, `docs/HISTORY.md`,
  `docs/EDITIONS.md`, `docs/HISTORY.md`). The baseline files change because
  they hash the edited sources; `docs/EDITIONS.md` changes because it gains the
  glossary pointer. The root README's generated block and every edition
  `README.md`, CSV, TEI, and manifest are regenerated and must stay
  byte-identical.
- **Hand-edited files:** `src/byz/reconcile/compare.py`,
  `src/byz/curate/diff.py`, `src/byz/reconcile/report.py`,
  `src/byz/curate/docs.py`, `docs/RELEASE-NOTES.md`, and the test files named in
  `plan.md`.
- **Not touched:** any file under `data/raw/`, `data/text/`, `editions/*/source/`,
  `editions/*/csv/`, `editions/*/tei/`, `editions/*/manifest.json`, and the
  dated `SPECS/2026-11-16-*` records.

## Requirements

### R1 - Rename the category to `apparatus-code` (C1)

1. `compare.classify_diff` returns `"apparatus-code"` where it returns
   `"variant-code"` today (`compare.py:51`), and the surrounding comment says
   "apparatus code" rather than "code".
2. Define the vocabulary once, next to the classifier:
   - `CATEGORY_MEANINGS`: an ordered mapping from every category the classifier
     can return (the nine names above) to a one-line meaning. `""` is not a key.
   - `APPARATUS_CODE_NAMES`: an ordered mapping `N`/`B`/`C`/`M`/`S`/`E` to the
     witness names from `data/text/README.md`.
   Both are the only copies of these strings in production code. A test asserts
   that `APPARATUS_CODE_NAMES` covers exactly the letters accepted by
   `VARIANT_CODE_RE`, so a new letter cannot appear without a name.
3. The rename reaches every produced and documented occurrence:
   the classifier, the diff report and its four `.diff` hunk labels, the
   `changes.csv` `category` value, the reconciliation `categories.csv`,
   `verses.csv`, `summary.md`, and `decision-log.md` R2, the generated README,
   and the tests that pin the value.
4. The distinction is stated in the produced documentation: `variant` means the
   apparatus *reading or note* changed; `apparatus-code` means only the *code
   letters* changed and the reading is identical.
5. `bad-variant-code` and the contract validator are unchanged.

### R2 - Print the tag change in every apparatus-code entry (C3)

1. A single helper in `src/byz/curate/diff.py` derives the code change from the
   row's `source_left` and `source_right` using `compare.VARIANT_CODE_RE`:
   - same codes -> empty string;
   - equal numbers of codes -> the differing positions, deduplicated in
     left-to-right order, rendered `N -> C` (or `N -> C; B -> M` when two
     different changes occur);
   - unequal numbers (defensive; the classifier does not produce it) -> the two
     full sequences, `N,N -> C`.
2. Every entry whose category is `apparatus-code` prints
   ``Apparatus code: `N` -> `C` (the reading is unchanged)`` as its first
   detail line. This applies to the 44 apparatus-only entries and to ACT 1:15.
3. The Beta-code evidence and the Unicode apparatus evidence stay:
   - apparatus-only entries keep `Apparatus (Unicode):` and
     `Apparatus (Beta code):`, with the tag line first;
   - the ACT 1:15 main-text entry gains `Apparatus (Unicode):` after its
     existing `Source (Beta code):` block. The Source block already is the
     Beta-code evidence, so it is not printed twice.
4. The arrow follows the document's own direction: the diff report renders
   `N -> C` for ACT 1:15; the reconciliation R2 row keeps `C` vs `N`. Do not
   hard-code a direction or a verse.

### R3 - Stop the label contradicting the evidence (C4)

1. The `## Main-text changes` heading becomes
   `## Main-text changes (derived text differs)`, and a lead sentence says the
   sections are grouped by the derived Unicode text while the category is the
   source-tier classification.
2. The `## Apparatus-only changes` section gains a lead sentence saying the
   normalised derived text is identical in every entry and the category names
   which source tier changed. Do not claim the source main text is unchanged:
   two `capitalization` rows live in this section.
3. In a main-text entry whose category is `apparatus-code`, the Text block is
   labelled `Text (derived; typographic only, not part of the source-tier
   change):` instead of `Text:`. The tag line states the actual source-tier
   change, and the Source and Apparatus blocks carry the evidence. Nothing is
   removed: the dash difference remains in the entry, in `text.diff`, and in
   `changes.csv`.
4. The per-pair `## Categories (source tier)` table gains a `Meaning` column
   from `CATEGORY_MEANINGS` and a sentence pointing at the README glossary
   (`../README.md#categories`). A category without a meaning is a loud
   `KeyError`, not a blank cell.

### R4 - Document every category with a worked example (C2)

`reports/diffs/README.md` (generated from `README_TEXT` in `diff.py`) gains a
`## Categories` section:

1. A table in classifier precedence order with columns
   `Category | Meaning | Example`. Meanings come from `CATEGORY_MEANINGS`;
   examples come from a single `CATEGORY_EXAMPLES` mapping in `diff.py` that
   stores `(pair, book, chapter, verse)` for the seven categories that occur in
   the current reports, and omits `missing` / `whitespace` (rendered
   "none in the current reports").
2. A sentence saying the table follows the classifier's precedence.
3. A paragraph distinguishing `variant` from `apparatus-code`, with both real
   examples:
   - `apparatus-code`: `ACT 1:15` in `rp2018--rp2018-2023`, tag `N` -> `C`,
     reading unchanged;
   - `variant`: `1CO 3:14` in `rp2005--rp2018`, the apparatus reading gains
     `{NA μένει > μενεῖ }`.
4. The apparatus-code names sentence generated from `APPARATUS_CODE_NAMES`,
   noting that the Unicode apparatus spells `{N` as `{NA` and `{C` as
   `{NA27/28`, so `{NA-]{+{NA27/28+}` is the same change as `{N-]{+{C+}`.
5. A sentence that `category` is a machine-readable value and that an empty
   category never appears in `changes.csv`.
6. The existing `report.md` and `changes.csv` bullets are updated to describe
   the tag line, the Meaning column, and the derived-text label.

The example references are not decorative: a test resolves each
`CATEGORY_EXAMPLES` entry in the corresponding generated `changes.csv` and
asserts the category still matches.

### R5 - Rename in the reconciliation report and decision log

1. `report._summary` keeps the combined apparatus count but states the split
   explicitly, for example:
   "`T` are apparatus differences (`R` reading changes, `C` code-only changes)".
2. `report._decision_log` R2 names the category `apparatus-code` and says the
   tag differs while the reading does not. R2 stays `pending`; this change does
   not decide R2.
3. The `## Categories` table sentence in `summary.md` points at
   `../diffs/README.md#categories` (the same meanings, one copy).
4. No other prose in `summary.md` or `docs/PROVENANCE.md` changes meaning.

### R6 - `changes.csv` and the `.diff` labels

1. `CSV_FIELDS` (`diff.py:37-51`) is unchanged: 13 columns, same order. The only
   machine-readable change is the `category` *value*.
2. `changes.csv`, `source.diff`, `text.diff`, `apparatus.diff`, and
   `derived.diff` render `apparatus-code` wherever the classifier would have
   emitted `variant-code`. No alias value is emitted.
3. The migration impact is stated in `docs/RELEASE-NOTES.md` (hand-maintained):
   which files carry the value, that no alias is emitted, why the name changed,
   and that consumers filtering `category == "variant-code"` must switch to
   `apparatus-code`.
4. `docs/EDITIONS.md`'s "Successive diffs" section gains one sentence pointing
   at `../reports/diffs/README.md#categories`, so the generated index explains
   the vocabulary without duplicating the table.

### R7 - Red/green tests and a rename lock

1. The unit test that pins the classifier value is renamed and updated; it is
   not weakened or deleted.
2. New tests cover: the tag helper; `CATEGORY_MEANINGS` completeness and order;
   `APPARATUS_CODE_NAMES` completeness; the README glossary; the ACT 1:15
   rendering; the apparatus-only tag line; and the reconciliation R2 row.
3. A guard test fails if `variant-code` reappears in generated output:
   every `.md`, `.csv`, and `.diff` under `reports/` is scanned, with
   `bad-variant-code` explicitly excluded because it is a different vocabulary.
   The guard is scoped to generated output; the hand-written release note and
   the dated specs may name the old value as history.
4. A positive guard asserts `apparatus-code` is present for ACT 1:15, so the
   rename cannot silently disappear.

### R8 - Determinism and no corpus drift

1. Every generated file is produced by its generator; no generated file is
   hand-edited.
2. A second full regeneration is byte-identical: no timestamps, hostnames,
   absolute paths, or run-dependent ordering.
3. The complete regeneration sequence either leaves `editions/`, `data/text/`, and
   `data/` byte-identical or the run is a failure.

## Decisions

The maintainer fixed C1-C4; this spec finalises the remaining presentation
choices.

1. **C1 - the name is `apparatus-code`.** It names the tier (apparatus) and the
   thing that changed (the code), and it is consistent with the sibling
   `variant`, which names the apparatus reading. `apparatus-tag` was rejected as
   a synonym for the same thing; `variant-code` was rejected because "variant"
   reads as the reading while the reading is unchanged.
2. **C2 - the glossary is generated from the code's own vocabulary.**
   `CATEGORY_MEANINGS` sits next to `classify_diff`, and the report table and the
   README table both read it. Categories with no current row (`missing`,
   `whitespace`) are documented as such rather than hidden, because the task is
   to document every category the pipeline can emit.
3. **C3 - the line is ``Apparatus code: `N` -> `C` (the reading is unchanged)``.**
   It uses the category's own noun, follows the document's left-to-right
   direction, and is printed in every apparatus-code entry so the 44
   apparatus-only rows and ACT 1:15 read the same way.
4. **C4 - the main-text/derived-text grouping is kept; the entries are made
   explicit.** ACT 1:15 stays in `Main-text changes` because its normalised
   derived text does differ (dash spacing), and the entry now states the
   source-tier change and labels the Text block as derived. The rejected
   alternative was to move every `apparatus-code`/`variant` row into
   `Apparatus-only changes` by source-tier category. That would align the
   section with its label, but it would hide the visible dash difference from
   `report.md`, contradict the section's current definition (which the
   counters and tests use), change the documented counts (156 -> 157), and
   still leave the two `capitalization` rows in a section whose name they do not
   match. The chosen fix is smaller, keeps all evidence in one entry, and does
   not reclassify any text.
5. The section headings gain parentheticals and lead sentences rather than being
   renamed wholesale, so existing readers and substring-based tests keep
   working.
6. The rename is a deliberate breaking change to a machine-readable value; the
   migration note lives in `docs/RELEASE-NOTES.md`, not in generated prose.
7. Dated specs under `SPECS/2026-11-16-*` are historical records and are not
   rewritten; the docs-clarity validation set that precedent for
   `provenance-unknown`. This spec supersedes their `variant-code` wording.

## Non-goals

- No change to `classify_diff`'s decision logic, precedence, or any category
  other than the `variant-code` name. In particular, the unreachable
  `whitespace` branch and the `variant` fallback for a brace-free
  whitespace-only difference are documented, not re-engineered.
- No removal or reclassification of `bad-variant-code`, or any other contract
  validator category.
- No new `changes.csv` column (the tag change is derived in the report), no new
  generated file, and no change to the `.diff` file formats.
- No change to `reports/diffs/README.md`'s existing notation, derived-only, or
  blank-verse sections beyond the new category section and the two updated
  bullets.
- No rewrite of the reconciliation decision R2 (keep current codes vs adopt
  official 2018 codes): it stays pending.
- No historical-spec rewrite.

## Acceptance criteria

- `compare.classify_diff("text {C x > y }", "text {N x > y }")` returns
  `apparatus-code`, and no production path returns `variant-code`.
- `CATEGORY_MEANINGS` has exactly the nine classifier categories, in precedence
  order; `APPARATUS_CODE_NAMES` has exactly `N B C M S E`.
- `grep -rn "variant-code" reports/ | grep -v bad-variant-code` prints nothing
  (no `bad-variant-code` occurs today; the guard excludes it if it ever does).
- `grep -c "Apparatus code: " reports/diffs/rp2018--rp2018-2023/report.md` is
  **45**; the values are `N -> C` (29 entries, including ACT 1:15) and
  `N -> S` (16 entries; 2PE 2:6 changes two positions and deduplicates to one
  line).
- In `reports/diffs/rp2018--rp2018-2023/report.md`:
  - ``### ACT 1:15 · `apparatus-code` `` is present;
  - its entry contains
    ``Apparatus code: `N` -> `C` (the reading is unchanged)``,
    `Text (derived; typographic only, not part of the source-tier change):`,
    `Source (Beta code):`, `Apparatus (Unicode):`, and
    `[-{NA-]{+{NA27/28+}`;
  - the apparatus-only entry ``- `ACT 1:10` · `apparatus-code` `` contains
    ``  - Apparatus code: `N` -> `C` (the reading is unchanged)``, followed by
    `Apparatus (Unicode):` and `Apparatus (Beta code):`.
- `reports/diffs/README.md` has `## Categories`, a nine-row table in precedence
  order, the ACT 1:15 apparatus-code example, the 1CO 3:14 variant example, the
  `variant` vs `apparatus-code` paragraph, and the apparatus-code names.
- Every `CATEGORY_EXAMPLES` reference resolves in the generated `changes.csv`
  with the stated category.
- The reconciliation `decision-log.md` R2 contains ``category `apparatus-code` ``;
  `summary.md` states the reading/code split and links the glossary.
- `changes.csv` keeps `book,chapter,verse,category,source_word_diff,
  text_word_diff,source_left,source_right,text_left,text_right,text_changed,
  apparatus_word_diff,apparatus_changed`, in that order, for all four pairs.
- `docs/RELEASE-NOTES.md` has the migration section; `docs/EDITIONS.md` has the
  glossary pointer.
- The full regeneration runs twice with no diff; all three suites pass; no file
  under `data/`, `data/text/`, `editions/*/source|csv|tei|manifest.json` changes.

## Risks

- **Count churn.** R3.1/R3.2 are presentation only, so the pinned counts
  (`161` source-tier, `156` apparatus-only, `97` derived, and the pairwise
  counts in `tests/curate/test_integration.py:96-157` and
  `tests/reconciliation/test_offline.py:20-25`) must not change. If a count
  changes, the implementation moved rows instead of relabelling them.
- **Generator KeyError.** Adding a `Meaning` column makes an unknown category a
  crash. That is deliberate, but it means a future classifier change must add a
  meaning in the same commit; the completeness test makes the coupling visible.
- **Direction and verse hard-coding.** `N -> C` is correct only for the
  `rp2018--rp2018-2023` direction. The helper must derive it; the reconciliation
  keeps `C` vs `N`.
- **Glossary drift.** Examples are real data references. They are asserted
  against the generated CSV; a future edition change that removes the verse will
  fail the test, not silently lie.
- **Generated-output guard vs `bad-variant-code`.** The guard excludes the
  contract validator category explicitly. Do not implement it as a bare
  substring test on `bad-variant-code` output.
- **Determinism.** The glossary order must come from the constant, never from a
  `set`. `changes.csv` field order must not move.
- **Historical specs.** `SPECS/2026-11-16-edition-recovery-curation/requirements.md:174`
  keeps the old name; the docs-clarity validation already treats dated specs as
  history. Record this in the validation deviations log.
