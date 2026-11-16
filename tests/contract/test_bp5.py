import tempfile
import unittest
from pathlib import Path

from byz.contract.bp5 import validate


def run(text, name="01_MAT.BP5"):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / name
        path.write_text(text, encoding="ascii")
        return validate(path)


class Bp5Tests(unittest.TestCase):
    def test_valid_line(self):
        result = run("01.01 biblos 976 {N-NSF} genesews 1078 {N-GSF}\n")
        self.assertEqual(result.violations, [])
        self.assertEqual(result.records[0]["book"], "MAT")

    def test_multiparsing_is_valid(self):
        result = run("01.01 to 3588 {T-NSN} 3588 {T-ASN}\n")
        self.assertEqual(result.violations, [])

    def test_missing_parsing(self):
        result = run("01.01 biblos 976\n")
        self.assertEqual(result.violations[0].category, "missing-strongs-parsing")

    def test_blank_record(self):
        result = run("17.36 \n")
        self.assertEqual(result.violations[0].category, "blank-record")
        self.assertEqual(result.violations[0].key, "MAT 17:36")

    def test_bad_prefix(self):
        result = run("nope\n")
        self.assertEqual(result.violations[0].category, "bad-prefix")

    def test_intentional_blank_is_allowed(self):
        result = run("17.36 \n", name="03_LUK.BP5")
        self.assertEqual(result.violations, [])
        self.assertEqual(len(result.records), 1)


if __name__ == "__main__":
    unittest.main()
