"""Generate the README files for the input tree under `data/`.

`data/` has two source classes: `data/raw/print/` holds published print-edition
material and `data/raw/repo/` holds this repository's own lineage. This module
renders eight documents: one for `data/` itself, one for `data/raw/`, one for
each of the two class roots, and one inside each of the four source folders.

Every count comes from the manifest that `byz.build` just wrote or from
`git ls-files` through `files.tracked_count`; no count is scraped from a
directory glob, so an untracked download cannot change a generated number. The
facts are read from the edition registry, the manifests, and
`sources.ARCHIVES`, never by parsing a provenance TOML. No clock, host name, or
absolute path is rendered.
"""

from .. import generated
from ..reconcile import sources

from . import editions, files

# Each edition id maps to its source-folder README path. The registry owns the
# `input_class`; this table records where the snapshot lives on disk.
SOURCE_READMES = {
    "rp2005": "data/raw/print/rp2005",
    "rp2018": "data/raw/print/rp2018",
    "rp2005-2019": "data/raw/repo/rp2005-2019",
    "rp2018-2023": "data/raw/repo/rp2018-2023",
}

# The hand-maintained provenance record and the generated ones. The names are a
# static fact about the layout, not a directory listing: `data/README.md` states
# what each record means, and `byz.verify` proves the generated ones.
PROVENANCE_RECORDS = (
    ("pdfs.toml", "hand-maintained: publisher URLs and local PDF paths"),
    ("rp2005.toml", "official 2005 archive hashes and downloads"),
    ("rp2018.toml", "official 2018 archive hashes and downloads"),
    ("rp2005-2019.toml", "the `v2.0.3` tag snapshot and its file hashes"),
    ("rp2018-2023.toml", "the current text's revision and file hashes"),
)


def _group_count(manifest: dict, root: str) -> int:
    """Return the pinned file count for the input group rooted at `root`."""
    for group in manifest.get("inputs", []):
        if group["root"] == root:
            return len(group["files"])
    return 0


def _snapshot_count(manifest: dict) -> int:
    """Return the total pinned inputs in one edition's snapshot."""
    return sum(len(group["files"]) for group in manifest.get("inputs", []))


def _include_count(manifest: dict, root: str, folder: str) -> int:
    """Count the pinned files that one include glob contributes.

    A repo snapshot has one input group with two include globs (one per source
    folder), so counting the whole group would report the total twice. Match
    each file against the include whose first segment is `folder`.
    """
    for group in manifest.get("inputs", []):
        if group["root"] != root:
            continue
        if not any(
            include.startswith(folder + "/") for include in group["include"]
        ):
            continue
        return sum(
            1
            for entry in group["files"]
            if entry["path"].startswith(folder + "/")
        )
    return 0


def _tracked_count(relative_dir: str, pattern: str = "*") -> int:
    """Committed-file count for a folder the manifests do not pin."""
    return files.tracked_count(relative_dir, pattern)


def _manifests_by_id(manifests) -> dict:
    if isinstance(manifests, dict):
        return manifests
    return {row["edition"]: row for row in manifests}


def _pinned_inputs(manifests: dict, kind: str) -> int:
    """Total pinned inputs for a class (`print` or `repo`)."""
    total = 0
    for row in manifests.values():
        for group in row.get("inputs", []):
            if group["root"].startswith(f"data/raw/{kind}/"):
                total += len(group["files"])
    return total


def _editions_in_class(kind: str) -> list:
    return [
        edition_id
        for edition_id, edition in editions.EDITIONS.items()
        if edition.get("input_class") == kind
    ]


def _archives_for(edition_id: str) -> list:
    return [
        spec for spec in sources.ARCHIVES if spec["edition"] == edition_id
    ]


def _pdf_count(edition_id: str) -> int:
    """One published PDF per edition that registers one."""
    return 1 if editions.EDITIONS[edition_id].get("pdf") else 0


