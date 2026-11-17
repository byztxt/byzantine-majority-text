# Validation - Official archive reconciliation (Cycle 2)

A cycle is complete only when every item below is verified against the actual
archives, files, and reports. Attach evidence (archive checksums, report
excerpts, commands) to each check.

> **Note (2026-11-17, PR #46).** The committed reports under
> `reports/reconciliation/`, `docs/PROVENANCE.md`, and the Cycle 2 block in
> `docs/HISTORY.md` were produced with all six archives present in
> `data/raw/_archives/`. Those zips are git-ignored, so a fresh clone cannot
> re-run the archive-dependent comparison until it fetches them
> (`python3 scripts/fetch_official.py --verify`). The archive-dependent boxes
> below are therefore left unticked for offline verification; instead the
> offline suite pins the six SHA-256 values in `src/byz/reconcile/sources.py`
> and checks that they match `data/provenance/*.toml`, and it asserts the
> headline totals in the committed reports (`7811/7972`, `7769/7972`).

## 1. Archives and provenance

- [ ] All six official archives were downloaded from the URLs in
      `requirements.md` with `?dl=1`, following redirects.
- [ ] Each archive has a recorded final URL, status, size, download date, and
      SHA-256 in `data/provenance/rp2005.toml` / `rp2018.toml`.
- [ ] The extracted inputs under `data/raw/<edition>/` are immutable copies.
- [ ] Re-running the fetch against the recorded checksums produces no unexpected
      change; any change is recorded and flagged.
- [ ] The maintainer has decided whether the original zips are committed or only
      the extracted inputs plus checksums.

## 2. Archive inventory

- [ ] `reports/reconciliation/archives.csv` lists every archive member with size,
      hash, encoding, line endings, and format class.
- [ ] Nested directories and naming differences are represented.
- [ ] Inventories are deterministic across two runs.

## 3. Mapping

- [ ] Every archive member is mapped to a current file or explicitly listed as
      unmapped with a reason.
- [ ] Every current source/CSV/TEI file is mapped to an archive member or
      explicitly marked `provenance-unknown`/`not-in-archives`.
- [ ] `04a_PA` and `05a_ACT24` are explicitly accounted for.
- [ ] Renamed/restructured files are documented, not silently normalized.

## 4. Match extent (the central question)

For **each edition** (`rp2005`, `rp2018`) and **each format/archive**, the report
states:

- [ ] the number and percentage of files that are `exact`, `normalized`,
      `textual`, `structural`, `missing`, `extra`, or
      `incomparable-pending-pipeline`;
- [ ] the number of verses identical vs different, per book, with totals;
- [ ] the number of word/variant/parsing/Strong's differences, by category;
- [ ] a one-paragraph plain-language verdict.

Specifically answer, with evidence:

- [ ] Does current `source/CCAT/` match the official 2005 `ccat` archive?
- [ ] Does current `source/CCAT/` match the official 2018 `ccat` archive?
- [ ] If it matches neither, what is it closest to, and where does it deviate?
- [ ] Does current `source/Strongs/` match any official archive? If not, is its
      provenance recorded as unknown and flagged?
- [ ] Do current `csv-unicode/` and `tei-xml-unicode/` correspond to an official
      edition at the text level? Which files are
      `incomparable-pending-pipeline` and why?
- [ ] Is the repo state better modelled as `rp2018` or as `rp2018@2023-07-20`?
      State the evidence.

Raw and normalized results must be presented separately, so encoding and
line-ending noise is not counted as textual change.

## 5. Difference categories

- [ ] Every non-exact difference has at least one category from
      `requirements.md` §R4/R8, or an explicit `other` with an explanation.
- [ ] Spot-check at least five differences per category against the archive and
      source text and confirm the classification.
- [ ] Normalization-only differences are confirmed to disappear under the
      documented normalization.

## 6. Strong's provenance

- [ ] Every archive was searched for parsing/Strong's content.
- [ ] The result is either a mapped comparison or a documented
      `provenance-unknown` with evidence.
- [ ] No provenance was inferred from file names alone.

## 7. Intentional blanks (D7)

- [ ] LUK 17:36, ACT 8:37, ACT 15:34, and ACT 24:7 are confirmed from the
      official archives as absent from the Byzantine tradition.
- [ ] The four verses are still preserved as empty records in the generated CSV
      and TEI after any reconciliation work.

## 8. External history and provenance docs

- [ ] `docs/HISTORY.md` includes the external evidence (archive checksums and the
      files they match) alongside the internal git-history map.
- [ ] `docs/PROVENANCE.md` describes each edition, its archives, checksums, and
      the maintainer's canonical-source decisions.
- [ ] Points where the evidence is insufficient are stated explicitly.

## 9. Determinism and safety

- [ ] Running the comparison twice produces byte-identical reports. *(Archive-
      dependent; not verified offline in PR #46.)*
- [x] `git status` shows no modifications under `source/`, `csv-unicode/`,
      `tei-xml-unicode/`, or `essay/`. *(Verified 2026-11-17: the legacy
      converters reproduce `csv-unicode/` and `tei-xml-unicode/` byte-identically
      and the curated editions live under `editions/`.)*
- [x] No corpus file was moved, deleted, or normalized in place.
- [ ] No canonical source was selected automatically. *(Decision log rows are
      still `pending`; the pipeline only flags.)*
- [x] Tests run offline and pass. *(2026-11-17: `tests/reconciliation` runs 39
      tests with 6 archive-dependent tests skipped; the six pinned hashes and the
      committed report totals are checked without the zips.)*

## 10. Decision log and handoff

- [ ] Every conflict has a row with: id, affected paths, evidence, options, and
      an empty "maintainer decision" field.
- [ ] The decision log is presented to the maintainer.
- [ ] Recorded decisions are added to `docs/PROVENANCE.md`, the relevant
      `data/provenance/<edition>.toml`, and `docs/DATA_CONTRACT.md` if needed.
- [ ] The maintainer has a plain-language answer to "how far do the current files
      match the official 2005/2018 archives?"

## 11. Definition of done

- [x] `data/raw/rp2005/` and `data/raw/rp2018/` exist with provenance records.
- [x] `reports/reconciliation/{summary.md,archives.csv,files.csv,verses.csv,categories.csv,decision-log.md}` exist.
- [x] `docs/PROVENANCE.md` exists and `docs/HISTORY.md` is updated. *(The Cycle 2
      block is preserved across `byz.contract` regeneration; see
      `tests/contract/test_integration.py`.)*
- [ ] Tests are green; reports are deterministic; corpus files are untouched.
      *(Offline tests are green and the corpus files are untouched; report
      determinism cannot be re-checked without the archives.)*
- [ ] The plan's task groups are complete, or every deviation is recorded here.
