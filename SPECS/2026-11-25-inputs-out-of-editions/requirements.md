# Requirements - Inputs out of the editions: `data/` -> pipeline -> `editions/`

## Context

The repository says its model is **inputs -> pipeline -> outputs**. The folders
now say it too, except for one stubborn exception: every curated edition still
carries a frozen copy of its own inputs under `editions/<edition>/source/`.

```
today
  data/
    text/CCAT, text/Strongs          <- repository input (current text)
    raw/<edition>/                   <- official archive extracts
    raw/_archives/                   <- committed official ZIPs
    provenance/*.toml                <- input metadata
  editions/<edition>/
    source/                          <- a COPY OF AN INPUT, inside an output
    csv/, tei/                       <- outputs
    manifest.json                    <- records source_files relative to the edition
    README.md
```

Two problems:

1. **An input lives inside an output.** `editions/rp2018-2023/source/` is
   byte-identical to `data/text/`; the three other snapshots are byte-identical
   to archive extracts or to tag `v2.0.3`. The edition looks self-contained, but
   it is self-contained by carrying a second copy of data that already exists.
   The copies are 172 files and 11,347,400 bytes (11.0% of the 103.3 MB
   `editions/` tree), and they were the snapshot half of the old recovery step.
2. **One input lives only in git history.** The `rp2005-2019` inputs are
   extracted on every build from tag `v2.0.3`; `data/` has no copy. A clone at
   any commit cannot build that edition without git archaeology, and the
   provenance of those files is a sentence in a README, not a record in
   `data/provenance/`.

This change removes the copies and moves the last input under `data/`, so the
shape is literally:

```
after
  data/                              <- every input, nothing else
  src/byz/                           <- the pipeline
  editions/<edition>/                <- outputs only: csv/, tei/, manifest.json, README.md
```

The manifest is the bridge: it names each input by **repo-relative path and
SHA-256**, so an edition can be checked against `data/` without embedding a
copy. A new `byz.verify` entry point performs that check.

## Goal

1. Delete `editions/<edition>/source/` for all four editions. No input snapshot
   remains under `editions/`.
2. Commit the 2005-2019 **source files** under `data/raw/rp2005-2019/`, with
   `data/provenance/rp2005-2019.toml` recording tag `v2.0.3`, its commit, and
   every file's SHA-256. Those 57 files are the edition's only inputs; the
   tag's released CSV/TEI are neither inputs nor outputs of this repository.
3. Replace the manifest's edition-relative `source_files` list with an `inputs`
   list of `{root, include, files}` groups whose paths are repo-relative.
4. Add `PYTHONPATH=src python3 -m byz.verify`, which checks an edition's manifest
   against the inputs under `data/` and against its committed `csv/` and `tei/`.
5. Keep `rp2005`, `rp2018`, and `rp2018-2023` byte-identical. `rp2005-2019` is
   **regenerated** from its sources by the current pipeline and changes by
   design (see Correction 2).
6. Keep the pipeline deterministic: a second full regeneration is byte-identical,
   and no artifact carries a timestamp, hostname, or absolute path.

## Correction (2026-11-25, maintainer)

The first draft of D2 moved all 170 `v2.0.3` files into `data/`. That was wrong.
Only the 57 files in `textonly-beta-code/` and `parsed/` are the edition's
inputs.

## Correction 2 (2026-11-25, maintainer) - regenerate the historical edition

Reproducing the 2019 release's artifacts is wrong, because they contain real
bugs that the current pipeline fixes. Measured against the committed edition:

- **7,482 malformed apparatus markers** across all 29
  `csv/accented/with-variants` files: `{Ν` (Greek capital Nu) 6,816 times and
  `{Β` (Greek capital Beta) 666 times. The 2019 converter transliterated the
  code initials instead of emitting `{NA`/`{Byz`.
- 1,920 verses whose only other difference is typography (`¶` placement, `’`
  vs `'`); **zero** letter or word differences in the main text. The count is
  measured over the 29 accented no-variants files after removing `¶` and
  normalising curly apostrophes to `'`.

Therefore `rp2005-2019` is generated from its 2019 sources by the current
pipeline, exactly like the other editions:

- `csv/accented/no-variants` and `csv/accented/with-variants` from
  `textonly-beta-code/*.CCT`, using `parse_cct_accented`;
- `csv/strongs/with-parsing`, `csv/strongs/no-parsing`, and `csv/unaccented`
  from `parsed/*.UB5`;
- `tei/unaccented` from the unaccented text and `tei/accented` from the
  accented no-variants text.

`byz.build` reads no git tag at all: no `git archive`, no artifact prefixes, no
copying of released CSV/TEI, and no MAR 16:8 post-correction (regeneration
produces the correct literals from the source). Tag `v2.0.3` is read only by
`byz.materialise`, and only to materialise the 57 sources. The docs say
`rp2005-2019` is "the 2019 sources, rebuilt by the current pipeline" and state
what changes versus the release artifacts (apparatus codes corrected,
typography normalised). This correction amends Goal 2, Goal 5, the non-goals,
D2, D6, D7, R1.4, R2, R3.3, R4, R9, the acceptance criteria, and the risks.
`reports/diffs/**` changes for the two pairs that include `rp2005-2019`; the
other two pairs stay byte-identical.

## Non-goals

- **No change to the `rp2005`, `rp2018`, or `rp2018-2023` CSV or TEI bytes.**
  Their 477 files keep their SHA-256. `rp2005-2019` changes by design: it is
  regenerated from its 2019 sources (Correction 2).
- **No change to the text, the archives, the PDFs, any `.TXT`/`.BP5` file under
  `data/text/`, or the existing `data/raw/rp2005` / `data/raw/rp2018` trees.**
  D2 only adds `data/raw/rp2005-2019/` and its provenance. `data/text/README.md`
  receives documentation edits (R8.2); its hash changes, but no text data does.
- **No release-bundling or downloading system.** Editions are still directories
  in git; no zip, checksum manifest for downloads, or installer is added.
- **No new dependency.** `beta-code==1.0.0` remains the only one. `byz.verify`
  uses the standard library.
- **No packaging.** Commands stay `PYTHONPATH=src python3 -m byz.<verb>`.
- **No compatibility shim.** `source_files` is removed, not duplicated; the
  old `byz.recover` name and its snapshot behaviour are removed, not aliased.
  See D5.
- **No change to the edition model, dataset set, diff categories, or report
  figures.** `csv/unaccented` remains outside the contract
  (`SPECS/2026-11-19-…` R5.3).
- **No re-download.** `byz.fetch --force` is not used; `data/provenance/rp2005.toml`
  and `rp2018.toml` keep their recorded timestamps and URLs.
