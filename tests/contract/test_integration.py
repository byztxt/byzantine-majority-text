import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from byz import generated
from byz.contract import (
    contracts,
    coverage,
    derivation,
    invariants,
    model,
    paths,
    report,
)


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
                paths.dataset_name("csv/accented/no-variants"),
                paths.dataset_name("csv/accented/with-variants"),
                paths.dataset_name("csv/strongs/no-parsing"),
                paths.dataset_name("csv/strongs/with-parsing"),
                paths.TEI_DATASET,
                paths.TEI_BYZ_DATASET,
            },
        )

    def test_dataset_names_live_in_the_current_edition(self):
        for dataset in self.results:
            if dataset.startswith("source/"):
                continue
            self.assertTrue(
                dataset.startswith(f"{paths.CURRENT_PREFIX}/")
                or dataset == paths.ASSETS_DATASET,
                dataset,
            )

    def test_contract_json_matches_the_dataset_names(self):
        directory = paths.CONTRACT_DIR
        expected = {"contracts.json"} | {
            f"{name.replace('/', '__')}.json" for name in contracts.DATASET_CONTRACTS
        }
        self.assertEqual({path.name for path in directory.glob("*.json")}, expected)

    def test_source_file_counts(self):
        self.assertEqual(len(self.results["source/CCAT"]), 29)
        self.assertEqual(len(self.results["source/Strongs"]), 27)
        self.assertEqual(
            len(self.results[paths.dataset_name("csv/accented/no-variants")]), 29
        )
        self.assertEqual(
            len(self.results[paths.dataset_name("csv/strongs/no-parsing")]), 27
        )
        self.assertEqual(len(self.results[paths.TEI_DATASET]), 27)

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
                paths.dataset_name("csv/strongs/no-parsing"),
                paths.TEI_DATASET,
            ):
                self.assertIsNotNone(
                    self._record(dataset, book, chapter, verse),
                    f"{dataset} is missing {book} {chapter}:{verse}",
                )
            csv_record = self._record(
                paths.dataset_name("csv/strongs/no-parsing"), book, chapter, verse
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
        self.assertEqual(text.count(generated.MARKDOWN_MARKER), 1)
        self.assertTrue(text.startswith(generated.MARKDOWN_MARKER + "\n"))
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


BASELINE_HEADERS = {
    "files.csv": (
        "dataset,path,size,sha256,lines,encoding,eol,format_class,"
        "git_blob,last_commit"
    ),
    "books.csv": (
        "dataset,book,file,chapters,verses,min_chapter,max_chapter,"
        "min_verse,max_verse,blank"
    ),
    "differences.csv": (
        "comparison,left,right,book,left_verses,right_verses,only_left,"
        "only_right,examples_only_left,examples_only_right"
    ),
    "derivations.csv": "source,derived,evidence,status",
    "invariants.csv": ",".join(model.VIOLATION_FIELDS),
}

# The declared field tuples that `report.write_all` passes to `write_csv`; the
# five tests below prove each one matches the committed header.
HEADER_FIELDS = {
    "files.csv": model.FILE_FIELDS,
    "books.csv": coverage.BOOK_FIELDS,
    "differences.csv": coverage.DIFFERENCE_FIELDS,
    "derivations.csv": derivation.DERIVATION_FIELDS,
    "invariants.csv": model.VIOLATION_FIELDS,
}


class BaselineCsvTests(unittest.TestCase):
    """R5: every baseline CSV declares its columns, even when it has no rows."""

    def setUp(self):
        self.reports = ROOT / "reports" / "baseline"

    def test_every_baseline_csv_has_a_header(self):
        for name, header in BASELINE_HEADERS.items():
            path = self.reports / name
            self.assertTrue(path.is_file(), name)
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text, f"{name} is empty")
            self.assertEqual(text.splitlines()[0], header, name)

    def test_every_header_uses_its_declared_fields(self):
        for name, fields in HEADER_FIELDS.items():
            self.assertEqual(BASELINE_HEADERS[name], ",".join(fields), name)

    def test_every_baseline_csv_writes_a_header_with_no_rows(self):
        # The "header is always written" rule must not depend on which CSV has
        # data today. `fields` is the mechanism; this proves it for all five.
        for name, fields in HEADER_FIELDS.items():
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / name
                report.write_csv(path, [], fields=fields)
                self.assertEqual(
                    path.read_text(encoding="utf-8"),
                    ",".join(fields) + "\n",
                    name,
                )

    def test_invariants_csv_is_header_only_when_clean(self):
        path = self.reports / "invariants.csv"
        text = path.read_text(encoding="utf-8")
        self.assertEqual(text, ",".join(model.VIOLATION_FIELDS) + "\n")
        self.assertEqual(len(text.splitlines()), 1)

    def test_invariant_header_matches_the_row_schema(self):
        violation = model.Violation(
            dataset="d",
            path="p",
            line=1,
            category="c",
            message="m",
            key="k",
            known_exception="",
        )
        self.assertEqual(tuple(violation.as_row()), model.VIOLATION_FIELDS)

    def test_invariants_csv_keeps_the_header_when_it_has_rows(self):
        violation = model.Violation(
            dataset="d",
            path="p",
            line=1,
            category="c",
            message="m",
            key="k",
            known_exception="",
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "invariants.csv"
            report.write_csv(
                path,
                [violation.as_row()],
                fields=model.VIOLATION_FIELDS,
            )
            lines = path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[0], ",".join(model.VIOLATION_FIELDS))
        self.assertEqual(
            lines[1], ",".join(str(value) for value in violation.as_row().values())
        )


