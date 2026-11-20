"""Build curated CSV/TEI exports and manifests for every edition."""

import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from byz import generated
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
# The parsed Strong's source line format is `NN.NN` (dot, not the CCAT colon).
BP5_RE = re.compile(r"^(\d{2})\.(\d{2})(?:\s(.*))?$")

# The retired convenience pipeline rendered two book titles with typos in the
# unaccented TEI ("Second Timoty", "Phillipians"). The committed
# `editions/rp2018-2023/tei/unaccented/` files carry them, and byte identity is
# the hard gate for this edition, so the build keeps them for that view only.
# The accented TEI (and every other edition) uses `editions.BOOK_NAMES`.
LEGACY_UNACCENTED_BOOK_NAMES = {
    **editions.BOOK_NAMES,
    "2TI": "Second Timoty",
    "PHP": "Phillipians",
}

# The current `source/CCAT` reader is a port of the retired CSV converter:
# `NN:NN` is stripped and the rest goes through `standardise_beta_code` and
# `convert_beta_to_unicode` (no production normalisation, which is for the
# mixed-case official `.CCT` archives).
CURRENT_VERSE_RE = re.compile(r"[0-9]+:[0-9]+")


def parse_cct_current(path: Path, drop_variants: bool) -> dict:
    """Convert one all-lowercase `source/CCAT` file to Unicode text.

    This reader serves only the current `source/CCAT` dialect. The official
    mixed-case `.CCT` archives need `parse_cct_accented`, which normalises case
    and apparatus markup; the two readers are not interchangeable.

    The legacy converter's reader and conversion calls are reproduced exactly,
    including the `? ` -> paragraph-marker rewrite, because the committed
    `csv/accented/` views must stay byte-identical.
    """
    buc = _buc()
    verses = {}
    for number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        line = raw_line.strip()
        if not line:
            continue
        # `CURRENT_VERSE_RE` is unanchored, so an in-text `1:1` would make the
        # `sub()` below truncate the verse. Demand exactly one reference and
        # name the file and line otherwise; every current source line has one.
        matches = list(CURRENT_VERSE_RE.finditer(line))
        if len(matches) != 1:
            raise ValueError(
                f"expected exactly one chapter:verse reference in "
                f"{path.name}:{number}: {line[:80]!r} "
                f"(found {len(matches)})"
            )
        match = matches[0]
        chapter, verse = (int(part) for part in match.group(0).split(":"))
        body = CURRENT_VERSE_RE.sub("", line).strip()
        beta = buc.standardise_beta_code(body, drop_variants)
        text = buc.convert_beta_to_unicode(beta)
        verses[(chapter, verse)] = text.replace("? ", "¶")
    return verses


# Source filenames carry the number prefix and the current book abbreviation:
# `01_MAT.TXT` or `04a_PA.TXT`.
SOURCE_NAME_RE = re.compile(r"^(\d{2}a?)_([A-Z0-9]+)\.(?:TXT|BP5)$")
PAREN_REF_RE = re.compile(r"\((\d+):(\d+)\)")