- **No new TOML parser dependency.** `rp2005-2019.toml` is written with the same
  hand-rolled, minimal TOML writer style `byz.fetch` already uses.

## Affected scope

- **Editions:** all four. `editions/*/source/` is deleted (172 files); the 672
  CSV/TEI files are unchanged; each `manifest.json` replaces `source_files` with
  `inputs`; each `README.md` drops the snapshot section and points at
  `manifest.json` / `byz.verify`.
- **Inputs added:** `data/raw/rp2005-2019/` (57 source files) and
  `data/provenance/rp2005-2019.toml`.
- **Pipeline:** `src/byz/curate/build.py` reads `data/` for all three build
  paths and stages `csv/`/`tei/`; `src/byz/curate/recover.py` shrinks to the
  `src/byz/curate/materialise.py` materialises the historical inputs;
  `src/byz/curate/diff.py` reads the source tier
  from `data/`; new `src/byz/curate/verify.py` and `src/byz/verify.py`;
  `src/byz/curate/editions.py` registers every input directory.
- **Generated docs/reports:** `README.md`, `docs/EDITIONS.md`,
  `docs/DATA_CONTRACT.md`, `docs/PROVENANCE.md` (one pointer sentence),
  `editions/*/README.md`, `docs/contract/*.json`, `reports/baseline/*`,
  `reports/diffs/*` (should be unchanged), and the four manifests.
- **Hand-written files edited directly:** `data/text/README.md`,
  `docs/BUILD.md`, `SPECS/TECH.md`, `.opencode/**`, and the tests.
- **Deleted files:** `editions/*/source/**` (172), `src/byz/recover.py`,
  `src/byz/curate/recover.py`, and `tests/curate/test_recover.py`.
- **New files:** `data/raw/rp2005-2019/**` (57, generated by
  `byz.materialise`), `data/provenance/rp2005-2019.toml` (generated),
  `src/byz/verify.py`,
  `src/byz/curate/verify.py`, `src/byz/curate/files.py`,
  `tests/curate/test_verify.py`, `tests/curate/test_materialise.py` (replacing
  `tests/curate/test_recover.py`).

## Verified inventory

Checked against the working tree at `7fb28fe`, 2026-11-25. The working tree had
uncommitted documentation edits at the time of writing (see "Preconditions" in
`plan.md`); none of them changes an edition CSV/TEI or an input file. No
generator was run.

### The four snapshots

| Edition | Snapshot | Files | Bytes | Source of the bytes |
| --- | --- | ---: | ---: | --- |
| `rp2005` | `editions/rp2005/source/ccat/` | 29 `.CCT` | 1,400,061 | `data/raw/rp2005/editions-rp2-ccat/` (byte-identical) |
| `rp2005-2019` | `editions/rp2005-2019/source/{textonly-beta-code,parsed}/` | 57 (30+27) | 4,426,583 | `git archive v2.0.3`, same paths |
| `rp2018` | `editions/rp2018/source/ccat/` | 30 `.CCT` (incl. `GREEK.CCT`) | 1,401,158 | `data/raw/rp2018/rp2018-ccat/` (byte-identical) |
| `rp2018-2023` | `editions/rp2018-2023/source/{CCAT,Strongs}/` | 56 (29+27) | 4,119,598 | `data/text/{CCAT,Strongs}/` (byte-identical) |
| **Total** | | **172** | **11,347,400** | |

`editions/` is 852 tracked files and 103,280,635 bytes; 672 of those files are
CSV/TEI, 172 are snapshots, and 8 are the four manifests and four READMEs.
`git count-objects -vH` reports an 18.31 MiB pack.

### What each build path reads today

| Function | Reads | Writes |
| --- | --- | --- |
| `build.build_official` (line 616) | `editions/<id>/source/ccat/*.CCT` (line 619) **and** `data/raw/<edition>/<ascii_dir>/*_Byz.txt` (line 618) | edition CSV/TEI |
| `build.build_historical` (line 676) | `editions/rp2005-2019/source/parsed/*.UB5` (line 678), and `editions/rp2005-2019/csv/unaccented/*.csv` as a reference (lines 683-687) | edition Strong's views and accented TEI |
| `build.build_current` (line 703) | `editions/rp2018-2023/source/{CCAT,Strongs}/` (lines 714-716) | edition CSV/TEI |
| `recover.recover_official` (line 252) | `data/raw/<edition>/<source_dir>/*.CCT` | edition `source/ccat/` |
| `recover.recover_current` (line 268) | `data/text/{CCAT,Strongs}/` | edition `source/{CCAT,Strongs}/` |
| `recover.recover_historical` (line 202) | `git archive v2.0.3` (six prefixes) | edition `source/` **and** the copied historical `csv/`/`tei/` |
| `diff._load_official` (line 150), `_load_historical` (line 160), `_load_current` (line 170) | the same edition snapshots | `reports/diffs/` |

Two facts the brief does not state:

1. `recover.recover_historical` is not only an input stager. It also copies the
   `v2.0.3` released `csv-unicode/` and `tei-xml-unicode/` artifacts into the
   edition (lines 215-231) and corrects the MAR 16:8 apparatus literal (line
   247). Those copied views are **inputs to the curated edition**, not outputs
   the current converter can regenerate: the 2019 lowercase dialect is not
   reproduced by the current converter (678 differences in Mark alone).
2. `byz.diff` reads the snapshots too. Removing `source/` changes a fourth
   consumer, not just the three `build_*` functions.

### The 2019 lineage in tag `v2.0.3`

`git rev-parse v2.0.3^{commit}` = `8ec95671e463030347c2c643358eb56e58235b19`.
The pre-change build reads six prefixes:

| Tag prefix | Files | Destination | Kind |
| --- | ---: | --- | --- |
| `textonly-beta-code/` | 30 `.CCT` | `data/raw/rp2005-2019/textonly-beta-code/` | input |
| `parsed/` | 27 `.UB5` | `data/raw/rp2005-2019/parsed/` | input |
| `csv-unicode/accents/no-variants/` | 29 `.csv` | `editions/rp2005-2019/csv/accented/no-variants/` | output |
| `csv-unicode/accents/with-variants/` | 29 `.csv` | `editions/rp2005-2019/csv/accented/with-variants/` | output (MAR 16:8 corrected) |
| `csv-unicode/no-accents/` | 27 `.csv` | `editions/rp2005-2019/csv/unaccented/` | output |
| `tei-xml-unicode/no-accents/` | 28 `.xml` | `editions/rp2005-2019/tei/unaccented/` | output |
| **Total** | **170** | | 57 inputs, 113 outputs |

