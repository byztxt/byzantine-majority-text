# Requirements - Official archive reconciliation (Cycle 2)

## Context

Cycle 1 established the internal baseline: the current corpus is documented and
machine-validated, the source files are authoritative, and the text is modelled
as `rp2018` with a `2023-07-20` revision (decision D3, still to be confirmed).
Cycle 1 also found that the Strong's/BP5 provenance is unknown and that the four
blank verses (LUK 17:36, ACT 8:37, ACT 15:34, ACT 24:7) are intentionally
absent from the Byzantine tradition (D7).

Now we bring in the official archives and determine, quantitatively, to what
extent the current corpus matches them. This cycle is a reconciliation, not a
rewrite: the source files are not changed without an explicit maintainer
decision.

## Goal

Fetch and checksum every official archive, compare each one with the current
`source/`, `csv-unicode/`, and `tei-xml-unicode/` datasets, classify every
difference, and give the maintainer a clear, evidence-backed answer for each
edition: what matches, what differs, and what should become canonical.

## Non-goals

- Rewriting the converters or building the final pipeline (Cycle 3).
- Reordering the repository folders or defining edition slots (Cycle 4).
- Producing edition-to-edition deltas for users (Cycle 5).
- Producing the TEI apparatus export (Cycle 6).
- Ingesting RP2026 (Cycle 8).
- Changing any source, CSV, or TEI file without an explicit maintainer decision.

## Inputs

### Official archives

Fetch each with `?dl=1`, follow redirects, and record the final URL, HTTP status,
size, download date, and SHA-256.

**2005**

- `editions-rp2-preformatted.zip`
  <https://www.dropbox.com/s/ago0uhvmjndbsy5/editions-rp2-preformatted.zip?dl=0>
- `editions-rp2-ascii.zip`
  <https://www.dropbox.com/s/oil2m3la4vsnbpb/editions-rp2-ascii.zip?dl=0>
- `editions-rp2-ccat.zip`
  <https://www.dropbox.com/s/f3di0cgdflqjwq4/editions-rp2-ccat.zip?dl=0>

**2018**

- `rp2018-ascii.zip`
  <https://www.dropbox.com/s/ug3i36zsvtg39x0/rp2018-ascii.zip?dl=0>
- `rp2018-ascii-one-line-per-verse.zip`
  <https://www.dropbox.com/s/cr592513g0v2imc/rp2018-ascii-one-line-per-verse.zip?dl=0>
- `rp2018-ccat.ZIP`
  <https://www.dropbox.com/s/u47y6wedewv4mv9/rp2018-ccat.ZIP?dl=0>

**2026** - not available in this cycle; see Cycle 8.

### Current corpus

The Cycle 1 baseline and the current tracked files:

- `source/CCAT/*.TXT`, `source/Strongs/*.BP5`
- `csv-unicode/{ccat,strongs}/...`
- `tei-xml-unicode/no-accents/...`
- `docs/DATA_CONTRACT.md`, `docs/HISTORY.md`, `reports/baseline/*`
- `SPECS/2026-11-16-existing-corpus-contract/decisions.md` (D1-D8)

## Definitions

- **Edition**: an officially published state of the text (`rp2005`, `rp2018`).
- **Archive**: one of the official zip files listed above.
- **Comparison unit**: a file, a verse, a word, or a variant/parsing/Strong's
  token.
