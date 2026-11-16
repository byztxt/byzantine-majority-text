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


if __name__ == "__main__":
    unittest.main()