The tag's `textonly-online-bible/` is **not** read by any build path and is not
materialised. The four released-artifact prefixes are not read by `byz.build`
either; the edition is regenerated from the 57 source files (Correction 2), and
the released files are pinned in no manifest and no provenance record.

### Current manifest shape

All four manifests have `artifact_files` (edition-relative `path`, `sha256`,
`size`), `generated_by` (`"PYTHONPATH=src python3 -m byz.build"`), and
`source_files` (edition-relative `path`, `sha256`, `size`). The counts and
edition-specific keys are:

| Edition | `source_files` | `artifact_files` | Other keys |
| --- | ---: | ---: | --- |
| `rp2005` | 29 | 141 | `ascii_source`, `preformatted_source`, `pdf_sha256`, `pdf_size` |
| `rp2005-2019` | 57 | 195 | `tag`, `commit` |
| `rp2018` | 30 | 141 | `ascii_source`, `preformatted_source`, `pdf_sha256`, `pdf_size` |
| `rp2018-2023` | 56 | 195 | `source_commit`, `strongs_commit` |

The official `source_files` lists pin only `.CCT`; the ASCII inputs are named by
`ascii_source` but are **not hashed** in the manifest today.

### Consumers that name the snapshots

| Consumer | What it does |
| --- | --- |
| `src/byz/curate/build.py` (72, 119-127, 616-781, 793-847, 864-905, 908-920) | `SNAPSHOT_DIR`, `EXPORT_NOTES`, all three build paths, README prose, manifest `source_files`, `recover.recover_all()` |
| `src/byz/curate/recover.py` (whole file) | staging, swap, three recover functions, historical artifact copy |
| `src/byz/curate/diff.py` (150-187) | the source tier for every diff |
| `src/byz/curate/docs.py` (237-241, 350-365, 474-489, 603-631) | generated `docs/EDITIONS.md` and root README prose |
| `src/byz/generated.py` (87-94) | the `editions/<edition>/source/` row in the README's generated-files table |
| `src/byz/contract/paths.py` (100-115), `report.py` (75-81) | derivation evidence and `docs/DATA_CONTRACT.md` prose |
| `README.md` (86, 110, 180, 187-191), `docs/BUILD.md` (21, 29, 40-44, 62, 135), `data/text/README.md` (9), `editions/*/README.md` | public prose |
| `.opencode/**` (10 files) | agent instructions that still say "recover then build" |
| `tests/curate/{test_current_pipeline,test_fidelity,test_integration,test_build,test_recover,test_layout,test_editions,test_generated}.py` | snapshot file sets, manifest gates, recovery safety, layout, docs |

## Definitions

- **Input** - a committed file under `data/` that a build reads: the current
  Beta-code text, an official archive extract, or the materialised 2005-2019
  lineage.
- **Output** - a committed file under `editions/<edition>/`: `csv/`, `tei/`,
  `manifest.json`, `README.md`.
- **Input group** - one `{root, include, files}` object in a manifest. `root` is
  a repo-relative directory; `include` lists the globs the build reads under
  it; `files` lists every matched file with `path` (relative to `root`),
  `sha256`, and `size`.
- **Snapshot** - the retired `editions/<edition>/source/` copy of an input.
- **Materialise** - extract the six `v2.0.3` prefixes into
  `data/raw/rp2005-2019/` and write `data/provenance/rp2005-2019.toml`.
- **Byte-identity gate** - the proof that all 672 CSV/TEI files are unchanged
  and no file is added or removed under `editions/*/{csv,tei}`.
- **Self-verification** - the retired property that an edition directory alone
  contains enough data to verify its own inputs. D1 removes it; D4 replaces it
  with `byz.verify` plus `data/`.

## Maintainer decisions (fixed requirements)

**D1 - remove `editions/<edition>/source/` entirely.** Editions keep only
`csv/`, `tei/`, `manifest.json`, and `README.md`. No input snapshot remains
anywhere under `editions/`. The edition is an output, not a partial input tree.

**D2 - materialise the 2019 source files into `data/` (corrected 2026-11-25;
regeneration confirmed).** Only the edition's inputs move: the 57 files in
`textonly-beta-code/` (30 `.CCT`) and `parsed/` (27 `.UB5`). They are committed
under `data/raw/rp2005-2019/`, with `data/provenance/rp2005-2019.toml` recording
tag `v2.0.3`, commit `8ec95671e463030347c2c643358eb56e58235b19`, and a per-file
SHA-256 list. The tag's 113 released CSV/TEI files are neither inputs nor the
edition's outputs: `byz.build` regenerates every `rp2005-2019` view from the 57
sources with the current pipeline (Correction 2), and the released artifacts
remain evidence of the 2019 converter's output. Exact location and contents:
D7.

**D3 - manifests pin inputs by path + hash.** Replace `source_files` with an
`inputs` list of `{root, include, files}` groups. `root` is repo-relative and
always under `data/`; `files[].path` is relative to `root`; each file carries
`sha256` and `size`. `artifact_files` stays edition-relative. Exact schema:
"Manifest schema" below.

**D4 - add `byz.verify`.** `PYTHONPATH=src python3 -m byz.verify [edition ...]`
checks each edition's manifest against the files in `data/` (inputs) and the
committed `csv/`/`tei/` (artifacts), failing loud with the edition, path, and
expected/actual hash. It replaces the self-containment that D1 removes. Exact
behaviour: D8.

## Decisions this spec finalises

These are decisions the brief leaves open. They are adopted throughout; the
maintainer may reject any of them, in which case the referenced requirements
change (see "Decision required" at the end).

**D5 - `byz.recover` becomes `byz.materialise` (corrected 2026-11-25).** The
command materialises `data/raw/rp2005-2019/` and writes
`data/provenance/rp2005-2019.toml` from tag `v2.0.3`. It writes nothing under
`editions/`, and `byz.build` never calls it. The old `byz.recover` name is
deleted, with no alias and no compatibility shim.

**D6 - the historical edition is regenerated, not copied (corrected
2026-11-25, superseded by Correction 2).** `build_historical` generates every
CSV/TEI view from `data/raw/rp2005-2019/` with the same readers as the other
editions: the accented views from `textonly-beta-code`, and the unaccented,
Strong's, and TEI views from `parsed`. It reads no git tag, applies no MAR 16:8
post-correction, and does not copy the release's CSV/TEI. The 113 released
files are evidence of the 2019 converter's output; the edition published here
corrects its malformed apparatus codes (`{Ν`/`{Β` -> `{NA`/`{Byz`) and
normalises typography while keeping the main text's words.

**D7 - location and layout of the historical input tree (corrected
2026-11-25; regeneration confirmed).** Use `data/raw/rp2005-2019/` with the
tag's two source prefixes unchanged:

