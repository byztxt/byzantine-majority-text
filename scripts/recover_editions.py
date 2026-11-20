#!/usr/bin/env python3
"""Recover and freeze the four curated editions."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from byz.curate import recover  # noqa: E402

if __name__ == "__main__":
    for path in recover.recover_all():
        print(f"recovered {path}")
