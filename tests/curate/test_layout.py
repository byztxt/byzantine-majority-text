"""Lock the repository layout: inputs under `data/`, outputs under `editions/`.

`SPECS/2026-11-21-input-and-code-layout/` moved the authoritative Beta-code
inputs to `data/text/` and folded `scripts/` into the `byz` package.
`SPECS/2026-11-25-inputs-out-of-editions/` removed the per-edition `source/`
snapshots: every input is now under `data/` and the manifest pins it. These
tests make the shape structural: the old directories cannot come back, the
entry points stay modules, the root README stays a render of its template, and
no tracked file tells a reader to use a path that no longer exists.
"""

import importlib
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from byz import generated
from byz.contract import contracts, history, paths
from byz.curate import build, docs

ROOT = Path(__file__).resolve().parents[2]

# Patterns for the older layout (the per-edition `source/` snapshots and the
# `scripts/` entry points). They are deliberately narrow: a lookbehind keeps
# `editions/<id>/source/CCAT` (the edition snapshot) out, and only a code span
# or a Markdown link to a *bare* `source/` counts. The entry-point pattern names
# the four removed `scripts/*.py` modules wherever a bare file name survives
# (for example an old command quoted without its `scripts/` prefix).
LEGACY_PATTERNS = (
    re.compile(r"(?<![\w./-])source/(CCAT|Strongs|README\.md)"),
    re.compile(r"`source/`"),
    re.compile(r"\]\(source/\)"),
    re.compile(r"\]\(\.\./source/\)"),
    re.compile(r"python3 scripts/"),
    re.compile(r"scripts/requirements\.txt"),
    re.compile(r"scripts/beta_to_unicode_custom"),
    re.compile(r"scripts/tei_xml_header\.xml"),
    re.compile(r"scripts/README\.md"),
    # No `scripts/` path can legitimately survive the move, so catch a bare
    # reference in prose or a code span as well as a relative Markdown link.
    re.compile(r"(?<![\w./-])scripts/"),
    re.compile(r"\]\(\.\./scripts/\)"),
    re.compile(
        r"(?<![\w./-])"
        r"(fetch_official|recover_editions|build_editions|diff_editions)\.py"
    ),
    # The per-edition input snapshots are gone; the only allowed references
    # render the retirement mapping or assert that they stay gone.
    re.compile(r"editions/[a-z0-9-]+/source/"),
)

# The 2026-11-25 input-class move retired these roots. The lookbehinds keep the
# new `print/` and `repo/` paths (`data/raw/print/rp2005/`,
# `data/raw/repo/rp2005-2019/`) out of the match.
INPUT_CLASS_PATTERNS = (
    re.compile(r"(?<![\w./-])data/text/"),
    re.compile(r"(?<!print/)data/raw/rp2005/"),
    re.compile(r"(?<!print/)data/raw/rp2018/"),
    re.compile(r"(?<!repo/)data/raw/rp2005-2019/"),
    re.compile(r"(?<!print/)data/raw/_archives/"),
)

# Every guard in this module sweeps both groups.
RETIRED_PATTERNS = LEGACY_PATTERNS + INPUT_CLASS_PATTERNS

# Files allowed to name the older layout. Each one either renders the
# authoritative old -> new mapping for a reader, holds the git selectors that
# keep pre-move history visible, or is this test's own needle list. The
# generated history documents and reports keep the label `v3.0.0 source/CCAT`
# because it names a path *inside* tag `v3.0.0`, not a working-tree path; that
# label is required to stay unchanged (validation.md section 6).
#
# Why each entry is here:
# - docs/EDITIONS.md: renders the authoritative mapping.
# - docs/HISTORY.md: keeps the historical tag labels.
# - docs/PROVENANCE.md: names paths inside the historical tags.
# - reports/reconciliation/{history.csv,summary.md}: the same tag labels.
# - src/byz/curate/docs.py: holds MOVED_PATHS / RETIRED_PATHS.
# - src/byz/contract/history.py: holds the git pathspecs.
# - src/byz/reconcile/historical.py, src/byz/reconcile/report.py: tag paths
#   and the generated archive prose.
# - tests/contract/test_integration.py: keeps the historical tag labels
#   `v3.0.0 source/CCAT`.
# - tests/curate/test_editions.py: asserts the retired tree is gone.
# - tests/curate/test_layout.py: this test's own needles.
LEGACY_ALLOWED = {
    "docs/EDITIONS.md",
    "docs/HISTORY.md",
    "docs/PROVENANCE.md",
    "reports/reconciliation/history.csv",
    "reports/reconciliation/summary.md",
    "src/byz/contract/history.py",
    "src/byz/curate/docs.py",
    "src/byz/reconcile/historical.py",
    "src/byz/reconcile/report.py",
    "tests/contract/test_integration.py",
    "tests/curate/test_editions.py",
    "tests/curate/test_layout.py",
}

