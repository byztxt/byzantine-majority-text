"""run: PYTHONPATH=src python3 -m byz.contract"""

import sys

from . import invariants, report


def main() -> int:
    results = invariants.annotate_known_exceptions(invariants.validate_all())
    summary = report.write_all(results)
    print(f"wrote {summary['reports']}")
    print(f"wrote {summary['docs']} and {summary['contracts']}")
    print(
        f"invariants={summary['invariants']} "
        f"unresolved={summary['unresolved']} known={summary['known']} "
        f"missing_derived={summary['missing_derived']} "
        f"comparison_rows={summary['differences']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
