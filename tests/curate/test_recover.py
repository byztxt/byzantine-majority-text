"""Recovery safety: a failed recovery must not destroy the existing edition,
and every snapshot must hold only the authoritative data files."""

import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from byz.curate import editions, recover

ROOT = editions.ROOT


def _cct_hashes(directory: Path) -> dict:
    """Map each `.CCT` file name in `directory` to its SHA-256."""
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.glob("*.CCT"))
    }


class RecoverySafetyTests(unittest.TestCase):
    def test_failed_archive_keeps_the_existing_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = editions.EDITIONS_DIR
            editions.EDITIONS_DIR = Path(tmp)
            try:
                final = Path(tmp) / "rp2005-2019"
                (final / "source").mkdir(parents=True)
                (final / "marker.txt").write_text("keep me", encoding="utf-8")
                with self.assertRaises(SystemExit):
                    recover.recover_historical(
                        {"id": "rp2005-2019", "tag": "no-such-tag"}
                    )
                self.assertEqual(
                    (final / "marker.txt").read_text(encoding="utf-8"),
                    "keep me",
                )
                self.assertFalse((Path(tmp) / ".rp2005-2019.staging").exists())
            finally:
                editions.EDITIONS_DIR = original


class OfficialSnapshotFileSetTests(unittest.TestCase):
    """Official snapshots hold only the archive `.CCT` files, never strays."""

    # rp2018 additionally carries GREEK.CCT, which is not a book.
    COUNTS = {"rp2005": 29, "rp2018": 30}

    def test_committed_snapshots_equal_the_archive_cct_globs(self):
        for edition_id, expected_count in self.COUNTS.items():
            edition = editions.metadata(edition_id)
            archive = ROOT / edition["source_dir"]
            snapshot = editions.edition_dir(edition_id) / "source" / "ccat"
            self.assertEqual(
                sorted(
                    path.name for path in snapshot.iterdir() if path.is_file()
                ),
                sorted(path.name for path in archive.glob("*.CCT")),
                edition_id,
            )
            self.assertEqual(
                len(_cct_hashes(snapshot)), expected_count, edition_id
            )
            # The snapshot is a copy, so the bytes must match the archive.
            self.assertEqual(
                _cct_hashes(snapshot), _cct_hashes(archive), edition_id
            )

    def test_recover_official_excludes_stray_archive_files(self):
        # The reviewer's reproduction: a scratch file next to the extracted
        # `.CCT` archive must neither enter the snapshot nor change its manifest
        # hash list. This calls the real recovery into a temp tree so a revert
        # to a whole-tree copy fails here.
        edition = {
            "id": "rp2005",
            "source_dir": "data/raw/rp2005/editions-rp2-ccat",
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / edition["source_dir"]
            archive.mkdir(parents=True)
            (archive / "MT.CCT").write_text(
                "     01:01 biblov\n", encoding="utf-8"
            )
            (archive / "zz_stray.txt").write_text("scratch\n", encoding="utf-8")
            final = root / "editions" / "rp2005"
            final.mkdir(parents=True)
            with mock.patch.object(recover.editions, "ROOT", root), mock.patch.object(
                recover.editions, "edition_dir", lambda _: final
            ):
                recovered = recover.recover_official(edition)

            snapshot = recovered / "source" / "ccat"
            self.assertEqual(
                sorted(
                    path.name for path in snapshot.iterdir() if path.is_file()
                ),
                ["MT.CCT"],
            )
            self.assertEqual(
                sorted(
                    path.relative_to(recovered).as_posix()
                    for path in recovered.rglob("*")
                    if path.is_file()
                ),
                ["source/ccat/MT.CCT"],
            )


class CopyDataFilesGuardTests(unittest.TestCase):
    """`_copy_data_files` fails loudly rather than snapshotting nothing."""

    def test_missing_source_directory_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "missing"
            dest = Path(tmp) / "dest"
            with self.assertRaises(SystemExit) as caught:
                recover._copy_data_files(source, dest, "*.CCT")
            self.assertIn(str(source), str(caught.exception))
            self.assertFalse(dest.exists())

    def test_empty_match_set_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            source.mkdir()
            (source / "zz_stray.txt").write_text("scratch\n", encoding="utf-8")
            dest = Path(tmp) / "dest"
            with self.assertRaises(SystemExit) as caught:
                recover._copy_data_files(source, dest, "*.CCT")
            self.assertIn("*.CCT", str(caught.exception))
            self.assertFalse(dest.exists())


if __name__ == "__main__":
    unittest.main()
