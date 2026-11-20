import hashlib
import re
import unittest
from pathlib import Path

from byz import generated
from byz.curate import diff, docs, editions

ROOT_ITEMS = (
    "editions",
    "source",
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

    def test_generated_block_is_marked_and_says_the_rest_is_hand_written(self):
        block = self.text[
            self.text.index(docs.BEGIN) : self.text.index(docs.END)
        ]
        self.assertIn(generated.BLOCK_MARKER, block)
        self.assertIn("hand-written", block)
        self.assertIn("python3 scripts/build_editions.py", block)

    def test_lists_generated_files_and_commands(self):
        block = self.text[
            self.text.index(docs.BEGIN) : self.text.index(docs.END)
        ]
        self.assertIn("## Generated files", block)
        for row in generated.GENERATED_FILES:
            self.assertIn(row["label"], block)
            self.assertIn(row["command"], block)
        # `pdfs.toml` is hand-maintained: it may only appear in the sentence
        # that says so, never as a generated table row.
        for line in block.splitlines():
            if "pdfs.toml" in line:
                self.assertIn("hand-maintained", line, line)


class EditionsDocLinkTests(unittest.TestCase):
    """R1: every reference a reader would want to follow is a link."""

    REPO = "https://github.com/byztxt/byzantine-majority-text"
    TAG_PREFIX = f"{REPO}/releases/tag/"
    COMMIT_PREFIX = f"{REPO}/commit/"

    def setUp(self):
        self.path = editions.DOCS_DIR / "EDITIONS.md"
        self.text = self.path.read_text(encoding="utf-8")

    def test_repo_url_is_defined_once(self):
        self.assertEqual(docs.REPO_URL, self.REPO)
        source = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "byz"
            / "curate"
            / "docs.py"
        ).read_text(encoding="utf-8")
        self.assertEqual(source.count(docs.REPO_URL), 1)

    def test_every_release_tag_is_a_link(self):
        tags = re.findall(r"`v\d+\.\d+\.\d+`", self.text)
        self.assertTrue(tags)
        self.assertEqual(
            len(tags), self.text.count(f"]({self.TAG_PREFIX}")
        )
        # A tag must not survive anywhere outside a link, with or without
        # backticks. The manifest's `Basis` prose is the case this catches.
        without_links = re.sub(r"\[[^\]]*\]\([^)]*\)", "", self.text)
        self.assertIsNone(
            re.search(r"v\d+\.\d+\.\d+", without_links),
            "unlinked release tag in docs/EDITIONS.md",
        )

    def test_commit_hash_is_a_link(self):
        self.assertIn(f"]({self.COMMIT_PREFIX}97371d7)", self.text)
        stripped = re.sub(r"\[`97371d7`\]\([^)]+\)", "", self.text)
        self.assertNotIn("97371d7", stripped)

    def test_tag_range_links_both_endpoints(self):
        for first, last in (("v1.0.0", "v2.0.3"), ("v3.0.0", "v3.3.4")):
            self.assertIn(
                f"[`{first}`]({self.TAG_PREFIX}{first})-"
                f"[`{last}`]({self.TAG_PREFIX}{last})",
                self.text,
            )

    def test_each_diff_directory_is_a_relative_link(self):
        for left, right in diff.PAIRS:
            href = f"../reports/diffs/{left}--{right}/"
            self.assertIn(f"({href})", self.text)
        self.assertIn(
            "[`RELEASE-NOTES.md`](RELEASE-NOTES.md)", self.text
        )

    def test_official_editions_keep_plain_none(self):
        # The two official editions have no repo release; that cell stays plain
        # text (only tags, commits, and diff directories are linkified).
        for edition_id in ("rp2005", "rp2018"):
            line = next(
                row
                for row in self.text.splitlines()
                if row.startswith(f"| `{edition_id}` |")
            )
            self.assertIn("| none |", line)
            self.assertNotIn("[`none`]", line)


