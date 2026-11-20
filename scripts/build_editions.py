#!/usr/bin/env python3
"""Build curated CSV/TEI, manifests, README files, and EDITIONS.md."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from byz.curate import build, docs  # noqa: E402

if __name__ == "__main__":
    manifests = build.build_all()
    print(f"built {len(manifests)} editions")
    print(f"wrote {docs.write_editions_doc()}")
    print(f"updated {docs.update_root_readme()}")
