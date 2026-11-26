import unittest

from byz.contract import paths
from byz.contract.coverage import diff_rows
from byz.contract.model import DatasetResult

NO_VARIANTS = paths.dataset_name("csv/accented/no-variants")
UNACCENTED = paths.dataset_name("csv/unaccented")


def result(name, book, keys):
    records = [
        {"book": book, "chapter": chapter, "verse": verse, "text": "x"}
        for chapter, verse in keys
    ]
    return DatasetResult(name=name, records=records, violations=[], meta={"path": name})


class CoverageTests(unittest.TestCase):
    def test_detects_missing_verse(self):
        results = {
            "data/raw/repo/rp2018-2023/ccat": [result("data/raw/repo/rp2018-2023/ccat", "MAT", [(1, 1), (1, 2)])],
            NO_VARIANTS: [result(NO_VARIANTS, "MAT", [(1, 1)])],
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
            UNACCENTED: [result(UNACCENTED, "MAT", [(1, 1)])],
            paths.TEI_DATASET: [
                result(paths.TEI_DATASET, "MAT", [(1, 1)])
            ],
        }
        rows = diff_rows(results)
        row = next(
            row
            for row in rows
            if row["comparison"] == "CSV unaccented vs TEI" and row["book"] == "MAT"
        )
        self.assertEqual(row["only_left"], 0)
        self.assertEqual(row["only_right"], 0)


if __name__ == "__main__":
    unittest.main()
