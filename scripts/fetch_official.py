#!/usr/bin/env python3
"""Fetch and checksum the official Byzantine text archives."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from byz.reconcile.fetch import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