```
data/raw/rp2005-2019/
  textonly-beta-code/*.CCT    (30)
  parsed/*.UB5                (27)
```

The released-artifact prefixes are not part of this tree and no build path
reads them. `data/raw/<edition>/` is the established per-edition input root,
and the two names are the immutable tag names. The released-artifact names
remain only in the materialiser's documentation and the tests that record the
tag's history, so the retired-path sweep still has a meaningful allowlist.

**D8 - `byz.verify` CLI and downloaded editions.** In repo mode it verifies the
named editions (default: all four, registry order) against `data/` and their
own `csv/`/`tei/`. `--edition-dir PATH` verifies one extracted edition's
manifest and artifacts and **skips inputs**, because inputs are no longer
shipped with an edition; the command says so in its report. Exit codes: `0` all
verified, `1` any mismatch/missing/invalid manifest, `2` usage error. It never
writes and never uses the network. Exact output: `validation.md` §5.

**D9 - `byz.build` stages the views.** Removing the snapshot staging removes
the only code that deleted stale edition files. `build_all`
builds `csv/` and `tei/` in a sibling staging directory and swaps them in on
success, so a failed build leaves the committed views untouched.
`manifest.json` and `README.md` are written after the swap. This preserves the
old "a failed recovery must not destroy the edition" property under the new
owner.

**D10 - the docs record the retirement.** `docs/EDITIONS.md` gains a dated
"Where the edition snapshots went (2026-11-25)" section that maps each retired
snapshot path to its `data/` home and explains the self-verification tradeoff.
The 2026-11-21 moved-paths table keeps its rows but gains a note that
`byz.materialise` now restores the historical inputs and is not part of the
normal build.

## Manifest schema

`editions/<edition>/manifest.json` is written by
`json.dumps(manifest, indent=2, sort_keys=True) + "\n"`. Lists have a canonical
order; object keys are sorted by `sort_keys`. No timestamps, hostnames, or
absolute paths.

Top-level keys are unchanged except `source_files` (removed) and `inputs`
(added). `artifact_files` is unchanged in meaning and order. The example shows
two of the 57 historical source files; the real list is complete.

```json
{
  "artifact_files": [
    {
      "path": "csv/accented/no-variants/MAT.csv",
      "sha256": "…",
      "size": 123456
    }
  ],
  "basis": "The 2019 sources (textonly-beta-code + parsed), rebuilt by the current pipeline",
  "commit": "8ec95671e463030347c2c643358eb56e58235b19",
  "edition": "rp2005-2019",
  "first_release": "v1.0.0",
  "generated_by": "PYTHONPATH=src python3 -m byz.build",
  "inputs": [
    {
      "files": [
        {
          "path": "parsed/MT.UB5",
          "sha256": "…",
          "size": 123456
        },
        {
          "path": "textonly-beta-code/MT.CCT",
          "sha256": "…",
          "size": 234567
        }
      ],
      "include": [
        "parsed/*.UB5",
        "textonly-beta-code/*.CCT"
      ],
      "root": "data/raw/rp2005-2019"
    }
  ],
  "latest_release": "v2.0.3",
  "pdf": "",
  "pdf_url": "",
  "release_range": "v1.0.0-v2.0.3",
  "status": "released",
  "tag": "v2.0.3",
  "title": "Robinson-Pierpont 2005 lineage, 2019 repo revision"
}
```

Rules:

1. `inputs` is a non-empty list. Sort groups by `(root, include)`; sort
   `include`; sort `files` by `path`. A build that constructs the same groups in
   a different order still writes the same JSON.
2. `root` is a repo-relative POSIX path, always under `data/` and never under
   `editions/`. It contains no `..`, no absolute prefix, and no backslash.
3. `files[].path` is a POSIX path relative to `root`; it contains no `..` and
   no leading `/`.
4. `files` is exactly the set matched by `root` + `include` (a missing or extra
   matched file is a verification failure, not a silent pass).
5. `files[].sha256` is 64 lowercase hex characters; `size` is a non-negative
   integer. The same shape is used for `artifact_files`.
6. `artifact_files[].path` is relative to the edition directory and starts with
   `csv/` or `tei/`.
7. `source_files` is absent. A manifest that contains both `inputs` and
   `source_files`, or neither, is invalid.
8. The edition-specific keys (`tag`, `commit`, `source_commit`,
   `strongs_commit`, `pdf_sha256`, `pdf_size`, `ascii_source`,
   `preformatted_source`) are unchanged. `ascii_source` and
   `preformatted_source` stay as archive pointers even though the ASCII files
   are now also hashed in `inputs`.

Per-edition input groups:

| Edition | `root` | `include` | Files |
| --- | --- | --- | ---: |
| `rp2005` | `data/raw/rp2005/editions-rp2-ccat` | `*.CCT` | 29 |
| `rp2005` | `data/raw/rp2005/editions-rp2-ascii` | `*_Byz.txt` | 27 |
| `rp2018` | `data/raw/rp2018/rp2018-ccat` | `*.CCT` | 30 |
| `rp2018` | `data/raw/rp2018/rp2018-ascii-one-line-per-verse` | `*_Byz.txt` | 27 |
| `rp2018-2023` | `data/text` | `CCAT/*.TXT`, `Strongs/*.BP5` | 56 |
| `rp2005-2019` | `data/raw/rp2005-2019` | `parsed/*.UB5`, `textonly-beta-code/*.CCT` | 57 |

The totals are 226 inputs and 672 artifacts. The 113 `v2.0.3` released files
are neither inputs nor published outputs here (Correction 2).

## Requirements

### R1 - Delete the edition snapshots (D1)

1. `editions/<edition>/source/` does not exist for any edition. `git ls-files
   'editions/*/source/*'` is empty. No stub, symlink, or `.gitkeep` replaces it.
2. Each edition directory contains exactly `csv/`, `tei/`, `manifest.json`, and
   `README.md`. The tracked file count under `editions/` drops from 852 to 680.
3. No build, diff, contract, reconciliation, or docs module reads a path under
   `editions/<edition>/source/`. `grep -R '"/source"\|/ "source"' src/byz` finds
   no such path.
4. The historical edition keeps all five CSV views and both TEI views, but they
   are **regenerated** from `data/raw/rp2005-2019/` by the current pipeline
   (Correction 2). Only its inputs move to `data/`.

### R2 - Materialise the 2019 source files under `data/` (D2, D7)

1. `data/raw/rp2005-2019/` contains the tag's two source prefixes: 57 files
   (30 `.CCT` + 27 `.UB5`), byte-identical to `git archive v2.0.3` at the same
   paths. It contains no released `csv-unicode/` or `tei-xml-unicode/` files.
