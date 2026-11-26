# Validation - PR #46 review fixes

**Date:** 2026-11-26
**Branch:** `feature/2026-11-16-edition-recovery-curation` (uncommitted working
tree; no commit, push, or merge performed).
**Environment:** Python 3.10.18; `beta-code==1.0.0`; commands run from the
repository root as `PYTHONPATH=src <python3.10> -m byz.<verb>`.

## 1. Bug RCA and H1/H2 sweeps

The three defect classes are recorded in `plan.md` section 1. Summary of what
was swept and locked:

| Class | Instance | H1 siblings fixed | H2 sweep / prevention |
| --- | --- | --- | --- |
| Book silently omitted | `build_official` skipped an unmapped ASCII code and omitted a book with no `.CCT` | `diff._load_official`, `diff._load_historical`, `diff._load_current`, `reconcile.historical._load_current` now raise on unknown/missing books | Swept all source loaders; expected-set validation is the shared prevention; shrunken-tree tests in `test_build.py` and `test_diff.py` |
| Partially swapped edition | `_swap_views` crashed on a missing edition dir and left new CSV + old TEI/manifest | no other output-swap helper exists; `materialise` does not stage a swap | Swept `build.py` and `materialise.py`; staged transaction + reverse rollback; missing-dir and mid-swap tests |
| Strong's numbers dropped | `convert_beta_to_unicode_strongs(drop_parsing=True)` dropped digits and braces, making `strongs/no-parsing` plain text | `parse_bp5_strongs`, `parse_parsed_ub5`, `_parse_ub5_text` | Swept both released editions' 54 CSVs, TEI, and contract validators; explicit modes + three golden shapes + shape validators |

The source text was not edited. `data/raw/repo/CONVENTIONS.md` changed only the
documented `2P` -> `2R` typo.

## 2. Blocking items

### 2.1 Official book-set guard

- `_official_source_maps` requires ASCII exactly the 27 canonical books and
  CCAT exactly those plus `PA`/`ACT24`; `GREEK.CCT` is documented as alphabet
  notes and skipped explicitly. Unknown, duplicate, and missing books raise.
- `tests/curate/test_build.py::OfficialBookSetTests` covers: committed official
  CSV/TEI byte identity for `rp2005` and `rp2018`; the only-`MT` shrunken tree
  failing (no `MAT.csv` written); missing `MAR.CCT`; unknown `ZZ.CCT`; duplicate
  `MT.CCT`/`mt.CCT`; `GREEK.CCT` accepted but not exported.
- `tests/curate/test_diff.py::SourceBookGuardTests` covers the same class in the
  diff loaders.

### 2.2 Atomic per-edition swap

- `_staging_views` creates `editions/<id>/`. `write_manifest` can write into the
  staging root and stage the current provenance TOML. `_swap_outputs` swaps
  `csv`, `tei`, `manifest.json`, `README.md`, and the provenance TOML, with
  backups and reverse rollback.
- `test_build.py::BuildStagingTests` covers a missing edition directory and a
  failure while moving the staged TEI (after the CSV view has already swapped);
  the test asserts the previous CSV, TEI, manifest, and README are restored and
  no `.old` backup remains.

### 2.3 Generated documentation

- `reports/diffs/README.md`: the blank-verse section now says all four verses
  are present empty records in every edition and that present-empty is not equal
  to absent. `test_diff.py::ReadmeCategoryTests` locks the wording.
- `reports/reconciliation/summary.md`: the sentence now includes the 2
  `capitalization` rows, so the named categories total 161 (23 accents + 45
  apparatus-code + 2 capitalization + 2 punctuation + 89 variant).
  `test_reconciliation/test_integration.py` asserts the category counts sum to
  the `rp2018` difference total and the sentence names capitalization.
- `reports/baseline/summary.md` and `decision-log.md` (D2/D3): the current text
  is the separate curated edition `rp2018-2023`, the unaccented TEI comes from
  `csv/unaccented`, and the derivation count is computed rather than hardcoded.
- `SPECS/2026-11-16-edition-recovery-curation/validation.md`: a dated
  "Superseded 2026-11-26" block plus inline notes preserve the historical text
  and state the current truth (blank rows present; accented typography differs).
- `SPECS/TECH.md`: four-edition/tag model, `data/raw/print/<edition>/` paths,
  `reports/diffs/`, the real `changes.csv` schema, and planned/target wording
  for CI, TEI RelaxNG, and apparatus. `SPECS/ROADMAP.md`: Cycle 2 decisions
  R4 resolved / R8 adopted / R9 added, and Cycle 3 status for this round.
- The PR description was not touched.

## 3. Non-blocking items

