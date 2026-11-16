"""Compare the official archives with the current corpus."""

import csv
import io
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from byz.contract import paths
from byz.contract.ccat import book_num
from byz.contract.encoding import decode, detect_encoding

from . import archive, normalize, sources

TEI_NS = "http://www.tei-c.org/ns/1.0"
VARIANT_CODE_RE = re.compile(r"\{([NBCMSE])")
PUNCTUATION = set(".,:;·!?")
ACCENTS = set("\\/()|+=~")


def _main_text(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"\{[^}]*\}", "", text)).strip()


def classify_diff(current: str, official: str) -> str:
    if current == official:
        return ""
    if not current or not official:
        return "missing"
    cur_codes = VARIANT_CODE_RE.findall(current)
    off_codes = VARIANT_CODE_RE.findall(official)
    if _main_text(current) == _main_text(official):
        if cur_codes == off_codes:
            return "variant"
        without = lambda text: VARIANT_CODE_RE.sub("{", text)
        if without(current) == without(official):
            return "variant-code"
        return "variant"
    if cur_codes != off_codes:
        without = lambda text: VARIANT_CODE_RE.sub("{", text)
        if without(current) == without(official):
            return "variant-code"
    if current.replace("*", "") == official.replace("*", ""):
        return "capitalization"
    if current.replace(" ", "") == official.replace(" ", ""):
        return "word-segmentation"
    if re.sub(r"\s+", "", current) == re.sub(r"\s+", "", official):
        return "whitespace"
    if "".join(ch for ch in current if ch not in PUNCTUATION) == "".join(
        ch for ch in official if ch not in PUNCTUATION
    ):
        return "punctuation"
    if "".join(ch for ch in current if ch not in ACCENTS) == "".join(
        ch for ch in official if ch not in ACCENTS
    ):
        return "accents-breathings"
    return "letters"


def compare_maps(current: dict, official: dict) -> dict:
    keys = set(current) | set(official)
    match = 0
    differences = []
    for key in sorted(keys):
        cur = current.get(key)
        off = official.get(key)
        if cur == off:
            match += 1
            continue
        category = classify_diff(cur or "", off or "")
        differences.append(
            {
                "chapter": key[0],
                "verse": key[1],
                "category": category,
                "current": cur or "",
                "official": off or "",
            }
        )
    return {
        "keys_current": len(current),
        "keys_official": len(official),
        "verses": len(keys),
        "verses_match": match,
        "verses_diff": len(differences),
        "only_current": len(set(current) - set(official)),
        "only_official": len(set(official) - set(current)),
        "differences": differences,
    }


def _decode_member(data: bytes) -> str:
    return decode(data, detect_encoding(data))


def _ccat_members(edition: str) -> dict:
    spec = next(
        item
        for item in sources.ARCHIVES
        if item["edition"] == edition and item["format"] == "ccat"
    )
    path = sources.ARCHIVE_DIR / edition / spec["name"]
    return {
        name: _decode_member(data)
        for name, data in archive.load_members(path).items()
        if name.lower().endswith(".cct")
    }


def _ascii_members(edition: str, ascii_format: str) -> dict:
    spec = next(
        item
        for item in sources.ARCHIVES
        if item["edition"] == edition and item["format"] == ascii_format
    )
    path = sources.ARCHIVE_DIR / edition / spec["name"]
    return {
        name: _decode_member(data) for name, data in archive.load_members(path).items()
    }