def _class_pdf_count(kind: str) -> int:
    """Published PDFs across the editions of one source class."""
    return sum(
        _pdf_count(edition_id) for edition_id in _editions_in_class(kind)
    )


def _links(pairs) -> list:
    """Render `(label, target)` pairs as one Markdown bullet list."""
    return [f"- [{label}]({target})" for label, target in pairs]


def _banner_section(lines, title):
    lines.extend(["", f"## {title}", ""])


def render_data_readme(manifests) -> str:
    """Render `data/README.md`, the index of every input."""
    manifests = _manifests_by_id(manifests)
    print_count = _pinned_inputs(manifests, "print")
    repo_count = _pinned_inputs(manifests, "repo")
    archive_count = len(sources.ARCHIVES)
    pdf_count = _class_pdf_count("print")
    lines = [
        "# Inputs (`data/`)",
        "",
        "## What this folder holds",
        "",
        "`data/` holds every input an edition is built from. It has two source classes",
        "under `data/raw/`: `print/` for the published print editions",
        "and `repo/` for this repository's own lineage. `data/provenance/`",
        "records where each input came from and what its files hash to.",
        "",
        "Nothing here is a build output: the curated editions live under",
        "`editions/` and contain outputs only. The Beta-code, variant, parsing,",
        "and Strong's conventions are in `data/raw/repo/CONVENTIONS.md`.",
        "",
        "## Contents",
        "",
        "| Folder | Files | Contents | Feeds |",
        "| --- | --- | --- | --- |",
        f"| `raw/print/` | {print_count} pinned inputs | Published print-edition "
        f"extracts, preformatted ASCII, the {archive_count} ZIP archives, and "
        f"the {pdf_count} PDFs | `rp2005`, `rp2018` |",
        f"| `raw/repo/` | {repo_count} pinned inputs | The 2019 lineage, the "
        "current text, and the shared conventions | `rp2005-2019`, `rp2018-2023` |",
        f"| `provenance/` | {len(PROVENANCE_RECORDS)} records | "
        "SHA-256, download, tag, and revision facts for every source tree | "
        "`byz.fetch`, `byz.materialise`, `byz.build`, `byz.verify` |",
        "",
        "## Classes",
        "",
        "| Class | Holds | Origin | Editions |",
        "| --- | --- | --- | --- |",
        "| `print` | Published print-edition material | Downloaded and "
        "checksummed from the publisher | `rp2005`, `rp2018` |",
        "| `repo` | This repository's own lineage | Committed to this "
        "repository and pinned by tag or revision | `rp2005-2019`, `rp2018-2023` |",
        "",
        "## Provenance",
        "",
        "Every record lives in `data/provenance/`:",
        "",
    ]
    lines.extend(
        f"- `{name}` - {description}" for name, description in PROVENANCE_RECORDS
    )
    _banner_section(lines, "Commands")
    lines.extend(
        [
            "```bash",
            f"PYTHONPATH=src python3 -m byz.fetch --verify  # validate the {archive_count} committed archives",
            "PYTHONPATH=src python3 -m byz.fetch           # re-record the print-class downloads",
            "PYTHONPATH=src python3 -m byz.materialise     # restore the 2019 lineage from tag v2.0.3",
            "PYTHONPATH=src python3 -m byz.build           # CSV, TEI, manifests, and these READMEs",
            "PYTHONPATH=src python3 -m byz.verify          # check inputs and artifacts against the manifests",
            "```",
        ]
    )
    _banner_section(lines, "Related")
    lines.extend(
        _links(
            [
                ("Source classes", "raw/README.md"),
                ("Published print-edition sources", "raw/print/README.md"),
                ("Repository-lineage sources", "raw/repo/README.md"),
                ("Conventions", "raw/repo/CONVENTIONS.md"),
                ("Edition model", "../docs/EDITIONS.md"),
                ("Build details", "../docs/BUILD.md"),
            ]
        )
    )
    lines.append("")
    return "\n".join(lines)