class PdfLinkTests(unittest.TestCase):
    """The official PDFs are committed, so user-facing links are local."""

    def _user_docs(self):
        paths = [
            editions.DOCS_DIR / "EDITIONS.md",
            editions.DOCS_DIR / "COLLATEX.md",
            editions.DOCS_DIR / "RELEASE-NOTES.md",
            editions.ROOT / "README.md",
        ]
        paths += [
            editions.edition_dir(edition_id) / "README.md"
            for edition_id in editions.EDITIONS
        ]
        return paths

    def test_relative_markdown_links_resolve(self):
        for path in self._user_docs():
            text = path.read_text(encoding="utf-8")
            for link in re.findall(r"\]\(([^)]+)\)", text):
                if link.startswith(("http://", "https://", "#")):
                    continue
                target = link.split("#", 1)[0]
                if not target:
                    continue
                resolved = (path.parent / target).resolve()
                self.assertTrue(
                    resolved.exists(), f"{path.name}: broken link {link}"
                )

    def test_official_pdf_links_point_at_the_committed_files(self):
        docs = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
        self.assertIn("](../data/raw/rp2005/official-pdf/editions-rp2.pdf)", docs)
        self.assertIn(
            "](../data/raw/rp2018/official-pdf/"
            "robinson-pierpont-2018-gnt-edition.pdf)",
            docs,
        )
        for edition_id, filename in (
            ("rp2005", "editions-rp2.pdf"),
            ("rp2018", "robinson-pierpont-2018-gnt-edition.pdf"),
        ):
            readme = (
                editions.edition_dir(edition_id) / "README.md"
            ).read_text(encoding="utf-8")
            expected = (
                f"(../../data/raw/{edition_id}/official-pdf/{filename})"
            )
            self.assertIn(expected, readme)
            self.assertNotIn("https://byzantinetext.com", readme)


class DocsTests(unittest.TestCase):
    """The reader-facing docs survive the removal of the convenience trees."""

    def test_collatex_doc_and_assets_exist(self):
        self.assertTrue(
            (editions.DOCS_DIR / "COLLATEX.md").is_file(), "COLLATEX.md"
        )
        for name in ("coll.png", "demo_collation.xlsx", "demo_john_1.xml"):
            self.assertTrue((editions.DOCS_DIR / "assets" / name).is_file(), name)

    def test_collatex_doc_keeps_the_walkthrough(self):
        text = (editions.DOCS_DIR / "COLLATEX.md").read_text(encoding="utf-8")
        self.assertIn("https://collatex.net/download/", text)
        self.assertIn(
            "https://ntvmr.uni-muenster.de/community/vmr/api/transcript/get/"
            "?docID=10066",
            text,
        )
        self.assertIn("java -jar collatex-tools-1.7.1.jar -xp '//w'", text)
        self.assertIn("demo_john_1.xml", text)
        self.assertIn("assets/coll.png", text)
        self.assertIn("assets/demo_collation.xlsx", text)
        self.assertIn("hand-prepared", text)
        self.assertIn("not a pipeline output", text)

    def test_release_notes_document_the_removal(self):
        text = (editions.DOCS_DIR / "RELEASE-NOTES.md").read_text(encoding="utf-8")
        self.assertIn("404", text)
        self.assertIn("EDITIONS.md", text)
        for old, _ in docs.RETIRED_PATHS:
            # The release note repeats the six data paths; the synthetic
            # "(second view)" row and the two removed READMEs point at the
            # canonical table in EDITIONS.md instead.
            if "(" in old:
                continue
            self.assertIn(old, text)

    def test_editions_doc_maps_every_retired_path(self):
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
        self.assertIn("## Where the old working-tree paths went", text)
        self.assertIn("| Retired path | Now |", text)
        for old, new in docs.RETIRED_PATHS:
            self.assertIn(old, text)
            for target in new.split(";"):
                self.assertIn(target.strip(), text)
        self.assertIn("The bytes did not change", text)

    def test_editions_doc_points_at_the_release_note(self):
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
        self.assertIn("RELEASE-NOTES.md", text)
        self.assertIn("COLLATEX.md", text)

    def test_root_readme_has_no_retired_tree(self):
        text = (editions.ROOT / "README.md").read_text(encoding="utf-8")
        prefixes = {
            old.split("/", 1)[0] + "/" for old, _ in docs.RETIRED_PATHS
        }
        for prefix in prefixes:
            self.assertNotIn(prefix, text)

    def test_scripts_readme_has_no_retired_converter(self):
        text = (editions.ROOT / "scripts" / "README.md").read_text(encoding="utf-8")
        for name in ("csv_converter", "tei_xml_converter", "Csv converter"):
            self.assertNotIn(name, text)


if __name__ == "__main__":
    unittest.main()
