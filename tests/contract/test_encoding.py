import unittest

from byz.contract.encoding import detect_encoding, detect_eol


class EncodingTests(unittest.TestCase):
    def test_ascii(self):
        self.assertEqual(detect_encoding(b"abc\n"), "ascii")

    def test_utf8(self):
        self.assertEqual(detect_encoding("βιβλος".encode("utf-8")), "utf-8")

    def test_utf8_bom(self):
        self.assertEqual(detect_encoding(b"\xef\xbb\xbfabc"), "utf-8-sig")

    def test_cp1252(self):
        self.assertEqual(detect_encoding(b"\x93quote\x94"), "cp1252")

    def test_eol(self):
        self.assertEqual(detect_eol(b"a\nb\n"), "lf")
        self.assertEqual(detect_eol(b"a\r\nb\r\n"), "crlf")
        self.assertEqual(detect_eol(b"a\r\nb\n"), "mixed")
        self.assertEqual(detect_eol(b"abc"), "none")


if __name__ == "__main__":
    unittest.main()
