"""Fidelity checks for the generated edition outputs.

These guard the review findings: iota-subscript ordering, capitalisation from
glued apparatus codes, apparatus abbreviations, orphan combining marks, dash
spacing, manifest integrity, and the frozen historical artifacts.
"""

import csv
import hashlib
import io
import json
import re
import subprocess
import tarfile
import unittest
from pathlib import Path

from byz.curate import editions
from byz.reconcile import sources

ROOT = editions.ROOT

# `whitespace` followed by an orphan combining mark.
ORPHAN_MARK_RE = re.compile(r"\s[\u0300-\u036f\u0345]")
# Apparatus blocks. The official apparatus quotes the Greek text using beta code
# `+` for a diaeresis (e.g. `"+"` for a quotation mark), which the historical
# converter renders as `" ̈"`. Those frozen apparatus strings are kept verbatim,
# so the readability invariant applies to the main text only.
APPARATUS_RE = re.compile(r"\{[^{}]*\}")
# A dash glued to the preceding word.
ATTACHED_DASH_RE = re.compile(r"\S- ")


def _csv_verses(path):
    verses = {}
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            verses[(int(row["chapter"]), int(row["verse"]))] = row["text"]
    return verses


def _verse(edition_id, view, book, chapter, verse):
    path = editions.edition_dir(edition_id) / "csv" / view / f"{book}.csv"
    return _csv_verses(path)[(chapter, verse)]


class ProductionTextTests(unittest.TestCase):
    def test_iota_subscript_is_a_single_word(self):
        # The official 2018 archive writes iota-before-accent (`mimnh|/skh|`).
        # The converter needs the accent first, otherwise it emits
        # `μιμνῃ ́σκῃ` (space + orphan acute).
        text = _verse("rp2018", "accented/no-variants", "HEB", 2, 6)
        self.assertIn("μιμνῄσκῃ", text)
        self.assertNotIn("μιμνῃ", text)

    def test_glued_apparatus_code_is_not_a_capital(self):
        # MR 14:65 and LU 9:22 glue the apparatus opener to the last word
        # (`e)/ballon.{B`). The `B` must not be read as capitalisation.
        for edition_id in ("rp2005", "rp2018"):
            mark = _verse(edition_id, "accented/no-variants", "MAR", 14, 65)
            self.assertIn("ἔβαλλον", mark, edition_id)
            self.assertNotIn("Ἔβαλλον", mark, edition_id)
            luke = _verse(edition_id, "accented/no-variants", "LUK", 9, 22)
            self.assertIn("ἀναστῆναι", luke, edition_id)
            self.assertNotIn("Ἀναστῆναι", luke, edition_id)

    def test_apparatus_abbreviation_is_greek_capitals(self):
        # `_DAD` is an apparatus abbreviation, not a capitalised word. The
        # correct rendering matches `csv-unicode/ccat/with-variants/REV.csv`.
        text = _verse("rp2018", "accented/with-variants", "REV", 3, 7)
        self.assertIn("—ΔΑΔ", text)
        self.assertNotIn("δαδ", text)
        text = _verse("rp2018", "accented/with-variants", "REV", 13, 18)
        self.assertIn("—ΧΞ$", text)

    def test_no_orphan_combining_marks_in_main_text(self):
        for edition_id in editions.EDITIONS:
            root = editions.edition_dir(edition_id)
            for path in sorted(root.rglob("*.csv")):
                text = APPARATUS_RE.sub("", path.read_text(encoding="utf-8"))
                self.assertIsNone(
                    ORPHAN_MARK_RE.search(text),
                    f"orphan combining mark in {path.relative_to(ROOT)}",
                )
            for path in sorted(root.rglob("*.xml")):
                text = APPARATUS_RE.sub("", path.read_text(encoding="utf-8"))
                self.assertIsNone(
                    ORPHAN_MARK_RE.search(text),
                    f"orphan combining mark in {path.relative_to(ROOT)}",
                )


class DashGuardTests(unittest.TestCase):
    """The review claim that the converter adds spaces before dashes is false.

    The official main text uses spaced dashes; only the 2023 `source/CCAT`
    switched to attached dashes. These checks are guards, not fixes.
    """

    def test_official_edition_keeps_the_spaced_dash(self):
        text = _verse("rp2018", "accented/no-variants", "JOH", 1, 14)
        self.assertIn("ἡμῖν - καὶ", text)

    def test_official_ccat_main_text_has_no_attached_dashes(self):
        for edition_id in ("rp2005", "rp2018"):
            directory = editions.edition_dir(edition_id) / "source" / "ccat"
            for path in sorted(directory.glob("*.CCT")):
                if path.stem.upper() == "GREEK":
                    continue
                text = APPARATUS_RE.sub("", path.read_text(encoding="utf-8"))
                self.assertIsNone(
                    ATTACHED_DASH_RE.search(text),
                    f"attached dash in {edition_id}/{path.name}",
                )


