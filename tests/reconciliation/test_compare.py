import unittest

from byz.reconcile import compare


class CompareTests(unittest.TestCase):
    def test_classify_variant_code(self):
        self.assertEqual(
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


if __name__ == "__main__":
    unittest.main()
