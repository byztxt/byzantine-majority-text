"""CCAT source parsing and structural validation."""

import re

from . import contracts, paths
from .encoding import read_text
from .model import DatasetResult, Violation

FILENAME_RE = re.compile(contracts.CCAT_FILENAME)
LINE_RE = re.compile(contracts.CCAT_LINE)
VARIANT_PREFIX_RE = re.compile(contracts.CCAT_VARIANT_PREFIX)


def book_num(path) -> str:
    match = FILENAME_RE.match(path.name)
    if not match:
        return ""
    return match.group(1)


def _brace_contents(body: str, path: str, dataset: str, lineno: int, violations):
    depth = 0
    start = None
    contents = []
    for index, char in enumerate(body):
        if char == "{":
            depth += 1
            if depth == 1:
                start = index
            elif depth == 2:
                violations.append(
                    Violation(
                        dataset, str(path), lineno, "nested-brace", "nested '{' in variant"
                    )
                )
        elif char == "}":
            depth -= 1
            if depth < 0:
                violations.append(
                    Violation(
                        dataset,
                        str(path),
                        lineno,
                        "unbalanced-brace",
                        "unexpected '}'",
                    )
                )
                depth = 0
                start = None
            elif depth == 0 and start is not None:
                contents.append(body[start + 1 : index])
                start = None
    if depth != 0:
        violations.append(
            Violation(
                dataset, str(path), lineno, "unbalanced-brace", "unclosed '{'"
            )
        )
    return contents


def validate(path, dataset="source/CCAT") -> DatasetResult:
    text, _ = read_text(path)
    num = book_num(path)
    abbr = paths.NUM_TO_ABBR.get(num, num)
    records = []
    violations = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            violations.append(
                Violation(dataset, str(path), lineno, "blank-line", "empty line")
            )
            continue
        match = LINE_RE.match(line)
        if not match:
            violations.append(
                Violation(
                    dataset,
                    str(path),
                    lineno,
                    "bad-prefix",
                    "line does not start with chapter:verse",
                    key=line[:40],
                )
            )
            continue
        chapter, verse, rest = match.group(1), match.group(2), match.group(3) or ""
        body = rest[2:] if rest.startswith("? ") else rest
        if not body.strip() and not contracts.is_intentional_blank(
            abbr, chapter, verse
        ):
            violations.append(
                Violation(
                    dataset,
                    str(path),
                    lineno,
                    "blank-record",
                    "verse reference is present but the text is empty",
                    key=f"{abbr} {int(chapter)}:{int(verse)}",
                )
            )
        for content in _brace_contents(body, str(path), dataset, lineno, violations):
            parts = content.split(None, 1)
            payload = parts[1] if len(parts) == 2 else ""
            if not VARIANT_PREFIX_RE.match(content):
                violations.append(
                    Violation(
                        dataset,
                        str(path),
                        lineno,
                        "bad-variant-code",
                        "variant does not begin with a known code",
                        key=content[:30],
                    )
                )
            if ">" not in content and payload.strip() != "~":
                violations.append(
                    Violation(
                        dataset,
                        str(path),
                        lineno,
                        "bad-variant-payload",
                        "variant has no '>' separator (or '~' omission marker)",
                        key=content[:30],
                    )
                )
        records.append(
            {
                "book": abbr,
                "num": num,
                "chapter": int(chapter),
                "verse": int(verse),
                "text": body,
                "line": lineno,
            }
        )
    return DatasetResult(
        name=dataset,
        records=records,
        violations=violations,
        meta={"book": abbr, "num": num, "path": str(path)},
    )
