"""Run every validator over the real corpus and annotate known exceptions."""

from dataclasses import replace

from . import bp5, ccat, csv_view, paths, tei_view

_BLANK_REASON = (
    "The verse reference is present with no text in the base file. The reading "
    "is not in the main text here; needs maintainer confirmation (decision log D7)."
)
_ACT24_REASON = (
    "Acts 24:6-8 Byzantine expansion lives in 05a_ACT24.TXT; "
    "05_ACT.TXT leaves 24:7 blank by design."
)

KNOWN_EXCEPTIONS = {
    ("source/CCAT", "blank-record", "LUK 17:36"): _BLANK_REASON,
    ("source/CCAT", "blank-record", "ACT 8:37"): _BLANK_REASON,
    ("source/CCAT", "blank-record", "ACT 15:34"): _BLANK_REASON,
    ("source/CCAT", "blank-record", "ACT 24:7"): _ACT24_REASON,
    ("source/Strongs", "blank-record", "LUK 17:36"): _BLANK_REASON,
    ("source/Strongs", "blank-record", "ACT 8:37"): _BLANK_REASON,
    ("source/Strongs", "blank-record", "ACT 15:34"): _BLANK_REASON,
    ("source/Strongs", "blank-record", "ACT 24:7"): _ACT24_REASON,
}


def _csv_results(root):
    results = {}
    for key, directory in list(paths.CSV_CCAT.items()) + list(
        paths.CSV_STRONGS.items()
    ):
        dataset = f"csv-unicode/{key}"
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
    results["tei-xml-unicode/no-accents"] = [
        tei_view.validate(path)
        for path in sorted(tei_dir.glob("*.xml"))
        if path.is_file()
    ]
    tei_byz = root / paths.TEI_BYZ.relative_to(paths.ROOT)
    results["tei-xml-unicode/BYZ"] = (
        [tei_view.validate(tei_byz, "tei-xml-unicode/BYZ")]
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
