"""`rp2005-2019` is regenerated from its 2019 sources by the current pipeline.

The edition used to copy the `v2.0.3` release's CSV/TEI byte-for-byte. Those
artifacts were produced by the 2019 converter, which transliterated the
apparatus code initials (`{N`/`{B` became the Greek capitals `{Ν`/`{Β`) and used
its own typography. The build now regenerates every view from the 57 source
files committed under `data/raw/repo/rp2005-2019/`, exactly like the other editions.
Only `byz.materialise` extracts tag `v2.0.3` into `data/`; the build reads
`data/` only (`byz.reconcile` reads the tag with `git show` for historical
comparison, and `byz.build` lists tags for the release ranges, but neither uses
the tag's files as build inputs).
"""

import csv
import hashlib
import io
import re
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

from byz.contract import paths
from byz.curate import build, editions
from byz.reconcile import sources

ROOT = editions.ROOT
EDITION_ID = "rp2005-2019"
TAG = "v2.0.3"

# Apparatus code initials. The 2019 converter emitted the Greek capitals.
GREEK_CAPITAL_INITIAL_RE = re.compile(r"\{[\u0391-\u03a9]")
MALFORMED_INITIALS = ("{Ν", "{Β")

# The views the build must produce, with their committed file counts.
VIEW_COUNTS = {
    "csv/accented/no-variants": 29,
    "csv/accented/with-variants": 29,
    "csv/unaccented": 27,
    "csv/strongs/with-parsing": 27,
    "csv/strongs/no-parsing": 27,
}


def _rel_hashes(root: Path) -> dict:
    """Map every file below `root` to its SHA-256, relative to `root`."""
    hashes = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            hashes[path.relative_to(root).as_posix()] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    return hashes


def _csv_verses(path: Path) -> dict:
    verses = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            verses[(int(row["chapter"]), int(row["verse"]))] = row["text"]
    return verses


def _normalise_main_text(text: str) -> str:
    """Drop the typography that the two pipelines represent differently."""
    text = text.replace("¶", "")
    return text.replace("\u2019", "'").replace("\u2018", "'")


def _tag_files(prefixes) -> dict:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "archive", TAG, *prefixes],
        capture_output=True,
        check=True,
    )
    files = {}
    with tarfile.open(fileobj=io.BytesIO(result.stdout), mode="r:") as archive:
        for member in archive.getmembers():
            if not member.isfile():
                continue
            if not any(member.name.startswith(p) for p in prefixes):
                continue
            extracted = archive.extractfile(member)
            if extracted is not None:
                files[member.name] = extracted.read()
    return files


class BuildHistoricalTests(unittest.TestCase):
    """The committed edition is what the current pipeline generates."""

    def test_build_historical_reproduces_the_committed_views(self):
        edition = editions.metadata(EDITION_ID)
        committed = editions.edition_dir(EDITION_ID)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / EDITION_ID
            target.mkdir()
            build.build_historical(edition, edition_dir=target)
            for view in ("csv", "tei"):
                self.assertEqual(
                    _rel_hashes(target / view),
                    _rel_hashes(committed / view),
                    f"{view} differs from the committed edition",
                )

    def test_build_historical_is_idempotent(self):
        edition = editions.metadata(EDITION_ID)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / EDITION_ID
            target.mkdir()
            build.build_historical(edition, edition_dir=target)
            first = {
                view: _rel_hashes(target / view) for view in ("csv", "tei")
            }
            build.build_historical(edition, edition_dir=target)
            second = {
                view: _rel_hashes(target / view) for view in ("csv", "tei")
            }
            self.assertEqual(first, second)

    def test_view_file_counts(self):
        root = editions.edition_dir(EDITION_ID)
        for view, expected in VIEW_COUNTS.items():
            files = sorted((root / view).glob("*.csv"))
            self.assertEqual(len(files), expected, view)
        for view in ("tei/accented", "tei/unaccented"):
            files = sorted((root / view).glob("*.xml"))
            self.assertEqual(len(files), 27, view)
            self.assertTrue((root / view / "BYZ" / "byz.xml").is_file(), view)


class ApparatusCodeTests(unittest.TestCase):
    """The regenerated with-variants view uses the documented Latin initials."""

    def test_no_greek_code_initials_in_any_with_variants_file(self):
        # Every apparatus code initial is Latin: `NA`, `Byz`, `NA27/28`, `ECM`,
        # `NA27`, `NA28`. A Greek capital after `{` means the 2019 transliteration
        # bug is back.
        for path in sorted(
            (editions.edition_dir(EDITION_ID)
             / "csv" / "accented" / "with-variants").glob("*.csv")
        ):
            text = path.read_text(encoding="utf-8")
            for malformed in MALFORMED_INITIALS:
                self.assertNotIn(malformed, text, path.name)
            match = GREEK_CAPITAL_INITIAL_RE.search(text)
            self.assertIsNone(
                match, f"{path.name}: Greek capital initial {match and match.group(0)}"
            )

    def test_sample_apparatus_labels_are_na_and_byz(self):
        # MAT 1:5 carries both code types in the source:
        # `{N ... }` and `{B ... }`. The generated view must render them as
        # `{NA` and `{Byz`, not as Greek capitals.
        text = _csv_verses(
            editions.edition_dir(EDITION_ID)
            / "csv" / "accented" / "with-variants" / "MAT.csv"
        )[(1, 5)]
        self.assertIn("{NA", text)
        self.assertIn("Βοὸζ", text)

        # A Byzantine-only reading: 1CO 5:7 in the 2019 source.
        text = _csv_verses(
            editions.edition_dir(EDITION_ID)
            / "csv" / "accented" / "with-variants" / "1CO.csv"
        )[(5, 7)]
        self.assertIn("{Byz", text)

    def test_the_whole_edition_has_both_code_types(self):
        total_na = 0
        total_byz = 0
        for path in sorted(
            (editions.edition_dir(EDITION_ID)
             / "csv" / "accented" / "with-variants").glob("*.csv")
        ):
            text = path.read_text(encoding="utf-8")
            total_na += text.count("{NA")
            total_byz += text.count("{Byz")
        self.assertGreater(total_na, 0)
        self.assertGreater(total_byz, 0)


