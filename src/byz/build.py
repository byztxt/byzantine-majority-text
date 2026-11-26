"""Build curated CSV/TEI, manifests, README files, and EDITIONS.md.

run: PYTHONPATH=src python3 -m byz.build
"""

import sys


def main() -> int:
    from .curate import build, data_docs, docs

    manifests = build.build_all()
    print(f"built {len(manifests)} editions")
    print(f"wrote {docs.write_editions_doc()}")
    print(f"updated {docs.update_root_readme()}")
    written = data_docs.write_data_docs(manifests)
    print(f"updated {len(written)} input-tree READMEs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
