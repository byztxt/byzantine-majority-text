"""The current edition is built from its own source snapshot, byte-for-byte.

`rp2018-2023` used to be copied out of the legacy `csv-unicode/` and
`tei-xml-unicode/` trees. This module locks the inverted pipeline: the edition's
own `source/` snapshot is the input, `build.build_current()` writes all five CSV
views and both TEI views, and the result is byte-identical to the committed
edition. The identity tests also lock the two intentional duplications
(`csv/unaccented` == `csv/strongs/no-parsing`, and the edition `source/` snapshot
== the repository `source/`).
"""

import hashlib
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from byz.curate import build, editions, recover

ROOT = editions.ROOT
EDITION_ID = "rp2018-2023"


def _rel_hashes(root):
    """Map every file below `root` to its SHA-256, relative to `root`."""
    hashes = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            hashes[str(path.relative_to(root))] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    return hashes


class BuildCurrentByteIdentityTests(unittest.TestCase):
    """Regenerating rp2018-2023 must reproduce the committed edition exactly."""

    def test_build_current_reproduces_the_committed_views(self):
        edition = editions.metadata(EDITION_ID)
        committed = editions.edition_dir(EDITION_ID)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / EDITION_ID
            shutil.copytree(committed / "source", target / "source")
            (target / "csv").mkdir()
            (target / "tei").mkdir()
            build.build_current(edition, edition_dir=target)
            for view in ("csv", "tei"):
                self.assertEqual(
                    _rel_hashes(target / view),
                    _rel_hashes(committed / view),
                    f"{view} differs from the committed edition",
                )

    def test_build_current_is_idempotent(self):
        edition = editions.metadata(EDITION_ID)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / EDITION_ID
            shutil.copytree(
                editions.edition_dir(EDITION_ID) / "source", target / "source"
            )
            (target / "csv").mkdir()
            (target / "tei").mkdir()
            build.build_current(edition, edition_dir=target)
            first = {
                view: _rel_hashes(target / view) for view in ("csv", "tei")
            }
            build.build_current(edition, edition_dir=target)
            second = {
                view: _rel_hashes(target / view) for view in ("csv", "tei")
            }
            self.assertEqual(first, second)


class ViewCountTests(unittest.TestCase):
    """The build writes every view, with the committed file counts."""

    COUNTS = {
        "csv/accented/no-variants": 29,
        "csv/accented/with-variants": 29,
        "csv/unaccented": 27,
        "csv/strongs/with-parsing": 27,
        "csv/strongs/no-parsing": 27,
    }

    def test_view_file_counts(self):
        root = editions.edition_dir(EDITION_ID)
        for view, expected in self.COUNTS.items():
            files = sorted((root / view).glob("*.csv"))
            self.assertEqual(len(files), expected, view)
        for view in ("tei/unaccented", "tei/accented"):
            files = sorted((root / view).glob("*.xml"))
            self.assertEqual(len(files), 27, view)
            self.assertTrue((root / view / "BYZ" / "byz.xml").is_file(), view)


class SourceSnapshotFileSetTests(unittest.TestCase):
    """The snapshot holds only the authoritative data files, never strays."""

    def test_committed_snapshot_equals_the_source_data_globs(self):
        snapshot = editions.edition_dir(EDITION_ID) / "source"
        repository = ROOT / "source"
        expected = {
            (Path("CCAT") / path.name).as_posix()
            for path in (repository / "CCAT").glob("*.TXT")
        } | {
            (Path("Strongs") / path.name).as_posix()
            for path in (repository / "Strongs").glob("*.BP5")
        }
        actual = {
            path.relative_to(snapshot).as_posix()
            for path in snapshot.rglob("*")
            if path.is_file()
        }
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 29 + 27)

    def test_recover_current_excludes_stray_working_tree_files(self):
        # The reviewer's reproduction: a scratch file under `source/CCAT` must
        # neither enter the snapshot nor change its manifest hash list. This
        # calls the real recovery into a temp tree so a revert to a whole-tree
        # copy fails here.
        edition = editions.metadata(EDITION_ID)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            (source / "CCAT").mkdir(parents=True)
            (source / "Strongs").mkdir()
            (source / "CCAT" / "01_MAT.TXT").write_text(
                "1:1 text\n", encoding="utf-8"
            )
            (source / "CCAT" / "stray.txt").write_text(
                "scratch\n", encoding="utf-8"
            )
            (source / "Strongs" / "01_MAT.BP5").write_text(
                "01.01 text\n", encoding="utf-8"
            )
            final = root / "editions" / EDITION_ID
            final.mkdir(parents=True)
            with mock.patch.object(recover.editions, "ROOT", root), mock.patch.object(
                recover.editions, "edition_dir", lambda _: final
            ):
                recovered = recover.recover_current(edition)

            snapshot = recovered / "source"
            actual = sorted(
                path.relative_to(snapshot).as_posix()
                for path in snapshot.rglob("*")
                if path.is_file()
            )
            self.assertEqual(actual, ["CCAT/01_MAT.TXT", "Strongs/01_MAT.BP5"])


