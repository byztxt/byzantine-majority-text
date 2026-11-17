"""Offline reconciliation checks: pinned hashes, committed archives, reports.

The six original zips are committed under `data/raw/_archives/`, so these tests
run in a normal checkout and need no network access or extra fetch step.
"""

import shutil
import subprocess
import unittest
from pathlib import Path

from byz.reconcile import fetch, sources

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "reports" / "reconciliation"
DIFFS = ROOT / "reports" / "diffs"

EXPECTED_DIFF_COUNTS = {
    "rp2005--rp2005-2019": 54,
    "rp2005-2019--rp2018": 3,
    "rp2018--rp2018-2023": 161,
    "rp2005--rp2018": 55,
}


def _provenance_hashes(edition):
    path = sources.PROVENANCE_DIR / f"{edition}.toml"
    hashes = {}
    name = None
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line == "[[archives]]":
            name = None
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"')
        if key == "name":
            name = value
        elif key == "sha256" and name:
            hashes[name] = value
    return hashes


class PinnedArchiveHashTests(unittest.TestCase):
    def test_six_archives_are_pinned(self):
        self.assertEqual(len(sources.ARCHIVES), 6)
        self.assertEqual(
            {spec["edition"] for spec in sources.ARCHIVES}, {"rp2005", "rp2018"}
        )

    def test_pinned_hashes_match_provenance(self):
        for edition in ("rp2005", "rp2018"):
            provenance = _provenance_hashes(edition)
            specs = [
                spec for spec in sources.ARCHIVES if spec["edition"] == edition
            ]
            self.assertEqual(len(specs), 3)
            for spec in specs:
                self.assertIn(spec["name"], provenance)
                self.assertEqual(
                    spec["sha256"],
                    provenance[spec["name"]],
                    f"{edition}/{spec['name']}",
                )

    def test_pinned_hashes_are_sha256(self):
        for spec in sources.ARCHIVES:
            self.assertEqual(len(spec["sha256"]), 64, spec["name"])
            int(spec["sha256"], 16)

    def test_archive_urls_are_https(self):
        for spec in sources.ARCHIVES:
            self.assertTrue(spec["url"].startswith("https://"), spec["name"])


class CommittedArchiveTests(unittest.TestCase):
    """The six official zips are committed, pinned, and not git-ignored."""

    def test_six_archives_are_committed_with_pinned_hashes(self):
        for spec in sources.ARCHIVES:
            path = sources.ARCHIVE_DIR / spec["edition"] / spec["name"]
            self.assertTrue(path.is_file(), f"missing committed archive: {path}")
            self.assertEqual(fetch.sha256_file(path), spec["sha256"], str(path))

    @unittest.skipIf(shutil.which("git") is None, "git is not installed")
    def test_committed_archives_are_not_gitignored(self):
        for spec in sources.ARCHIVES:
            path = sources.ARCHIVE_DIR / spec["edition"] / spec["name"]
            result = subprocess.run(
                ["git", "check-ignore", "--quiet", str(path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                result.returncode, 1, f"committed archive is git-ignored: {path}"
            )


class CommittedReportTests(unittest.TestCase):
    def test_reconciliation_reports_exist(self):
        for name in (
            "summary.md",
            "files.csv",
            "verses.csv",
            "categories.csv",
            "history.csv",
            "archives.csv",
            "decision-log.md",
        ):
            self.assertTrue((REPORTS / name).is_file(), name)

    def test_headline_totals_are_stable(self):
        summary = (REPORTS / "summary.md").read_text(encoding="utf-8")
        self.assertIn("7769/7972", summary)
        self.assertIn("7811/7972", summary)

    def test_history_lineage_totals_are_stable(self):
        text = (REPORTS / "history.csv").read_text(encoding="utf-8")
        self.assertIn("7918", text)
        self.assertIn("7969", text)
        self.assertIn("7754", text)
        self.assertIn("7796", text)

    def test_successive_diff_counts_are_stable(self):
        for name, count in EXPECTED_DIFF_COUNTS.items():
            report = (DIFFS / name / "report.md").read_text(encoding="utf-8")
            self.assertIn(f"**Differing verses:** {count}", report, name)


if __name__ == "__main__":
    unittest.main()
