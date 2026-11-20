import hashlib
import io
import tempfile
import unittest
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from byz import generated
from byz.reconcile import fetch, sources


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


def _zip_payload():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("MT.CCT", b"x")
    return buffer.getvalue()


def _fixture_spec(payload, edition="rp2018"):
    return {
        "edition": edition,
        "name": "fixture.zip",
        "url": "https://www.dropbox.com/s/abc/fixture.zip?dl=0",
        "format": "ccat",
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def _provenance_record(name="fixture.zip"):
    return {
        "name": name,
        "format": "ccat",
        "source_page": sources.SOURCE_PAGE,
        "requested_url": "https://www.dropbox.com/s/abc/fixture.zip?dl=0",
        "download_url": "https://www.dropbox.com/s/abc/fixture.zip?dl=1",
        "final_url": "https://recorded.example/file?dl=1",
        "http_status": 200,
        "downloaded": "2026-11-16T18:37:00Z",
        "size": 1234,
        "sha256": "a" * 64,
        "extracted": "data/raw/rp2018/fixture",
    }


class _FixedDatetime:
    @classmethod
    def now(cls, tz=None):
        return datetime(2026, 11, 19, 12, 0, 0, tzinfo=timezone.utc)


def _run_force_in(root, spec, payload):
    """Run `--force` against a temporary root and return the written TOMLs."""

    def fake_download(url, dest):
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(payload)
        return {"http_status": 200, "final_url": url.replace("?dl=0", "?dl=1")}

    with (
        mock.patch.object(fetch.sources, "ARCHIVES", [spec]),
        mock.patch.object(fetch.sources, "ARCHIVE_DIR", root / "archives"),
        mock.patch.object(fetch.sources, "PROVENANCE_DIR", root / "provenance"),
        mock.patch.object(fetch.sources, "RAW_DIR", root / "raw"),
        mock.patch.object(fetch.sources, "ROOT", root),
        mock.patch.object(fetch, "download", side_effect=fake_download),
    ):
        written = fetch.run(force=True)
    return {path.name: path.read_text(encoding="utf-8") for path in written}


class WriteProvenanceTests(unittest.TestCase):
    RECORDS = [
        _provenance_record("a.zip"),
        _provenance_record("b.zip"),
        _provenance_record("c.zip"),
    ]

    def _write(self, records):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(sources, "PROVENANCE_DIR", Path(tmp)):
                path = fetch._write_provenance("rp2018", records)
                return path.read_text(encoding="utf-8")

    def test_write_provenance_puts_source_page_on_every_record(self):
        text = self._write(self.RECORDS)
        self.assertEqual(text.count("[[archives]]"), 3)
        self.assertEqual(
            text.count(f'source_page = "{sources.SOURCE_PAGE}"'), 3
        )

    def test_write_provenance_places_source_page_after_format(self):
        text = self._write(self.RECORDS)
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if line == 'format = "ccat"':
                self.assertEqual(
                    lines[index + 1], f'source_page = "{sources.SOURCE_PAGE}"'
                )

    def test_write_provenance_starts_with_the_toml_banner(self):
        lines = self._write(self.RECORDS).splitlines()
        self.assertEqual(lines[:3], generated.toml_header())
        self.assertEqual(lines[3], "")
        self.assertEqual(lines[4], 'edition = "rp2018"')

    def test_write_provenance_is_deterministic(self):
        first = self._write(self.RECORDS)
        second = self._write(self.RECORDS)
        self.assertEqual(first, second)
        self.assertEqual(first.count("2026-11-16T18:37:00Z"), 3)
        self.assertNotIn(datetime.now(timezone.utc).strftime("%Y-%m-%d"), first)

    def test_write_provenance_fails_loudly_without_source_page(self):
        records = [_provenance_record("a.zip"), _provenance_record("b.zip")]
        del records[1]["source_page"]
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(sources, "PROVENANCE_DIR", Path(tmp)):
                with self.assertRaises(KeyError):
                    fetch._write_provenance("rp2018", records)
                self.assertFalse((Path(tmp) / "rp2018.toml").exists())


class ExistingRecordsTests(unittest.TestCase):
    def test_existing_records_ignores_comment_lines_even_with_equals(self):
        text = (
            "# generated-file: do not edit by hand\n"
            '# See the "Generated files" section of the repository README for '
            "the command\n"
            "# that regenerates it.\n"
            "# note = not a field\n"
            "\n"
            'edition = "rp2018"\n'
            "\n"
            "[[archives]]\n"
            'name = "a.zip"\n'
            "# note = not a field\n"
            'sha256 = "abc"\n'
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rp2018.toml"
            path.write_text(text, encoding="utf-8")
            records = fetch._existing_records(path)
        self.assertEqual(list(records), ["a.zip"])
        self.assertEqual(records["a.zip"], {"name": "a.zip", "sha256": "abc"})


class RecordModeTests(unittest.TestCase):
    """Record mode reuses the committed archives and preserves metadata."""

    def test_record_mode_adds_source_page_and_preserves_previous_metadata(self):
        payload = _zip_payload()
        spec = _fixture_spec(payload)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "archives" / "rp2018" / "fixture.zip"
            archive.parent.mkdir(parents=True)
            archive.write_bytes(payload)
            provenance = root / "provenance" / "rp2018.toml"
            provenance.parent.mkdir(parents=True)
            provenance.write_text(
                'edition = "rp2018"\n'
                "\n"
                "[[archives]]\n"
                'name = "fixture.zip"\n'
                'format = "ccat"\n'
                'requested_url = "https://www.dropbox.com/s/abc/fixture.zip?dl=0"\n'
                'download_url = "https://www.dropbox.com/s/abc/fixture.zip?dl=1"\n'
                'final_url = "https://recorded.example/file?dl=1"\n'
                "http_status = 200\n"
                'downloaded = "2026-11-16T18:37:00Z"\n'
                "size = 1234\n"
                f'sha256 = "{hashlib.sha256(b"old").hexdigest()}"\n'
                'extracted = "data/raw/rp2018/fixture"\n',
                encoding="utf-8",
            )
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
                    fetch,
                    "download",
                    side_effect=AssertionError("network access"),
                ),
            ):
                written = fetch.run()
            text = provenance.read_text(encoding="utf-8")
            extracted = (root / "raw" / "rp2018" / "fixture" / "MT.CCT").is_file()
        self.assertEqual(written, [provenance])
        self.assertTrue(extracted)
        self.assertIn(f'source_page = "{sources.SOURCE_PAGE}"', text)
        self.assertIn('final_url = "https://recorded.example/file?dl=1"', text)
        self.assertIn('downloaded = "2026-11-16T18:37:00Z"', text)
        self.assertIn("http_status = 200", text)


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
        payload = _zip_payload()
        expected = hashlib.sha256(payload).hexdigest()
        spec = _fixture_spec(payload)

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
            self.assertIn(f'source_page = "{sources.SOURCE_PAGE}"', text)
            self.assertEqual(
                text.splitlines()[0], generated.TOML_MARKER
            )

    def test_force_output_is_deterministic_when_the_clock_is_fixed(self):
        payload = _zip_payload()
        spec = _fixture_spec(payload)
        with mock.patch.object(fetch, "datetime", _FixedDatetime):
            with tempfile.TemporaryDirectory() as first:
                with tempfile.TemporaryDirectory() as second:
                    one = _run_force_in(Path(first), spec, payload)
                    two = _run_force_in(Path(second), spec, payload)
        self.assertEqual(one, two)
        text = one["rp2018.toml"]
        self.assertIn('downloaded = "2026-11-19T12:00:00Z"', text)
        self.assertIn(f'source_page = "{sources.SOURCE_PAGE}"', text)


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
