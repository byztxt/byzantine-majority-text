"""Tests for `data/provenance/rp2018-2023.toml` and its writer.

The current text is a repository-lineage source snapshot, so it gets the same
kind of provenance record as the 2019 lineage: the revision, the two source
commits, and a SHA-256 per input. `byz.build` writes it from the manifest it
just produced, so the record and the pins cannot disagree.
"""

import hashlib
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from byz import generated
from byz.curate import build, editions, files

ROOT = editions.ROOT
PROVENANCE = ROOT / "data" / "provenance" / "rp2018-2023.toml"


def parse_record(raw: str) -> dict:
    """Parse the fixed-shape provenance TOML without a 3.11+ parser.

    `build._current_provenance_text` writes the record in a known shape: scalar
    `key = value` lines, then `[[prefixes]]` and `[[files]]` tables of the same
    scalar lines. This repository targets Python 3.10, which has no `tomllib`,
    so the test parses that shape directly rather than adding a dependency.
    """
    record = {"prefixes": [], "files": []}
    table = None
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        header = re.fullmatch(r"\[\[(prefixes|files)\]\]", line)
        if header:
            table = {}
            record[header.group(1)].append(table)
            continue
        match = re.fullmatch(
            r'([A-Za-z_][A-Za-z0-9_]*) = "([^"]*)"', line
        )
        if match:
            key, value = match.group(1), match.group(2)
        else:
            match = re.fullmatch(
                r"([A-Za-z_][A-Za-z0-9_]*) = (\d+)", line
            )
            if not match:
                raise AssertionError(f"unparsed provenance line: {line!r}")
            key, value = match.group(1), int(match.group(2))
        if table is None:
            record[key] = value
        else:
            table[key] = value
    return record


def manifests():
    rows = {}
    for edition_id in editions.EDITIONS:
        path = editions.edition_dir(edition_id) / "manifest.json"
        rows[edition_id] = json.loads(path.read_text(encoding="utf-8"))
    return rows


class ProvenanceRecordTests(unittest.TestCase):
    def setUp(self):
        self.raw = PROVENANCE.read_text(encoding="utf-8")
        self.record = parse_record(self.raw)

    def test_file_has_the_toml_banner(self):
        self.assertTrue(PROVENANCE.is_file())
        self.assertEqual(self.raw.splitlines()[0], generated.TOML_MARKER)
        self.assertFalse(self.raw.startswith(generated.MARKDOWN_MARKER))

    def test_scalar_facts(self):
        self.assertEqual(self.record["edition"], "rp2018-2023")
        self.assertEqual(self.record["revision"], "2023-07-20")
        self.assertEqual(self.record["method"], "working-tree snapshot")
        self.assertEqual(
            self.record["extracted"], "data/raw/repo/rp2018-2023"
        )
        self.assertEqual(
            self.record["generated_by"], "PYTHONPATH=src python3 -m byz.build"
        )
        for key in ("ccat_commit", "strongs_commit"):
            self.assertRegex(self.record[key], r"^[0-9a-f]{40}$")

    def test_no_url_timestamp_or_absolute_path(self):
        self.assertNotIn("http", self.raw)
        self.assertNotIn("downloaded", self.raw)
        self.assertNotIn("/home/", self.raw)
        self.assertNotRegex(self.raw, r"\b\d{4}-\d{2}-\d{2}T")

    def test_two_sorted_prefix_blocks(self):
        prefixes = self.record["prefixes"]
        self.assertEqual(
            [block["path"] for block in prefixes], ["ccat/", "strongs/"]
        )
        self.assertEqual(prefixes[0]["files"], 29)
        self.assertEqual(prefixes[1]["files"], 27)

    def test_file_blocks_are_sorted_and_complete(self):
        blocks = self.record["files"]
        self.assertEqual(len(blocks), 56)
        paths = [block["path"] for block in blocks]
        self.assertEqual(paths, sorted(paths))
        for block in blocks:
            path = ROOT / "data" / "raw" / "repo" / "rp2018-2023" / block["path"]
            self.assertTrue(path.is_file(), block["path"])
            self.assertEqual(
                block["sha256"], files.sha256_file(path), block["path"]
            )
            self.assertEqual(
                block["size"], path.stat().st_size, block["path"]
            )

    def test_file_set_equals_the_manifest_group(self):
        group = manifests()["rp2018-2023"]["inputs"][0]
        # The manifest and the provenance both state paths relative to the
        # source root, so each one starts with `ccat/` or `strongs/`.
        expected = {entry["path"] for entry in group["files"]}
        actual = {block["path"] for block in self.record["files"]}
        self.assertEqual(actual, expected)

    def test_hashes_match_the_committed_files(self):
        for block in self.record["files"]:
            path = (
                ROOT / "data" / "raw" / "repo" / "rp2018-2023" / block["path"]
            )
            self.assertEqual(
                block["sha256"],
                hashlib.sha256(path.read_bytes()).hexdigest(),
                block["path"],
            )

    def test_historical_commit_matches_the_tag(self):
        result = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "v2.0.3^{commit}"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            editions.EDITIONS["rp2005-2019"]["commit"],
            result.stdout.strip(),
        )
        historical = manifests()["rp2005-2019"]
        self.assertEqual(historical["commit"], result.stdout.strip())


class WriterTests(unittest.TestCase):
    def test_writer_is_deterministic(self):
        manifest = manifests()["rp2018-2023"]
        first = build._current_provenance_text(
            editions.EDITIONS["rp2018-2023"],
            manifest["inputs"],
            manifest["source_commit"],
            manifest["strongs_commit"],
        )
        second = build._current_provenance_text(
            editions.EDITIONS["rp2018-2023"],
            manifest["inputs"],
            manifest["source_commit"],
            manifest["strongs_commit"],
        )
        self.assertEqual(first, second)
        self.assertEqual(first, PROVENANCE.read_text(encoding="utf-8"))

    def test_write_manifest_twice_writes_identical_bytes(self):
        edition = editions.metadata("rp2018-2023")
        manifest = manifests()["rp2018-2023"]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            edition_root = root / "editions" / "rp2018-2023"
            (edition_root / "csv").mkdir(parents=True)
            (edition_root / "tei").mkdir()
            provenance_dir = root / "provenance"
            provenance_dir.mkdir()
            with (
                mock.patch.object(
                    editions, "edition_dir", lambda _: edition_root
                ),
                mock.patch.object(
                    editions, "PROVENANCE_DIR", provenance_dir
                ),
            ):
                build.write_manifest(edition, manifest["inputs"])
                first = (provenance_dir / "rp2018-2023.toml").read_bytes()
                build.write_manifest(edition, manifest["inputs"])
                second = (provenance_dir / "rp2018-2023.toml").read_bytes()
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
