"""Fetch and checksum the official archives.

run: PYTHONPATH=src python3 -m byz.fetch [--verify|--force]
"""

import sys


def main(argv=None) -> int:
    from .reconcile.fetch import main as fetch_main

    return fetch_main(argv)


if __name__ == "__main__":
    sys.exit(main())