class ReleasedWordsRegressionTests(unittest.TestCase):
    """The regenerated main text keeps the words of the 2019 release.

    The released `v2.0.3` accented no-variants CSV is an independent record of
    the 2019 text. Compared verse by verse, the only differences allowed are
    paragraph markers (`¶`) and apostrophe typography; any letter or word change
    is a conversion regression. Missing and empty rows compare equal, so the
    four intentional blank verses do not register.
    """

    @classmethod
    def setUpClass(cls):
        cls.released = _tag_files(("csv-unicode/accents/no-variants",))

    def test_accented_main_text_words_match_the_release(self):
        root = editions.edition_dir(EDITION_ID) / "csv" / "accented" / "no-variants"
        differences = []
        for name, data in sorted(self.released.items()):
            stem = Path(name).stem
            abbr = sources.OFFICIAL_TO_ABBR.get(stem, stem)
            released = {}
            for row in csv.DictReader(io.StringIO(data.decode("utf-8"))):
                released[(int(row["chapter"]), int(row["verse"]))] = row["text"]
            generated = _csv_verses(root / f"{abbr}.csv")
            for key in sorted(set(released) | set(generated)):
                if _normalise_main_text(
                    released.get(key, "")
                ) != _normalise_main_text(generated.get(key, "")):
                    differences.append((abbr, key))
        self.assertEqual(differences, [])


class HistoricalInputPinTests(unittest.TestCase):
    """The manifest pins exactly the 57 source files under `data/`."""

    def test_manifest_pins_the_historical_inputs(self):
        import json

        root = editions.edition_dir(EDITION_ID)
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["inputs"]), 1)
        group = manifest["inputs"][0]
        self.assertEqual(group["root"], "data/raw/repo/rp2005-2019")
        self.assertEqual(
            sorted(group["include"]),
            ["parsed/*.UB5", "textonly-beta-code/*.CCT"],
        )
        self.assertEqual(len(group["files"]), 57)
        pinned = {entry["path"]: entry for entry in group["files"]}
        for name, entry in pinned.items():
            path = ROOT / group["root"] / name
            self.assertTrue(path.is_file(), name)
            self.assertEqual(
                entry["sha256"],
                hashlib.sha256(path.read_bytes()).hexdigest(),
                name,
            )

    def test_no_released_artifact_tree_is_an_input(self):
        root = ROOT / "data" / "raw" / "repo" / "rp2005-2019"
        for retired in ("csv-unicode", "tei-xml-unicode"):
            self.assertFalse((root / retired).exists(), retired)


class HistoricalSourceGuardTests(unittest.TestCase):
    """An unmapped or missing historical book fails the build loudly."""

    def test_unknown_book_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "ZZ.CCT").write_text("     01:01 x\n", encoding="utf-8")
            with self.assertRaises(ValueError) as caught:
                build._historical_source_map(Path(tmp), "*.CCT", ".CCT")
        self.assertIn("ZZ.CCT", str(caught.exception))

    def test_missing_book_is_refused(self):
        with self.assertRaises(ValueError) as caught:
            build._check_historical_books(
                {}, paths.CANONICAL_BOOKS, ".UB5", EDITION_ID
            )
        self.assertIn("missing", str(caught.exception))

    def test_greek_notes_file_is_not_a_book(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "GREEK.CCT").write_text("notes\n", encoding="utf-8")
            self.assertEqual(
                build._historical_source_map(Path(tmp), "*.CCT", ".CCT"), {}
            )


class BlankVerseTests(unittest.TestCase):
    """The four intentional blanks are emitted like the other editions."""

    REFS = {
        ("LUK", 17, 36),
        ("ACT", 8, 37),
        ("ACT", 15, 34),
        ("ACT", 24, 7),
    }

    def test_every_view_keeps_the_four_blank_verses(self):
        base = editions.edition_dir(EDITION_ID) / "csv"
        for view in (
            "accented/no-variants",
            "accented/with-variants",
            "unaccented",
            "strongs/with-parsing",
            "strongs/no-parsing",
        ):
            for book, chapter, verse in self.REFS:
                text = _csv_verses(base / view / f"{book}.csv")[(chapter, verse)]
                self.assertEqual(text, "", f"{view}/{book} {chapter}:{verse}")

    def test_tei_has_empty_anchors_for_the_four_blanks(self):
        base = editions.edition_dir(EDITION_ID) / "tei"
        for view in ("accented", "unaccented"):
            for book, chapter, verse in self.REFS:
                book_id = "B" + {
                    "LUK": "03",
                    "ACT": "05",
                }[book]
                anchor = f"{book_id}K{chapter}V{verse}"
                text = (base / view / f"{book}.xml").read_text(encoding="utf-8")
                self.assertIn(f'<ab n="{anchor}"/>', text, f"{view}/{book}")


if __name__ == "__main__":
    unittest.main()