def render_raw_readme(manifests) -> str:
    """Render `data/raw/README.md`, the print/repo boundary."""
    manifests = _manifests_by_id(manifests)
    lines = [
        "# Source classes (`data/raw/`)",
        "",
        "## What this folder holds",
        "",
        "`data/raw/` contains exactly two class directories. `print/` holds",
        "published print-edition material that was downloaded and checksummed;",
        "`repo/` holds material from this repository's own lineage. Every source",
        "tree belongs to exactly one class, and each class keeps its per-edition",
        "snapshots in named subfolders.",
        "",
        "## Contents",
        "",
        "| Folder | Files | Contents | Feeds |",
        "| --- | --- | --- | --- |",
    ]
    for edition_id in _editions_in_class("print"):
        manifest = manifests.get(edition_id, {})
        base = SOURCE_READMES[edition_id]
        count = _group_count(manifest, f"{base}/ccat") + _group_count(
            manifest, f"{base}/ascii"
        )
        lines.append(
            f"| `{base}/` | {count} pinned inputs, "
            f"{_tracked_count(f'{base}/preformatted', '*.ASC')} preformatted, "
            f"{_pdf_count(edition_id)} PDF | Print-edition extracts and the "
            "published PDF | "
            f"`editions/{edition_id}/` |"
        )
    for edition_id in _editions_in_class("repo"):
        manifest = manifests.get(edition_id, {})
        base = SOURCE_READMES[edition_id]
        count = sum(
            len(group["files"])
            for group in manifest.get("inputs", [])
            if group["root"] == base
        )
        lines.append(
            f"| `{base}/` | {count} pinned inputs | Repository-lineage snapshot | "
            f"`editions/{edition_id}/` |"
        )
    archive_total = len(sources.ARCHIVES)
    lines.append(
        f"| `print/_archives/` | {archive_total} ZIPs | The published "
        "archives the print sources were extracted from | `byz.fetch` |"
    )
    _banner_section(lines, "Classes")
    lines.extend(
        [
            "**`print/`** is published material. The publisher's ZIP archives",
            "are committed under `print/_archives/`, and the extracted `.CCT`,",
            "ASCII, and preformatted folders sit beside the PDF of the same",
            "edition. `byz.fetch` checks the pinned SHA-256 and extracts them;",
            "`byz.verify` checks the manifest against the committed files.",
            "",
            "**`repo/`** is this repository's lineage. `rp2005-2019/` is",
            "restored from git tag `v2.0.3`, and `rp2018-2023/` is the",
            "maintained current text snapshotted from the working tree. Both are",
            "inputs to `byz.build`, and both use the conventions in",
            "[`repo/CONVENTIONS.md`](repo/CONVENTIONS.md).",
            "",
            "The print class feeds `rp2005` and `rp2018`; the repo class",
            "feeds `rp2005-2019` and `rp2018-2023`. The print extracts are the",
            "publisher's own format; the repository conventions are not asserted",
            "for them.",
            "",
        ]
    )
    _banner_section(lines, "Provenance")
    lines.extend(
        [
            "- Print class: `data/provenance/rp2005.toml`, "
            "`data/provenance/rp2018.toml`, and the hand-maintained "
            "`data/provenance/pdfs.toml`.",
            "- Repo class: `data/provenance/rp2005-2019.toml` and "
            "`data/provenance/rp2018-2023.toml`.",
        ]
    )
    _banner_section(lines, "Commands")
    lines.extend(
        [
            "```bash",
            "PYTHONPATH=src python3 -m byz.fetch --verify",
            "PYTHONPATH=src python3 -m byz.materialise",
            "PYTHONPATH=src python3 -m byz.build",
            "PYTHONPATH=src python3 -m byz.verify",
            "```",
        ]
    )
    _banner_section(lines, "Related")
    lines.extend(
        _links(
            [
                ("Input index", "../README.md"),
                ("Published print-edition sources", "print/README.md"),
                ("Repository-lineage sources", "repo/README.md"),
                ("Conventions", "repo/CONVENTIONS.md"),
            ]
        )
    )
    lines.append("")
    return "\n".join(lines)


