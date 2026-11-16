"""Build curated CSV/TEI exports and manifests for every edition."""

import csv
import hashlib
import json
import re
import subprocess
import sys
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

UB5_TO_GREEK = dict(ASCII_TO_GREEK)
UB5_TO_GREEK["q"] = "θ"
UB5_TO_GREEK["y"] = "ψ"

VERSE_RE = re.compile(r"^\s*(\d+):(\d+)\s?(.*)$")
CCT_RE = re.compile(r"^(\d{2}):(\d{2})(?:\s(.*))?$")
PAREN_REF_RE = re.compile(r"\((\d+):(\d+)\)")

EXPORT_NOTES = {
    "official": "Accented CSV (with/without variants) and accented TEI are generated from the official `.CCT` source. Unaccented CSV and TEI are generated from the official ASCII. Strong's and parsing are not included because the official archives do not contain them.",
    "historical": "Accented with/without variants, unaccented, Strong's with/no parsing, and accented/unaccented TEI are recovered or generated from `v2.0.3`. The historical `parsed` source includes apparatus markup; the Strong's views use the main text only.",
    "current": "Accented with/without variants, unaccented, Strong's with/no parsing, and accented/unaccented TEI are copied or generated from the current working tree.",
}


def ascii_to_greek(text: str) -> str:
    return "".join(ASCII_TO_GREEK.get(char, char) for char in text)


