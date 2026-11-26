"""Unit tests for the word-diff helpers used by the edition reports."""

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from byz.curate import diff, editions
from byz.reconcile import compare


class WordDiffTests(unittest.TestCase):
    def test_identical_text_is_unchanged(self):
        text = "ἐν ἀρχῇ ἦν ὁ λόγος."
        self.assertEqual(diff.word_diff(text, text), text)

    def test_replacement_marks_only_the_changed_word(self):
        self.assertEqual(
            diff.word_diff("ὁ λόγος ἦν", "ὁ λόγος ἐστίν"),
            "ὁ λόγος [-ἦν-]{+ἐστίν+}",
        )

    def test_insertion_marks_only_the_added_word(self):
        self.assertEqual(
            diff.word_diff("ἐν ἀρχῇ ἦν λόγος", "ἐν ἀρχῇ ἦν ὁ λόγος"),
            "ἐν ἀρχῇ ἦν {+ὁ+} λόγος",
        )

    def test_deletion_marks_only_the_removed_word(self):
        self.assertEqual(
            diff.word_diff("ἐν ἀρχῇ ἦν ὁ λόγος", "ἐν ἀρχῇ ἦν λόγος"),
            "ἐν ἀρχῇ ἦν [-ὁ-] λόγος",
        )

    def test_punctuation_change_marks_the_word(self):
        self.assertEqual(
            diff.word_diff("τοῦ κόσμου, τοῦ", "τοῦ κόσμου τοῦ"),
            "τοῦ [-κόσμου,-]{+κόσμου+} τοῦ",
        )
        self.assertEqual(
            diff.word_diff("λόγος,", "λόγος·"),
            "[-λόγος,-]{+λόγος·+}",
        )

    def test_multiple_changes_are_each_marked(self):
        self.assertEqual(
            diff.word_diff("α β γ δ", "α γ δ"),
            "α [-β-] γ δ",
        )
        self.assertEqual(
            diff.word_diff("ὁ λόγος", "τὸν λόγον"),
            "[-ὁ-]{+τὸν+} [-λόγος-]{+λόγον+}",
        )

    def test_pure_whitespace_change_is_not_marked(self):
        self.assertEqual(diff.word_diff("ἐν  ἀρχῇ", "ἐν ἀρχῇ"), "ἐν ἀρχῇ")
        self.assertEqual(diff.word_diff("ἐν ἀρχῇ", "ἐν  ἀρχῇ"), "ἐν  ἀρχῇ")
        marker = diff.word_diff("ἐν  ἀρχῇ", "ἐν ἀρχῇ")
        self.assertNotIn("[-", marker)
        self.assertNotIn("{+", marker)

    def test_markers_wrap_changed_words_not_the_whole_verse(self):
        left = "¶Καὶ ὁ ἕβδομος ἄγγελος ἐσάλπισεν, καὶ ἐγένοντο φωναί."
        right = "¶Καὶ ὁ ἕβδομος ἄγγελος ἐσάλπισεν, καὶ ἐγένοντο φωναί·"
        result = diff.word_diff(left, right)
        self.assertTrue(result.startswith("¶Καὶ ὁ ἕβδομος ἄγγελος"))
        self.assertIn("[-φωναί.-]{+φωναί·+}", result)

    def test_source_tier_beta_code(self):
        result = diff.word_diff(
            "EI) MH/ TI A)\\N", "EI) MH/TI A)\\N"
        )
        self.assertEqual(result, "EI) [-MH/ TI-]{+MH/TI+} A)\\N")