- **Match classes**:
  - `exact` - byte-identical.
  - `normalized` - identical after documented normalization (encoding, line
    endings, trailing whitespace, Unicode NFC).
  - `textual` - real content difference (letters, accents/breathings,
    punctuation, capitalization, variants, parsing, Strong's).
  - `structural` - different file structure, naming, verse/chapter numbering, or
    section mapping.
  - `missing` - present in the archive but absent from the repo.
  - `extra` - present in the repo but absent from the archive.
  - `incomparable-pending-pipeline` - a faithful comparison needs the Cycle 3
    parser; the reason must be stated.
- **Source tier**: direct comparison of CCAT/BP5 source files.
- **Derived tier**: comparison of generated CSV/TEI against text reconstructed
  from the official ASCII/preformatted/CCAT archives.

## Functional requirements

### R1 - Acquisition and provenance

- Provide a fetch step that downloads all six archives and records per archive:
  requested URL, final URL, HTTP status, download date, byte size, SHA-256, and
  extraction destination.
- Write `data/provenance/rp2005.toml` and `data/provenance/rp2018.toml` per
  `TECH.md` §3.
- Extraction is immutable: never edit an extracted input.
- Commit the extracted inputs under `data/raw/<edition>/` and the six original
  zips under `data/raw/_archives/<edition>/`; their URLs and checksums are
  recorded. Keeping the original zips committed preserves the exact published
  files for posterity and lets the offline tests verify them.
- Re-running the fetch against the recorded checksums must produce no unexpected
  change; a changed hash is recorded and flagged.
- Tests must run offline; only the fetch step uses the network.

### R2 - Archive inventory

- Record every member of every archive: path, uncompressed size, CRC/SHA-256,
  detected encoding, line endings, and format class (CCAT, ASCII, preformatted,
  documentation, other).
- Account for nested directories and naming differences.

### R3 - Mapping

- Build an explicit mapping between archive members and current files, per
  edition and per format.
- Map section files (`04a_PA`, `05a_ACT24`) explicitly; do not assume the
  official archives use the same layout.
- Every archive member and every current file must be mapped or listed as
  unmapped with a reason. Never drop them silently.

### R4 - Match extent (the central deliverable)

For each edition and format, answer quantitatively:

- how many files/books are `exact`, `normalized`, `textual`, `structural`,
  `missing`, `extra`, or `incomparable-pending-pipeline`;
- how many verses are identical, differ, or are absent;
- how many words and variant/parsing/Strong's tokens differ, by category;
- an overall percentage and a one-paragraph plain-language verdict.

Required comparisons:

- **Source tier:** `source/CCAT/*.TXT` vs each `ccat` archive;
  `source/Strongs/*.BP5` vs every archive member that plausibly contains
  parsing/Strong's data (or `provenance-unknown` if none does).
- **Derived tier:** `csv-unicode/**` and `tei-xml-unicode/**` vs text
  reconstructed from `ascii`, `preformatted`, and `ccat`. Where an exact
  comparison needs the Cycle 3 parser, mark `incomparable-pending-pipeline` and
  state why.

The report must keep **raw** and **normalized** comparisons separate, so
encoding and line-ending noise is never reported as textual change.

Every non-exact difference is classified into at least one category:

- encoding / line endings / BOM;
- Unicode normalization (NFC/NFD);
- whitespace;
- Beta-code convention difference;
- letters / spelling;
- accents, breathings, diaeresis, iota subscript;
- punctuation;
- capitalization;
- variant/apparatus marker or reading (N/B/C/M/S/E);
- parsing code;
- Strong's number;
- verse/chapter numbering or book/section mapping;
- other (explained).

### R5 - Strong's/BP5 provenance

- Determine whether `source/Strongs/*.BP5` comes from any listed archive.
- If not, record `provenance-unknown`, state what is known (e.g. file names,
  encoding, change history), and add a maintainer decision.
- Do not assume the Strong's files share the CCAT archive's provenance.

### R6 - Edition and revision determination

- Decide, with evidence, whether the current text is `rp2018` or a distinct
  revision (`rp2018@2023-07-20`), and whether the current files correspond to
  the 2005 archive, the 2018 archive, both in different files, or neither.
- Record which archive, if any, matches each current file exactly.
- If the official 2018 archive predates the July 2023 corrections, document the
  specific differences.

### R7 - External history and provenance docs

- Update `docs/HISTORY.md` with the external evidence (archive checksums and the
  files they match).
- Create `docs/PROVENANCE.md` describing each edition, its archives, their
  checksums, and the maintainer's canonical-source decisions.
- Keep the internal git-history map; add external evidence alongside it.

### R8 - Reports and decision log

- `reports/reconciliation/summary.md` - verdict and match matrix.
- `reports/reconciliation/files.csv` - per-file mapping and match class.
- `reports/reconciliation/verses.csv` - verse-level differences.
- `reports/reconciliation/categories.csv` - category totals.
- `reports/reconciliation/archives.csv` - archive inventory and checksums.
- `reports/reconciliation/decision-log.md` - every conflict with evidence,
  options, and a maintainer decision field. The archive-commit question (R8) is
  resolved: the six original zips are committed under `data/raw/_archives/`.
- Reports are deterministic (stable ordering, no timestamps).

### R9 - Safety

- The comparison is read-only with respect to the current corpus.
- Never overwrite, move, normalize, or delete any file under `source/`,
  `csv-unicode/`, `tei-xml-unicode/`, or `essay/` during comparison.
- Never select a canonical source automatically. The pipeline flags; the
  maintainer decides (TECH.md §4).
- Any later adoption of an official archive into `source/` is a separate,
  explicitly approved change with its own validation.

### R10 - Tests and reproducibility

- Red/green TDD for all reconciliation tooling.
- Tests for: hashing/inventory, encoding and line-ending detection,
  normalization, file mapping, verse/word alignment, category assignment, and
  deterministic report generation.
- A golden test on a small real book locks the comparison output.
- Tests run offline and are deterministic.
- Document the exact commands in `reports/reconciliation/summary.md`.

### R11 - Intentional blanks confirmation

- Confirm from the official archives that LUK 17:36, ACT 8:37, ACT 15:34, and
  ACT 24:7 are absent from the Byzantine tradition, and record the evidence.
- Do not treat their absence as missing data.

## Deliverable layout

```
data/
  raw/rp2005/ ...
  raw/rp2018/ ...
  provenance/rp2005.toml
  provenance/rp2018.toml
docs/
  PROVENANCE.md
  HISTORY.md                  # updated
reports/reconciliation/
  summary.md
  archives.csv
  files.csv
  verses.csv
  categories.csv
  decision-log.md
src/byz/reconcile/...
tests/reconciliation/...
```

## Acceptance criteria

- All six archives are fetched, hashed, and recorded in provenance.
- Every archive member and every current file is mapped or explicitly flagged.
- The match matrix gives exact/normalized/textual/structural/missing/extra counts
  and a verdict per edition and format, with raw and normalized results separate.
- The specific question "to what extent do the current `source/CCAT` and
  `source/Strongs` files match the official 2005 and 2018 archives?" is answered
  with evidence.
- Strong's provenance is resolved or explicitly recorded as unknown.
- `rp2018` vs `rp2018@2023-07-20` is decided with evidence.
- The four intentional blanks are confirmed from the official archives.
- `docs/PROVENANCE.md` and the updated `docs/HISTORY.md` exist.
- Reports are deterministic; no corpus file changed; tests pass.
- The maintainer has a decision log to approve.

## Open questions (to resolve with the maintainer during the cycle)

1. Is the Dropbox `rp2018-ccat.ZIP` the original 2018 release or the July 2023
   revision (or neither)?
2. Where did `source/Strongs/*.BP5` come from? None of the six archives is
   obviously a parsed/Strong's archive. Is there an official parsed-file URL?
3. Which archive is the reference for each derived format: CCAT, ASCII, or
   preformatted?
4. For derived files, is a text-level comparison acceptable now, or should exact
   comparison wait for the Cycle 3 parser?
5. If an official file differs from `source/`, should the official file replace
   it (with approval), or should the repository keep its current revision?
6. Should the original zip files be committed, or only the extracted inputs plus
   checksums? **Resolved (2026-11-17):** the six original zips are committed
   under `data/raw/_archives/`, alongside the extracted inputs and checksums.

## Risks

- Dropbox links may expire, rate-limit, or require a browser; capture checksums
  immediately.
- Archives may use different nesting, naming, encoding, or line endings.
- Encoding/line-ending noise can swamp real differences; the raw vs normalized
  split mitigates this.
- The 2018 archive may not include the July 2023 corrections.
- The Strong's files may have no official archive at all.
- Full-New-Testament diffs can be large; use streaming and hashing.
