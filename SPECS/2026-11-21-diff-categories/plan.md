# Plan - Diff categories: rename `variant-code`, document every category, show the tag change

Specced against branch `feature/2026-11-16-edition-recovery-curation`, HEAD
`9a5a9d1`. The concurrent layout refactor
(`SPECS/2026-11-21-input-and-code-layout/`) has since landed at `fc71f28`:
`scripts/` became the `byz` modules under `src/`, and `source/` became
`data/text/`. Every command and path below is updated to that layout; the
amendments are recorded in `validation.md` §10.

The requirements are `requirements.md` (R1-R8, decisions, acceptance); this plan
turns them into ordered red/green task groups. `validation.md` is the checklist.

## Repository contract

- Source is authoritative: `data/text/CCAT/*.TXT` and `data/text/Strongs/*.BP5`.
  This change reads them; it never edits them.
- Generated files are derivatives. `reports/**`, `docs/EDITIONS.md`,
  `docs/PROVENANCE.md`, `docs/HISTORY.md`, `reports/baseline/*`, and the root
  README's generated block are written by generators, never by hand.
- `docs/RELEASE-NOTES.md` is hand-maintained (verified: no generator touches
  it; it is only linked from `docs/EDITIONS.md`).
- Python 3.10/3.12 with the single pinned dependency `beta-code==1.0.0`.
- Public domain; no new dependency, no network access in tests.

## Category vocabulary found in the code

From `src/byz/reconcile/compare.py:35-73`, in classifier precedence order
(the first matching test wins). `""` means identical and is never a
`changes.csv` / `categories.csv` value.

| Value | Line | Current occurrences in `reports/diffs` |
| --- | --- | --- |
| `missing` | 39 | 0 |
| `variant` | 48, 52 | 103 |
| `variant-code` | 51 | 45 (all in `rp2018--rp2018-2023`) |
| `capitalization` | 58 | 12 |
| `word-segmentation` | 62 | 8 |
| `whitespace` | 64 | 0 (unreachable today: `_main_text` collapses whitespace first) |
| `punctuation` | 68 | 50 |
| `accents-breathings` | 72 | 51 |
| `letters` | 73 | 4 |

`bad-variant-code` (`src/byz/contract/ccat.py:111`) is a different vocabulary
and is out of scope.

## Files changed

| Path | Kind | Change |
| --- | --- | --- |
| `src/byz/reconcile/compare.py` | hand | return `apparatus-code` at 51; add `APPARATUS_CODE_NAMES` and `CATEGORY_MEANINGS` next to `VARIANT_CODE_RE` (line 14); comment at 43-44 |
| `src/byz/curate/diff.py` | hand | `tag_change()`; `CATEGORY_EXAMPLES`; glossary builder; `_report` tag line, Meaning column, section leads/labels; `README_TEXT` glossary |
| `src/byz/reconcile/report.py` | hand | `_summary` reading/code split at 372-374; categories table sentence at 433-442; `_decision_log` R2 at 484 |
| `src/byz/curate/docs.py` | hand | one glossary pointer in the "Successive diffs" section of `write_editions_doc` (around 400-470) |
| `docs/RELEASE-NOTES.md` | hand | new `2026-11-21` migration section at the top |
| `tests/reconciliation/test_compare.py` | hand | rename the pinning test; vocabulary/name-mapping tests |
| `tests/curate/test_diff.py` | hand | `TagChangeTests`; glossary tests |
| `tests/curate/test_integration.py` | hand | ACT 1:15 and apparatus-only rendering; glossary examples; rename guard |
| `tests/reconciliation/test_integration.py` | hand | summary wording and R2 assertions |
| `tests/reconciliation/test_offline.py` | hand | committed-output rename guard and R2 assertion |
| `reports/diffs/README.md` | generated | `PYTHONPATH=src python3 -m byz.diff` |
| `reports/diffs/<pair>/*` | generated | same |
| `reports/reconciliation/*` | generated | `PYTHONPATH=src python3 -m byz.reconcile` |
| `reports/baseline/*`, `docs/HISTORY.md`, `docs/EDITIONS.md`, `README.md` | generated | `PYTHONPATH=src python3 -m byz.contract`, `PYTHONPATH=src python3 -m byz.build`, `PYTHONPATH=src python3 -m byz.reconcile` |

The current `editions/` tree is generated too, but nothing in this change may
alter it: `git status --porcelain -- editions/ data/` must stay empty.

## Phase 0 - Baseline (no writes)

1. Record the state and the counts that must not move:

