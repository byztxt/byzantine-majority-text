import tempfile
import unittest
import zipfile
from pathlib import Path

from byz.reconcile import archive


class ArchiveTests(unittest.TestCase):
    def test_inventory_and_format_class(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.zip"
            with zipfile.ZipFile(path, "w") as zf:
                zf.writestr("MT.CCT", b"     01:01 Bi/blos\r\n")
                zf.writestr("MT_Byz.txt", b"1:1 biblov\r\n")
            rows = archive.inventory_archive(path, "rp2018", "fixture.zip")
            by_name = {row["member"]: row for row in rows}
            self.assertEqual(by_name["MT.CCT"]["format"], "ccat")
            self.assertEqual(by_name["MT_Byz.txt"]["format"], "ascii-one-line")
            self.assertEqual(by_name["MT.CCT"]["eol"], "crlf")
            self.assertEqual(by_name["MT.CCT"]["encoding"], "ascii")
            members = archive.load_members(path)
            self.assertIn("MT.CCT", members)


if __name__ == "__main__":
    unittest.main()
