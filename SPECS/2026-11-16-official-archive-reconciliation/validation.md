# Validation - Official archive reconciliation (Cycle 2)

A cycle is complete only when every item below is verified against the actual
archives, files, and reports. Attach evidence (archive checksums, report
excerpts, commands) to each check.

> **Note (2026-11-17, PR #46).** The six official zips are committed under
> `data/raw/_archives/<edition>/` and are pinned by SHA-256 in
> `data/provenance/*.toml`; the extracted inputs under `data/raw/<edition>/`
> are produced from those zips (they are not separately hashed in the
> provenance files). A normal checkout can therefore re-run the
> archive-dependent comparison offline
> (`PYTHONPATH=src python3 -m byz.reconcile`), and
> `python3 scripts/fetch_official.py --verify` checks the committed copies
> against the pinned digests without network access and without writing.
> The committed reports under `reports/reconciliation/`,
> `docs/PROVENANCE.md`, and the Cycle 2 block in `docs/HISTORY.md` were
> regenerated from those archives. The offline suite pins the six SHA-256 values
> and checks that they match `data/provenance/*.toml`, asserts the headline
> totals in the committed reports (`7811/7972`, `7769/7972`), and checks that
> the committed zips are not git-ignored.

## 1. Archives and provenance

- [ ] All six official archives were downloaded from the URLs in
      `requirements.md` with `?dl=1`, following redirects. *(Original download;
      not re-runnable offline. `--force` repeats it.)*
- [x] Each archive has a recorded final URL, status, size, download date, and
      SHA-256 in `data/provenance/rp2005.toml` / `rp2018.toml`. *(Verified
      2026-11-17 from the committed provenance files.)*
- [ ] The extracted inputs under `data/raw/<edition>/` are immutable copies.
- [x] Re-running the fetch against the recorded checksums produces no unexpected
      change; any change is recorded and flagged. *(Verified 2026-11-17:
      `python3 scripts/fetch_official.py --verify` re-checks the six committed
      zips against the pinned digests, needs no network, and writes nothing.)*
- [x] The maintainer has decided: the six original zips are committed under
      `data/raw/_archives/<edition>/`, alongside the extracted inputs plus
      checksums (decision-log R8, adopted 2026-11-17).

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

- [x] Running the comparison twice produces byte-identical reports. *(Verified
      2026-11-17 offline: two consecutive `python3 -m byz.reconcile` runs leave
      the reports unchanged.)*
- [x] `git status` shows no modifications under `source/`, `csv-unicode/`,
      `tei-xml-unicode/`, or `essay/`. *(Verified 2026-11-17: the legacy
      converters reproduce `csv-unicode/` and `tei-xml-unicode/` byte-identically
      and the curated editions live under `editions/`.)*
- [x] No corpus file was moved, deleted, or normalized in place.
- [ ] No canonical source was selected automatically. *(Decision log rows are
      still `pending`; the pipeline only flags.)*
- [x] Tests run offline and pass. *(2026-11-17: `tests/reconciliation` runs 47
      tests with 0 skips; the six pinned hashes, the committed report totals, and
      `fetch_official.py --verify` are all checked without the network.)*

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
- [x] Tests are green; reports are deterministic; corpus files are untouched.
      *(Offline tests are green (47 reconciliation, 0 skipped), reports are
      deterministic across two runs, and the corpus files are untouched.)*
- [ ] The plan's task groups are complete, or every deviation is recorded here.
