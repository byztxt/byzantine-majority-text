import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from byz.contract import inventory


class TrackedOnlyInventoryTests(unittest.TestCase):
    """The inventory describes the committed corpus, never a local draft."""

    def test_untracked_file_is_not_yielded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            essay = root / "essay"
            essay.mkdir()
            (essay / "tracked.md").write_text("tracked\n", encoding="utf-8")
            (essay / "stray.docx").write_text("stray\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(root), "init", "-q"], check=True
            )
            subprocess.run(
                ["git", "-C", str(root), "add", "essay/tracked.md"], check=True
            )

            paths = {
                path.relative_to(root).as_posix()
                for _, path, _ in inventory.iter_specs(root)
            }

            self.assertIn("essay/tracked.md", paths)
            self.assertNotIn("essay/stray.docx", paths)

    def test_tracked_paths_are_repository_relative(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "essay").mkdir()
            (root / "essay" / "tracked.md").write_text("tracked\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(root), "init", "-q"], check=True
            )
            subprocess.run(
                ["git", "-C", str(root), "add", "essay/tracked.md"], check=True
            )

            self.assertEqual(
                inventory.tracked_paths(root), {"essay/tracked.md"}
            )

    def test_untracked_doc_is_not_yielded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("tracked\n", encoding="utf-8")
            (root / "LICENSE").write_text("local copy\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(root), "init", "-q"], check=True
            )
            subprocess.run(
                ["git", "-C", str(root), "add", "README.md"], check=True
            )

            docs = {
                path.name for _, path, _ in inventory.iter_docs(root)
            }

            self.assertEqual(docs, {"README.md"})

    def test_missing_git_binary_raises_runtime_error(self):
        # A git-less environment must fail with the documented RuntimeError,
        # not a bare FileNotFoundError from subprocess.
        with mock.patch(
            "byz.contract.inventory.subprocess.run",
            side_effect=FileNotFoundError("git"),
        ):
            with self.assertRaises(RuntimeError):
                inventory.tracked_paths(Path("/tmp"))


if __name__ == "__main__":
    unittest.main()