```bash
git status --porcelain > /tmp/byz-categories-before.txt
git rev-parse --short HEAD
for f in reports/diffs/*/changes.csv; do echo "$f"; cut -d, -f4 "$f" | tail -n +2 | sort | uniq -c; done
grep -c "variant-code" reports/diffs/rp2018--rp2018-2023/report.md   # 46
grep -c "variant-code" reports/reconciliation/{summary.md,decision-log.md,verses.csv,categories.csv}
```

Expected: 161 / 3 / 54 / 55 source-tier rows and 156 / 0 / 8 / 8
apparatus-only rows for the four pairs, unchanged by this work.

2. Confirm the four pins that make the plan safe:

```bash
grep -n "variant-code" src/byz/reconcile/compare.py
grep -n "def _report\|README_TEXT\|def diff_pair" src/byz/curate/diff.py
grep -n "variant" src/byz/reconcile/report.py
sed -n '/^01:15/p' data/text/CCAT/05_ACT.TXT
grep -n "01:15" editions/rp2018/source/ccat/AC.CCT
```

## Phase 1 - Classifier rename and one vocabulary (R1)

### 1a. Red

Edit `tests/reconciliation/test_compare.py:6-18`:

- rename `test_classify_variant_code` to `test_classify_apparatus_code` and
  expect `"apparatus-code"` (the ACT 1:15-like fixture
  `"text {C x > y }"` / `"text {N x > y }"` stays);
- add `test_classify_variant_code_is_gone`: the same call is **not**
  `"variant-code"`;
- add `VocabularyTests`:
  - `compare.CATEGORY_MEANINGS` keys, in order, are
    `missing, variant, apparatus-code, capitalization, word-segmentation,
    whitespace, punctuation, accents-breathings, letters`;
  - no result of `classify_diff` over a table of fixtures is outside the keys;
  - `compare.APPARATUS_CODE_NAMES` keys are exactly
    `set(compare.VARIANT_CODE_RE.findall("{N {B {C {M {S {E"))`, i.e.
    `N B C M S E`;
  - `"bad-variant-code"` is not a key (the contract vocabulary is separate).

Run:

```bash
PYTHONPATH=src python3 -m unittest tests.reconciliation.test_compare -v
```

Red reason: `classify_diff` returns `variant-code`; the constants do not exist
(`AttributeError`). Both failures are wanted.

### 1b. Green

In `src/byz/reconcile/compare.py`:

1. After `VARIANT_CODE_RE` (line 14), add the two ordered mappings:

```python
# `data/text/README.md` is the authority for the letters and their witnesses.
APPARATUS_CODE_NAMES = {
    "N": "Nestle-Aland", "B": "Byzantine", "C": "NA27/28",
    "M": "ECM", "S": "NA27", "E": "NA28",
}
# One-line meanings, in the order classify_diff tests them.  "" (identical) is
# deliberately absent: it is not a category value in any output.
CATEGORY_MEANINGS = {
    "missing": "...", "variant": "...", "apparatus-code": "...",
    "capitalization": "...", "word-segmentation": "...", "whitespace": "...",
    "punctuation": "...", "accents-breathings": "...", "letters": "...",
}
```

Use the meanings promised in `requirements.md` R4/README; keep each under about
70 characters so the report table stays readable.

2. In `classify_diff`, change line 51 to `return "apparatus-code"` and update
   the comment at 43-44 to speak of an "apparatus code" change.

Re-run the red command; it must pass. No generator runs yet.

## Phase 2 - Tag change and honest rendering (R2, R3)

### 2a. Red

In `tests/curate/test_diff.py`, append a `TagChangeTests` class after
`ApparatusWordDiffTests` (around line 72):

```python
def test_tag_change_is_reported_in_direction(self):
    self.assertEqual(
        diff.tag_change("x {N a > b }", "x {C a > b }"), "N -> C"
    )
def test_tag_change_deduplicates_repeated_positions(self):
    self.assertEqual(
        diff.tag_change("{N a }{N b }", "{S a }{S b }"), "N -> S"
    )
def test_tag_change_is_empty_when_codes_match(self):
    self.assertEqual(diff.tag_change("x {N a > b }", "x {N a > b }"), "")
def test_tag_change_lists_distinct_changes(self):
    self.assertEqual(
        diff.tag_change("{N a }{B b }", "{C a }{M b }"), "N -> C; B -> M"
    )
```

In `tests/curate/test_integration.py`, next to
`test_diff_has_unicode_first_examples` (307-345), add assertions against the
*committed* report (they fail until Phase 5 regenerates it):

