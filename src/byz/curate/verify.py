"""Verify curated editions against their manifests.

A manifest pins every input under `data/` by repository-relative path and
SHA-256, and every artifact under the edition by edition-relative path and
SHA-256. This module checks both, reports every failure rather than the first,
and never writes or downloads anything.
"""

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath

from . import editions, files

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

# `matching_files` patterns for an edition's committed artifacts.
ARTIFACT_INCLUDES = ("csv/**/*", "tei/**/*")


class VerificationError(Exception):
    """One verification failure, with enough context to fix it."""

    def __init__(self, edition, path, kind, expected="", actual=""):
        self.edition = edition
        self.path = path
        self.kind = kind
        self.expected = expected
        self.actual = actual
        super().__init__(self.message)

    @property
    def message(self) -> str:
        if self.kind == "sha256":
            return (
                f"{self.path}: sha256 expected {self.expected}, "
                f"actual {self.actual}"
            )
        if self.kind == "size":
            return (
                f"{self.path}: size expected {self.expected}, "
                f"actual {self.actual}"
            )
        if self.kind in ("missing", "unexpected"):
            return f"{self.path}: {self.kind}"
        return f"{self.path}: {self.expected}"


def _is_relative(value) -> bool:
    if not isinstance(value, str) or not value:
        return False
    if "\\" in value or value.startswith("/"):
        return False
    return ".." not in PurePosixPath(value).parts


def _check_entry(entry, label: str) -> None:
    if not isinstance(entry, dict):
        raise ValueError(f"{label} must be an object")
    path = entry.get("path")
    if not _is_relative(path):
        raise ValueError(f"{label}.path must be a relative POSIX path")
    if not isinstance(entry.get("sha256"), str) or not SHA256_RE.match(
        entry["sha256"]
    ):
        raise ValueError(f"{label}.sha256 must be 64 lowercase hex characters")
    size = entry.get("size")
    if not isinstance(size, int) or isinstance(size, bool) or size < 0:
        raise ValueError(f"{label}.size must be a non-negative integer")


def load_manifest(
    edition_dir: Path,
    edition_id: str = "",
    *,
    display_path: str | None = None,
) -> dict:
    """Load and shape-check `edition_dir/manifest.json`.

    Raises `VerificationError` instead of returning a partial manifest. The
    directory basename is deliberately not compared with the manifest's
    `edition`; that repository-mode check belongs to the caller.
    `display_path` overrides the path in the error, so repository mode can
    report the repo-relative `editions/<id>/manifest.json` rather than the
    absolute working-tree path (R5.3).
    """
    path = Path(edition_dir) / "manifest.json"
    label = edition_id or Path(edition_dir).name
    shown = display_path or path.as_posix()
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise VerificationError(label, shown, "missing")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError(
            label, shown, "invalid", expected=str(error)
        )
    try:
        if not isinstance(manifest, dict):
            raise ValueError("manifest must be a JSON object")
        if "source_files" in manifest:
            raise ValueError("manifest must not contain source_files")
        inputs = manifest.get("inputs")
        if not isinstance(inputs, list) or not inputs:
            raise ValueError("manifest must contain a non-empty inputs list")
        artifacts = manifest.get("artifact_files")
        if not isinstance(artifacts, list) or not artifacts:
            raise ValueError(
                "manifest must contain a non-empty artifact_files list"
            )
        for index, group in enumerate(inputs):
            group_label = f"inputs[{index}]"
            if not isinstance(group, dict):
                raise ValueError(f"{group_label} must be an object")
            root = group.get("root")
            if not _is_relative(root):
                raise ValueError(
                    f"{group_label}.root must be a relative POSIX path"
                )
            if not (root == "data" or root.startswith("data/")):
                raise ValueError(f"{group_label}.root must be under data/")
            includes = group.get("include")
            if not isinstance(includes, list) or not includes:
                raise ValueError(
                    f"{group_label}.include must be a non-empty list"
                )
            for pattern in includes:
                if not _is_relative(pattern):
                    raise ValueError(
                        f"{group_label}.include must hold relative globs"
                    )
            group_files = group.get("files")
            if not isinstance(group_files, list) or not group_files:
                raise ValueError(
                    f"{group_label}.files must be a non-empty list"
                )
            for file_index, entry in enumerate(group_files):
                _check_entry(entry, f"{group_label}.files[{file_index}]")
        for index, entry in enumerate(artifacts):
            _check_entry(entry, f"artifact_files[{index}]")
            if not entry["path"].startswith(("csv/", "tei/")):
                raise ValueError(
                    f"artifact_files[{index}].path must start with csv/ or tei/"
                )
    except ValueError as error:
        raise VerificationError(
            label,
            shown,
            "invalid",
            expected=str(error),
        )
    return manifest


