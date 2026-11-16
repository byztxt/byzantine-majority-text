"""BP5 source parsing and structural validation."""

import re

from . import contracts, paths
from .encoding import read_text
from .model import DatasetResult, Violation

FILENAME_RE = re.compile(contracts.BP5_FILENAME)
LINE_RE = re.compile(contracts.BP5_LINE)
STRONGS_RE = re.compile(contracts.BP5_STRONGS)
PARSING_RE = re.compile(contracts.BP5_PARSING)


def book_num(path) -> str:
    match = FILENAME_RE.match(path.name)
    return match.group(1) if match else ""


def validate(path, dataset="source/Strongs") -> DatasetResult:
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
                    "line does not start with chapter.verse",
                    key=line[:40],
                )
            )
            continue
        chapter, verse, rest = match.group(1), match.group(2), match.group(3) or ""
        rest = rest.strip()
        if not rest and not contracts.is_intentional_blank(abbr, chapter, verse):
            violations.append(
                Violation(
                    dataset,
                    str(path),
                    lineno,
                    "blank-record",
                    "verse has a reference but no text",
                    key=f"{abbr} {int(chapter)}:{int(verse)}",
                )
            )
        tokens = rest.split()
        index = 0
        while index < len(tokens):
            word = tokens[index]
            if word.startswith("{") or STRONGS_RE.match(word):
                violations.append(
                    Violation(
                        dataset,
                        str(path),
                        lineno,
                        "orphan-token",
                        "Strong's number or parsing code without a word",
                        key=word[:30],
                    )
                )
                index += 1
                continue
            index += 1
            pairs = 0
            while (
                index + 1 < len(tokens)
                and STRONGS_RE.match(tokens[index])
                and PARSING_RE.match(tokens[index + 1])
            ):
                if int(tokens[index]) <= 0:
                    violations.append(
                        Violation(
                            dataset,
                            str(path),
                            lineno,
                            "bad-strongs",
                            "Strong's number is not positive",
                            key=tokens[index],
                        )
                    )
                pairs += 1
                index += 2
            if pairs == 0:
                violations.append(
                    Violation(
                        dataset,
                        str(path),
                        lineno,
                        "missing-strongs-parsing",
                        "word is not followed by a Strong's number and parsing code",
                        key=word[:30],
                    )
                )
        records.append(
            {
                "book": abbr,
                "num": num,
                "chapter": int(chapter),
                "verse": int(verse),
                "text": rest,
                "line": lineno,
            }
        )
    return DatasetResult(
        name=dataset,
        records=records,
        violations=violations,
        meta={"book": abbr, "num": num, "path": str(path)},
    )
