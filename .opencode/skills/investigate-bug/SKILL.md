---
name: investigate-bug
description: Guide for investigating data-conversion and script bugs via RCA and category sweeps in byzantine-majority-text. Use whenever a conversion error, wrong Unicode output, wrong parsing/Strong's number, malformed CSV/TEI-XML, or suspected defect is reported - before patching. Accessible to all agents.
---

# Investigate Bug

You are investigating a bug. Your job is to diagnose the **instance**, classify
the **category**, and patch the **class** - not just the symptom. Follow the
three horizons in order. **Report your findings** to your caller (the
orchestrating agent if you are a subagent in a loop, otherwise the user). Do not
write plan files to disk - crafting `SPECS/` plans is the plan agent's job. Your
report informs that next step.

## When to invoke

Invoke this skill whenever:

- A bug report, reproduction, log, or failing check is handed to you.
- You observe wrong Greek text, a lost accent/breathing, a stripped variant, a
  dropped parsing code, a misplaced Strong's number, malformed CSV, or invalid
  TEI-XML that looks like a bug class.
- The code-reviewer or verifier suspects a pattern that may have siblings.

If you are not sure whether something is a bug-class, treat it as one and ask
the caller.

## The three horizons

Investigate in this order. Do not skip a horizon. Each horizon must produce an
explicit finding - even "nothing found" is a finding.

### Horizon 0 - The instance (RCA)

1. **Reproduce.** Reproduce with the smallest possible input: the affected verse
   or book, the exact source line from `data/raw/repo/rp2018-2023/ccat/*.TXT` or
   `data/raw/repo/rp2018-2023/strongs/*.BP5`, and the failing output under
   `editions/rp2018-2023/`. Regenerate from the repository root with
   `PYTHONPATH=src python3 -m byz.build` after
   `pip install -r requirements.txt` (from the repository root). Confirm the
   failure is about the bug, not a typo or a stale generated file.
2. **Mechanism.** Explain _why_ it fails - the data shape, Beta-code variant,
   regex overreach, ordering, unhandled parsing alternative, or a mismatch
   between Prof. Robinson's Beta code and the `beta-code` library - not just
   _where_. Quote the line(s) and the mechanism. Examples of the shape this
   takes here:
   - a regex strips `{...}` variants but also removes text that is not a variant;
   - `standardise_beta_code()` does not handle a `+/` vs `/+` ordering, so an
     accent is lost or misplaced;
   - a final sigma is converted to a medial sigma because the following
     dash/bracket was not spaced;
   - a multi-parsing word loses its second Strong's number or parsing code in the
     with-parsing CSV but keeps it in another output;
   - a book is omitted or duplicated because of its id in `book_dict`;
   - a section heading file (for example `04a_PA.TXT`, `05a_ACT24.TXT`) is not
     mapped to the same output as its main book.
3. **Silence analysis.** Why did this stay silent? Missing invariant, swallowed
   exception, un-validated conversion, or a check that only covered one book?
   Name the gap.

**Exit criterion:** You can state the root cause in one sentence with evidence
linked (file:line, source input, wrong output).

### Horizon 1 - Narrow blast radius (siblings next door)

Same pattern, same root cause, close by.

1. **Define the radius.** The narrow radius is: the same script, the same helper
   (`standardise_beta_code`, `convert_beta_to_unicode`,
   `convert_beta_to_unicode_strongs`), the same book or the same conversion path,
   and directly neighbouring call sites that were copy-pasted or share the
   helper.
2. **Sweep.** Run a systematic search - `grep` for the literal pattern, inspect
   the sibling books, and read the neighbouring functions. Do not eyeball a
   single verse and declare "no siblings".
3. **Classify each hit.** For every hit record: `file:line | snippet |
   affected? (yes/no/unsure) | impact`. When unsure whether two findings are the
   same class, ask the caller.