def _verify_entries(label, manifest_entries, matched, prefix) -> list:
    """Compare a manifest file list with a `{relative: Path}` match set."""
    errors = []
    expected = {}
    for entry in manifest_entries:
        if entry["path"] in expected:
            errors.append(
                VerificationError(
                    label,
                    f"{prefix}/{entry['path']}",
                    "invalid",
                    expected="duplicate path in manifest",
                )
            )
            continue
        expected[entry["path"]] = entry
    for missing in sorted(set(expected) - set(matched)):
        errors.append(
            VerificationError(label, f"{prefix}/{missing}", "missing")
        )
    for extra in sorted(set(matched) - set(expected)):
        errors.append(
            VerificationError(label, f"{prefix}/{extra}", "unexpected")
        )
    for relative in sorted(set(expected) & set(matched)):
        entry = expected[relative]
        path = matched[relative]
        actual_hash = files.sha256_file(path)
        if actual_hash != entry["sha256"]:
            errors.append(
                VerificationError(
                    label,
                    f"{prefix}/{relative}",
                    "sha256",
                    expected=entry["sha256"],
                    actual=actual_hash,
                )
            )
        actual_size = path.stat().st_size
        if actual_size != entry["size"]:
            errors.append(
                VerificationError(
                    label,
                    f"{prefix}/{relative}",
                    "size",
                    expected=str(entry["size"]),
                    actual=str(actual_size),
                )
            )
    return errors


def verify_inputs(manifest, edition_id, root: Path) -> list:
    """Check every input group against `root` (the repository root)."""
    errors = []
    for group in manifest["inputs"]:
        group_root = root / group["root"]
        if not group_root.is_dir():
            errors.append(
                VerificationError(edition_id, group["root"], "missing")
            )
            continue
        matched = files.matching_files(group_root, group["include"])
        errors.extend(
            _verify_entries(
                edition_id, group["files"], matched, group["root"]
            )
        )
    return errors


def verify_artifacts(manifest, edition_id, edition_dir: Path) -> list:
    """Check the committed `csv/` and `tei/` trees against the manifest."""
    matched = files.matching_files(edition_dir, ARTIFACT_INCLUDES)
    return _verify_entries(
        edition_id,
        manifest["artifact_files"],
        matched,
        f"editions/{edition_id}",
    )


def verify_artifacts_external(manifest, edition_dir: Path) -> list:
    """Check an extracted edition's artifacts, naming its own paths."""
    matched = files.matching_files(edition_dir, ARTIFACT_INCLUDES)
    label = manifest.get("edition", edition_dir.name)
    return _verify_entries(
        label, manifest["artifact_files"], matched, edition_dir.as_posix()
    )


def verify_pdf(manifest, edition_id, root: Path) -> list:
    """Check the committed official PDF when the manifest pins one."""
    if manifest.get("pdf") and "pdf_sha256" not in manifest:
        return [
            VerificationError(
                edition_id,
                str(manifest["pdf"]),
                "invalid",
                expected="pdf_sha256 is required when pdf is set",
            )
        ]
    if "pdf_sha256" not in manifest:
        return []
    relative = manifest.get("pdf", "")
    if not _is_relative(relative):
        return [
            VerificationError(
                edition_id,
                str(relative),
                "invalid",
                expected="pdf must be a relative POSIX path",
            )
        ]
    path = root / relative
    if not path.is_file():
        return [VerificationError(edition_id, relative, "missing")]
    errors = []
    actual_hash = files.sha256_file(path)
    if actual_hash != manifest["pdf_sha256"]:
        errors.append(
            VerificationError(
                edition_id,
                relative,
                "sha256",
                expected=manifest["pdf_sha256"],
                actual=actual_hash,
            )
        )
    expected_size = manifest.get("pdf_size")
    actual_size = path.stat().st_size
    if expected_size is not None and expected_size != actual_size:
        errors.append(
            VerificationError(
                edition_id,
                relative,
                "size",
                expected=str(expected_size),
                actual=str(actual_size),
            )
        )
    return errors


