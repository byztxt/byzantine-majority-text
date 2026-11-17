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


def _production_token(token: str) -> str:
    """Mark capitalisation from the original mixed-case token.

    The official `.CCT` files are mixed case: an uppercase ASCII letter carries
    the word's capitalisation, while the apparatus codes glued to some tokens
    (`e)/ballon.{B`) must not be interpreted as capitals. Only the word part
    (everything before the first `{`) can be capitalised.
    """
    if VARIANT_CODE_RE.match(token) or token.startswith("*"):
        return _canonicalize_token(token)
    brace = token.find("{")
    if brace == -1:
        word, code = token, ""
    else:
        word, code = token[:brace], token[brace:]
    letters = [char for char in word if char.isascii() and char.isalpha()]
    if len(letters) > 1 and all(char.isupper() for char in letters):
        # An all-uppercase word part is an apparatus abbreviation such as
        # `_DAD`, not a capitalised word. Beta code marks every capital
        # separately, so the converter renders `—ΔΑΔ` instead of `—δαδ`.
        return (
            "".join(
                "*" + char if char.isascii() and char.isalpha() else char
                for char in word
            )
            + code
        )
    if letters and letters[0].isupper():
        # The asterisk must precede leading punctuation and breathings;
        # `_canonicalize_token` then moves it after any leading `[`.
        return _canonicalize_token("*" + token)
    return token


def official_ccat_line(
    line: str, reorder_iota: bool = True, faithful_capitals: bool = False
) -> str:
    line = line.strip()
    line = line.replace("{P}", "? ")
    tokens = []
    for token in line.split(" "):
        if not token:
            continue
        if faithful_capitals:
            tokens.append(_production_token(token))
            continue
        if VARIANT_CODE_RE.match(token) or token.startswith("*"):
            tokens.append(_canonicalize_token(token))
            continue
        marked = "*" + token if re.search(r"[A-Z]", token) else token
        tokens.append(_canonicalize_token(marked))
    line = " ".join(tokens).upper().replace("^", "=")
    if faithful_capitals:
        # The official .CCT puts the iota subscript before the accent (`|/`),
        # but the beta-code library expects the accent first (`/|`). Without
        # this the converter emits a space plus an orphan acute accent
        # (`μιμνῃ ́σκῃ`) instead of `μιμνῄσκῃ`.
        line = re.sub(r"\|([/\\])", r"\1|", line)
    return normalize_spacing(line, reorder_iota=reorder_iota)


def production_ccat_line(line: str) -> str:
    """Convert an official `.CCT` line for production output.

    Unlike `official_ccat_line`, which exists to align the official text with
    the repository's current convention for comparison, this keeps the
    official conventions that the historical converter expects:

    - capitals are read from the original mixed-case token, so glued apparatus
      codes are not mistaken for capitals;
    - the official iota-subscript ordering (`|/`) is rewritten to the ordering
      the beta-code library needs (`/|`).

    The shared spacing canonicalisation is retained deliberately: it reproduces
    the historical converter's apparatus formatting and never touches the
    official main text, which always uses spaced dashes.
    """
    return official_ccat_line(line, reorder_iota=False, faithful_capitals=True)


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
