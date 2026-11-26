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

## 2. Official sources: PDFs and archives

The official files are published by the Byzantine Text website. The **published
PDFs are the ultimate source of truth**; the ZIP archives are machine-readable
companions.

### Official published PDFs

- 2005: `editions-rp2.pdf` (Chilton Book Publishing, Southborough,
  Massachusetts) -
  <https://byzantinetext.com/wp-content/uploads/2016/11/editions-rp2.pdf>
- 2018: `robinson-pierpont-2018-gnt-edition.pdf` (VTR, Nuremberg) -
  <https://byzantinetext.com/wp-content/uploads/2021/03/robinson-pierpont-2018-gnt-edition.pdf>

The PDFs are stored at `data/raw/<edition>/official-pdf/` and recorded in
`data/provenance/pdfs.toml`. If an archive or a repository file disagrees with a
PDF, the conflict is recorded and escalated to the maintainer instead of being
resolved automatically.

### Machine-readable archives

The six archives were listed on and retrieved from the Byzantine Text editions
listing page
<https://byzantinetext.com/study/editions/robinson-pierpont/> in November 2026.
The Dropbox URLs below are the per-file download targets.
`data/provenance/rp2005.toml` and `data/provenance/rp2018.toml` record the
listing page as `source_page` on every archive record;
`data/provenance/pdfs.toml` is hand-maintained and has no such field.

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

The six archives are committed under `data/raw/print/_archives/<edition>/`, so a clone
carries the exact published files for posterity and offline reproducibility.
`data/provenance/*.toml` pins each SHA-256, and
`PYTHONPATH=src python3 -m byz.fetch --verify` re-checks the committed copies
without network access. `data/raw/` has two source classes: `print/` for the
published print editions (extracts, PDFs, and the six ZIPs) and `repo/` for this
repository's own lineage (the 2019 tag snapshot and the current text).

`data/raw/repo/rp2018-2023/strongs/*.BP5` are Dr Robinson's official parsed files
(see `data/raw/repo/CONVENTIONS.md`); none of the six archives listed above
contains a
parsed/Strong's file, so the delivery route for the parsed files is not
recorded.

The 2019 lineage is a git-tag input rather than an archive extract. Its
`textonly-beta-code` and `parsed` files are committed at
`data/raw/repo/rp2005-2019/`, and `data/provenance/rp2005-2019.toml` records tag
`v2.0.3`, its commit, and every file's SHA-256 and size.
`PYTHONPATH=src python3 -m byz.materialise` restores that tree from the tag;
only it extracts the tag's files into `data/`, and the build reads `data/` only.
(`byz.reconcile` reads the tag with `git show` for historical comparison, and
`byz.build` lists tags for the release ranges, but neither uses the tag's files
as build inputs.) The tag's released CSV/TEI are not inputs and are not used by
the build: `byz.build` regenerates every `editions/rp2005-2019/` view from the
57 source files with the current pipeline, which corrects the 2019 converter's
malformed apparatus codes and typography while keeping the main text's words.

## 3. Provenance

Every edition has a machine-readable provenance record
(`data/provenance/<edition>.toml` or equivalent) containing at least:

- edition id and revision date;
- each official archive: file name, URL, download date, SHA-256;
- **git-tag provenance** for the 2019 lineage: tag, commit, and per-file
  SHA-256 under `data/raw/repo/rp2005-2019/`;
- **working-tree provenance** for the current text: revision `2023-07-20`, the
  two source commits, and per-file SHA-256 under `data/raw/repo/rp2018-2023/`;
- the provenance kinds: `official archive`, `published PDF`, `git tag`, and
  `working-tree snapshot`;
- what was extracted and where it lives under `data/raw/`;
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
  README.md                 # generated index of the two source classes
  provenance/<edition>.toml # urls, sha256, dates, decisions, tag/revision inputs
  raw/
    README.md               # generated: print vs repo
    print/                  # published print-edition material
      README.md
      _archives/{rp2005,rp2018}/          # immutable original official zips
      rp2005/{ccat,ascii,preformatted,official-pdf}/
      rp2018/{ccat,ascii,preformatted,official-pdf}/
    repo/                   # this repository's lineage
      README.md
      CONVENTIONS.md        # hand-maintained Beta-code/parsing conventions
      rp2005-2019/{textonly-beta-code,parsed}/
      rp2018-2023/{ccat,strongs}/

