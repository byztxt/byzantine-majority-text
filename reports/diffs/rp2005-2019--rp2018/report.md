# Diff: rp2005-2019 -> rp2018

- **Left:** `rp2005-2019` (released; Recovered from git tag v2.0.3 (textonly-beta-code + parsed))
- **Right:** `rp2018` (official; Published in print by VTR, Nuremberg)
- **Source-tier differing verses:** 3
- **Derived-text differing verses (normalised):** 3
- **Apparatus-only changes (source differs, main text identical):** 0
- **Derived-only differences (text differs, source-tier comparison unchanged):** 0

## Notation

- **Text** is the Unicode accented main text from
  `editions/rp2005-2019/csv/accented/no-variants/` and
  `editions/rp2018/csv/accented/no-variants/`.
- **Source** is the edition's Beta-code source tier (official `.CCT`,
  historical `textonly-beta-code`, or current `source/CCAT`).
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

## Categories (source tier)

| Category | Count |
| --- | ---: |
| `accents-breathings` | 1 |
| `letters` | 1 |
| `punctuation` | 1 |

## Books (source tier)

| Book | Differing verses |
| --- | ---: |
| `MAT` | 1 |
| `ACT` | 1 |
| `REV` | 1 |

## Main-text changes

### MAT 1:18 · `letters`

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
