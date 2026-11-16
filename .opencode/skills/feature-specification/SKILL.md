---
name: feature-specification
description: Guide for planning changes to the byzantine-majority-text repository (scripts, Unicode CSV/TEI-XML regeneration, source-data corrections, docs, essay). Use when asked to plan or specify a non-trivial change.
---

Read `README.md`, `source/README.md`, `scripts/README.md`, and the README of
every folder the change touches. These document the repository contract. Then
create a plan for the requested change. Create a branch and ask the user about
the plan before writing.

Create:

- A new directory `SPECS/YYYY-MM-DD-<change-name>/` for this work.
- In there:
  - `plan.md` as a series of numbered task groups. If a step needs checks, say
    exactly how to verify it (install `scripts/requirements.txt`, run the
    relevant converter from `scripts/`, inspect the regenerated files).
  - `requirements.md` for the scope, decisions, and context.
  - `validation.md` for how to know the change succeeded and can be merged.

# Repository contract

- **Source is authoritative.** `source/CCAT/*.TXT` (accented, with variants) and
  `source/Strongs/*.BP5` (Strong's numbers and parsing, unaccented) come from
  Dr. Maurice A. Robinson. Do not plan content changes to them unless the user
  has approved a correction to the official edition. Preserve Beta code, variant
  markers (N/B/C/M/S/E), parsing codes, and Strong's numbers exactly.
- **Generated files are derivatives.** `csv-unicode/` and `tei-xml-unicode/` are
  produced by `scripts/csv_converter.py` and `scripts/tei_xml_converter.py`. Plan
  to regenerate them, never to hand-edit them.
- **Scripts are Python 3.10** with pinned dependencies in
  `scripts/requirements.txt` (`pandas==1.4.2`, `beta-code==1.0.0`). They use
  relative paths (`../source`, `../csv-unicode`, `../tei-xml-unicode`) and must be
  run from inside `scripts/`.
- **Everything is public domain.** Do not introduce license-incompatible content
  or dependencies.
- **No tests, linter, or build system exist.** Plan verification around
  regeneration, diffs, and explicit data checks (verse counts, CSV parsing,
  XML well-formedness, no Beta-code remnants). Do not invent tooling. If you
  propose adding tests or checks, ask first and keep them dependency-light.

# Requirements

- Privilege proper, explicit validation over ad-hoc regexes and eyeballing. A
  validator should check structure and types and fail with a message naming the
  offending book, verse, or field.
- Do not assume backward compatibility for the generated formats; ask the user
  in each specific instance where a decision must be made.
- Privilege solutions that are simple, elegant, and general; minimize complexity
  and arbitrariness. Propose simpler alternatives when you see them.
- Keep the repository contract visible in the plan: source vs generated, Beta
  code and parsing conventions, pinned dependencies, public domain.

# Root cause, category & prevention (bug-fixing plans)

When a plan fixes a bug (or a set of related bugs), it must go beyond the
reported symptom. **Invoke the `investigate-bug` skill** - it is the canonical
protocol for RCA and category sweeps.

- **Investigate the root cause** (Horizon 0) - why the failure happens (data
  shape, Beta-code mismatch, regex overreach, ordering, unhandled variant), with
  evidence.
- **Fix the category, not the instance** (Horizons 1 & 2) - sweep the sibling
  books, converters, and outputs that share the root cause; fix every instance.
- **Prevent recurrence** - include at least one general, mechanism-level guard:
  a conversion assertion that fails loud, a single canonical helper shared by
  every output path, or a small check script that validates the generated data.
- **Lock the category in** - verify the instance and its siblings, plus a check
  that the prevention actually fires.
- **Name the category** - give it a stable name (e.g. "variant stripped in one
  output only", "final sigma converted to medial", "multi-parsing word loses its
  second Strong's number") matching the `investigate-bug` skill.

The plan's `plan.md` must include the sweeps as explicit tasks; a plan that only
patches the reported call site is rejected. When unsure whether two findings are
the same class, ask the user.

# Contracts against arbitrary inputs & outputs

- Treat every boundary as untrusted: the hand-maintained source files, the CSV
  and XML output formats, and the `beta-code` library.
- Validate at the edge, then work with known-good values internally. Never pass
  unchecked fixture data or raw lines across module boundaries.
- Where a field's meaning matters (book id, chapter/verse, variant code, parsing
  code, Strong's number), derive it from a single canonical source - never match
  free text in several places.
- The converter scripts are the only producers of graded output; the source files
  are the only authority on the text.

# YAGNI

- Plan only what is needed now. Do not add speculative abstractions, config
  toggles, or extra formats "just in case".
- Cut scope by default; when unsure, leave it out and ask the user.

# Validation

The validation step also includes surfacing differences between what was
implemented and the plan, and updating the plan and docs upon the user's
approval.

# Important

- You _must_ ask the user for clarifications before writing to disk.
