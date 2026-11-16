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
