import importlib.util
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

    def test_parse_parsed_ub5_handles_tvm_multiparse_and_apparatus(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "MT.UB5"
            path.write_text(
                "     1:1 biblov 976 {N-NSF}\n"
                "     1:2 egennhsen 1080 5656 {V-AAI-3S} gh 1093 {N-NSF} 1093 {N-VSF}\n"
                "     5:39 epi 1909 {PREP} | dexian 1188 {A-ASF} | <dexian> 1188 {A-ASF} "
                "VAR: dexian 1188 {A-ASF} sou 4771 {P-2GS} :END | siagona 4600 {N-ASF}\n"
                "     24:6 os 3739 {R-NSM} (24:7) parelqwn 3928 5631 {V-2AAP-NSM} "
                "(24:8) keleusav 2753 5660 {V-AAP-NSM}\n"
                "     24:7 par 3844 {PREP} ou 3739 {R-GSM}\n"
                "     24:8 keleusav 2753 5660 {V-AAP-NSM} touv 3588 {T-APM}\n",
                encoding="utf-8",
            )
            parsed, text_only = build.parse_parsed_ub5(path)
            self.assertEqual(text_only[(1, 2)], "εγεννησεν γη")
            self.assertEqual(
                parsed[(1, 2)],
                "εγεννησεν 1080 {V-AAI-3S} γη 1093 {N-NSF} 1093 {N-VSF}",
            )
            self.assertNotIn("VAR", parsed[(5, 39)])
            self.assertNotIn("<", parsed[(5, 39)])
            self.assertNotIn("|", parsed[(5, 39)])
            self.assertIn("δεξιαν", text_only[(5, 39)])
            self.assertIn("σιαγονα", text_only[(5, 39)])
            self.assertEqual(text_only[(24, 6)], "ος")
            self.assertEqual(text_only[(24, 7)], "παρ ου")
            self.assertEqual(text_only[(24, 8)], "κελευσας τους")

    @unittest.skipUnless(
        importlib.util.find_spec("beta_code") is not None,
        "beta_code is not installed",
    )
    def test_parse_cct_accented_has_no_literal_pipe(self):
        path = (
            build.editions.ROOT
            / "data/raw/rp2018/rp2018-ccat/MR.CCT"
        )
        verses = build.parse_cct_accented(path, drop_variants=True)
        self.assertTrue(verses)
        for key, text in verses.items():
            self.assertNotIn("|", text, f"literal pipe in MR {key}")

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