# Files allowed to name a retired *input root*. This list is deliberately
# narrower than `LEGACY_ALLOWED`: a file that must keep a historical
# `source/CCAT` tag label is not thereby allowed to name `data/text/`, so the
# new-root guard keeps its teeth. The only legitimate names are the mapping
# constants, the git selectors that keep pre-move history visible, and the
# guard/absence assertions.
INPUT_CLASS_ALLOWED = {
    "docs/EDITIONS.md",
    "src/byz/contract/history.py",
    "src/byz/curate/docs.py",
    "tests/curate/test_editions.py",
    "tests/curate/test_layout.py",
}

# Only text files are scanned; the PDFs and the committed ZIP archives are
# binary data and are covered by their own hash tests.
TEXT_SUFFIXES = (
    ".py",
    ".md",
    ".txt",
    ".json",
    ".toml",
    ".csv",
    ".xml",
    ".yml",
    ".yaml",
    ".cfg",
    ".ini",
)
TEXT_NAMES = (".gitignore",)


def tracked_files():
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z"],
        capture_output=True,
        check=True,
    )
    return [
        name.decode("utf-8", "surrogateescape")
        for name in result.stdout.split(b"\0")
        if name
    ]


class InputTreeTests(unittest.TestCase):
    def test_input_tree_has_the_two_classes(self):
        self.assertTrue((ROOT / "data" / "raw" / "print").is_dir())
        self.assertTrue((ROOT / "data" / "raw" / "repo").is_dir())
        self.assertFalse((ROOT / "data" / "text").exists())
        self.assertFalse((ROOT / "source").exists())
        repo = ROOT / "data" / "raw" / "repo" / "rp2018-2023"
        self.assertEqual(len(list((repo / "ccat").glob("*.TXT"))), 29)
        self.assertEqual(len(list((repo / "strongs").glob("*.BP5"))), 27)
        self.assertTrue(
            (
                ROOT / "data" / "raw" / "repo" / "CONVENTIONS.md"
            ).is_file()
        )

    def test_print_trees_are_under_the_print_class(self):
        counts = {"rp2005": (29, 27, 27), "rp2018": (30, 27, 27)}
        for edition_id, (ccat, ascii_count, preformatted) in counts.items():
            base = ROOT / "data" / "raw" / "print" / edition_id
            self.assertEqual(len(list((base / "ccat").glob("*.CCT"))), ccat)
            self.assertEqual(
                len(list((base / "ascii").glob("*_Byz.txt"))), ascii_count
            )
            self.assertEqual(
                len(list((base / "preformatted").glob("*.ASC"))), preformatted
            )
            self.assertEqual(
                len(list((base / "official-pdf").glob("*.pdf"))), 1
            )

    def test_contract_uses_the_repo_dataset_names(self):
        self.assertEqual(
            paths.CCAT_DATASET, "data/raw/repo/rp2018-2023/ccat"
        )
        self.assertEqual(
            paths.BP5_DATASET, "data/raw/repo/rp2018-2023/strongs"
        )
        self.assertEqual(
            paths.CCAT_DIR,
            ROOT / "data" / "raw" / "repo" / "rp2018-2023" / "ccat",
        )
        self.assertEqual(
            paths.BP5_DIR,
            ROOT / "data" / "raw" / "repo" / "rp2018-2023" / "strongs",
        )
        self.assertEqual(
            set(contracts.DATASET_CONTRACTS)
            & {"data/raw/repo/rp2018-2023/ccat",
               "data/raw/repo/rp2018-2023/strongs"},
            {"data/raw/repo/rp2018-2023/ccat",
             "data/raw/repo/rp2018-2023/strongs"},
        )

    def test_editions_register_their_input_class(self):
        from byz.curate import editions

        expected = {
            "rp2005": "print",
            "rp2018": "print",
            "rp2005-2019": "repo",
            "rp2018-2023": "repo",
        }
        for edition_id, kind in expected.items():
            edition = editions.EDITIONS[edition_id]
            self.assertEqual(edition["input_class"], kind)
            self.assertTrue(
                edition["source_dir"].startswith(f"data/raw/{kind}/"),
                edition_id,
            )
        self.assertEqual(
            editions.EDITIONS["rp2018-2023"]["revision"], "2023-07-20"
        )

    def test_history_keeps_the_pre_move_evidence(self):
        labels = dict(history.DATASETS)
        self.assertIn(paths.CCAT_DATASET, labels)
        self.assertIn("source/CCAT", labels[paths.CCAT_DATASET])
        self.assertIn("data/text/CCAT", labels[paths.CCAT_DATASET])
        self.assertIn(
            "data/raw/repo/rp2018-2023/ccat", labels[paths.CCAT_DATASET]
        )
        self.assertIn(paths.BP5_DATASET, labels)

    def test_retired_input_roots_do_not_exist(self):
        for retired in (
            "data/text",
            "data/raw/rp2005",
            "data/raw/rp2018",
            "data/raw/rp2005-2019",
            "data/raw/_archives",
        ):
            self.assertFalse((ROOT / retired).exists(), retired)

    def test_no_tracked_file_under_a_retired_input_root(self):
        result = subprocess.run(
            [
                "git",
                "-C",
                str(ROOT),
                "ls-files",
                "data/text",
                "data/raw/rp2005",
                "data/raw/rp2018",
                "data/raw/rp2005-2019",
                "data/raw/_archives",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(result.stdout.strip(), "")

    def test_current_edition_readme_names_the_repository_input_tree(self):
        # The edition is outputs only; its README points at `data/` and the
        # manifest that pins the inputs.
        text = (ROOT / "editions" / "rp2018-2023" / "README.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("data/", text)
        self.assertIn("manifest.json", text)
        self.assertNotIn("repository `source/`", text)

    def test_editions_contain_only_outputs(self):
        for edition_dir in sorted((ROOT / "editions").iterdir()):
            if not edition_dir.is_dir():
                continue
            self.assertEqual(
                sorted(path.name for path in edition_dir.iterdir()),
                ["README.md", "csv", "manifest.json", "tei"],
                edition_dir.name,
            )
            self.assertFalse((edition_dir / "source").exists())

    def test_no_tracked_file_under_an_edition_source(self):
        result = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "editions/*/source/*"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(result.stdout.strip(), "")

    def test_no_manifest_input_root_points_under_editions(self):
        import json

        for manifest_path in sorted((ROOT / "editions").glob("*/manifest.json")):
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            for group in manifest["inputs"]:
                self.assertFalse(
                    group["root"].startswith("editions/"),
                    (manifest_path.name, group["root"]),
                )
                self.assertTrue(
                    group["root"].startswith("data/"),
                    (manifest_path.name, group["root"]),
                )


class EntryPointTests(unittest.TestCase):
    def test_scripts_directory_is_gone(self):
        self.assertFalse((ROOT / "scripts").exists())
        result = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "scripts"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(result.stdout.strip(), "")

    def test_entry_points_are_modules_with_main(self):
        for name in ("fetch", "materialise", "build", "diff", "verify"):
            module = importlib.import_module(f"byz.{name}")
            self.assertTrue(callable(module.main), name)

    def test_recover_entry_point_is_gone(self):
        self.assertFalse((ROOT / "src" / "byz" / "recover.py").exists())

    def test_root_files_moved(self):
        self.assertTrue((ROOT / "requirements.txt").is_file())
        self.assertFalse((ROOT / "scripts" / "requirements.txt").exists())
        self.assertTrue((ROOT / "docs" / "BUILD.md").is_file())
        self.assertFalse((ROOT / "scripts" / "README.md").exists())

    def test_requirements_pin_only_the_converter_dependency(self):
        text = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        self.assertEqual(
            [line for line in text.splitlines() if line.strip()],
            ["beta-code==1.0.0"],
        )

    def test_tei_header_is_package_data(self):
        self.assertTrue(
            (ROOT / "src" / "byz" / "curate" / "tei_xml_header.xml").is_file()
        )
        # Build a book and check the output carries the package header, rather
        # than asserting how `build.py` spells the path to it.
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "MAT.xml"
            build.write_tei(path, [("MAT", "B01", {(1, 1): "βιβλος"})])
            built = path.read_text(encoding="utf-8")
        self.assertIn("<teiHeader>", built)
        self.assertIn("Maurice A. Robinson and William Pierpont", built)
        self.assertNotIn("BOOK_METADATA_PLACEHOLDER", built)

    def test_no_module_manipulates_sys_path(self):
        # A structural layout rule (R2.3), so it lives with the other layout
        # gates rather than in the converter tests it was duplicated in.
        for path in sorted((ROOT / "src").rglob("*.py")):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("sys.path", text, str(path))

    def test_generated_by_names_an_existing_entry_point(self):
        # R6.5: the manifest's `generated_by` must not name a command that does
        # not exist.
        import json

        for manifest_path in sorted((ROOT / "editions").glob("*/manifest.json")):
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(
                manifest["generated_by"], "PYTHONPATH=src python3 -m byz.build"
            )
        self.assertTrue((ROOT / "src" / "byz" / "build.py").is_file())


class ReadmeTemplateTests(unittest.TestCase):
    def setUp(self):
        self.template_path = ROOT / "src" / "byz" / "curate" / "README.template.md"
        self.template = self.template_path.read_text(encoding="utf-8")

    def test_template_is_hand_maintained_and_banner_free(self):
        self.assertIn(
            "src/byz/curate/README.template.md", generated.HAND_MAINTAINED
        )
        self.assertNotIn("README.md", generated.HAND_MAINTAINED)
        self.assertFalse(self.template.startswith(generated.MARKDOWN_MARKER))

    def test_template_starts_with_the_edit_note(self):
        self.assertEqual(
            self.template.splitlines()[0], docs.TEMPLATE_NOTE
        )

    def test_template_tokens_are_known_and_used_once(self):
        tokens = re.findall(r"\{\{([A-Z_]+)\}\}", self.template)
        self.assertEqual(sorted(tokens), ["CURATED_EDITIONS", "GENERATED_FILES"])
        self.assertEqual(sorted(docs.TEMPLATE_TOKENS), sorted(tokens))

    def test_template_declares_its_two_machine_sections(self):
        self.assertIn("{{CURATED_EDITIONS}}", self.template.splitlines())
        self.assertIn("{{GENERATED_FILES}}", self.template.splitlines())


class TechTests(unittest.TestCase):
    def test_tech_md_describes_the_current_layout(self):
        text = (ROOT / "SPECS" / "TECH.md").read_text(encoding="utf-8")
        for needle in (
            "data/raw/repo/",
            "data/raw/print/",
            "data/raw/repo/CONVENTIONS.md",
            "byz.verify",
            "python -m byz.",
            "requirements.txt",
        ):
            self.assertIn(needle, text)
        self.assertNotIn("data/text", text)
        self.assertNotIn("scripts/", text)
        self.assertNotIn("source/CCAT", text)
        self.assertNotIn("editions/<edition>/source", text)


class ConventionsDocumentTests(unittest.TestCase):
    def test_conventions_document_is_hand_maintained(self):
        path = ROOT / "data" / "raw" / "repo" / "CONVENTIONS.md"
        self.assertTrue(path.is_file())
        self.assertFalse((ROOT / "data" / "text" / "README.md").exists())
        text = path.read_text(encoding="utf-8")
        self.assertFalse(text.startswith(generated.MARKDOWN_MARKER))
        self.assertIn("data/raw/repo/CONVENTIONS.md", generated.HAND_MAINTAINED)
        self.assertIn(
            "data/raw/repo/CONVENTIONS.md", generated.HAND_MAINTAINED_DOCS
        )
        for pattern in generated.GENERATED_FILES:
            for needle in pattern["patterns"]:
                self.assertNotEqual(
                    needle, "data/raw/repo/CONVENTIONS.md"
                )

    def test_preamble_scopes_the_document_to_the_repo_class(self):
        text = (
            ROOT / "data" / "raw" / "repo" / "CONVENTIONS.md"
        ).read_text(encoding="utf-8")
        preamble = text[: text.index("## Variant codes")]
        for needle in (
            "rp2018-2023/",
            "rp2005-2019/",
            "data/raw/print/",
            "not asserted",
            "src/byz/beta/converter.py",
            "../README.md",
            "../../../docs/EDITIONS.md",
        ):
            self.assertIn(needle, preamble)

    def test_robinson_prose_is_intact(self):
        text = (
            ROOT / "data" / "raw" / "repo" / "CONVENTIONS.md"
        ).read_text(encoding="utf-8")
        for needle in (
            "* `N`: Nestle-Aland variant.",
            "* `B`: Byzantine variant.",
            "* `C`: NA27/28 variant.",
            "* `M`: ECM (*Editio Critica Maior*) variant.",
            "* `S`: NA27 variant.",
            "* `E`: NA28 variant.",
            "| Present           | P            |",
            "| Indicative  | I            |",
            "For example, in James 4:5 the text reads:",
            "it is ASSUMED that all Strong's numbers are correct",
            "The Analytical Greek Lexicon",
        ):
            self.assertIn(needle, text)

    def test_conventions_relative_links_resolve(self):
        path = ROOT / "data" / "raw" / "repo" / "CONVENTIONS.md"
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)#]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            self.assertTrue((path.parent / target).exists(), target)


class RetiredLayoutSweepTests(unittest.TestCase):
    def test_no_tracked_file_names_the_removed_layout(self):
        # Each pattern group has its own allowlist, so a file exempted from
        # the older `source/…` guard is still checked against the 2026-11-25
        # retired input roots.
        groups = (
            (LEGACY_PATTERNS, LEGACY_ALLOWED),
            (INPUT_CLASS_PATTERNS, INPUT_CLASS_ALLOWED),
        )
        offenders = []
        for rel in tracked_files():
            if rel.startswith(("SPECS/", "editions/")):
                continue
            if not rel.endswith(TEXT_SUFFIXES) and rel not in TEXT_NAMES:
                continue
            # A file deleted in the working tree but still in the index (until
            # the next commit) cannot contain a live reference.
            if not (ROOT / rel).is_file():
                continue
            text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
            hit = None
            for patterns, allowed in groups:
                if rel in allowed:
                    continue
                for pattern in patterns:
                    match = pattern.search(text)
                    if match:
                        hit = match.group(0)
                        break
                if hit:
                    break
            if hit:
                offenders.append(f"{rel}: {hit!r}")
        self.assertEqual(offenders, [])

    def test_specs_tech_md_has_no_retired_reference(self):
        text = (ROOT / "SPECS" / "TECH.md").read_text(encoding="utf-8")
        for pattern in RETIRED_PATTERNS:
            self.assertIsNone(pattern.search(text), pattern.pattern)


class ReleaseNotesRemovalTests(unittest.TestCase):
    """Release history now lives in GitHub releases, not a docs page.

    The hand-maintained page was deleted because every fact a reader needs is
    in `docs/EDITIONS.md` or the release itself. These guards make a
    half-removal fail: the page cannot reappear, and no tracked file may still
    point at it.
    """

    # Split so this test file does not trip its own sweep.
    NEEDLE = "RELEASE" + "-NOTES"

    def test_release_notes_page_is_gone(self):
        self.assertFalse(
            (ROOT / "docs" / (self.NEEDLE + ".md")).exists()
        )

    def test_no_tracked_file_references_the_release_notes_page(self):
        offenders = []
        for rel in tracked_files():
            if rel.startswith("SPECS/"):
                continue
            if not rel.endswith(TEXT_SUFFIXES) and rel not in TEXT_NAMES:
                continue
            # A file deleted in the working tree but still in the index (until
            # the next commit) cannot contain a live reference.
            if not (ROOT / rel).is_file():
                continue
            text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
            if self.NEEDLE in text:
                offenders.append(rel)
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
