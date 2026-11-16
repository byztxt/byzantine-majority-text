"""TEI-XML structure validation for the unaccented export."""

import re
import xml.etree.ElementTree as ET

from . import contracts, paths
from .model import DatasetResult, Violation

NS = "http://www.tei-c.org/ns/1.0"
ANCHOR_RE = re.compile(contracts.TEI_ANCHOR)


def _tag(name):
    return f"{{{NS}}}{name}"


def validate(path, dataset="tei-xml-unicode/no-accents") -> DatasetResult:
    violations = []
    records = []
    try:
        root = ET.parse(str(path)).getroot()
    except ET.ParseError as exc:
        return DatasetResult(
            name=dataset,
            records=[],
            violations=[
                Violation(dataset, str(path), 0, "not-well-formed", str(exc))
            ],
            meta={"books": []},
        )
    if root.tag != _tag("TEI"):
        violations.append(
            Violation(
                dataset, str(path), 0, "bad-root", f"unexpected root {root.tag}"
            )
        )
    book_divs = root.findall(f".//{_tag('div')}[@type='book']")
    if not book_divs:
        violations.append(
            Violation(dataset, str(path), 0, "no-books", "no book divisions found")
        )
    expected_book = path.stem
    seen_anchors = set()
    books = []
    total_chapters = 0
    total_verses = 0
    total_words = 0
    for book_div in book_divs:
        book_id = book_div.get("n", "")
        abbr = paths.BOOK_ID_TO_ABBR.get(book_id)
        if abbr is None:
            violations.append(
                Violation(
                    dataset,
                    str(path),
                    0,
                    "unknown-book",
                    f"unknown book id {book_id!r}",
                )
            )
            continue
        books.append(abbr)
        if expected_book not in ("byz",) and abbr != expected_book:
            violations.append(
                Violation(
                    dataset,
                    str(path),
                    0,
                    "book-mismatch",
                    f"file is {expected_book} but contains {abbr}",
                )
            )
        chapters = book_div.findall(f"{_tag('div')}[@type='chapter']")
        total_chapters += len(chapters)
        for chapter in chapters:
            for verse in chapter.findall(_tag("ab")):
                anchor = verse.get("n", "")
                total_verses += 1
                if not ANCHOR_RE.match(anchor):
                    violations.append(
                        Violation(
                            dataset,
                            str(path),
                            0,
                            "bad-anchor",
                            f"invalid verse anchor {anchor!r}",
                        )
                    )
                    continue
                if anchor in seen_anchors:
                    violations.append(
                        Violation(
                            dataset,
                            str(path),
                            0,
                            "duplicate-anchor",
                            f"duplicate verse anchor {anchor!r}",
                        )
                    )
                seen_anchors.add(anchor)
                match = ANCHOR_RE.match(anchor)
                chapter_number = int(match.group(2))
                verse_number = int(match.group(3))
                words = verse.findall(_tag("w"))
                total_words += len(words)
                records.append(
                    {
                        "book": abbr,
                        "chapter": chapter_number,
                        "verse": verse_number,
                        "n": anchor,
                        "text": "" if not words else "present",
                    }
                )
                if not words:
                    if not contracts.is_intentional_blank(
                        abbr, chapter_number, verse_number
                    ):
                        violations.append(
                            Violation(
                                dataset,
                                str(path),
                                0,
                                "empty-verse",
                                f"empty <ab> that is not an intentional blank: {anchor}",
                            )
                        )
                for word in words:
                    if not (word.text or "").strip():
                        violations.append(
                            Violation(
                                dataset,
                                str(path),
                                0,
                                "empty-word",
                                f"empty <w> in {anchor}",
                            )
                        )
    return DatasetResult(
        name=dataset,
        records=records,
        violations=violations,
        meta={
            "books": books,
            "chapters": total_chapters,
            "verses": total_verses,
            "words": total_words,
            "path": str(path),
        },
    )
