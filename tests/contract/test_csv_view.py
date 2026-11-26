import tempfile
import unittest
from pathlib import Path

from byz.contract import paths
from byz.contract.csv_view import validate


def run(text, name="MAT.csv"):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / name
        path.write_text(text, encoding="utf-8")
        return validate(path, "test")


class CsvTests(unittest.TestCase):
    def test_valid(self):
        result = run("chapter,verse,text\n1,1,βιβλος\n")
        self.assertEqual(result.violations, [])
        self.assertEqual(len(result.records), 1)

    def test_bad_header(self):
        result = run("chapter,text\n1,βιβλος\n")
        self.assertEqual(result.violations[0].category, "bad-header")

    def test_duplicate_verse(self):
        result = run("chapter,verse,text\n1,1,a\n1,1,b\n")
        self.assertEqual(result.violations[0].category, "duplicate-verse")

    def test_empty_text(self):
        result = run("chapter,verse,text\n1,1,\n")
        self.assertEqual(result.violations[0].category, "empty-text")

    def test_beta_code_leftover(self):
        result = run("chapter,verse,text\n1,1,bi\\\\blos\n")
        self.assertEqual(result.violations[0].category, "beta-code-leftover")

    def test_intentional_blank_is_allowed(self):
        result = run("chapter,verse,text\n17,36,\n", name="LUK.csv")
        self.assertEqual(result.violations, [])
        self.assertEqual(len(result.records), 1)

    def test_unaccented_rejects_numbers_and_braces(self):
        dataset = paths.dataset_name("csv/unaccented")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "MAT.csv"
            path.write_text(
                "chapter,verse,text\n1,1,βιβλος 976 {N-NSF}\n",
                encoding="utf-8",
            )
            result = validate(path, dataset)
        categories = {violation.category for violation in result.violations}
        self.assertEqual(categories, {"unexpected-strongs", "unexpected-parsing"})

    def test_numbers_only_rejects_braces_and_requires_numbers(self):
        dataset = paths.dataset_name("csv/strongs/no-parsing")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "MAT.csv"
            path.write_text(
                "chapter,verse,text\n"
                "1,1,βιβλος 976\n"
                "1,2,γενεσεως {N-GSF}\n"
                "1,3,ιησου\n"
                "1,4,γη 1093 1093\n",
                encoding="utf-8",
            )
            result = validate(path, dataset)
        categories = [violation.category for violation in result.violations]
        self.assertIn("unexpected-parsing", categories)
        self.assertIn("missing-strongs", categories)
        self.assertIn("repeated-strongs", categories)

    def test_numbers_only_accepts_the_real_shape(self):
        dataset = paths.dataset_name("csv/strongs/no-parsing")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "MAT.csv"
            path.write_text(
                "chapter,verse,text\n1,1,βιβλος 976 γενεσεως 1078\n",
                encoding="utf-8",
            )
            result = validate(path, dataset)
        self.assertEqual(result.violations, [])


if __name__ == "__main__":
    unittest.main()