EXPORT_NOTES = {
    "official": "Accented CSV (with/without variants) and accented TEI are generated from the official `.CCT` source. Unaccented CSV and TEI are generated from the official ASCII. Strong's and parsing are not included because the official archives do not contain them.",
    "historical": "Accented with/without variants, unaccented, Strong's with/no parsing, and accented/unaccented TEI are recovered or generated from `v2.0.3`. The historical `parsed` source includes apparatus markup; the Strong's views use the main text only.",
    "current": "Accented with/without variants, unaccented, Strong's with/no parsing, and accented/unaccented TEI are generated from the edition's own `source/` snapshot.",
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
    if result.returncode != 0:
        raise ValueError(f"cannot resolve git tag {tag!r}")
    return result.stdout.strip()


def _last_commit(*paths: str) -> str:
    result = subprocess.run(
        [
            "git",
            "-C",
            str(editions.ROOT),
            "log",
            "-1",
            "--format=%H",
            "--",
            *paths,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise ValueError(f"cannot resolve last commit for {paths!r}")
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


def _abbr_for(path: Path) -> str:
    """Return the current book abbreviation for a source file name.

    A source file is named `NN_ABBR.TXT` or `NNx_ABBR.BP5`; the prefix and the
    abbreviation must agree with `paths.NUM_TO_ABBR`. Anything else is a loud
    failure, never a silent skip, so a new book cannot be dropped from a view.
    """
    match = SOURCE_NAME_RE.match(path.name)
    if not match:
        raise ValueError(f"unknown source filename: {path}")
    num, abbr = match.groups()
    if paths.NUM_TO_ABBR.get(num) != abbr:
        raise ValueError(
            f"unknown book in {path}: abbreviation {abbr!r} does not match "
            f"number prefix {num!r}"
        )
    return abbr


def _check_source_books(files, expected, source_label: str, edition_id: str) -> None:
    """Fail loudly unless `files` holds exactly the expected book set.

    A missing source file would otherwise shrink a view silently. The error
    names the edition, the source directory, and every missing/unexpected book.
    """
    found = {}
    for path in files:
        abbr = _abbr_for(path)
        if abbr in found:
            raise ValueError(
                f"{edition_id} {source_label} contains book {abbr} twice: "
                f"{found[abbr].name} and {path.name}"
            )
        found[abbr] = path
    missing = sorted(set(expected) - set(found))
    unexpected = sorted(set(found) - set(expected))
    if missing or unexpected:
        details = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if unexpected:
            details.append("unexpected " + ", ".join(unexpected))
        raise ValueError(
            f"{edition_id} {source_label} does not contain the canonical book "
            f"set: {'; '.join(details)}"
        )


def parse_cct_accented(path: Path, drop_variants: bool) -> dict:
    """Convert one official mixed-case `.CCT` archive file.

    This reader serves the official 2005/2018 archives (`data/raw/<edition>/`).
    It is not the current-source reader: `production_ccat_line` upper-cases the
    line, so `source/CCAT` must go through `parse_cct_current` instead.
    """
    buc = _buc()
    verses = {}
    for line in path.read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        # The official `.CCT` line carries the quoted apparatus notes in the
        # source's own case and spacing (for example `[[ "shorter ending" ]]`),
        # but `production_ccat_line` upper-cases the line and collapses the
        # spaces around `[[ ]]`. Protect those literals before normalisation so
        # the generated editions reproduce the archive exactly.
        protected, literals = buc.protect_literals(line)
        normalized = normalize.production_ccat_line(protected)
        match = CCT_RE.match(normalized)
        if not match:
            raise ValueError(
                f"unmatched .CCT line in {path.name}: {line[:80]}"
            )
        key = (int(match.group(1)), int(match.group(2)))
        body = match.group(3) or ""
        body = buc.standardise_beta_code(body, drop_variants=drop_variants)
        text = buc.convert_beta_to_unicode(body)
        # The inherited historical converter unconditionally rewrites `ς -` to
        # `ς-`, which is right for the historical converter output but wrong for
        # the official `.CCT` text: its main text contains no attached dashes at
        # all, and a genuinely attached source dash renders with a *medial*
        # sigma (`σ-`), never `ς-`. So every `ς-` followed by whitespace or the
        # end of the verse came from a spaced source dash. Restore it here only,
        # in the production path, so the historical pipeline and the recovered
        # `v2.0.3` views are not touched.
        text = re.sub(r"ς-(?=\s|$)", "ς -", text)
        text = buc.restore_literals(text, literals)
        verses[key] = text.replace("? ", "¶")
    return verses


def parse_bp5_strongs(path: Path) -> tuple:
    """Return (with_parsing, without_parsing) for one `source/Strongs` file.

    This is the port of the `.BP5` reader that used to live in the retired CSV
    converter; the conversion rules stay in the shared
    `beta_to_unicode_custom` module. `drop_parsing=True` keeps the Strong's
    numbers and drops the morphology, which is the `strongs/no-parsing` and
    `csv/unaccented` view.
    """
    buc = _buc()
    with_parsing = {}
    without_parsing = {}
    for lineno, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        if not line.strip():
            continue
        match = BP5_RE.match(line)
        if not match:
            raise ValueError(
                f"unmatched .BP5 line in {path.name}:{lineno}: {line[:80]}"
            )
        key = (int(match.group(1)), int(match.group(2)))
        body = (match.group(3) or "").strip()
        with_parsing[key] = buc.convert_beta_to_unicode_strongs(body, False)
        without_parsing[key] = buc.convert_beta_to_unicode_strongs(body, True)
    return with_parsing, without_parsing


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
                    # The parsed files carry Strong's + TVM numbers, and use
                    # "0" as a spurious-Strong's marker. Keep the real Strong's
                    # number and the parsing; drop the TVM number.
                    strongs = next(
                        (number for number in numbers if number != "0"), "0"
                    )
                    pairs.append((strongs, parsing))
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
        # Generated CSV uses Unix line endings everywhere. Copied historical and
        # current views keep whatever the source artifact used.
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["chapter", "verse", "text"])
        for chapter, verse in sorted(verses):
            writer.writerow([chapter, verse, verses[(chapter, verse)]])


def _tei_tokens(text: str):
    """Split a verse into TEI tokens, yielding None for a paragraph marker."""
    for token in text.split(" "):
        while token.startswith("¶"):
            yield None
            token = token[1:]
        if token:
            yield token


def _tei_token(token: str) -> str:
    if not any(char.isalnum() for char in token):
        # Standalone punctuation: the official text uses a bare `-` as a
        # punctuation/deletion mark, not as a word. Emit it as TEI punctuation.
        return f"<pc>{token}</pc>"
    return f"<w>{token}</w>"


def _tei_verse(book_id: str, chapter: int, verse: int, text: str) -> str:
    anchor = f"{book_id}K{chapter}V{verse}"
    if not text:
        return f'\t\t\t\t\t<ab n="{anchor}"/>'
    items = []
    for token in _tei_tokens(text):
        if token is None:
            items.append('<milestone unit="paragraph" type="start"/>')
        else:
            items.append(_tei_token(token))
    words = "\n".join(f"\t\t\t\t\t\t{item}" for item in items)
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
    path: Path,
    books: list,
    combined: bool = False,
    edition_label: str = "",
    book_names: dict | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    template = _header_template()
    names = book_names or editions.BOOK_NAMES
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
        # `book_names` only feeds the per-book `<title>` metadata below. The
        # combined file has no per-book title block, so a caller-supplied
        # spelling must not leak into it; assert that so a template change
        # cannot reintroduce mixed spellings.
        prefix = template.replace("BOOK_METADATA_PLACEHOLDER", "")
        if '<title type="work"' in prefix or '<title type="short"' in prefix:
            raise ValueError("combined TEI header must not carry per-book titles")
    else:
        abbr, book_id, _ = books[0]
        num = paths.ABBR_TO_NUM[abbr]
        metadata = (
            f'\n\t\t\t\t<title type="work" level="m" xml:lang="en" n="{num}">'
            f"{names[abbr]}</title>\n"
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


def write_accented_tei(edition: dict, edition_dir: Path | None = None) -> None:
    edition_dir = edition_dir or editions.edition_dir(edition["id"])
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


def build_current(edition: dict, edition_dir: Path | None = None) -> None:
    """Generate every `rp2018-2023` view from the edition's `source/` snapshot.

    The edition owns its inputs (`editions/<id>/source/`), so this function
    reads nothing from the working-tree `source/` and nothing from a retired
    convenience tree. The write order and the two book orders are load-bearing:
    the unaccented TEI is written without an edition label and in canonical
    order, while ``write_accented_tei`` keeps its alphabetical order and its
    curated label. Changing either would change committed edition bytes.
    """
    edition_dir = edition_dir or editions.edition_dir(edition["id"])
    source = edition_dir / "source"
    ccat_source = source / "CCAT"
    strongs_source = source / "Strongs"
    if not ccat_source.is_dir():
        raise ValueError(f"missing CCAT source directory: {ccat_source}")
    if not strongs_source.is_dir():
        raise ValueError(f"missing Strong's source directory: {strongs_source}")

    ccat_files = sorted(ccat_source.glob("*.TXT"))
    _check_source_books(
        ccat_files,
        paths.CANONICAL_BOOKS + paths.SECTION_ABBRS,
        "source/CCAT",
        edition["id"],
    )
    bp5_files = sorted(strongs_source.glob("*.BP5"))
    _check_source_books(
        bp5_files,
        paths.CANONICAL_BOOKS,
        "source/Strongs",
        edition["id"],
    )

    for cct_file in ccat_files:
        abbr = _abbr_for(cct_file)
        write_csv(
            edition_dir / "csv" / "accented" / "no-variants" / f"{abbr}.csv",
            parse_cct_current(cct_file, drop_variants=True),
        )
        write_csv(
            edition_dir / "csv" / "accented" / "with-variants" / f"{abbr}.csv",
            parse_cct_current(cct_file, drop_variants=False),
        )

    books = []
    for bp5_file in bp5_files:
        abbr = _abbr_for(bp5_file)
        with_parsing, no_parsing = parse_bp5_strongs(bp5_file)
        write_csv(
            edition_dir / "csv" / "strongs" / "with-parsing" / f"{abbr}.csv",
            with_parsing,
        )
        write_csv(
            edition_dir / "csv" / "strongs" / "no-parsing" / f"{abbr}.csv",
            no_parsing,
        )
        # `csv/unaccented` is the same dict, not a second conversion: the two
        # views are two names for one text (locked by a test).
        write_csv(edition_dir / "csv" / "unaccented" / f"{abbr}.csv", no_parsing)
        books.append((abbr, paths.ABBR_TO_BOOK_ID[abbr], no_parsing))

    books.sort(key=lambda item: editions.BOOK_ORDER.index(item[0]))
    for abbr, book_id, verses in books:
        write_tei(
            edition_dir / "tei" / "unaccented" / f"{abbr}.xml",
            [(abbr, book_id, verses)],
            book_names=LEGACY_UNACCENTED_BOOK_NAMES,
        )
    write_tei(
        edition_dir / "tei" / "unaccented" / "BYZ" / "byz.xml",
        books,
        combined=True,
    )
    write_accented_tei(edition, edition_dir=edition_dir)


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
        # This README lives at editions/<id>/README.md, two levels below the
        # repository root, so the committed PDF is linked relative to it.
        lines.append(
            f"- **Official PDF:** [`{Path(edition['pdf']).name}`]"
            f"(../../{edition['pdf']})"
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
            "`source/` is a frozen copy of the edition's inputs, so the edition",
            "can be downloaded and verified on its own.",
        ]
    )
    if edition["source_kind"] == "current":
        lines.extend(
            [
                "",
                "For `rp2018-2023` this `source/` snapshot intentionally",
                "duplicates the repository `source/`.",
                "",
                "`csv/unaccented/` and `csv/strongs/no-parsing/` hold the same",
                "bytes because they are two names for one text: the plain",
                "Unicode text and the Strong's view with parsing dropped. The",
                "duplication is intentional, and a test asserts the identity.",
            ]
        )
    lines.extend(
        [
            "",
            "## Derived artifacts",
            "",
        ]
    )
    for path in _artifact_dirs(root):
        lines.append(f"- `{path}`")
    note = edition.get("note", "")
    if note:
        lines.extend(["", "## Notes", "", note])
    lines.append("")
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
    if edition["source_kind"] == "current":
        # The Greek text and the Strong's/parsing data have separate lineages.
        # Restrict each lookup to its data directory so that documentation
        # pointers such as `source/README.md` never masquerade as a text change.
        manifest["source_commit"] = _last_commit("source/CCAT")
        manifest["strongs_commit"] = _last_commit("source/Strongs")
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
    generated.write_markdown(root / "README.md", _readme(edition))
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
