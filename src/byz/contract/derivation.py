"""Static derivation map with existence checks, evidenced by the converters."""

from . import bp5, ccat, paths

# The columns of `reports/baseline/derivations.csv`. Declared once so the header
# written for an empty result and the row dicts cannot drift apart.
DERIVATION_FIELDS = ("source", "derived", "evidence", "status")


def check(root=paths.ROOT):
    rows = []

    def add(source, derived_path, evidence):
        try:
            rel = str(derived_path.relative_to(root))
        except ValueError:
            rel = str(derived_path)
        rows.append(
            {
                "source": source,
                "derived": rel,
                "evidence": evidence,
                "status": "ok" if derived_path.is_file() else "missing",
            }
        )

    for path in sorted(
        (root / paths.CCAT_DIR.relative_to(paths.ROOT)).glob("*.TXT")
    ):
        num = ccat.book_num(path)
        abbr = paths.NUM_TO_ABBR.get(num, num)
        for view, directory in paths.CSV_CCAT.items():
            target = (
                root / directory.relative_to(paths.ROOT) / f"{abbr}.csv"
            )
            add(str(path.relative_to(root)), target, paths.DERIVATION_EVIDENCE["ccat"])

    for path in sorted(
        (root / paths.BP5_DIR.relative_to(paths.ROOT)).glob("*.BP5")
    ):
        num = bp5.book_num(path)
        abbr = paths.NUM_TO_ABBR.get(num, num)
        for view, directory in paths.CSV_STRONGS.items():
            target = (
                root / directory.relative_to(paths.ROOT) / f"{abbr}.csv"
            )
            add(
                str(path.relative_to(root)),
                target,
                paths.DERIVATION_EVIDENCE["strongs"],
            )
        target = (
            root
            / paths.CSV_UNACCENTED["csv/unaccented"].relative_to(paths.ROOT)
            / f"{abbr}.csv"
        )
        add(
            str(path.relative_to(root)),
            target,
            paths.DERIVATION_EVIDENCE["unaccented"],
        )

    tei_dir = root / paths.TEI_DIR.relative_to(paths.ROOT)
    unaccented = root / paths.CSV_UNACCENTED["csv/unaccented"].relative_to(
        paths.ROOT
    )
    for path in sorted(unaccented.glob("*.csv")):
        target = tei_dir / f"{path.stem}.xml"
        add(str(path.relative_to(root)), target, paths.DERIVATION_EVIDENCE["tei"])

    add(
        f"{paths.dataset_name('csv/unaccented')}/*.csv",
        root / paths.TEI_BYZ.relative_to(paths.ROOT),
        paths.DERIVATION_EVIDENCE["tei"],
    )

    demo = root / paths.ASSETS_DIR.relative_to(paths.ROOT) / "demo_john_1.xml"
    if demo.is_file():
        rows.append(
            {
                "source": "n/a",
                "derived": str(demo.relative_to(root)),
                "evidence": "hand-prepared demo asset (see docs/COLLATEX.md)",
                "status": "auxiliary",
            }
        )
    rows.sort(key=lambda row: (row["source"], row["derived"]))
    return rows


def summary(rows):
    groups = {}
    for row in rows:
        group = groups.setdefault(
            row["evidence"],
            {
                "checked": 0,
                "ok": 0,
                "missing": 0,
                "auxiliary": 0,
                "example_source": row["source"],
                "example_derived": row["derived"],
            },
        )
        group["checked"] += 1
        group[row["status"]] = group.get(row["status"], 0) + 1
    return groups
