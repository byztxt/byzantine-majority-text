import tempfile
import unittest
from pathlib import Path

from byz.contract.ccat import validate


def run(text, name="01_MAT.TXT"):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / name
        path.write_text(text, encoding="ascii")
        return validate(path)


class CcatTests(unittest.TestCase):
    def test_valid_line(self):
        result = run("01:01 *BIBLOS {N A > B }\n")
        self.assertEqual(len(result.records), 1)
        self.assertEqual(result.violations, [])
        self.assertEqual(result.records[0]["book"], "MAT")

    def test_bad_prefix(self):
        result = run("nope\n")
        self.assertEqual(result.violations[0].category, "bad-prefix")

    def test_unbalanced_brace(self):
        result = run("01:01 text {N A > B\n")
        self.assertEqual(result.violations[0].category, "unbalanced-brace")

    def test_bad_variant_code(self):
        result = run("01:01 text {Z A > B }\n")
        self.assertEqual(result.violations[0].category, "bad-variant-code")

    def test_omission_marker_is_valid(self):
        result = run("01:01 text {N ~ }\n")
        self.assertEqual(result.violations, [])

    def test_blank_record(self):
        result = run("17:36 \n")
        self.assertEqual(result.violations[0].category, "blank-record")
        self.assertEqual(result.violations[0].key, "MAT 17:36")

    def test_intentional_blank_is_allowed(self):
        result = run("17:36 \n", name="03_LUK.TXT")
        self.assertEqual(result.violations, [])
        self.assertEqual(len(result.records), 1)


if __name__ == "__main__":
    unittest.main()