def render_class_readme(kind: str, manifests) -> str:
    """Render the README at `data/raw/<kind>/`."""
    manifests = _manifests_by_id(manifests)
    if kind == "print":
        title = "Print sources (`data/raw/print/`)"
        archive_count = len(sources.ARCHIVES)
        pdf_count = _class_pdf_count(kind)
        what = [
            "`data/raw/print/` holds the published print-edition material: the",
            "official `.CCT`, ASCII, and preformatted extracts, the",
            f"{pdf_count} published PDFs, and the {archive_count} committed ZIP",
            "archives they came from. Everything here was published by the",
            "publisher and downloaded, not authored in this repository.",
        ]
        commands = [
            "PYTHONPATH=src python3 -m byz.fetch --verify  # validate the committed ZIPs; no network",
            "PYTHONPATH=src python3 -m byz.fetch           # re-record provenance; no network after --verify",
            "PYTHONPATH=src python3 -m byz.build           # build the official editions",
            "PYTHONPATH=src python3 -m byz.verify          # check inputs and artifacts",
        ]
        provenance = [
            "- `data/provenance/rp2005.toml` and `data/provenance/rp2018.toml` - "
            "the archive hashes, downloads, and extraction paths.",
            "- `data/provenance/pdfs.toml` - hand-maintained publisher URLs and "
            "the local PDF paths.",
        ]
        editions_heading = "Editions"
        siblings = [
            ("Input index", "../../README.md"),
            ("Source classes", "../README.md"),
            ("Repository-lineage sources", "../repo/README.md"),
            ("rp2005 sources", "rp2005/README.md"),
            ("rp2018 sources", "rp2018/README.md"),
        ]
    elif kind == "repo":
        title = "Repository-lineage sources (`data/raw/repo/`)"
        what = [
            "`data/raw/repo/` holds this repository's own lineage: the 2019",
            "sources restored from tag `v2.0.3` and the maintained current text.",
            "Both are inputs to `byz.build`, and both share the conventions in",
            "`CONVENTIONS.md`.",
        ]
        commands = [
            "PYTHONPATH=src python3 -m byz.materialise  # restore the 2019 lineage from tag v2.0.3",
            "PYTHONPATH=src python3 -m byz.build        # build the repo editions",
            "PYTHONPATH=src python3 -m byz.verify       # check inputs and artifacts",
        ]
        provenance = [
            "- `data/provenance/rp2005-2019.toml` - the tag, commit, and "
            f"{_snapshot_count(manifests.get('rp2005-2019', {}))} file hashes.",
            "- `data/provenance/rp2018-2023.toml` - the revision, the two "
            f"source commits, and the "
            f"{_snapshot_count(manifests.get('rp2018-2023', {}))} file hashes.",
        ]
        editions_heading = "Editions"
        siblings = [
            ("Input index", "../../README.md"),
            ("Source classes", "../README.md"),
            ("Published print-edition sources", "../print/README.md"),
            ("Conventions", "CONVENTIONS.md"),
            ("rp2005-2019 sources", "rp2005-2019/README.md"),
            ("rp2018-2023 sources", "rp2018-2023/README.md"),
        ]
    else:
        raise ValueError(f"unknown source class: {kind!r}")

    lines = [
        f"# {title}",
        "",
        "## What this folder holds",
        "",
        *what,
        "",
        "## Contents",
        "",
        "| Folder | Files | Contents | Feeds |",
        "| --- | --- | --- | --- |",
    ]
    if kind == "print":
        for edition_id in _editions_in_class(kind):
            manifest = manifests.get(edition_id, {})
            base = SOURCE_READMES[edition_id]
            lines.append(
                f"| `{edition_id}/` | "
                f"{_group_count(manifest, f'{base}/ccat')} `.CCT`, "
                f"{_group_count(manifest, f'{base}/ascii')} `*_Byz.txt`, "
                f"{_tracked_count(f'{base}/preformatted', '*.ASC')} `.ASC`, "
                f"{_pdf_count(edition_id)} PDF | Print-edition extracts and "
                "PDF | "
                f"`editions/{edition_id}/` |"
            )
        lines.append(
            f"| `_archives/` | {len(sources.ARCHIVES)} ZIPs | The published "
            "archives, kept under their published names | `byz.fetch` |"
        )
    else:
        for edition_id in _editions_in_class(kind):
            manifest = manifests.get(edition_id, {})
            counts = _source_counts(edition_id, manifest)
            if edition_id == "rp2005-2019":
                breakdown = (
                    f"{counts['textonly']} `textonly-beta-code`, "
                    f"{counts['parsed']} `parsed`"
                )
                contents = "2019 lineage"
            else:
                breakdown = (
                    f"{counts['ccat']} `ccat`, {counts['strongs']} `strongs`"
                )
                contents = "current text"
            lines.append(
                f"| `{edition_id}/` | {breakdown} | {contents} | "
                f"`editions/{edition_id}/` |"
            )
        lines.append(
            "| `CONVENTIONS.md` | 1 | Beta-code, variant, parsing, and Strong's "
            "conventions shared by both repo sources | the repo build |"
        )
    _banner_section(lines, editions_heading)
    if kind == "print":
        for edition_id in _editions_in_class(kind):
            edition = editions.metadata(edition_id)
            lines.extend(
                [
                    f"- `{edition_id}` - {edition['title']}.",
                    f"  Sources: `{SOURCE_READMES[edition_id]}/`; "
                    f"PDF: `{edition['pdf']}`.",
                ]
            )
            for spec in _archives_for(edition_id):
                lines.append(
                    f"  Archive `{spec['name']}` (`{spec['format']}`) feeds "
                    f"`{SOURCE_READMES[edition_id]}/"
                    f"{sources.FORMAT_DIRS[spec['format']]}/`."
                )
        lines.extend(
            [
                "",
                "The archives are the download source; the extracts are",
                "committed, so a rebuild needs no network.",
            ]
        )
    else:
        for edition_id in _editions_in_class(kind):
            edition = editions.metadata(edition_id)
            manifest = manifests.get(edition_id, {})
            lines.append(f"- `{edition_id}` - {edition['title']}.")
            if edition.get("tag"):
                lines.append(
                    f"  Restored from tag `{edition['tag']}` (commit "
                    f"`{edition['commit']}`)."
                )
            if edition.get("revision"):
                lines.append(
                    f"  Revision `{edition['revision']}`; source commits "
                    f"`{manifest.get('source_commit', '')}` and "
                    f"`{manifest.get('strongs_commit', '')}`."
                )
        lines.extend(
            [
                "",
                "Both editions are regenerated by `byz.build`, not copied from",
                "a release. Their shared conventions are in",
                "[`CONVENTIONS.md`](CONVENTIONS.md).",
            ]
        )
    _banner_section(lines, "Provenance")
    lines.extend(provenance)
    _banner_section(lines, "Commands")
    lines.append("```bash")
    lines.extend(commands)
    lines.append("```")
    _banner_section(lines, "Related")
    lines.extend(_links(siblings))
    lines.append("")
    return "\n".join(lines)


