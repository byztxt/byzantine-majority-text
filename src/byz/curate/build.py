"""Build curated CSV/TEI exports and manifests for every edition."""

import csv
import hashlib
import json
import re
from pathlib import Path

from byz.contract import paths
from byz.reconcile import normalize, sources

from . import editions, recover

ASCII_TO_GREEK = {
    "a": "α",
    "b": "β",
    "g": "γ",
    "d": "δ",
    "e": "ε",
    "z": "ζ",
    "h": "η",
    "y": "θ",
    "i": "ι",
    "k": "κ",
    "l": "λ",
    "m": "μ",
    "n": "ν",
    "x": "ξ",
    "o": "ο",
    "p": "π",
    "r": "ρ",
    "s": "σ",
    "v": "ς",
    "t": "τ",
    "u": "υ",
    "f": "φ",
    "c": "χ",
    "q": "ψ",
    "w": "ω",
}

VERSE_RE = re.compile(r"^\s*(\d+):(\d+)\s?(.*)$")


def ascii_to_greek(text: str) -> str:
    return "".join(ASCII_TO_GREEK.get(char, char) for char in text)


def parse_ascii_main(path: Path) -> dict:
    verses = {}
    for line in path.read_text().splitlines():
        match = VERSE_RE.match(line)
        if not match:
            continue
        key = (int(match.group(1)), int(match.group(2)))
        verses[key] = ascii_to_greek(match.group(3).strip())
    return verses


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _hash_tree(path: Path, root: Path) -> list:
    rows = []
    for file in sorted(path.rglob("*")):
        if file.is_file():
            rows.append(
                {
                    "path": str(file.relative_to(root)),
                    "sha256": _sha256(file),
                    "size": file.stat().st_size,
                }
            )
    return rows


def write_csv(path: Path, verses: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["chapter", "verse", "text"])
        for (chapter, verse) in sorted(verses):
            writer.writerow([chapter, verse, verses[(chapter, verse)]])


def _tei_verse(book_id: str, chapter: int, verse: int, text: str) -> str:
    anchor = f"{book_id}K{chapter}V{verse}"
    if not text:
        return f'\t\t\t\t\t<ab n="{anchor}"/>'
    words = "\n".join(
        f"\t\t\t\t\t\t<w>{word}</w>" for word in text.split(" ")
    )
    return f'\t\t\t\t\t<ab n="{anchor}">\n{words}\n\t\t\t\t\t</ab>'


def _tei_book(abbr: str, book_id: str, verses: dict) -> str:
    chapters = {}
    for (chapter, verse), text in verses.items():
        chapters.setdefault(chapter, {})[verse] = text
    lines = [f'\t\t\t<div type="book" n="{book_id}">']
    for chapter in sorted(chapters):
        chapter_id = f"{book_id}K{chapter}"
        lines.append(f'\t\t\t\t<div type="chapter" n="{chapter_id}">')
        for verse in sorted(chapters[chapter]):
            lines.append(
                _tei_verse(book_id, chapter, verse, chapters[chapter][verse])
            )
        lines.append("\t\t\t\t</div>")
    lines.append("\t\t\t</div>")
    return "\n".join(lines)


def _header_template() -> str:
    return (editions.ROOT / "scripts" / "tei_xml_header.xml").read_text()


