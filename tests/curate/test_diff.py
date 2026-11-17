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
