import hashlib
import io
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from byz.reconcile import fetch


class _FakeResponse:
    """Minimal stand-in for the object returned by urllib."""

    status = 200
    headers = {}

    def __init__(self, payload):
        self._chunks = [payload]

    def geturl(self):
        return "https://www.dropbox.com/s/abc/file.zip?dl=1"

    def read(self, size):
        return self._chunks.pop(0) if self._chunks else b""

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class DownloadTests(unittest.TestCase):
    URL = "https://www.dropbox.com/s/abc/file.zip?dl=0"

    def test_successful_download_writes_archive_atomically(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "file.zip"
            dest.write_bytes(b"old archive")
            response = _FakeResponse(b"official archive bytes")
            with mock.patch.object(
                fetch.urllib.request, "urlopen", return_value=response
            ) as urlopen:
                meta = fetch.download(self.URL, dest)
            self.assertTrue(urlopen.called)
            request = urlopen.call_args[0][0]
            self.assertTrue(request.full_url.endswith("?dl=1"))
            self.assertEqual(dest.read_bytes(), b"official archive bytes")
            self.assertFalse(dest.with_name(dest.name + ".part").exists())
            self.assertEqual(meta["http_status"], 200)
            self.assertEqual(
                meta["final_url"],
                "https://www.dropbox.com/s/abc/file.zip?dl=1",
            )

    def test_failed_download_keeps_previous_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "good.zip"
            dest.write_bytes(b"last known good")
            with mock.patch.object(
                fetch.urllib.request,
                "urlopen",
                side_effect=OSError("network down"),
            ):
                with self.assertRaises(OSError):
                    fetch.download(self.URL, dest)
            self.assertEqual(dest.read_bytes(), b"last known good")
            self.assertFalse(dest.with_name(dest.name + ".part").exists())


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


class ForceModeTests(unittest.TestCase):
    """`--force` is the only mode that downloads, extracts, and records."""

    def test_force_downloads_extracts_and_writes_provenance(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            archive.writestr("MT.CCT", b"x")
        payload = buffer.getvalue()
        expected = hashlib.sha256(payload).hexdigest()
        spec = {
            "edition": "rp2018",
            "name": "fixture.zip",
            "url": "https://www.dropbox.com/s/abc/fixture.zip?dl=0",
            "format": "ccat",
            "sha256": expected,
        }

        def fake_download(url, dest):
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(payload)
            return {
                "http_status": 200,
                "final_url": url.replace("?dl=0", "?dl=1"),
            }

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with (
                mock.patch.object(fetch.sources, "ARCHIVES", [spec]),
                mock.patch.object(
                    fetch.sources, "ARCHIVE_DIR", root / "archives"
                ),
                mock.patch.object(
                    fetch.sources, "PROVENANCE_DIR", root / "provenance"
                ),
                mock.patch.object(fetch.sources, "RAW_DIR", root / "raw"),
                mock.patch.object(fetch.sources, "ROOT", root),
                mock.patch.object(
                    fetch, "download", side_effect=fake_download
                ) as download,
            ):
                written = fetch.run(force=True)

            archive = root / "archives" / "rp2018" / "fixture.zip"
            self.assertEqual(download.call_count, 1)
            self.assertEqual(archive.read_bytes(), payload)
            self.assertTrue(
                (root / "raw" / "rp2018" / "fixture" / "MT.CCT").is_file()
            )
            provenance = root / "provenance" / "rp2018.toml"
            self.assertEqual(written, [provenance])
            text = provenance.read_text(encoding="utf-8")
            self.assertIn(f'sha256 = "{expected}"', text)
            self.assertIn(f"size = {len(payload)}", text)
            self.assertIn("downloaded = ", text)


class VerifyModeTests(unittest.TestCase):
    """`--verify` is pure validation: no downloads and no provenance writes."""

    def test_verify_all_present_leaves_provenance_byte_identical(self):
        before = {
            path.name: fetch.sha256_file(path)
            for path in sorted(fetch.sources.PROVENANCE_DIR.glob("*.toml"))
        }
        with mock.patch.object(
            fetch, "download", side_effect=AssertionError("network access")
        ):
            written = fetch.run(verify=True)
        after = {
            path.name: fetch.sha256_file(path)
            for path in sorted(fetch.sources.PROVENANCE_DIR.glob("*.toml"))
        }
        self.assertEqual(written, [])
        self.assertEqual(after, before)

    def test_verify_missing_archive_fails_without_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(fetch.sources, "ARCHIVE_DIR", Path(tmp)):
                with mock.patch.object(
                    fetch, "download", side_effect=AssertionError("network access")
                ):
                    with self.assertRaises(SystemExit) as caught:
                        fetch.run(verify=True)
        message = str(caught.exception)
        self.assertIn("archive missing", message)
        self.assertIn("git checkout --", message)

    def test_verify_corrupt_archive_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "rp2018" / "fixture.zip"
            archive.parent.mkdir(parents=True)
            archive.write_bytes(b"not the official archive")
            spec = {
                "edition": "rp2018",
                "name": "fixture.zip",
                "url": "https://www.dropbox.com/s/abc/fixture.zip?dl=0",
                "format": "ccat",
                "sha256": "0" * 64,
            }
            with mock.patch.object(fetch.sources, "ARCHIVES", [spec]):
                with mock.patch.object(fetch.sources, "ARCHIVE_DIR", root):
                    with mock.patch.object(fetch.sources, "ROOT", root):
                        with mock.patch.object(
                            fetch,
                            "download",
                            side_effect=AssertionError("network access"),
                        ):
                            with self.assertRaises(SystemExit) as caught:
                                fetch.run(verify=True)
        self.assertIn("does not match the pinned sha256", str(caught.exception))

    def test_verify_and_force_are_mutually_exclusive(self):
        with self.assertRaises(SystemExit):
            fetch.run(verify=True, force=True)


if __name__ == "__main__":
    unittest.main()
