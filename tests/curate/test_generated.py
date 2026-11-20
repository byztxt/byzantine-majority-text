"""Tests for the shared generated-file banner, registry, and classification.

`byz.generated` is the single source of truth for the banner wording, the
idempotent insertion helper, and the list of generated paths that the root
README documents. These tests lock the exact strings and the banner scope so a
new writer cannot quietly produce an unidentified generated file.
"""

import fnmatch
import unittest
from pathlib import Path

from byz import generated
from byz.reconcile import sources

ROOT = Path(__file__).resolve().parents[2]

VISIBLE_HEADING = "> **Generated file. Do not edit by hand.**"


def expand(patterns):
    """Expand a registry pattern tuple to repo-relative file paths."""
    matches = set()
    for pattern in patterns:
        if any(char in pattern for char in "*?["):
            matches.update(
                str(path.relative_to(ROOT))
                for path in ROOT.glob(pattern)
                if path.is_file()
            )
        else:
            matches.add(pattern)
    return matches


def generated_markdown():
    return expand(generated.GENERATED_MARKDOWN)


class MarkdownBannerTests(unittest.TestCase):
    def test_marker_and_wording_are_exact(self):
        self.assertEqual(
            generated.MARKDOWN_MARKER,
            "<!-- generated-file: do not edit by hand -->",
        )
        self.assertEqual(
            generated.markdown("# Title\n"),
            "<!-- generated-file: do not edit by hand -->\n"
            "> **Generated file. Do not edit by hand.**\n"
            '> See the "Generated files" section of the repository README for '
            "the command\n"
            "> that regenerates it.\n"
            "\n"
            "# Title\n",
        )

    def test_markdown_helper_is_idempotent(self):
        once = generated.markdown("# Title\n")
        self.assertEqual(generated.markdown(once), once)
        twice = generated.markdown(generated.markdown("Body"))
        self.assertEqual(twice, generated.markdown("Body"))

    def test_markdown_helper_preserves_the_body(self):
        text = "# Title\n\nBody with no banner.\n"
        self.assertTrue(generated.markdown(text).endswith(text))

    def test_toml_header_is_three_comment_lines_without_equals(self):
        header = generated.toml_header()
        self.assertEqual(
            header,
            [
                "# generated-file: do not edit by hand",
                '# See the "Generated files" section of the repository README '
                "for the command",
                "# that regenerates it.",
            ],
        )
        for line in header:
            self.assertNotIn("=", line)

    def test_block_banner_names_the_command_and_partial_generation(self):
        banner = generated.block_banner("python3 scripts/build_editions.py")
        text = "\n".join(banner)
        self.assertEqual(banner[0], generated.BLOCK_MARKER)
        self.assertIn("python3 scripts/build_editions.py", text)
        self.assertIn("hand-written", text)
        self.assertNotIn("=", text)


class BannerScopeTests(unittest.TestCase):
    def test_every_generated_markdown_starts_with_the_banner(self):
        paths = sorted(generated_markdown())
        self.assertEqual(len(paths), 17, paths)
        for rel in paths:
            lines = (ROOT / rel).read_text(encoding="utf-8").splitlines()
            self.assertEqual(lines[0], generated.MARKDOWN_MARKER, rel)
            self.assertEqual(lines[1], VISIBLE_HEADING, rel)
            self.assertEqual(lines[4], "", f"{rel}: no blank line after banner")
            self.assertTrue(lines[5].startswith("#"), f"{rel}: body moved")

    def test_every_markdown_under_generated_trees_is_classified(self):
        found = set()
        for tree in ("docs", "editions", "reports"):
            found.update(
                str(path.relative_to(ROOT))
                for path in (ROOT / tree).rglob("*.md")
            )
        self.assertEqual(
            found, generated_markdown() | set(generated.HAND_MAINTAINED_DOCS)
        )

    def test_hand_maintained_docs_are_explicit_and_banner_free(self):
        # The classification test above only passes because these two files are
        # listed in HAND_MAINTAINED_DOCS; keep the list, not a "anything goes"
        # exception.
        for rel in generated.HAND_MAINTAINED_DOCS:
            self.assertIn(rel, generated.HAND_MAINTAINED)
            self.assertTrue((ROOT / rel).is_file(), rel)
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertFalse(text.startswith(generated.MARKDOWN_MARKER), rel)

    def test_pdfs_toml_is_hand_maintained_and_has_no_banner(self):
        path = ROOT / "data" / "provenance" / "pdfs.toml"
        self.assertIn("data/provenance/pdfs.toml", generated.HAND_MAINTAINED)
        text = path.read_text(encoding="utf-8")
        self.assertFalse(text.startswith(generated.TOML_MARKER))
        self.assertNotIn("source_page", text)

    def test_hand_maintained_files_are_not_matched_by_the_registry(self):
        patterns = [
            pattern
            for row in generated.GENERATED_FILES
            for pattern in row["patterns"]
        ]
        for rel in generated.HAND_MAINTAINED:
            for path in ROOT.glob(rel):
                relative = str(path.relative_to(ROOT))
                for pattern in patterns:
                    self.assertFalse(
                        fnmatch.fnmatch(relative, pattern),
                        f"hand-maintained {relative} matches generated {pattern}",
                    )


class RegistryTests(unittest.TestCase):
    def test_registry_has_one_row_per_generated_family(self):
        self.assertEqual(len(generated.GENERATED_FILES), 12)
        for row in generated.GENERATED_FILES:
            self.assertTrue(row["label"])
            self.assertTrue(row["command"])
            self.assertIsInstance(row["patterns"], tuple)

    def test_generated_registry_covers_the_banner_scope(self):
        patterns = [
            pattern
            for row in generated.GENERATED_FILES
            for pattern in row["patterns"]
        ]
        for rel in sorted(generated_markdown()):
            self.assertTrue(
                any(fnmatch.fnmatch(rel, pattern) for pattern in patterns),
                f"{rel} is not listed in GENERATED_FILES",
            )

    def test_registry_lists_the_two_generated_tomls_and_not_pdfs(self):
        rendered = "\n".join(
            f"{row['label']} {row['command']}"
            for row in generated.GENERATED_FILES
        )
        self.assertIn("data/provenance/rp2005.toml", rendered)
        self.assertIn("data/provenance/rp2018.toml", rendered)
        self.assertNotIn("data/provenance/pdfs.toml", rendered)


class ProseTests(unittest.TestCase):
    def test_tech_section_two_names_the_listing_page(self):
        tech = (ROOT / "SPECS" / "TECH.md").read_text(encoding="utf-8")
        section = tech.split("## 2.", 1)[1].split("## 3.", 1)[0]
        self.assertIn(sources.SOURCE_PAGE, section)
        self.assertIn("November 2026", section)
        self.assertIn("source_page", section)


if __name__ == "__main__":
    unittest.main()
