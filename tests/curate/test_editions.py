import hashlib
import re
import unittest

from byz.curate import editions


class EditionTests(unittest.TestCase):
    def test_four_editions(self):
        self.assertEqual(
            set(editions.EDITIONS),
            {"rp2005", "rp2005-2019", "rp2018", "rp2018-2023"},
        )

    def test_release_ranges(self):
        historical = editions.metadata("rp2005-2019")
        current = editions.metadata("rp2018-2023")
        self.assertEqual(historical["release_range"], "v1.0.0-v2.0.3")
        self.assertEqual(current["release_range"], "v3.0.0-v3.3.4")
        self.assertEqual(editions.metadata("rp2005")["release_range"], "")
        self.assertEqual(editions.metadata("rp2018")["release_range"], "")

    def test_official_status(self):
        self.assertEqual(editions.metadata("rp2005")["status"], "official")
        self.assertEqual(editions.metadata("rp2018")["status"], "official")
        self.assertEqual(editions.metadata("rp2005-2019")["status"], "released")
        self.assertEqual(editions.metadata("rp2018-2023")["status"], "released")

    def test_pdf_hashes(self):
        text = (editions.PROVENANCE_DIR / "pdfs.toml").read_text()
        records = {}
        current = {}
        for line in text.splitlines():
            if line.strip() == "[[pdfs]]":
                if current.get("path"):
                    records[current["path"]] = current.get("sha256", "")
                current = {}
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                current[key.strip()] = value.strip().strip('"')
        if current.get("path"):
            records[current["path"]] = current.get("sha256", "")
        self.assertEqual(len(records), 2)
        for relpath, expected in records.items():
            path = editions.ROOT / relpath
            self.assertTrue(path.is_file())
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(digest, expected)


if __name__ == "__main__":
    unittest.main()
