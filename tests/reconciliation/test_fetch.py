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

    def test_extract_removes_stale_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.zip"
            with zipfile.ZipFile(path, "w") as zf:
                zf.writestr("MT.CCT", b"x")
            dest = Path(tmp) / "out"
            dest.mkdir()
            (dest / "stale.txt").write_text("old", encoding="utf-8")
            fetch.extract(path, dest)
            self.assertTrue((dest / "MT.CCT").is_file())
            self.assertFalse((dest / "stale.txt").exists())

    def test_download_keeps_previous_archive_on_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "good.zip"
            dest.write_bytes(b"last known good")
            original = fetch.urllib.request.urlopen

            def unavailable(*args, **kwargs):
                raise OSError("network down")

            fetch.urllib.request.urlopen = unavailable
            try:
                with self.assertRaises(OSError):
                    fetch.download(
                        "https://www.dropbox.com/s/abc/file.zip?dl=0", dest
                    )
            finally:
                fetch.urllib.request.urlopen = original
            self.assertEqual(dest.read_bytes(), b"last known good")
            self.assertFalse(dest.with_name(dest.name + ".part").exists())


class ExtractSafetyTests(unittest.TestCase):
    def _zip(self, tmp, name):
        path = Path(tmp) / "fixture.zip"
        with zipfile.ZipFile(path, "w") as zf:
            zf.writestr(name, b"x")
        return path

    def test_extract_rejects_parent_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._zip(tmp, "../evil.txt")
            dest = Path(tmp) / "out"
            with self.assertRaises(ValueError):
                fetch.extract(path, dest)
            self.assertFalse((Path(tmp) / "evil.txt").exists())

    def test_extract_rejects_absolute_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._zip(tmp, "/tmp/evil.txt")
            with self.assertRaises(ValueError):
                fetch.extract(path, Path(tmp) / "out")


class DownloadUrlTests(unittest.TestCase):
    def test_accepts_https_dropbox(self):
        fetch._check_url("https://www.dropbox.com/s/abc/file.zip?dl=1")
        fetch._check_url(
            "https://ucabc.dl.dropboxusercontent.com/cd/0/get/x/file?dl=1"
        )

    def test_rejects_non_https(self):
        with self.assertRaises(ValueError):
            fetch._check_url("http://www.dropbox.com/s/abc/file.zip")

    def test_rejects_untrusted_host(self):
        with self.assertRaises(ValueError):
            fetch._check_url("https://evil.example.com/file.zip")
        with self.assertRaises(ValueError):
            fetch._check_url("https://dropbox.com.evil.example/file.zip")


class PinnedDigestTests(unittest.TestCase):
    """`run()` must verify every archive against the pinned digest."""

    def test_run_fails_loudly_on_a_wrong_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            original = (
                fetch.sources.ARCHIVES,
                fetch.sources.ARCHIVE_DIR,
                fetch.sources.PROVENANCE_DIR,
                fetch.sources.RAW_DIR,
                fetch.download,
            )

            def fake_download(url, dest):
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(b"not the official archive")
                return {"http_status": 200, "final_url": url}

            fetch.sources.ARCHIVES = [
                {
                    "edition": "rp2018",
                    "name": "fixture.zip",
                    "url": "https://www.dropbox.com/s/abc/fixture.zip?dl=0",
                    "format": "ccat",
                    "sha256": "0" * 64,
                }
            ]
            fetch.sources.ARCHIVE_DIR = tmp / "archives"
            fetch.sources.PROVENANCE_DIR = tmp / "provenance"
            fetch.sources.RAW_DIR = tmp / "raw"
            fetch.download = fake_download
            try:
                with self.assertRaises(SystemExit):
                    fetch.run(verify=True)
            finally:
                (
                    fetch.sources.ARCHIVES,
                    fetch.sources.ARCHIVE_DIR,
                    fetch.sources.PROVENANCE_DIR,
                    fetch.sources.RAW_DIR,
                    fetch.download,
                ) = original


if __name__ == "__main__":
    unittest.main()
