# Requirements - PR #46 review fixes

**Date:** 2026-11-26
**Branch:** `feature/2026-11-16-edition-recovery-curation` (PR #46)
**Source:** `/tmp/opencode/pr46-review.md` plus two explicit maintainer
decisions (A and B below).

This round closes the blocking and non-blocking items from the maintainer's
review. It is a bug-fix and record-accuracy round: the source text under
`data/raw/repo/rp2018-2023/{ccat,strongs}/`, the official print extracts, and
the committed archives are unchanged. One documentation typo in
`data/raw/repo/CONVENTIONS.md` (2P -> 2R) is corrected; it is not source text.

## Maintainer decisions beyond the review

**A. Fix the inherited unaccented-TEI title typos.** `rp2018-2023`'s
unaccented TEI carried `Second Timoty` (2TI) and `Phillipians` (PHP) only to
keep old bytes. TEI is derived, so the typos are fixed and the
`LEGACY_UNACCENTED_BOOK_NAMES` workaround is removed. `2TI.xml` and `PHP.xml`
in `editions/rp2018-2023/tei/unaccented/` change; the manifest hashes follow.

**B. `csv/strongs/no-parsing` is a real numbers-only view.** In both released
editions (`rp2005-2019`, `rp2018-2023`) it must keep the word and the Strong's
number(s) and drop the `{...}` morphology. `csv/unaccented` stays plain text
(no numbers, no parsing) and the unaccented TEI keeps using that plain text, so
the unaccented TEI bytes do not change. This is an approved data change: the 27
`strongs/no-parsing` CSVs per released edition and their manifest hashes/docs
change. `rp2005-2019` therefore no longer matches `v2.0.3` for those files.
The converter API uses explicit modes (`with-parsing`, `numbers-only`,
`plain-text`), not the misleading boolean `drop_parsing`.

## Blocking items

1. **Official book-set guard.** `build_official` must validate the source book
   set loudly: ASCII exactly the 27 canonical books; CCAT exactly the canonical
   27 plus `PA` and `ACT24`, with `GREEK.CCT` handled explicitly as alphabet
   notes. Unknown, duplicate, or missing books raise. A shrunken official tree
   (the reviewer's "only MT" reproduction) must fail, and the committed official
   outputs must stay byte-identical.
2. **Atomic per-edition swap.** Create `editions/<id>/` before swapping.
   Stage and swap `csv/`, `tei/`, `manifest.json`, `README.md`, and (for the
   current edition) the provenance TOML as one transaction, with rollback after
   any failure. A missing edition directory must be rebuilt, and a failure after
   the first view swap must restore every previous output.
3. **Fix generated documentation at the generators and regenerate.**
   - `diff.py` README: the four blank verses are present in every view; a
     present-empty verse is not silently equal to an absent verse.
   - `reconcile/report.py`: the summary must account for all 161 `rp2018`
     differences, including the two `capitalization` rows.
   - `contract/report.py`: the current text is the separate curated edition
     `rp2018-2023`; D2/D3 and the summary must say so. Regenerate
     `reports/baseline/`, `reports/reconciliation/`, and `reports/diffs/`.
   - `SPECS/2026-11-16-edition-recovery-curation/validation.md`: add a dated
     "superseded 2026-11-26" note with the current truth (blank rows present;
     accented-view typography differs). Do not silently rewrite history.
   - `SPECS/TECH.md`: fix retired paths, the four-edition/tag model, the
     `reports/diffs` path and real `changes.csv` schema, and mark CI,
     TEI-RelaxNG, and apparatus items as planned/target.
   - `SPECS/ROADMAP.md`: update Cycle 2 and Cycle 3 status.
4. **Do not touch the stale PR description.** The build agent rewrites it after
   this round.

## Non-blocking items

- Correct the misleading `strongs/no-parsing` prose in the build docstrings,
  `EXPORT_NOTES`, both released edition READMEs, `docs/EDITIONS.md`,
  `docs/DATA_CONTRACT.md`, and the contract/inventory/coverage datasets. Add
  `csv/unaccented` as a first-class validated dataset and document that it is
  plain text, distinct from `strongs/no-parsing`.
- Remove silent fallbacks: `parse_parsed_ub5` raises on an unmatched
  `(chapter:verse)` segment; `_last_commit` raises on empty output; a test
  compares the hardcoded `v2.0.3` commit with `git rev-parse v2.0.3^{commit}`;
  `docs._manifests` raises on a missing manifest; `verify_pdf` reports an error
  when `pdf` is set without `pdf_sha256`; `write_accented_tei` whitelists
  `paths.SECTION_ABBRS` and raises on any other unknown CSV stem.
- Test hygiene: no test writes into the real data tree; the reconciliation
  Strong's test derives from the same code path; add a mid-swap staging test;
  assert the recorded 6816/666 NA/Byz counts.
- `GREEK.CCT` handling is explicit and documented as alphabet notes, with a
  comment/test.
- Smaller fixes: explicit UTF-8 on locale-default reads, `as_posix()` in
  `_hash_tree`, `docs/BUILD.md` tag wording, `data/README.md` generated-file
  claim, CONVENTIONS 2R typo, `docs/EDITIONS.md` cross-reference.
- Document that `byz.build` needs a git checkout with tags and embeds input
  last-commit metadata (a squash/rebase requires metadata regeneration).
- Governance: this spec maps every item to code, tests, and regenerated output,
  and records the bug RCA and H1/H2 category sweeps.

## Out of scope

- No change to official source text or to the official print archives.
- No new edition, no apparatus TEI, no CI workflow, no TEI RelaxNG validation.
- The PR description is left untouched.
