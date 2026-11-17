"""Fetch, checksum, extract, and record the official archives."""

import argparse
import hashlib
import json
import shutil
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from . import sources

# Refuse to download anything larger than this. The official archives are all
# under 0.5 MB, so 50 MB leaves plenty of headroom.
MAX_DOWNLOAD_BYTES = 50 * 1024 * 1024

# The official archives are hosted on Dropbox. Downloads are https-only and the
# host (including redirect targets such as `*.dl.dropboxusercontent.com`) must be
# on this allow-list.
ALLOWED_HOSTS = ("dropbox.com", "dropboxusercontent.com")


def sha256_file(path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _download_url(url: str) -> str:
    return url.replace("?dl=0", "?dl=1")


def _check_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https":
        raise ValueError(f"refusing non-https archive URL: {url}")
    host = (parsed.hostname or "").lower()
    allowed = any(
        host == suffix or host.endswith("." + suffix)
        for suffix in ALLOWED_HOSTS
    )
    if not allowed:
        raise ValueError(
            f"refusing archive URL from untrusted host {host!r}: {url}"
        )
    return url


def download(url: str, dest: Path) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        _check_url(_download_url(url)), headers={"User-Agent": "byz-reconcile/1.0"}
    )
    temp = dest.with_name(dest.name + ".part")
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            status = getattr(response, "status", None) or 200
            final_url = response.geturl()
            _check_url(final_url)
            length = response.headers.get("Content-Length")
            if length is not None and int(length) > MAX_DOWNLOAD_BYTES:
                raise ValueError(
                    f"archive at {final_url} is {length} bytes, above the "
                    f"{MAX_DOWNLOAD_BYTES}-byte download cap"
                )
            written = 0
            with open(temp, "wb") as handle:
                while True:
                    chunk = response.read(1 << 20)
                    if not chunk:
                        break
                    written += len(chunk)
                    if written > MAX_DOWNLOAD_BYTES:
                        raise ValueError(
                            f"archive at {final_url} exceeds the "
                            f"{MAX_DOWNLOAD_BYTES}-byte download cap"
                        )
                    handle.write(chunk)
        os.replace(temp, dest)
    except BaseException:
        # Delete only the partial file: a pre-existing archive at `dest` is
        # still the last known-good copy.
        if temp.exists():
            temp.unlink()
        raise
    return {"http_status": status, "final_url": final_url}


def _safe_member(dest: Path, name: str) -> Path:
    """Return the extraction target for a zip member, rejecting escapes."""
    member = Path(name)
    if member.is_absolute() or ".." in member.parts:
        raise ValueError(f"unsafe absolute or parent path in archive member: {name!r}")
    target = (dest / name).resolve()
    if not target.is_relative_to(dest.resolve()):
        raise ValueError(f"archive member escapes the destination: {name!r}")
    return target


def extract(zip_path: Path, dest: Path) -> None:
    with zipfile.ZipFile(zip_path) as archive:
        # Validate every member before touching the destination, so a bad
        # archive cannot leave a half-cleared tree.
        members = [
            (_safe_member(dest, member.filename), member)
            for member in archive.infolist()
        ]
        # Clear stale files from a previous extraction of the same archive.
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True, exist_ok=True)
        for target, member in members:
            if member.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(member) as source, open(target, "wb") as handle:
                shutil.copyfileobj(source, handle)


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
        zip_path = sources.ARCHIVE_DIR / edition / spec["name"]
        expected = spec["sha256"]

        need_download = force or not zip_path.exists()
        if zip_path.exists() and not need_download:
            actual = sha256_file(zip_path)
            if actual != expected:
                if verify:
                    raise SystemExit(
                        f"archive {spec['name']} does not match the pinned "
                        f"sha256: expected {expected}, got {actual}. Delete "
                        f"{zip_path} to re-download it."
                    )
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

        # The pinned digest is authoritative: verify every archive we are about
        # to record and extract, whether it was just downloaded or reused.
        digest = sha256_file(zip_path)
        if digest != expected:
            raise SystemExit(
                f"checksum mismatch for {spec['name']}: pinned {expected}, "
                f"got {digest}. Delete {zip_path} to re-download it."
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
        help="verify existing archives against the pinned checksums",
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
