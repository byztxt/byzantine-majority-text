"""Recovery safety: a failed recovery must not destroy the existing edition."""

import tempfile
import unittest
from pathlib import Path

from byz.curate import editions, recover


class RecoverySafetyTests(unittest.TestCase):
    def test_failed_archive_keeps_the_existing_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = editions.EDITIONS_DIR
            editions.EDITIONS_DIR = Path(tmp)
            try:
                final = Path(tmp) / "rp2005-2019"
                (final / "source").mkdir(parents=True)
                (final / "marker.txt").write_text("keep me", encoding="utf-8")
                with self.assertRaises(SystemExit):
                    recover.recover_historical(
                        {"id": "rp2005-2019", "tag": "no-such-tag"}
                    )
                self.assertEqual(
                    (final / "marker.txt").read_text(encoding="utf-8"),
                    "keep me",
                )
                self.assertFalse((Path(tmp) / ".rp2005-2019.staging").exists())
            finally:
                editions.EDITIONS_DIR = original


if __name__ == "__main__":
    unittest.main()
