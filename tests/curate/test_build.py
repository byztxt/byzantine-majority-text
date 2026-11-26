import importlib.util
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from byz.contract import paths
from byz.curate import build, editions
from byz.reconcile import sources


@unittest.skipUnless(
    importlib.util.find_spec("beta_code") is not None,
    "beta_code is not installed",
)
class ConverterPackageTests(unittest.TestCase):
    """The converter is package code, never a script imported by path."""

    def test_converter_lives_in_the_package(self):
        from byz.beta import converter

        self.assertTrue(
            hasattr(converter, "convert_beta_to_unicode_strongs")
        )

    def test_build_uses_the_package_converter(self):
        self.assertEqual(build._buc().__name__, "byz.beta.converter")

    def test_input_groups_are_under_data_for_every_edition(self):
        for edition_id in build.editions.EDITIONS:
            edition = build.editions.metadata(edition_id)
            groups = build._input_groups(edition)
            self.assertTrue(groups, edition_id)
            for root, includes in groups:
                self.assertTrue(root.startswith("data/"), (edition_id, root))
                self.assertFalse(root.startswith("editions/"), (edition_id, root))
                self.assertTrue(includes, (edition_id, root))


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
            parsed, numbers_only, text_only = build.parse_parsed_ub5(path)
            self.assertEqual(parsed[(1, 1)], "βιβλος 976 {N-NSF} γενεσεως 1078 {N-GSF}")
            self.assertEqual(numbers_only[(1, 1)], "βιβλος 976 γενεσεως 1078")
            self.assertEqual(text_only[(1, 1)], "βιβλος γενεσεως")

    def test_parse_bp5_strongs(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "01_MAT.BP5"
            path.write_text(
                "01.01 biblos 976 {N-NSF} genesews 1078 {N-GSF}\n"
                "01.02\n",
                encoding="utf-8",
            )
            with_parsing, numbers_only, plain_text = build.parse_bp5_strongs(
                path
            )
            self.assertEqual(
                with_parsing[(1, 1)],
                "βιβλος 976 {N-NSF} γενεσεως 1078 {N-GSF}",
            )
            self.assertEqual(
                numbers_only[(1, 1)],
                "βιβλος 976 γενεσεως 1078",
            )
            self.assertEqual(plain_text[(1, 1)], "βιβλος γενεσεως")
            for view in (with_parsing, numbers_only, plain_text):
                self.assertEqual(view[(1, 2)], "")

    def test_strongs_converter_has_three_distinct_shapes(self):
        from byz.beta import converter

        body = "biblos 976 {N-NSF} genesews 1078 {N-GSF}"
        self.assertEqual(
            converter.convert_beta_to_unicode_strongs(
                body, converter.STRONGS_WITH_PARSING
            ),
            "βιβλος 976 {N-NSF} γενεσεως 1078 {N-GSF}",
        )
        self.assertEqual(
            converter.convert_beta_to_unicode_strongs(
                body, converter.STRONGS_NUMBERS_ONLY
            ),
            "βιβλος 976 γενεσεως 1078",
        )
        self.assertEqual(
            converter.convert_beta_to_unicode_strongs(
                body, converter.STRONGS_PLAIN_TEXT
            ),
            "βιβλος γενεσεως",
        )

    def test_strongs_converter_rejects_an_unknown_mode(self):
        from byz.beta import converter

        with self.assertRaises(ValueError) as caught:
            converter.convert_beta_to_unicode_strongs("biblos 976", "typo")
        self.assertIn("typo", str(caught.exception))

    def test_strongs_converter_numbers_only_collapses_repeated_numbers(self):
        from byz.beta import converter

        self.assertEqual(
            converter.convert_beta_to_unicode_strongs(
                "gh 1093 {N-NSF} 1093 {N-VSF}",
                converter.STRONGS_NUMBERS_ONLY,
            ),
            "γη 1093",
        )

    def test_strongs_converter_numbers_only_keeps_distinct_alternatives(self):
        from byz.beta import converter

        self.assertEqual(
            converter.convert_beta_to_unicode_strongs(
                "prwton 4412 {A-ASN} 4413 {A-ASN}",
                converter.STRONGS_NUMBERS_ONLY,
            ),
            "πρωτον 4412 4413",
        )

    def test_strongs_converter_modes_are_unchanged_apart_from_numbers_only(self):
        from byz.beta import converter

        body = "gh 1093 {N-NSF} 1093 {N-VSF}"
        self.assertEqual(
            converter.convert_beta_to_unicode_strongs(
                body, converter.STRONGS_WITH_PARSING
            ),
            "γη 1093 {N-NSF} 1093 {N-VSF}",
        )
        self.assertEqual(
            converter.convert_beta_to_unicode_strongs(
                body, converter.STRONGS_PLAIN_TEXT
            ),
            "γη",
        )

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
                    [present],
                    ["MAT", "MAR"],
                    "data/raw/repo/rp2018-2023/ccat",
                    "rp2018-2023",
                )
            message = str(caught.exception)
            self.assertIn("rp2018-2023", message)
            self.assertIn("data/raw/repo/rp2018-2023/ccat", message)
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
            parsed, numbers_only, text_only = build.parse_parsed_ub5(
                path,
                reference={(24, 6): "ος παρελθων κελευσας"},
            )
            self.assertEqual(text_only[(1, 2)], "εγεννησεν γη")
            self.assertEqual(
                numbers_only[(1, 2)],
                "εγεννησεν 1080 γη 1093",
            )
            self.assertEqual(
                parsed[(1, 2)],
                "εγεννησεν 1080 {V-AAI-3S} γη 1093 {N-NSF} 1093 {N-VSF}",
            )
            self.assertNotIn("VAR", parsed[(5, 39)])
            self.assertNotIn("<", parsed[(5, 39)])
            self.assertNotIn("|", parsed[(5, 39)])
            self.assertIn("δεξιαν", text_only[(5, 39)])
            self.assertIn("σιαγονα", text_only[(5, 39)])
            # The `(24:7)` and `(24:8)` segments belong to the current verse
            # because their words are found in its reference text.
            self.assertEqual(text_only[(24, 6)], "ος παρελθων κελευσας")
            self.assertEqual(text_only[(24, 7)], "παρ ου")
            self.assertEqual(text_only[(24, 8)], "κελευσας τους")
            self.assertEqual(parsed[(1, 3)], "εκπερισσου 4053 {ADV}")
            self.assertEqual(
                parsed[(1, 4)], "διενθυμουμενου 1760 {V-PNP-GSM}"
            )

    def test_parse_parsed_ub5_raises_on_an_unmatched_segment(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "MT.UB5"
            path.write_text(
                "     1:1 biblov 976 {N-NSF} (9:9) xulon 3586 {N-ASN}\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError) as caught:
                build.parse_parsed_ub5(
                    path, reference={(1, 1): "βιβλος", (9, 9): ""}
                )
            message = str(caught.exception)
            self.assertIn("unmatched", message)
            self.assertIn("9:9", message)

    def test_parse_parsed_ub5_requires_a_reference_for_a_segment(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "MT.UB5"
            path.write_text(
                "     1:1 biblov 976 {N-NSF} (1:2) xulon 3586 {N-ASN}\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError) as caught:
                build.parse_parsed_ub5(path)
            self.assertIn("no reference text", str(caught.exception))

    def test_parse_parsed_ub5_raises_when_a_segment_target_has_no_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "MT.UB5"
            path.write_text(
                "     1:1 biblov 976 {N-NSF} (1:2) xulon 3586 {N-ASN}\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError) as caught:
                build.parse_parsed_ub5(
                    path, reference={(1, 1): "βιβλος", (1, 2): "ξυλον"}
                )
            message = str(caught.exception)
            self.assertIn("1:2", message)
            self.assertIn("no parsed line", message)

    def test_ub5_numbers_only_collapses_only_identical_alternatives(self):
        number_only = build._parse_ub5_text(
            "gh 1093 {N-NSF} 1093 {N-VSF} prwton 4412 {A} 4413 {B}",
            "test",
        )[1]
        self.assertEqual(number_only, "γη 1093 πρωτον 4412 4413")

    @unittest.skipUnless(
        importlib.util.find_spec("beta_code") is not None,
        "beta_code is not installed",
    )
    def test_parse_cct_accented_has_no_literal_pipe(self):
        path = (
            build.editions.ROOT
            / "data/raw/print/rp2018/ccat/MR.CCT"
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
    """`parse_cct_current` reads the all-lowercase `data/raw/repo/rp2018-2023/ccat` dialect.

    It is deliberately separate from `parse_cct_accented`, which serves the
    mixed-case official `.CCT` archives and therefore capitalises the text.
    """

    @classmethod
    def setUpClass(cls):
        cls.ccat = paths.CCAT_DIR

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
            'biblov 976 {N-NSF} "+" [[ "shorter ending" ]]',
            self.buc.STRONGS_WITH_PARSING,
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


def _rel_hashes(root):
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _write_minimal_official_tree(base, canonical=None, sections=None):
    """Create a tiny official ASCII/CCAT tree under `base`."""
    canonical = canonical if canonical is not None else list(
        paths.CANONICAL_BOOKS
    )
    sections = sections if sections is not None else list(paths.SECTION_ABBRS)
    ascii_dir = base / "data" / "raw" / "print" / "rp2005" / "ascii"
    ccat_dir = base / "data" / "raw" / "print" / "rp2005" / "ccat"
    ascii_dir.mkdir(parents=True)
    ccat_dir.mkdir(parents=True)
    for abbr in canonical:
        code = sources.ABBR_TO_OFFICIAL[abbr]
        (ascii_dir / f"{code}_Byz.txt").write_text(
            "1:1 biblov\n", encoding="utf-8"
        )
    for abbr in list(canonical) + list(sections):
        code = sources.ABBR_TO_OFFICIAL[abbr]
        (ccat_dir / f"{code}.CCT").write_text(
            "     01:01 biblov\n", encoding="utf-8"
        )
    return ascii_dir, ccat_dir


class OfficialBookSetTests(unittest.TestCase):
    """The official build must never shrink silently."""

    def test_committed_official_outputs_stay_byte_identical(self):
        for edition_id in ("rp2005", "rp2018"):
            edition = editions.metadata(edition_id)
            committed = editions.edition_dir(edition_id)
            with tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / edition_id
                target.mkdir()
                build.build_official(edition, edition_dir=target)
                for view in ("csv", "tei"):
                    self.assertEqual(
                        _rel_hashes(target / view),
                        _rel_hashes(committed / view),
                        f"{edition_id}/{view} differs from the committed edition",
                    )

    def test_shrunken_ascii_tree_fails_loudly(self):
        edition = {
            "id": "rp2005",
            "ascii_dir": "data/raw/print/rp2005/ascii",
            "source_dir": "data/raw/print/rp2005/ccat",
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ascii_dir, ccat_dir = _write_minimal_official_tree(
                root, canonical=["MAT"], sections=[]
            )
            target = root / "editions" / "rp2005"
            target.mkdir(parents=True)
            with mock.patch.object(build.editions, "ROOT", root):
                with self.assertRaises(ValueError) as caught:
                    build.build_official(edition, edition_dir=target)
            message = str(caught.exception)
            self.assertIn("rp2005", message)
            self.assertIn("missing", message)
            self.assertIn("MAR", message)
            self.assertFalse((target / "csv" / "unaccented" / "MAT.csv").exists())

    def test_missing_cct_book_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            _ascii_dir, ccat_dir = _write_minimal_official_tree(Path(tmp))
            (ccat_dir / "MR.CCT").unlink()
            with self.assertRaises(ValueError) as caught:
                build._official_source_maps(
                    Path(tmp) / "data" / "raw" / "print" / "rp2005" / "ascii",
                    ccat_dir,
                    "rp2005",
                )
            self.assertIn("missing", str(caught.exception))
            self.assertIn("MAR", str(caught.exception))

    def test_unknown_cct_book_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            _ascii_dir, ccat_dir = _write_minimal_official_tree(Path(tmp))
            (ccat_dir / "ZZ.CCT").write_text("     01:01 biblov\n", encoding="utf-8")
            with self.assertRaises(ValueError) as caught:
                build._official_source_maps(
                    Path(tmp) / "data" / "raw" / "print" / "rp2005" / "ascii",
                    ccat_dir,
                    "rp2005",
                )
            self.assertIn("ZZ.CCT", str(caught.exception))

    def test_duplicate_cct_book_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            _ascii_dir, ccat_dir = _write_minimal_official_tree(Path(tmp))
            # `MT` and `mt` both map to MAT on a case-sensitive filesystem.
            (ccat_dir / "mt.CCT").write_text("     01:01 biblov\n", encoding="utf-8")
            with self.assertRaises(ValueError) as caught:
                build._official_source_maps(
                    Path(tmp) / "data" / "raw" / "print" / "rp2005" / "ascii",
                    ccat_dir,
                    "rp2005",
                )
            self.assertIn("twice", str(caught.exception))

    def test_greek_cct_is_allowed_and_not_exported(self):
        edition = {
            "id": "rp2005",
            "ascii_dir": "data/raw/print/rp2005/ascii",
            "source_dir": "data/raw/print/rp2005/ccat",
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _ascii_dir, ccat_dir = _write_minimal_official_tree(root)
            (ccat_dir / "GREEK.CCT").write_text(
                "alphabet notes\n", encoding="utf-8"
            )
            target = root / "editions" / "rp2005"
            target.mkdir(parents=True)
            with mock.patch.object(build.editions, "ROOT", root):
                build.build_official(edition, edition_dir=target)
            self.assertTrue(
                (target / "csv" / "unaccented" / "MAT.csv").is_file()
            )
            for view in ("no-variants", "with-variants"):
                self.assertFalse(
                    (
                        target / "csv" / "accented" / view / "GREEK.csv"
                    ).exists()
                )
            self.assertFalse(
                (target / "tei" / "unaccented" / "GREEK.xml").exists()
            )

    def test_committed_greek_cct_is_pinned_but_not_exported(self):
        manifest = json.loads(
            (
                editions.edition_dir("rp2018") / "manifest.json"
            ).read_text(encoding="utf-8")
        )
        pinned = {
            entry["path"]
            for group in manifest["inputs"]
            for entry in group["files"]
            if entry["path"].lower() == "greek.cct"
        }
        self.assertEqual(len(pinned), 1)
        root = editions.edition_dir("rp2018")
        self.assertFalse((root / "csv" / "accented" / "no-variants" / "GREEK.csv").exists())
        self.assertFalse((root / "tei" / "unaccented" / "GREEK.xml").exists())


class BuildStagingTests(unittest.TestCase):
    """A failed build must not touch the committed views or leave staging."""

    def _hashes(self, root):
        return {
            path.relative_to(root).as_posix(): hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

    def test_staging_creates_a_missing_edition_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            final = Path(tmp) / "editions" / "rp2005"
            with mock.patch.object(
                build.editions, "edition_dir", lambda _: final
            ):
                staging, created = build._staging_views("rp2005")
            self.assertEqual(created, final)
            self.assertTrue(final.is_dir())
            self.assertTrue((staging / "csv").is_dir())
            self.assertTrue((staging / "tei").is_dir())

    def test_failed_swap_rolls_back_every_output_at_each_pair(self):
        # Fail at every staged pair after the first: TEI (after CSV), manifest,
        # README, and provenance. Each case must restore all five old outputs.
        for fail_name in ("tei", "manifest.json", "README.md", ".provenance.toml"):
            with self.subTest(fail_name=fail_name):
                with tempfile.TemporaryDirectory() as tmp:
                    final = Path(tmp) / "editions" / "rp2005"
                    final.mkdir(parents=True)
                    staging = Path(tmp) / "editions" / ".rp2005.staging"
                    (staging / "csv").mkdir(parents=True)
                    (staging / "tei").mkdir()
                    (staging / "csv" / "MAT.csv").write_text(
                        "new csv\n", encoding="utf-8"
                    )
                    (staging / "tei" / "MAT.xml").write_text(
                        "new tei\n", encoding="utf-8"
                    )
                    (staging / "manifest.json").write_text(
                        '{"new": true}\n', encoding="utf-8"
                    )
                    (staging / "README.md").write_text(
                        "new readme\n", encoding="utf-8"
                    )
                    (staging / ".provenance.toml").write_text(
                        "new provenance\n", encoding="utf-8"
                    )
                    (final / "csv").mkdir()
                    (final / "csv" / "MAT.csv").write_text(
                        "old csv\n", encoding="utf-8"
                    )
                    (final / "tei").mkdir()
                    (final / "tei" / "MAT.xml").write_text(
                        "old tei\n", encoding="utf-8"
                    )
                    (final / "manifest.json").write_text(
                        '{"old": true}\n', encoding="utf-8"
                    )
                    (final / "README.md").write_text(
                        "old readme\n", encoding="utf-8"
                    )
                    provenance_dir = Path(tmp) / "provenance"
                    provenance_dir.mkdir()
                    provenance_final = provenance_dir / "rp2018-2023.toml"
                    provenance_final.write_text(
                        "old provenance\n", encoding="utf-8"
                    )

                    real_replace = os.replace

                    def flaky_replace(source, destination):
                        # Restoring a backup uses a different source path, so
                        # rollback itself still works.
                        if Path(source) == staging / fail_name:
                            raise OSError("simulated swap failure")
                        return real_replace(source, destination)

                    with mock.patch.object(
                        build.os, "replace", side_effect=flaky_replace
                    ):
                        with self.assertRaises(OSError):
                            build._swap_outputs(
                                staging,
                                final,
                                staging / ".provenance.toml",
                                provenance_final,
                            )

                    self.assertEqual(
                        (final / "csv" / "MAT.csv").read_text(encoding="utf-8"),
                        "old csv\n",
                    )
                    self.assertEqual(
                        (final / "tei" / "MAT.xml").read_text(encoding="utf-8"),
                        "old tei\n",
                    )
                    self.assertEqual(
                        (final / "manifest.json").read_text(encoding="utf-8"),
                        '{"old": true}\n',
                    )
                    self.assertEqual(
                        (final / "README.md").read_text(encoding="utf-8"),
                        "old readme\n",
                    )
                    self.assertEqual(
                        provenance_final.read_text(encoding="utf-8"),
                        "old provenance\n",
                    )
                    self.assertEqual(list(final.rglob(".*.old")), [])
                    self.assertEqual(
                        list(provenance_dir.glob(".*.old")), []
                    )

    def test_last_commit_raises_when_the_path_has_no_history(self):
        with self.assertRaises(ValueError) as caught:
            build._last_commit("path/that/does/not/exist/in/history")
        self.assertIn("no commit history", str(caught.exception))

    def test_write_accented_tei_rejects_an_unknown_csv_stem(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            view = root / "csv" / "accented" / "no-variants"
            view.mkdir(parents=True)
            (view / "TYPO.csv").write_text(
                "chapter,verse,text\n1,1,βιβλος\n", encoding="utf-8"
            )
            with self.assertRaises(ValueError) as caught:
                build.write_accented_tei({"id": "rp2005"}, edition_dir=root)
            self.assertIn("TYPO", str(caught.exception))

    def test_failed_build_leaves_the_committed_views_untouched(self):
        root = editions.edition_dir("rp2005")
        before = self._hashes(root)
        with mock.patch.object(
            build, "build_official", side_effect=ValueError("missing input")
        ):
            with self.assertRaises(ValueError):
                build.build_all()
        self.assertEqual(self._hashes(root), before)
        self.assertEqual(
            [
                path.name
                for path in (editions.EDITIONS_DIR).iterdir()
                if path.name.startswith(".")
            ],
            [],
        )


if __name__ == "__main__":
    unittest.main()
