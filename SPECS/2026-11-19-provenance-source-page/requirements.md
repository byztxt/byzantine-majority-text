# Requirements - Provenance source page and generated-file banners

## Context

The six official ZIP archives committed under `data/raw/_archives/` were
retrieved in November 2026 from the Byzantine Text editions listing page
<https://byzantinetext.com/study/editions/robinson-pierpont/>. The provenance
records pin each archive's SHA-256 and the per-file Dropbox URL, but they do not
record the page a human actually used to find those files. A reader who wants
to re-check or re-download an archive therefore has to infer the page from the
Dropbox links, and the November 2026 retrieval window is invisible.

Separately, several Markdown files are written by scripts, but a reader cannot
tell which ones. Users hand-edit generated Markdown and open pull requests for
changes that the next generator run overwrites. The generated provenance TOMLs
have the same problem: `fetch_official.py --force` silently replaces them.

This change closes both gaps. It is documentation and provenance plumbing only:
no text, CSV, TEI, archive, or checksum changes.

## Goal

1. Record where the official archives came from, both machine-readably
   (`source_page` on every `[[archives]]` record) and in prose
   (`docs/PROVENANCE.md`, `SPECS/TECH.md` §2).
2. Make generated files self-identifying: a visible banner on every generated
   Markdown file and on the two generated provenance TOMLs, plus one authoritative
   list in the root `README.md` mapping each generated path to the command that
   regenerates it.

## Non-goals

- Re-downloading, re-hashing, re-extracting, or changing any archive, PDF, or
  source file.
- Changing the text, CSV, TEI-XML, manifests, or any checksum in them.
- Adding a banner to CSV, TEI-XML, JSON, `.diff`, or other non-Markdown outputs.
- Bannerizing `data/provenance/pdfs.toml`. It is hand-maintained and stays so.
- Claiming that the whole root `README.md` is generated. It is only partially
  generated; the banner and the list must say so.
- Documenting or resolving the unknown provenance of `source/Strongs/*.BP5`.
- Adding a docs site, a lint step, a pre-commit hook, or a new dependency.
- Re-fetching over the network. The change must be reproducible offline.

## Affected scope

- **Editions:** all four curated editions are affected only through generated
  documentation (`editions/<id>/README.md`, `docs/EDITIONS.md`, the root README
  block). Their source, CSV, TEI, and manifests are unchanged.
- **Inputs touched:** none. The six committed archives are read by
  `fetch_official.py --verify` and by record mode; neither downloads. The
  provenance TOMLs are re-recorded from the committed copies.
- **Outputs touched:** `data/provenance/rp2005.toml`,
  `data/provenance/rp2018.toml`, `docs/PROVENANCE.md`, `docs/EDITIONS.md`,
  `docs/HISTORY.md`, `docs/DATA_CONTRACT.md`, the four `editions/<id>/README.md`,
  `reports/diffs/README.md` and `reports/diffs/<pair>/report.md`,
  `reports/baseline/{summary.md,decision-log.md}`,
  `reports/reconciliation/{summary.md,decision-log.md}`, and the generated
  `<!-- editions:begin -->` ... `<!-- editions:end -->` block of the root
  `README.md`. `SPECS/TECH.md` §2 and the hand-written parts of `README.md` and
  `scripts/README.md` are edited by hand.

## Verified inventory of generated files and writers

Confirmed on branch `feature/2026-11-16-edition-recovery-curation`, 2026-11-19.