2. `data/provenance/rp2005-2019.toml` is generated with
   `generated.toml_header()` and contains:
   - `edition = "rp2005-2019"`;
   - `tag = "v2.0.3"`;
   - `commit = "8ec95671e463030347c2c643358eb56e58235b19"`;
   - `extracted = "data/raw/rp2005-2019"`;
   - `generated_by = "PYTHONPATH=src python3 -m byz.materialise"`;
   - `method = "git archive v2.0.3"`;
   - one `[[prefixes]]` block per data prefix (`parsed/`, `textonly-beta-code/`),
     with `path` and `files`;
   - one `[[files]]` block per file, sorted by `path`, with `path`, `sha256`,
     and `size`.
   It has no `downloaded`/timestamp field and no URL. It is deterministic.
3. `byz.materialise` writes both the tree and the provenance. It reads
   `git archive v2.0.3` in memory, maps the two source prefixes to the same
   names under `data/raw/rp2005-2019/`, asserts the expected file count per
   prefix (30/27), and fails loud on any mismatch.
4. Materialisation is idempotent: a second run writes no byte and exits 0. It
   validates the whole destination before writing anything: if a destination
   file exists with different bytes, it fails with the path and both hashes
   instead of overwriting; a stray extra file under `data/raw/rp2005-2019/` is
   a failure, not a silent deletion. Only after the validation passes are
   missing files written.
5. `byz.build` does not call `byz.materialise`. The committed tree is already
   present; a normal rebuild reads it.
6. `data/raw/rp2005-2019/` is not an official archive extract. The docs say so,
   and `data/provenance/rp2005-2019.toml` records its git origin.
7. The retired-path sweep (`tests/curate/test_current_pipeline.py`) is updated:
   `tests/curate/test_materialise.py` is allowlisted because it records the tag
   prefix mapping; no generated manifest, provenance file, live data path, or
   `src/byz/curate/build.py` may contain `csv-unicode/` or `tei-xml-unicode/`.
   The released-artifact prefixes remain only in the tests that record the
   tag's history and in `docs/EDITIONS.md`'s retired-paths table.

### R3 - Build from `data/` only (D5, D9)

1. `src/byz/curate/editions.py` registers the input directories for every
   edition:
   - `rp2005-2019`: `source_dir = "data/raw/rp2005-2019/textonly-beta-code"`,
     `parsed_dir = "data/raw/rp2005-2019/parsed"`, and the tag `v2.0.3` with
     its commit as registry metadata (the build never resolves the tag);
   - `rp2018-2023`: `source_dir = "data/text/CCAT"`,
     `strongs_dir = "data/text/Strongs"`;
   - the official entries keep `source_dir`, `ascii_dir`, and
     `preformatted_dir`.
   A test asserts the current `source_dir` resolves to `paths.CCAT_DIR`.
2. `build.build_official` reads `editions.ROOT / edition["source_dir"]` and
   `editions.ROOT / edition["ascii_dir"]`; it gains an
   `edition_dir: Path | None = None` parameter and writes only under that
   directory.
3. `build.build_historical`:
   - generates the accented no-variants and with-variants CSV from
     `data/raw/rp2005-2019/textonly-beta-code/` with `parse_cct_accented`;
   - generates the Strong's views and `csv/unaccented` from
     `data/raw/rp2005-2019/parsed/` with `parse_parsed_ub5`; the reference for
     its parenthetical-verse routing is the accent-free, punctuation-free form
     of the accented view just generated from the same `.CCT` source (no
     released artifact is read);
   - generates `tei/unaccented` from the unaccented text and `tei/accented`
     from the accented no-variants text;
   - reads no git tag, copies no released CSV/TEI, and applies no MAR 16:8
     post-correction;
   - gains an `edition_dir` parameter and writes only under it.
4. `build.build_current` reads `data/text/CCAT` and `data/text/Strongs`; its
   `source/` snapshot code, labels, and docstring are removed. The error
   messages name `data/text/...`, not `editions/<id>/source/...`.
5. `build.build_all` no longer calls `recover.recover_all()`. For each edition it
   builds `csv/` and `tei/` into a sibling `.<id>.staging/` directory, swaps
   them into the edition on success, then writes `manifest.json` and
   `README.md`. A failure removes the staging directory and leaves the
   committed `csv/`/`tei/` untouched.
6. `build._readme` no longer has a `source/` layout row or the "frozen copy"
   paragraph; it says the edition contains outputs and that `manifest.json`
   pins the inputs under `data/`.
7. `src/byz/curate/diff.py` loads the source tier from
   `editions.ROOT / edition["source_dir"]` for official and historical editions,
   and from `data/text/CCAT` for the current edition. `reports/diffs/**` changes
   only for the two pairs that include `rp2005-2019`; its source-tier counts are
   unchanged, while the exact Unicode text (paragraph markers, apostrophes, and
   apparatus codes) now comes from the regenerated edition.
8. `src/byz/curate/materialise.py` replaces `recover.py` and keeps only the
   git-archive reader, the two source prefixes, the conflict-checked writer,
   and `materialise_historical(dest_root=None)`. The snapshot functions and
   `_copy_data_files` are deleted, along with the old `src/byz/recover.py`
   entry point and `tests/curate/test_recover.py`.

### R4 - Manifests pin inputs by path and hash (D3)

1. `write_manifest` writes `inputs` per "Manifest schema" and omits
   `source_files`.
2. The input groups come from one helper, `build._input_groups(edition)`, which
   uses the registry's input directories. It does not hardcode `data/...`
   strings that are not also in the registry, except for the fixed historical
   prefix names.
3. A shared helper `src/byz/curate/files.py` provides:
   - `sha256_file(path) -> str`;
   - `matching_files(root, includes) -> dict[str, Path]`.
   Build and verify both use it, so the set that is hashed is the set that is
   verified.
4. `write_manifest` refuses to hash an input group whose `root` is under
   `editions/` or outside `data/`; this is the D1 invariant in code.
5. Every input file's hash is computed from the working-tree file, not from git;
   `input` paths are repo-relative, so the manifest is portable across clones.
6. `artifact_files` keeps the same 672 entries in count. The 477 entries for
   `rp2005`, `rp2018`, and `rp2018-2023` keep their `path`, `sha256`, and
   `size`; the 195 `rp2005-2019` entries are regenerated and change (Correction
   2).
7. `generated_by` stays `"PYTHONPATH=src python3 -m byz.build"`. The commit keys
   are unchanged in meaning; `source_commit`/`strongs_commit` still use the
   `data/text` pathspecs.

### R5 - `byz.verify` (D4, D8)

1. `PYTHONPATH=src python3 -m byz.verify [edition ...]` exists and verifies the
   named editions (default: all four, registry order).