class DataContractDocTests(unittest.TestCase):
    """R5: the contract document explains itself without prior context."""

    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT / "docs" / "DATA_CONTRACT.md").read_text(
            encoding="utf-8"
        )

    def test_doc_explains_itself(self):
        for needle in (
            "How to read this document",
            "## Terms",
            "Dataset",
            "invariant",
            "derivation",
            "PYTHONPATH=src python3 -m byz.contract",
        ):
            self.assertIn(needle, self.text)

    def test_doc_documents_invariants_csv(self):
        self.assertIn("reports/baseline/invariants.csv", self.text)
        self.assertIn(",".join(model.VIOLATION_FIELDS), self.text)
        self.assertIn("no data rows", self.text)

    def test_doc_documents_every_baseline_csv(self):
        for name in BASELINE_HEADERS:
            self.assertIn(f"reports/baseline/{name}", self.text, name)

    def test_doc_has_no_stale_cycle_sentence(self):
        self.assertNotIn("that is the next cycle", self.text)
        self.assertIn("docs/PROVENANCE.md", self.text)
        self.assertIn("Cycle 2", self.text)

    def test_doc_has_no_known_exception_placeholder(self):
        # A clean run renders a table with no data rows; a fake `-` row would
        # contradict "an empty table means none".
        self.assertNotIn("| - | - | None |", self.text)
        self.assertIn("KNOWN_EXCEPTIONS", self.text)
        self.assertIn("src/byz/contract/invariants.py", self.text)

    def test_doc_qualifies_the_coverage_row_count(self):
        prose = re.sub(r"\s+", " ", self.text)
        self.assertIn("one row per validated corpus dataset", prose)
        self.assertIn("asset files appear only", prose)

    def test_doc_names_the_official_unaccented_source(self):
        self.assertIn("data/raw/<edition>/", self.text)
        self.assertIn("unaccented CSV and TEI", self.text)

    def test_coverage_table_describes_each_dataset(self):
        section = self.text.split("## Coverage", 1)[1].split("## ", 1)[0]
        coverage_rows = {
            line.split("|")[1].strip().strip("`"): line
            for line in section.splitlines()
            if line.startswith("| `")
        }
        for dataset, contract in contracts.DATASET_CONTRACTS.items():
            self.assertIn(dataset, coverage_rows, dataset)
            self.assertIn(contract["purpose"], coverage_rows[dataset], dataset)


if __name__ == "__main__":
    unittest.main()
