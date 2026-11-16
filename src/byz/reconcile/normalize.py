"""Normalization for comparing the official archives with the current corpus."""

import re

VERSE_RE = re.compile(r"^(\d{2}):(\d{2})(?:\s(.*))?$")
ASCII_VERSE_RE = re.compile(r"^\s*(\d+):(\d+)\s?(.*)$")
VARIANT_CODE_RE = re.compile(r"^\{\s*[NBCMSE]$")

GREEK_TO_BETA = {
    "α": "a",
    "β": "b",
    "γ": "g",
    "δ": "d",
    "ε": "e",
    "ζ": "z",
    "η": "h",
    "θ": "q",
    "ι": "i",
    "κ": "k",
    "λ": "l",
    "μ": "m",
    "ν": "n",
    "ξ": "c",
    "ο": "o",
    "π": "p",
    "ρ": "r",
    "σ": "s",
    "ς": "s",
    "τ": "t",
    "υ": "u",
    "φ": "f",
    "χ": "x",
    "ψ": "y",
    "ω": "w",
}

# The ASCII exports use a different transliteration from the .CCT Beta code:
# final sigma is `v`, theta is `y`, chi is `c`, psi is `q`, xi is `x`.
ASCII_TO_BETA = {"v": "s", "y": "q", "c": "x", "q": "y", "x": "c"}


def _canonicalize_token(token: str) -> str:
    if "*" in token and "[" in token:
        without_star = token.replace("*", "", 1)
        prefix_len = len(without_star) - len(without_star.lstrip("["))
        if prefix_len:
            return (
                without_star[:prefix_len]
                + "*"
                + without_star[prefix_len:]
            )
    return token


def normalize_spacing(text: str, reorder_iota: bool = True) -> str:
    text = text.replace("\r", "")
    text = re.sub(r"\s*\.\.\.\s*", " ... ", text)
    text = re.sub(r"\s*>\s*", " > ", text)
    text = re.sub(r"\[\s+", "[", text)
    text = re.sub(r"\s+\]", "]", text)
    text = re.sub(r"\s*-\s*", " - ", text)
    if reorder_iota:
        # Comparison only: align the official iota-subscript ordering with the
        # repository's current convention. Production conversion must not use
        # this (it would corrupt the accented text).
        text = re.sub(r"\|([A-Z])", r"\1|", text)
    text = re.sub(r" +", " ", text)
    return text.strip()


def official_ccat_line(line: str, reorder_iota: bool = True) -> str:
    line = line.strip()
    line = line.replace("{P}", "? ")
    tokens = []
    for token in line.split(" "):
        if not token:
            continue
        if VARIANT_CODE_RE.match(token) or token.startswith("*"):
            tokens.append(_canonicalize_token(token))
            continue
        marked = "*" + token if re.search(r"[A-Z]", token) else token
        tokens.append(_canonicalize_token(marked))
    line = " ".join(tokens).upper().replace("^", "=")
    return normalize_spacing(line, reorder_iota=reorder_iota)


def current_ccat_line(line: str) -> str:
    tokens = [_canonicalize_token(token) for token in line.strip().split(" ")]
    return normalize_spacing(" ".join(tokens))


def parse_cct(text: str) -> dict:
    verses = {}
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        normalized = official_ccat_line(line)
        match = VERSE_RE.match(normalized)
        if not match:
            continue
        key = (int(match.group(1)), int(match.group(2)))
        verses[key] = match.group(3) or ""
    return verses


def parse_current_ccat(text: str) -> dict:
    verses = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        normalized = current_ccat_line(line)
        match = VERSE_RE.match(normalized)
        if not match:
            continue
        key = (int(match.group(1)), int(match.group(2)))
        verses[key] = match.group(3) or ""
    return verses


def transliterate_greek(text: str) -> str:
    output = []
    for char in text:
        if char in GREEK_TO_BETA:
            output.append(GREEK_TO_BETA[char])
        elif char in " \n\r\t":
            output.append(char)
        elif char in "¶.,:;·":
            output.append(" ")
    return re.sub(r" +", " ", "".join(output)).strip()


def map_official_ascii(text: str) -> str:
    return "".join(ASCII_TO_BETA.get(char, char) for char in text)


def parse_ascii(text: str) -> dict:
    verses = {}
    current = None
    for line in text.splitlines():
        match = ASCII_VERSE_RE.match(line)
        if match:
            current = (int(match.group(1)), int(match.group(2)))
            verses[current] = match.group(3).strip()
        elif current is not None and line.strip():
            verses[current] = (verses[current] + " " + line.strip()).strip()
    return {
        key: map_official_ascii(re.sub(r" +", " ", value).strip())
        for key, value in verses.items()
    }
