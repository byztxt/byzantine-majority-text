"""Tests for the generated READMEs of the input tree.

The eight READMEs are rendered by `byz.curate.data_docs` from the manifests that
`byz.build` just wrote, the edition registry, and `sources.ARCHIVES`. They are
generated files: each carries the banner, states the folder's own path, the
consuming edition, the provenance record, and the command, and resolves every
relative link. No count is scraped from a directory glob.
"""

import json
import re
import unittest
from pathlib import Path

from byz import generated
from byz.curate import data_docs, editions
from byz.reconcile import sources

ROOT = editions.ROOT

README_PATHS = (
    "data/README.md",
    "data/raw/README.md",
    "data/raw/print/README.md",
    "data/raw/repo/README.md",
    "data/raw/print/rp2005/README.md",
    "data/raw/print/rp2018/README.md",
    "data/raw/repo/rp2005-2019/README.md",
    "data/raw/repo/rp2018-2023/README.md",
)

REQUIRED_HEADINGS = (
    "## What this folder holds",
    "## Contents",
    "## Provenance",
    "## Commands",
    "## Related",
)


def manifests():
    rows = {}
    for edition_id in editions.EDITIONS:
        path = editions.edition_dir(edition_id) / "manifest.json"
        rows[edition_id] = json.loads(path.read_text(encoding="utf-8"))
    return rows


