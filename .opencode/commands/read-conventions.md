---
description: Review this repository's conventions
---

1. Read the constitution:

- SPECS/MISSION.md
- SPECS/TECH.md
- SPECS/ROADMAP.md

2. Then read these files:

- README.md
- docs/BUILD.md
- data/raw/repo/CONVENTIONS.md
- essay/README.md

`data/raw/repo/CONVENTIONS.md` is the most important: it documents the Beta-code conventions,
the variant codes (N/B/C/M/S/E), the parsing codes, and the Strong's-number
conventions that the build relies on. `docs/BUILD.md` describes how to run the
pipeline; the root README is generated from `src/byz/curate/README.template.md`.

3. Then read the build in `src/byz/curate/` (`build.py`, `materialise.py`,
   `verify.py`, `docs.py`) and the shared converter in `src/byz/beta/`, so you
   understand how the Unicode CSV and TEI-XML derivatives are generated from
   the committed `data/` inputs for each edition.

4. Once you've done that, stand by for further instructions.
