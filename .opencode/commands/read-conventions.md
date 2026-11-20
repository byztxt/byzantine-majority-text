---
description: Review this repository's conventions
---

1. Read the constitution:

- SPECS/MISSION.md
- SPECS/TECH.md
- SPECS/ROADMAP.md

2. Then read these files:

- README.md
- source/README.md
- scripts/README.md
- essay/README.md

`source/README.md` is the most important: it documents the Beta-code conventions,
the variant codes (N/B/C/M/S/E), the parsing codes, and the Strong's-number
conventions that the build relies on. The other READMEs describe each folder's
purpose and how to run the pipeline.

3. Then read the build in `src/byz/curate/` (`build.py`, `recover.py`,
   `docs.py`) and the shared converter in
   `scripts/beta_to_unicode_custom/`, so you understand how the Unicode CSV and
   TEI-XML derivatives are generated from each edition's `source/` snapshot.

4. Once you've done that, stand by for further instructions.
