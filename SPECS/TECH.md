# Technical constitution

This document is the technical contract for `byzantine-majority-text`. It defines
editions, sources, provenance, repository layout, the pipeline, output formats,
testing, and the rules that every change must follow. Where this document and an
individual spec disagree, the spec wins only if this document is updated in the
same change.

## 1. Editions

An **edition** is an immutable, officially published state of the text. Edition
ids are lowercase and stable:

- `rp2005` - Robinson-Pierpont 2005.
- `rp2018` - Robinson-Pierpont 2018 (including later official corrections such
  as the July 20, 2023 update, recorded as revision metadata).
- `rp2026` - reserved for a future cycle; no data is invented before the
  official files exist.

An edition is defined by its official input archives, not by a git branch or by
the current state of `master`. Editions may have a `revision` (date) and a
`source_url`; both are recorded in provenance. Git tags freeze each edition
(`rp2005`, `rp2018`, `rp2026`).

## 2. Official source archives (for the record)

The official files are published by the Byzantine Text website. Known archives:

**2005**

- `editions-rp2-preformatted.zip` -
  <https://www.dropbox.com/s/ago0uhvmjndbsy5/editions-rp2-preformatted.zip?dl=0>
- `editions-rp2-ascii.zip` -
  <https://www.dropbox.com/s/oil2m3la4vsnbpb/editions-rp2-ascii.zip?dl=0>
- `editions-rp2-ccat.zip` -
  <https://www.dropbox.com/s/f3di0cgdflqjwq4/editions-rp2-ccat.zip?dl=0>

**2018**

- `rp2018-ascii.zip` -
  <https://www.dropbox.com/s/ug3i36zsvtg39x0/rp2018-ascii.zip?dl=0>
- `rp2018-ascii-one-line-per-verse.zip` -
  <https://www.dropbox.com/s/cr592513g0v2imc/rp2018-ascii-one-line-per-verse.zip?dl=0>
- `rp2018-ccat.ZIP` -
  <https://www.dropbox.com/s/u47y6wedewv4mv9/rp2018-ccat.ZIP?dl=0>

**2026** - to be supplied when the edition is published (see `ROADMAP.md`).

The provenance of the existing `source/Strongs/*.BP5` (parsing and Strong's
numbers) must be established separately during the reconciliation cycle; it is
not assumed to come from the archives listed above.

## 3. Provenance

Every edition has a machine-readable provenance record
(`data/provenance/<edition>.toml` or equivalent) containing at least:

- edition id and revision date;
- each official archive: file name, URL, download date, SHA-256;
- what was extracted and where it lives under `data/raw/<edition>/`;
- the canonical commit or tag that froze the edition;
- free-text notes on known discrepancies.

Provenance is append-only in spirit: never rewrite the history of an edition; add
a new revision when the official files change.

## 4. Canonical-source conflict policy

When the official archives differ from the existing repository files, or from
each other:

1. **Do not overwrite anything silently.**
2. Produce a reconciliation report: per file, per book, and per verse where
   possible, showing the difference and a normalized/word-level summary.
