"""`byz.verify`: manifest shape, inputs, artifacts, and the CLI."""

import hashlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from byz.curate import verify


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _entry(root: Path, relative: str) -> dict:
    path = root / relative
    return {
        "path": relative,
        "sha256": _sha(path),
        "size": path.stat().st_size,
    }


def _write_manifest(edition_dir: Path, manifest: dict) -> None:
    (edition_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


class TempEdition:
    """A tiny repository-shaped tree with one input and one artifact."""

    def __init__(self, root: Path):
        self.root = root
        self.input_root = root / "data" / "raw" / "repo" / "rp2018-2023"
        self.source = self.input_root / "ccat" / "01_MAT.TXT"
        self.source.parent.mkdir(parents=True)
        self.source.write_text("1:1 biblov\n", encoding="utf-8")
        self.edition_dir = root / "editions" / "test"
        self.artifact = (
            self.edition_dir / "csv" / "accented" / "no-variants" / "MAT.csv"
        )
        self.artifact.parent.mkdir(parents=True)
        self.artifact.write_text("chapter,verse,text\n1,1,βιβλος\n", encoding="utf-8")
        self.manifest = {
            "edition": "test",
            "inputs": [
                {
                    "root": "data/raw/repo/rp2018-2023",
                    "include": ["ccat/*.TXT"],
                    "files": [_entry(self.input_root, "ccat/01_MAT.TXT")],
                }
            ],
            "artifact_files": [
                _entry(self.edition_dir, "csv/accented/no-variants/MAT.csv")
            ],
        }
        _write_manifest(self.edition_dir, self.manifest)

    def verify(self):
        with mock.patch.object(
            verify.editions, "edition_dir", lambda _: self.edition_dir
        ):
            return verify.verify_edition("test", root=self.root)


class CleanTreeTests(unittest.TestCase):
    def test_clean_temp_tree_has_no_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            self.assertEqual(fixture.verify(), [])

    def test_clean_repository_tree_passes(self):
        self.assertEqual(verify.main([]), 0)

    def test_selected_edition_passes(self):
        self.assertEqual(verify.main(["rp2018-2023"]), 0)


class InputFailureTests(unittest.TestCase):
    def test_corrupted_input_hash_is_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            fixture.manifest["inputs"][0]["files"][0]["sha256"] = "0" * 64
            _write_manifest(fixture.edition_dir, fixture.manifest)
            errors = fixture.verify()
            self.assertEqual(len(errors), 1)
            self.assertEqual(errors[0].kind, "sha256")
            self.assertIn("data/raw/repo/rp2018-2023/ccat/01_MAT.TXT", errors[0].path)
            self.assertIn("sha256 expected", errors[0].message)
            self.assertIn("0" * 64, errors[0].message)

    def test_missing_input_is_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            fixture.source.unlink()
            errors = fixture.verify()
            kinds = {(error.path, error.kind) for error in errors}
            self.assertIn(("data/raw/repo/rp2018-2023/ccat/01_MAT.TXT", "missing"), kinds)

    def test_extra_matching_input_is_unexpected(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            (fixture.source.parent / "99_ZZZ.TXT").write_text(
                "1:1 scratch\n", encoding="utf-8"
            )
            errors = fixture.verify()
            self.assertIn(
                ("data/raw/repo/rp2018-2023/ccat/99_ZZZ.TXT", "unexpected"),
                {(error.path, error.kind) for error in errors},
            )

    def test_unpinned_input_group_is_unexpected(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            fixture.manifest["inputs"][0]["files"] = []
            _write_manifest(fixture.edition_dir, fixture.manifest)
            errors = fixture.verify()
            self.assertEqual(errors[0].kind, "invalid")
            self.assertIn("non-empty", errors[0].message)


class ArtifactFailureTests(unittest.TestCase):
    def test_corrupted_artifact_hash_is_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            fixture.artifact.write_text("changed\n", encoding="utf-8")
            errors = fixture.verify()
            kinds = {error.kind for error in errors}
            self.assertEqual(kinds, {"sha256", "size"})
            for error in errors:
                self.assertIn(
                    "csv/accented/no-variants/MAT.csv", error.path
                )
                self.assertIn("editions/test", error.path)

    def test_missing_artifact_is_named(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            fixture.artifact.unlink()
            self.assertEqual(fixture.verify()[0].kind, "missing")

    def test_extra_artifact_is_unexpected(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            extra = fixture.edition_dir / "csv" / "extra.csv"
            extra.write_text("x\n", encoding="utf-8")
            self.assertIn(
                ("editions/test/csv/extra.csv", "unexpected"),
                {(error.path, error.kind) for error in fixture.verify()},
            )


class ManifestShapeTests(unittest.TestCase):
    def test_legacy_source_files_manifest_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            fixture.manifest["source_files"] = []
            _write_manifest(fixture.edition_dir, fixture.manifest)
            errors = fixture.verify()
            self.assertEqual(errors[0].kind, "invalid")
            self.assertIn("source_files", errors[0].message)

    def test_absolute_root_is_rejected_before_hashing(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            fixture.manifest["inputs"][0]["root"] = "/etc"
            _write_manifest(fixture.edition_dir, fixture.manifest)
            errors = fixture.verify()
            self.assertEqual(errors[0].kind, "invalid")
            self.assertIn("relative", errors[0].message)

    def test_root_outside_data_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            fixture.manifest["inputs"][0]["root"] = "src"
            _write_manifest(fixture.edition_dir, fixture.manifest)
            with self.assertRaises(verify.VerificationError) as caught:
                verify.load_manifest(fixture.edition_dir)
            self.assertEqual(caught.exception.kind, "invalid")
            self.assertIn("under data/", caught.exception.message)

    def test_root_under_editions_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            fixture.manifest["inputs"][0]["root"] = "editions/other"
            _write_manifest(fixture.edition_dir, fixture.manifest)
            with self.assertRaises(verify.VerificationError) as caught:
                verify.load_manifest(fixture.edition_dir)
            self.assertEqual(caught.exception.kind, "invalid")
            self.assertIn("under data/", caught.exception.message)

    def test_duplicate_artifact_path_is_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            fixture.manifest["artifact_files"].append(
                dict(fixture.manifest["artifact_files"][0])
            )
            _write_manifest(fixture.edition_dir, fixture.manifest)
            errors = fixture.verify()
            self.assertEqual(len(errors), 1)
            self.assertEqual(errors[0].kind, "invalid")
            self.assertIn("duplicate path", errors[0].message)

    def test_unsafe_pdf_path_is_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            fixture.manifest["pdf"] = "../editions-rp2.pdf"
            fixture.manifest["pdf_sha256"] = "0" * 64
            _write_manifest(fixture.edition_dir, fixture.manifest)
            errors = fixture.verify()
            self.assertEqual(errors[0].kind, "invalid")
            self.assertIn("pdf must be a relative POSIX path", errors[0].message)

    def test_parent_traversal_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            fixture.manifest["inputs"][0]["files"][0]["path"] = "../x.TXT"
            _write_manifest(fixture.edition_dir, fixture.manifest)
            errors = fixture.verify()
            self.assertEqual(errors[0].kind, "invalid")

    def test_invalid_json_is_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            (fixture.edition_dir / "manifest.json").write_text(
                "{not json", encoding="utf-8"
            )
            self.assertEqual(fixture.verify()[0].kind, "invalid")


class CommandLineTests(unittest.TestCase):
    def test_unknown_edition_exits_2(self):
        self.assertEqual(verify.main(["no-such-edition"]), 2)

    def test_edition_dir_cannot_be_combined_with_ids(self):
        self.assertEqual(
            verify.main(["rp2018-2023", "--edition-dir", "elsewhere"]), 2
        )


class ExternalEditionTests(unittest.TestCase):
    def test_downloaded_edition_verifies_artifacts_and_skips_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            download = Path(tmp) / "download"
            shutil.copytree(fixture.edition_dir, download)
            stream = io.StringIO()
            checked, errors = verify.verify_all(
                edition_dir=download, stream=stream
            )
            self.assertEqual(checked, 1)
            self.assertEqual(errors, [])
            output = stream.getvalue()
            self.assertIn("OK test: 1 artifacts", output)
            self.assertIn("inputs skipped", output)

    def test_external_artifact_corruption_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            download = Path(tmp) / "download"
            shutil.copytree(fixture.edition_dir, download)
            (download / "csv" / "accented" / "no-variants" / "MAT.csv").write_text(
                "changed\n", encoding="utf-8"
            )
            stream = io.StringIO()
            checked, errors = verify.verify_all(
                edition_dir=download, stream=stream
            )
            self.assertEqual(checked, 1)
            self.assertEqual(len(errors), 2)
            self.assertIn("FAIL test", stream.getvalue())
            self.assertIn("sha256 expected", stream.getvalue())

    def test_external_label_uses_the_manifest_edition(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            download = Path(tmp) / "renamed-copy"
            shutil.copytree(fixture.edition_dir, download)
            stream = io.StringIO()
            checked, errors = verify.verify_all(
                edition_dir=download, stream=stream
            )
            self.assertEqual(checked, 1)
            self.assertEqual(errors, [])
            output = stream.getvalue()
            self.assertIn("OK test: 1 artifacts", output)
            self.assertNotIn("renamed-copy", output)


class NoWriteTests(unittest.TestCase):
    def test_verify_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))

            def snapshot():
                return {
                    path.relative_to(fixture.root).as_posix(): path.read_bytes()
                    for path in fixture.root.rglob("*")
                    if path.is_file()
                }

            before = snapshot()
            fixture.verify()
            verify.verify_all(
                edition_ids=["test"], root=fixture.root, stream=io.StringIO()
            )
            self.assertEqual(snapshot(), before)


class SummaryTests(unittest.TestCase):
    def test_report_counts_inputs_and_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            stream = io.StringIO()
            with mock.patch.object(
                verify.editions, "edition_dir", lambda _: fixture.edition_dir
            ):
                checked, errors = verify.verify_all(
                    edition_ids=["test"], root=fixture.root, stream=stream
                )
            self.assertEqual(checked, 1)
            self.assertEqual(errors, [])
            self.assertIn("OK test: 1 inputs, 1 artifacts", stream.getvalue())
            self.assertIn(
                "verified 1 editions (1 inputs, 1 artifacts)",
                stream.getvalue(),
            )

    def test_failures_are_all_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = TempEdition(Path(tmp))
            fixture.source.write_text("changed\n", encoding="utf-8")
            fixture.artifact.write_text("changed\n", encoding="utf-8")
            stream = io.StringIO()
            with mock.patch.object(
                verify.editions, "edition_dir", lambda _: fixture.edition_dir
            ):
                checked, errors = verify.verify_all(
                    edition_ids=["test"], root=fixture.root, stream=stream
                )
            self.assertEqual(checked, 1)
            # A changed file reports both its hash and its size.
            self.assertEqual(len(errors), 4)
            self.assertEqual(stream.getvalue().count("FAIL test:"), 4)
            self.assertIn("verified 1 editions, 1 failed", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