2. For each edition it checks:
   - the manifest exists, parses, and (in repo mode) has `edition` equal to the
     directory name; in `--edition-dir` mode the manifest's `edition` id is
     used as-is, so the directory may have any name;
   - `source_files` is absent and `inputs` is a valid non-empty list;
   - every `inputs[].root` is relative, under `data/`, and not under
     `editions/`; in repo mode it also exists;
   - every `inputs[].include` entry is a relative glob with no `..` and no
     absolute or backslash prefix;
   - in repo mode, for every group, the actual set of files matched by
     `root` + `include` is exactly the manifest's `files` set;
   - in repo mode, every input file exists, and its `sha256` and `size` match;
     in `--edition-dir` mode the input fields are shape-checked but not
     resolved (inputs are not shipped);
   - every `artifact_files[].path` starts with `csv/` or `tei/` and stays inside
     the edition directory;
   - the actual set of files under `csv/` and `tei/` is exactly the manifest's
     artifact set;
   - every artifact's `sha256` and `size` match;
   - if `pdf` and `pdf_sha256` are present, the committed PDF matches.
3. Failures are loud and name the edition, the repo-relative path, and both the
   expected and actual value. It reports every failure, not just the first.
4. Output and exit codes:
   - success, one line per edition, e.g.
     `OK rp2018-2023: 56 inputs, 195 artifacts`; final
     `verified 4 editions (226 inputs, 672 artifacts)`; exit 0.
   - failure: `FAIL <edition>: <path>: sha256 expected <hex>, actual <hex>` (or
     `missing`, `unexpected`, `size expected …, actual …`); final
     `verified N editions, M failed`; exit 1.
   - usage error: a message on stderr naming the bad argument and the valid
     edition ids; exit 2.
5. `--edition-dir PATH` reads `PATH/manifest.json`, verifies its `csv/`/`tei/`
   against the manifest, and skips input checks with an explicit
   `inputs skipped (external edition directory)` note. It cannot be combined
   with positional edition ids. This is how a downloaded edition is checked for
   artifact integrity; its inputs are not shipped.
6. It never writes, never downloads, and never needs a git checkout beyond the
   committed files.
7. `src/byz/verify.py` is a thin `main(argv=None)` entry point; the logic lives
   in `src/byz/curate/verify.py`.

### R6 - `byz.materialise` (D5)

1. `src/byz/materialise.py` prints what it materialised, e.g.
   `materialised data/raw/rp2005-2019 (57 files)` and
   `wrote data/provenance/rp2005-2019.toml`; it never prints an edition path.
2. `src/byz/curate/materialise.py` has no `_staging`, `_swap`, `_recover`,
   `recover_official`, `recover_current`, `recover_all`, or `_copy_data_files`.
3. It writes only `data/raw/rp2005-2019/` and
   `data/provenance/rp2005-2019.toml` under `dest_root` (default: repository
   root). A test passes a temporary `dest_root` and asserts the file set and
   hashes without touching the repository.
4. `byz.build` and `byz.diff` do not import `materialise`. The `byz.recover`
   module and command are deleted.
5. The docs state that `byz.materialise` is an ingest command, not part of the
   normal rebuild; `byz.build` reads the committed `data/` tree.

### R7 - Contract, history, and reports (D10)

1. `src/byz/contract/paths.py` `DERIVATION_EVIDENCE` no longer says
   `recover.recover_all copies data/text/... into the editions/.../source
   snapshot`; it names `build_current` reading `data/text/...` directly.
2. `src/byz/contract/report.py`'s `docs/DATA_CONTRACT.md` introduction names
   the committed `data/` inputs for each edition, not a frozen snapshot.
3. `src/byz/contract/history.py` keeps its pre-move git pathspecs (they are git
   selectors, not working-tree paths); `data/text` remains in
   `CORPUS_PATHSPECS`; `editions` remains because manifests and editions are
   corpus files. No path is removed from history.
4. `docs/PROVENANCE.md` gains one sentence in "Historical lineage" pointing at
   `data/raw/rp2005-2019/` and `data/provenance/rp2005-2019.toml`. It is rendered
   by `src/byz/reconcile/report.py`; do not hand-edit it.
5. `reports/baseline/derivations.csv` and `docs/DATA_CONTRACT.md` change only
   through the evidence strings. `reports/baseline/files.csv` changes only for
   the three documentation rows it inventories (`README.md`,
   `data/text/README.md`, `docs/BUILD.md`); it does not invent `data/raw/` or
   snapshot rows. Record the row delta in `validation.md`.
6. `reports/diffs/**` changes only for the two pairs that include
   `rp2005-2019` (`rp2005--rp2005-2019` and `rp2005-2019--rp2018`); the other
   two pairs stay byte-identical, and the source-tier counts are unchanged.

### R8 - Public docs, TECH.md, and agent instructions (D10)

1. `src/byz/curate/README.template.md`:
   - the `editions/` layout row no longer says "self-contained (source, CSV,
     TEI, manifest, README)";
   - the `data/` row includes `raw/rp2005-2019/` and `provenance/`;
   - the "Source of truth and provenance" paragraph points at
     `data/raw/rp2005-2019/` and `data/provenance/rp2005-2019.toml` for the
     historical input tree;
   - the `src/` row lists `fetch.py`, `recover.py`, `build.py`, `diff.py`, and
     `verify.py`;
   - "Reproducing the curated data" drops the old recovery step from the
     normal sequence and adds `byz.verify`; it says `byz.materialise` only
     restores `data/raw/rp2005-2019/` and is not needed when that tree is
     present;
   - the paragraph about freezing inputs is replaced by the new role;
   - "The recovery and the tests also need the full git history" becomes "The
     materialisation and the worktree-based tests…".
2. `data/text/README.md`: the paragraph "This folder is not
   `editions/<edition>/source/`…" is replaced by one that says `data/text/` is
   an input, editions contain only outputs, and `manifest.json` pins the inputs
   by repo-relative path and hash.
3. `docs/BUILD.md`:
   - "The input tree" lists `data/raw/rp2005-2019/` and says editions have no
     snapshots;
   - "The pipeline" describes `byz.materialise` as the historical-input
     materialiser, `byz.build` as the only view producer (reading `data/`), and
     `byz.verify` as the checker;
   - the run sequence is `fetch --verify`, `build`, `diff`, `contract`,
     `reconcile`, `verify`; `materialise` is documented separately;
   - a "Verifying the editions" section documents the manifest schema, the
     `byz.verify` output/exit codes, and `--edition-dir`;
   - "The recovery and the worktree-based tests…" is reworded for
     materialisation.