- ``### ACT 1:15 · `apparatus-code` `` in
  `reports/diffs/rp2018--rp2018-2023/report.md`;
- the entry between that heading and the next `"\n"` heading contains
  ``Apparatus code: `N` -> `C` (the reading is unchanged)``,
  `Text (derived; typographic only, not part of the source-tier change):`,
  `Source (Beta code):`, `Apparatus (Unicode):`, and
  `[-{NA-]{+{NA27/28+}`;
- the apparatus-only entry ``- `ACT 1:10` · `apparatus-code` `` is followed by
  ``  - Apparatus code: `N` -> `C` (the reading is unchanged)`` then
  `  - Apparatus (Unicode): ` then `  - Apparatus (Beta code): `;
- the `1CO 3:14` `variant` entry in `rp2005--rp2018` has **no**
  `Apparatus code:` line, so a reading change is not mislabelled;
- the report contains
  `## Main-text changes (derived text differs)` and the section lead.

Run:

```bash
PYTHONPATH=src python3 -m unittest tests.curate.test_diff -v
PYTHONPATH=src python3 -m unittest tests.curate.test_integration -v
```

Red reason: `diff.tag_change` does not exist; the committed report still says
`variant-code` and has no tag line.

### 2b. Green

In `src/byz/curate/diff.py`:

1. Add `CATEGORY_EXAMPLES` and the helper after `DERIVED_ONLY_TEXT`
   (lines 53-66). `CATEGORY_EXAMPLES` maps category -> `(pair, book, chapter,
   verse)` for exactly the rows verified in `requirements.md`:

```python
CATEGORY_EXAMPLES = {
    "variant": ("rp2005--rp2018", "1CO", 3, 14),
    "apparatus-code": ("rp2018--rp2018-2023", "ACT", 1, 15),
    "capitalization": ("rp2005--rp2005-2019", "MAT", 22, 37),
    "word-segmentation": ("rp2005--rp2005-2019", "1CO", 7, 5),
    "punctuation": ("rp2005-2019--rp2018", "MAT", 1, 18),
    "accents-breathings": ("rp2005--rp2005-2019", "MAT", 27, 13),
    "letters": ("rp2005--rp2018", "JOH", 18, 11),
}
```

2. Add `tag_change(left, right)`:

```python
def tag_change(left: str, right: str) -> str:
    left_codes = compare.VARIANT_CODE_RE.findall(left)
    right_codes = compare.VARIANT_CODE_RE.findall(right)
    if left_codes == right_codes:
        return ""
    if len(left_codes) != len(right_codes):
        return f"{','.join(left_codes)} -> {','.join(right_codes)}"
    pairs = [f"{a} -> {b}" for a, b in zip(left_codes, right_codes) if a != b]
    return "; ".join(dict.fromkeys(pairs))
```

`dict.fromkeys` preserves left-to-right order and deduplicates, which is the
one two-position `N -> S` row in `rp2018--rp2018-2023`.

3. Change `_report` (339-521):

   - **Category table (423-429):** header
     `"| Category | Meaning | Count |"` / `"| --- | --- | ---: |"`; each row
     ``f"| `{category}` | {compare.CATEGORY_MEANINGS[category]} | {count} |"``.
     After the table add a sentence naming `../README.md#categories` as the
     glossary (definitions and worked examples). A missing meaning is a loud
     `KeyError`, not a blank cell.
   - **Main-text section (442-459):** heading
     `"## Main-text changes (derived text differs)"`; add the lead sentence
     from R3.1. In the loop, when `row["category"] == "apparatus-code"`:
     print the tag line, use the derived Text label, and after the
     `Source (Beta code)` block print an `Apparatus (Unicode):` block with
     `row["apparatus_word_diff"]`. Other entries keep `Text:` exactly.
   - **Apparatus-only section (461-494):** add the lead sentence from R3.2;
     for `row["category"] == "apparatus-code"` append the tag line before the
     Unicode sub-item. Keep the existing formatting-only suffix and the
     encoding-only sentence unchanged.

4. Do not add a CSV column. `CSV_FIELDS` (37-51) and `_write_changes` (293-302)
   stay as they are.

Re-run the red commands; the `test_diff` tag tests pass. The integration tests
still fail until Phase 5 regenerates the committed reports.

## Phase 3 - Generated README glossary (R4)

### 3a. Red

In `tests/curate/test_diff.py`, add `ReadmeCategoryTests`:

