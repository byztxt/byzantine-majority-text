"""Shared data types for the baseline contract."""

from dataclasses import dataclass


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
        return {
            "dataset": self.dataset,
            "path": self.path,
            "size": self.size,
            "sha256": self.sha256,
            "lines": self.lines,
            "encoding": self.encoding,
            "eol": self.eol,
            "format_class": self.format_class,
            "git_blob": self.git_blob,
            "last_commit": self.last_commit,
        }


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
        return {
            "dataset": self.dataset,
            "path": self.path,
            "line": self.line,
            "category": self.category,
            "message": self.message,
            "key": self.key,
            "known_exception": self.known_exception,
        }


@dataclass
class DatasetResult:
    name: str
    records: list
    violations: list
    meta: dict
