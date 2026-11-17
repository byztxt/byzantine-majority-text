import hashlib
import re
import unittest

from byz.curate import docs, editions

ROOT_ITEMS = (
    "editions",
    "source",
    "csv-unicode",
    "tei-xml-unicode",
    "data",
    "docs",
    "reports",
    "scripts",
    "src",
    "tests",
    "essay",
    "SPECS",
    ".opencode",
)


class EditionTests(unittest.TestCase):
    def test_four_editions(self):
        self.assertEqual(
            set(editions.EDITIONS),
            {"rp2005", "rp2005-2019", "rp2018", "rp2018-2023"},
        )

    def test_release_ranges(self):
        historical = editions.metadata("rp2005-2019")
        current = editions.metadata("rp2018-2023")
        self.assertEqual(historical["first_release"], "v1.0.0")
        self.assertEqual(historical["latest_release"], "v2.0.3")
        self.assertEqual(current["first_release"], "v3.0.0")
        self.assertTrue(current["latest_release"].startswith("v3."))
        self.assertEqual(
            historical["release_range"],
            f"{historical['first_release']}-{historical['latest_release']}",
        )
        self.assertEqual(editions.metadata("rp2005")["release_range"], "")
        self.assertEqual(editions.metadata("rp2018")["release_range"], "")

    def test_official_status(self):
        self.assertEqual(editions.metadata("rp2005")["status"], "official")
        self.assertEqual(editions.metadata("rp2018")["status"], "official")
        self.assertEqual(editions.metadata("rp2005-2019")["status"], "released")
        self.assertEqual(editions.metadata("rp2018-2023")["status"], "released")

    def test_official_edition_has_no_release_range(self):
        self.assertEqual(editions.release_range(editions.EDITIONS["rp2005"]), ("", ""))
        self.assertEqual(editions.release_range(editions.EDITIONS["rp2018"]), ("", ""))

    def test_released_edition_without_tags_raises(self):
        original = editions.tags
        editions.tags = lambda: []
        try:
            with self.assertRaises(RuntimeError) as caught:
                editions.release_range(editions.EDITIONS["rp2018-2023"])
        finally:
            editions.tags = original
        self.assertIn("rp2018-2023", str(caught.exception))

    def test_tag_command_failure_names_the_command(self):
        original = editions.subprocess.run

        class Result:
            returncode = 128
            stdout = ""
            stderr = "fatal: not a git repository"

        editions.subprocess.run = lambda *args, **kwargs: Result()
        try:
            with self.assertRaises(RuntimeError) as caught:
                editions.tags()
        finally:
            editions.subprocess.run = original
        message = str(caught.exception)
        self.assertIn("git -C", message)
        self.assertIn("tag --list", message)

    def test_pdf_hashes(self):
        text = (editions.PROVENANCE_DIR / "pdfs.toml").read_text()
        records = {}
        current = {}
        for line in text.splitlines():
            if line.strip() == "[[pdfs]]":
                if current.get("path"):
                    records[current["path"]] = current.get("sha256", "")
                current = {}
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                current[key.strip()] = value.strip().strip('"')
        if current.get("path"):
            records[current["path"]] = current.get("sha256", "")
        self.assertEqual(len(records), 2)
        for relpath, expected in records.items():
            path = editions.ROOT / relpath
            self.assertTrue(path.is_file())
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(digest, expected)


class RootReadmeTests(unittest.TestCase):
    """The root README orients newcomers and stays generator-reproducible."""

    def setUp(self):
        self.path = editions.ROOT / "README.md"
        self.text = self.path.read_text(encoding="utf-8")

    def test_lists_every_root_directory(self):
        for name in ROOT_ITEMS:
            self.assertIn(f"`{name}/`", self.text, f"README does not list {name}/")

    def test_has_exactly_one_generated_block(self):
        self.assertEqual(self.text.count(docs.BEGIN), 1)
        self.assertEqual(self.text.count(docs.END), 1)
        self.assertLess(self.text.index(docs.BEGIN), self.text.index(docs.END))
        for edition_id in editions.EDITIONS:
            self.assertIn(f"| `{edition_id}` |", self.text)

    def test_has_no_contradictory_version_wording(self):
        self.assertNotIn("Four versions are available", self.text)
        # "source of truth" may only be claimed for the PDFs (the ultimate
        # authority for the printed editions) or with machine-readable context.
        for sentence in re.split(r"(?<=[.!?])\s+", self.text):
            if "source of truth" in sentence:
                self.assertTrue(
                    "PDF" in sentence or "machine-readable" in sentence,
                    f"unqualified source-of-truth claim: {sentence!r}",
                )

    def test_generated_block_matches_the_generator(self):
        self.assertEqual(docs.render_root_readme(self.text), self.text)


if __name__ == "__main__":
    unittest.main()
