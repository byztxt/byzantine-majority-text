"""Shared data types for the baseline contract."""

from dataclasses import dataclass

# The columns of `reports/baseline/files.csv`. Declared once so the header
# written for an empty result and the row dicts cannot drift apart.
FILE_FIELDS = (
    "dataset",
    "path",
    "size",
    "sha256",
    "lines",
    "encoding",
    "eol",
    "format_class",
    "git_blob",
    "last_commit",
)


@dataclass(frozen=True)
class FileRecord:
    dataset: str
    path: str
    size: int
    sha256: str
    lines: int
    encoding: str
    eol: str
    format_class: str
    git_blob: str = ""
    last_commit: str = ""

    def as_row(self) -> dict:
        return {name: getattr(self, name) for name in FILE_FIELDS}


# The columns of `reports/baseline/invariants.csv`. Declared once so the header
# written for an empty result and the row dicts cannot drift apart.
VIOLATION_FIELDS = (
    "dataset",
    "path",
    "line",
    "category",
    "message",
    "key",
    "known_exception",
)


@dataclass(frozen=True)
class Violation:
    dataset: str
    path: str
    line: int
    category: str
    message: str
    key: str = ""
    known_exception: str = ""

    def as_row(self) -> dict:
        return {name: getattr(self, name) for name in VIOLATION_FIELDS}


@dataclass
class DatasetResult:
    name: str
    records: list
    violations: list
    meta: dict
