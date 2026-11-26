"""Verify the curated editions against their manifests.

run: PYTHONPATH=src python3 -m byz.verify [edition ...] [--edition-dir PATH]
"""

import sys


def main(argv=None) -> int:
    from .curate import verify

    return verify.main(argv)


if __name__ == "__main__":
    sys.exit(main())
