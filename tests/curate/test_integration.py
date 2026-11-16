import csv
import hashlib
import json
import subprocess
import unittest

from byz.curate import editions


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
        expected = {
            "rp2005--rp2005-2019": 54,
            "rp2005-2019--rp2018": 3,
            "rp2018--rp2018-2023": 161,
            "rp2005--rp2018": 55,
        }
        for name, count in expected.items():
            directory = editions.DIFFS_DIR / name
            self.assertTrue((directory / "report.md").is_file())
            self.assertTrue((directory / "changes.csv").is_file())
            self.assertIn(
                f"**Differing verses:** {count}",
                (directory / "report.md").read_text(),
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


if __name__ == "__main__":
    unittest.main()
