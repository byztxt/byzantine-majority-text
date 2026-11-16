# Requirements - Edition recovery, curation & successive diffs (Cycle 3)

## Context

Cycle 2 established two uncomfortable facts:

- The current `source/CCAT` and `source/Strongs` are the **2018 edition with
  2023 adjustments**. They were first added in commit `97371d7` (2023-05-30)
  and released in `v3.0.0` (2023-05-31, PR #25 "update_to_2023").
- The repo's 2005-lineage text exists only in history: `textonly-beta-code` and
  `parsed` at `v2.0.3` and earlier. That text was last updated in 2019, and it
  matches the official 2018 archive in 99.96% of verses and the official 2005
  archive in 99.32%. It is a **2019 revision** of the 2005 edition, not the
  official 2005 print edition.

Users should not have to use `git show` or compare Dropbox zips to understand
what text they are reading. The four historical texts must be recovered,
curated, documented, and made directly downloadable, with their CSV and TEI
exports.

## Terms

- **Official** - published by Dr. Maurice A. Robinson in print (2005, 2018).
- **Released** - published as an artifact in this repository.
- An edition may be official, released, both, or neither. The docs must never
  blur these axes.

The **published PDFs are the ultimate source of truth** (see `TECH.md` §2). The
ZIP archives are machine-readable companions. If an archive or a repository file
disagrees with a PDF, the conflict must be flagged for the maintainer; it must
not be resolved silently.

## Editions in scope

| Edition id | Status | Basis | Repo releases |
| --- | --- | --- | --- |
| `rp2005` | official | Official print 2005; official `.CCT`/ASCII archive | - |
| `rp2005-2019` | released | Repo's 2019 revision of the 2005 lineage; `textonly-beta-code` + `parsed` at `v2.0.3` | `v1.0.0`-`v2.0.3` (latest `v2.0.3`, 2022-12-31) |
| `rp2018` | official | Official print 2018; official `.CCT`/ASCII archive | - |
| `rp2018-2023` | released | Current maintained text: 2018 edition with 2023 adjustments (and later minor fixes) | `v3.0.0`-`v3.3.4` (latest `v3.3.4`, 2026-11-11) |

`rp2005-2019` and `rp2018-2023` are unofficial revisions; the docs must say so
explicitly and give their release numbers. `rp2018-2023` continues to receive
releases; the latest release number must be derivable from git tags and recorded
in its manifest.

Official PDFs:

- `rp2005`: `editions-rp2.pdf` (Chilton Book Publishing, Southborough,
  Massachusetts) -
  <https://byzantinetext.com/wp-content/uploads/2016/11/editions-rp2.pdf>
- `rp2018`: `robinson-pierpont-2018-gnt-edition.pdf` (VTR, Nuremberg) -
  <https://byzantinetext.com/wp-content/uploads/2021/03/robinson-pierpont-2018-gnt-edition.pdf>

These are the ultimate source of truth for the two official editions.

## Goal

Recover, freeze, and curate the four editions into a stable, discoverable
layout; generate CSV and TEI for each; publish clear docs; and provide
reproducible diffs between each successive edition.

## Non-goals

- Creating a new critical edition or adjudicating readings.
- Changing `source/`, the official inputs, or the current maintained text.
- RP2026 (future cycle).
- The TEI apparatus export (later cycle); this cycle produces the main-text TEI.
- Rewriting the final pipeline architecture (Cycle 4); this cycle may refactor
  the existing converters enough to parameterize them.

## Functional requirements

### R1 - Edition metadata and terminology

- Define a single machine-readable edition registry with: id, display name,
  official/released status, basis, source locations, repo release range, latest
  release, and notes.
- Record release numbers from git tags, not guesses.
- Docs must use "official" and "released" exactly as defined above.

### R2 - Recover `rp2005-2019` from git

- Recover the source files from the last pre-2023 release (`v2.0.3`):
  `textonly-beta-code/*.CCT` and `parsed/*.UB5` (or the appropriate parsed
  extension) for all books.
- Record the exact tag, commit hashes, and SHA-256 of every recovered file.
- Compare the recovered text against the official 2005 and 2018 archives and
  record the result (the known baseline: 99.32% vs 2005, 99.96% vs 2018).
- Label it clearly as the **2019 repo revision of the 2005 lineage**, not the
  official 2005 print edition.
- Optional: also preserve `v2016-07-28` as an archival snapshot if the maintainer
  wants it; if not, document why it is omitted.

### R3 - Freeze the official editions

- `rp2005`: use the official PDF (`data/raw/rp2005/official-pdf/editions-rp2.pdf`)
  as the ultimate source of truth, with `data/raw/rp2005/editions-rp2-ccat` as
  the machine-readable companion; retain the ASCII/preformatted archives for
  cross-checking.
- `rp2018`: use the official PDF
  (`data/raw/rp2018/official-pdf/robinson-pierpont-2018-gnt-edition.pdf`) as the
  ultimate source of truth, with `data/raw/rp2018/rp2018-ccat` as the
  machine-readable companion; retain the ASCII/preformatted archives for
  cross-checking.
- Store the PDFs at `data/raw/<edition>/official-pdf/` and record URL, publisher,
  page count, size, and SHA-256 in `data/provenance/pdfs.toml`.
- Copy the source bytes into the edition directory without editing them.
- Record archive URL, SHA-256, extraction date, and file hashes.
- Link the PDFs from `docs/EDITIONS.md` and each official edition's README.
- If an archive or generated output disagrees with the PDF, flag it; do not
  silently choose.
- The official editions have no repo release range; the docs must say so.

### R4 - Freeze `rp2018-2023`

- Use the current `source/CCAT` + `source/Strongs` as the source, or the latest
  release `v3.3.4` if it differs from the working tree; state which was used.
- Record the first release (`v3.0.0`) and the latest release (`v3.3.4` or later).
- Include the 2023 adjustments and later fixes; do not silently call it "the
  2018 print edition".

### R5 - Stable edition layout

```
editions/
  rp2005/
    README.md
    manifest.json
    source/
    csv/
    tei/
  rp2005-2019/
    ...
  rp2018/
    ...
  rp2018-2023/
    ...
```

- Every edition has `README.md`, `manifest.json`, `source/`, `csv/`, `tei/`.
- `manifest.json` records: edition id, status, basis, source provenance, release
  range, generation command, and per-file SHA-256.
- The source files in each edition are immutable; generation writes only to
  `csv/` and `tei/`.

### R6 - Generate CSV and TEI for every edition

- CSV views: with/without variants and with/without parsing where the source
  supports it. At minimum, each edition must have a usable main-text CSV and a
  TEI main-text export.
- TEI: well-formed TEI P5 following the existing IGNTP structure; no apparatus
  in this cycle.
- Generation must be deterministic and documented.
- For official `.CCT`/ASCII input, implement a faithful parser. Do not use the
  reconciliation normalizer as a production converter.
- For `rp2005-2019`, either reuse the historical converter at `v2.0.3` or port
  it; document which, and verify the output against the historical artifacts.
- Tests must include a golden pericope for each edition and a determinism check.

### R7 - Successive edition diffs

- Produce diffs for:
  - `rp2005` -> `rp2005-2019`
  - `rp2005-2019` -> `rp2018`
  - `rp2018` -> `rp2018-2023`
- Also produce `rp2005` -> `rp2018` for the official-to-official view.
- Each diff has a human-readable `report.md` and machine-readable `changes.csv`,
  categorized: letters, accents/breathings, punctuation, capitalization,
  variants/apparatus, parsing, Strong's, word segmentation, encoding/EOL, other.
- Diffs are verse-aligned (and word-aligned where possible), deterministic, and
  documented with counts and examples.
- Do not report encoding/normalization noise as textual change.

### R8 - Documentation and discoverability

- `docs/EDITIONS.md`: the canonical explanation of official vs released, the four
  editions, release numbers, provenance, what each is and is not, how they
  relate, checksums, and where to get them.
- Root `README.md`: an "Editions" section with a table and links to
  `docs/EDITIONS.md` and `editions/`.
- `editions/<id>/README.md`: per-edition summary and generation command.
- `scripts/README.md`: document the recovery, generation, and diff scripts.
- Update `source/README.md`, `csv-unicode/README.md`, and
  `tei-xml-unicode/README.md` to point to the curated editions and explain that
  the top-level folders are the working/current tree, not the archive of all
  editions.
- Explicitly explain the messy history: the 2005 lineage in tags, the 2019
  revision, the 2023 switch, and why the current tree is not 2005.

### R9 - Scripts

- A recovery script (recover historical editions from tags).
- A build/curation script (generate CSV/TEI manifests for all editions).
- A diff script (successive editions).
- Scripts must be runnable from the repo root and documented in
  `scripts/README.md`.
- Scripts must not require network access once the official inputs are committed.

### R10 - Tests and reproducibility

- Red/green TDD for the recovery, generation, and diff tooling.
- Tests for: recovery hashes, official source hashes, golden output per edition,
  determinism, diff categorization, and manifest completeness.
- All tests run offline and are deterministic.
- The curated artifacts are committed (artifacts live in git, per the earlier
  decision).

### R11 - Release numbers

- Docs and manifests must show the repo release range and latest release for
  `rp2005-2019` and `rp2018-2023`, and must state that the official editions
  have no repo release number.
- If git tags change, the docs/manifest generation must pick up the new latest
  release rather than hard-coding an old one.

### R12 - Safety

- Do not modify `source/`, `csv-unicode/`, `tei-xml-unicode/`, `essay/`, or
  `data/raw/` in this cycle.
- Curated editions are new outputs under `editions/`.
- Never silently drop or rewrite a historical reading. If a conversion cannot
  represent something, fail loud and record the limitation.

## Deliverable layout

```
docs/
  EDITIONS.md
editions/
  rp2005/
  rp2005-2019/
  rp2018/
  rp2018-2023/
reports/diffs/
  rp2005--rp2005-2019/
  rp2005-2019--rp2018/
  rp2018--rp2018-2023/
  rp2005--rp2018/
scripts/
  recover_editions.py
  build_editions.py
  diff_editions.py
src/byz/curate/...
tests/curate/...
```

## Acceptance criteria

- All four editions exist in `editions/` with source, CSV, TEI, manifest, and
  README.
- `rp2005-2019` is recovered from `v2.0.3`, with hashes and provenance, and is
  labelled as the 2019 revision of the 2005 lineage.
- The official PDFs are committed, checksummed, and linked from the docs.
- `rp2005` and `rp2018` match their official archive inputs byte-for-byte in the
  source directories, and any PDF/archive conflict is flagged.
- `rp2018-2023` matches the current maintained source (or the stated latest
  release), with release numbers recorded.
- Every edition has deterministic CSV and TEI exports, with golden tests.
- Successive diff reports exist for the four pairs and are categorized and
  deterministic.
- `docs/EDITIONS.md` explains official vs released, the four editions, the
  release numbers, and the history, without requiring git archaeology.
- Root README and script/folder READMEs are updated.
- No source or official input files were modified.
- All tests pass offline.

## Open questions (to resolve with the maintainer)

1. For `rp2005-2019`, use `v2.0.3` only, or also preserve `v2016-07-28` as an
   archival snapshot? Recommendation: `v2.0.3` only, because it is the last
   pre-2023 release; mention `v2016-07-28` in docs.
2. For `rp2018-2023`, use the current working tree or the latest release
   `v3.3.4`? Recommendation: current tree (it is the maintained text), with the
   latest release recorded as `v3.3.4` and future releases appended.
3. Do the official editions get Strong's/parsing exports? The official archives
   do not contain parsed files. Recommendation: main-text CSV/TEI for the
   official editions; do not attach the repo's parsed files to them without a
   clear "provenance-unknown" label.
4. Should `rp2005`/`rp2018` source directories use the official `.CCT` files,
   the ASCII ones, or both? Recommendation: `.CCT` as source, ASCII retained as
   cross-check material.
5. Edition id style: `rp2005-2019` vs `rp2005.2019`. Recommendation:
   `rp2005-2019`, matching the existing hyphenated directory style.
6. Should the successive diffs use the source tier or the generated CSV/TEI?
   Recommendation: both where possible; the user-facing report should be based
   on the main text, with source-level apparatus differences listed separately.

## Risks

- The historical converter may not reproduce the old CSV/TEI exactly; document
  every difference.
- The official `.CCT` parser is the first real pipeline component; it must be
  tested and faithful.
- The repo's 2005 lineage is a 2019 revision; users may still call it "2005".
  The docs must be unambiguous without being confusing.
- Large curated artifacts will increase repository size; manifests and
  determinism checks are mandatory.
