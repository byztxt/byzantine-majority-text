import csv
import hashlib
import json
import re
import subprocess
import unittest

from byz import generated
from byz.contract import paths
from byz.curate import diff, editions


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CurateIntegrationTests(unittest.TestCase):
    def test_edition_layout(self):
        for edition_id in editions.EDITIONS:
            root = editions.edition_dir(edition_id)
            for name in ("csv", "tei", "manifest.json", "README.md"):
                self.assertTrue((root / name).exists(), f"{edition_id}/{name}")
            self.assertFalse((root / "source").exists(), edition_id)

    def test_manifests(self):
        for edition_id in editions.EDITIONS:
            manifest = json.loads(
                (editions.edition_dir(edition_id) / "manifest.json").read_text()
            )
            self.assertEqual(manifest["edition"], edition_id)
            self.assertNotIn("source_files", manifest)
            self.assertTrue(manifest["inputs"])
            for group in manifest["inputs"]:
                self.assertTrue(group["root"].startswith("data/"))
                self.assertFalse(group["root"].startswith("editions/"))
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
            editions.ROOT
            / "data"
            / "raw"
            / "repo"
            / "rp2005-2019"
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
        rp2005 = editions.ROOT / editions.EDITIONS["rp2005"]["source_dir"]
        rp2018 = editions.ROOT / editions.EDITIONS["rp2018"]["source_dir"]
        self.assertEqual(len(list(rp2005.glob("*.CCT"))), 29)
        self.assertEqual(len(list(rp2018.glob("*.CCT"))), 30)

    def test_current_manifest_pins_the_current_inputs(self):
        manifest = json.loads(
            (
                editions.edition_dir("rp2018-2023") / "manifest.json"
            ).read_text()
        )
        self.assertEqual(len(manifest["inputs"]), 1)
        group = manifest["inputs"][0]
        self.assertEqual(group["root"], "data/raw/repo/rp2018-2023")
        self.assertEqual(
            sorted(group["include"]), ["ccat/*.TXT", "strongs/*.BP5"]
        )
        self.assertEqual(len(group["files"]), 56)
        first = next(
            entry for entry in group["files"] if entry["path"] == "ccat/01_MAT.TXT"
        )
        self.assertEqual(
            first["sha256"],
            sha256(paths.CCAT_DIR / "01_MAT.TXT"),
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
                "apparatus.diff",
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
            "apparatus_word_diff",
            "apparatus_changed",
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
                self.assertIn(row["apparatus_changed"], ("true", "false"), name)
                self.assertEqual(
                    row["apparatus_changed"] == "true",
                    bool(
                        "[-" in row["apparatus_word_diff"]
                        or "{+" in row["apparatus_word_diff"]
                    ),
                    f"{name}: {row['book']} "
                    f"{row['chapter']}:{row['verse']}: apparatus flag",
                )
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
            report = (directory / "report.md").read_text(encoding="utf-8")
            derived_count = int(
                re.search(
                    r"Derived-text differing verses \(normalised\):\*\* (\d+)",
                    report,
                ).group(1)
            )
            source_diff = (directory / "source.diff").read_text(
                encoding="utf-8"
            )
            text_diff = (directory / "text.diff").read_text(encoding="utf-8")
            derived_diff = (directory / "derived.diff").read_text(
                encoding="utf-8"
            )
            apparatus_diff = (directory / "apparatus.diff").read_text(
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
            self.assertEqual(
                sum(1 for line in derived_diff.splitlines() if line.startswith("@@ ")),
                derived_count,
                name,
            )
            self.assertEqual(
                sum(
                    1
                    for line in apparatus_diff.splitlines()
                    if line.startswith("@@ ")
                ),
                sum(
                    1
                    for row in rows
                    if row["text_changed"] == "false"
                    and row["apparatus_changed"] == "true"
                ),
                name,
            )
            left, right = name.split("--")
            self.assertIn(
                f"# Word diff: {left} -> {right} (Beta-code source tier)",
                source_diff,
            )
            self.assertIn(
                f"# Word diff: {left} -> {right} "
                "(exact Unicode accented main text)",
                text_diff,
            )
            self.assertIn(
                f"# Word diff: {left} -> {right} "
                "(normalised Unicode accented main text)",
                derived_diff,
            )
            self.assertIn(
                f"# Word diff: {left} -> {right} "
                "(Unicode accented text with apparatus)",
                apparatus_diff,
            )
            # Word-diff style: every hunk carries `[-removed-]{+added+}`, and
            # verse lines never use `-`/`+` prefixes.
            for kind, text in (
                ("source", source_diff),
                ("text", text_diff),
                ("apparatus", apparatus_diff),
                ("derived", derived_diff),
            ):
                for line in text.splitlines():
                    if line.startswith(("#", "@@")):
                        continue
                    self.assertFalse(
                        line.startswith(("-", "+")),
                        f"{name}/{kind}: verse text uses a diff prefix: "
                        f"{line[:40]}",
                    )
                    self.assertTrue(
                        "[-" in line or "{+" in line,
                        f"{name}/{kind}: unmarked hunk line: {line[:80]}",
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

    def test_diff_has_unicode_first_examples(self):
        report = (
            editions.DIFFS_DIR / "rp2005-2019--rp2018" / "report.md"
        ).read_text(encoding="utf-8")
        # Punctuation (plus capitalisation): the Unicode diff marks the words.
        self.assertIn("### MAT 1:18 · `punctuation`", report)
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
        # The Unicode apparatus line comes first, the Beta code second.
        self.assertIn(
            "- `1CO 3:14` · `variant`\n"
            "  - Apparatus (Unicode): ",
            official,
        )
        self.assertIn("  - Apparatus (Beta code): `", official)
        self.assertIn("Apparatus (Unicode): `", official)
        # The Unicode line is Greek, not Beta code.
        entry = official.split("- `1CO 3:14` · `variant`", 1)[1].split("\n- ", 1)[0]
        self.assertRegex(entry, r"[\u0370-\u03ff]")
        app = (editions.DIFFS_DIR / "rp2005--rp2018" / "apparatus.diff").read_text(
            encoding="utf-8"
        )
        start = app.index("@@ 1CO 3:14")
        block = app[start : app.find("\n@@ ", start + 1)]
        self.assertRegex(block, r"[\u0370-\u03ff]")
        self.assertIn("{+{NA μένει > μενεῖ }+}", block)

    def test_apparatus_code_rendering_at_act_1_15(self):
        # R2/R3: the tag change is explicit and the derived dash difference is
        # labelled as derived, so the category no longer contradicts the Text
        # block.  This is the positive rename guard: if the category disappears
        # or the tag line is dropped, the test fails.
        directory = editions.DIFFS_DIR / "rp2018--rp2018-2023"
        report = (directory / "report.md").read_text(encoding="utf-8")
        heading = "### ACT 1:15 \u00b7 `apparatus-code`"
        self.assertIn(heading, report)
        entry = report.split(heading, 1)[1].split("\n### ", 1)[0]
        self.assertIn(
            "Apparatus code: `N` -> `C` (the reading is unchanged)", entry
        )
        self.assertIn(
            "Text (derived; typographic only, not part of the source-tier "
            "change):",
            entry,
        )
        # Nothing is suppressed: the visible dash difference stays.
        self.assertIn("[-εἶπεν --]{+εἶπεν-+}", entry)
        self.assertIn("Source (Beta code):", entry)
        self.assertIn("[-{N-]{+{C+}", entry)
        self.assertIn("Apparatus (Unicode):", entry)
        self.assertIn("[-{NA-]{+{NA27/28+}", entry)
        with (directory / "changes.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            row = next(
                row
                for row in csv.DictReader(handle)
                if row["book"] == "ACT"
                and row["chapter"] == "1"
                and row["verse"] == "15"
            )
        self.assertEqual(row["category"], "apparatus-code")

    def test_apparatus_only_entries_print_the_tag_change(self):
        report = (
            editions.DIFFS_DIR / "rp2018--rp2018-2023" / "report.md"
        ).read_text(encoding="utf-8")
        marker = "- `ACT 1:10` \u00b7 `apparatus-code`"
        self.assertIn(marker, report)
        entry = report.split(marker, 1)[1].split("\n- ", 1)[0]
        self.assertTrue(
            entry.startswith(
                "\n  - Apparatus code: `N` -> `C` "
                "(the reading is unchanged)\n"
                "  - Apparatus (Unicode): "
            ),
            entry,
        )
        self.assertIn("\n  - Apparatus (Beta code): ", entry)
        # A reading change (`variant`) is not mislabelled as a code change.
        official = (
            editions.DIFFS_DIR / "rp2005--rp2018" / "report.md"
        ).read_text(encoding="utf-8")
        marker = "- `1CO 3:14` \u00b7 `variant`"
        self.assertIn(marker, official)
        entry = official.split(marker, 1)[1].split("\n- ", 1)[0]
        self.assertNotIn("Apparatus code:", entry)

    def test_report_categories_table_has_meanings_and_glossary_pointer(self):
        report = (
            editions.DIFFS_DIR / "rp2018--rp2018-2023" / "report.md"
        ).read_text(encoding="utf-8")
        self.assertIn("| Category | Meaning | Count |", report)
        self.assertIn("| `apparatus-code` |", report)
        self.assertIn("../README.md#categories", report)
        self.assertIn("## Main-text changes (derived text differs)", report)
        self.assertIn("grouped by the derived Unicode text", report)
        self.assertIn("## Apparatus-only changes", report)
        self.assertIn("normalised derived text", report)

    def test_glossary_examples_are_real(self):
        # The README examples are references to generated rows, not decoration.
        for category, example in diff.CATEGORY_EXAMPLES.items():
            pair, book, chapter, verse = example
            with (
                editions.DIFFS_DIR / pair / "changes.csv"
            ).open(newline="", encoding="utf-8") as handle:
                matches = [
                    row
                    for row in csv.DictReader(handle)
                    if row["book"] == book
                    and int(row["chapter"]) == chapter
                    and int(row["verse"]) == verse
                ]
            self.assertTrue(matches, f"{category}: {pair} {book} {chapter}:{verse}")
            self.assertEqual(matches[0]["category"], category, example)

    def test_generated_diff_output_has_no_old_category_name(self):
        # The old `variant-code` value must not reappear anywhere in generated
        # output.  `bad-variant-code` is the unrelated contract-validator
        # category, so it is excluded explicitly rather than by a fragile
        # pattern.
        for path in sorted(editions.DIFFS_DIR.rglob("*")):
            if path.suffix not in {".md", ".csv", ".diff"}:
                continue
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(
                "variant-code", text.replace("bad-variant-code", ""), str(path)
            )

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
        self.assertEqual(changed["category"], "word-segmentation")
        self.assertEqual(changed["text_changed"], "true")
        self.assertIn("[-μή τι-]{+μήτι+}", changed["text_word_diff"])
        self.assertIn("[-MH/", changed["source_word_diff"])
        self.assertIn("MH/TI", changed["source_word_diff"])

    def test_encoding_only_rows_say_so(self):
        # 36 rows in rp2018 -> rp2018-2023 have no Unicode apparatus difference;
        # they are Beta-code encoding-order differences. The report must name
        # them, not render an empty code span.
        report = (
            editions.DIFFS_DIR / "rp2018--rp2018-2023" / "report.md"
        ).read_text(encoding="utf-8")
        sentence = (
            "no difference after conversion to Unicode (Beta-code encoding only)"
        )
        self.assertGreaterEqual(report.count(sentence), 36)
        marker = "- `MAT 11:23` · `accents-breathings`"
        self.assertIn(marker, report)
        entry = report.split(marker, 1)[1].split("\n- ", 1)[0]
        self.assertIn(sentence, entry)
        self.assertIn("Apparatus (Beta code): `", entry)
        # The sibling pair with a single encoding-only row names it too.
        official = (
            editions.DIFFS_DIR / "rp2005--rp2018" / "report.md"
        ).read_text(encoding="utf-8")
        marker = "- `2PE 1:12` · `accents-breathings`"
        self.assertIn(marker, official)
        entry = official.split(marker, 1)[1].split("\n- ", 1)[0]
        self.assertIn(sentence, entry)

    def test_apparatus_counters_add_up(self):
        for name, total in (
            ("rp2005--rp2005-2019", 8),
            ("rp2018--rp2018-2023", 156),
            ("rp2005--rp2018", 8),
        ):
            report = (editions.DIFFS_DIR / name / "report.md").read_text(
                encoding="utf-8"
            )
            counts = {}
            for label in (
                "Apparatus-only changes shown in Unicode",
                "Apparatus-only changes with no Unicode difference "
                "(Beta-code encoding only)",
            ):
                match = re.search(re.escape(label) + r":\*\* (\d+)", report)
                self.assertIsNotNone(match, f"{name}: {label}")
                counts[label] = int(match.group(1))
            self.assertEqual(
                counts["Apparatus-only changes shown in Unicode"]
                + counts[
                    "Apparatus-only changes with no Unicode difference "
                    "(Beta-code encoding only)"
                ],
                total,
                name,
            )

    def test_readme_documents_apparatus_diff(self):
        self.assertIn("apparatus.diff", diff.README_TEXT)
        self.assertIn("Apparatus", diff.README_TEXT)
        self.assertIn("apparatus_word_diff", diff.README_TEXT)
        self.assertIn("apparatus_changed", diff.README_TEXT)
        self.assertIn("{+{Byz τε > δε }+}", diff.README_TEXT)
        readme = re.sub(r"\s+", " ", diff.README_TEXT)
        self.assertIn("one entry per verse", readme)
        self.assertIn(
            "every apparatus-only change that has a Unicode difference "
            "(encoding-only rows are named in `report.md`)",
            readme,
        )

    def test_editions_doc_lists_apparatus_diff(self):
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
        self.assertIn("apparatus.diff", text)
        self.assertIn("Unicode apparatus", text)
        prose = re.sub(r"\s+", " ", text)
        self.assertIn("one entry per verse", prose)
        self.assertIn(
            "every apparatus-only change that has a Unicode difference "
            "(encoding-only rows are named in `report.md`)",
            prose,
        )

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
        # The exact text columns keep the paragraph marker as stored. Both
        # editions now carry it: the 2019 typography is normalised.
        self.assertTrue(row["text_left"].startswith("¶Καὶ"))
        self.assertTrue(row["text_right"].startswith("¶Καὶ"))
        self.assertIn("¶", row["text_left"])
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

    def test_text_diff_shows_the_exact_stored_text(self):
        """`text.diff` carries the stored text, formatting included.

        The historical regeneration normalised the 2019 typography, so no
        current pair differs only by a paragraph marker. The exactness property
        is still locked: stripping the word-diff markers from every block must
        reproduce the exact `text_left`/`text_right` columns.
        """
        marker = re.compile(r"\[-(.*?)-\]|\{\+(.*?)\+\}", re.S)

        def side(text, which):
            def replace(match):
                deleted, added = match.group(1), match.group(2)
                return (deleted or "") if which == "left" else (added or "")

            return marker.sub(replace, text)

        directory = editions.DIFFS_DIR / "rp2005--rp2005-2019"
        with (directory / "changes.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            rows = {
                (row["book"], int(row["chapter"]), int(row["verse"])): row
                for row in csv.DictReader(handle)
            }
        text_diff = (directory / "text.diff").read_text(encoding="utf-8")
        blocks = re.split(r"^@@ ", text_diff, flags=re.M)[1:]
        expected_blocks = sum(
            1 for row in rows.values() if row["text_left"] != row["text_right"]
        )
        self.assertEqual(len(blocks), expected_blocks)
        self.assertGreater(len(blocks), 0)
        for block in blocks:
            header, _, line = block.partition("\n")
            match = re.match(r"(\S+) (\d+):(\d+) ", header)
            self.assertIsNotNone(match, header)
            book, chapter, verse = match.groups()
            row = rows[(book, int(chapter), int(verse))]
            line = line.rstrip("\n")
            self.assertEqual(side(line, "left"), row["text_left"])
            self.assertEqual(side(line, "right"), row["text_right"])
        # Paragraph markers are shown as stored, not stripped from this view.
        self.assertIn("¶", text_diff)

    def test_diff_files_use_word_diff_samples(self):
        source = (
            editions.DIFFS_DIR / "rp2005--rp2018" / "source.diff"
        ).read_text(encoding="utf-8")
        start = source.index("@@ 1CO 7:5")
        block = source[start : source.find("\n@@ ", start + 1)]
        self.assertIn("@@ 1CO 7:5 [word-segmentation] @@", block)
        self.assertIn("[-MH/", block)
        self.assertIn("MH/TI", block)
        self.assertNotIn("\n-*MH\\", source)

        text = (
            editions.DIFFS_DIR / "rp2005-2019--rp2018" / "text.diff"
        ).read_text(encoding="utf-8")
        start = text.index("@@ REV 11:15")
        block = text[start : text.find("\n@@ ", start + 1)]
        self.assertIn("@@ REV 11:15 [punctuation] @@", block)
        # Both editions carry the paragraph marker; the exact line shows it and
        # the word diff marks only the punctuation change.
        self.assertIn("¶Καὶ ὁ ἕβδομος", block)
        self.assertIn("[-κόσμου,-]{+κόσμου+}", block)
        # No whole-verse line-diff prefixes.
        self.assertNotIn("\n-Καὶ ὁ ἕβδομος", text)
        self.assertNotIn("\n+¶Καὶ ὁ ἕβδομος", text)

    def test_readme_is_generated_from_the_module_constant(self):
        path = editions.DIFFS_DIR / "README.md"
        self.assertTrue(path.is_file())
        self.assertEqual(
            path.read_text(encoding="utf-8"),
            generated.markdown(diff.README_TEXT),
        )
        self.assertIn("canonicalises dash spacing", diff.README_TEXT)
        self.assertIn("attached-vs-spaced dashes", diff.README_TEXT)
        self.assertIn("empty rows", diff.README_TEXT)
        self.assertIn("not patchable line-based diffs", diff.README_TEXT)
        self.assertIn("word-diff style", diff.README_TEXT)
        self.assertIn("no `-`/`+` whole-verse", diff.README_TEXT)
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
            directory = editions.DIFFS_DIR / name
            left_id, right_id = name.split("--")
            left_variants = diff.load_text(left_id, "with-variants")
            right_variants = diff.load_text(right_id, "with-variants")
            with (directory / "changes.csv").open(
                newline="", encoding="utf-8"
            ) as handle:
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
                if row["apparatus_changed"] == "false":
                    # The Unicode line is prose, not a marked word diff.
                    continue
                key = (
                    row["book"],
                    int(row["chapter"]),
                    int(row["verse"]),
                )
                for side, source in (
                    ("left", left_variants),
                    ("right", right_variants),
                ):
                    rebuilt = apply_markers(row["apparatus_word_diff"], side)
                    expected = diff.normalize_text(source.get(key, ""))
                    self.assertEqual(
                        words(rebuilt), words(expected), f"{label} apparatus"
                    )

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

    def test_historical_unaccented_equals_strongs_no_parsing(self):
        # Both views are generated from `parsed/*.UB5` and share one text, so
        # they are byte-identical, as in `rp2018-2023`. The old edition copied
        # the released unaccented CSV and generated the Strong's view separately,
        # which left four verses segmented differently.
        base = editions.edition_dir("rp2005-2019") / "csv"
        for path in (base / "strongs" / "no-parsing").glob("*.csv"):
            unaccented_path = base / "unaccented" / path.name
            self.assertEqual(
                path.read_bytes(),
                unaccented_path.read_bytes(),
                f"{path.name}: unaccented and strongs/no-parsing differ",
            )

    def test_docs_cover_all_editions(self):
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text()
        self.assertTrue(text.startswith(generated.MARKDOWN_MARKER + "\n"))
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
        self.assertIn("word-diff style", text)
        self.assertIn("no `-`/`+` whole-verse lines", text)


if __name__ == "__main__":
    unittest.main()
