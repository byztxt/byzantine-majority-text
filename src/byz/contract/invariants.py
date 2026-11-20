"""Run every validator over the real corpus and annotate known exceptions."""

from dataclasses import replace

from . import bp5, ccat, csv_view, paths, tei_view

KNOWN_EXCEPTIONS = {}


def _csv_results(root):
    results = {}
    for key, directory in list(paths.CSV_CCAT.items()) + list(
        paths.CSV_STRONGS.items()
    ):
        dataset = paths.dataset_name(key)
        directory = root / directory.relative_to(paths.ROOT)
        results[dataset] = [
            csv_view.validate(path, dataset)
            for path in sorted(directory.glob("*.csv"))
            if path.is_file()
        ]
    return results


def validate_all(root=paths.ROOT):
    results = {
        "source/CCAT": [
            ccat.validate(path)
            for path in sorted((root / "source" / "CCAT").glob("*.TXT"))
            if path.is_file()
        ],
        "source/Strongs": [
            bp5.validate(path)
            for path in sorted((root / "source" / "Strongs").glob("*.BP5"))
            if path.is_file()
        ],
    }
    results.update(_csv_results(root))

    tei_dir = root / paths.TEI_DIR.relative_to(paths.ROOT)
    results[paths.TEI_DATASET] = [
        tei_view.validate(path, paths.TEI_DATASET)
        for path in sorted(tei_dir.glob("*.xml"))
        if path.is_file()
    ]
    tei_byz = root / paths.TEI_BYZ.relative_to(paths.ROOT)
    results[paths.TEI_BYZ_DATASET] = (
        [tei_view.validate(tei_byz, paths.TEI_BYZ_DATASET)]
        if tei_byz.is_file()
        else []
    )
    return results


def annotate_known_exceptions(results):
    for items in results.values():
        for result in items:
            annotated = []
            for violation in result.violations:
                reason = KNOWN_EXCEPTIONS.get(
                    (violation.dataset, violation.category, violation.key)
                )
                if reason:
                    annotated.append(replace(violation, known_exception=reason))
                else:
                    annotated.append(violation)
            result.violations = annotated
    return results


def all_violations(results):
    for items in results.values():
        for result in items:
            yield from result.violations
