import hashlib
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from byz import generated
from byz.curate import diff, docs, editions

ROOT_ITEMS = (
    "editions",
    "data",
    "docs",
    "reports",
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
    """The root README is a render of a template the generator owns."""

    def setUp(self):
        self.path = editions.ROOT / "README.md"
        self.text = self.path.read_text(encoding="utf-8")
        self.template = (
            editions.ROOT / "src" / "byz" / "curate" / "README.template.md"
        ).read_text(encoding="utf-8")

    def test_readme_equals_the_template_render(self):
        self.assertEqual(
            self.text,
            generated.markdown(docs.render_root_readme(self.template)),
        )

    def test_readme_starts_with_the_generated_banner(self):
        lines = self.text.splitlines()
        self.assertEqual(lines[0], generated.MARKDOWN_MARKER)
        self.assertEqual(lines[1], "> **Generated file. Do not edit by hand.**")

    def test_readme_has_no_block_markers(self):
        self.assertNotIn("editions:begin", self.text)
        self.assertNotIn("editions:end", self.text)
        self.assertNotIn("generated-block", self.text)

    def test_lists_every_root_directory(self):
        for name in ROOT_ITEMS:
            self.assertIn(f"`{name}/`", self.text, f"README does not list {name}/")
        # The inputs moved under `data/` and `scripts/` became modules: neither
        # may keep a top-level row in the layout table. (The curated-editions
        # prose still names an edition's own source snapshot, which is not
        # the repository input tree.)
        self.assertNotIn("| `source/` |", self.text)
        self.assertNotIn("| `scripts/` |", self.text)

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

    def test_lists_generated_files_and_commands(self):
        self.assertIn("## Generated files", self.text)
        section = self.text.split("## Generated files", 1)[1].split("\n## ", 1)[0]
        for row in generated.GENERATED_FILES:
            self.assertIn(row["label"], section)
            self.assertIn(row["command"], section)
        # `pdfs.toml` is hand-maintained: within the generated-files section it
        # may only appear in the sentence that says so, never as a table row.
        for line in section.splitlines():
            if "pdfs.toml" in line:
                self.assertIn(
                    "hand-maintained", line, line
                )


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
            editions.DOCS_DIR / "BUILD.md",
            editions.ROOT / "data" / "raw" / "repo" / "CONVENTIONS.md",
            editions.ROOT / "README.md",
        ]
        paths += [
            editions.ROOT / "data" / "README.md",
            editions.ROOT / "data" / "raw" / "README.md",
            editions.ROOT / "data" / "raw" / "print" / "README.md",
            editions.ROOT / "data" / "raw" / "repo" / "README.md",
        ]
        paths += [
            editions.ROOT / "data" / "raw" / "print" / edition_id / "README.md"
            for edition_id in ("rp2005", "rp2018")
        ]
        paths += [
            editions.ROOT / "data" / "raw" / "repo" / edition_id / "README.md"
            for edition_id in ("rp2005-2019", "rp2018-2023")
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
        self.assertIn("](../data/raw/print/rp2005/official-pdf/editions-rp2.pdf)", docs)
        self.assertIn(
            "](../data/raw/print/rp2018/official-pdf/"
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
                f"(../../data/raw/print/{edition_id}/official-pdf/{filename})"
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

    def test_editions_doc_maps_every_retired_path(self):
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
        self.assertIn("## Where the old working-tree paths went", text)
        self.assertIn("| Retired path | Now |", text)
        self.assertIn("404", text)
        for old, new in docs.RETIRED_PATHS:
            self.assertIn(old, text)
            for target in new.split(";"):
                self.assertIn(target.strip(), text)
        # The retired-path paragraph must name the one content exception
        # instead of claiming a blanket byte identity.
        self.assertIn("MAR 16:8", text)
        self.assertNotIn("The bytes did not change:", text)

    def test_editions_doc_points_at_the_apparatus_literals(self):
        # The retired release-notes page used to explain the MAR 16:8
        # correction; the same document's apparatus section now carries it.
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
        self.assertIn("[Apparatus literals](#apparatus-literals)", text)
        self.assertIn("COLLATEX.md", text)

    def test_root_readme_has_no_retired_tree(self):
        text = (editions.ROOT / "README.md").read_text(encoding="utf-8")
        prefixes = {
            old.split("/", 1)[0] + "/" for old, _ in docs.RETIRED_PATHS
        }
        for prefix in prefixes:
            self.assertNotIn(prefix, text)

    def test_editions_doc_maps_every_moved_path(self):
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
        self.assertIn("## Where the code and inputs moved", text)
        self.assertIn("no shims", text)
        for old, new, code in docs.MOVED_PATHS:
            self.assertIn(old, text)
            # The right-hand cell always names a destination as a code span; a
            # trailing parenthetical qualifier stays prose. Only the left-hand
            # cell honours the prose flag.
            if " (" in new:
                path, _, note = new.partition(" (")
                self.assertIn(path, text)
                self.assertIn(note, text)
                self.assertIn(f"`{path}` ({note}", text)
            else:
                self.assertIn(new, text)
                self.assertIn(f"`{new}`", text)
            if code:
                self.assertIn(f"`{old}`", text)
            else:
                # A prose row must not be rendered as a code span on the left.
                self.assertNotIn(f"`{old}`", text)

    def test_editions_doc_documents_the_apparatus_literal_correction(self):
        # The one content difference from the previous release is the apparatus
        # literal at MAR 16:8; this is the only rendered account of it now.
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
        self.assertIn("## Apparatus literals", text)
        self.assertIn("MAR 16:8", text)
        self.assertIn("SHORTER ENDING", text)
        self.assertIn("σηορτερ", text)

    def test_build_doc_names_the_new_commands(self):
        text = (editions.DOCS_DIR / "BUILD.md").read_text(encoding="utf-8")
        for verb in (
            "fetch",
            "materialise",
            "build",
            "diff",
            "contract",
            "reconcile",
            "verify",
        ):
            self.assertIn(f"python3 -m byz.{verb}", text)
        self.assertIn("pip install -r requirements.txt", text)
        self.assertIn("--edition-dir", text)

    def test_editions_doc_records_where_the_snapshots_went(self):
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
        self.assertIn("## Where the edition snapshots went (2026-11-25)", text)
        for old, new in docs.SNAPSHOT_MOVES:
            self.assertIn(old, text)
            self.assertIn(new, text)
        for old, new in docs.RELEASED_ARTIFACT_MOVES:
            self.assertIn(old, text)
            self.assertIn(new, text)
        self.assertIn("`editions/<edition>/source/`", text)
        self.assertIn("`byz.verify`", text)
        self.assertIn("outputs only", text)
        self.assertIn(
            "| `manifest.json source_files` | `manifest.json inputs` |", text
        )

    def test_editions_doc_maps_the_input_class_moves(self):
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
        self.assertIn(
            "## Where the inputs moved into the print and repo classes "
            "(2026-11-25)",
            text,
        )
        for old, new in docs.INPUT_CLASS_MOVES:
            self.assertIn(old, text)
            self.assertIn(new, text)
        self.assertIn("no symlink", text)
        self.assertIn("data/raw/repo/CONVENTIONS.md", text)

    def test_source_feature_matrix_names_the_repo_paths(self):
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
        self.assertIn("`data/raw/repo/rp2018-2023/ccat`", text)
        self.assertIn("`data/raw/repo/rp2018-2023/strongs`", text)
        self.assertNotIn("| `data/text/CCAT` |", text)

    def test_editions_doc_states_the_self_verification_tradeoff(self):
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
        self.assertIn("--edition-dir", text)
        self.assertIn("cannot prove", text)
        self.assertIn("they came from the pinned inputs", text)

    def test_editions_doc_rebuild_block_uses_verify_not_recover(self):
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
        block = text.split("### Rebuilding the curated editions", 1)[1]
        block = block.split("```", 2)[1]
        self.assertIn("python3 -m byz.build", block)
        self.assertIn("python3 -m byz.verify", block)
        self.assertNotIn("python3 -m byz.recover", block)
        self.assertNotIn("python3 -m byz.materialise", block)

    def test_editions_doc_distinguishes_unaccented_from_numbers_only(self):
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
        prose = " ".join(text.split())
        self.assertIn(
            "`csv/unaccented/` is the plain unaccented text with no Strong's "
            "numbers and no parsing",
            prose,
        )
        self.assertIn("`csv/strongs/no-parsing/` keeps the Strong's numbers", prose)
        self.assertNotIn("hold the same bytes", prose)
        self.assertIn("### Book titles", text)
        self.assertIn("`Second Timothy`", text)
        self.assertIn("`Philippians`", text)
        self.assertIn("corrected on 2026-11-26", text)
        self.assertNotIn("titles the\nbooks `Second Timoty`", text)

    def test_retired_no_parsing_points_at_the_plain_text_view(self):
        text = (editions.DOCS_DIR / "EDITIONS.md").read_text(encoding="utf-8")
        self.assertIn(
            "| `csv-unicode/strongs/no-parsing` | "
            "`editions/rp2018-2023/csv/unaccented` |",
            text,
        )
        self.assertIn("numbers-only successor", text)
        self.assertIn("2026-11-26 review fix changed 54 numbers-only", text)
        self.assertNotIn(
            "Their bytes changed only at the corrected apparatus literal", text
        )

    def test_build_doc_has_no_retired_converter(self):
        text = (editions.DOCS_DIR / "BUILD.md").read_text(encoding="utf-8")
        for name in ("csv_converter", "tei_xml_converter", "Csv converter"):
            self.assertNotIn(name, text)

    def test_missing_manifest_fails_loudly(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "rp2005"
            with mock.patch.object(
                docs.editions, "edition_dir", lambda _: missing
            ):
                with self.assertRaises(ValueError) as caught:
                    docs._manifests()
            self.assertIn("missing edition manifest", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