def _git_commit(tag: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(editions.ROOT), "rev-parse", f"{tag}^{{commit}}"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


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


def parse_ascii_main(path: Path) -> dict:
    verses = {}
    for line in path.read_text().splitlines():
        match = VERSE_RE.match(line)
        if not match:
            if line.strip():
                raise ValueError(
                    f"unmatched ASCII line in {path.name}: {line[:80]}"
                )
            continue
        key = (int(match.group(1)), int(match.group(2)))
        verses[key] = ascii_to_greek(match.group(3).strip())
    return verses


def _buc():
    scripts = str(editions.ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import beta_to_unicode_custom.beta_to_unicode_custom as buc

    return buc


def parse_cct_accented(path: Path, drop_variants: bool) -> dict:
    buc = _buc()
    verses = {}
    for line in path.read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        normalized = normalize.official_ccat_line(line, reorder_iota=False)
        match = CCT_RE.match(normalized)
        if not match:
            raise ValueError(
                f"unmatched .CCT line in {path.name}: {line[:80]}"
            )
        key = (int(match.group(1)), int(match.group(2)))
        body = match.group(3) or ""
        body = buc.standardise_beta_code(body, drop_variants=drop_variants)
        text = buc.convert_beta_to_unicode(body)
        verses[key] = text.replace("? ", "¶")
    return verses


def ub5_to_greek(text: str) -> str:
    greek = "".join(UB5_TO_GREEK.get(char, char) for char in text)
    if greek.endswith("σ"):
        greek = greek[:-1] + "ς"
    return greek


def _sanitize_ub5(text: str, label: str) -> str:
    # Remove <word> plus the numbers/parsing that belong to the apparatus lemma.
    text = re.sub(r"<[^>]+>(?:\s+\d+)*(?:\s+\{[^}]*\})*", " ", text)
    # Remove variant blocks and their separators.
    text = re.sub(r"(?:VAR|OR):?.*?:END", " ", text)
    text = re.sub(r"M5:.*?:M5|M6:.*?:M6", " ", text)
    text = re.sub(r"\|", " ", text)
    text = re.sub(r"\b(?:OMIT|M5:|M6:)\b", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    if re.search(r"[|<>]|VAR:|:END", text):
        raise ValueError(f"unparsed apparatus markup in {label}: {text[:120]}")
    return text


def _parse_ub5_text(text: str, label: str) -> tuple:
    tokens = text.split()
    parsed = []
    text_only = []
    index = 0
    while index < len(tokens):
        word = tokens[index]
        index += 1
        if word.isdigit() or word.startswith("{"):
            raise ValueError(f"unexpected token {word!r} in {label}")
        greek = ub5_to_greek(word)
        text_only.append(greek)
        pairs = []
        while index < len(tokens):
            numbers = []
            lookahead = index
            while lookahead < len(tokens) and tokens[lookahead].isdigit():
                numbers.append(tokens[lookahead])
                lookahead += 1
            if (
                lookahead < len(tokens)
                and tokens[lookahead].startswith("{")
                and tokens[lookahead].endswith("}")
            ):
                parsing = tokens[lookahead]
                if numbers:
                    # The parsed files carry Strong's + TVM numbers. Keep the
                    # Strong's number and the parsing; drop the TVM number.
                    pairs.append((numbers[0], parsing))
                index = lookahead + 1
                if index < len(tokens) and tokens[index].isdigit():
                    continue
                break
            break
        if pairs:
            parsed.append(
                greek + " " + " ".join(f"{strongs} {parsing}" for strongs, parsing in pairs)
            )
        else:
            parsed.append(greek)
    return " ".join(parsed), " ".join(text_only)


def _split_parenthetical_refs(text: str):
    # A leading (chapter:verse) is an alternative numbering note; keep the text.
    text = re.sub(r"^\s*\(\d+:\d+\)\s*", "", text)
    parts = PAREN_REF_RE.split(text)
    base = parts[0]
    segments = []
    index = 1
    while index + 2 < len(parts):
        segments.append(
            ((int(parts[index]), int(parts[index + 1])), parts[index + 2])
        )
        index += 3
    return base, segments

def parse_parsed_ub5(path: Path, reference=None) -> tuple:
    with_parsing = {}
    without_parsing = {}
    prefixes_parsed = {}
    prefixes_text = {}
    verses = {}
    current = None
    for line in path.read_text().splitlines():
        match = VERSE_RE.match(line)
        if match:
            current = (int(match.group(1)), int(match.group(2)))
            verses[current] = match.group(3).strip()
        elif current is not None and line.strip():
            verses[current] = (verses[current] + " " + line.strip()).strip()
    for key, raw in verses.items():
        label = f"{path.name} {key[0]}:{key[1]}"
        sanitized = _sanitize_ub5(raw, label)
        base, segments = _split_parenthetical_refs(sanitized)
        parsed, text_only = _parse_ub5_text(base, label)
        for target_key, segment in segments:
            segment_parsed, segment_text = _parse_ub5_text(
                segment, f"{path.name} {target_key[0]}:{target_key[1]}"
            )
            if not reference or not segment_text:
                continue
            current_ref = reference.get(key, "")
            target_ref = reference.get(target_key, "")
            if segment_text in current_ref:
                parsed = (parsed + " " + segment_parsed).strip()
                text_only = (text_only + " " + segment_text).strip()
            elif segment_text in target_ref:
                prefixes_parsed[target_key] = (
                    prefixes_parsed.get(target_key, "") + " " + segment_parsed
                ).strip()
                prefixes_text[target_key] = (
                    prefixes_text.get(target_key, "") + " " + segment_text
                ).strip()
        if key in with_parsing:
            with_parsing[key] += " " + parsed
            without_parsing[key] += " " + text_only
        else:
            with_parsing[key] = parsed
            without_parsing[key] = text_only
    for key, prefix in prefixes_parsed.items():
        if key in with_parsing:
            with_parsing[key] = (prefix + " " + with_parsing[key]).strip()
            without_parsing[key] = (
                prefixes_text[key] + " " + without_parsing[key]
            ).strip()
    return with_parsing, without_parsing

def write_csv(path: Path, verses: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["chapter", "verse", "text"])
        for chapter, verse in sorted(verses):
            writer.writerow([chapter, verse, verses[(chapter, verse)]])


def _tei_verse(book_id: str, chapter: int, verse: int, text: str) -> str:
    anchor = f"{book_id}K{chapter}V{verse}"
    if not text:
        return f'\t\t\t\t\t<ab n="{anchor}"/>'
    words = "\n".join(f"\t\t\t\t\t\t<w>{word}</w>" for word in text.split(" "))
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
            f'<edition n="{edition_label}">Curated edition</edition>',
            template,
            flags=re.S,
        )
    body = "\n".join(
        _tei_book(abbr, book_id, verses) for abbr, book_id, verses in books
    )
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


def _read_csv_verses(path: Path) -> dict:
    verses = {}
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            verses[(int(row["chapter"]), int(row["verse"]))] = row["text"]
    return verses


def _edition_label(edition: dict) -> str:
    if edition["id"] == "rp2005":
        return "2005"
    if edition["id"] == "rp2005-2019":
        return "2005 (2019 revision)"
    if edition["id"] == "rp2018":
        return "2018"
    return "2018 (2023 revision)"


def write_accented_tei(edition: dict) -> None:
    edition_dir = editions.edition_dir(edition["id"])
    csv_dir = edition_dir / "csv" / "accented" / "no-variants"
    books = []
    for path in sorted(csv_dir.glob("*.csv")):
        abbr = path.stem
        if abbr not in paths.ABBR_TO_BOOK_ID:
            # PA/ACT24 are section exports, not separate TEI books.
            continue
        verses = _read_csv_verses(path)
        book_id = paths.ABBR_TO_BOOK_ID[abbr]
        books.append((abbr, book_id, verses))
        write_tei(
            edition_dir / "tei" / "accented" / f"{abbr}.xml",
            [(abbr, book_id, verses)],
            edition_label=_edition_label(edition),
        )
    write_tei(
        edition_dir / "tei" / "accented" / "BYZ" / "byz.xml",
        books,
        combined=True,
        edition_label=_edition_label(edition),
    )


def build_official(edition: dict) -> None:
    edition_dir = editions.edition_dir(edition["id"])
    ascii_dir = editions.ROOT / edition["ascii_dir"]
    ccat_dir = edition_dir / "source" / "ccat"
    label = _edition_label(edition)
    books = []
    for ascii_file in sorted(ascii_dir.glob("*_Byz.txt")):
        code = ascii_file.name.split("_", 1)[0]
        abbr = sources.OFFICIAL_TO_ABBR.get(code)
        if not abbr:
            continue
        unaccented = parse_ascii_main(ascii_file)
        ccat_file = ccat_dir / f"{code}.CCT"
        if ccat_file.exists():
            for key in parse_cct_accented(ccat_file, drop_variants=True):
                unaccented.setdefault(key, "")
        write_csv(edition_dir / "csv" / "unaccented" / f"{abbr}.csv", unaccented)
        book_id = paths.ABBR_TO_BOOK_ID[abbr]
        books.append((abbr, book_id, unaccented))
        if ccat_file.exists():
            write_csv(
                edition_dir / "csv" / "accented" / "no-variants" / f"{abbr}.csv",
                parse_cct_accented(ccat_file, drop_variants=True),
            )
            write_csv(
                edition_dir / "csv" / "accented" / "with-variants" / f"{abbr}.csv",
                parse_cct_accented(ccat_file, drop_variants=False),
            )
    processed = {abbr for abbr, _, _ in books}
    for cct_file in sorted(ccat_dir.glob("*.CCT")):
        if cct_file.stem.upper() == "GREEK":
            continue
        abbr = sources.OFFICIAL_TO_ABBR.get(cct_file.stem.upper())
        if not abbr or abbr in processed:
            continue
        # Longer alternative sections (PA/ACT24) have no separate ASCII book,
        # but they are part of the accented CCAT source.
        write_csv(
            edition_dir / "csv" / "accented" / "no-variants" / f"{abbr}.csv",
            parse_cct_accented(cct_file, drop_variants=True),
        )
        write_csv(
            edition_dir / "csv" / "accented" / "with-variants" / f"{abbr}.csv",
            parse_cct_accented(cct_file, drop_variants=False),
        )
    for abbr, book_id, verses in books:
        write_tei(
            edition_dir / "tei" / "unaccented" / f"{abbr}.xml",
            [(abbr, book_id, verses)],
            edition_label=label,
        )
    write_tei(
        edition_dir / "tei" / "unaccented" / "BYZ" / "byz.xml",
        books,
        combined=True,
        edition_label=label,
    )
    write_accented_tei(edition)


def build_historical(edition: dict) -> None:
    edition_dir = editions.edition_dir(edition["id"])
    parsed_dir = edition_dir / "source" / "parsed"
    for path in sorted(parsed_dir.glob("*.UB5")):
        abbr = sources.OFFICIAL_TO_ABBR.get(path.stem.upper())
        if not abbr:
            continue
        reference_path = (
            edition_dir / "csv" / "unaccented" / f"{abbr}.csv"
        )
        reference = (
            _read_csv_verses(reference_path) if reference_path.exists() else {}
        )
        with_parsing, without_parsing = parse_parsed_ub5(
            path, reference=reference
        )
        write_csv(
            edition_dir / "csv" / "strongs" / "with-parsing" / f"{abbr}.csv",
            with_parsing,
        )
        write_csv(
            edition_dir / "csv" / "strongs" / "no-parsing" / f"{abbr}.csv",
            without_parsing,
        )
    write_accented_tei(edition)


def build_current(edition: dict) -> None:
    write_accented_tei(edition)


def _artifact_dirs(root: Path) -> list:
    dirs = set()
    for base in ("csv", "tei"):
        for path in (root / base).rglob("*"):
            if path.is_dir() and any(path.iterdir()):
                dirs.add(str(path.relative_to(root)))
    return sorted(dirs)


def _readme(edition: dict) -> str:
    root = editions.edition_dir(edition["id"])
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
            "- `tei/` - generated TEI-XML",
            "- `manifest.json` - provenance and hashes",
            "",
            EXPORT_NOTES[edition["source_kind"]],
            "",
            "Curated CSV/TEI filenames use the current book abbreviations",
            "(`MAT`, `MAR`, ...). Historical source files may use the older",
            "official codes (`MT`, `MR`, ...).",
            "",
            "## Derived artifacts",
            "",
        ]
    )
    for path in _artifact_dirs(root):
        lines.append(f"- `{path}`")
    lines.extend(["", "## Notes", "", edition.get("note", ""), ""])
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
    if edition.get("tag"):
        manifest["tag"] = edition["tag"]
        manifest["commit"] = _git_commit(edition["tag"])
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
        elif edition["source_kind"] == "historical":
            build_historical(edition)
        else:
            build_current(edition)
        built.append(write_manifest(edition))
    return built
