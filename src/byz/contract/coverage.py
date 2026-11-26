"""Book/verse coverage matrix and cross-dataset key comparison."""

from . import paths

COMPARISONS = [
    (
        paths.CCAT_DATASET,
        paths.dataset_name("csv/accented/no-variants"),
        "CCAT source vs CSV no-variants",
    ),
    (
        paths.CCAT_DATASET,
        paths.dataset_name("csv/accented/with-variants"),
        "CCAT source vs CSV with-variants",
    ),
    (
        paths.BP5_DATASET,
        paths.dataset_name("csv/strongs/no-parsing"),
        "Strong's source vs CSV no-parsing",
    ),
    (
        paths.BP5_DATASET,
        paths.dataset_name("csv/strongs/with-parsing"),
        "Strong's source vs CSV with-parsing",
    ),
    (
        paths.BP5_DATASET,
        paths.dataset_name("csv/unaccented"),
        "Strong's source vs CSV unaccented",
    ),
    (
        paths.dataset_name("csv/unaccented"),
        paths.TEI_DATASET,
        "CSV unaccented vs TEI",
    ),
]

# The columns of `reports/baseline/books.csv` and `differences.csv`. Declared
# once so the header written for an empty result and the row dicts cannot drift
# apart.
BOOK_FIELDS = (
    "dataset",
    "book",
    "file",
    "chapters",
    "verses",
    "min_chapter",
    "max_chapter",
    "min_verse",
    "max_verse",
    "blank",
)

DIFFERENCE_FIELDS = (
    "comparison",
    "left",
    "right",
    "book",
    "left_verses",
    "right_verses",
    "only_left",
    "only_right",
    "examples_only_left",
    "examples_only_right",
)


def _books(results):
    books = {}
    for result in results:
        for record in result.records:
            books.setdefault(record["book"], []).append(record)
    return books


def book_rows(results):
    rows = []
    for dataset, items in results.items():
        for result in items:
            for book, records in _books([result]).items():
                keys = {(r["chapter"], r["verse"]) for r in records}
                chapters = {r["chapter"] for r in records}
                row = {
                    "dataset": dataset,
                    "book": book,
                    "file": result.meta.get("path", ""),
                    "chapters": len(chapters),
                    "verses": len(keys),
                    "min_chapter": min(chapters) if chapters else "",
                    "max_chapter": max(chapters) if chapters else "",
                    "min_verse": min(k[1] for k in keys) if keys else "",
                    "max_verse": max(k[1] for k in keys) if keys else "",
                    "blank": sum(1 for r in records if not str(r.get("text", "")).strip()),
                }
                rows.append(row)
    rows.sort(key=lambda row: (row["dataset"], row["book"]))
    return rows


def _key_sets(results, dataset):
    sets = {}
    for result in results.get(dataset, []):
        for record in result.records:
            sets.setdefault(record["book"], set()).add(
                (record["chapter"], record["verse"])
            )
    return sets


def diff_rows(results):
    rows = []
    for left, right, label in COMPARISONS:
        left_sets = _key_sets(results, left)
        right_sets = _key_sets(results, right)
        for book in sorted(set(left_sets) | set(right_sets)):
            left_keys = left_sets.get(book, set())
            right_keys = right_sets.get(book, set())
            only_left = sorted(left_keys - right_keys)
            only_right = sorted(right_keys - left_keys)
            rows.append(
                {
                    "comparison": label,
                    "left": left,
                    "right": right,
                    "book": book,
                    "left_verses": len(left_keys),
                    "right_verses": len(right_keys),
                    "only_left": len(only_left),
                    "only_right": len(only_right),
                    "examples_only_left": " ".join(
                        f"{c}:{v}" for c, v in only_left[:5]
                    ),
                    "examples_only_right": " ".join(
                        f"{c}:{v}" for c, v in only_right[:5]
                    ),
                }
            )
    return rows


def dataset_summary(results):
    rows = []
    for dataset in sorted(results):
        items = results[dataset]
        books = sorted(_books(items))
        verses = sum(len(r.records) for r in items)
        keys = set()
        for result in items:
            for record in result.records:
                keys.add((record["book"], record["chapter"], record["verse"]))
        rows.append(
            {
                "dataset": dataset,
                "files": len(items),
                "books": len(books),
                "book_list": " ".join(books),
                "verses": verses,
                "unique_verses": len(keys),
            }
        )
    return rows
