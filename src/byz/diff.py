"""Generate successive edition diffs.

run: PYTHONPATH=src python3 -m byz.diff
"""

import sys


def main() -> int:
    from .curate import diff

    for path in diff.diff_all():
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
