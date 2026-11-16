import tempfile
import unittest
from pathlib import Path

from byz.curate import build


class BuildTests(unittest.TestCase):
    def test_ascii_to_greek(self):
        self.assertEqual(build.ascii_to_greek("biblov"), "βιβλος")
        self.assertEqual(build.ascii_to_greek("yamar"), "θαμαρ")

    def test_parse_ascii_main(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "MT_Byz.txt"
            path.write_text("1:1 biblov genesewv\n1:2 abraam\n", encoding="utf-8")
            verses = build.parse_ascii_main(path)
            self.assertEqual(verses[(1, 1)], "βιβλος γενεσεως")
            self.assertEqual(verses[(1, 2)], "αβρααμ")

    def test_parse_parsed_ub5(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "MT.UB5"
            path.write_text(
                "     1:1 biblov 976 {N-NSF} genesewv 1078 {N-GSF}\n",
                encoding="utf-8",
            )
            parsed, text_only = build.parse_parsed_ub5(path)
            self.assertEqual(parsed[(1, 1)], "βιβλος 976 {N-NSF} γενεσεως 1078 {N-GSF}")
            self.assertEqual(text_only[(1, 1)], "βιβλος γενεσεως")

    def test_write_csv_and_tei_empty_verse(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "MAT.csv"
            tei_path = Path(tmp) / "MAT.xml"
            verses = {(1, 1): "βιβλος", (1, 2): ""}
            build.write_csv(csv_path, verses)
            self.assertIn("chapter,verse,text", csv_path.read_text())
            build.write_tei(
                tei_path, [("MAT", "B01", verses)], edition_label="2005"
            )
            text = tei_path.read_text()
            self.assertIn('<ab n="B01K1V2"/>', text)
            self.assertIn('<edition n="2005">', text)

    def test_tei_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "a.xml"
            second = Path(tmp) / "b.xml"
            verses = {(1, 1): "βιβλος γενεσεως"}
            build.write_tei(first, [("MAT", "B01", verses)])
            build.write_tei(second, [("MAT", "B01", verses)])
            self.assertEqual(first.read_text(), second.read_text())


if __name__ == "__main__":
    unittest.main()