editions/<edition>/         # committed outputs only: manifest.json, csv/, tei/, README.md
  csv/                      # committed generated CSV artifacts
  tei/                      # committed generated TEI-XML artifacts
  manifest.json             # per-file hashes, inputs pinned under data/

reports/
  diff/<edition-a>--<edition-b>/
    report.md               # human-readable, categorized
    changes.csv             # machine-readable

src/byz/                    # Python package (parse, model, validate, render, diff)
  fetch.py materialise.py   # entry points, run as `python -m byz.<verb>`
  build.py diff.py verify.py
  beta/converter.py         # Beta-code converter
  curate/tei_xml_header.xml # TEI header template
tests/                      # unittest suites
docs/                       # build reference, provenance, history, release notes
requirements.txt            # beta-code==1.0.0
```

The finished layout is **sources -> pipeline -> editions**. `data/raw/print/`
(published material, including the committed archives) and `data/raw/repo/`
(this repository's lineage) are the two source classes and the inputs;
`byz.build` is the only producer of
`editions/<edition>/csv/` and `editions/<edition>/tei/`, and it regenerates
every edition, including `rp2005-2019`, from those inputs. An edition directory
contains outputs only, never an input snapshot; its `manifest.json` pins every
input by repository-relative path and SHA-256, and `byz.verify` checks both the
inputs and the artifacts. The repository code is
one package: entry points are `PYTHONPATH=src python3 -m byz.<verb>` modules, and
there is no `scripts` directory. The 2026-11-21 move is recorded in
`SPECS/2026-11-21-input-and-code-layout/` and mapped in `docs/EDITIONS.md`.
The 2026-11-25 removal of the per-edition input snapshots is recorded in
`SPECS/2026-11-25-inputs-out-of-editions/`, and the same date's input-class move
(print/repo, with the current text under `data/raw/repo/rp2018-2023/`) is
recorded in `SPECS/2026-11-25-data-source-classes/`.
There is no working-tree mirror: the legacy `csv-unicode/` and
`tei-xml-unicode/` trees were removed on 2026-11-19 (see
`SPECS/2026-11-19-retire-legacy-unicode-trees/`), and every old path is
documented in `docs/EDITIONS.md`.

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
- **Parsing**: the Robinson codes documented in
  `data/raw/repo/CONVENTIONS.md`.
- **Strong's number**: integer, with the repo's documented deviations from
  classic Strong's.

Two-parsing words (for example James 4:5, 2 Timothy 2:6) keep both parsing/Strong's
alternatives in the parsed views and appear once in the unparsed/TEI main text.

## 8. Output artifacts

Artifacts are **committed to git** (maintainer decision) and also attached to
edition releases. Generated files are never hand-edited; a change to an artifact
comes from a change to the pipeline or to the input. An edition directory
contains outputs only; `manifest.json` pins its inputs under `data/` by
repository-relative path and SHA-256.

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
- Pin dependencies in `requirements.txt` at the repository root
  (`beta-code==1.0.0`); install with `pip install -r requirements.txt`.
- A clean rebuild must produce no diff against the committed artifacts; CI
  enforces this with `git diff --exit-code` after a build.
- Every artifact is listed in `editions/<edition>/manifest.json` with its hash and
  the pipeline version.
- `PYTHONPATH=src python3 -m byz.verify` is the clean-tree integrity check: it
  re-hashes every pinned input under `data/` and every committed artifact, and
  exits non-zero on any mismatch, missing file, or unexpected file. It writes
  nothing and needs no network.

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

- Python 3.10+ (match the current package), typed where useful,
  packaged under `src/byz/`.
- No silent failures: invalid input or an impossible lookup raises with context
  naming the edition, book, chapter, and verse.
- No hand-edited generated files and no generated data in tests as a substitute
  for real fixtures.
- Keep the human-facing entry points as thin modules run with
  `PYTHONPATH=src python3 -m byz.<verb>`; logic lives in `src/byz/`. The entry
  points are `fetch`, `materialise`, `build`, `diff`, `contract`, `reconcile`,
  and `verify`. There is no `scripts` directory, no module manipulates
  `sys.path`, and no build reads an input from under `editions/`.
- The input tree has two classes under `data/raw/`: `print/` for published
  print-edition material and `repo/` for this repository's lineage. `byz.build`
  writes the eight input-tree READMEs and the current-text provenance record;
  never hand-edit them.
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