class ApparatusWordDiffTests(unittest.TestCase):
    """R6: the with-variants view renders the apparatus in Unicode."""

    def test_word_diff_marks_a_variant_reading(self):
        left = diff.load_text("rp2005", "with-variants")[("ROM", 1, 27)]
        right = diff.load_text("rp2018", "with-variants")[("ROM", 1, 27)]
        self.assertIn("{Byz", right)
        self.assertNotIn("{Byz", left)
        result = diff.word_diff(
            diff.normalize_text(left), diff.normalize_text(right)
        )
        self.assertIn("{+{Byz τε > δε }+}", result)
        self.assertIn("ὁμοίως τε", result)

    def test_word_diff_of_identical_variant_text_has_no_markers(self):
        left = diff.load_text("rp2018", "with-variants")[("MAT", 11, 23)]
        right = diff.load_text("rp2018-2023", "with-variants")[("MAT", 11, 23)]
        left = diff.normalize_text(left)
        right = diff.normalize_text(right)
        self.assertEqual(left, right)
        self.assertEqual(diff.word_diff(left, right), left)
        self.assertNotIn("[-", diff.word_diff(left, right))

    def test_load_text_can_read_the_variants_view(self):
        variants = diff.load_text("rp2018", "with-variants")[("ROM", 1, 27)]
        main = diff.load_text("rp2018")[("ROM", 1, 27)]
        self.assertIn("{Byz", variants)
        self.assertNotIn("{", main)
        self.assertEqual(
            main, diff.load_text("rp2018", "no-variants")[("ROM", 1, 27)]
        )

    def test_load_text_rejects_an_unknown_view(self):
        # A typo must not look like an empty edition.
        with self.assertRaises(ValueError):
            diff.load_text("rp2018", "with-variant")

    def test_load_text_reports_a_missing_view_directory(self):
        with self.assertRaises(FileNotFoundError):
            diff.load_text("no-such-edition")


