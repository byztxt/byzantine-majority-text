import tempfile
import unittest
from pathlib import Path

from byz.contract.tei_view import validate

TEI = """<?xml version="1.0" encoding="utf-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <text><body>
    <div type="book" n="B01">
      <div type="chapter" n="B01K1">
        <ab n="B01K1V1"><w>βιβλος</w><w>γενεσεως</w></ab>
      </div>
    </div>
  </body></text>
</TEI>
"""


def run(text, name="MAT.xml"):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / name
        path.write_text(text, encoding="utf-8")
        return validate(path, "test")


class TeiTests(unittest.TestCase):
    def test_valid(self):
        result = run(TEI)
        self.assertEqual(result.violations, [])
        self.assertEqual(len(result.records), 1)

    def test_empty_word(self):
        result = run(TEI.replace("<w>γενεσεως</w>", "<w> </w>"))
        self.assertEqual(result.violations[0].category, "empty-word")

    def test_duplicate_anchor(self):
        duplicate = """<?xml version="1.0" encoding="utf-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <text><body>
    <div type="book" n="B01">
      <div type="chapter" n="B01K1">
        <ab n="B01K1V1"><w>a</w></ab>
        <ab n="B01K1V1"><w>b</w></ab>
      </div>
    </div>
  </body></text>
</TEI>
"""
        result = run(duplicate)
        self.assertEqual(result.violations[0].category, "duplicate-anchor")

    def test_bad_anchor(self):
        result = run(TEI.replace("B01K1V1", "BAD"))
        self.assertEqual(result.violations[0].category, "bad-anchor")

    def test_not_well_formed(self):
        result = run(TEI.replace("</TEI>", ""))
        self.assertEqual(result.violations[0].category, "not-well-formed")


if __name__ == "__main__":
    unittest.main()