- `"## Categories"` in `diff.README_TEXT`;
- every key of `compare.CATEGORY_MEANINGS` appears as `` `name` `` in the table;
- the table order equals `list(compare.CATEGORY_MEANINGS)`;
- `"ACT 1:15"`, `"1CO 3:14"`, and the rendered tag line text, plus
  `"the reading is unchanged"`, appear;
- `"The classifier applies these tests in order"` (or the final precedence
  sentence) appears;
- `"variant-code"` does **not** appear in `diff.README_TEXT`;
- the apparatus-code names sentence contains all six witness names.

In `tests/curate/test_integration.py`, extend
`test_readme_is_generated_from_the_module_constant` (527-545) so the committed
`reports/diffs/README.md` equals `generated.markdown(diff.README_TEXT)` after
regeneration (the existing equality already enforces this; add the category
assertions against the committed file).

Red reason: `README_TEXT` has no `## Categories`; the old name is still in the
committed file until Phase 5.

### 3b. Green

In `README_TEXT` (524-630):

1. Insert a `## Categories` section after `## Notation` (or before
   ``## The `derived.diff` caveat``). It contains the precedence sentence, the
   table, the `variant` vs `apparatus-code` paragraph, and the apparatus-code
   names sentence. Use two placeholders like the existing
   `__DERIVED_ONLY_NOTE__`:
   `__CATEGORY_GLOSSARY__` and `__APPARATUS_CODE_NAMES__`.
2. Add small builders next to `derived_only_lines()`:

   - `_category_glossary()` renders the nine rows from
     `compare.CATEGORY_MEANINGS` + `CATEGORY_EXAMPLES`, with the example cell
     `` `BOOK C:V` in `pair` `` and `none in the current reports` for
     `missing`/`whitespace`;
   - `_apparatus_code_names()` renders
     "`N` Nestle-Aland; `B` Byzantine; ..." from
     `compare.APPARATUS_CODE_NAMES`.
3. Replace the placeholders at module import, next to the existing
   `README_TEXT.replace("__DERIVED_ONLY_NOTE__", ...)` (628-630), so
   `diff.README_TEXT` stays the single final string that `write_readme()` writes.
4. Update the `report.md` and `changes.csv` bullets in `## Files` for the tag
   line, the Meaning column, and the derived-text label.

Re-run the tests; the README tests pass at module level, and the committed-file
assertion passes after Phase 5.

## Phase 4 - Reconciliation report and decision log (R5)

### 4a. Red

In `tests/reconciliation/test_integration.py`, add:

- `_summary`/`_decision_log` text assertions: R2 contains
  ``category `apparatus-code` `` and not `variant-code`; the summary names both
  apparatus categories (e.g. "reading changes" and "code-only").
- a vocabulary assertion over `compare.run()["verses"]`: every `category` is a
  key of `CATEGORY_MEANINGS`.

In `tests/reconciliation/test_offline.py`, extend `CommittedReportTests`
(172-218):

- `decision-log.md` R2 contains `apparatus-code`, not `variant-code`;
- `summary.md` contains the reading/code split and
  `../diffs/README.md#categories`;
- the generated-output rename guard (R7.3), scoped to `reports/`:

```python
for path in sorted((ROOT / "reports").rglob("*")):
    if path.suffix not in {".md", ".csv", ".diff"}:
        continue
    text = path.read_text(encoding="utf-8")
    # `bad-variant-code` is the unrelated source-validator category.
    self.assertNotIn("variant-code", text.replace("bad-variant-code", ""), path)
```

Red reason: the committed reconciliation files still say `variant-code`; the
summary has no split.

### 4b. Green

In `src/byz/reconcile/report.py`:

1. `_summary` (367-389): replace the single `apparatus` sum with
   `apparatus_reading = best_categories.get("variant", 0)` and
   `apparatus_code = best_categories.get("apparatus-code", 0)`; render
   "`T` are apparatus differences (`R` reading, `C` code-only)". Keep the total
   unchanged so `test_headline_totals_are_stable` still passes.
2. Categories table (433-442): add a sentence before the table:
   "Category meanings and worked examples: [`reports/diffs/README.md`](../diffs/README.md#categories)."
   Relative to `reports/reconciliation/summary.md`, `../diffs/README.md`
   resolves.
3. `_decision_log` R2 (484): category `apparatus-code`; evidence
   "e.g. `C` vs `N` in Acts (`apparatus-code`: the tag differs, the reading does
   not)". Keep `pending`.

## Phase 5 - Regenerate and close the red tests

1. Run the diff generator and the reconciliation generator:

```bash
PYTHONPATH=src python3 -m byz.diff
PYTHONPATH=src python3 -m byz.reconcile
```

