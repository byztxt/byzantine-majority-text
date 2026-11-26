"""The current edition is built from `data/raw/repo/rp2018-2023/`, byte-for-byte.

`rp2018-2023` used to be copied out of the legacy `csv-unicode/` and
`tei-xml-unicode/` trees, then built from a per-edition snapshot. This module
locks the final pipeline: `data/raw/repo/rp2018-2023/` is the only input,
`build.build_current()` writes all five CSV views and both TEI views, and the
result is byte-identical to the committed edition. The shape tests prove the
three Strong's/unaccented views are distinct: with parsing, numbers-only, and
plain text.
"""

import csv
import hashlib
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from byz.curate import build, editions

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
            target.mkdir()
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
            target.mkdir()
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


class ViewShapeTests(unittest.TestCase):
    """The Strong's and unaccented views have three distinct shapes."""

    def _row(self, view, book="MAT", chapter=1, verse=1):
        path = editions.edition_dir(EDITION_ID) / "csv" / view / f"{book}.csv"
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                if (int(row["chapter"]), int(row["verse"])) == (
                    chapter,
                    verse,
                ):
                    return row["text"]
        self.fail(f"{view}/{book} {chapter}:{verse} is missing")

    def test_with_parsing_keeps_numbers_and_morphology(self):
        text = self._row("strongs/with-parsing")
        self.assertIn("976", text)
        self.assertIn("{N-NSF}", text)

    def test_numbers_only_keeps_numbers_and_drops_morphology(self):
        text = self._row("strongs/no-parsing")
        self.assertIn("976", text)
        self.assertNotIn("{", text)
        self.assertNotIn("}", text)
        self.assertEqual(
            text.split(),
            ["βιβλος", "976", "γενεσεως", "1078", "ιησου", "2424", "χριστου",
             "5547", "υιου", "5207", "δαυιδ", "1138", "υιου", "5207",
             "αβρααμ", "11"],
        )

    def test_unaccented_is_plain_text_without_numbers_or_parsing(self):
        text = self._row("unaccented")
        self.assertNotRegex(text, r"\d")
        self.assertNotIn("{", text)
        self.assertNotIn("}", text)
        self.assertEqual(
            text,
            "βιβλος γενεσεως ιησου χριστου υιου δαυιδ υιου αβρααμ",
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

    def test_no_tracked_file_reads_a_retired_path(self):
        # R9.3: the allowlist is explicit, so a new reference fails here. The
        # allowed Python locations name paths inside git tag `v2.0.3` or hold
        # the authoritative old -> new mapping; the two docs render that
        # mapping for readers. The same sweep locks the retired converter
        # names, which may only appear in the docs that record their removal
        # and in the tests that record the tag's history or assert absence.
        allowed = {
            "docs/EDITIONS.md",
            "src/byz/curate/docs.py",
            "src/byz/contract/history.py",
            "tests/curate/test_editions.py",
            "tests/curate/test_current_pipeline.py",
            # Records the `v2.0.3` tag prefixes (including `csv-unicode/`) to
            # compare the regenerated edition with the release's words.
            "tests/curate/test_historical_pipeline.py",
        }
        needles = ("csv-unicode/", "tei-xml-unicode/", "csv_converter", "tei_xml_converter")
        suffixes = (".py", ".md", ".txt", ".json", ".toml")
        offenders = []
        for path in _tracked_files():
            if path.startswith("SPECS/"):
                continue
            if path in allowed or not path.endswith(suffixes):
                continue
            # A file deleted in the working tree but still in the index (until
            # the next commit) cannot contain a live reference.
            if not (ROOT / path).is_file():
                continue
            text = (ROOT / path).read_text(encoding="utf-8", errors="ignore")
            if any(needle in text for needle in needles):
                offenders.append(path)
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
