---
name: fix-typing-linting-issues
description: Guide for fixing Python syntax, typing, or linting issues in the conversion modules. Use when a checker surfaces problems (py_compile, ruff, mypy, flake8, editor warnings) or before claiming a module is clean.
---

Best practices for fixing typing and linting issues in this repo:

- Fix all the issues, including pre-existing ones in the file you are touching.
- Do not add ignore flags (`# noqa`, `# type: ignore`, `# pyright: ignore`, etc.)
  unless strictly necessary, and explain why when you do.
- Do not bypass or delete checks to make them pass.
- Do not upgrade or add dependencies to work around a checker. The modules pin
  `beta-code==1.0.0` in `requirements.txt` at the repository root; ask the user
  before changing that file.
- Keep Python 3.10 compatibility.

There is no configured linter or type-checker in this repository. To confirm the
modules are at least syntactically valid, run:

```bash
find src -name '*.py' -print0 | xargs -0 python3 -m py_compile
```

If you introduce a checker (ruff, mypy, etc.), get the user's agreement, add it
to `requirements.txt`, and document the command in `docs/BUILD.md`.
