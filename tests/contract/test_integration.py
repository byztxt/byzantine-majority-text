import os
import subprocess
import sys
import unittest
from pathlib import Path

from byz.contract import coverage, derivation, invariants
from byz.reconcile import report


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


class HistoryReproducibilityTests(unittest.TestCase):
    ROOT = Path(__file__).resolve().parents[2]
    PATH = ROOT / "docs" / "HISTORY.md"

    def test_summary_documents_commit_column_lag(self):
        text = (self.ROOT / "reports" / "baseline" / "summary.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("`files.csv` records", text)
        self.assertIn("lags", text)

    def _run_contract(self):
        env = dict(os.environ)
        env["PYTHONPATH"] = str(self.ROOT / "src")
        result = subprocess.run(
            [sys.executable, "-m", "byz.contract"],
            cwd=str(self.ROOT),
            env=env,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr[-2000:])

    def test_contract_is_idempotent_and_preserves_cycle2_block(self):
        self._run_contract()
        before = self.PATH.read_text(encoding="utf-8")
        self.assertIn("<!-- cycle2:begin -->", before)
        self.assertIn("v2016-07-28", before)
        self._run_contract()
        after = self.PATH.read_text(encoding="utf-8")
        self.assertEqual(after, before)
        self.assertEqual(after.count("## External archive evidence"), 1)
        self.assertEqual(after.count("<!-- cycle2:begin -->"), 1)
        self.assertEqual(after.count("<!-- cycle2:end -->"), 1)


class ReconciliationHistoryTests(unittest.TestCase):
    """`contract` then `reconcile` must keep exactly one evidence block."""

    ROOT = Path(__file__).resolve().parents[2]
    PATH = ROOT / "docs" / "HISTORY.md"
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

    def setUp(self):
        env = dict(os.environ)
        env["PYTHONPATH"] = str(self.ROOT / "src")
        subprocess.run(
            [sys.executable, "-m", "byz.contract"],
            cwd=str(self.ROOT),
            env=env,
            capture_output=True,
            text=True,
            check=True,
        )

    def test_update_history_is_idempotent(self):
        before = self.PATH.read_text(encoding="utf-8")
        report._update_history(self.STATS, "rp2018", self.ROWS)
        once = self.PATH.read_text(encoding="utf-8")
        self.assertEqual(once, before)
        report._update_history(self.STATS, "rp2018", self.ROWS)
        twice = self.PATH.read_text(encoding="utf-8")
        self.assertEqual(twice, once)
        self.assertEqual(twice.count("## External archive evidence"), 1)
        self.assertEqual(twice.count("<!-- cycle2:begin -->"), 1)
        self.assertEqual(twice.count("<!-- cycle2:end -->"), 1)


if __name__ == "__main__":
    unittest.main()