def _source_counts(edition_id: str, manifest: dict) -> dict:
    base = SOURCE_READMES[edition_id]
    if editions.EDITIONS[edition_id]["input_class"] == "print":
        return {
            "ccat": _group_count(manifest, f"{base}/ccat"),
            "ascii": _group_count(manifest, f"{base}/ascii"),
            "preformatted": _tracked_count(
                f"{base}/preformatted", "*.ASC"
            ),
            "pdf": 1 if editions.EDITIONS[edition_id].get("pdf") else 0,
        }
    return {
        "textonly": _include_count(manifest, base, "textonly-beta-code"),
        "parsed": _include_count(manifest, base, "parsed"),
        "ccat": _include_count(manifest, base, "ccat"),
        "strongs": _include_count(manifest, base, "strongs"),
    }


def render_source_readme(edition_id: str, manifest: dict) -> str:
    """Render the README inside one source snapshot."""
    edition = editions.metadata(edition_id)
    base = SOURCE_READMES[edition_id]
    kind = editions.EDITIONS[edition_id]["input_class"]
    counts = _source_counts(edition_id, manifest)
    lines = [
        f"# `{edition_id}` sources",
        "",
        "## What this folder holds",
        "",
    ]
    if kind == "print":
        lines.extend(
            [
                f"The published sources of the {edition['title']}. The `.CCT`",
                "extract supplies the accented text, the ASCII extract the",
                "unaccented text, and the published PDF is the ultimate source",
                "of truth. The files are the publisher's own format; the",
                "repository conventions in `data/raw/repo/CONVENTIONS.md` are",
                "not asserted for them.",
            ]
        )
    elif edition_id == "rp2005-2019":
        lines.extend(
            [
                "The 2019 lineage, restored from git tag `v2.0.3` by",
                "`byz.materialise`. It is an input: `byz.build` regenerates",
                "the edition from these "
                f"{_snapshot_count(manifest)} files; it does not copy the",
                "release's CSV/TEI. The files follow the repository",
                "conventions in [`../CONVENTIONS.md`](../CONVENTIONS.md).",
            ]
        )
    else:
        lines.extend(
            [
                "The maintained current text: the Byzantine Textform as",
                "published in 2018 plus the 2023 adjustments, created and",
                "maintained by Dr. Maurice A. Robinson. This is the repository's",
                "own input, not a copy of the official printed editions' files,",
                "and `byz.build` regenerates every view from it. It is an input",
                "tree: the curated editions under `editions/` contain outputs",
                "only and pin these files by path and SHA-256. The published",
                "PDFs are the ultimate source of truth for the printed",
                "editions. The files follow the repository conventions in",
                "[`../CONVENTIONS.md`](../CONVENTIONS.md).",
            ]
        )
    lines.extend(["", "## Contents", ""])
    if kind == "print":
        lines.extend(
            [
                "| Folder | Files | Contents | Feeds |",
                "| --- | --- | --- | --- |",
                f"| `ccat/` | {counts['ccat']} `.CCT` | Accented Beta-code with "
                "apparatus | Accented CSV and TEI |",
                f"| `ascii/` | {counts['ascii']} `*_Byz.txt` | One line per "
                "verse, unaccented | Unaccented CSV and TEI |",
                f"| `preformatted/` | {counts['preformatted']} `.ASC` | The "
                "publisher's preformatted ASCII; not a build input | Archived "
                "reference |",
                f"| `official-pdf/` | {counts['pdf']} PDF | The published print "
                "edition | Source of truth |",
            ]
        )
    elif edition_id == "rp2005-2019":
        lines.extend(
            [
                "| Folder | Files | Contents | Feeds |",
                "| --- | --- | --- | --- |",
                f"| `textonly-beta-code/` | {counts['textonly']} `.CCT` | "
                "Mixed-case Beta-code with apparatus | Accented CSV and TEI |",
                f"| `parsed/` | {counts['parsed']} `.UB5` | Parsed text with "
                "Strong's numbers | Unaccented CSV, Strong's views, TEI |",
            ]
        )
    else:
        lines.extend(
            [
                "| Folder | Files | Contents | Feeds |",
                "| --- | --- | --- | --- |",
                f"| `ccat/` | {counts['ccat']} `.TXT` | All-lowercase accented "
                "Beta-code | Accented CSV and TEI |",
                f"| `strongs/` | {counts['strongs']} `.BP5` | Parsed text with "
                "Strong's numbers and morphology | Unaccented CSV, Strong's "
                "views, TEI |",
            ]
        )
    _banner_section(lines, "Edition")
    lines.append(f"- Folder: `{base}/`.")
    lines.append(f"- Edition: `editions/{edition_id}/` ({edition['title']}).")
    if kind == "print":
        lines.append(f"- Publisher: {edition['basis']}.")
        lines.append(f"- Published PDF: `{edition['pdf']}`.")
        lines.append(f"- PDF SHA-256: `{manifest.get('pdf_sha256', '')}`.")
        for spec in _archives_for(edition_id):
            lines.append(
                f"- Archive `{spec['name']}` (`{spec['format']}`) extracts to "
                f"`{sources.FORMAT_DIRS[spec['format']]}/`."
            )
    elif edition_id == "rp2005-2019":
        lines.extend(
            [
                f"- Tag: `{edition['tag']}` (commit `{edition['commit']}`).",
                "- Method: `git archive v2.0.3`.",
                "- Written by `PYTHONPATH=src python3 -m byz.materialise`.",
            ]
        )
    else:
        lines.extend(
            [
                f"- Revision: `{edition['revision']}`.",
                f"- `ccat_commit`: `{manifest.get('source_commit', '')}`.",
                f"- `strongs_commit`: `{manifest.get('strongs_commit', '')}`.",
            ]
        )
    _banner_section(lines, "Provenance")
    if kind == "print":
        lines.extend(
            [
                f"- `data/provenance/{edition_id}.toml` - the archive hashes "
                "and downloads.",
                "- `data/provenance/pdfs.toml` - the hand-maintained PDF URL "
                "and local path.",
            ]
        )
    else:
        lines.append(
            f"- `data/provenance/{edition_id}.toml` - "
            + (
                "the tag, commit, and file hashes."
                if edition_id == "rp2005-2019"
                else "the revision, the two source commits, and the file hashes."
            )
        )
    _banner_section(lines, "Commands")
    lines.append("```bash")
    if kind == "print":
        lines.extend(
            [
                "PYTHONPATH=src python3 -m byz.fetch --verify",
                "PYTHONPATH=src python3 -m byz.fetch",
                "PYTHONPATH=src python3 -m byz.build",
                "PYTHONPATH=src python3 -m byz.verify",
            ]
        )
    elif edition_id == "rp2005-2019":
        lines.extend(
            [
                "PYTHONPATH=src python3 -m byz.materialise",
                "PYTHONPATH=src python3 -m byz.build",
                "PYTHONPATH=src python3 -m byz.verify",
            ]
        )
    else:
        lines.extend(
            [
                "PYTHONPATH=src python3 -m byz.build",
                "PYTHONPATH=src python3 -m byz.verify",
            ]
        )
    lines.append("```")
    _banner_section(lines, "Related")
    parent = "../README.md"
    related = [
        ("Class README", parent),
        ("Conventions", "../CONVENTIONS.md")
        if kind == "repo"
        else ("Input index", "../../../README.md"),
        (f"Edition `{edition_id}`", f"../../../../editions/{edition_id}/README.md"),
        ("Provenance record", f"../../../../data/provenance/{edition_id}.toml"),
    ]
    lines.extend(_links(related))
    lines.append("")
    return "\n".join(lines)


def write_data_docs(manifests) -> list:
    """Render and write the eight generated input-tree READMEs."""
    by_id = _manifests_by_id(manifests)
    documents = [
        ("data/README.md", render_data_readme(by_id)),
        ("data/raw/README.md", render_raw_readme(by_id)),
        (
            "data/raw/print/README.md",
            render_class_readme("print", by_id),
        ),
        (
            "data/raw/repo/README.md",
            render_class_readme("repo", by_id),
        ),
    ]
    for edition_id in editions.EDITIONS:
        path = f"{SOURCE_READMES[edition_id]}/README.md"
        documents.append(
            (
                path,
                render_source_readme(edition_id, by_id.get(edition_id, {})),
            )
        )
    written = []
    for relative, text in documents:
        written.append(generated.write_markdown(editions.ROOT / relative, text))
    return written
