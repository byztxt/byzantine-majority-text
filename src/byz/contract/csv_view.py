"""CSV artifact validation for the four generated views."""

import csv
import io

from . import contracts
from .encoding import read_text
from .model import DatasetResult, Violation

HEADER = contracts.CSV_HEADER


def validate(path, dataset) -> DatasetResult:
    text, _ = read_text(path)
    book = path.stem
    reader = csv.reader(io.StringIO(text))
    violations = []
    records = []
    try:
        header = next(reader)
    except StopIteration:
        return DatasetResult(
            name=dataset,
            records=[],
            violations=[
                Violation(dataset, str(path), 0, "empty-file", "CSV is empty")
            ],
            meta={"book": book, "rows": 0},
        )
    if header != HEADER:
        violations.append(
            Violation(
                dataset,
                str(path),
                1,
                "bad-header",
                f"expected {HEADER}, found {header}",
            )
        )
    seen = set()
    for lineno, row in enumerate(reader, 2):
        if len(row) != 3:
            violations.append(
                Violation(
                    dataset,
                    str(path),
                    lineno,
                    "bad-column-count",
                    f"expected 3 columns, found {len(row)}",
                )
            )
            continue
        chapter, verse, body = row
        try:
            chapter_int = int(chapter)
            verse_int = int(verse)
        except ValueError:
            violations.append(
                Violation(
                    dataset,
                    str(path),
                    lineno,
                    "bad-number",
                    f"chapter/verse are not integers: {chapter!r}/{verse!r}",
                )
            )
            continue
        if not body.strip() and not contracts.is_intentional_blank(
            book, chapter_int, verse_int
        ):
            violations.append(
                Violation(
                    dataset,
                    str(path),
                    lineno,
                    "empty-text",
                    "verse text is empty",
                    key=f"{book} {chapter_int}:{verse_int}",
                )
            )
        if "\\" in body:
            violations.append(
                Violation(
                    dataset,
                    str(path),
                    lineno,
                    "beta-code-leftover",
                    "backslash found in Unicode CSV text",
                    key=f"{book} {chapter_int}:{verse_int}",
                )
            )
        key = (chapter_int, verse_int)
        if key in seen:
            violations.append(
                Violation(
                    dataset,
                    str(path),
                    lineno,
                    "duplicate-verse",
                    "duplicate (chapter, verse) key",
                    key=f"{book} {chapter_int}:{verse_int}",
                )
            )
        seen.add(key)
        records.append(
            {
                "book": book,
                "chapter": chapter_int,
                "verse": verse_int,
                "text": body,
                "line": lineno,
            }
        )
    return DatasetResult(
        name=dataset,
        records=records,
        violations=violations,
        meta={"book": book, "rows": len(records), "path": str(path)},
    )
