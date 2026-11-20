"""Unit tests for the word-diff helpers used by the edition reports."""

import unittest

from byz.curate import diff


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
