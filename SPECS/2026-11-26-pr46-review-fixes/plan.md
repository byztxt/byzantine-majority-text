# Plan - PR #46 review fixes

## 1. Bug investigation (investigate-bug skill)

Three defect classes were investigated before patching. The source tree was
unchanged throughout; the defects were in the pipeline's guard/transaction
logic and in the inherited converter contract.

### 1.1 Silent book loss in `build_official`

- **H0 - instance / RCA.** `build_official` iterated whatever ASCII files
  existed (`ascii_dir.glob("*_Byz.txt")`), skipped an unmapped code with
  `continue`, and wrote a book's accented views only `if ccat_file.exists()`.
  There was no expected-set check, unlike `build_current` (`_check_source_books`)
  and `build_historical` (`_check_historical_books`). Reproduced in a temporary
  tree containing only `MT`: the build returned success, emitted only `MAT`, and
  `byz.verify` accepted the shrunken manifest as OK.
- **Silence analysis.** `byz.verify` proves a manifest matches the tree it is
  given; it cannot know which books a faithful edition must contain. The build
  was the only layer that could catch it and did not.
- **H1 - narrow radius.** One function (`build_official`), used by both official
  editions (`rp2005`, `rp2018`). The same shape (glob + map + silent skip)
  existed in the diff source loaders (`diff._load_official`,
  `diff._load_historical`, `diff._load_current`) and in
  `reconcile.historical._load_current`. All were hardened; the immutable-tag
  readers in `reconcile.historical` intentionally compare intersections of
  historical tag content and are not edition producers.
- **H2 - category.** Category name: **book silently omitted from a source
  loader**. Signature: `glob(...)` + `dict.get(...)` + `if abbr:`/`continue`.
  Swept `src/byz/curate/build.py`, `src/byz/curate/diff.py`,
  `src/byz/reconcile/historical.py`, and `src/byz/reconcile/compare.py`, and
  checked every official/historical/current source directory. Prevention:
  validate the expected canonical (+section) set at every loader boundary, and
  lock it with a shrunken-tree test.

### 1.2 Non-atomic edition swap

- **H0 - instance / RCA.** `_staging_views` created only the staging tree, so
  `_swap_views` crashed with `FileNotFoundError` when `editions/<id>/` was
  missing. The manifest (and current provenance TOML) were written only after
  both view swaps, so a failure between CSV and TEI left new CSV, old TEI, and
  an old manifest. The rollback comment covered only a failed move inside one
  view.
- **Silence analysis.** There was no transaction boundary and no invariant that
  the five outputs agree. A partial tree is still valid-looking to a later run.
- **H1 - narrow radius.** One swap helper and one caller (`build_all`). The
  `materialise` ingest path does not stage a swap.
- **H2 - category.** Category name: **partially swapped edition directory**.
  Signature: several `os.replace`/`rename` calls with no shared backup/rollback.
  Prevention: stage every output (views, manifest, README, provenance), swap as
  a list, keep backups, roll back in reverse, and test a failure after the first
  view.

### 1.3 Dropped Strong's numbers in `strongs/no-parsing`

- **H0 - instance / RCA.** `convert_beta_to_unicode_strongs(beta,
  drop_parsing=True)` skipped both digit tokens and `{...}` tokens. The boolean
  name claimed "drop parsing" but the code dropped the numbers too, so
  `csv/strongs/no-parsing` was byte-identical to `csv/unaccented` (27/27 files
  in both released editions; inherited from `master`).
- **Silence analysis.** The two outputs were compared to each other and declared
  intentionally equal; no check asserted the intended numbers-only shape, so
  the missing numbers were invisible.
- **H1 - narrow radius.** `parse_bp5_strongs` and `parse_parsed_ub5` in
  `build.py`, plus the converter. Both parsers returned only two shapes and
  reused the plain-text result for `strongs/no-parsing`.
- **H2 - category.** Category name: **Strong's numbers dropped from a view**.
  Signature: a boolean `drop_parsing` / reuse of the plain-text dict for the
  numbers-only path. Swept `src/byz/beta/converter.py`, `src/byz/curate/build.py`,
  all five CSV views in both released editions, both TEI views, and the contract
  validators. Prevention: explicit conversion modes, three golden shapes, and a
  contract validator that rejects braces in numbers-only and digits/braces in
  unaccented.

## 2. Implementation tasks

1. **Converter API.** Replace `drop_parsing` with
   `STRONGS_WITH_PARSING` / `STRONGS_NUMBERS_ONLY` / `STRONGS_PLAIN_TEXT`; raise
   on an unknown mode. Add golden tests.
2. **Parsers.** `parse_bp5_strongs` and `parse_parsed_ub5` return
   `(with_parsing, numbers_only, plain_text)`. `_parse_ub5_text` emits the
   numbers-only shape by dropping morphology tokens. `build_historical` and
   `build_current` write `strongs/no-parsing` from numbers-only and
   `unaccented`/unaccented TEI from plain text. `parse_parsed_ub5` raises on an
   unmatched `(chapter:verse)` segment and on a segment with no reference.
3. **Official guard.** Add `_official_source_maps`, check the exact ASCII/CCAT
   sets, handle `GREEK.CCT` explicitly, and raise for unknown/duplicate/missing
   books. Add the shrunken-tree and byte-identity tests.
4. **Atomic swap.** `_staging_views` creates the final directory. `write_manifest`
   accepts a staging root and staged provenance path. `_swap_outputs` stages
   views + manifest + README + provenance and rolls back in reverse. Add the
   missing-directory and mid-swap tests.
5. **Title fix.** Delete `LEGACY_UNACCENTED_BOOK_NAMES`; use
   `editions.BOOK_NAMES` for every TEI. Update docs/tests and regenerate.
6. **Contract.** Add `csv/unaccented` to paths, contracts, inventory, coverage,
   invariants, and derivation. Change the TEI derivation to `csv/unaccented`.
   Add shape validators for unaccented/numbers-only. Update D2/D3 and the summary.
7. **Documentation generators.** Fix the diff blank-verse paragraph, reconciliation
   capitalization sentence, contract summary/decision log, docs/EDITIONS
   unaccented/title/cross-reference text, data/README generated-file claim, and
   BUILD/README tag/metadata wording.
8. **Specs.** Fix TECH.md and ROADMAP.md; add the dated superseded note to the
   Cycle 3 validation.
9. **Hygiene.** Move the untracked-file test to a temporary git repo, derive the
   reconciliation Strong's assertion from the code path, assert 6816/666, and
   add the remaining guard tests.
10. **Regenerate** in order: build, diff, contract, reconcile, verify; then run
    the three test suites.

## 3. Validation gates

- `byz.verify` reports 226 inputs / 672 artifacts.
- The three suites pass.
- Only the approved title fix, numbers-only CSVs, and docs/manifests change.
- The official source text and `csv/unaccented`/unaccented TEI bytes do not
  change.