def source_rows() -> tuple[list, list, list]:
    file_rows = []
    verse_rows = []
    blank_rows = []
    for edition in ("rp2005", "rp2018"):
        members = _ccat_members(edition)
        for current_path in sorted((sources.ROOT / "source" / "CCAT").glob("*.TXT")):
            num = book_num(current_path)
            abbr = paths.NUM_TO_ABBR.get(num, num)
            official_code = sources.ABBR_TO_OFFICIAL.get(abbr)
            member = f"{official_code}.CCT" if official_code else ""
            if member not in members:
                file_rows.append(
                    {
                        "tier": "source",
                        "edition": edition,
                        "dataset": "source/CCAT",
                        "current": str(current_path.relative_to(sources.ROOT)),
                        "archive_member": member,
                        "class": "missing",
                        "verses": 0,
                        "verses_match": 0,
                        "verses_diff": 0,
                        "note": "official member not found",
                    }
                )
                continue
            current_text = _decode_member(current_path.read_bytes())
            current = normalize.parse_current_ccat(current_text)
            official = normalize.parse_cct(members[member])
            metrics = compare_maps(current, official)
            if metrics["verses_diff"] == 0 and metrics["only_current"] == 0 and metrics["only_official"] == 0:
                match_class = "normalized"
            elif metrics["only_current"] or metrics["only_official"]:
                match_class = "structural"
            else:
                match_class = "textual"
            file_rows.append(
                {
                    "tier": "source",
                    "edition": edition,
                    "dataset": "source/CCAT",
                    "current": str(current_path.relative_to(sources.ROOT)),
                    "archive_member": f"{edition}/{member}",
                    "class": match_class,
                    "verses": metrics["verses"],
                    "verses_match": metrics["verses_match"],
                    "verses_diff": metrics["verses_diff"],
                    "note": "",
                }
            )
            for diff in metrics["differences"]:
                verse_rows.append(
                    {
                        "tier": "source",
                        "edition": edition,
                        "dataset": "source/CCAT",
                        "current": str(current_path.relative_to(sources.ROOT)),
                        "book": abbr,
                        "chapter": diff["chapter"],
                        "verse": diff["verse"],
                        "category": diff["category"],
                        "current_text": diff["current"],
                        "official_text": diff["official"],
                    }
                )
            if abbr in ("LUK", "ACT"):
                for blank_book, chapter, verse in sources.INTENTIONAL_BLANKS:
                    if blank_book != abbr:
                        continue
                    official_body = official.get((chapter, verse))
                    blank_rows.append(
                        {
                            "edition": edition,
                            "book": abbr,
                            "chapter": chapter,
                            "verse": verse,
                            "in_official_ccat": (chapter, verse) in official,
                            "official_blank": official_body == "",
                        }
                    )
    return file_rows, verse_rows, blank_rows


def _load_current_csv(abbr: str) -> dict:
    path = (
        sources.ROOT
        / "csv-unicode"
        / "strongs"
        / "no-parsing"
        / f"{abbr}.csv"
    )
    verses = {}
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            text = normalize.transliterate_greek(row["text"])
            verses[(int(row["chapter"]), int(row["verse"]))] = text
    return verses


def _load_current_tei(abbr: str) -> dict:
    path = (
        sources.ROOT / "tei-xml-unicode" / "no-accents" / f"{abbr}.xml"
    )
    tree = ET.parse(path)
    verses = {}
    for ab_element in tree.getroot().iter(f"{{{TEI_NS}}}ab"):
        anchor = ab_element.get("n", "")
        match = re.match(r"^B\d{2}K(\d+)V(\d+)$", anchor)
        if not match:
            continue
        words = [word.text or "" for word in ab_element.findall(f"{{{TEI_NS}}}w")]
        verses[(int(match.group(1)), int(match.group(2)))] = (
            normalize.transliterate_greek(" ".join(words))
        )
    return verses