class SkeletonTests(unittest.TestCase):
    def test_all_eight_readmes_exist_and_are_alone(self):
        for relative in README_PATHS:
            path = ROOT / relative
            self.assertTrue(path.is_file(), relative)
            siblings = [
                item.name
                for item in path.parent.iterdir()
                if item.name == "README.md"
            ]
            self.assertEqual(siblings, ["README.md"], relative)

    def test_each_starts_with_the_banner(self):
        for relative in README_PATHS:
            lines = (ROOT / relative).read_text(encoding="utf-8").splitlines()
            self.assertEqual(lines[0], generated.MARKDOWN_MARKER, relative)
            self.assertEqual(
                lines[1], "> **Generated file. Do not edit by hand.**", relative
            )

    def test_each_states_its_own_folder(self):
        for relative in README_PATHS:
            text = (ROOT / relative).read_text(encoding="utf-8")
            folder = relative.rsplit("/", 1)[0]
            self.assertIn(folder, text, relative)

    def test_required_headings_are_present(self):
        for relative in README_PATHS:
            text = (ROOT / relative).read_text(encoding="utf-8")
            for heading in REQUIRED_HEADINGS:
                self.assertIn(heading, text, relative)

    def test_level_specific_heading(self):
        expected = {
            "data/README.md": "## Classes",
            "data/raw/README.md": "## Classes",
            "data/raw/print/README.md": "## Editions",
            "data/raw/repo/README.md": "## Editions",
            "data/raw/print/rp2005/README.md": "## Edition",
            "data/raw/print/rp2018/README.md": "## Edition",
            "data/raw/repo/rp2005-2019/README.md": "## Edition",
            "data/raw/repo/rp2018-2023/README.md": "## Edition",
        }
        for relative, heading in expected.items():
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn(heading, text, relative)

    def test_consumer_edition_and_provenance_are_named(self):
        map_ = {
            "data/raw/print/rp2005/README.md": ("editions/rp2005/", "rp2005.toml"),
            "data/raw/print/rp2018/README.md": ("editions/rp2018/", "rp2018.toml"),
            "data/raw/repo/rp2005-2019/README.md": (
                "editions/rp2005-2019/",
                "rp2005-2019.toml",
            ),
            "data/raw/repo/rp2018-2023/README.md": (
                "editions/rp2018-2023/",
                "rp2018-2023.toml",
            ),
        }
        for relative, (edition, record) in map_.items():
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn(edition, text, relative)
            self.assertIn(record, text, relative)

    def test_repo_source_readmes_link_the_conventions(self):
        for relative in (
            "data/raw/repo/rp2005-2019/README.md",
            "data/raw/repo/rp2018-2023/README.md",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("../CONVENTIONS.md", text, relative)

    def test_print_source_readmes_do_not_claim_the_repo_conventions(self):
        for relative in (
            "data/raw/print/rp2005/README.md",
            "data/raw/print/rp2018/README.md",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertNotIn("[CONVENTIONS.md]", text, relative)
            self.assertIn("not asserted", text, relative)


class ContentTests(unittest.TestCase):
    def test_data_readme_counts_the_two_classes(self):
        text = (ROOT / "data/README.md").read_text(encoding="utf-8")
        self.assertIn("113 pinned inputs", text)
        self.assertIn("two source classes", text)
        self.assertIn("data/raw/repo/CONVENTIONS.md", text)
        for command in ("byz.fetch", "byz.materialise", "byz.build", "byz.verify"):
            self.assertIn(command, text)

    def test_raw_readme_defines_both_classes(self):
        text = (ROOT / "data/raw/README.md").read_text(encoding="utf-8")
        self.assertIn("`print/`", text)
        self.assertIn("`repo/`", text)
        self.assertIn("`rp2005`", text)
        self.assertIn("`rp2018-2023`", text)

    def test_print_readme_states_the_archives_and_counts(self):
        text = (ROOT / "data/raw/print/README.md").read_text(encoding="utf-8")
        self.assertIn(f"{len(sources.ARCHIVES)} ZIPs", text)
        self.assertIn("29 `.CCT`", text)
        self.assertIn("30 `.CCT`", text)
        self.assertIn("byz.fetch", text)

    def test_repo_readme_names_tag_and_revision(self):
        text = (ROOT / "data/raw/repo/README.md").read_text(encoding="utf-8")
        self.assertIn("v2.0.3", text)
        self.assertIn("2023-07-20", text)
        self.assertIn("byz.materialise", text)
        self.assertIn("byz.build", text)

    def test_source_readmes_state_their_counts(self):
        text = (ROOT / "data/raw/print/rp2005/README.md").read_text(
            encoding="utf-8"
        )
        for needle in ("29 `.CCT`", "27 `*_Byz.txt`", "27 `.ASC`", "1 PDF"):
            self.assertIn(needle, text)
        text = (ROOT / "data/raw/print/rp2018/README.md").read_text(
            encoding="utf-8"
        )
        for needle in ("30 `.CCT`", "27 `*_Byz.txt`", "27 `.ASC`", "1 PDF"):
            self.assertIn(needle, text)
        self.assertIn(
            "30 `.CCT`",
            (ROOT / "data/raw/repo/rp2005-2019/README.md").read_text(
                encoding="utf-8"
            ),
        )
        self.assertIn(
            "29 `.TXT`",
            (ROOT / "data/raw/repo/rp2018-2023/README.md").read_text(
                encoding="utf-8"
            ),
        )

    def test_rp2018_2023_readme_carries_the_revision_and_commits(self):
        manifest = manifests()["rp2018-2023"]
        text = (ROOT / "data/raw/repo/rp2018-2023/README.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("`2023-07-20`", text)
        self.assertIn(manifest.get("source_commit", ""), text)
        self.assertIn(manifest.get("strongs_commit", ""), text)

    def test_no_timestamp_host_or_absolute_path(self):
        for relative in README_PATHS:
            text = (ROOT / relative).read_text(encoding="utf-8")
            for needle in ("/home/", "localhost", "/tmp/", "http://127."):
                self.assertNotIn(needle, text, relative)
            dates = set(re.findall(r"\b\d{4}-\d{2}-\d{2}\b", text))
            self.assertTrue(
                dates <= {"2023-07-20"}, f"{relative}: {dates}"
            )

    def test_relative_links_resolve(self):
        for relative in README_PATHS:
            path = ROOT / relative
            text = path.read_text(encoding="utf-8")
            for link in re.findall(r"\]\(([^)]+)\)", text):
                if link.startswith(("http://", "https://", "#")):
                    continue
                target = link.split("#", 1)[0]
                if not target:
                    continue
                self.assertTrue(
                    (path.parent / target).exists(),
                    f"{relative}: broken link {link}",
                )


class RenderTests(unittest.TestCase):
    def test_rendering_twice_is_byte_identical(self):
        rows = manifests()
        self.assertEqual(
            data_docs.render_data_readme(rows),
            data_docs.render_data_readme(rows),
        )
        self.assertEqual(
            data_docs.render_raw_readme(rows),
            data_docs.render_raw_readme(rows),
        )
        for kind in ("print", "repo"):
            self.assertEqual(
                data_docs.render_class_readme(kind, rows),
                data_docs.render_class_readme(kind, rows),
            )
        for edition_id in ("rp2005", "rp2018", "rp2005-2019", "rp2018-2023"):
            self.assertEqual(
                data_docs.render_source_readme(edition_id, rows[edition_id]),
                data_docs.render_source_readme(edition_id, rows[edition_id]),
            )

    def test_pinned_counts_come_from_the_manifest(self):
        manifest = manifests()["rp2005"]
        root = "data/raw/print/rp2005/ccat"
        before = data_docs._group_count(manifest, root)
        self.assertEqual(before, 29)
        extended = json.loads(json.dumps(manifest))
        group = next(g for g in extended["inputs"] if g["root"] == root)
        group["files"].append({"path": "99_ZZZ.CCT", "sha256": "0" * 64,
                               "size": 1})
        self.assertEqual(data_docs._group_count(extended, root), before + 1)

    def test_auxiliary_counts_use_git_not_a_glob(self):
        # An untracked file cannot enter `git ls-files`; the helper is the only
        # source for the preformatted and PDF counts.
        self.assertEqual(
            data_docs._tracked_count("data/raw/print/rp2005/preformatted", "*.ASC"),
            27,
        )
        self.assertEqual(
            data_docs._tracked_count(
                "data/raw/print/rp2005/preformatted", "*.UNTRACKED"
            ),
            0,
        )

    def test_untracked_file_does_not_change_a_pinned_count(self):
        # R6.8: dropping an untracked file into an auxiliary directory (one the
        # manifest does not pin) must not move a generated count. The file is
        # created and removed inside the test, so the committed tree is
        # untouched even when the assertion fails.
        rows = manifests()
        base = ROOT / "data" / "raw" / "print" / "rp2005" / "preformatted"
        before = data_docs.render_source_readme("rp2005", rows["rp2005"])
        stray = base / "untracked.ASC"
        stray.write_text("not a published file\n", encoding="utf-8")
        self.addCleanup(stray.unlink)
        after = data_docs.render_source_readme("rp2005", rows["rp2005"])
        self.assertEqual(before, after)
        self.assertEqual(
            data_docs._tracked_count(
                "data/raw/print/rp2005/preformatted", "*.ASC"
            ),
            27,
        )

    def test_written_files_match_a_fresh_render(self):
        rows = manifests()
        expected = {
            "data/README.md": data_docs.render_data_readme(rows),
            "data/raw/README.md": data_docs.render_raw_readme(rows),
            "data/raw/print/README.md": data_docs.render_class_readme(
                "print", rows
            ),
            "data/raw/repo/README.md": data_docs.render_class_readme(
                "repo", rows
            ),
        }
        for edition_id in ("rp2005", "rp2018", "rp2005-2019", "rp2018-2023"):
            relative = f"{data_docs.SOURCE_READMES[edition_id]}/README.md"
            expected[relative] = data_docs.render_source_readme(
                edition_id, rows[edition_id]
            )
        for relative, text in expected.items():
            self.assertEqual(
                (ROOT / relative).read_text(encoding="utf-8"),
                generated.markdown(text),
                relative,
            )


if __name__ == "__main__":
    unittest.main()
