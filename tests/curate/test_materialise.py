"""Materialisation of the historical 2005-2019 inputs into `data/`."""

import hashlib
import io
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from byz import generated
from byz.curate import editions, materialise

ROOT = editions.ROOT
TAG = "v2.0.3"
PREFIX_COUNTS = {
    "textonly-beta-code/": 30,
    "parsed/": 27,
}


def _tag_files() -> dict:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "archive", TAG],
        capture_output=True,
        check=True,
    )
    files = {}
    with tarfile.open(fileobj=io.BytesIO(result.stdout), mode="r:") as archive:
        for member in archive.getmembers():
            if not member.isfile():
                continue
            if not any(member.name.startswith(p) for p in PREFIX_COUNTS):
                continue
            extracted = archive.extractfile(member)
            if extracted is not None:
                files[member.name] = extracted.read()
    return files


def _provenance_value(text: str, key: str) -> str:
    for line in text.splitlines():
        if line.startswith(f"{key} = "):
            return line.split("=", 1)[1].strip().strip('"')
    return ""


class HistoricalTreeTests(unittest.TestCase):
    """The committed tree is the tag's two source prefixes, and nothing else."""

    @classmethod
    def setUpClass(cls):
        cls.tag = _tag_files()

    def test_tree_has_the_two_source_prefixes(self):
        root = ROOT / materialise.HISTORICAL_INPUT_ROOT
        for tag_prefix, expected in PREFIX_COUNTS.items():
            data_prefix = tag_prefix
            self.assertEqual(
                len(list((root / data_prefix).glob("*"))), expected, tag_prefix
            )
        actual = sorted(
            path.relative_to(root).as_posix()
            for path in root.rglob("*")
            if path.is_file()
            and path.relative_to(root).as_posix()
            not in materialise.GENERATED_NEIGHBOURS
        )
        self.assertEqual(len(actual), 57)

    def test_tree_matches_the_tag_byte_for_byte(self):
        root = ROOT / materialise.HISTORICAL_INPUT_ROOT
        for name, expected in self.tag.items():
            self.assertEqual(
                hashlib.sha256((root / name).read_bytes()).hexdigest(),
                hashlib.sha256(expected).hexdigest(),
                name,
            )

    def test_provenance_records_the_tag_commit_and_every_file(self):
        path = ROOT / materialise.HISTORICAL_PROVENANCE
        text = path.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("\n".join(generated.toml_header())))
        self.assertEqual(_provenance_value(text, "edition"), "rp2005-2019")
        self.assertEqual(_provenance_value(text, "tag"), TAG)
        self.assertEqual(
            _provenance_value(text, "commit"), materialise.HISTORICAL_COMMIT
        )
        self.assertEqual(
            _provenance_value(text, "extracted"),
            materialise.HISTORICAL_INPUT_ROOT,
        )
        self.assertEqual(
            _provenance_value(text, "generated_by"),
            "PYTHONPATH=src python3 -m byz.materialise",
        )
        self.assertNotIn("downloaded", text)
        self.assertNotIn("http://", text)
        self.assertNotIn("https://", text)
        self.assertEqual(text.count("[[prefixes]]"), 2)
        self.assertEqual(text.count("[[files]]"), 57)
        rows = [
            line.split("=", 1)[1].strip().strip('"')
            for line in text.splitlines()
            if line.startswith("path = ")
        ]
        # Two prefix rows plus one row per file.
        self.assertEqual(len(rows), 2 + 57)
        self.assertEqual(
            rows[2:], sorted(rows[2:]), "file rows must be sorted by path"
        )
        for name in self.tag:
            self.assertIn(name, rows)
            digest = hashlib.sha256(self.tag[name]).hexdigest()
            self.assertIn(f'sha256 = "{digest}"', text)


class MaterialiseTempTreeTests(unittest.TestCase):
    """`materialise_historical` is safe outside the repository."""

    def test_writes_exactly_the_source_prefixes(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = materialise.materialise_historical(
                dest_root=Path(tmp)
            )
            self.assertEqual(
                destination, Path(tmp) / materialise.HISTORICAL_INPUT_ROOT
            )
            files = sorted(
                path.relative_to(destination).as_posix()
                for path in destination.rglob("*")
                if path.is_file()
            )
            self.assertEqual(len(files), 57)
            self.assertTrue(files[0].startswith("parsed/"))
            self.assertTrue(files[-1].startswith("textonly-beta-code/"))
            provenance = Path(tmp) / materialise.HISTORICAL_PROVENANCE
            self.assertTrue(provenance.is_file())
            self.assertEqual(
                provenance.read_text(encoding="utf-8").count("[[files]]"),
                57,
            )

    def test_second_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            destination = materialise.materialise_historical(dest_root=root)
            before = {
                path.relative_to(root).as_posix(): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file()
            }
            materialise.materialise_historical(dest_root=root)
            after = {
                path.relative_to(root).as_posix(): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file()
            }
            self.assertEqual(before, after)
            self.assertTrue(destination.is_dir())

    def test_conflicting_file_is_refused_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            destination = materialise.materialise_historical(dest_root=root)
            path = destination / "parsed" / "MT.UB5"
            original = path.read_bytes()
            path.write_bytes(original + b"x")
            with self.assertRaises(SystemExit) as caught:
                materialise.materialise_historical(dest_root=root)
            message = str(caught.exception)
            self.assertIn("MT.UB5", message)
            self.assertIn("sha256", message)
            self.assertNotEqual(path.read_bytes(), original)

    def test_stray_file_is_refused_before_any_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            destination = materialise.materialise_historical(dest_root=root)
            stray = destination / "parsed" / "stray.txt"
            stray.write_text("scratch\n", encoding="utf-8")
            with self.assertRaises(SystemExit) as caught:
                materialise.materialise_historical(dest_root=root)
            self.assertIn("unexpected", str(caught.exception))
            self.assertIn("parsed/stray.txt", str(caught.exception))
            self.assertTrue(stray.is_file())

    def test_failed_archive_leaves_the_existing_tree_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sentinel = root / materialise.HISTORICAL_INPUT_ROOT / "marker.txt"
            sentinel.parent.mkdir(parents=True)
            sentinel.write_text("keep me", encoding="utf-8")
            with mock.patch.object(materialise, "HISTORICAL_TAG", "no-such-tag"):
                with self.assertRaises(SystemExit):
                    materialise.materialise_historical(dest_root=root)
            self.assertEqual(
                sentinel.read_text(encoding="utf-8"), "keep me"
            )


if __name__ == "__main__":
    unittest.main()