class IdentityTests(unittest.TestCase):
    """Lock the intentional duplications documented in docs/EDITIONS.md."""

    def test_unaccented_csv_equals_strongs_no_parsing(self):
        root = editions.edition_dir(EDITION_ID)
        unaccented = root / "csv" / "unaccented"
        no_parsing = root / "csv" / "strongs" / "no-parsing"
        self.assertEqual(_rel_hashes(unaccented), _rel_hashes(no_parsing))

    def test_edition_source_snapshot_equals_repository_source(self):
        snapshot = editions.edition_dir(EDITION_ID) / "source"
        self.assertEqual(
            _rel_hashes(snapshot / "CCAT"), _rel_hashes(ROOT / "source" / "CCAT")
        )
        self.assertEqual(
            _rel_hashes(snapshot / "Strongs"),
            _rel_hashes(ROOT / "source" / "Strongs"),
        )

    def test_unaccented_tei_is_not_accented_and_keeps_the_source_header(self):
        text = (
            editions.edition_dir(EDITION_ID) / "tei" / "unaccented" / "MAT.xml"
        ).read_text(encoding="utf-8")
        self.assertNotIn("<pc>", text)
        self.assertNotIn("¶", text)
        self.assertIn('<edition n="2018">', text)

    def test_combined_unaccented_tei_is_in_canonical_book_order(self):
        text = (
            editions.edition_dir(EDITION_ID)
            / "tei"
            / "unaccented"
            / "BYZ"
            / "byz.xml"
        ).read_text(encoding="utf-8")
        ids = re.findall(r'<div type="book" n="(B\d{2})">', text)
        self.assertEqual(len(ids), 27)
        self.assertEqual(ids[0], "B01")
        self.assertEqual(ids[-1], "B27")


def _tracked_files():
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files"],
        capture_output=True,
        text=True,
        check=True,
    )
    return sorted(line for line in result.stdout.splitlines() if line)


class LegacyTreesAreGoneTests(unittest.TestCase):
    def test_legacy_trees_do_not_exist(self):
        for name in ("csv-unicode", "tei-xml-unicode"):
            self.assertFalse((ROOT / name).exists(), name)

    def test_retired_converters_do_not_exist(self):
        for name in ("csv_converter.py", "tei_xml_converter.py"):
            self.assertFalse((ROOT / "scripts" / name).exists(), name)

    def test_requirements_pin_only_the_converter_dependency(self):
        text = (ROOT / "scripts" / "requirements.txt").read_text(encoding="utf-8")
        self.assertEqual(
            [line for line in text.splitlines() if line.strip()],
            ["beta-code==1.0.0"],
        )

    def test_no_tracked_file_reads_a_retired_path(self):
        # R9.3: the allowlist is explicit, so a new reference fails here. The
        # allowed Python locations name paths inside git tag `v2.0.3` or hold
        # the authoritative old -> new mapping; the two docs render that
        # mapping for readers. The same sweep locks the retired converter
        # names, which may only appear in the docs that record their removal
        # and in the two tests that assert the absence.
        allowed = {
            "docs/EDITIONS.md",
            "docs/RELEASE-NOTES.md",
            "src/byz/curate/docs.py",
            "src/byz/curate/recover.py",
            "src/byz/contract/history.py",
            "tests/curate/test_editions.py",
            "tests/curate/test_fidelity.py",
            "tests/curate/test_current_pipeline.py",
        }
        needles = ("csv-unicode/", "tei-xml-unicode/", "csv_converter", "tei_xml_converter")
        suffixes = (".py", ".md", ".txt", ".json", ".toml")
        offenders = []
        for path in _tracked_files():
            if path.startswith("SPECS/"):
                continue
            if path in allowed or not path.endswith(suffixes):
                continue
            text = (ROOT / path).read_text(encoding="utf-8", errors="ignore")
            if any(needle in text for needle in needles):
                offenders.append(path)
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
