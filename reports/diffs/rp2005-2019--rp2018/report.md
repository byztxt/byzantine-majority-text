<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

# Diff: rp2005-2019 -> rp2018

- **Left:** `rp2005-2019` (released; The 2019 sources (textonly-beta-code + parsed), rebuilt by the current pipeline)
- **Right:** `rp2018` (official; Published in print by VTR, Nuremberg)
- **Source-tier differing verses:** 3
- **Derived-text differing verses (normalised):** 3
- **Apparatus-only changes (source differs, main text identical):** 0
- **Apparatus-only changes shown in Unicode:** 0
- **Apparatus-only changes with no Unicode difference (Beta-code encoding only):** 0
- **Derived-only differences (text differs, source-tier comparison unchanged):** 0

## Notation

- **Text** is the Unicode accented main text from
  `editions/rp2005-2019/csv/accented/no-variants/` and
  `editions/rp2018/csv/accented/no-variants/`.
- **Source** is the edition's Beta-code source tier (official `.CCT`,
  historical `textonly-beta-code`, or current `data/raw/repo/rp2018-2023/ccat`).
- `[-removed-]{+added+}` marks a word-level change, in the style of
  `git diff --word-diff`. Text outside the markers is unchanged
  context. Beta-code apparatus braces (`{N ... }`) are part of the
  source text and can appear next to or inside the markers.
- The marker delimiters are the fixed strings `[-`, `-]`, `{+`, `+}`; a
  literal `-` or `>` next to a delimiter is part of the text (for
  example, a dash-spacing change can render as
  `[-εἶπεν --]{+εἶπεν-+}`).
- Text comparison ignores paragraph markers (`¶`) and normalises
  apostrophe typography (`’`/`‘` -> `'`) and whitespace; the
  word-diff shown omits those conventions. The exact text is in
  `changes.csv` (`text_left`/`text_right`).
- **Apparatus** is the Unicode accented text with variants, from
  `editions/rp2005-2019/csv/accented/with-variants/` and
  `editions/rp2018/csv/accented/with-variants/`.

### Why the main text can be unchanged while the apparatus changes

A variant reading lives inside literal `{...}` braces in the
with-variants view; the main text drops the braces together with the
note. When an edition adds or rewrites an apparatus note and the main
reading does not move, the source tier and the apparatus differ while
the main text stays identical. The rendered apparatus change therefore
doubles the braces: the outer `{+` and `+}` are the diff markers, and
the inner `{Byz ... }` is the reading itself, so an added variant
renders as `{+{Byz τε > δε }+}`.

An apparatus-only entry can take any of these shapes (they can
combine): it has a Unicode difference and appears in `apparatus.diff`;
it differs only in the Beta-code encoding and converts to the same
Unicode, in which case the report names it as encoding-only and
`apparatus.diff` omits it; or the exact main text changed without a
normalised change, in which case the entry is also marked
`see text.diff`.

## Categories (source tier)

| Category | Meaning | Count |
| --- | --- | ---: |
| `accents-breathings` | The main text differs only in accents or breathings. | 1 |
| `punctuation` | The main text differs in punctuation (capitalisation is not considered here). | 2 |

Category meanings and worked examples: [`../README.md#categories`](../README.md#categories).

## Books (source tier)

| Book | Differing verses |
| --- | ---: |
| `MAT` | 1 |
| `ACT` | 1 |
| `REV` | 1 |

## Main-text changes (derived text differs)

The sections are grouped by the derived Unicode text; the category
is the source-tier classification. So a row can appear here while
its category names an apparatus change: the apparatus tag moved
while only the derived typography differs.

### MAT 1:18 · `punctuation`

Text:

```
Τοῦ δὲ Ἰησοῦ χριστοῦ ἡ γέννησις οὕτως [-ἦν.-]{+ἦν·+} [-Μνηστευθείσης-]{+μνηστευθείσης+} γὰρ τῆς μητρὸς αὐτοῦ Μαρίας τῷ Ἰωσήφ, πρὶν ἢ συνελθεῖν αὐτούς, εὑρέθη ἐν γαστρὶ ἔχουσα ἐκ πνεύματος ἁγίου.
```

Source (Beta code):

```
? *TOU= DE\ *)IHSOU= XRISTOU= H( GE/NNHSIS {N GE/NNHSIS > GE/NESIS } OU(/TWS [-H)=N.-]{+H)=N:+} [-*MNHSTEUQEI/SHS-]{+MNHSTEUQEI/SHS+} GA\R {N GA\R > - } TH=S MHTRO\S AU)TOU= *MARI/AS TW=| *)IWSH/F, PRI\N H)\ SUNELQEI=N AU)TOU/S, EU(RE/QH E)N GASTRI\ E)/XOUSA E)K PNEU/MATOS A(GI/OU.
```

### ACT 28:2 · `accents-breathings`

Text:

```
Οἱ δὲ βάρβαροι παρεῖχον οὐ τὴν τυχοῦσαν φιλανθρωπίαν ἡμῖν· ἀνάψαντες γὰρ πυράν, προσελάβοντο πάντας ἡμᾶς, διὰ τὸν ὑετὸν τὸν ἐφεστῶτα, καὶ διὰ τὸ [-ψύχος.-]{+ψῦχος.+}
```

Source (Beta code):

```
*OI( DE\ {N DE\ > TE } BA/RBAROI PAREI=XON OU) TH\N TUXOU=SAN FILANQRWPI/AN H(MI=N: A)NA/YANTES {N A)NA/YANTES > A(/YANTES } GA\R PURA/N, PROSELA/BONTO PA/NTAS H(MA=S, DIA\ TO\N U(ETO\N TO\N E)FESTW=TA, KAI\ DIA\ TO\ [-YU/XOS.-]{+YU=XOS.+}
```

### REV 11:15 · `punctuation`

Text:

```
Καὶ ὁ ἕβδομος ἄγγελος ἐσάλπισεν, καὶ ἐγένοντο φωναὶ μεγάλαι ἐν τῷ οὐρανῷ, λέγουσαι, Ἐγένετο ἡ βασιλεία τοῦ [-κόσμου,-]{+κόσμου+} τοῦ κυρίου [-ἡμῶν,-]{+ἡμῶν+} καὶ τοῦ χριστοῦ αὐτοῦ, καὶ βασιλεύσει εἰς τοὺς αἰῶνας τῶν αἰώνων.
```

Source (Beta code):

```
? *KAI\ O( E(/BDOMOS A)/GGELOS E)SA/LPISEN, KAI\ E)GE/NONTO FWNAI\ MEGA/LAI E)N TW=| OU)RANW=|, LE/GOUSAI, {N LE/GOUSAI > LE/GONTES } *)EGE/NETO H( BASILEI/A TOU= [-KO/SMOU,-]{+KO/SMOU+} TOU= KURI/OU [-H(MW=N,-]{+H(MW=N+} KAI\ TOU= XRISTOU= AU)TOU=, KAI\ BASILEU/SEI EI)S TOU\S AI)W=NAS TW=N AI)W/NWN.
```

## Apparatus-only changes

None: every source-tier difference also changes the normalised main text.

## Derived-only differences

None: every derived-text difference is also a source-tier
difference.
