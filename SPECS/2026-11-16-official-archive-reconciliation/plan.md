# Plan - Official archive reconciliation (Cycle 2)

Red/green TDD throughout. The comparison is read-only with respect to the current
corpus; only fetched archives, provenance, and reconciliation reports are added.
The maintainer decides canonical sources (TECH.md §4).

## Task group 1 - Branch, skeleton, and test harness

- [ ] Create branch `feature/2026-11-16-official-archive-reconciliation` off
      `master`.
- [ ] Use the standard library (`hashlib`, `zipfile`, `csv`, `tomllib`,
      `difflib`, `unicodedata`) for the reconciliation tooling. Add a dependency
      only if it is genuinely necessary, and state why.
- [ ] Create `src/byz/reconcile/` with modules: `fetch.py`, `archive.py`,
      `inventory.py`, `normalize.py`, `mapping.py`, `compare.py`, `classify.py`,
      `history.py`, `report.py`.
- [ ] Create `tests/reconciliation/`; write the failing test first for each
      module (RED), then implement (GREEN).

## Task group 2 - Fetch, checksum, and freeze the archives

- [ ] Write `scripts/fetch_official.py` (or a `python -m byz.reconcile fetch`
      entry point). Test it against local fixture zips; the network path is
      isolated and not used in tests.
- [ ] Download each archive with `?dl=1`, following redirects.
- [ ] Record per archive: requested URL, final URL, HTTP status, download date,
      size, SHA-256, and extraction destination.
- [ ] Extract into `data/raw/<edition>/<archive-name>/` without editing contents.
- [ ] Write `data/provenance/rp2005.toml` and `rp2018.toml`.
- [ ] Re-running the fetch against recorded checksums produces no unexpected
      change; a changed hash is recorded and flagged.
- [x] Decided with the maintainer (2026-11-17, open question 6): commit the six
      original zips under `data/raw/_archives/<edition>/` alongside the
      extracted inputs and checksums, for posterity and offline reproducibility.

## Task group 3 - Archive inventory

- [ ] Inventory every member: path, uncompressed size, CRC, SHA-256, encoding,
      line endings, format class.
- [ ] Test encoding/line-ending detection on fixtures (ASCII, UTF-8, BOM,
      Windows-1252, LF, CRLF, mixed).
- [ ] Emit `reports/reconciliation/archives.csv`.

## Task group 4 - File mapping

- [ ] Map `source/CCAT/<NN>_<BOOK>.TXT` to the 2005 and 2018 `ccat` members.
      Account for `04a_PA`, `05a_ACT24`, and any naming differences.
- [ ] Map `source/Strongs/*.BP5` against plausible parsed members; if none, mark
      `provenance-unknown`.
- [ ] Map each CSV view and TEI file to its reconstructed official counterpart at
      the text level.
- [ ] Test mapping on fixtures with missing, extra, and renamed files.
- [ ] Never drop an unmapped file; record it with a reason.

## Task group 5 - Comparison core

- [ ] Implement raw comparison (byte hashes) and normalized comparison.
      Normalization is explicit: encoding decode, line-ending normalization,
      trailing whitespace, Unicode NFC. Never normalize away letters, accents,
      punctuation, variants, or parsing.
- [ ] Test each normalization independently and prove a textual difference
      survives normalization.
- [ ] Implement file-level, line-level, verse-level, and word-level comparison
      with stable ordering.
- [ ] Implement the classifier categories from `requirements.md` §R4/R8 and test
      every category on fixtures (letters, accents/breathings, punctuation,
      capitalization, variants, parsing, Strong's, numbering, encoding/EOL, NFC,
      whitespace).
- [ ] Keep raw and normalized results in separate columns/rows.

## Task group 6 - Source-tier reconciliation

- [ ] Compare `source/CCAT` against both `ccat` archives: raw, normalized,
      verse-level, word-level.
- [ ] Compare `source/Strongs` against any plausible official parsed files, or
      record `provenance-unknown`.
- [ ] Produce a match matrix and one-paragraph verdict per edition:
      "current source/CCAT vs official rp2018 ccat: X/Y files exact, N verses
      differ, categories ..., overall ...".
- [ ] Add a golden test on one Gospel that locks the comparison output.

## Task group 7 - Derived-tier reconciliation (best-effort)

- [ ] Compare `csv-unicode/**` and `tei-xml-unicode/**` against text reconstructed
      from the `ascii`, `preformatted`, and `ccat` archives.
- [ ] Where an exact comparison needs the Cycle 3 parser, classify as
      `incomparable-pending-pipeline` with a specific reason; do not guess.
- [ ] At minimum, verify book coverage, verse counts, CSV shape, and TEI
      well-formedness against the reconstructed official text.
- [ ] Record which derived files are confirmed and which await Cycle 3.

## Task group 8 - Strong's provenance

- [ ] Search every archive for parsing/Strong's-like content.
- [ ] If found, map and compare; if not, record `provenance-unknown` with the
      evidence (names, encodings, git history) and a decision-log row.
- [ ] Do not infer provenance from file-name similarity alone.

## Task group 9 - Edition/revision determination and external history

- [ ] Decide `rp2018` vs `rp2018@2023-07-20` from the evidence (D3).
- [ ] Confirm the four intentional blanks (LUK 17:36, ACT 8:37, ACT 15:34,
      ACT 24:7) against the official archives (D7).
- [ ] Update `docs/HISTORY.md` with external evidence.
- [ ] Write `docs/PROVENANCE.md` with edition, archive, checksum, and decision
      details.

## Task group 10 - Reports and decision log

- [ ] Generate `reports/reconciliation/{summary.md,archives.csv,files.csv,verses.csv,categories.csv,decision-log.md}`.
- [ ] The decision log lists every conflict with evidence, options, and an empty
      maintainer decision field. Present it to the maintainer and record decisions.
- [ ] Ensure deterministic ordering and no timestamps.

## Task group 11 - Validation and handoff

- [ ] Run the full comparison twice and prove identical reports (hash them).
- [ ] Confirm `git status` shows no changes under `source/`, `csv-unicode/`,
      `tei-xml-unicode/`, or `essay/`.
- [ ] Run the test suite; all green.
- [ ] Walk `validation.md` item by item.
- [ ] Present the match matrix, verdicts, and decision log to the maintainer.
- [ ] Do not commit the spec/reports without the user's instruction; leave them
      for review.

## Suggested commands

```bash
# fetch and checksum (network)
python3 scripts/fetch_official.py --verify

# compare and report (offline; stdlib)
PYTHONPATH=src python3 -m byz.reconcile

# tests (offline)
PYTHONPATH=src python3 -m unittest discover -s tests/reconciliation -v
```

## Guardrails

- The current `source/`, `csv-unicode/`, `tei-xml-unicode/`, and `essay/` files
  are read-only inputs to this cycle.
- A mismatch is a finding, not permission to edit.
- If an official file should replace a current file, that is a separate approved
  change after this cycle.
