"""Encoding and line-ending detection kept deliberately simple and explicit."""

BOM_UTF8 = b"\xef\xbb\xbf"


def detect_encoding(data: bytes) -> str:
    if data.startswith(BOM_UTF8):
        return "utf-8-sig"
    if not data:
        return "empty"
    if all(byte < 0x80 for byte in data):
        return "ascii"
    try:
        data.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        pass
    try:
        data.decode("cp1252")
        return "cp1252"
    except UnicodeDecodeError:
        return "latin-1"


def detect_eol(data: bytes) -> str:
    crlf = data.count(b"\r\n")
    lf = data.count(b"\n") - crlf
    cr = data.count(b"\r") - crlf
    kinds = [name for name, count in (("crlf", crlf), ("lf", lf), ("cr", cr)) if count]
    if not kinds:
        return "none"
    if len(kinds) > 1:
        return "mixed"
    return kinds[0]


def decode(data: bytes, encoding: str) -> str:
    if encoding == "utf-8-sig":
        return data.decode("utf-8-sig")
    if encoding in ("ascii", "utf-8"):
        return data.decode("utf-8")
    return data.decode(encoding)


def read_text(path) -> tuple[str, str]:
    data = path.read_bytes()
    encoding = detect_encoding(data)
    return decode(data, encoding), encoding