4. `src/byz/curate/docs.py`:
   - `docs/EDITIONS.md` "Layout, exports, and verification" says each edition
     has `csv/`, `tei/`, `manifest.json`, `README.md`; inputs are under `data/`
     and pinned in `inputs`;
   - the snapshot paragraph (lines 237-241) is replaced by the new dated
     section;
   - a new `SNAPSHOT_MOVES` constant and section
     `## Where the edition snapshots went (2026-11-25)` map each retired
     snapshot to its `data/` home and state that editions are no longer
     self-verifiable; a second small table records the `v2.0.3`
     `csv-unicode/` / `tei-xml-unicode/` tag prefixes mapping to
     `editions/rp2005-2019/{csv,tei}/` so the released-artifact recovery is
     auditable without pretending those files are inputs;
   - the "Rebuilding the curated editions" block drops the old recovery step
     and adds `byz.verify`; it mentions `byz.materialise` only for restoring the
     historical input tree;
   - the 2026-11-21 moved-paths sentence about `source_files` is corrected:
     `artifact_files` hashes are unchanged, and `source_files` was replaced by
     `inputs` on 2026-11-25;
   - the source feature matrix says the `v2.0.3` `textonly-beta-code` and
     `parsed` files are also committed at `data/raw/rp2005-2019/`;
   - `_curated_editions_section()` no longer says "own input snapshot".
5. `src/byz/generated.py`: remove the `editions/<edition>/source/` row; add one
   row for `` `data/raw/rp2005-2019/` `` and
   `` `data/provenance/rp2005-2019.toml` `` with command
   `` `PYTHONPATH=src python3 -m byz.materialise` `` and patterns
   `("data/raw/rp2005-2019/**", "data/provenance/rp2005-2019.toml")`. The
   registry stays at 12 rows.
6. `SPECS/TECH.md`:
   - §5 removes `editions/<edition>/source/` from the layout and the prose,
     adds `data/raw/rp2005-2019/`, and states the inputs -> pipeline -> outputs
     rule, the manifest `inputs` schema, and `byz.verify`;
   - §2 adds the 2019 lineage under `data/raw/rp2005-2019/` and its
     provenance;
   - §3 adds git-tag provenance as a provenance kind;
   - §8 says editions contain only outputs and the manifest pins the inputs;
   - §9 adds `byz.verify` as the clean-tree integrity check;
   - §11 lists `fetch`, `materialise`, `build`, `diff`, `verify` and the no-snapshot
     rule.
7. `.opencode/**` (the 10 files listed in
   `SPECS/2026-11-21-input-and-code-layout/` R7.3) describes the new role:
   `byz.build` reads `data/`; `byz.verify` checks; `byz.materialise` only
   restores the historical inputs. No agent instruction says to run a recovery
   step before the build.
8. Per-edition `README.md` (generated by `build._readme`) drops the
   `source/` layout row and the "frozen copy / downloaded and verified on its
   own" paragraph. It says the edition is outputs only and `manifest.json`
   points into `data/`. The `rp2018-2023` README no longer says the snapshot
   duplicates `data/text/`.

### R9 - Byte identity, determinism, and tests

1. Every file under `editions/{rp2005,rp2018,rp2018-2023}/{csv,tei}` is
   byte-identical to the pre-change tree (477 files). `rp2005-2019` is
   regenerated and changes by design (Correction 2). No file is added or
   removed under `editions/*/{csv,tei}`: 672 files before and after.
2. For `rp2005`, `rp2018`, and `rp2018-2023`, every `artifact_files` entry keeps
   its `path`, `sha256`, and `size`. For `rp2005-2019` the entries are
   regenerated. The only manifest key differences are `source_files` (removed)
   and `inputs` (added); `rp2005-2019`'s `basis` and `note` also change.
3. `reports/diffs/**` changes only for the two pairs that include
   `rp2005-2019`; the other two pairs are byte-identical.
4. No `.TXT` or `.BP5` file under `data/text/`, and no file under
   `data/raw/rp2005/`, `data/raw/rp2018/`, `data/raw/_archives/`,
   `data/provenance/rp2005.toml`, or `data/provenance/rp2018.toml` changes.
   `data/text/README.md` is edited for documentation (R8.2). The only additions
   under `data/` are `data/raw/rp2005-2019/` and
   `data/provenance/rp2005-2019.toml`.
5. A second full regeneration is byte-identical. No timestamp, hostname, or
   absolute path appears in a generated file.
6. The three suites pass: `tests/contract`, `tests/curate`,
   `tests/reconciliation`. `tests/curate/test_reproducible.py` passes after the
   committed change and the follow-up regeneration commits (see `validation.md`
   §8).
7. The historical input tree is verified against `git archive v2.0.3` in a test
   and in `validation.md`; the test does not write the repository.
8. `byz.verify` is tested clean, with a corrupted input hash, with a corrupted
   artifact hash, with a missing artifact, with an extra input, with a legacy
   `source_files` manifest, with an absolute/`..` path, and with
   `--edition-dir`.
9. `tests/curate/test_historical_pipeline.py` pins the regeneration: the
   committed views equal a fresh `build_historical` output, no with-variants
   file contains a Greek code initial (`{Ν`/`{Β`, or any `{` + Greek capital),
   a sample of labels is `{NA`/`{Byz`, the four blank verses are emitted as
   empty records, the manifest pins the 57 inputs, and the regenerated accented
   main text matches the `v2.0.3` release's words after normalising `¶` and
   apostrophes.

## Breaking changes

| Removed | Replacement |
| --- | --- |
| `editions/<edition>/source/` | `data/` inputs pinned by `manifest.json` `inputs`; `byz.verify` |
| `manifest.json` `source_files` | `manifest.json` `inputs` (`root`, `include`, `files`) |
| `byz.recover` freezing edition snapshots | `byz.materialise` restoring 57 source files under `data/raw/rp2005-2019/`; `byz.build` reads `data/` |
| `editions/<edition>/source/` in the README generated-files table | `data/raw/rp2005-2019/` and its provenance row |
| An edition that verifies itself without `data/` | `byz.verify` with `data/`; an extracted edition is artifact-only |

No shims, no aliases, no duplicated `source_files`.

## Acceptance criteria

- `editions/<edition>/source/` does not exist; `git ls-files 'editions/*/source/*'`
  is empty; each edition has exactly `csv/`, `tei/`, `manifest.json`, and
  `README.md`; `editions/` has 680 tracked files.
- `data/raw/rp2005-2019/` has 57 source files matching `git archive v2.0.3`;
  `data/provenance/rp2005-2019.toml` records the tag, the commit, and every
  file's hash/size, with no timestamp. Every `rp2005-2019` CSV/TEI view is
  regenerated from those files by `byz.build`; no release artifact is copied.
