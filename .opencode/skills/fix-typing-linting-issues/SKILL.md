---
name: fix-typing-linting-issues
description: Guide for fixing Python syntax, typing, or linting issues in the conversion scripts. Use when a checker surfaces problems (py_compile, ruff, mypy, flake8, editor warnings) or before claiming a script is clean.
---

Best practices for fixing typing and linting issues in this repo:

- Fix all the issues, including pre-existing ones in the file you are touching.
- Do not add ignore flags (`# noqa`, `# type: ignore`, `# pyright: ignore`, etc.)
  unless strictly necessary, and explain why when you do.
- Do not bypass or delete checks to make them pass.
- Do not upgrade or add dependencies to work around a checker. The scripts pin
  `pandas==1.4.2` and `beta-code==1.0.0` in `scripts/requirements.txt`; ask the
  user before changing that file.
- Keep Python 3.10 compatibility.

There is no configured linter or type-checker in this repository. To confirm a
script is at least syntactically valid, run:

```bash
python3 -m py_compile scripts/csv_converter.py scripts/tei_xml_converter.py scripts/beta_to_unicode_custom/*.py
```

If you introduce a checker (ruff, mypy, etc.), get the user's agreement, add it
to `scripts/requirements.txt`, and document the command in `scripts/README.md`.
