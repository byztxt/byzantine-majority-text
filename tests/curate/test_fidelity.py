"""Fidelity checks for the generated edition outputs.

These guard the review findings: iota-subscript ordering, capitalisation from
glued apparatus codes, apparatus abbreviations, orphan combining marks, dash
spacing, manifest integrity, and the recovered historical artifacts.
"""

import csv
import hashlib
import json
import re
import unittest
from pathlib import Path

from byz.contract import paths
from byz.curate import docs, editions

ROOT = editions.ROOT

# `whitespace` followed by an orphan combining mark.
ORPHAN_MARK_RE = re.compile(r"\s[\u0300-\u036f\u0345]")
# Apparatus blocks. The official apparatus quotes the Greek text using beta code
# `+` for a diaeresis and carries English notes in `[[ "..." ]]`. Those literals
# are now preserved verbatim (see `ApparatusLiteralFidelityTests`), but the
# apparatus is not normalised running text, so the readability invariants below
# apply to the main text only.
APPARATUS_RE = re.compile(r"\{[^{}]*\}")
# A dash glued to the preceding word.
ATTACHED_DASH_RE = re.compile(r"\S- ")
# A dash glued to the preceding word, at end of text too.
ATTACHED_MAIN_DASH_RE = re.compile(r"\S-(?=\s|$)")


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
        # correct rendering matches
        # `editions/rp2018-2023/csv/accented/with-variants/REV.csv`.
        text = _verse("rp2018", "accented/with-variants", "REV", 3, 7)
        self.assertIn("—ΔΑΔ", text)
        self.assertNotIn("δαδ", text)
        # The repo's 2023 `editions/rp2018-2023/csv/accented/with-variants/REV.csv`
        # renders this as `—ΧΞ*$` (digit marker), while the official archive's
        # `_XC$` is `—ΧΞ$` with no marker. The curated official edition follows
        # the archive, as it must.
        text = _verse("rp2018", "accented/with-variants", "REV", 13, 18)
        self.assertIn("—ΧΞ$", text)
        self.assertNotIn("—ΧΞ*$", text)

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

    The official main text uses spaced dashes; only the 2023 `data/raw/repo/rp2018-2023/ccat`
    switched to attached dashes. These checks are guards, not fixes — except for
    the final-sigma case, where the inherited converter's unconditional
    `ς -` -> `ς-` rewrite is undone in the production path.
    """

    # Verses whose printed dashes follow a word ending in final sigma. Each dash
    # is spaced in the official `.CCT` source but was emitted attached until the
    # production path restored the source spacing (2CO 9:4 has two dashes).
    AFFECTED_VERSES = [
        ("MAT", 9, 6),
        ("MAR", 2, 10),
        ("LUK", 5, 24),
        ("JOH", 1, 14),
        ("JOH", 1, 42),
        ("JOH", 7, 50),
        ("JOH", 21, 7),
        ("ACT", 4, 36),
        ("ACT", 13, 8),
        ("ROM", 1, 13),
        ("2CO", 2, 5),
        ("2CO", 9, 4),
        ("COL", 4, 10),
        ("HEB", 7, 20),
        ("HEB", 10, 8),
        ("HEB", 11, 38),
        ("REV", 21, 25),
    ]

    def test_official_edition_keeps_the_spaced_dash(self):
        text = _verse("rp2018", "accented/no-variants", "JOH", 1, 14)
        self.assertIn("ἡμῖν - καὶ", text)

    def test_spaced_dash_restored_after_final_sigma(self):
        for edition_id in ("rp2005", "rp2018"):
            for book, chapter, verse in self.AFFECTED_VERSES:
                text = _verse(
                    edition_id, "accented/no-variants", book, chapter, verse
                )
                self.assertIn(
                    "ς -", text, f"{edition_id} {book} {chapter}:{verse}"
                )
                self.assertNotRegex(
                    text,
                    r"ς-",
                    f"{edition_id} {book} {chapter}:{verse} still attached",
                )
            # The examples named by the verifier.
            self.assertIn(
                "πατρός - πλήρης",
                _verse(edition_id, "accented/no-variants", "JOH", 1, 14),
            )
            self.assertIn(
                "ἁμαρτίας - τότε",
                _verse(edition_id, "accented/no-variants", "MAT", 9, 6),
            )
            self.assertIn(
                "ὁρκωμοσίας - οἱ",
                _verse(edition_id, "accented/no-variants", "HEB", 7, 20),
            )

    def test_official_accents_have_no_attached_main_text_dashes(self):
        # Corpus-wide invariant: the source has no attached main-text dashes, so
        # neither may the generated official editions. This catches any
        # final-sigma (or other) dash regression, including at end of verse.
        for edition_id in ("rp2005", "rp2018"):
            root = editions.edition_dir(edition_id) / "csv" / "accented"
            for path in sorted(root.rglob("*.csv")):
                text = APPARATUS_RE.sub(
                    "", path.read_text(encoding="utf-8")
                )
                self.assertIsNone(
                    ATTACHED_MAIN_DASH_RE.search(text),
                    f"attached dash in {edition_id}/{path.name}",
                )

    def test_official_ccat_main_text_has_no_attached_dashes(self):
        for edition_id in ("rp2005", "rp2018"):
            directory = (
                editions.ROOT / editions.EDITIONS[edition_id]["source_dir"]
            )
            for path in sorted(directory.glob("*.CCT")):
                if path.stem.upper() == "GREEK":
                    continue
                text = APPARATUS_RE.sub("", path.read_text(encoding="utf-8"))
                self.assertIsNone(
                    ATTACHED_DASH_RE.search(text),
                    f"attached dash in {edition_id}/{path.name}",
                )

    def test_official_tei_splits_the_dash_after_final_sigma(self):
        anchor = f"{paths.ABBR_TO_BOOK_ID['JOH']}K1V14"
        text = (
            editions.edition_dir("rp2018") / "tei" / "accented" / "JOH.xml"
        ).read_text(encoding="utf-8")
        block = re.search(
            rf'<ab n="{anchor}">(.*?)</ab>', text, re.S
        ).group(1)
        self.assertNotIn("<w>πατρός-</w>", block)
        self.assertRegex(
            block, r"<w>πατρός</w>\s+<pc>-</pc>\s+<w>πλήρης</w>"
        )


class ManifestIntegrityTests(unittest.TestCase):
    def test_manifest_hashes_match_the_files(self):
        for edition_id in editions.EDITIONS:
            root = editions.edition_dir(edition_id)
            manifest = json.loads(
                (root / "manifest.json").read_text(encoding="utf-8")
            )
            self.assertNotIn("source_files", manifest, edition_id)
            self.assertTrue(manifest["inputs"], edition_id)
            self.assertTrue(manifest["artifact_files"], edition_id)
            for group in manifest["inputs"]:
                self.assertFalse(
                    group["root"].startswith("editions/"), edition_id
                )
                for entry in group["files"]:
                    path = editions.ROOT / group["root"] / entry["path"]
                    self.assertTrue(
                        path.is_file(),
                        f"{edition_id}/{group['root']}/{entry['path']}",
                    )
                    self.assertEqual(
                        hashlib.sha256(path.read_bytes()).hexdigest(),
                        entry["sha256"],
                        f"{edition_id}/{group['root']}/{entry['path']}",
                    )
                    self.assertEqual(
                        path.stat().st_size,
                        entry["size"],
                        f"{edition_id}/{group['root']}/{entry['path']}",
                    )
            for entry in manifest["artifact_files"]:
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


class ApparatusLiteralFidelityTests(unittest.TestCase):
    """MAR 16:8 apparatus notes survive the conversion.

    `[[ "shorter ending" ]]` and the literal `"+"` are apparatus text, not beta
    code. The historical converter transliterated the note and rendered the
    quotation mark as `" ̈"`; all curated editions now keep both verbatim.
    """

    OLD_NOTE = "σηορτερ"
    OLD_PLUS = '" ̈"'

    def test_generated_editions_preserve_the_literals(self):
        # The official `.CCT` archives carry the note in lower case with spaces
        # inside the brackets; the production parser must not upper-case or
        # re-space it.
        for edition_id in ("rp2005", "rp2018"):
            text = _verse(edition_id, "accented/with-variants", "MAR", 16, 8)
            self.assertIn('[[ "shorter ending" ]]', text, edition_id)
            self.assertIn('"+"', text, edition_id)
            self.assertNotIn(self.OLD_NOTE, text, edition_id)
            self.assertNotIn(self.OLD_PLUS, text, edition_id)
        # `data/raw/repo/rp2018-2023/ccat` (the basis of `rp2018-2023`) is upper-case with no
        # spaces inside the brackets, and that form is correct for it.
        text = _verse("rp2018-2023", "accented/with-variants", "MAR", 16, 8)
        self.assertIn('[["SHORTER ENDING"]]', text)
        self.assertIn('"+"', text)
        self.assertNotIn(self.OLD_NOTE, text)
        self.assertNotIn(self.OLD_PLUS, text)

    def test_historical_with_variants_has_the_literal(self):
        # The 2019 sources carry the same literals; regeneration by the current
        # pipeline keeps them, so no special post-correction is needed.
        text = _verse("rp2005-2019", "accented/with-variants", "MAR", 16, 8)
        self.assertIn('[[ "shorter ending" ]]', text)
        self.assertIn('"+"', text)
        self.assertNotIn(self.OLD_NOTE, text)
        self.assertNotIn(self.OLD_PLUS, text)


class DocumentationTests(unittest.TestCase):
    def test_every_readme_has_edition_specific_notes(self):
        for edition_id in editions.EDITIONS:
            text = (editions.edition_dir(edition_id) / "README.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("## Notes", text, edition_id)
            notes = text.split("## Notes", 1)[1].strip()
            self.assertTrue(notes, f"{edition_id} has empty notes")

    def test_historical_readme_documents_regeneration(self):
        text = (editions.edition_dir("rp2005-2019") / "README.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("LUK 17:36", text)
        self.assertIn("7972", text)
        self.assertIn("7957", text)
        # The edition is regenerated from its sources, not copied from the tag.
        self.assertIn("regenerated from them by the current pipeline", text)
        self.assertIn("malformed apparatus codes", text)
        self.assertNotIn("byte-identical", text)

    def test_editions_doc_documents_blank_verse_omission_and_tei(self):
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
        for reference in ("LUK 17:36", "ACT 8:37", "ACT 15:34", "ACT 24:7"):
            self.assertIn(reference, text)
        # The archives contain blank verse lines; every edition keeps the four
        # verses as explicit empty records, including the regenerated 2019 one.
        self.assertIn("as **blank verse lines**", text)
        for count in ("7972", "7957"):
            self.assertIn(count, text, f"missing row count {count}")
        self.assertIn("four empty", text)
        self.assertIn("<ab/>", text)
        self.assertIn("omission is not reproduced", text)
        self.assertIn("accented TEI", text)
        self.assertIn("<pc>", text)

    def test_editions_doc_documents_apparatus_literals(self):
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
        self.assertIn("## Apparatus literals", text)
        self.assertIn("preserve apparatus literals verbatim", text)
        self.assertIn('[[ "..." ]]', text)
        self.assertIn("regenerates `rp2005-2019` from the sources", text)
        self.assertIn("needs no post-correction", text)
        self.assertNotIn("by design", text)


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


class BlankVerseTests(unittest.TestCase):
    """The four intentional blanks are data, not omitted conversions.

    The official `.CCT` and ASCII archives carry blank verse lines for
    LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7. The official editions and
    `rp2018-2023` emit them as explicit empty records; only the recovered
    `rp2005-2019` artifacts omit the rows entirely, while its generated Strong's
    views keep them.
    """

    REFS = {
        ("LUK", 17, 36),
        ("ACT", 8, 37),
        ("ACT", 15, 34),
        ("ACT", 24, 7),
    }
    ANCHORS = {
        f"{paths.ABBR_TO_BOOK_ID[book]}K{chapter}V{verse}"
        for book, chapter, verse in REFS
    }

    def _view(self, edition_id, view):
        total = 0
        values = {}
        root = editions.edition_dir(edition_id) / "csv" / view
        for path in sorted(root.glob("*.csv")):
            verses = _csv_verses(path)
            total += len(verses)
            for (chapter, verse), text in verses.items():
                values[(path.stem, chapter, verse)] = text
        return total, values

    def _tei_empty_anchors(self, edition_id, kind):
        anchors = set()
        root = editions.edition_dir(edition_id) / "tei" / kind
        for path in sorted(root.rglob("*.xml")):
            text = path.read_text(encoding="utf-8")
            anchors.update(re.findall(r'<ab n="([^"]+)"/>', text))
        return anchors

    def test_every_edition_keeps_the_blank_verses(self):
        for edition_id in editions.EDITIONS:
            for view, expected in (
                ("accented/no-variants", 7972),
                ("accented/with-variants", 7972),
                ("unaccented", 7957),
            ):
                total, values = self._view(edition_id, view)
                self.assertEqual(total, expected, f"{edition_id}/{view}")
                for ref in self.REFS:
                    self.assertIn(ref, values, f"{edition_id}/{view}/{ref}")
                    self.assertEqual(
                        values[ref], "", f"{edition_id}/{view}/{ref} is not empty"
                    )
            for kind in ("accented", "unaccented"):
                self.assertTrue(
                    self.ANCHORS <= self._tei_empty_anchors(edition_id, kind),
                    f"{edition_id}/{kind} is missing empty <ab/> anchors",
                )

    def test_current_strongs_views_keep_the_blank_verses(self):
        for view in ("strongs/no-parsing", "strongs/with-parsing"):
            total, values = self._view("rp2018-2023", view)
            self.assertEqual(total, 7957, view)
            for ref in self.REFS:
                self.assertEqual(values.get(ref), "", f"{view}/{ref}")

    def test_historical_strongs_views_keep_the_blank_verses(self):
        for view in ("strongs/no-parsing", "strongs/with-parsing"):
            total, values = self._view("rp2005-2019", view)
            self.assertEqual(total, 7957, view)
            for ref in self.REFS:
                self.assertEqual(values.get(ref), "", f"{view}/{ref}")


if __name__ == "__main__":
    unittest.main()