| Generated path | Writer |
| --- | --- |
| `docs/EDITIONS.md` | `src/byz/curate/docs.py` `write_editions_doc` (write at line 325), via `scripts/build_editions.py` |
| `editions/<id>/README.md` | `src/byz/curate/build.py` `_readme` / `write_manifest` (write at line 635) |
| `editions/<id>/manifest.json`, `editions/<id>/csv/`, `editions/<id>/tei/` | `src/byz/curate/build.py` |
| `docs/HISTORY.md` | **two writers:** `src/byz/contract/report.py` `_render_history` (write at line 335) and `src/byz/reconcile/report.py` `_update_history` (write at line 444, called from line 496) |
| `docs/DATA_CONTRACT.md` | `src/byz/contract/report.py` `_contract_doc` (write at line 336) |
| `reports/baseline/summary.md`, `reports/baseline/decision-log.md` | `src/byz/contract/report.py` (writes at lines 339-343) |
| `docs/PROVENANCE.md` | `src/byz/reconcile/report.py` `_provenance_doc` (write at line 492) |
| `reports/reconciliation/summary.md`, `reports/reconciliation/decision-log.md` | `src/byz/reconcile/report.py` (writes at lines 487-491) |
| `reports/diffs/README.md` | `src/byz/curate/diff.py` `write_readme` (write at line 540) |
| `reports/diffs/<left>--<right>/report.md` | `src/byz/curate/diff.py` `_report` (write at line 441) |
| root `README.md`, only the `<!-- editions:begin -->` ... `<!-- editions:end -->` block | `src/byz/curate/docs.py` `root_readme_block` / `update_root_readme` |
| `data/provenance/rp2005.toml`, `data/provenance/rp2018.toml` | `src/byz/reconcile/fetch.py` `_write_provenance` (lines 166-187) |

Hand-maintained files in the same area (must stay banner-free and must not be
listed as generated):

- `data/provenance/pdfs.toml` - no code writes it; only
  `tests/curate/test_editions.py:84` reads it.
- `SPECS/*.md`, `source/README.md`, `scripts/README.md`, `essay/README.md`,
  `csv-unicode/README.md`, `tei-xml-unicode/README.md`.

The repository currently contains 17 generated Markdown files (4 under `docs/`,
4 edition READMEs, 5 under `reports/diffs/`, 2 under `reports/baseline/`, 2 under
`reports/reconciliation/`) plus the partially generated root README and the two
generated provenance TOMLs.

## Definitions

- **Source page** - the human-facing listing page from which the six archive
  links were taken: `https://byzantinetext.com/study/editions/robinson-pierpont/`.
- **Retrieval window** - November 2026; the recorded `downloaded` values are
  `2026-11-16T18:37:00Z` through `2026-11-16T18:37:10Z`.
- **Generated file** - a file whose committed content is produced by a script
  and is overwritten on the next run. Generated files must not be hand-edited.
- **Banner** - the fixed header defined in `plan.md`, "Banner wording (exact)":
  an HTML-comment marker used for tests and idempotence, followed by a visible
  Markdown blockquote. For TOML, the same marker and note as `#` comment lines.
- **Record mode** - `python3 scripts/fetch_official.py` with neither `--verify`
  nor `--force`: after `--verify` passes, it reuses the committed archives,
  preserves the recorded `downloaded` and `final_url` values, and rewrites the
  provenance TOMLs offline. It downloads only if an archive is missing or fails
  its digest.

## Maintainer decisions (fixed requirements)

1. This change gets a full spec folder before any implementation.
2. Part A is recorded in both places: a machine-readable `source_page` field on
   every `[[archives]]` record, and prose in `docs/PROVENANCE.md` plus a note in
   `SPECS/TECH.md` §2. The field is emitted by the generator, so
   `fetch_official.py --force` cannot drop it.
3. Banner scope is all generated `.md` files plus
   `data/provenance/rp2005.toml` and `data/provenance/rp2018.toml`. The root
   README gets a new section listing every generated file with its command.
4. `data/provenance/pdfs.toml` is hand-maintained: no banner, not listed as
   generated.
5. The root README is only partially generated; no banner may claim otherwise.
6. Both writers of `docs/HISTORY.md` must preserve the same banner.
7. A second full regeneration must be byte-identical, and the tracked tree must
   be clean afterwards.

## Functional requirements

### Part A - Source page