def verify_edition(
    edition_id: str, *, edition_dir: Path | None = None, root: Path | None = None
) -> list:
    """Return the failures for one edition; an empty list means success."""
    root = Path(root) if root is not None else editions.ROOT
    external = edition_dir is not None
    edition_path = Path(edition_dir) if external else editions.edition_dir(
        edition_id
    )
    try:
        manifest = load_manifest(
            edition_path,
            "" if external else edition_id,
            display_path=(
                None
                if external
                else f"editions/{edition_id}/manifest.json"
            ),
        )
    except VerificationError as error:
        return [error]
    if external:
        return verify_artifacts_external(manifest, edition_path)
    errors = []
    actual_label = manifest.get("edition", edition_id)
    if actual_label != edition_id:
        errors.append(
            VerificationError(
                edition_id,
                "manifest.json",
                "invalid",
                expected=f"edition {edition_id}, actual {actual_label}",
            )
        )
    errors.extend(verify_inputs(manifest, edition_id, root))
    errors.extend(verify_artifacts(manifest, edition_id, edition_path))
    errors.extend(verify_pdf(manifest, edition_id, root))
    return errors


def _counts(manifest: dict) -> tuple:
    inputs = sum(len(group["files"]) for group in manifest["inputs"])
    return inputs, len(manifest["artifact_files"])


def verify_all(
    edition_ids=None,
    *,
    edition_dir: Path | None = None,
    root: Path | None = None,
    stream=None,
) -> tuple:
    """Verify the selected editions, print a report, return `(checked, errors)`."""
    out = stream or sys.stdout
    root = Path(root) if root is not None else editions.ROOT
    if edition_dir is not None:
        entries = [(None, Path(edition_dir))]
    else:
        ids = list(edition_ids) if edition_ids else list(editions.EDITIONS)
        entries = [(edition_id, editions.edition_dir(edition_id)) for edition_id in ids]

    checked = 0
    failed = 0
    total_inputs = 0
    total_artifacts = 0
    all_errors = []
    for edition_id, path in entries:
        checked += 1
        display_path = (
            path.as_posix()
            if edition_dir is not None
            else f"editions/{edition_id}/manifest.json"
        )
        try:
            manifest = load_manifest(
                path, edition_id or "", display_path=display_path
            )
        except VerificationError as error:
            failed += 1
            all_errors.append(error)
            print(f"FAIL {error.edition}: {error.message}", file=out)
            continue
        label = manifest.get("edition", edition_id or path.name)
        if edition_dir is not None:
            errors = verify_artifacts_external(manifest, path)
        else:
            errors = []
            if label != edition_id:
                errors.append(
                    VerificationError(
                        edition_id,
                        "manifest.json",
                        "invalid",
                        expected=f"edition {edition_id}, actual {label}",
                    )
                )
            errors.extend(verify_inputs(manifest, edition_id, root))
            errors.extend(verify_artifacts(manifest, edition_id, path))
            errors.extend(verify_pdf(manifest, edition_id, root))
        if errors:
            failed += 1
            all_errors.extend(errors)
            for error in errors:
                print(f"FAIL {error.edition}: {error.message}", file=out)
            continue
        inputs, artifacts = _counts(manifest)
        total_inputs += inputs if edition_dir is None else 0
        total_artifacts += artifacts
        if edition_dir is not None:
            print(
                f"OK {label}: {artifacts} artifacts "
                "(external edition directory; inputs skipped)",
                file=out,
            )
        else:
            print(f"OK {label}: {inputs} inputs, {artifacts} artifacts", file=out)

    if failed:
        print(f"verified {checked} editions, {failed} failed", file=out)
    else:
        print(
            f"verified {checked} editions "
            f"({total_inputs} inputs, {total_artifacts} artifacts)",
            file=out,
        )
    return checked, all_errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="byz.verify",
        description="Verify curated editions against their manifests.",
    )
    parser.add_argument(
        "editions",
        nargs="*",
        metavar="edition",
        help="edition id(s) to verify (default: all four, registry order)",
    )
    parser.add_argument(
        "--edition-dir",
        metavar="PATH",
        help="verify an extracted edition's artifacts only",
    )
    args = parser.parse_args(argv)

    if args.edition_dir and args.editions:
        print(
            "byz.verify: --edition-dir cannot be combined with edition ids",
            file=sys.stderr,
        )
        return 2
    if args.editions:
        unknown = [
            edition_id
            for edition_id in args.editions
            if edition_id not in editions.EDITIONS
        ]
        if unknown:
            print(
                "byz.verify: unknown edition(s): "
                + ", ".join(unknown)
                + "; valid ids: "
                + ", ".join(editions.EDITIONS),
                file=sys.stderr,
            )
            return 2

    _, errors = verify_all(
        args.editions or None, edition_dir=args.edition_dir
    )
    return 1 if errors else 0
