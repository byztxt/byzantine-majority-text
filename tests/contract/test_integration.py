import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from byz.contract import coverage, derivation, invariants


class IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = invariants.annotate_known_exceptions(
            invariants.validate_all()
        )

    def test_dataset_set(self):
        self.assertEqual(
            set(self.results),
            {
                "source/CCAT",
                "source/Strongs",
                "csv-unicode/ccat/no-variants",
                "csv-unicode/ccat/with-variants",
                "csv-unicode/strongs/no-parsing",
                "csv-unicode/strongs/with-parsing",
                "tei-xml-unicode/no-accents",
                "tei-xml-unicode/BYZ",
            },
        )

    def test_source_file_counts(self):
        self.assertEqual(len(self.results["source/CCAT"]), 29)
        self.assertEqual(len(self.results["source/Strongs"]), 27)
        self.assertEqual(len(self.results["csv-unicode/ccat/no-variants"]), 29)
        self.assertEqual(len(self.results["csv-unicode/strongs/no-parsing"]), 27)
        self.assertEqual(len(self.results["tei-xml-unicode/no-accents"]), 27)

    def _record(self, dataset, book, chapter, verse):
        for result in self.results[dataset]:
            for record in result.records:
                if (
                    record["book"] == book
                    and record["chapter"] == chapter
                    and record["verse"] == verse
                ):
                    return record
        return None

    def test_no_invariant_findings(self):
        findings = list(invariants.all_violations(self.results))
        self.assertEqual(findings, [])

    def test_derivation_has_no_missing_files(self):
        rows = derivation.check()
        self.assertTrue(rows)
        self.assertFalse([row for row in rows if row["status"] == "missing"])

    def test_no_coverage_differences(self):
        rows = coverage.diff_rows(self.results)
        self.assertFalse(
            [row for row in rows if row["only_left"] or row["only_right"]]
        )

    def test_intentional_blanks_are_present_as_empty_records(self):
        for book, chapter, verse in (
            ("LUK", 17, 36),
            ("ACT", 8, 37),
            ("ACT", 15, 34),
            ("ACT", 24, 7),
        ):
            for dataset in (
                "source/CCAT",
                "source/Strongs",
                "csv-unicode/strongs/no-parsing",
                "tei-xml-unicode/no-accents",
            ):
                self.assertIsNotNone(
                    self._record(dataset, book, chapter, verse),
                    f"{dataset} is missing {book} {chapter}:{verse}",
                )
            csv_record = self._record(
                "csv-unicode/strongs/no-parsing", book, chapter, verse
            )
            self.assertEqual(csv_record["text"], "")

    def test_tei_matches_csv_no_parsing_exactly(self):
        rows = coverage.diff_rows(self.results)
        tei_rows = [
            row for row in rows if row["comparison"] == "CSV no-parsing vs TEI"
        ]
        self.assertTrue(tei_rows)
        self.assertFalse(
            [row for row in tei_rows if row["only_left"] or row["only_right"]]
        )


ROOT = Path(__file__).resolve().parents[2]
SKIP_MESSAGE = (
    "`git worktree` is unavailable, so the hermetic contract checks cannot run; "
    "run them in a normal git clone with worktree support"
)


