# Mission

## What this repository is

`byzantine-majority-text` is the canonical, public-domain, machine-readable
distribution of the Robinson-Pierpont edition of the Greek New Testament (the
Byzantine Majority Text / Byzantine Textform). It is built directly from the
official files published for Dr. Maurice A. Robinson's editions, and it exists so
that anyone can obtain any published edition, reproduce it byte-for-byte, and see
exactly what changed between editions.

The repository is not itself a critical edition. Dr. Robinson's official files
are the authority; this project's job is faithful, transparent, reproducible
redistribution.

## Who it is for

- **Textual critics and scholars** who need edition-accurate data and deltas.
- **Translators and students** who need a clean, documented Greek text.
- **Software developers** who need stable CSV and TEI-XML exports.
- **Librarians and archivists** who need provenance, checksums, and snapshots.
- **Collation tools** (e.g. CollateX, INTF workflows) that consume TEI-XML.

## Principles

1. **Fidelity to the official text.** Never invent, harmonize, normalize away, or
   silently "fix" a reading. The official Robinson files are the source of truth.
2. **Provenance is mandatory.** Every input and artifact must be traceable to an
   official archive, a checksum, and a pipeline version. No anonymous data.
3. **Editions are first-class.** RP2005 and RP2018 coexist as immutable, clearly
   labelled editions. RP2026 is a future cycle. No edition is inferred from git
   history alone.
4. **Snapshots and deltas.** A user must be able to download any edition and see
   a clear, readable, categorized diff against any other edition.
5. **Reproducibility.** The same inputs and the same pipeline must produce the
   same outputs, byte-for-byte, on a clean machine.
6. **Spec-driven, red/green TDD.** Every non-trivial change has a spec
   (`requirements.md`, `plan.md`, `validation.md`). Tests are written first and
   must fail for the right reason before code is written.
7. **The user decides on conflict.** When the official archives disagree with the
   existing repository files, or with each other, the pipeline flags the conflict
   with evidence and the maintainer decides. It never silently picks a winner.
8. **Public domain, open access.** The text and code remain in the Public Domain.
   No lock-in, no runtime network dependency, no proprietary tooling required to
   read the outputs.

## Scope

**In scope**

- Official source ingestion and provenance for RP2005, RP2018, and later editions.
- A reproducible Python pipeline from raw files to final artifacts.
- CSV exports (with/without variants, with/without parsing).
- TEI-XML exports (main text and apparatus following the TEI P5 and IGNTP
  guidelines).
- Categorized deltas between editions.
- Committed artifacts, checksums, manifests, and release snapshots.
- Documentation of conventions (Beta code, variant codes, parsing, Strong's).

**Out of scope (for now)**

- Creating a new critical edition or adjudicating readings.
- Translations, lexical definitions, or morphological disambiguation beyond the
  official parsing data.
- A web application or API service.
- Changing the official text to match external editions (NA/ECM) except where the
  official apparatus already records those variants.

## Success criteria

- A user can check out a tag or release for each edition and get the exact files.
- A user can read a diff between any two editions and understand *what* changed
  and *why category* of change it is.
- A clean machine can rebuild every committed artifact and get no diff.
- Every artifact carries a checksum and a provenance record.
- The test suite passes in CI, and every change is backed by a spec.

## Non-goals

- Becoming the authority on the text. The maintainers distribute Dr. Robinson's
  work; they do not own it.
- Keeping every historical path forever. Path compatibility is best-effort.
- Optimizing for a single downstream format at the expense of fidelity.
