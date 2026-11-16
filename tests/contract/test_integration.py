import unittest

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

    def test_all_findings_are_known_exceptions(self):
        findings = list(invariants.all_violations(self.results))
        self.assertEqual(len(findings), 8)
        self.assertTrue(all(finding.known_exception for finding in findings))

    def test_derivation_has_no_missing_files(self):
        rows = derivation.check()
        self.assertTrue(rows)
        self.assertFalse([row for row in rows if row["status"] == "missing"])

    def test_only_blank_verses_differ_between_source_and_csv(self):
        rows = coverage.diff_rows(self.results)
        nonzero = [
            row for row in rows if row["only_left"] or row["only_right"]
        ]
        self.assertEqual(len(nonzero), 8)
        self.assertTrue(all(row["only_right"] == 0 for row in nonzero))
        self.assertEqual(
            {row["examples_only_left"] for row in nonzero},
            {"8:37 15:34 24:7", "17:36"},
        )

    def test_tei_matches_csv_no_parsing_exactly(self):
        rows = coverage.diff_rows(self.results)
        tei_rows = [
            row for row in rows if row["comparison"] == "CSV no-parsing vs TEI"
        ]
        self.assertTrue(tei_rows)
        self.assertFalse(
            [row for row in tei_rows if row["only_left"] or row["only_right"]]
        )


if __name__ == "__main__":
    unittest.main()