def _run(command, cwd, env=None):
    result = subprocess.run(
        command, cwd=str(cwd), env=env, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise AssertionError(
            f"{' '.join(command)} failed: {result.stderr[-2000:]}"
        )
    return result


def _make_worktree():
    parent = Path(tempfile.mkdtemp(prefix="byz-contract-"))
    target = parent / "wt"
    result = subprocess.run(
        ["git", "-C", str(ROOT), "worktree", "add", "--detach", str(target), "HEAD"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        shutil.rmtree(parent, ignore_errors=True)
        return None
    return target


def _remove_worktree(path):
    if path is None:
        return
    subprocess.run(
        ["git", "-C", str(ROOT), "worktree", "remove", "--force", str(path)],
        capture_output=True,
        text=True,
    )
    shutil.rmtree(path.parent, ignore_errors=True)
    # Prune after the directory is gone so a failed `worktree remove` cannot
    # leave stale worktree metadata behind.
    subprocess.run(
        ["git", "-C", str(ROOT), "worktree", "prune"],
        capture_output=True,
        text=True,
    )


def _contract(worktree):
    env = dict(os.environ)
    env["PYTHONPATH"] = str(worktree / "src")
    _run([sys.executable, "-m", "byz.contract"], cwd=worktree, env=env)


def _status(worktree):
    return _run(
        ["git", "-C", str(worktree), "status", "--porcelain"], cwd=worktree
    ).stdout.strip()


class ContractWorktreeTests(unittest.TestCase):
    """Reproducibility checks that never touch the developer's working tree."""

    STATS = {
        "rp2005": {"match": 7769, "verses": 7972},
        "rp2018": {"match": 7811, "verses": 7972},
    }
    ROWS = [
        {
            "state": "v2.0.3 textonly-beta-code",
            "compared_to": "rp2005",
            "match": 7918,
            "verses": 7972,
            "percent": "99.32%",
        },
        {
            "state": "v2.0.3 textonly-beta-code",
            "compared_to": "rp2018",
            "match": 7969,
            "verses": 7972,
            "percent": "99.96%",
        },
        {
            "state": "v3.0.0 source/CCAT",
            "compared_to": "rp2005",
            "match": 7754,
            "verses": 7957,
            "percent": "97.45%",
        },
        {
            "state": "v3.0.0 source/CCAT",
            "compared_to": "rp2018",
            "match": 7796,
            "verses": 7957,
            "percent": "97.98%",
        },
        {
            "state": "current source/CCAT",
            "compared_to": "rp2005",
            "match": 7769,
            "verses": 7972,
            "percent": "97.45%",
        },
        {
            "state": "current source/CCAT",
            "compared_to": "rp2018",
            "match": 7811,
            "verses": 7972,
            "percent": "97.98%",
        },
    ]

    @classmethod
    def setUpClass(cls):
        cls.worktree = _make_worktree()
        if cls.worktree is None:
            raise unittest.SkipTest(SKIP_MESSAGE)
        cls.history = cls.worktree / "docs" / "HISTORY.md"

    @classmethod
    def tearDownClass(cls):
        _remove_worktree(cls.worktree)

    def _assert_single_cycle2_block(self, text):
        self.assertEqual(text.count("## External archive evidence"), 1)
        self.assertEqual(text.count("<!-- cycle2:begin -->"), 1)
        self.assertEqual(text.count("<!-- cycle2:end -->"), 1)
        self.assertIn("v2016-07-28", text)

    def test_summary_documents_commit_column_lag(self):
        text = (
            self.worktree / "reports" / "baseline" / "summary.md"
        ).read_text(encoding="utf-8")
        self.assertIn("`files.csv` records", text)
        self.assertIn("lags", text)

    def test_committed_contract_outputs_match_a_fresh_run(self):
        self.assertEqual(_status(self.worktree), "", "worktree is not clean")
        _contract(self.worktree)
        text = self.history.read_text(encoding="utf-8")
        self._assert_single_cycle2_block(text)
        self.assertEqual(
            _status(self.worktree),
            "",
            "a fresh `byz.contract` run differs from the committed HEAD",
        )

    def test_contract_is_idempotent_and_preserves_cycle2_block(self):
        _contract(self.worktree)
        first = self.history.read_text(encoding="utf-8")
        _contract(self.worktree)
        second = self.history.read_text(encoding="utf-8")
        self.assertEqual(second, first)
        self._assert_single_cycle2_block(second)

    def test_update_history_is_idempotent(self):
        _contract(self.worktree)
        before = self.history.read_text(encoding="utf-8")
        code = (
            "from byz.reconcile import report\n"
            f"stats = {self.STATS!r}\n"
            f"rows = {self.ROWS!r}\n"
            "report._update_history(stats, 'rp2018', rows)\n"
        )
        env = dict(os.environ)
        env["PYTHONPATH"] = str(self.worktree / "src")
        for _ in range(2):
            _run([sys.executable, "-c", code], cwd=self.worktree, env=env)
            current = self.history.read_text(encoding="utf-8")
            self.assertEqual(current, before)
            self._assert_single_cycle2_block(current)
        self.assertEqual(
            _status(self.worktree),
            "",
            "re-running the reconciliation history update changed the tree",
        )


if __name__ == "__main__":
    unittest.main()
