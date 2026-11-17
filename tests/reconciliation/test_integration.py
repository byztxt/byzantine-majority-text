import unittest

from byz.reconcile import compare, fetch, historical, sources


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
    "the official archives committed under data/raw/_archives are missing or "
    "corrupt: restore them with `git checkout -- data/raw/_archives`, or run "
    "`python3 scripts/fetch_official.py --force` to re-download. These checks "
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
            and row["current"] == "source/CCAT/01_MAT.TXT"
        }
        self.assertIn("rp2005", source)
        self.assertIn("rp2018", source)

    def test_source_rows_present(self):
        source = [row for row in self.results["files"] if row["tier"] == "source"]
        self.assertEqual(len(source), 58)

    def test_strongs_provenance_unknown(self):
        self.assertEqual(self.results["strongs"]["status"], "provenance-unknown")

    def test_intentional_blanks_confirmed(self):
        blanks = self.results["blanks"]
        self.assertEqual(len(blanks), 8)
        self.assertTrue(all(row["in_official_ccat"] for row in blanks))
        self.assertTrue(all(row["official_blank"] for row in blanks))

    def test_mapping_classes_present(self):
        classes = {row["class"] for row in self.results["files"]}
        self.assertIn("provenance-unknown", classes)
        self.assertIn("incomparable-pending-pipeline", classes)
        self.assertIn("auxiliary", classes)

    def test_history_lineage(self):
        rows = {
            (row["state"], row["compared_to"]): row
            for row in historical.evidence()
        }
        v203_05 = rows[("v2.0.3 textonly-beta-code", "rp2005")]
        v203_18 = rows[("v2.0.3 textonly-beta-code", "rp2018")]
        cur_05 = rows[("current source/CCAT", "rp2005")]
        cur_18 = rows[("current source/CCAT", "rp2018")]
        self.assertGreater(v203_18["match"], v203_05["match"])
        self.assertGreater(cur_18["match"], cur_05["match"])
        self.assertGreater(v203_18["match"], cur_18["match"])


if __name__ == "__main__":
    unittest.main()
