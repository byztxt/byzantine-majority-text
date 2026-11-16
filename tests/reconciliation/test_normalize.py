import unittest

from byz.reconcile import normalize


class NormalizeTests(unittest.TestCase):
    def test_official_ccat_to_current_style(self):
        line = "     01:02 {P} )Abraa\\m e)ge/nnhsen to\\n )Isaa/k:"
        self.assertEqual(
            normalize.official_ccat_line(line),
            "01:02 ? *)ABRAA\\M E)GE/NNHSEN TO\\N *)ISAA/K:",
        )

    def test_circumflex_and_iota_subscript(self):
        self.assertEqual(
            normalize.official_ccat_line("     15:55 *(/A|dh"),
            "15:55 *(/AD|H",
        )

    def test_star_moves_after_leading_brackets(self):
        self.assertEqual(
            normalize.official_ccat_line("     12:47 {N x > *[EI)=PEN }"),
            "12:47 {N X > [*EI)=PEN }",
        )

    def test_parse_cct(self):
        verses = normalize.parse_cct(
            "# header\n     01:01 Bi/blos\n     01:02 {P} )Abraa\\m\n"
        )
        self.assertEqual(verses[(1, 1)], "*BI/BLOS")
        self.assertEqual(verses[(1, 2)], "? *)ABRAA\\M")

    def test_transliterate_greek(self):
        self.assertEqual(
            normalize.transliterate_greek("βιβλος γενεσεως"),
            "biblos genesews",
        )

    def test_map_official_ascii(self):
        self.assertEqual(normalize.map_official_ascii("biblov yamar cristou"), "biblos qamar xristou")

    def test_parse_ascii_one_line_and_wrapped(self):
        one_line = normalize.parse_ascii("1:1 biblov genesewv\n1:2 abraam\n")
        self.assertEqual(one_line[(1, 1)], "biblos genesews")
        wrapped = normalize.parse_ascii("     1:1 biblov genesewv\nihsou\n")
        self.assertEqual(wrapped[(1, 1)], "biblos genesews ihsou")


if __name__ == "__main__":
    unittest.main()