**A1 - Machine-readable field.** Every `[[archives]]` record in
`data/provenance/rp2005.toml` and `data/provenance/rp2018.toml` carries
`source_page = "https://byzantinetext.com/study/editions/robinson-pierpont/"`,
in a fixed position (after `format`, before `requested_url`).

**A2 - Single source of truth.** The URL is defined once, as
`sources.SOURCE_PAGE` in `src/byz/reconcile/sources.py`. `fetch.py` writes it;
`report.py` uses it for prose. No second literal copy of the URL exists in
Python code.

**A3 - Generator owns the field.** `_write_provenance` includes `source_page` in
its fixed key tuple and `run()` puts it in every record dict. `--force` therefore
re-emits it. A record missing the key must fail loudly rather than write a
partial TOML.

**A4 - Re-record without network.** The provenance TOMLs can be regenerated from
the committed archives without downloading, by running
`python3 scripts/fetch_official.py` (record mode) after `--verify` passes. When
the committed archives are present and match their pinned digests, record mode
reuses them, preserves the existing `downloaded`, `final_url`, `http_status`,
`size`, and `sha256` values, and only adds the banner and `source_page`. It falls
back to a download only if an archive is missing or fails its digest, which
`--verify` has already ruled out. This is the required method for this change;
`--force` must not be used, because it always re-downloads and replaces the
recorded timestamps and Dropbox final URLs.

**A5 - Parser tolerance.** `_existing_records` ignores blank lines and lines
whose first non-space character is `#` before looking for `=`, so a leading
comment banner is tolerated even if a future comment contains `=`.
`fetch_official.py --verify` must still pass with the banner present, must not
download, and must leave both TOMLs byte-identical.

**A6 - Prose.** `docs/PROVENANCE.md` (generated) states the listing page and the
November 2026 retrieval window, and names the `source_page` field. The statement
must be emitted by `_provenance_doc`, not hand-added after generation.
`SPECS/TECH.md` §2 names the same listing page as the origin of the six archives,
in addition to the existing per-file Dropbox URLs.

### Part B - Self-identifying generated documentation

**B1 - One shared banner implementation.** A single module,
`src/byz/generated.py`, owns the banner marker, wording, idempotent insertion,
and the generated-file registry. Every writer calls it; no writer keeps a private
copy of the banner string.

**B2 - Banner scope.** Every file in the verified inventory gets a top banner:
the 17 generated Markdown files, and the two generated provenance TOMLs. The
banner is the first content in the file. In Markdown the visible part renders as
a blockquote; the marker comment makes insertion idempotent and testable.

**B3 - Partial root README.** The root README banner sits immediately after
`<!-- editions:begin -->` and says the block is generated while the rest of the
file is hand-written. It also names `python3 scripts/build_editions.py`. The
hand-written prose above and below the block is preserved byte-for-byte by
`replace_block` / `render_root_readme`.

**B4 - Two HISTORY writers.** `byz.contract` and `byz.reconcile` both apply the
same idempotent banner, so whichever runs last leaves exactly one banner at the
top and the `<!-- cycle2:begin -->` block intact.

**B5 - Exclusions.** `data/provenance/pdfs.toml` receives no banner and
is not listed as generated. `csv-unicode/README.md`, `tei-xml-unicode/README.md`,
`source/README.md`, `scripts/README.md`, `essay/README.md`, and `SPECS/*.md` are
hand-written and receive no banner.

**B6 - Root README list.** The generated block gains a `## Generated files`
section: a table with one row per generated path family and the exact command
that regenerates it, plus a sentence that says the rest of the README and
`data/provenance/pdfs.toml` are hand-maintained. The table is rendered from the
registry in `src/byz/generated.py`, so it cannot drift from the banner scope.

**B7 - Every generated artifact family is covered.** The table also lists
`editions/<id>/source/`, `editions/<id>/manifest.json`, `csv/`, `tei/`,
`docs/contract/*.json`, `reports/baseline/`, `reports/reconciliation/`,
`reports/diffs/`, `csv-unicode/`, and `tei-xml-unicode/`, even though only the
Markdown members carry banners.