- `strongs/no-parsing` prose corrected in `build.py` (`EXPORT_NOTES`, docstrings,
  edition READMEs), `docs/EDITIONS.md`, `docs/DATA_CONTRACT.md`,
  `data/raw/repo/CONVENTIONS.md`, and the contract datasets. `csv/unaccented` is
  a first-class dataset in paths, contracts, inventory, coverage, invariants,
  and derivation; the TEI derivation now names `csv/unaccented`.
- The numbers-only view collapses consecutive identical numbers for one word
  and keeps distinct alternatives (`το 3588 3588` -> `το 3588`; 2TI 2:6
  `πρωτον 4412 4413` stays two). The converter and the `.UB5` parser share the
  rule; corpus-wide tests assert no adjacent duplicate remains in either
  released edition and the contract validator rejects one.
- The retired-path table points the old `csv-unicode/strongs/no-parsing` bytes
  at `editions/rp2018-2023/csv/unaccented` and names the new numbers-only view
  separately; `docs/EDITIONS.md` records the 2026-11-26 byte change rather than
  claiming the only change was the apparatus literal.
- Silent fallbacks removed: `parse_parsed_ub5` unmatched segment and a segment
  whose target verse has no parsed line (tests in `test_build.py`);
  `_last_commit` empty output (test); hardcoded `v2.0.3` commit compared with
  `git rev-parse v2.0.3^{commit}` (test); `docs._manifests` missing manifest
  (test); `verify_pdf` with `pdf` but no `pdf_sha256` (test);
  `write_accented_tei` unknown CSV stem (test).
- Test hygiene: `test_data_docs.py` uses a throwaway git repository;
  `test_reconciliation/test_integration.py` asserts the expected Strong's dict
  instead of restating `compare.run()`; the mid-swap test fails at each staged
  pair (TEI, manifest, README, provenance), asserts all five outputs roll back,
  and scans the edition and provenance directories for `.old` leftovers; the
  historical NA/Byz counts assert 6816/666. New tests lock the corrected titles
  and word-for-word `tei/unaccented` == `csv/unaccented` equality (7957 verses
  per release).
- Dead code removed: `write_tei` no longer accepts `book_names`, and
  `_official_source_maps` no longer computes an unreachable `unexpected` set.
- Stale prose annotated/corrected: the 2026-11-19 validations, the
  2026-11-25 inputs requirements, `.opencode/skills/write-tests/SKILL.md`,
  `SPECS/TECH.md` (`generated_by`, not "pipeline version"; converter mode
  strings), and the data/README/BUILD/README wording.
- `GREEK.CCT`: documented as alphabet notes in the print source READMEs and
  build comment; pinned-but-not-exported is tested.
- Smaller: UTF-8 on every `read_text`; `as_posix()` in `_hash_tree` and
  `_artifact_dirs`; BUILD/README tag and squash-metadata wording; data/README
  generated-file claim; CONVENTIONS 2R; EDITIONS cross-reference.
- Build/git coupling note added to `README.md` (template source) and
  `docs/BUILD.md`.

## 4. Regeneration and verification

Commands run from the repository root in this order:

```bash
PYTHONPATH=src $PY310 -m byz.build
PYTHONPATH=src $PY310 -m byz.diff
PYTHONPATH=src $PY310 -m byz.contract
PYTHONPATH=src $PY310 -m byz.reconcile
PYTHONPATH=src $PY310 -m byz.verify
```

Final verify output:

```text
OK rp2005: 56 inputs, 141 artifacts
OK rp2005-2019: 57 inputs, 195 artifacts
OK rp2018: 57 inputs, 141 artifacts
OK rp2018-2023: 56 inputs, 195 artifacts
verified 4 editions (226 inputs, 672 artifacts)
```

Test suites:

| Suite | Tests | Result |
| --- | ---: | --- |
| `tests/contract` | 69 | OK |
| `tests/curate` | 324 | OK |
| `tests/reconciliation` | 85 | OK |

(Previous round: 68 / 313 / 85; original baseline: 64 / 287 / 84.)

## 5. Committed artifacts changed

**(a) Approved unaccented-TEI title fix**

- `editions/rp2018-2023/tei/unaccented/2TI.xml` (`Second Timothy`)
- `editions/rp2018-2023/tei/unaccented/PHP.xml` (`Philippians`)

**(b) Approved numbers-only `csv/strongs/no-parsing` fix**

- 27 files under `editions/rp2005-2019/csv/strongs/no-parsing/`
- 27 files under `editions/rp2018-2023/csv/strongs/no-parsing/`

The numbers-only change left `csv/unaccented/` and the unaccented TEI text
untouched; only the two approved `<title type="work">` lines in `2TI.xml` and
`PHP.xml` changed.

**(c) Docs and manifests**