def write_tei(
    path: Path, books: list, combined: bool = False, edition_label: str = ""
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    template = _header_template()
    if edition_label:
        template = re.sub(
            r'<edition n="[^"]*">.*?</edition>',
            f'<edition n="{edition_label}">Official print edition</edition>',
            template,
            flags=re.S,
        )
    body = "\n".join(_tei_book(abbr, book_id, verses) for abbr, book_id, verses in books)
    if combined:
        prefix = template.replace("BOOK_METADATA_PLACEHOLDER", "")
    else:
        abbr, book_id, _ = books[0]
        num = paths.ABBR_TO_NUM[abbr]
        metadata = (
            f'\n\t\t\t\t<title type="work" level="m" xml:lang="en" n="{num}">'
            f"{editions.BOOK_NAMES[abbr]}</title>\n"
            f'\t\t\t\t<title type="short" level="m" xml:lang="en" n="{num}">'
            f"{abbr}</title>"
        )
        prefix = template.replace("BOOK_METADATA_PLACEHOLDER", metadata)
    path.write_text(prefix + body + "\n\t\t</body>\n\t</text>\n</TEI>", encoding="utf-8")


def build_official(edition: dict) -> None:
    edition_dir = editions.edition_dir(edition["id"])
    ascii_dir = editions.ROOT / edition["ascii_dir"]
    ccat_dir = edition_dir / "source" / "ccat"
    books = []
    for ascii_file in sorted(ascii_dir.glob("*_Byz.txt")):
        code = ascii_file.name.split("_", 1)[0]
        abbr = sources.OFFICIAL_TO_ABBR.get(code)
        if not abbr:
            continue
        verses = parse_ascii_main(ascii_file)
        ccat_file = ccat_dir / f"{code}.CCT"
        if ccat_file.exists():
            official_keys = normalize.parse_cct(ccat_file.read_text())
            for key in official_keys:
                verses.setdefault(key, "")
        write_csv(edition_dir / "csv" / "ascii-one-line" / f"{abbr}.csv", verses)
        book_id = paths.ABBR_TO_BOOK_ID[abbr]
        books.append((abbr, book_id, verses))
    label = edition["id"].replace("rp", "")
    for abbr, book_id, verses in books:
        write_tei(
            edition_dir / "tei" / "ascii-one-line" / f"{abbr}.xml",
            [(abbr, book_id, verses)],
            edition_label=label,
        )
    write_tei(
        edition_dir / "tei" / "ascii-one-line" / "BYZ" / "byz.xml",
        books,
        combined=True,
        edition_label=label,
    )


EXPORT_NOTES = {
    "official": "`csv/` and `tei/` are unaccented main-text exports generated from the official ASCII. `source/ccat` holds the official `.CCT` source; the published PDF is the ultimate source of truth.",
    "historical": "`csv/main` and `tei/no-accents` are the historical released artifacts recovered from `v2.0.3`.",
    "current": "`csv/main` and `tei/no-accents` are copied from the current working tree (accented CCAT no-variants CSV and unaccented TEI).",
}


def _readme(edition: dict) -> str:
    lines = [
        f"# {edition['id']} - {edition['title']}",
        "",
        f"- **Status:** {edition['status']}",
        f"- **Basis:** {edition['basis']}",
    ]
    if edition["release_range"]:
        lines.append(
            f"- **Repo releases:** `{edition['first_release']}` to "
            f"`{edition['latest_release']}`"
        )
    else:
        lines.append("- **Repo releases:** none (official print edition)")
    if edition["pdf"]:
        lines.append(
            f"- **Official PDF:** [`{Path(edition['pdf']).name}`]"
            f"({edition['pdf_url']})"
        )
    lines.extend(
        [
            "",
            "## Layout",
            "",
            "- `source/` - frozen source files",
            "- `csv/` - generated Unicode CSV",
            "- `tei/` - generated TEI-XML main text",
            "- `manifest.json` - provenance and hashes",
            "",
            EXPORT_NOTES[edition["source_kind"]],
            "",
            "Curated CSV/TEI filenames use the current book abbreviations",
            "(`MAT`, `MAR`, ...). Historical source files may use the older",
            "official codes (`MT`, `MR`, ...).",
            "",
            "## Notes",
            "",
            edition.get("note", ""),
            "",
        ]
    )
    return "\n".join(lines)


def write_manifest(edition: dict) -> dict:
    root = editions.edition_dir(edition["id"])
    manifest = {
        "edition": edition["id"],
        "title": edition["title"],
        "status": edition["status"],
        "basis": edition["basis"],
        "release_range": edition["release_range"],
        "first_release": edition["first_release"],
        "latest_release": edition["latest_release"],
        "pdf": edition["pdf"],
        "pdf_url": edition["pdf_url"],
        "generated_by": "python3 scripts/build_editions.py",
        "source_files": _hash_tree(root / "source", root),
        "artifact_files": _hash_tree(root / "csv", root)
        + _hash_tree(root / "tei", root),
    }
    if edition["pdf"]:
        pdf_path = editions.ROOT / edition["pdf"]
        manifest["pdf_sha256"] = _sha256(pdf_path)
        manifest["pdf_size"] = pdf_path.stat().st_size
    if edition["source_kind"] == "official":
        manifest["ascii_source"] = edition["ascii_dir"]
        manifest["preformatted_source"] = edition["preformatted_dir"]
    (root / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (root / "README.md").write_text(_readme(edition), encoding="utf-8")
    return manifest


def build_all() -> list:
    recover.recover_all()
    built = []
    for edition_id in editions.EDITIONS:
        edition = editions.metadata(edition_id)
        if edition["source_kind"] == "official":
            build_official(edition)
        built.append(write_manifest(edition))
    return built
