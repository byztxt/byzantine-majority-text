import unittest

from byz.contract.coverage import diff_rows
from byz.contract.model import DatasetResult


def result(name, book, keys):
    records = [
        {"book": book, "chapter": chapter, "verse": verse, "text": "x"}
        for chapter, verse in keys
    ]
    return DatasetResult(name=name, records=records, violations=[], meta={"path": name})


class CoverageTests(unittest.TestCase):
    def test_detects_missing_verse(self):
        results = {
            "source/CCAT": [result("source/CCAT", "MAT", [(1, 1), (1, 2)])],
            "csv-unicode/ccat/no-variants": [
                result("csv-unicode/ccat/no-variants", "MAT", [(1, 1)])
            ],
        }
        rows = diff_rows(results)
        row = next(
            row
            for row in rows
            if row["comparison"] == "CCAT source vs CSV no-variants"
            and row["book"] == "MAT"
        )
        self.assertEqual(row["only_left"], 1)
        self.assertEqual(row["only_right"], 0)
        self.assertEqual(row["examples_only_left"], "1:2")

    def test_ignores_matching_keys(self):
        results = {
            "csv-unicode/strongs/no-parsing": [
                result("csv-unicode/strongs/no-parsing", "MAT", [(1, 1)])
            ],
            "tei-xml-unicode/no-accents": [
                result("tei-xml-unicode/no-accents", "MAT", [(1, 1)])
            ],
        }
        rows = diff_rows(results)
        row = next(
            row
            for row in rows
            if row["comparison"] == "CSV no-parsing vs TEI" and row["book"] == "MAT"
        )
        self.assertEqual(row["only_left"], 0)
        self.assertEqual(row["only_right"], 0)


if __name__ == "__main__":
    unittest.main()
