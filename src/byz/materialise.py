"""Materialise the historical 2005-2019 inputs into `data/`.

run: PYTHONPATH=src python3 -m byz.materialise
"""

import sys


def main(argv=None) -> int:
    from .curate import materialise

    destination = materialise.materialise_historical()
    files = [
        path
        for path in destination.rglob("*")
        if path.is_file()
        and path.relative_to(destination).as_posix()
        not in materialise.GENERATED_NEIGHBOURS
    ]
    print(
        f"materialised {materialise.HISTORICAL_INPUT_ROOT} "
        f"({len(files)} files)"
    )
    print(f"wrote {materialise.HISTORICAL_PROVENANCE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