3. Classify each difference (letters, accents/breathings, punctuation,
   capitalization, apparatus, parsing, Strong's, encoding).
4. Present the report to the maintainer. **The maintainer decides which state is
   canonical for each edition.**
5. Record the decision and the evidence in provenance and in the spec's
   `validation.md`.

No tool may auto-select a canonical source. This is a hard rule.

## 5. Repository layout (target)

```
SPECS/                      # constitution + one folder per change
  MISSION.md
  TECH.md
  ROADMAP.md
  YYYY-MM-DD-<change>/
    requirements.md
    plan.md
    validation.md

data/
  raw/<edition>/            # immutable extracted official inputs (committed)
  provenance/<edition>.toml # urls, sha256, dates, decisions

editions/<edition>/
  csv/                      # committed generated CSV artifacts
  tei/                      # committed generated TEI-XML artifacts
  manifest.json             # per-file hashes + pipeline version

reports/
  diff/<edition-a>--<edition-b>/
    report.md               # human-readable, categorized
    changes.csv             # machine-readable

src/byz/                    # Python package (parse, model, validate, render, diff)
tests/                      # pytest suite
scripts/                    # thin wrappers: test, lint, build, verify, diff
docs/                       # provenance, history, release notes
```

The migration from the current `source/`, `csv-unicode/`, and `tei-xml-unicode/`
layout is a spec of its own. Path compatibility is best-effort, not obligatory;
any move must be documented in the README and release notes.

## 6. Pipeline

The pipeline is deterministic and staged. Each stage has a clear input and output:

1. **Ingest** - copy the extracted official files into `data/raw/<edition>/`;
   verify checksums; never edit in place.
2. **Parse** - turn CCAT/Beta/ASCII/BP5 into a canonical in-memory model.
3. **Validate** - check structure, book coverage, verse numbering, encoding,
   variant and parsing conventions; fail loud with book/chapter/verse context.
4. **Normalize** - Unicode NFC and documented whitespace rules, applied
   consistently and reported separately from textual change.
5. **Transform** - produce the requested views (with/without variants,
   with/without parsing, per edition).
6. **Render** - emit CSV, TEI-XML (main text and apparatus), and delta reports.
7. **Package** - compute hashes and manifests; the artifacts are committed.

Stages communicate through explicit data structures, not through ad-hoc globals.
Parsing, validation, and rendering are separate concerns and must not be mixed.

## 7. Canonical data model

At minimum:

- **Edition**: id, revision, provenance.
- **Book**: id (e.g. `MAT`, `1CO`), name, ordinal, section files.
- **Chapter** and **Verse**: numeric ids; a verse is the unit of comparison.
- **Word**: surface form, position, optional variants, optional parsing, optional
  Strong's number.
- **Variant / apparatus entry**: code (`N`, `B`, `C`, `M`, `S`, `E`), text, witness
  mapping.
- **Parsing**: the Robinson codes documented in `source/README.md`.
- **Strong's number**: integer, with the repo's documented deviations from
  classic Strong's.

Two-parsing words (for example James 4:5, 2 Timothy 2:6) keep both parsing/Strong's
alternatives in the parsed views and appear once in the unparsed/TEI main text.

## 8. Output artifacts

Artifacts are **committed to git** (maintainer decision) and also attached to
edition releases. Generated files are never hand-edited; a change to an artifact
comes from a change to the pipeline or to the input.

### CSV

Per edition, matching the existing shapes where sensible:

- variants dropped / kept;
- parsing dropped / kept;
- columns `chapter,verse,text` (as today), integer chapter/verse.

### TEI-XML

Per edition:

- **Main text** - no apparatus, IGNTP-style `<div type="book">`,
  `<div type="chapter">`, `<ab n="...">`, `<w>`; valid, well-formed TEI P5.
- **Apparatus** - follows the TEI P5 apparatus guidelines and the IGNTP
  guidelines. Witnesses are declared in `<listWit>` (mapped from the variant
  codes), and readings use `<app>`, `<lem>`, `<rdg>` with `@wit` and stable `@n`
  anchors. The base/lemma witness is the Byzantine text. Validate against the TEI
  RelaxNG schema in tests.

### Deltas

Per edition pair (`reports/diff/<a>--<b>/`):

- `report.md` - human-readable, grouped by book/chapter/verse and by category.
- `changes.csv` - one row per change: edition pair, book, chapter, verse, word
  position, old, new, category, source (main text or apparatus).

Comparison is verse-aligned and then word-aligned. Normalization-only differences
(Unicode form, whitespace) are reported in their own category and never mixed with
textual change.

## 9. Determinism and reproducibility

- No timestamps, hostnames, absolute paths, or run-dependent ordering in
  artifacts. Use stable sort keys and, where a date is unavoidable,
  `SOURCE_DATE_EPOCH`.
- Pin dependencies in `pyproject.toml` (and keep `scripts/requirements.txt`
  consistent during migration).
- A clean rebuild must produce no diff against the committed artifacts; CI
  enforces this with `git diff --exit-code` after a build.
- Every artifact is listed in `editions/<edition>/manifest.json` with its hash and
  the pipeline version.

## 10. Testing (red/green TDD)

This is a red/green TDD repository. For every behaviour:

1. **Red** - write a failing test that expresses it and confirm it fails for the
   right reason.
2. **Green** - write the smallest change that makes it pass.
3. **Refactor** - clean up while green.

Test layers:

- **Unit** - Beta-code standardization, parsing, Strong's, variant extraction.
- **Golden** - exact expected output for a small real pericope (e.g. John 1) in
  every format.
- **Property/invariant** - every book present exactly once; no unmapped book;
  verse counts stable; NFC; no Beta-code leftovers in Unicode outputs.
- **Schema** - TEI-XML validates against the TEI P5 RelaxNG schema and the
  apparatus follows the documented structure.
- **Determinism** - build twice, compare hashes; rebuild committed artifacts and
  assert no diff.
- **Delta** - categorization and alignment tests over known edition pairs.

Tests use the real committed inputs and artifacts wherever possible. No network
access in tests. Do not mock the source files.

## 11. Code conventions

- Python 3.10+ (match the current scripts during migration), typed where useful,
  packaged under `src/byz/`.
- No silent failures: invalid input or an impossible lookup raises with context
  naming the edition, book, chapter, and verse.
- No hand-edited generated files and no generated data in tests as a substitute
  for real fixtures.
- Keep the human-facing scripts in `scripts/` thin; logic lives in `src/byz/`.
- README files document commands; if a command changes, update the README.

## 12. Specs and governance

- Every non-trivial change gets `SPECS/YYYY-MM-DD-<change>/` with
  `requirements.md`, `plan.md`, and `validation.md`.
- A spec must state the affected editions, inputs, outputs, and how it will be
  validated.
- Bug fixes must follow the `investigate-bug` skill (RCA + sibling/category
  sweeps + prevention) and lock the category with tests.
- The maintainer decides conflicts, canonical sources, and backward-compatibility
  questions. The pipeline only flags.
