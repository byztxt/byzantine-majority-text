---
name: write-tests
description: Guide for writing verification checks and tests in byzantine-majority-text. Invoke whenever you add or modify a test, or a script that validates the Unicode CSV/TEI-XML conversion output.
---

# Write Tests

This skill guides verification in `byzantine-majority-text`, the public-domain
repository of the Robinson-Pierpont Byzantine Textform Greek New Testament.
**Invoke it every time you write, extend, or modify a test or a validation
check.**

This repository has **no linter and no build system**; verification is the
`unittest` suites under `tests/`. The source files under `data/raw/repo/rp2018-2023/ccat/` and
`data/raw/repo/rp2018-2023/strongs/` are authoritative, and the `python3 -m byz.<verb>` modules
generate the Unicode CSV and TEI-XML derivatives. Tests here should protect that
pipeline: correct conversion, complete book coverage, and stable, well-formed
output.

Before adding a test framework or dependency, ask the user. Prefer checks that run
with the standard library (`python3 -m unittest`) or a small script over new
tooling.

---

## 1. Red/Green

1. **RED - write a failing check first.** Express the desired behaviour (an exact
   Unicode string, a parsing code, a verse count, valid XML). Run it and confirm
   it fails for the right reason, not because of a missing import or a stale
   generated file.
2. **GREEN - fix the script (or, with approval, the source data).** Make the
   smallest change that satisfies the check.
3. **REFACTOR - clean up** while keeping the check green, then re-run the
   affected converter(s).

If the change is in a generated file, fix the generator, never the output.

---

## 2. Cover the happy path

Every change needs a check proving the primary behaviour works on a real input.
Prefer the **real source files and real converter output** over hand-built stubs:
a stub cannot catch source drift.

- Assert the observable result: the exact Unicode text, the CSV columns, the
  TEI-XML structure, the book/verse counts.
- For a converter change, re-run the converter and assert on the regenerated
  file, not on intermediate state.

---

## 3. Cover the edge cases

This project's real edge cases:

- **Beta-code quirks** - `+/` versus `/+` (dialytika + tonos/varia), apostrophes,
  final sigma before a dash or bracket (`S-`, `S]`), and the ` = ` workaround for
  issue #33.
- **Variants** - text inside `{...}` must be dropped for the no-variants outputs
  and kept for the with-variants outputs; variant codes N/B/C/M/S/E must be
  preserved and rendered correctly.
- **Parsing and Strong's** - words with two parsings and two Strong's numbers
  (e.g. James 4:5, 2 Timothy 2:6) must keep both in `with-parsing` and appear once
  in `no-parsing`/TEI. In `no-parsing`, distinct alternative numbers stay
  (2TI 2:6 `4412 4413`), while consecutive identical numbers for one word
  collapse to one (`3588 3588` -> `3588`, 2026-11-26).
- **Book coverage** - every book in `book_dict` is produced exactly once,
  including `04a_PA` and `05a_ACT24`, which have no Strong's equivalent.
- **Format integrity** - CSVs parse, have the expected `chapter,verse,text`
  columns, and integer chapter/verse; TEI-XML is well-formed and uses the
  documented `ab`/`w` structure.
- **Empty/short input** - a blank line, a verse with no words, or a section
  heading must not crash the converter or emit an empty row.

For each edge case, either add a check or state explicitly why it is out of
scope.

---

## 4. Test behaviour, not implementation

Assert what the converter produces (the output file's contents), not which
private helper was called. This keeps checks stable across refactors.

- Prefer asserting the exact Unicode string for a known verse and the presence of
  its parsing/Strong's data.
- Prefer asserting the generated file set and counts over internal data
  structures.
- Do not depend on third-party library internals or on dict ordering.

---

## 5. Naming and structure

- Name checks for the behaviour: `test_final_sigma_before_dash_is_not_medial`,
  `test_multiparsing_word_keeps_both_strongs_numbers`.
- Group related checks by build stage (`test_parse_bp5_strongs`,
  `test_parse_cct_accented`, `test_beta_standardisation`).
- Keep each check focused on one behaviour.
- Do not delete existing checks unless replaced by a stronger one.

The suites already exist; add to the matching one instead of creating a new test
framework:

- `tests/curate/test_build.py` - Beta-code helpers and the parsers.
- `tests/curate/test_current_pipeline.py` - the byte-identity gate for
  `rp2018-2023` and the identity/deletion locks.
- `tests/curate/test_fidelity.py` - CSV/TEI content and well-formedness.
- `tests/contract/` - inventory, dataset names, and coverage.

---

## 6. Category lock-in (bug-fixing checks)

When you write checks for a bug fix, in addition to the reported instance:

- Add a check per **sibling instance** found in the investigate-bug sweeps.
- Add a check asserting the **prevention mechanism actually fires** (the
  converter raises on an unknown input, the output checker fails on a mismatch).
- Add a **book-coverage** check when the bug was an omitted or duplicated book.

This ensures the class of bug cannot silently recur, not just the one instance.
