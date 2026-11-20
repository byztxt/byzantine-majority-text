#!/usr/bin/env python3
"""Generate successive edition diffs."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from byz.curate import diff  # noqa: E402

if __name__ == "__main__":
    for path in diff.diff_all():
        print(f"wrote {path}")
