"""Regeneration determinism: a real subprocess rebuild must be byte-identical."""

import hashlib
import subprocess
import sys
import unittest
from pathlib import Path

from byz.curate import editions

ROOT = editions.ROOT
SCRIPTS = [
    ROOT / "scripts" / "recover_editions.py",
    ROOT / "scripts" / "build_editions.py",
    ROOT / "scripts" / "diff_editions.py",
]


def _snapshot():
    hashes = {}
    for base in (ROOT / "editions", ROOT / "reports" / "diffs"):
        for path in sorted(base.rglob("*")):
            if path.is_file():
                hashes[str(path.relative_to(ROOT))] = hashlib.sha256(
                    path.read_bytes()
                ).hexdigest()
    for path in (ROOT / "docs" / "EDITIONS.md", ROOT / "README.md"):
        hashes[str(path.relative_to(ROOT))] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
    return hashes


class RegenerationDeterminismTests(unittest.TestCase):
    def test_rebuild_is_byte_identical(self):
        first = _snapshot()
        for script in SCRIPTS:
            result = subprocess.run(
                [sys.executable, str(script)],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                result.returncode,
                0,
                f"{script.name} failed: {result.stderr[-2000:]}",
            )
        second = _snapshot()
        changed = sorted(
            path
            for path in set(first) | set(second)
            if first.get(path) != second.get(path)
        )
        self.assertEqual(changed, [], "regeneration is not deterministic")
        staging = [
            path.name
            for path in (ROOT / "editions").iterdir()
            if path.name.startswith(".")
        ]
        self.assertEqual(staging, [], "recovery left a staging directory behind")


if __name__ == "__main__":
    unittest.main()