class SourceBookGuardTests(unittest.TestCase):
    """A shrunken source tree must not silently shrink a diff."""

    def test_official_loader_rejects_a_missing_book(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ccat = root / "data" / "raw" / "print" / "rp2005" / "ccat"
            ccat.mkdir(parents=True)
            (ccat / "MT.CCT").write_text(
                "     01:01 biblov\n", encoding="utf-8"
            )
            with mock.patch.object(diff.editions, "ROOT", root):
                with self.assertRaises(ValueError) as caught:
                    diff._load_official("rp2005")
            self.assertIn("missing", str(caught.exception))
            self.assertIn("MAR", str(caught.exception))

    def test_current_loader_rejects_an_unknown_book(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ccat = root / "data" / "raw" / "repo" / "rp2018-2023" / "ccat"
            ccat.mkdir(parents=True)
            (ccat / "99_XXX.TXT").write_text(
                "1:1 biblov\n", encoding="utf-8"
            )
            with mock.patch.object(diff.editions, "ROOT", root):
                with self.assertRaises(ValueError) as caught:
                    diff._load_current("rp2018-2023")
            self.assertIn("99_XXX.TXT", str(caught.exception))


class TagChangeTests(unittest.TestCase):
    """C3: the report states the code change in its own direction."""

    def test_tag_change_is_reported_in_direction(self):
        self.assertEqual(
            diff.tag_change("x {N a > b }", "x {C a > b }"), "N -> C"
        )

    def test_tag_change_deduplicates_repeated_positions(self):
        self.assertEqual(
            diff.tag_change("{N a }{N b }", "{S a }{S b }"), "N -> S"
        )

    def test_tag_change_is_empty_when_codes_match(self):
        self.assertEqual(diff.tag_change("x {N a > b }", "x {N a > b }"), "")

    def test_tag_change_lists_distinct_changes(self):
        self.assertEqual(
            diff.tag_change("{N a }{B b }", "{C a }{M b }"), "N -> C; B -> M"
        )

    def test_tag_change_falls_back_to_full_sequences(self):
        # Defensive: the classifier does not produce unequal counts.
        self.assertEqual(diff.tag_change("{N a }", "{C a }{M b }"), "N -> C,M")

    def test_tag_line_uses_the_category_noun_and_code_spans(self):
        self.assertEqual(
            diff.tag_line("x {N a > b }", "x {C a > b }"),
            "Apparatus code: `N` -> `C` (the reading is unchanged)",
        )
        self.assertEqual(diff.tag_line("x {N a }", "x {N a }"), "")


class ReadmeCategoryTests(unittest.TestCase):
    """R4: every classifier category is documented with a worked example."""

    def test_glossary_section_exists(self):
        self.assertIn("## Categories", diff.README_TEXT)

    def test_every_category_is_in_the_table(self):
        for category in compare.CATEGORY_MEANINGS:
            self.assertIn(f"| `{category}` |", diff.README_TEXT)

    def test_table_order_follows_the_classifier(self):
        positions = [
            diff.README_TEXT.index(f"| `{category}` |")
            for category in compare.CATEGORY_MEANINGS
        ]
        self.assertEqual(positions, sorted(positions))

    def test_precedence_sentence_is_present(self):
        self.assertIn(
            "The classifier applies these tests in order", diff.README_TEXT
        )

    def test_both_worked_examples_are_present(self):
        self.assertIn("`ACT 1:15` in `rp2018--rp2018-2023`", diff.README_TEXT)
        self.assertIn("`1CO 3:14` in `rp2005--rp2018`", diff.README_TEXT)
        self.assertIn("the reading is unchanged", diff.README_TEXT)

    def test_variant_and_apparatus_code_are_distinguished(self):
        text = " ".join(diff.README_TEXT.split())
        self.assertIn("`variant` means the apparatus *reading or note* changed", text)
        self.assertIn(
            "`apparatus-code` means only the code *letter* changed", text
        )

    def test_apparatus_code_names_sentence_lists_every_witness(self):
        for name in compare.APPARATUS_CODE_NAMES.values():
            self.assertIn(name, diff.README_TEXT)
        self.assertIn("`{N` is spelled `{NA`", diff.README_TEXT)
        self.assertIn("`{C` is spelled `{NA27/28`", diff.README_TEXT)

    def test_old_name_does_not_appear_in_the_readme(self):
        self.assertNotIn("variant-code", diff.README_TEXT)

    def test_missing_categories_say_so(self):
        self.assertIn("none in the current reports", diff.README_TEXT)

    def test_blank_verses_are_present_in_every_edition(self):
        text = " ".join(diff.README_TEXT.split())
        self.assertIn(
            "Every curated edition, including `rp2005-2019`, carries them as "
            "present empty records",
            text,
        )
        self.assertNotIn("absent in `rp2005-2019`", text)
        self.assertNotIn("ignores row presence", text)


class NormalizeTextTests(unittest.TestCase):
    def test_paragraph_marker_is_ignored(self):
        self.assertEqual(
            diff.normalize_text("¶Καὶ ὁ λόγος"),
            diff.normalize_text("Καὶ ὁ λόγος"),
        )

    def test_apostrophe_typography_is_normalised(self):
        self.assertEqual(
            diff.normalize_text("τοῦτ’ ἔστιν"),
            "τοῦτ' ἔστιν",
        )
        self.assertEqual(
            diff.normalize_text("‘τοῦτ’ ἔστιν"),
            "'τοῦτ' ἔστιν",
        )

    def test_whitespace_is_collapsed(self):
        self.assertEqual(
            diff.normalize_text("  ἐν \n ἀρχῇ  "),
            "ἐν ἀρχῇ",
        )

    def test_dash_spacing_is_preserved(self):
        # The source-tier comparison canonicalises `\s*-\s*` to ` - `; the
        # derived-text comparison must not, so raw dash spacing survives.
        self.assertNotEqual(
            diff.normalize_text("τοῦ ἀμνοῦ - τοῦ θεοῦ"),
            diff.normalize_text("τοῦ ἀμνοῦ- τοῦ θεοῦ"),
        )
        self.assertEqual(
            diff.normalize_text("ἀμνοῦ-  τοῦ"),
            "ἀμνοῦ- τοῦ",
        )


if __name__ == "__main__":
    unittest.main()