**B8 - Runbook.** The root README "Reproducing the curated data" block and
`scripts/README.md` document record mode (`python3 scripts/fetch_official.py`)
as the way to re-record provenance from the committed archives after
`--verify` passes, and warn that `--force` always re-downloads and replaces the
recorded timestamps and final URLs.

### Cross-cutting

**C1 - Determinism.** No timestamps, hostnames, or run-dependent ordering are
added. A second full regeneration produces byte-identical tracked files.
`--force` remains the only mode that changes `downloaded`.

**C2 - Tests.** New tests cover the helper, the `source_page` field, parser
tolerance, record mode, banner presence on every generated file, the
hand-maintained exclusion, and the README registry. Existing tests that assert
document content, exact file equality, or first-line structure are updated.

**C3 - No data change.** `data/raw/`, `source/`, `csv-unicode/`,
`tei-xml-unicode/`, `editions/*/source/`, `editions/*/csv/`,
`editions/*/tei/`, and `editions/*/manifest.json` are byte-identical to before.
Only documentation, provenance TOMLs, and tests change.

**C4 - Public domain and offline.** No new dependency, no license change, no
network access in the test suite or in record mode.

## Acceptance criteria

- `data/provenance/rp2005.toml` and `rp2018.toml` each contain three
  `[[archives]]` records and three `source_page` lines with the exact URL.
- Both TOMLs begin with the TOML banner marker; `pdfs.toml` has neither the
  marker nor a `source_page` field and is unchanged.
- `python3 scripts/fetch_official.py --verify` exits 0 and leaves both TOMLs
  byte-identical.
- `git diff data/provenance/` shows only added banner lines and one added
  `source_page` line per record; `sha256`, `size`, `downloaded`, and `final_url`
  are unchanged.
- All 17 generated Markdown files begin with the Markdown marker and visible
  banner; the root README generated block begins with the block banner and says
  the rest of the file is hand-written.
- `docs/PROVENANCE.md` contains the listing-page URL and "November 2026".
  `SPECS/TECH.md` §2 contains the same URL.
- The root README `## Generated files` table lists every row in
  `generated.GENERATED_FILES`, names the commands, and does not list
  `pdfs.toml` as generated.
- `docs/HISTORY.md` has exactly one banner and exactly one Cycle 2 block after
  `byz.contract` followed by `byz.reconcile`.
- The full regeneration routine runs twice with no diff; the tracked tree is
  clean; all three test suites pass.
- No file under `data/raw/`, `source/`, `csv-unicode/`, `tei-xml-unicode/`, or
  `editions/*/{source,csv,tei,manifest.json}` changed.

## Risks

- **`--force` is tempting and wrong here.** It rewrites `downloaded` to today's
  date and refreshes `final_url`; using it to add a key would create a large,
  misleading diff. Record mode exists precisely for this.
- **Banner breaks the TOML reader.** `_existing_records` currently treats any
  line containing `=` as a key/value pair. A comment such as
  `# source_page = ...` would corrupt the parsed record. The banner must avoid
  `=`, and the parser must skip `#` lines explicitly.
- **Partial-generation claim.** A top-of-file banner on the root README would be
  false. The banner must live inside the generated block.
- **Two HISTORY writers.** Applying the banner in only one writer, or applying
  different wording in each, makes the second run non-deterministic.
- **`pdfs.toml` collateral damage.** A glob such as `data/provenance/*.toml`
  would bannerize a hand-maintained file. The registry must name the two
  generated TOMLs explicitly.
- **Tests that pin exact content.** `reports/diffs/README.md` is compared for
  equality with `diff.README_TEXT`; content assertions in the curate, contract,
  and reconciliation suites need updating when the banner moves line numbers.
- **Registry drift.** A hand-written README table would go stale. Render it from
  the same registry the banner tests use.
