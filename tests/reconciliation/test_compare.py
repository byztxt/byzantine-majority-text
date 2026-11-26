import string
import unittest

from byz.reconcile import compare


class CompareTests(unittest.TestCase):
    def test_classify_apparatus_code(self):
        self.assertEqual(
            compare.classify_diff("text {C x > y }", "text {N x > y }"),
            "apparatus-code",
        )

    def test_classify_apparatus_code_is_not_the_old_name(self):
        # C1: the value names the tier (apparatus) and what changed (the code),
        # because the reading is unchanged.  The old name is gone, not aliased.
        self.assertNotEqual(
            compare.classify_diff("text {C x > y }", "text {N x > y }"),
            "variant-code",
        )

    def test_classify_variant_content(self):
        self.assertEqual(
            compare.classify_diff("text {E a > - } more", "text more"),
            "variant",
        )

    def test_classify_capitalization(self):
        self.assertEqual(compare.classify_diff("*word", "word"), "capitalization")

    def test_classify_capitalization_with_apparatus(self):
        # MAR 14:2: rp2005 has lowercase `E)/LEGON`, the current source the
        # capital `*)/ELEGON`.  The shared apparatus must not force `letters`.
        self.assertEqual(
            compare.classify_diff(
                "*)/ELEGON DE/, {N DE/ > GA/R } *MH\\ E)N TH=| E(ORTH=|.",
                "E)/LEGON DE/, {N DE/ > GA/R } *MH\\ E)N TH=| E(ORTH=|.",
            ),
            "capitalization",
        )

    def test_classify_capitalization_with_breathing_before_letter(self):
        # LUK 7:4: the capital `*)/ACIO/S` and lowercase `A)/CIO/S` differ
        # only in where beta code puts the breathing relative to the letter.
        self.assertEqual(
            compare.classify_diff(
                "LE/GONTES O(/TI A)/CIO/S E)STIN {N PARE/CEI > PARE/CH| }.",
                "LE/GONTES O(/TI *)/ACIO/S E)STIN {N PARE/CEI > PARE/CH| }.",
            ),
            "capitalization",
        )

    def test_classify_punctuation_wins_over_capitalization(self):
        # MAT 1:18 changes both punctuation (`.` -> `:`) and capitalisation.
        self.assertEqual(
            compare.classify_diff(
                "OU(/TWS H)=N: MNHSTEUQEI/SHS GA\\R {N GA\\R > - }.",
                "OU(/TWS H)=N. *MNHSTEUQEI/SHS GA\\R {N GA\\R > - }.",
            ),
            "punctuation",
        )

    def test_classify_word_segmentation(self):
        self.assertEqual(compare.classify_diff("mhti", "mh ti"), "word-segmentation")

    def test_classify_punctuation(self):
        self.assertEqual(compare.classify_diff("a: b", "a, b"), "punctuation")

    def test_classify_accents(self):
        self.assertEqual(compare.classify_diff("a\\b", "a/b"), "accents-breathings")

    def test_classify_letters(self):
        self.assertEqual(compare.classify_diff("abc", "abd"), "letters")

    def test_compare_maps(self):
        metrics = compare.compare_maps(
            {(1, 1): "a", (1, 2): "b"}, {(1, 1): "a", (1, 3): "c"}
        )
        self.assertEqual(metrics["verses"], 3)
        self.assertEqual(metrics["verses_match"], 1)
        self.assertEqual(metrics["only_current"], 1)
        self.assertEqual(metrics["only_official"], 1)

    def test_pure_whitespace_reaches_the_variant_branch(self):
        # `_main_text` collapses whitespace before the comparison, so a
        # whitespace-only difference never reaches the `whitespace` branch.
        # This is documented in the README rather than re-engineered.
        self.assertEqual(compare.classify_diff("a b", "a  b"), "variant")


class VocabularyTests(unittest.TestCase):
    def test_category_meanings_cover_the_classifier_in_precedence_order(self):
        self.assertEqual(
            list(compare.CATEGORY_MEANINGS),
            [
                "missing",
                "variant",
                "apparatus-code",
                "capitalization",
                "word-segmentation",
                "whitespace",
                "punctuation",
                "accents-breathings",
                "letters",
            ],
        )

    def test_every_classifier_result_has_a_meaning(self):
        fixtures = [
            ("a", "a"),
            ("a", ""),
            ("x {N a > b }", "x {C a > b }"),
            ("*word", "word"),
            ("mhti", "mh ti"),
            ("a b", "a  b"),
            ("a: b", "a, b"),
            ("a\\b", "a/b"),
            ("abc", "abd"),
        ]
        for current, official in fixtures:
            category = compare.classify_diff(current, official)
            if category:
                self.assertIn(category, compare.CATEGORY_MEANINGS, category)

    def test_apparatus_code_names_cover_the_regex(self):
        # A new letter in `VARIANT_CODE_RE` must arrive with a witness name.
        # Probe every printable character, not just A-Z, so widening the
        # character class - for example to a lowercase letter - fails here
        # instead of shipping a nameless code.
        expected = set(
            compare.VARIANT_CODE_RE.findall(
                "".join("{" + c for c in string.printable)
            )
        )
        self.assertEqual(set(compare.APPARATUS_CODE_NAMES), expected)
        # `data/raw/repo/CONVENTIONS.md` fixes the order and spelling of the six names.
        self.assertEqual(list(compare.APPARATUS_CODE_NAMES), list("NBCMSE"))

    def test_contract_vocabulary_is_not_a_diff_category(self):
        # `bad-variant-code` is a source-validation violation, not a diff
        # category, and is deliberately absent from this vocabulary.
        self.assertNotIn("bad-variant-code", compare.CATEGORY_MEANINGS)
        self.assertNotIn("variant-code", compare.CATEGORY_MEANINGS)


if __name__ == "__main__":
    unittest.main()
