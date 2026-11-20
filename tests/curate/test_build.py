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

    def test_parse_bp5_strongs(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "01_MAT.BP5"
            path.write_text(
                "01.01 biblos 976 {N-NSF} genesews 1078 {N-GSF}\n"
                "01.02\n",
                encoding="utf-8",
            )
            with_parsing, without_parsing = build.parse_bp5_strongs(path)
            self.assertEqual(
                with_parsing[(1, 1)],
                "βιβλος 976 {N-NSF} γενεσεως 1078 {N-GSF}",
            )
            self.assertEqual(without_parsing[(1, 1)], "βιβλος γενεσεως")
            self.assertEqual(with_parsing[(1, 2)], "")
            self.assertEqual(without_parsing[(1, 2)], "")

    def test_abbr_for_rejects_an_unknown_book(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "99_XXX.BP5"
            path.write_text("01.01 biblos 976 {N-NSF}\n", encoding="utf-8")
            with self.assertRaises(ValueError) as caught:
                build._abbr_for(path)
            self.assertIn("99_XXX.BP5", str(caught.exception))

    def test_abbr_for_rejects_mismatched_prefix(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "02_MAT.BP5"
            path.write_text("01.01 biblos 976 {N-NSF}\n", encoding="utf-8")
            with self.assertRaises(ValueError) as caught:
                build._abbr_for(path)
            self.assertIn("02_MAT.BP5", str(caught.exception))

    def test_check_source_books_names_the_edition_and_missing_book(self):
        with tempfile.TemporaryDirectory() as tmp:
            present = Path(tmp) / "01_MAT.TXT"
            present.write_text("", encoding="utf-8")
            with self.assertRaises(ValueError) as caught:
                build._check_source_books(
                    [present], ["MAT", "MAR"], "source/CCAT", "rp2018-2023"
                )
            message = str(caught.exception)
            self.assertIn("rp2018-2023", message)
            self.assertIn("source/CCAT", message)
            self.assertIn("MAR", message)

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
                "     24:8 keleusav 2753 5660 {V-AAP-NSM} touv 3588 {T-APM}\n"
                "     1:3 ekperissou 0 4053 {ADV}\n"
                "     1:4 dienqumoumenou 0 1760 5740 {V-PNP-GSM}\n",
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
            self.assertEqual(parsed[(1, 3)], "εκπερισσου 4053 {ADV}")
            self.assertEqual(
                parsed[(1, 4)], "διενθυμουμενου 1760 {V-PNP-GSM}"
            )

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

    def test_tei_marks_punctuation_and_paragraphs(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "MAT.xml"
            verses = {(1, 1): "¶Καὶ - λόγος"}
            build.write_tei(path, [("MAT", "B01", verses)])
            text = path.read_text()
            self.assertIn('<milestone unit="paragraph" type="start"/>', text)
            self.assertIn("<pc>-</pc>", text)
            self.assertNotIn("<w>-</w>", text)
            self.assertIn("<w>λόγος</w>", text)


@unittest.skipUnless(
    importlib.util.find_spec("beta_code") is not None,
    "beta_code is not installed",
)
class CurrentCctReaderTests(unittest.TestCase):
    """`parse_cct_current` reads the all-lowercase `source/CCAT` dialect.

    It is deliberately separate from `parse_cct_accented`, which serves the
    mixed-case official `.CCT` archives and therefore capitalises the text.
    """

    @classmethod
    def setUpClass(cls):
        cls.ccat = build.editions.ROOT / "source" / "CCAT"

    def test_matches_mat_1_1(self):
        verses = build.parse_cct_current(self.ccat / "01_MAT.TXT", drop_variants=True)
        self.assertEqual(
            verses[(1, 1)],
            "Βίβλος γενέσεως Ἰησοῦ χριστοῦ, υἱοῦ Δαυίδ, υἱοῦ Ἀβραάμ.",
        )

    def test_blank_verse_stays_an_empty_record(self):
        # LUK 17:36 is intentionally blank in the Byzantine tradition and the
        # source carries an empty verse line, not a missing one.
        verses = build.parse_cct_current(self.ccat / "03_LUK.TXT", drop_variants=True)
        self.assertIn((17, 36), verses)
        self.assertEqual(verses[(17, 36)], "")

    def test_paragraph_line_becomes_a_paragraph_marker(self):
        # The source writes a paragraph start as a leading `? ` on the verse
        # line (MAT 1:2).
        verses = build.parse_cct_current(self.ccat / "01_MAT.TXT", drop_variants=True)
        self.assertTrue(verses[(1, 2)].startswith("¶"))
        self.assertNotIn("? ", verses[(1, 2)])

    def test_two_references_in_one_line_name_the_file_and_line(self):
        # `CURRENT_VERSE_RE` is unanchored, so a second `NN:NN` in the verse
        # text would make the reader truncate it. The guard must fail loudly
        # and name the file and line instead of guessing.
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "01_MAT.TXT"
            path.write_text("1:1 biblov 2:3 genesewv\n", encoding="utf-8")
            with self.assertRaises(ValueError) as caught:
                build.parse_cct_current(path, drop_variants=True)
        message = str(caught.exception)
        self.assertIn("01_MAT.TXT:1", message)
        self.assertIn("found 2", message)


@unittest.skipUnless(
    importlib.util.find_spec("beta_code") is not None,
    "beta_code is not installed",
)
class ApparatusLiteralTests(unittest.TestCase):
    """Apparatus literals must survive the historical converter.

    Quoted notes (`[[ "..." ]]`) and the exact `"+"` are natural-language
    apparatus text, not beta code. They used to be transliterated
    (`"shorter ending"` -> `σηορτερ ενδινγ`) and rendered as a diaeresis
    (`"+"` -> `" ̈"`).
    """

    @classmethod
    def setUpClass(cls):
        cls.buc = build._buc()

    def test_quoted_note_and_literal_plus_are_preserved(self):
        for note in ('[[ "shorter ending" ]]', '[["SHORTER ENDING"]]'):
            text = self.buc.convert_beta_to_unicode(
                f'GA/R. {{N GA/R > GA/R "+" {note}}}'
            )
            self.assertIn(note, text)
            self.assertIn('"+"', text)
            self.assertNotIn("σηορτερ", text)
            self.assertNotIn('" ̈"', text)

    def test_greek_variant_brackets_still_convert(self):
        # `[[` is also the Greek variant delimiter; only quoted notes are
        # protected, so the variant text keeps going through beta_code.
        text = self.buc.convert_beta_to_unicode(
            "{N *KAI\\ > [[*KAI\\ } E)POREU/QH"
        )
        self.assertIn("[[Καὶ", text)
        self.assertNotIn("[[*", text)

    def test_strongs_path_preserves_apparatus_literals(self):
        text = self.buc.convert_beta_to_unicode_strongs(
            'biblov 976 {N-NSF} "+" [[ "shorter ending" ]]', False
        )
        self.assertIn('[[ "shorter ending" ]]', text)
        self.assertIn('"+"', text)
        self.assertNotIn("σηορτερ", text)

    def test_production_parser_preserves_literal_case_and_spacing(self):
        # `production_ccat_line` upper-cases the line and collapses the spaces
        # around `[[ ]]`; the production parser must protect the raw literals
        # first so their case and spacing survive.
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "MR.CCT"
            path.write_text(
                '     16:08 KAI\\ E)GENETO {N ga/r > ga/r "+" '
                '[[ "shorter ending" ]]}\n',
                encoding="utf-8",
            )
            text = build.parse_cct_accented(path, drop_variants=False)[(16, 8)]
        self.assertIn('[[ "shorter ending" ]]', text)
        self.assertIn('"+"', text)
        self.assertNotIn("σηορτερ", text)
        # The rest of the line still goes through the production normaliser.
        self.assertIn("ΓΕΝΕΤΟ", text)


class ProductionNormalizeTests(unittest.TestCase):
    """The production wrapper must keep the comparison default untouched."""

    def test_comparison_default_is_unchanged(self):
        from byz.reconcile import normalize

        line = "     14:65 Kai\\ e)/ballon.{B e)/ballon > e)/balon }"
        self.assertEqual(
            normalize.official_ccat_line(line),
            normalize.official_ccat_line(line, reorder_iota=True),
        )
        self.assertIn("*E)/BALLON.{B", normalize.official_ccat_line(line))

    def test_production_splits_word_from_glued_code(self):
        from byz.reconcile import normalize

        line = "     14:65 Kai\\ e)/ballon.{B e)/ballon > e)/balon }"
        normalized = normalize.production_ccat_line(line)
        self.assertIn("E)/BALLON.{B", normalized)
        self.assertNotIn("*E)/BALLON", normalized)

    def test_production_marks_each_abbreviation_letter(self):
        from byz.reconcile import normalize

        normalized = normalize.production_ccat_line("     03:07 {B Daui/d > _DAD }")
        self.assertIn("_*D*A*D", normalized)

    def test_production_reorders_iota_subscript(self):
        from byz.reconcile import normalize

        normalized = normalize.production_ccat_line("     02:06 mimnh|/skh|")
        self.assertIn("MIMNH/|SKH|", normalized)


if __name__ == "__main__":
    unittest.main()