2. Inspect the ACT 1:15 entry before running the full suite:

```bash
sed -n '/### ACT 1:15/,/^### /p' reports/diffs/rp2018--rp2018-2023/report.md
sed -n '/- `ACT 1:10`/,/^- `/p' reports/diffs/rp2018--rp2018-2023/report.md
```

Expected ACT 1:15: the `apparatus-code` heading, the tag line, the derived Text
label, the Text block with `[-εἶπεν --]{+εἶπεν-+}`, the Source block with
`[-{N-]{+{C+}`, and an Apparatus (Unicode) block with
`[-{NA-]{+{NA27/28+}`. Expected ACT 1:10: tag line, Unicode line, Beta line.

3. Count the tag lines and values:

```bash
grep -c "Apparatus code: " reports/diffs/rp2018--rp2018-2023/report.md   # 45
grep -o "Apparatus code: \`[NBCMSE]\` -> \`[NBCMSE]\`" reports/diffs/rp2018--rp2018-2023/report.md | sort | uniq -c
```

Expected: `29 N -> C`, `16 N -> S` (`2PE 2:6` deduplicates two positions to
one line; see `validation.md` §10.5).

4. Confirm no old value remains:

```bash
grep -rn "variant-code" reports/ | grep -v bad-variant-code || echo clean
grep -n "apparatus-code" reports/reconciliation/categories.csv reports/reconciliation/decision-log.md
```

5. Run the full suites (Phase 6 covers the complete sequence).

## Phase 6 - Documentation and the complete regeneration

1. Add the `2026-11-21` section at the top of `docs/RELEASE-NOTES.md`
   (hand-written): old value, new value, which generated files carry it, no
   alias, why (`variant` = reading, `apparatus-code` = label), and the migration
   instruction for consumers. Link the diff README with a relative link
   (`../reports/diffs/README.md`) so the existing relative-link test covers it.
2. In `src/byz/curate/docs.py`, inside `write_editions_doc`'s "Successive
   diffs" bullets (around 400-470), add one sentence after the `derived.diff`
   bullet: "Category names, with worked examples, are defined in
   [`reports/diffs/README.md`](../reports/diffs/README.md#categories)."
3. Run the complete sequence from the repository root:

```bash
PYTHONPATH=src python3 -m byz.fetch --verify
PYTHONPATH=src python3 -m byz.fetch
PYTHONPATH=src python3 -m byz.recover
PYTHONPATH=src python3 -m byz.build
PYTHONPATH=src python3 -m byz.diff
PYTHONPATH=src python3 -m byz.contract
PYTHONPATH=src python3 -m byz.reconcile
```

4. `git status --porcelain -- editions/ data/` must be empty. If not, a
   converter was run unnecessarily or an untracked file was copied into an
   edition; stop and record it in `validation.md` §Deviations.

## Phase 7 - Rename lock and positive guard

1. The guard from Phase 4a is in `tests/reconciliation/test_offline.py`; add the
   sibling in `tests/curate/test_integration.py` over the four diff
   directories (all six files per pair), with the same
   `bad-variant-code` exclusion.
2. Add the positive guard: the ACT 1:15 row in
   `reports/diffs/rp2018--rp2018-2023/changes.csv` has
   `category == "apparatus-code"` and the report has the tag line. A rename
   regression then fails both the negative and the positive test.
3. Add `test_glossary_examples_are_real`: for every `CATEGORY_EXAMPLES` entry,
   read `reports/diffs/<pair>/changes.csv`, find the verse, and assert its
   `category` equals the key. This also proves the examples are not decorative.

## Rejected alternative (record it in the commit message)

Moving every `variant`/`apparatus-code` row into `Apparatus-only changes` by
source-tier category. It would make the section name literal, but it hides the
ACT 1:15 dash difference from `report.md`, changes the pinned counts
(156 -> 157), contradicts the current section definition used by the counters
and tests, and still leaves two `capitalization` rows in a section they do not
match. The chosen presentation keeps both tiers in one entry.

## Ordering and determinism notes

- The glossary order comes from `CATEGORY_MEANINGS`; never iterate a `set`.
- `changes.csv` field order is fixed by `CSV_FIELDS`; do not append a column.
- `reports/baseline/files.csv` changes because it hashes the edited sources;
  that is expected and generated by `byz.contract`, not hand-edited.
- Run `byz.contract` before `byz.reconcile` (both write `docs/HISTORY.md`); see
  `docs/BUILD.md`, "Report generation order".
- The twice-run byte-identity check is in `validation.md`; run it after the
  first green regeneration, before any commit.
