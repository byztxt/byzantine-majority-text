"""run: PYTHONPATH=src python3 -m byz.reconcile"""

import sys

from . import compare, report, sources


def main() -> int:
    results = compare.run()
    summary = report.write_all(results)
    for edition, stat in sorted(summary["source_stats"].items()):
        print(
            f"{edition}: source files={stat['files']} "
            f"normalized={stat['normalized']} "
            f"verses={stat['match']}/{stat['verses']}"
        )
    print(f"closest edition: {summary['best']}")
    print(f"strongs provenance: {summary['strongs']}")
    print(
        f"wrote {summary['files']} file rows and {summary['verses']} verse rows "
        f"to {sources.REPORTS_DIR}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