class ManifestIntegrityTests(unittest.TestCase):
    def test_manifest_hashes_match_the_files(self):
        for edition_id in editions.EDITIONS:
            root = editions.edition_dir(edition_id)
            manifest = json.loads(
                (root / "manifest.json").read_text(encoding="utf-8")
            )
            entries = manifest["source_files"] + manifest["artifact_files"]
            self.assertTrue(entries, edition_id)
            for entry in entries:
                path = root / entry["path"]
                self.assertTrue(path.is_file(), f"{edition_id}/{entry['path']}")
                self.assertEqual(
                    hashlib.sha256(path.read_bytes()).hexdigest(),
                    entry["sha256"],
                    f"{edition_id}/{entry['path']}",
                )
                self.assertEqual(
                    path.stat().st_size,
                    entry["size"],
                    f"{edition_id}/{entry['path']}",
                )


class DocumentationTests(unittest.TestCase):
    def test_every_readme_has_edition_specific_notes(self):
        for edition_id in editions.EDITIONS:
            text = (editions.edition_dir(edition_id) / "README.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("## Notes", text, edition_id)
            notes = text.split("## Notes", 1)[1].strip()
            self.assertTrue(notes, f"{edition_id} has empty notes")

    def test_historical_readme_documents_blank_verse_omission(self):
        text = (editions.edition_dir("rp2005-2019") / "README.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("LUK 17:36", text)
        self.assertIn("7953", text)
        self.assertIn("byte-identical", text)

    def test_editions_doc_documents_blank_verse_omission_and_tei(self):
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
        for reference in ("LUK 17:36", "ACT 8:37", "ACT 15:34", "ACT 24:7"):
            self.assertIn(reference, text)
        self.assertIn("<pc>", text)
        self.assertIn("<ab/>", text)


class TeiPunctuationTests(unittest.TestCase):
    def test_accented_tei_uses_pc_and_paragraph_milestone(self):
        text = (editions.edition_dir("rp2018") / "tei" / "accented" / "MAT.xml").read_text(
            encoding="utf-8"
        )
        self.assertIn("<pc>-</pc>", text)
        self.assertNotIn("<w>-</w>", text)
        self.assertIn('<milestone unit="paragraph" type="start"/>', text)

    def test_unaccented_tei_has_no_pc_or_milestone(self):
        text = (
            editions.edition_dir("rp2018") / "tei" / "unaccented" / "MAT.xml"
        ).read_text(encoding="utf-8")
        self.assertNotIn("<pc>", text)
        self.assertNotIn("<milestone", text)


class HistoricalArtifactTests(unittest.TestCase):
    """`editions/rp2005-2019/` must stay byte-identical to tag `v2.0.3`."""

    MAPPING = {
        "csv-unicode/accents/no-variants": "csv/accented/no-variants",
        "csv-unicode/accents/with-variants": "csv/accented/with-variants",
        "csv-unicode/no-accents": "csv/unaccented",
        "tei-xml-unicode/no-accents": "tei/unaccented",
    }
    PREFIXES = (
        "textonly-beta-code/",
        "parsed/",
        "csv-unicode/accents/no-variants/",
        "csv-unicode/accents/with-variants/",
        "csv-unicode/no-accents/",
        "tei-xml-unicode/no-accents/",
    )

    @classmethod
    def setUpClass(cls):
        result = subprocess.run(
            ["git", "-C", str(ROOT), "archive", "v2.0.3"],
            capture_output=True,
            check=True,
        )
        cls.files = {}
        with tarfile.open(fileobj=io.BytesIO(result.stdout), mode="r:") as archive:
            for member in archive.getmembers():
                if not member.isfile():
                    continue
                if not any(member.name.startswith(p) for p in cls.PREFIXES):
                    continue
                extracted = archive.extractfile(member)
                if extracted is not None:
                    cls.files[member.name] = extracted.read()

    def _target(self, name):
        for prefix, target in self.MAPPING.items():
            if name.startswith(prefix + "/"):
                rel = name[len(prefix) + 1 :]
                stem, suffix = rel.rsplit(".", 1)
                abbr = sources.OFFICIAL_TO_ABBR.get(stem, stem)
                return Path(target) / f"{abbr}.{suffix}"
        return Path("source") / name

    def test_counts(self):
        self.assertEqual(
            sum(1 for name in self.files if name.startswith("textonly-beta-code/")),
            30,
        )
        self.assertEqual(
            sum(1 for name in self.files if name.startswith("parsed/")), 27
        )
        for prefix in self.MAPPING:
            self.assertTrue(
                any(name.startswith(prefix + "/") for name in self.files), prefix
            )

    def test_bytes_match(self):
        root = editions.edition_dir("rp2005-2019")
        for name, expected in self.files.items():
            path = root / self._target(name)
            self.assertTrue(path.is_file(), f"missing {path}")
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                hashlib.sha256(expected).hexdigest(),
                f"{path} differs from v2.0.3",
            )

    def test_no_empty_rows_for_omitted_verses(self):
        # v2.0.3 predates the intentional blank verses; they are absent, not
        # empty. The rows must not be added back (byte identity).
        unaccented = editions.edition_dir("rp2005-2019") / "csv" / "unaccented"
        total = sum(len(_csv_verses(path)) for path in unaccented.glob("*.csv"))
        self.assertEqual(total, 7953)


if __name__ == "__main__":
    unittest.main()