- Manifests/READMEs: `editions/rp2005-2019/{manifest.json,README.md}`,
  `editions/rp2018-2023/{manifest.json,README.md}`.
- Root/data docs: `README.md`, `data/README.md`,
  `data/raw/print/rp2005/README.md`, `data/raw/print/rp2018/README.md`.
- Docs: `docs/EDITIONS.md`, `docs/DATA_CONTRACT.md`, `docs/PROVENANCE.md`,
  `docs/BUILD.md` (hand-maintained), `data/raw/repo/CONVENTIONS.md`
  (documentation-only update), `.opencode/skills/write-tests/SKILL.md`.
- Reports: `reports/diffs/README.md`; `reports/baseline/{books.csv,
  decision-log.md,derivations.csv,differences.csv,files.csv,summary.md}`;
  `reports/reconciliation/{files.csv,summary.md,verses.csv}`;
  `docs/contract/{contracts.json,editions__rp2018-2023__csv__strongs__no-parsing.json,editions__rp2018-2023__tei__unaccented.json}`
  plus the new `editions__rp2018-2023__csv__unaccented.json`.
- Specs: this folder; the Cycle 3 validation note; the 2026-11-19 validation
  notes; the 2026-11-25 inputs requirement note; `SPECS/TECH.md`;
  `SPECS/ROADMAP.md`.

No other committed artifact changed: the official edition CSV/TEI, the
accented views, the unaccented CSVs, the accented TEI, and the input source
text are unchanged.

## 6. Notes and residual risk

- `byz.build` embeds input last-commit metadata and lists release tags. The
  current working tree is uncommitted, so the recorded commit metadata still
  names the branch head until the build agent commits and reruns the generators;
  this is the documented squash/rebase caveat, not a defect in this round.
- The PR description is intentionally untouched; the build agent rewrites it.
- CI enforcement, TEI RelaxNG validation, and the apparatus TEI remain planned
  targets, not implemented here.
- `GREEK.CCT` remains pinned in the official manifest include but is never
  parsed as a book; the choice is documented and tested.
- The numbers-only duplicate collapse changes the bytes of the same 54 CSVs
  again; no new artifact path appears. Earlier-cycle prose that described the
  two released views as byte-identical aliases is superseded by the dated notes
  listed in section 3.
- No item from this review round was left unaddressed.

## 7. Independent verifier pass - 2026-11-26

Verified the uncommitted working tree on
`feature/2026-11-16-edition-recovery-curation` with Python 3.10.18 and
`beta-code==1.0.0`, from the repository root:

```bash
PYTHONPATH=src $PY310 -m byz.build
PYTHONPATH=src $PY310 -m byz.diff
PYTHONPATH=src $PY310 -m byz.contract
PYTHONPATH=src $PY310 -m byz.reconcile
PYTHONPATH=src $PY310 -m byz.verify
PYTHONPATH=src $PY310 -m byz.fetch --verify
```

- `byz.verify`: `verified 4 editions (226 inputs, 672 artifacts)`, all four
  editions `OK`. `byz.fetch --verify`: `verified 6 archives`.
- A second full build -> diff -> contract -> reconcile run produced no file
  change: a SHA-256 snapshot of the whole working tree before and after the
  second run was identical.
- Tests: **69 contract, 324 curate, 85 reconciliation**, all OK; the suites
  left the working tree unchanged.
- Outputs: in both released editions, every `csv/strongs/no-parsing` row has
  Strong's numbers, no `{...}`, and no adjacent duplicate numbers (0/7957
  occurrences each); its words match `csv/unaccented` word for word.
  `csv/unaccented` has no digits or braces. `tei/unaccented` matches
  `csv/unaccented` for all 7957 verses per edition and keeps the four empty
  `<ab/>` records. Accented CSV/TEI, `csv/strongs/with-parsing`, and
  `csv/unaccented` are byte-identical to `HEAD`; the only TEI changes are the
  two approved title lines, and the official editions are byte-identical to
  `HEAD`.
- Manifests changed only for approved artifacts: 27 CSVs for `rp2005-2019`;
  27 CSVs plus `2TI.xml`/`PHP.xml` for `rp2018-2023`. No manifest metadata key
  changed.
- No official source text, archive, PDF, or provenance TOML changed; no
  staging, `.old`, or `.tmp` files remain.
- Verifier doc fix: `SPECS/ROADMAP.md` still put the Cycle 3 inputs under
  `data/raw/<edition>/` and used `data/raw/rp2026/` plus `reports/diff/` in the
  future plan; corrected to `data/raw/print/<edition>/`, `data/raw/repo/`,
  `data/raw/print/rp2026/`, and `reports/diffs/`. No generated output changed.