- Every manifest has `inputs` and no `source_files`; every `inputs[].root` is
  under `data/`; every file resolves; the input sets match their `include`
  globs. `artifact_files` is unchanged for the three non-historical editions and
  regenerated for `rp2005-2019`.
- `PYTHONPATH=src python3 -m byz.verify` exits 0 on the clean tree and reports
  `226 inputs, 672 artifacts`. A deliberately corrupted input hash exits 1 and
  prints the edition, path, expected hash, and actual hash. An unknown edition
  exits 2. `--edition-dir` verifies an extracted edition's artifacts and says
  inputs were skipped.
- The 477 CSV/TEI files of `rp2005`, `rp2018`, and `rp2018-2023` are
  byte-identical; `rp2005-2019` changes as Correction 2 describes. No file is
  added or removed under `editions/*/{csv,tei}` (672 before and after). The two
  diff-report pairs that include `rp2005-2019` change; the other two are
  byte-identical.
- `rp2005-2019/csv/accented/with-variants/*.csv` contains no Greek code initial;
  the same view carries `{NA` and `{Byz`, and the regenerated accented main text
  matches the `v2.0.3` release's words after normalising `¶` and apostrophes.
- The full sequence runs twice with no diff; no generated file has a timestamp,
  hostname, or absolute path.
- The three suites pass; `README.md`, `docs/EDITIONS.md`, `docs/BUILD.md`,
  `docs/DATA_CONTRACT.md`, `docs/PROVENANCE.md`, `data/text/README.md`,
  `editions/*/README.md`, `SPECS/TECH.md`, and `.opencode/**` describe the new
  model; no public doc tells a reader to use `editions/<edition>/source/` or to
  run a recovery step before `byz.build`.
- No text, archive, PDF, or `.TXT`/`.BP5` input content changed; the only
  documentation edit under `data/text/` is `data/text/README.md`.

## The self-verification tradeoff

D1 removes the property that an edition directory alone contains enough to
verify its inputs. This is intentional, and it is the price of the inputs ->
pipeline -> outputs model:

- A **repository checkout** verifies inputs and artifacts with `byz.verify`.
- A **downloaded edition** verifies its artifacts (the files it ships) against
  `manifest.json` with `byz.verify --edition-dir PATH`. It cannot prove that its
  CSV/TEI were built from the pinned inputs, because the inputs are not shipped.
- `manifest.json` still names every input by repo-relative path and hash, so the
  edition is traceable to `data/` without embedding a second copy.
- The alternative (keep the snapshots) preserves self-verification but keeps
  inputs inside outputs and keeps two copies of 11.6 MB of data. The maintainer
  chose the model over the copy; this spec records the cost.

## Resolved decision: the historical released artifacts (superseded)

The original draft treated the 113 released `v2.0.3` CSV/TEI files as inputs and
proposed materialising all 170 files. The maintainer corrected this on
2026-11-25: only the 57 `textonly-beta-code`/`parsed` files are inputs, and they
are committed under `data/raw/rp2005-2019/`.

**Correction 2 supersedes the second half of that decision.** The 113 released
files are not the edition's published outputs here. They are evidence of what
the 2019 converter produced, including 7,482 malformed apparatus markers and
1,920 typography-only verse differences (measured after `¶` + apostrophe
normalisation). `byz.build` regenerates every
`rp2005-2019` view from the 57 sources with the current pipeline; the docs say
so in `docs/BUILD.md`, `docs/EDITIONS.md`, and `docs/PROVENANCE.md`.

## Risks

- **Historical regeneration.** The fragile part is now the source-to-view
  conversion: a wrong reader, book mapping, or verse-segmentation reference
  changes hundreds of rows. `tests/curate/test_historical_pipeline.py` rebuilds
  the whole edition into a temporary directory and compares it byte-for-byte
  with the committed tree, and it checks the accented main text against the
  release's words.
- **Malformed apparatus codes.** The reason for the regeneration is that the
  2019 release carried `{Ν`/`{Β`; a test forbids any Greek capital after `{` in
  the generated with-variants files, so the bug cannot silently return.
- **PARENTHETICAL VERSES.** `parse_parsed_ub5` needs a reference to decide
  whether a `(chapter:verse)` note inside a `.UB5` verse is an alternative
  numbering or a verse boundary. The build derives it from the accented view
  generated from the same `.CCT`; if that reference is empty, ACT 24:2 and REV
  17:8 lose text. The byte-identity rebuild test catches it.
- **Parsing reference.** `build_historical` derives the `.UB5` segmentation
  reference from the accented view generated from the same `.CCT` source, not
  from a released `csv/unaccented`. `csv/unaccented` and `csv/strongs/
  no-parsing` are now the same text (a test asserts byte identity); the
  byte-identity rebuild test proves the segmentation.
- **Manifest schema drift.** `inputs` is a new format; an external consumer that
  reads `source_files` breaks. This is documented as a breaking change, not
  hidden behind a duplicate key.
- **`include` completeness.** If a group's `include` omits a glob the build
  reads, `byz.verify` passes while the build reads an unpinned file. The groups
  and the build paths must use the same registry keys; the test that compares
  `_input_groups` with the build's read directories locks this.
- **Staging swap.** Moving `_staging`/`_swap` into `build` must preserve the old
  safety: a failed build leaves the committed views intact. Add the test.
- **Retired-path names.** The released-artifact tag prefixes stay only in the
  retired-paths documentation and the tests that record the tag's history; they
  do not appear in `build.py`, the manifest, the provenance, or a live data
  path. The retired-path sweep's allowlist names those files.
- **Worktree convergence.** Deleting snapshots and changing manifests touches
  `editions`, which is in `CORPUS_PATHSPECS`; `docs/HISTORY.md`'s "Last corpus
  commit" moves. Expect the same two-follow-up-commit convergence as the
  2026-11-21 change; record it in `validation.md`.
- **Dirty baseline.** The working tree at the time of writing had uncommitted
  documentation edits. The byte snapshot is only meaningful from a clean
  commit; commit or stash them before phase 0.

## Sequencing

- Independent of any concurrent spec. Do not edit `SPECS/` folders other than
  this one and `SPECS/TECH.md`.
- The change is self-contained on
  `feature/2026-11-16-edition-recovery-curation`.
- Phase order is mandatory: materialise the data first (phase 1), switch the
  build (phase 2), switch the manifests and add verify (phase 3), delete the
  snapshots (phase 4), then docs (phase 5) and the gates (phase 6). Deleting the
  snapshots before the build reads `data/` breaks the build; writing `inputs`
  before the data exists breaks `byz.verify`.