def derived_rows() -> tuple[list, list]:
    file_rows = []
    verse_rows = []
    for edition in ("rp2005", "rp2018"):
        references = {
            "ascii-one-line": _ascii_members(edition, "ascii-one-line"),
            "preformatted": _ascii_members(edition, "preformatted"),
        }
        for reference_name, members in references.items():
            suffix = "_Byz.txt" if reference_name == "ascii-one-line" else "05.ASC"
            for abbr in paths.CANONICAL_BOOKS:
                official_code = sources.ABBR_TO_OFFICIAL[abbr]
                member = f"{official_code}{suffix}"
                if member not in members:
                    continue
                official = normalize.parse_ascii(members[member])
                for dataset, loader in (
                    ("csv-unicode/strongs/no-parsing", _load_current_csv),
                    ("tei-xml-unicode/no-accents", _load_current_tei),
                ):
                    current = loader(abbr)
                    metrics = compare_maps(current, official)
                    if metrics["verses_diff"] == 0 and metrics["only_current"] == 0 and metrics["only_official"] == 0:
                        match_class = "exact-transliteration"
                    elif metrics["only_current"] or metrics["only_official"]:
                        match_class = "structural"
                    else:
                        match_class = "textual"
                    file_rows.append(
                        {
                            "tier": "derived",
                            "edition": edition,
                            "dataset": dataset,
                            "current": f"{dataset}/{abbr}",
                            "archive_member": f"{edition}/{member}",
                            "class": match_class,
                            "verses": metrics["verses"],
                            "verses_match": metrics["verses_match"],
                            "verses_diff": metrics["verses_diff"],
                            "note": f"reference format: {reference_name}",
                        }
                    )
                    for diff in metrics["differences"]:
                        verse_rows.append(
                            {
                                "tier": "derived",
                                "edition": edition,
                                "dataset": dataset,
                                "current": f"{dataset}/{abbr}",
                                "book": abbr,
                                "chapter": diff["chapter"],
                                "verse": diff["verse"],
                                "category": diff["category"],
                                "current_text": diff["current"],
                                "official_text": diff["official"],
                            }
                        )
    return file_rows, verse_rows


def strongs_provenance() -> dict:
    hits = []
    for spec in sources.ARCHIVES:
        path = sources.ARCHIVE_DIR / spec["edition"] / spec["name"]
        if not path.exists():
            continue
        for name in archive.load_members(path):
            if name.lower().endswith((".bp5", ".b5", ".parse", ".strongs")):
                hits.append(f"{spec['edition']}/{name}")
    return {
        "status": "found" if hits else "provenance-unknown",
        "hits": hits,
    }


def mapping_rows() -> list:
    rows = []
    for path in sorted((sources.ROOT / "source" / "Strongs").glob("*.BP5")):
        rows.append(
            {
                "tier": "mapping",
                "edition": "unknown",
                "dataset": "source/Strongs",
                "current": str(path.relative_to(sources.ROOT)),
                "archive_member": "",
                "class": "provenance-unknown",
                "verses": 0,
                "verses_match": 0,
                "verses_diff": 0,
                "note": "no parsed/Strong's file in the official archives",
            }
        )
    for view in ("no-variants", "with-variants"):
        for path in sorted((sources.ROOT / "csv-unicode" / "ccat" / view).glob("*.csv")):
            rows.append(
                {
                    "tier": "mapping",
                    "edition": "unknown",
                    "dataset": f"csv-unicode/ccat/{view}",
                    "current": str(path.relative_to(sources.ROOT)),
                    "archive_member": "",
                    "class": "incomparable-pending-pipeline",
                    "verses": 0,
                    "verses_match": 0,
                    "verses_diff": 0,
                    "note": "accented CCAT CSV; exact comparison needs the Cycle 3 parser",
                }
            )
    for rel, note in (
        (
            "tei-xml-unicode/no-accents/BYZ/byz.xml",
            "combined file; the per-book TEI files are compared",
        ),
        (
            "tei-xml-unicode/assets/demo_john_1.xml",
            "hand-prepared demo asset",
        ),
    ):
        path = sources.ROOT / rel
        if path.is_file():
            rows.append(
                {
                    "tier": "mapping",
                    "edition": "unknown",
                    "dataset": str(path.parent.relative_to(sources.ROOT)),
                    "current": rel,
                    "archive_member": "",
                    "class": "auxiliary",
                    "verses": 0,
                    "verses_match": 0,
                    "verses_diff": 0,
                    "note": note,
                }
            )
    rows.append(
        {
            "tier": "mapping",
            "edition": "rp2018",
            "dataset": "archive",
            "current": "",
            "archive_member": "rp2018/GREEK.CCT",
            "class": "auxiliary",
            "verses": 0,
            "verses_match": 0,
            "verses_diff": 0,
            "note": "transliteration documentation, not text",
        }
    )
    return rows


def run() -> dict:
    source_file_rows, source_verse_rows, blank_rows = source_rows()
    derived_file_rows, derived_verse_rows = derived_rows()
    return {
        "files": source_file_rows + derived_file_rows + mapping_rows(),
        "verses": source_verse_rows + derived_verse_rows,
        "blanks": blank_rows,
        "strongs": strongs_provenance(),
    }
