"""Fetch, checksum, extract, and record the official archives."""

import argparse
import hashlib
import json
import shutil
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from . import sources


def sha256_file(path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _download_url(url: str) -> str:
    return url.replace("?dl=0", "?dl=1")


def download(url: str, dest: Path) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        _download_url(url), headers={"User-Agent": "byz-reconcile/1.0"}
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        status = getattr(response, "status", None) or 200
        final_url = response.geturl()
        with open(dest, "wb") as handle:
            shutil.copyfileobj(response, handle)
    return {"http_status": status, "final_url": final_url}


def extract(zip_path: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(dest)


def _existing_records(provenance_path: Path) -> dict:
    if not provenance_path.exists():
        return {}
    records = {}
    current = {}
    for line in provenance_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line == "[[archives]]":
            if current.get("name"):
                records[current["name"]] = current
            current = {}
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if value.startswith('"'):
            value = json.loads(value)
        elif value.isdigit():
            value = int(value)
        current[key.strip()] = value
    if current.get("name"):
        records[current["name"]] = current
    return records


def _existing_hashes(provenance_path: Path) -> dict:
    return {
        name: record.get("sha256", "")
        for name, record in _existing_records(provenance_path).items()
    }


def _toml_value(value) -> str:
    if isinstance(value, int):
        return str(value)
    return json.dumps(str(value))


def _write_provenance(edition: str, records: list) -> Path:
    path = sources.PROVENANCE_DIR / f"{edition}.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"edition = {_toml_value(edition)}", ""]
    for record in records:
        lines.append("[[archives]]")
        for key in (
            "name",
            "format",
            "requested_url",
            "download_url",
            "final_url",
            "http_status",
            "downloaded",
            "size",
            "sha256",
            "extracted",
        ):
            lines.append(f"{key} = {_toml_value(record[key])}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def run(verify: bool = False, force: bool = False) -> list:
    by_edition = {}
    for spec in sources.ARCHIVES:
        edition = spec["edition"]
        provenance_path = sources.PROVENANCE_DIR / f"{edition}.toml"
        existing_records = _existing_records(provenance_path)
        existing = {
            name: record.get("sha256", "")
            for name, record in existing_records.items()
        }
        zip_path = sources.ARCHIVE_DIR / edition / spec["name"]
        expected = existing.get(spec["name"])

        need_download = force or not zip_path.exists()
        if zip_path.exists() and expected and sha256_file(zip_path) != expected:
            need_download = True
        if verify and zip_path.exists() and expected is None:
            need_download = True

        if need_download:
            meta = download(spec["url"], zip_path)
            downloaded = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            previous = existing_records.get(spec["name"], {})
            meta = {
                "http_status": previous.get("http_status", ""),
                "final_url": previous.get("final_url", ""),
            }
            downloaded = previous.get("downloaded", "")

        digest = sha256_file(zip_path)
        if expected and digest != expected:
            raise SystemExit(
                f"checksum changed for {spec['name']}: {expected} -> {digest}"
            )

        stem = Path(spec["name"]).stem
        extract_path = sources.RAW_DIR / edition / stem
        if force or not extract_path.exists():
            extract(zip_path, extract_path)

        record = {
            "name": spec["name"],
            "format": spec["format"],
            "requested_url": spec["url"],
            "download_url": _download_url(spec["url"]),
            "final_url": meta["final_url"],
            "http_status": meta["http_status"],
            "downloaded": downloaded,
            "size": zip_path.stat().st_size,
            "sha256": digest,
            "extracted": str(extract_path.relative_to(sources.ROOT)),
        }
        by_edition.setdefault(edition, []).append(record)

    written = []
    for edition, records in by_edition.items():
        written.append(_write_provenance(edition, records))
    return written


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verify",
        action="store_true",
        help="verify existing archives against recorded checksums",
    )
    parser.add_argument(
        "--force", action="store_true", help="re-download and re-extract"
    )
    args = parser.parse_args(argv)
    written = run(verify=args.verify, force=args.force)
    for path in written:
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
