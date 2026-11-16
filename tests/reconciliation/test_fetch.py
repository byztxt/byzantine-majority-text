import tempfile
import unittest
import zipfile
from pathlib import Path

from byz.reconcile import fetch


class FetchTests(unittest.TestCase):
    def test_sha256_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x"
            path.write_bytes(b"abc")
            self.assertEqual(
                fetch.sha256_file(path),
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            )

    def test_extract(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.zip"
            with zipfile.ZipFile(path, "w") as zf:
                zf.writestr("MT.CCT", b"x")
            dest = Path(tmp) / "out"
            fetch.extract(path, dest)
            self.assertTrue((dest / "MT.CCT").is_file())

    def test_existing_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rp2018.toml"
            path.write_text(
                'edition = "rp2018"\n\n[[archives]]\nname = "a.zip"\n'
                'sha256 = "abc"\n',
                encoding="utf-8",
            )
            self.assertEqual(fetch._existing_hashes(path), {"a.zip": "abc"})


if __name__ == "__main__":
    unittest.main()
