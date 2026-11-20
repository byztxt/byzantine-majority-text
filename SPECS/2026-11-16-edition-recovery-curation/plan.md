# Plan - Edition recovery, curation & successive diffs (Cycle 3)

Red/green TDD throughout. This cycle adds curated outputs; it does not modify
`source/`, `csv-unicode/`, `tei-xml-unicode/`, `essay/`, or `data/raw/`.

## Task group 1 - Branch, skeleton, and tests

- [ ] Create branch `feature/2026-11-16-edition-recovery-curation` (off the
      branch that contains the Cycle 2 work, or off `master` once Cycle 2 is
      merged).
- [ ] Create `src/byz/curate/` with modules: `editions.py` (registry),
      `recover.py`, `build.py`, `diff.py`, `manifest.py`, `report.py`.
- [ ] Create `tests/curate/`; write the failing test first for each module.
- [ ] Define the edition registry (`editions/rp*.json` or a single
      `editions/registry.toml`) with the fields from `requirements.md` R1.

## Task group 2 - Terminology, metadata, and release numbers

- [ ] Implement a git helper that reads tags and returns the release range and
      latest release for `rp2005-2019` and `rp2018-2023`.
- [ ] Test the helper against fixture data and the real repo.
- [ ] Record: `rp2005-2019` = `v1.0.0`-`v2.0.3`; `rp2018-2023` =
      `v3.0.0`-`v3.3.4` (and future tags).
- [ ] Ensure the registry distinguishes official vs released explicitly.

## Task group 3 - Recover `rp2005-2019` from git

- [ ] Recover `textonly-beta-code/*.CCT` and `parsed/*.UB5` from `v2.0.3`.
- [ ] Write each file into `editions/rp2005-2019/source/` unchanged.
- [ ] Record the tag, commit, path, and SHA-256 for every recovered file.
- [ ] Compare the recovered text to the official 2005 and 2018 archives; record
      the known baseline (99.32% vs 2005, 99.96% vs 2018) in the manifest.
- [ ] Label the edition "2019 repo revision of the 2005 lineage" everywhere.
- [ ] Test that recovered hashes match the git blobs.

## Task group 4 - Freeze the official editions

- [ ] Download and verify the official PDFs; store them under
      `data/raw/<edition>/official-pdf/` and record URL, publisher, page count,
      size, and SHA-256 in `data/provenance/pdfs.toml`.
- [ ] Commit the PDFs (maintainer decision; they are the ultimate source of
      truth and should be in git).
- [ ] Copy `data/raw/rp2005/editions-rp2-ccat` into
      `editions/rp2005/source/` unchanged.
- [ ] Copy `data/raw/rp2018/rp2018-ccat` into
      `editions/rp2018/source/` unchanged.
- [ ] Retain the ASCII/preformatted archives as cross-check material (either in
      the edition directory or referenced by manifest; do not duplicate
      unnecessarily).
- [ ] Record archive URL, archive SHA-256, extraction date, and per-file hashes.
- [ ] Test byte-for-byte equality with the official inputs.

## Task group 5 - Freeze `rp2018-2023`

- [ ] Decide current tree vs latest release `v3.3.4` (recommendation: current
      tree), and record the choice.
- [ ] Copy `source/CCAT` and `source/Strongs` into
      `editions/rp2018-2023/source/` unchanged.
- [ ] Record first release `v3.0.0`, latest release, and the 2023/2026 basis.
- [ ] Test byte-for-byte equality with the chosen source.

## Task group 6 - Build CSV and TEI for every edition

- [ ] Implement a faithful parser for official `.CCT` and ASCII inputs. Do not
      reuse the reconciliation normalizer as a production converter.
- [ ] Parameterize the existing CSV/TEI logic by input/output paths and edition
      source format.
- [ ] For `rp2005-2019`, use the historical converter at `v2.0.3` or port it;
      document the choice.
- [ ] Generate CSV views and TEI main text for all four editions.
- [ ] Add a golden pericope test per edition and a determinism test.
- [ ] Write `manifest.json` per edition with per-file hashes and the generation
      command.

## Task group 7 - Successive diffs

- [ ] Build a verse-aligned diff over the edition main text; add word-level
      detail where possible.
- [ ] Categorize changes: letters, accents/breathings, punctuation,
      capitalization, variants/apparatus, parsing, Strong's, word segmentation,
      encoding/EOL, other.
- [ ] Generate the four reports:
      `rp2005--rp2005-2019`, `rp2005-2019--rp2018`, `rp2018--rp2018-2023`,
      `rp2005--rp2018`.
- [ ] Each report has `report.md` and `changes.csv`, with counts and examples.
- [ ] Test categorization on fixtures and on known changes.
- [ ] Ensure deterministic ordering and no timestamps.

## Task group 8 - Documentation

- [ ] Write `docs/EDITIONS.md` with the official/released table, release
      numbers, provenance, checksums, PDF links, and the history explanation.
- [ ] Update the root `README.md` with an "Editions" section and links.
- [ ] Write `editions/<id>/README.md` for each edition.
- [ ] Update `scripts/README.md` with the recovery/build/diff commands.
- [ ] Update `source/README.md`, `csv-unicode/README.md`, and
      `tei-xml-unicode/README.md` to point to the curated editions and explain
      the working-tree vs archive distinction.
- [ ] Explain the messy history: 2005 lineage in tags, 2019 revision, 2023
      switch, current tree is 2018+2023.

## Task group 9 - Scripts

- [ ] `scripts/recover_editions.py` - recover historical editions from tags.
- [ ] `scripts/build_editions.py` - generate CSV/TEI/manifests for all editions.
- [ ] `scripts/diff_editions.py` - generate successive diffs.
- [ ] Thin wrappers only; logic lives in `src/byz/curate/`.
- [ ] Document exact commands and expected outputs.

## Task group 10 - Validation and handoff

- [ ] Run the build twice and compare manifests and output hashes.
- [ ] Confirm `git status` shows no changes under `source/`,
      `csv-unicode/`, `tei-xml-unicode/`, `essay/`, or `data/raw/`.
- [ ] Run all test suites.
- [ ] Walk `validation.md` item by item.
- [ ] Present `docs/EDITIONS.md`, the manifests, and the diff reports to the
      maintainer.
- [ ] Leave the spec/artifacts for review unless the user asks to commit.

## Suggested commands

```bash
python3 scripts/recover_editions.py
python3 scripts/build_editions.py
python3 scripts/diff_editions.py
PYTHONPATH=src python3 -m unittest discover -s tests/curate -v
```

## Guardrails

- Official inputs and the current working tree are read-only.
- A conversion failure must fail loud with the edition/book/verse.
- Do not collapse the 2005 official and 2005-2019 editions into one label.
- Release numbers come from git tags, not prose.
