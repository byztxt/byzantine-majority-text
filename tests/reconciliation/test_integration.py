import unittest
from unittest import mock

from byz.reconcile import compare, fetch, historical, report, sources


def _archive_path(spec):
    return sources.ARCHIVE_DIR / spec["edition"] / spec["name"]


def _archive_ok(spec):
    """True when the committed archive exists and matches its pinned digest."""
    path = _archive_path(spec)
    if not path.is_file():
        return False
    return fetch.sha256_file(path) == spec["sha256"]


ARCHIVES_PRESENT = all(_archive_ok(spec) for spec in sources.ARCHIVES)

MISSING_MESSAGE = (
    "the official archives committed under data/raw/print/_archives are missing or "
    "corrupt: restore them with `git checkout -- data/raw/print/_archives`, or run "
    "`PYTHONPATH=src python3 -m byz.fetch --force` to re-download. These checks "
    "also need the pinned Python 3.10 environment."
)


@unittest.skipUnless(ARCHIVES_PRESENT, MISSING_MESSAGE)
class IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = compare.run()

    def test_2018_is_closer_than_2005(self):
        source = {
            row["edition"]: row
            for row in self.results["files"]
            if row["tier"] == "source"
            and row["current"] == "data/raw/repo/rp2018-2023/ccat/01_MAT.TXT"
        }
        self.assertIn("rp2005", source)
        self.assertIn("rp2018", source)

    def test_source_rows_present(self):
        source = [row for row in self.results["files"] if row["tier"] == "source"]
        self.assertEqual(len(source), 58)

    def test_every_verse_category_has_a_documented_meaning(self):
        for row in self.results["verses"]:
            if row["category"]:
                self.assertIn(row["category"], compare.CATEGORY_MEANINGS)

    def test_summary_and_decision_log_name_both_apparatus_categories(self):
        results = self.results
        source_stats = report._source_stats(results["files"])
        derived_stats = report._derived_stats(results["files"])
        history_rows = historical.evidence()
        categories = report._categories(results["verses"])
        summary = report._summary(
            results, source_stats, derived_stats, categories, history_rows
        )
        self.assertIn("reading changes", summary)
        self.assertIn("code-only changes", summary)
        self.assertIn("../diffs/README.md#categories", summary)
        self.assertNotIn("variant-code", summary)
        decision_log = report._decision_log(results)
        row = next(
            line
            for line in decision_log.splitlines()
            if line.startswith("| R2 |")
        )
        self.assertIn("category `apparatus-code`", row)
        self.assertIn("the tag differs, the reading does not", row)
        self.assertNotIn("variant-code", row)
        self.assertTrue(row.rstrip().endswith("| pending |"))

    def test_strongs_provenance_is_official_source(self):
        # R7: `data/raw/repo/rp2018-2023/strongs/*.BP5` are Dr Robinson's official parsed files.
        # The only gap is the delivery route: no published ZIP contains one.
        strongs = self.results["strongs"]
        self.assertEqual(strongs["status"], "official-source-files")
        self.assertEqual(
            strongs["delivery"],
            "recorded" if strongs["hits"] else "not-recorded",
        )

    def test_strongs_delivery_follows_the_hits(self):
        # The delivery status is derived from the scan, not hardcoded: if an
        # archive ever carries a parsed file, the report must stop saying the
        # route is unrecorded.
        with mock.patch.object(
            compare.archive, "load_members", return_value=["PARSED.BP5"]
        ):
            strongs = compare.strongs_provenance()
        self.assertTrue(strongs["hits"])
        self.assertEqual(strongs["delivery"], "recorded")

    def test_strongs_report_prose_follows_the_hits(self):
        # The same simulated hit must remove the "None of the six ..." wording
        # from every generated document, not just change the status field.
        results = dict(self.results)
        results["strongs"] = {
            "status": "official-source-files",
            "delivery": "recorded",
            "hits": ["rp2005/PARSED.BP5"],
        }
        source_stats = report._source_stats(results["files"])
        derived_stats = report._derived_stats(results["files"])
        history_rows = historical.evidence()
        provenance = report._provenance_doc(
            results, source_stats, derived_stats, history_rows
        )
        summary = report._summary(
            results, source_stats, derived_stats, [], history_rows
        )
        decision_log = report._decision_log(results)
        for text in (provenance, summary, decision_log):
            self.assertNotIn("None of the six", text)
            self.assertIn("delivery route is recorded", text)
            self.assertIn("PARSED.BP5", text)
        self.assertIn("resolved (2026-11-19)", decision_log)

    def test_strongs_rows_are_not_unknown(self):
        rows = [
            row
            for row in self.results["files"]
            if row["dataset"] == "data/raw/repo/rp2018-2023/strongs"
        ]
        self.assertEqual(len(rows), 27)
        for row in rows:
            self.assertEqual(row["class"], "official-source", row["current"])
            self.assertIn("Dr Robinson", row["note"])
            self.assertNotIn("unknown", row["class"])

    def test_intentional_blanks_confirmed(self):
        blanks = self.results["blanks"]
        self.assertEqual(len(blanks), 8)
        self.assertTrue(all(row["in_official_ccat"] for row in blanks))
        self.assertTrue(all(row["official_blank"] for row in blanks))

    def test_mapping_classes_present(self):
        classes = {row["class"] for row in self.results["files"]}
        self.assertIn("official-source", classes)
        self.assertIn("incomparable-pending-pipeline", classes)
        self.assertIn("auxiliary", classes)
        self.assertNotIn("provenance-unknown", classes)

    def test_history_lineage(self):
        rows = {
            (row["state"], row["compared_to"]): row
            for row in historical.evidence()
        }
        v203_05 = rows[("v2.0.3 textonly-beta-code", "rp2005")]
        v203_18 = rows[("v2.0.3 textonly-beta-code", "rp2018")]
        cur_05 = rows[("current data/raw/repo/rp2018-2023/ccat", "rp2005")]
        cur_18 = rows[("current data/raw/repo/rp2018-2023/ccat", "rp2018")]
        self.assertGreater(v203_18["match"], v203_05["match"])
        self.assertGreater(cur_18["match"], cur_05["match"])
        self.assertGreater(v203_18["match"], cur_18["match"])


if __name__ == "__main__":
    unittest.main()