**Exit criterion:** A table listing every H1 sibling found (or "none found after
sweeping X") with verdict and references. Every affected sibling must be flagged
for fixing alongside the instance.

### Horizon 2 - Codebase-wide category (the class)

The same root cause across books, modules, and outputs.

1. **Name the category.** Give the class a stable name, drawn from the examples
   below, so future findings can reference the class:
   `variant stripped in one output only`, `accent lost by Beta-code
   standardisation`, `final sigma rendered as medial`, `multi-parsing word loses
   its second parsing`, `Strong's number misaligned`, `book id omitted from
   book_dict`, `CSV/TEI output not regenerated`.
2. **Codify the signature.** Write down the searchable signature of the class:
   function name, regex, operator, literal shape, or field you are sweeping for.
3. **Sweep the codebase.** Repeat the systematic search across all of
   `data/raw/repo/rp2018-2023/ccat/`, `data/raw/repo/rp2018-2023/strongs/`, `src/byz/curate/`, `editions/*/csv/`,
   and `editions/*/tei/`. Check every book (including
   `04a_PA` and `05a_ACT24`) and every output variant (with/without variants,
   with/without parsing).
4. **Report.** Produce a second table - same columns as H1 but for H2. Include
   false positives you eliminated and why. "No codebase-wide siblings found
   after sweeping Y" is a valid result, but you must state what you swept.

**Exit criterion:** A category sweep table with stable category name, signature,
scope swept, and every codebase-wide sibling classified. No silent "I didn't
look".

## From findings to fixes

After the three horizons, present findings and potential fixes grouped by
horizon:

| Horizon            | Finding                 | Proposed fix                                                  | Prevention                               |
| ------------------ | ----------------------- | ------------------------------------------------------------- | ---------------------------------------- |
| H0 - instance      | one-line RCA            | direct patch                                                  | -                                        |
| H1 - narrow radius | N siblings at file:line | fix each sibling alongside instance                           | shared helper / guard at module boundary |
| H2 - codebase-wide | M siblings at file:line | fix each sibling (or a follow-up plan if scope is large)      | general mechanism (see below)            |

**Prevention (required).** Every bug-fixing report must propose at least one
_general, mechanism-level_ prevention so the class cannot silently recur. Prefer
these, in order:

- **Fail-loud conversion invariant.** If a conversion or lookup cannot handle an
  input (unknown variant code, unparsable line, missing book mapping), raise with
  a message naming the book, chapter, and verse instead of emitting a silently
  wrong line.
- **Single canonical derivation.** One helper produces the Unicode text and one
  produces the CSV/TEI record; every output path uses them, so conventions cannot
  drift between `with-variants` and `no-variants`, or between parsing and
  non-parsing outputs.
- **Small check script.** A check under `tests/` that re-derives the generated
  files and asserts they match what is committed, checks verse counts and book
  coverage, and validates CSV shape / XML well-formedness. Wire the command into
  `docs/BUILD.md`.
- **Round-trip / spot check.** Re-convert a known verse and assert the exact
  expected Unicode string and parsing, including a multi-parsing word.

Cite the repo-precedented option you recommend and where it would be wired. If no
precedent exists yet, say so and recommend the simplest mechanism.

**Lock-in (propose).** Propose checks that would lock the class:

- One check per sibling instance (H1 + H2) proving it no longer reproduces.
- At least one check asserting the prevention mechanism actually fires (the
  converter raises, the output check fails).
- A book-coverage check when the class is an omitted/duplicated book or section.

Do not implement checks unless your caller asks - you are reporting, not taking
over the implementer's job.

## How to report

- **In a loop (subagent -> orchestrator):** Return a structured report to the
  calling agent via your final message. The orchestrator decides whether to hand
  it to the plan agent (new plan), the spec-implementer (patch loop), or the
  user. Do not write `SPECS/...` files yourself.
- **Invoked directly by the user:** Report to the user in the same structured
  format (RCA -> H1 table -> H2 table -> proposed fixes -> prevention -> check
  proposals -> open questions).
- Keep the report concise but evidence-rich: cite `file:line`, the source line,
  the wrong output, and the greps you ran.
- End with **Open questions** - genuine ambiguities (is X the same class? should
  we fix H2 siblings now or in a follow-up plan?) - so the caller can decide
  rather than you assuming.

## What not to do

- Do not patch only the reported call site.
- Do not declare "no siblings" without stating what you swept.
- Do not hand-edit generated files to hide the symptom; fix the script.
- Do not change source text to make a converter pass without user approval.
- Do not invent a plan folder or edit production code - report, then let the
  plan/build pipeline act.

## Reference precedents

- Concrete precedents accumulate in the READMEs and commit history. Record every
  new class in the relevant README (or a `SPECS/` plan) so it becomes a
  searchable precedent.
- The governing invariant to cite for every conversion bug: **the source files
  are the truth; the modules are the only producers of the Unicode CSV/TEI-XML
  outputs. A wrong output is a script bug or a source bug, never something to
  patch by hand.**
