import csv
import hashlib
import json
import re
import subprocess
import unittest

from byz.curate import diff, editions


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CurateIntegrationTests(unittest.TestCase):
    def test_edition_layout(self):
        for edition_id in editions.EDITIONS:
            root = editions.edition_dir(edition_id)
            for name in ("source", "csv", "tei", "manifest.json", "README.md"):
                self.assertTrue((root / name).exists(), f"{edition_id}/{name}")

    def test_manifests(self):
        for edition_id in editions.EDITIONS:
            manifest = json.loads(
                (editions.edition_dir(edition_id) / "manifest.json").read_text()
            )
            self.assertEqual(manifest["edition"], edition_id)
            self.assertTrue(manifest["source_files"])
            self.assertTrue(manifest["artifact_files"])

    def test_historical_manifest_tag_and_commit(self):
        manifest = json.loads(
            (
                editions.edition_dir("rp2005-2019") / "manifest.json"
            ).read_text()
        )
        self.assertEqual(manifest["tag"], "v2.0.3")
        self.assertEqual(len(manifest["commit"]), 40)

    def test_golden_matthew_1_1(self):
        expected = "Βίβλος γενέσεως Ἰησοῦ χριστοῦ, υἱοῦ Δαυίδ, υἱοῦ Ἀβραάμ."
        for edition_id in editions.EDITIONS:
            path = (
                editions.edition_dir(edition_id)
                / "csv"
                / "accented"
                / "no-variants"
                / "MAT.csv"
            )
            rows = list(csv.DictReader(path.open(encoding="utf-8")))
            self.assertEqual(rows[0]["text"], expected, edition_id)

    def test_historical_recovery_matches_git(self):
        path = (
            editions.edition_dir("rp2005-2019")
            / "source"
            / "textonly-beta-code"
            / "MT.CCT"
        )
        self.assertTrue(path.is_file())
        result = subprocess.run(
            [
                "git",
                "-C",
                str(editions.ROOT),
                "show",
                "v2.0.3:textonly-beta-code/MT.CCT",
            ],
            capture_output=True,
            check=True,
        )
        self.assertEqual(
            hashlib.sha256(result.stdout).hexdigest(),
            sha256(path),
        )

    def test_official_source_counts(self):
        rp2005 = editions.edition_dir("rp2005") / "source" / "ccat"
        rp2018 = editions.edition_dir("rp2018") / "source" / "ccat"
        self.assertEqual(len(list(rp2005.glob("*.CCT"))), 29)
        self.assertEqual(len(list(rp2018.glob("*.CCT"))), 30)

    def test_current_source_matches_working_tree(self):
        path = (
            editions.edition_dir("rp2018-2023")
            / "source"
            / "CCAT"
            / "01_MAT.TXT"
        )
        self.assertEqual(
            sha256(path),
            sha256(editions.ROOT / "source" / "CCAT" / "01_MAT.TXT"),
        )

    def test_diff_reports_and_counts(self):
        source_counts = {
            "rp2005--rp2005-2019": 54,
            "rp2005-2019--rp2018": 3,
            "rp2018--rp2018-2023": 161,
            "rp2005--rp2018": 55,
        }
        derived_counts = {
            "rp2005--rp2005-2019": 46,
            "rp2005-2019--rp2018": 3,
            "rp2018--rp2018-2023": 97,
            "rp2005--rp2018": 47,
        }
        apparatus_only = {
            "rp2005--rp2005-2019": 8,
            "rp2005-2019--rp2018": 0,
            "rp2018--rp2018-2023": 156,
            "rp2005--rp2018": 8,
        }
        for name, count in source_counts.items():
            directory = editions.DIFFS_DIR / name
            for filename in (
                "report.md",
                "changes.csv",
                "source.diff",
                "text.diff",
                "derived.diff",
            ):
                self.assertTrue(
                    (directory / filename).is_file(), f"{name}/{filename}"
                )
            report = (directory / "report.md").read_text(encoding="utf-8")
            self.assertIn(
                f"**Source-tier differing verses:** {count}", report
            )
            self.assertIn(
                "**Derived-text differing verses (normalised):** "
                f"{derived_counts[name]}",
                report,
            )
            self.assertIn(
                "**Apparatus-only changes (source differs, main text "
                f"identical):** {apparatus_only[name]}",
                report,
            )
            # The legend and at least one accented word diff must be visible.
            self.assertIn("`[-removed-]{+added+}`", report)
            self.assertRegex(
                report, r"[\u0370-\u03ff].*\[-.*?-\]\{\+.*?\+\}"
            )
            self.assertIn("## Main-text changes", report)
            self.assertIn("## Apparatus-only changes", report)
            self.assertIn(
                "The marker delimiters are the fixed strings", report
            )
            # Greek epsilon, not Latin `e`, in the dash-spacing example.
            self.assertIn("[-εἶπεν --]{+εἶπεν-+}", report)
            self.assertNotIn("{+eἶπεν-+}", report)
            if apparatus_only[name]:
                self.assertIn("## Apparatus-only changes", report)

    def test_diff_files_agree_with_the_csv(self):
        expected_fields = [
            "book",
            "chapter",
            "verse",
            "category",
            "source_word_diff",
            "text_word_diff",
            "source_left",
            "source_right",
            "text_left",
            "text_right",
            "text_changed",
        ]
        for name in (
            "rp2005--rp2005-2019",
            "rp2005-2019--rp2018",
            "rp2018--rp2018-2023",
            "rp2005--rp2018",
        ):
            directory = editions.DIFFS_DIR / name
            with (directory / "changes.csv").open(
                newline="", encoding="utf-8"
            ) as handle:
                reader = csv.DictReader(handle)
                self.assertEqual(reader.fieldnames, expected_fields, name)
                rows = list(reader)
            self.assertTrue(rows, name)
            for row in rows:
                self.assertIn(row["text_changed"], ("true", "false"), name)
                # A pure-whitespace source change is intentionally unmarked.
                if row["category"] != "whitespace":
                    self.assertTrue(
                        "[-" in row["source_word_diff"]
                        or "{+" in row["source_word_diff"],
                        f"{name}: {row['book']} "
                        f"{row['chapter']}:{row['verse']}",
                    )
            exact = [
                row for row in rows if row["text_left"] != row["text_right"]
            ]
            source_diff = (directory / "source.diff").read_text(
                encoding="utf-8"
            )
            text_diff = (directory / "text.diff").read_text(encoding="utf-8")
            derived_diff = (directory / "derived.diff").read_text(
                encoding="utf-8"
            )
            self.assertEqual(
                sum(1 for line in source_diff.splitlines() if line.startswith("@@ ")),
                len(rows),
                name,
            )
            self.assertEqual(
                sum(1 for line in text_diff.splitlines() if line.startswith("@@ ")),
                len(exact),
                name,
            )
            self.assertIn(
                "Includes typographic/converter-generation differences", derived_diff
            )
            self.assertIn("paragraph markers", derived_diff)
            self.assertIn("apostrophe typography", derived_diff)
            self.assertIn("exact Unicode accented main text", text_diff)
            self.assertIn(
                "derived.diff is the normalised full view", text_diff
            )
            self.assertIn(
                f"--- {name.split('--')[0]}/text (Unicode accented main text)",
                derived_diff,
            )

    def test_diff_has_unicode_first_examples(self):
        report = (
            editions.DIFFS_DIR / "rp2005-2019--rp2018" / "report.md"
        ).read_text(encoding="utf-8")
        # Letters/punctuation change: the Unicode diff marks the words.
        self.assertIn("### MAT 1:18 · `letters`", report)
        self.assertIn("[-ἦν.-]{+ἦν·+}", report)
        self.assertIn("[-Μνηστευθείσης-]{+μνηστευθείσης+}", report)
        self.assertIn("### REV 11:15 · `punctuation`", report)
        self.assertIn("[-κόσμου,-]{+κόσμου+}", report)
        self.assertIn("[-ἡμῶν,-]{+ἡμῶν+}", report)
        # The Text view is normalised, so no paragraph-marker noise.
        self.assertNotIn("{+¶", report)
        # Apparatus-only variant in an official-to-official pair.
        official = (
            editions.DIFFS_DIR / "rp2005--rp2018" / "report.md"
        ).read_text(encoding="utf-8")
        # Apparatus-only changes are compact bullets, not full verse blocks.
        self.assertIn("- `1CO 3:14` · `variant`", official)
        self.assertIn("{+{N ME/NEI > MENEI= }+}", official)

    def test_diff_csv_rows_flag_apparatus_only(self):
        with (
            editions.DIFFS_DIR / "rp2005--rp2018" / "changes.csv"
        ).open(newline="", encoding="utf-8") as handle:
            rows = {
                (row["book"], int(row["chapter"]), int(row["verse"])): row
                for row in csv.DictReader(handle)
            }
        apparatus = rows[("1CO", 3, 14)]
        self.assertEqual(apparatus["category"], "variant")
        self.assertEqual(apparatus["text_changed"], "false")
        # The apparatus change is still visible in the source word diff.
        self.assertIn("{+{N ME/NEI > MENEI= }+}", apparatus["source_word_diff"])
        changed = rows[("1CO", 7, 5)]
        self.assertEqual(changed["category"], "letters")
        self.assertEqual(changed["text_changed"], "true")
        self.assertIn("[-μή τι-]{+μήτι+}", changed["text_word_diff"])
        self.assertIn("[-MH/", changed["source_word_diff"])
        self.assertIn("MH/TI", changed["source_word_diff"])

    def test_text_word_diff_is_normalised_but_text_columns_are_exact(self):
        with (
            editions.DIFFS_DIR / "rp2005-2019--rp2018" / "changes.csv"
        ).open(newline="", encoding="utf-8") as handle:
            rows = {
                (row["book"], int(row["chapter"]), int(row["verse"])): row
                for row in csv.DictReader(handle)
            }
        row = rows[("REV", 11, 15)]
        # The readable word diff omits paragraph markers and shows the real
        # punctuation changes.
        self.assertNotIn("¶", row["text_word_diff"])
        self.assertIn("[-κόσμου,-]{+κόσμου+}", row["text_word_diff"])
        self.assertIn("[-ἡμῶν,-]{+ἡμῶν+}", row["text_word_diff"])
        # The exact text columns keep the paragraph marker as stored.
        self.assertTrue(row["text_left"].startswith("Καὶ"))
        self.assertTrue(row["text_right"].startswith("¶Καὶ"))
        self.assertIn("¶", row["text_right"])

    def test_derived_only_section(self):
        report = (
            editions.DIFFS_DIR / "rp2018--rp2018-2023" / "report.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "**Derived-only differences (text differs, source-tier "
            "comparison unchanged):** 92",
            report,
        )
        self.assertIn("## Derived-only differences", report)
        section = report[report.index("## Derived-only differences") :]
        self.assertIn("canonicalises dash spacing", section)
        self.assertIn("attached-vs-spaced dashes", section)
        # Paragraph markers are normalised away, so they cannot explain a
        # derived-only row.
        self.assertNotIn("paragraph markers", section)
        self.assertIn("`1CO`: 7:11", report)
        # Pairs with no derived-only difference say so explicitly.
        clean = (
            editions.DIFFS_DIR / "rp2005-2019--rp2018" / "report.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "None: every derived-text difference is also a source-tier",
            clean,
        )

    def test_text_diff_includes_exact_formatting_changes(self):
        text_diff = (
            editions.DIFFS_DIR / "rp2005--rp2005-2019" / "text.diff"
        ).read_text(encoding="utf-8")
        # 2PE 1:12 differs only by a paragraph marker in the exact text.
        self.assertIn("@@ 2PE 1:12 [accents-breathings] @@", text_diff)
        start = text_diff.index("@@ 2PE 1:12")
        end = text_diff.find("\n@@ ", start + 1)
        block = text_diff[start : end if end != -1 else None]
        self.assertIn("¶", block)
        # rp2005 has the paragraph marker, rp2005-2019 does not.
        self.assertIn("-¶Διὸ", block)
        self.assertIn("+Διὸ", block)

    def test_readme_is_generated_from_the_module_constant(self):
        path = editions.DIFFS_DIR / "README.md"
        self.assertTrue(path.is_file())
        self.assertEqual(path.read_text(encoding="utf-8"), diff.README_TEXT)
        self.assertIn("canonicalises dash spacing", diff.README_TEXT)
        self.assertIn("attached-vs-spaced dashes", diff.README_TEXT)
        self.assertIn("empty rows", diff.README_TEXT)
        self.assertIn("not patchable unified diffs", diff.README_TEXT)
        self.assertIn(
            "The marker delimiters are the fixed strings", diff.README_TEXT
        )
        self.assertIn("[-εἶπεν --]{+εἶπεν-+}", diff.README_TEXT)
        self.assertNotIn("{+eἶπεν-+}", diff.README_TEXT)

    def test_word_diffs_reconstruct_the_reference_text(self):
        marker = re.compile(r"\[-(.*?)-\]|\{\+(.*?)\+\}", re.S)

        def apply_markers(text, side):
            def replace(match):
                deleted, added = match.group(1), match.group(2)
                if side == "left":
                    return deleted or ""
                return added or ""

            return marker.sub(replace, text)

        def words(text):
            return re.findall(r"\S+", text)

        for name in (
            "rp2005--rp2005-2019",
            "rp2005-2019--rp2018",
            "rp2018--rp2018-2023",
            "rp2005--rp2018",
        ):
            with (
                editions.DIFFS_DIR / name / "changes.csv"
            ).open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            for row in rows:
                label = f"{name}: {row['book']} {row['chapter']}:{row['verse']}"
                for side, column in (
                    ("left", "source_left"),
                    ("right", "source_right"),
                ):
                    rebuilt = apply_markers(
                        row["source_word_diff"], side
                    )
                    self.assertEqual(words(rebuilt), words(row[column]), label)
                for side, column in (
                    ("left", "text_left"),
                    ("right", "text_right"),
                ):
                    rebuilt = apply_markers(row["text_word_diff"], side)
                    expected = diff.normalize_text(row[column])
                    self.assertEqual(words(rebuilt), words(expected), label)

    def test_official_artifact_views(self):
        for edition_id in ("rp2005", "rp2018"):
            root = editions.edition_dir(edition_id)
            for rel in (
                "csv/accented/no-variants",
                "csv/accented/with-variants",
                "csv/unaccented",
                "tei/accented",
                "tei/unaccented",
            ):
                self.assertTrue((root / rel).is_dir(), f"{edition_id}/{rel}")
            self.assertFalse((root / "csv" / "strongs").exists())
            text = (root / "csv" / "accented" / "no-variants" / "MAT.csv").read_text()
            self.assertIn("Βίβλος", text)

    def test_released_artifact_views(self):
        for edition_id in ("rp2005-2019", "rp2018-2023"):
            root = editions.edition_dir(edition_id)
            for rel in (
                "csv/accented/no-variants",
                "csv/accented/with-variants",
                "csv/unaccented",
                "csv/strongs/with-parsing",
                "csv/strongs/no-parsing",
                "tei/accented",
                "tei/unaccented",
            ):
                self.assertTrue((root / rel).is_dir(), f"{edition_id}/{rel}")
            text = (
                root / "csv" / "strongs" / "with-parsing" / "MAT.csv"
            ).read_text()
            self.assertIn("976", text)

    def test_historical_strongs_views_are_clean(self):
        base = editions.edition_dir("rp2005-2019") / "csv" / "strongs"
        for kind in ("no-parsing", "with-parsing"):
            for path in (base / kind).glob("*.csv"):
                for row in csv.DictReader(path.open(encoding="utf-8")):
                    text = row["text"]
                    for marker in (
                        "VAR:",
                        ":END",
                        "|",
                        "<",
                        ">",
                        "OMIT",
                        "M5:",
                        "M6:",
                    ):
                        self.assertNotIn(marker, text, f"{path.name}:{row}")
                    if kind == "no-parsing":
                        self.assertNotRegex(text, r"\d|\{|\}")
                    else:
                        self.assertNotIn(" 0 ", text)
                        self.assertNotIn(" 0 {", text)

    def test_historical_strongs_matches_unaccented_except_segmentation(self):
        base = editions.edition_dir("rp2005-2019") / "csv"
        expected = {
            ("1CO", 7, 5),
            ("2CO", 1, 17),
            ("2CO", 12, 18),
            ("2CO", 13, 5),
        }
        found = set()
        for path in (base / "strongs" / "no-parsing").glob("*.csv"):
            unaccented_path = base / "unaccented" / path.name
            first = {
                (int(row["chapter"]), int(row["verse"])): row["text"]
                for row in csv.DictReader(path.open(encoding="utf-8"))
            }
            second = {
                (int(row["chapter"]), int(row["verse"])): row["text"]
                for row in csv.DictReader(unaccented_path.open(encoding="utf-8"))
            }
            for key in set(first) | set(second):
                if first.get(key, "") != second.get(key, ""):
                    found.add((path.stem, key[0], key[1]))
        self.assertEqual(found, expected)

    def test_docs_cover_all_editions(self):
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text()
        for edition_id in editions.EDITIONS:
            self.assertIn(edition_id, text)
        self.assertIn("official", text)
        self.assertIn("released", text)
        self.assertIn("v1.0.0", text)
        self.assertIn("v3.0.0", text)
        self.assertIn(
            "The marker delimiters are the fixed strings", text
        )
        self.assertIn("[-εἶπεν --]{+εἶπεν-+}", text)
        self.assertNotIn("{+eἶπεν-+}", text)


if __name__ == "__main__":
    unittest.main()
