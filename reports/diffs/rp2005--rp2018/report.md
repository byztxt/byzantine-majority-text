<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

# Diff: rp2005 -> rp2018

- **Left:** `rp2005` (official; Published in print by Chilton Book Publishing, Southborough, Massachusetts)
- **Right:** `rp2018` (official; Published in print by VTR, Nuremberg)
- **Source-tier differing verses:** 55
- **Derived-text differing verses (normalised):** 47
- **Apparatus-only changes (source differs, main text identical):** 8
- **Apparatus-only changes shown in Unicode:** 7
- **Apparatus-only changes with no Unicode difference (Beta-code encoding only):** 1
- **Derived-only differences (text differs, source-tier comparison unchanged):** 0

## Notation

- **Text** is the Unicode accented main text from
  `editions/rp2005/csv/accented/no-variants/` and
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
  `editions/rp2005/csv/accented/with-variants/` and
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
| `accents-breathings` | The main text differs only in accents or breathings. | 13 |
| `capitalization` | The main text differs only in capitalisation. | 5 |
| `letters` | The main text letters differ. | 2 |
| `punctuation` | The main text differs in punctuation (capitalisation is not considered here). | 24 |
| `variant` | The apparatus reading or note changed; the main text is identical. | 7 |
| `word-segmentation` | The same letters are divided into words differently. | 4 |

Category meanings and worked examples: [`../README.md#categories`](../README.md#categories).

## Books (source tier)

| Book | Differing verses |
| --- | ---: |
| `MAT` | 10 |
| `MAR` | 9 |
| `LUK` | 7 |
| `JOH` | 3 |
| `ACT` | 2 |
| `ROM` | 6 |
| `1CO` | 3 |
| `2CO` | 4 |
| `EPH` | 1 |
| `PHP` | 1 |
| `1TI` | 1 |
| `2TI` | 2 |
| `TIT` | 1 |
| `HEB` | 2 |
| `2PE` | 1 |
| `REV` | 2 |

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

### MAT 13:6 · `punctuation`

Text:

```
ἡλίου δὲ ἀνατείλαντος ἐκαυματίσθη, καὶ διὰ τὸ μὴ ἔχειν [-ῥίζαν,-]{+ῥίζαν+} ἐξηράνθη.
```

Source (Beta code):

```
H(LI/OU DE\ A)NATEI/LANTOS E)KAUMATI/SQH, KAI\ DIA\ TO\ MH\ E)/XEIN [-R(I/ZAN,-]{+R(I/ZAN+} E)CHRA/NQH.
```

### MAT 15:26 · `punctuation`

Text:

```
Ὁ δὲ ἀποκριθεὶς εἶπεν, Οὐκ ἔστιν καλὸν λαβεῖν τὸν ἄρτον τῶν [-τέκνων,-]{+τέκνων+} καὶ βαλεῖν τοῖς κυναρίοις.
```

Source (Beta code):

```
*(O DE\ A)POKRIQEI\S EI)=PEN, *OU)K E)/STIN KALO\N LABEI=N TO\N A)/RTON TW=N [-TE/KNWN,-]{+TE/KNWN+} KAI\ BALEI=N TOI=S KUNARI/OIS.
```

### MAT 21:21 · `punctuation`

Text:

```
Ἀποκριθεὶς δὲ ὁ Ἰησοῦς εἶπεν αὐτοῖς, Ἀμὴν λέγω ὑμῖν, ἐὰν ἔχητε πίστιν, καὶ μὴ διακριθῆτε, οὐ μόνον τὸ τῆς συκῆς ποιήσετε, ἀλλὰ κἂν τῷ ὄρει τούτῳ εἴπητε, [-Ἄρθητι-]{+Ἄρθητι,+} καὶ βλήθητι εἰς τὴν θάλασσαν, γενήσεται.
```

Source (Beta code):

```
*)APOKRIQEI\S DE\ O( *)IHSOU=S EI)=PEN AU)TOI=S, *)AMH\N LE/GW U(MI=N, E)A\N E)/XHTE PI/STIN, KAI\ MH\ DIAKRIQH=TE, OU) MO/NON TO\ TH=S SUKH=S POIH/SETE, A)LLA\ KA)\N TW=| O)/REI TOU/TW| EI)/PHTE, [-*)/ARQHTI-]{+*)/ARQHTI,+} KAI\ BLH/QHTI EI)S TH\N QA/LASSAN, GENH/SETAI.
```

### MAT 22:37 · `capitalization`

Text:

```
[-ὁ-]{+Ὁ+} δὲ Ἰησοῦς ἔφη αὐτῷ, Ἀγαπήσεις κύριον τὸν θεόν σου, ἐν ὅλῃ καρδίᾳ σου, καὶ ἐν ὅλῃ ψυχῇ σου, καὶ ἐν ὅλῃ τῇ διανοίᾳ σου.
```

Source (Beta code):

```
[-O(-]{+*(O+} DE\ *)IHSOU=S {N *)IHSOU=S > - } E)/FH AU)TW=|, *)AGAPH/SEIS KU/RION TO\N QEO/N SOU, E)N O(/LH| KARDI/A| {N KARDI/A| > TH=| KARDI/A| } SOU, KAI\ E)N O(/LH| YUXH=| {N YUXH=| > TH=| YUXH=| } SOU, KAI\ E)N O(/LH| TH=| DIANOI/A| SOU.
```

### MAT 26:18 · `accents-breathings`

Text:

```
Ὁ δὲ εἶπεν, Ὑπάγετε εἰς τὴν πόλιν πρὸς τὸν δεῖνα, καὶ εἴπατε αὐτῷ, Ὁ διδάσκαλος λέγει, Ὁ καιρός μου ἐγγύς ἐστιν· [-πρὸς-]{+πρός+} [-σὲ-]{+σε+} ποιῶ τὸ Πάσχα μετὰ τῶν μαθητῶν μου.
```

Source (Beta code):

```
*(O DE\ EI)=PEN, *(UPA/GETE EI)S TH\N PO/LIN PRO\S TO\N DEI=NA, KAI\ EI)/PATE AU)TW=|, *(O DIDA/SKALOS LE/GEI, *(O KAIRO/S MOU E)GGU/S E)STIN: [-PRO\S-]{+PRO/S+} [-SE\-]{+SE+} POIW= TO\ *PA/SXA META\ TW=N MAQHTW=N MOU.
```

### MAT 26:58 · `punctuation`

Text:

```
Ὁ δὲ Πέτρος ἠκολούθει αὐτῷ ἀπὸ μακρόθεν, ἕως τῆς αὐλῆς τοῦ [-ἀρχιερέως,-]{+ἀρχιερέως·+} καὶ εἰσελθὼν ἔσω ἐκάθητο μετὰ τῶν ὑπηρετῶν, ἰδεῖν τὸ τέλος.
```

Source (Beta code):

```
*(O DE\ *PE/TROS H)KOLOU/QEI AU)TW=| A)PO\ MAKRO/QEN, E(/WS TH=S AU)LH=S TOU= [-A)RXIERE/WS,-]{+A)RXIERE/WS:+} KAI\ EI)SELQW\N E)/SW E)KA/QHTO META\ TW=N U(PHRETW=N, I)DEI=N TO\ TE/LOS.
```

### MAT 27:13 · `accents-breathings`

Text:

```
Τότε λέγει αὐτῷ ὁ Πιλάτος, Οὐκ ἀκούεις πόσα [-σοῦ-]{+σου+} καταμαρτυροῦσιν;
```

Source (Beta code):

```
*TO/TE LE/GEI AU)TW=| O( *PILA/TOS, *OU)K A)KOU/EIS PO/SA [-SOU=-]{+SOU+} KATAMARTUROU=SIN;
```

### MAT 27:45 · `punctuation`

Text:

```
Ἀπὸ δὲ ἕκτης ὥρας σκότος ἐγένετο ἐπὶ πᾶσαν τὴν γῆν ἕως ὥρας [-ἐνάτης·-]{+ἐνάτης.+}
```

Source (Beta code):

```
? *)APO\ DE\ E(/KTHS W(/RAS SKO/TOS E)GE/NETO E)PI\ PA=SAN TH\N GH=N E(/WS W(/RAS [-E)NA/THS:-]{+E)NA/THS.+}
```

### MAT 27:46 · `capitalization`

Text:

```
[-περὶ-]{+Περὶ+} δὲ τὴν ἐνάτην ὥραν ἀνεβόησεν ὁ Ἰησοῦς φωνῇ μεγάλῃ, λέγων, Ἠλί, Ἠλί, λιμὰ σαβαχθανί; Τοῦτ' ἔστιν, Θεέ μου, Θεέ μου, ἵνα τί με ἐγκατέλιπες;
```

Source (Beta code):

```
[-PERI\-]{+*PERI\+} DE\ TH\N E)NA/THN W(/RAN A)NEBO/HSEN O( *)IHSOU=S FWNH=| MEGA/LH|, LE/GWN, *)HLI/, *)HLI/, LIMA\ {N LIMA\ > LEMA } SABAXQANI/; *TOU=T' E)/STIN, *QEE/ MOU, *QEE/ MOU, I(/NA {N I(/NA TI/ > I(NATI/ } TI/ ME E)GKATE/LIPES;
```

### MAR 1:44 · `punctuation`

Text:

```
καὶ λέγει αὐτῷ, [-Ὅρα,-]{+Ὅρα+} μηδενὶ μηδὲν εἴπῃς· ἀλλ' ὕπαγε, σεαυτὸν δεῖξον τῷ ἱερεῖ, καὶ προσένεγκε περὶ τοῦ καθαρισμοῦ σου ἃ προσέταξεν Μωσῆς, εἰς μαρτύριον αὐτοῖς.
```

Source (Beta code):

```
KAI\ LE/GEI AU)TW=|, [-*(/ORA,-]{+*(/ORA+} MHDENI\ MHDE\N EI)/PHS|: A)LL' {N A)LL' > A)LLA\ } U(/PAGE, SEAUTO\N DEI=CON TW=| I(EREI=, KAI\ PROSE/NEGKE PERI\ TOU= KAQARISMOU= SOU A(\ PROSE/TACEN *MWSH=S, {N *MWSH=S > *MWU+SH=S } EI)S MARTU/RION AU)TOI=S.
```

### MAR 3:4 · `punctuation`

Text:

```
Καὶ λέγει αὐτοῖς, Ἔξεστιν τοῖς σάββασιν [-ἀγαθοποιῆσαι,-]{+ἀγαθοποιῆσαι+} ἢ κακοποιῆσαι; Ψυχὴν [-σῶσαι,-]{+σῶσαι+} ἢ ἀποκτεῖναι; Οἱ δὲ ἐσιώπων.
```

Source (Beta code):

```
*KAI\ LE/GEI AU)TOI=S, *)/ECESTIN TOI=S SA/BBASIN [-A)GAQOPOIH=SAI,-]{+A)GAQOPOIH=SAI+} {N A)GAQOPOIH=SAI > A)GAQO\N POIH=SAI } H)\ KAKOPOIH=SAI; *YUXH\N [-SW=SAI,-]{+SW=SAI+} H)\ A)POKTEI=NAI; *OI( DE\ E)SIW/PWN.
```

### MAR 8:24 · `punctuation`

Text:

```
Καὶ ἀναβλέψας ἔλεγεν, Βλέπω τοὺς [-ἀνθρώπους-]{+ἀνθρώπους,+} ὅτι ὡς δένδρα ὁρῶ περιπατοῦντας.
```

Source (Beta code):

```
*KAI\ A)NABLE/YAS E)/LEGEN, *BLE/PW TOU\S [-A)NQRW/POUS-]{+A)NQRW/POUS,+} O(/TI W(S DE/NDRA O(RW= PERIPATOU=NTAS.
```

### MAR 9:40 · `punctuation`

Text:

```
Ὃς γὰρ οὐκ ἔστιν καθ' [-ὑμῶν,-]{+ὑμῶν+} ὑπὲρ ὑμῶν ἐστιν.
```

Source (Beta code):

```
*(\OS GA\R OU)K E)/STIN KAQ' [-U(MW=N,-]{+U(MW=N+} {N U(MW=N U(PE\R U(MW=N > H(MW=N U(PE\R H(MW=N } U(PE\R U(MW=N E)STIN.
```

### MAR 10:44 · `punctuation`

Text:

```
καὶ ὃς ἐὰν θέλῃ ὑμῶν γενέσθαι [-πρῶτος-]{+πρῶτος,+} ἔσται πάντων δοῦλος.
```

Source (Beta code):

```
KAI\ O(\S E)A\N {N E)A\N QE/LH| U(MW=N GENE/SQAI > A)\N QE/LH| E)N U(MI=N EI)=NAI } QE/LH| U(MW=N GENE/SQAI [-PRW=TOS-]{+PRW=TOS,+} E)/STAI PA/NTWN DOU=LOS.
```

### MAR 14:1 · `punctuation`

Text:

```
Ἦν δὲ τὸ Πάσχα καὶ τὰ ἄζυμα μετὰ δύο ἡμέρας· καὶ ἐζήτουν οἱ ἀρχιερεῖς καὶ οἱ γραμματεῖς πῶς αὐτὸν ἐν δόλῳ κρατήσαντες [-ἀποκτείνωσιν·-]{+ἀποκτείνωσιν.+}
```

Source (Beta code):

```
*)=HN DE\ TO\ *PA/SXA KAI\ TA\ A)/ZUMA META\ DU/O H(ME/RAS: KAI\ E)ZH/TOUN OI( A)RXIEREI=S KAI\ OI( GRAMMATEI=S PW=S AU)TO\N E)N DO/LW| KRATH/SANTES [-A)POKTEI/NWSIN:-]{+A)POKTEI/NWSIN.+}
```

### MAR 14:2 · `capitalization`

Text:

```
[-ἔλεγον-]{+Ἔλεγον+} δέ, Μὴ ἐν τῇ ἑορτῇ, μήποτε θόρυβος ἔσται τοῦ λαοῦ.
```

Source (Beta code):

```
[-E)/LEGON-]{+*)/ELEGON+} DE/, {N DE/ > GA/R } *MH\ E)N TH=| E(ORTH=|, MH/POTE QO/RUBOS {N QO/RUBOS E)/STAI > E)/STAI QO/RUBOS } E)/STAI TOU= LAOU=.
```

### MAR 14:23 · `punctuation`

Text:

```
Καὶ λαβὼν τὸ [-ποτήριον-]{+ποτήριον,+} εὐχαριστήσας ἔδωκεν αὐτοῖς, καὶ ἔπιον ἐξ αὐτοῦ πάντες.
```

Source (Beta code):

```
*KAI\ LABW\N TO\ {N TO\ > - } [-POTH/RION-]{+POTH/RION,+} EU)XARISTH/SAS E)/DWKEN AU)TOI=S, KAI\ E)/PION E)C AU)TOU= PA/NTES.
```

### MAR 15:29 · `accents-breathings`

Text:

```
Καὶ οἱ παραπορευόμενοι ἐβλασφήμουν αὐτόν, κινοῦντες τὰς κεφαλὰς αὐτῶν, καὶ λέγοντες, Οὐά, ὁ καταλύων τὸν [-ναόν-]{+ναὸν+} καὶ ἐν τρισὶν ἡμέραις οἰκοδομῶν,
```

Source (Beta code):

```
*KAI\ OI( PARAPOREUO/MENOI E)BLASFH/MOUN AU)TO/N, KINOU=NTES TA\S KEFALA\S AU)TW=N, KAI\ LE/GONTES, *OU)A/, O( KATALU/WN TO\N [-NAO/N-]{+NAO\N+} KAI\ E)N {N E)N TRISI\N H(ME/RAIS OI)KODOMW=N > OI)KODOMW=N E)N TRISI\N H(ME/RAIS } TRISI\N H(ME/RAIS OI)KODOMW=N,
```

### LUK 6:9 · `punctuation`

Text:

```
Εἶπεν οὖν ὁ Ἰησοῦς πρὸς αὐτούς, Ἐπερωτήσω ὑμᾶς τί, Ἔξεστιν τοῖς [-σάββασιν,-]{+σάββασιν+} ἀγαθοποιῆσαι ἢ κακοποιῆσαι; Ψυχὴν σῶσαι ἢ ἀποκτεῖναι;
```

Source (Beta code):

```
*EI)=PEN OU)=N {N OU)=N > DE\ } O( *)IHSOU=S PRO\S AU)TOU/S, *)EPERWTH/SW {N *)EPERWTH/SW > *)EPERWTW= } U(MA=S TI/, {N U(MA=S TI/, *)/ECESTIN > U(MA=S, *EI) E)/CESTIN } *)/ECESTIN TOI=S {N TOI=S SA/BBASIN > TW=| SABBA/TW| } [-SA/BBASIN,-]{+SA/BBASIN+} A)GAQOPOIH=SAI H)\ KAKOPOIH=SAI; *YUXH\N SW=SAI H)\ A)POKTEI=NAI; {N A)POKTEI=NAI > A)POLE/SAI }
```

### LUK 6:16 · `punctuation`

Text:

```
Ἰούδαν Ἰακώβου, καὶ Ἰούδαν Ἰσκαριώτην, ὃς καὶ ἐγένετο [-προδότης,-]{+προδότης.+}
```

Source (Beta code):

```
*)IOU/DAN {N *)IOU/DAN *)IAKW/BOU > KAI\ *)IOU/DAN *)IAKW/BOU } *)IAKW/BOU, KAI\ *)IOU/DAN *)ISKARIW/THN, {N *)ISKARIW/THN > *)ISKARIW/Q } O(\S {N O(\S KAI\ > O(\S } KAI\ E)GE/NETO [-PRODO/THS,-]{+PRODO/THS.+}
```

### LUK 7:4 · `capitalization`

Text:

```
Οἱ δέ, παραγενόμενοι πρὸς τὸν Ἰησοῦν, παρεκάλουν αὐτὸν σπουδαίως, λέγοντες ὅτι [-Ἄξιός-]{+ἄξιός+} ἐστιν ᾧ παρέξει τοῦτο·
```

Source (Beta code):

```
*OI( DE/, PARAGENO/MENOI PRO\S TO\N *)IHSOU=N, PAREKA/LOUN AU)TO\N SPOUDAI/WS, LE/GONTES O(/TI [-*)/ACIO/S-]{+A)/CIO/S+} E)STIN W(=| PARE/CEI {N PARE/CEI > PARE/CH| } TOU=TO:
```

### LUK 20:18 · `punctuation`

Text:

```
Πᾶς ὁ πεσὼν ἐπ' ἐκεῖνον τὸν [-λίθον,-]{+λίθον+} συνθλασθήσεται· ἐφ' ὃν δ' ἂν πέσῃ, λικμήσει αὐτόν.
```

Source (Beta code):

```
*PA=S O( PESW\N E)P' E)KEI=NON TO\N [-LI/QON,-]{+LI/QON+} SUNQLASQH/SETAI: E)F' O(\N D' A)\N PE/SH|, LIKMH/SEI AU)TO/N.
```

### LUK 22:19 · `punctuation`

Text:

```
Καὶ λαβὼν ἄρτον, εὐχαριστήσας ἔκλασεν καὶ ἔδωκεν αὐτοῖς, λέγων, Τοῦτό ἐστιν τὸ σῶμά [-μου,-]{+μου+} τὸ ὑπὲρ ὑμῶν διδόμενον· τοῦτο ποιεῖτε εἰς τὴν ἐμὴν ἀνάμνησιν.
```

Source (Beta code):

```
*KAI\ LABW\N A)/RTON, EU)XARISTH/SAS E)/KLASEN KAI\ E)/DWKEN AU)TOI=S, LE/GWN, *TOU=TO/ E)STIN TO\ SW=MA/ [-MOU,-]{+MOU+} TO\ U(PE\R U(MW=N DIDO/MENON: TOU=TO POIEI=TE EI)S TH\N E)MH\N A)NA/MNHSIN.
```

### LUK 22:42 · `punctuation`

Text:

```
λέγων, Πάτερ, εἰ [-βούλει,-]{+βούλει+} παρενεγκεῖν τὸ ποτήριον τοῦτο ἀπ' ἐμοῦ· πλὴν μὴ τὸ θέλημά μου, ἀλλὰ τὸ σὸν γενέσθω.
```

Source (Beta code):

```
LE/GWN, *PA/TER, EI) [-BOU/LEI,-]{+BOU/LEI+} PARENEGKEI=N {N PARENEGKEI=N TO\ POTH/RION TOU=TO > PARE/NEGKE TOU=TO TO\ POTH/RION } TO\ POTH/RION TOU=TO A)P' E)MOU=: PLH\N MH\ TO\ QE/LHMA/ MOU, A)LLA\ TO\ SO\N GENE/SQW. {B GENE/SQW > GINE/SQW } {N GENE/SQW > GINE/SQW }
```

### LUK 22:54 · `punctuation`

Text:

```
Συλλαβόντες δὲ αὐτὸν ἤγαγον, καὶ εἰσήγαγον αὐτὸν εἰς τὸν οἶκον τοῦ [-ἀρχιερέως.-]{+ἀρχιερέως·+} [-Ὁ-]{+ὁ+} δὲ Πέτρος ἠκολούθει μακρόθεν.
```

Source (Beta code):

```
? *SULLABO/NTES DE\ AU)TO\N H)/GAGON, KAI\ EI)SH/GAGON AU)TO\N {N AU)TO\N EI)S TO\N OI)=KON > EI)S TH\N OI)KI/AN } EI)S TO\N OI)=KON TOU= [-A)RXIERE/WS.-]{+A)RXIERE/WS:+} [-*(O-]{+O(+} DE\ *PE/TROS H)KOLOU/QEI MAKRO/QEN.
```

### JOH 18:11 · `letters`

Text:

```
Εἶπεν οὖν ὁ Ἰησοῦς τῷ Πέτρῳ, Βάλε τὴν [-μάχαιράν σου-]{+μάχαιραν+} εἰς τὴν θήκην· τὸ ποτήριον ὃ δέδωκέν μοι ὁ πατήρ, οὐ μὴ πίω αὐτό;
```

Source (Beta code):

```
*EI)=PEN OU)=N O( *)IHSOU=S TW=| *PE/TRW|, *BA/LE TH\N {+MA/XAIRAN {B MA/XAIRAN >+} MA/XAIRA/N SOU [-{N SOU > --] } EI)S TH\N QH/KHN: TO\ POTH/RION O(\ DE/DWKE/N MOI O( PATH/R, OU) MH\ PI/W AU)TO/;
```

### JOH 18:32 · `letters`

Text:

```
ἵνα ὁ λόγος τοῦ Ἰησοῦ πληρωθῇ, ὃν εἶπεν, σημαίνων ποίῳ θανάτῳ [-ἤμελλεν-]{+ἔμελλεν+} ἀποθνῄσκειν.
```

Source (Beta code):

```
I(/NA O( LO/GOS TOU= *)IHSOU= PLHRWQH=|, O(\N EI)=PEN, SHMAI/NWN POI/W| QANA/TW| {+E)/MELLEN {B E)/MELLEN >+} H)/MELLEN {+} {N E)/MELLEN > H)/MELLEN }+} A)POQNH/S|KEIN.
```

### JOH 19:31 · `punctuation`

Text:

```
Οἱ οὖν Ἰουδαῖοι, ἵνα μὴ μείνῃ ἐπὶ τοῦ σταυροῦ τὰ σώματα ἐν τῷ [-σαββάτῳ-]{+σαββάτῳ,+} ἐπεὶ Παρασκευὴ ἦν - ἦν γὰρ μεγάλη ἡ ἡμέρα ἐκείνου τοῦ σαββάτου - ἠρώτησαν τὸν Πιλάτον ἵνα κατεαγῶσιν αὐτῶν τὰ σκέλη, καὶ ἀρθῶσιν.
```

Source (Beta code):

```
? *OI( OU)=N *)IOUDAI=OI, I(/NA {N I(/NA MH\ > E)PEI\ *PARASKEUH\ H)=N I(/NA MH\ } MH\ MEI/NH| E)PI\ TOU= STAUROU= TA\ SW/MATA E)N TW=| [-SABBA/TW|-]{+SABBA/TW|,+} E)PEI\ {N E)PEI\ *PARASKEUH\ H)=N > - } *PARASKEUH\ H)=N - H)=N GA\R MEGA/LH H( H(ME/RA E)KEI/NOU TOU= SABBA/TOU - H)RW/THSAN TO\N *PILA/TON I(/NA KATEAGW=SIN AU)TW=N TA\ SKE/LH, KAI\ A)RQW=SIN.
```

### ACT 10:6 · `punctuation`

Text:

```
οὗτος ξενίζεται παρά τινι Σίμωνι βυρσεῖ, ᾧ ἐστιν οἰκία παρὰ [-θάλασσαν·-]{+θάλασσαν.+}
```

Source (Beta code):

```
OU(=TOS CENI/ZETAI PARA/ TINI *SI/MWNI BURSEI=, W(=| E)STIN OI)KI/A PARA\ [-QA/LASSAN:-]{+QA/LASSAN.+}
```

### ACT 10:7 · `capitalization`

Text:

```
[-ὡς-]{+Ὡς+} δὲ ἀπῆλθεν ὁ ἄγγελος ὁ λαλῶν τῷ Κορνηλίῳ, φωνήσας δύο τῶν οἰκετῶν αὐτοῦ, καὶ στρατιώτην εὐσεβῆ τῶν προσκαρτερούντων αὐτῷ,
```

Source (Beta code):

```
[-W(S-]{+*(WS+} DE\ A)PH=LQEN O( A)/GGELOS O( LALW=N TW=| {N TW=| *KORNHLI/W| > AU)TW=| } *KORNHLI/W|, FWNH/SAS DU/O TW=N OI)KETW=N AU)TOU=, {N AU)TOU= > - } KAI\ STRATIW/THN EU)SEBH= TW=N PROSKARTEROU/NTWN AU)TW=|,
```

### ROM 11:22 · `accents-breathings`

Text:

```
Ἴδε οὖν χρηστότητα καὶ ἀποτομίαν θεοῦ· ἐπὶ μὲν τοὺς πεσόντας, ἀποτομίαν· ἐπὶ [-δέ-]{+δὲ+} [-σε,-]{+σὲ,+} χρηστότητα, ἐὰν ἐπιμείνῃς τῇ χρηστότητι· ἐπεὶ καὶ σὺ ἐκκοπήσῃ.
```

Source (Beta code):

```
*)/IDE OU)=N XRHSTO/THTA KAI\ A)POTOMI/AN QEOU=: E)PI\ ME\N TOU\S PESO/NTAS, A)POTOMI/AN: {N A)POTOMI/AN E)PI\ > A)POTOMI/A E)PI\ } E)PI\ [-DE/-]{+DE\+} [-SE,-]{+SE\,+} XRHSTO/THTA, {N XRHSTO/THTA E)A\N E)PIMEI/NHS| > XRHSTO/THS QEOU= E)A\N E)PIME/NHS| } E)A\N E)PIMEI/NHS| TH=| XRHSTO/THTI: E)PEI\ KAI\ SU\ E)KKOPH/SH|.
```

### ROM 15:15 · `accents-breathings`

Text:

```
Τολμηρότερον δὲ ἔγραψα ὑμῖν, ἀδελφοί, ἀπὸ μέρους, ὡς [-ἐπαναμιμνήσκων-]{+ἐπαναμιμνῄσκων+} ὑμᾶς, διὰ τὴν χάριν τὴν δοθεῖσάν μοι ὑπὸ τοῦ θεοῦ,
```

Source (Beta code):

```
*TOLMHRO/TERON DE\ E)/GRAYA U(MI=N, A)DELFOI/, {N A)DELFOI/ > - } A)PO\ ME/ROUS, W(S [-E)PANAMIMNH/SKWN-]{+E)PANAMIMNH|/SKWN+} U(MA=S, DIA\ TH\N XA/RIN TH\N DOQEI=SA/N MOI U(PO\ TOU= QEOU=,
```

### 1CO 7:5 · `word-segmentation`

Text:

```
Μὴ ἀποστερεῖτε ἀλλήλους, εἰ [-μή τι-]{+μήτι+} ἂν ἐκ συμφώνου πρὸς καιρόν, ἵνα σχολάζητε τῇ νηστείᾳ καὶ τῇ προσευχῇ, καὶ πάλιν ἐπὶ τὸ αὐτὸ συνέρχησθε, ἵνα μὴ πειράζῃ ὑμᾶς ὁ Σατανᾶς διὰ τὴν ἀκρασίαν ὑμῶν.
```

Source (Beta code):

```
*MH\ A)POSTEREI=TE A)LLH/LOUS, EI) [-MH/ {N MH/ TI >-] MH/TI [-} TI-] A)\N E)K SUMFW/NOU PRO\S KAIRO/N, I(/NA SXOLA/ZHTE {N SXOLA/ZHTE > SXOLA/SHTE } TH=| {N TH=| NHSTEI/A| KAI\ > - } NHSTEI/A| KAI\ TH=| PROSEUXH=|, KAI\ PA/LIN E)PI\ TO\ AU)TO\ SUNE/RXHSQE, {N SUNE/RXHSQE > H)=TE } I(/NA MH\ PEIRA/ZH| U(MA=S O( *SATANA=S DIA\ TH\N A)KRASI/AN U(MW=N.
```

### 1CO 11:24 · `punctuation`

Text:

```
καὶ εὐχαριστήσας ἔκλασεν καὶ εἶπεν, Λάβετε, [-φάγετε,-]{+φάγετε·+} [-Τοῦτό-]{+τοῦτό+} μού ἐστιν τὸ σῶμα τὸ ὑπὲρ ὑμῶν κλώμενον· τοῦτο ποιεῖτε εἰς τὴν ἐμὴν ἀνάμνησιν.
```

Source (Beta code):

```
KAI\ EU)XARISTH/SAS E)/KLASEN KAI\ EI)=PEN, *LA/BETE, {N *LA/BETE FA/GETE > - } [-FA/GETE,-]{+FA/GETE:+} [-*TOU=TO/-]{+TOU=TO/+} MOU/ E)STIN TO\ SW=MA TO\ U(PE\R U(MW=N KLW/MENON: {N KLW/MENON > - } TOU=TO POIEI=TE EI)S TH\N E)MH\N A)NA/MNHSIN.
```

### 2CO 1:17 · `word-segmentation`

Text:

```
Τοῦτο οὖν βουλευόμενος, [-μή τι-]{+μήτι+} ἄρα τῇ ἐλαφρίᾳ ἐχρησάμην; Ἢ ἃ βουλεύομαι, κατὰ σάρκα βουλεύομαι, ἵνα ᾖ παρ' ἐμοὶ τὸ Ναί, ναὶ καὶ τὸ Οὔ, οὔ;
```

Source (Beta code):

```
*TOU=TO OU)=N BOULEUO/MENOS, {N BOULEUO/MENOS [-MH/ TI-] > BOULO/MENOS [-MH/TI-] } [-MH/ TI-]{+MH/TI+} A)/RA TH=| E)LAFRI/A| E)XRHSA/MHN; *)\H A(\ BOULEU/OMAI, KATA\ SA/RKA BOULEU/OMAI, I(/NA H)=| PAR' E)MOI\ TO\ *NAI/, NAI\ KAI\ TO\ *OU)/, OU)/;
```

### 2CO 7:15 · `accents-breathings`

Text:

```
Καὶ τὰ σπλάγχνα αὐτοῦ περισσοτέρως εἰς ὑμᾶς ἐστίν, [-ἀναμιμνησκομένου-]{+ἀναμιμνῃσκομένου+} τὴν πάντων ὑμῶν ὑπακοήν, ὡς μετὰ φόβου καὶ τρόμου ἐδέξασθε αὐτόν.
```

Source (Beta code):

```
*KAI\ TA\ SPLA/GXNA AU)TOU= PERISSOTE/RWS EI)S U(MA=S E)STI/N, [-A)NAMIMNHSKOME/NOU-]{+A)NAMIMNHS|KOME/NOU+} TH\N PA/NTWN U(MW=N U(PAKOH/N, W(S META\ FO/BOU KAI\ TRO/MOU E)DE/CASQE AU)TO/N.
```

### 2CO 12:18 · `word-segmentation`

Text:

```
Παρεκάλεσα Τίτον, καὶ συναπέστειλα τὸν ἀδελφόν· [-μή τι-]{+μήτι+} ἐπλεονέκτησεν ὑμᾶς Τίτος; Οὐ τῷ αὐτῷ πνεύματι περιεπατήσαμεν; Οὐ τοῖς αὐτοῖς ἴχνεσιν;
```

Source (Beta code):

```
*PAREKA/LESA *TI/TON, KAI\ SUNAPE/STEILA TO\N A)DELFO/N: [-MH/ {N MH/ TI >-] MH/TI [-} TI-] E)PLEONE/KTHSEN U(MA=S *TI/TOS; *OU) TW=| AU)TW=| PNEU/MATI PERIEPATH/SAMEN; *OU) TOI=S AU)TOI=S I)/XNESIN;
```

### 2CO 13:5 · `word-segmentation`

Text:

```
Ἑαυτοὺς πειράζετε εἰ ἐστὲ ἐν τῇ πίστει, ἑαυτοὺς δοκιμάζετε. Ἢ οὐκ ἐπιγινώσκετε ἑαυτούς, ὅτι Ἰησοῦς χριστὸς ἐν ὑμῖν ἐστίν; Εἰ [-μή τι-]{+μήτι+} ἀδόκιμοί ἐστε.
```

Source (Beta code):

```
*(EAUTOU\S PEIRA/ZETE EI) E)STE\ E)N TH=| PI/STEI, E(AUTOU\S DOKIMA/ZETE. *)\H OU)K E)PIGINW/SKETE E(AUTOU/S, O(/TI *)IHSOU=S XRISTO\S E)N U(MI=N E)STI/N; {N E)STI/N *EI) [-MH/-]{+>+} [-TI-]{+*EI)+} [->-]{+}+} *EI) MH/TI [-} *EI) MH/ TI-] A)DO/KIMOI/ E)STE.
```

### 1TI 1:18 · `accents-breathings`

Text:

```
Ταύτην τὴν παραγγελίαν παρατίθεμαί σοι, τέκνον Τιμόθεε, κατὰ τὰς προαγούσας [-ἐπί-]{+ἐπὶ+} [-σε-]{+σὲ+} προφητείας, ἵνα στρατεύῃ ἐν αὐταῖς τὴν καλὴν στρατείαν,
```

Source (Beta code):

```
? *TAU/THN TH\N PARAGGELI/AN PARATI/QEMAI/ SOI, TE/KNON *TIMO/QEE, KATA\ TA\S PROAGOU/SAS [-E)PI/-]{+E)PI\+} [-SE-]{+SE\+} PROFHTEI/AS, I(/NA STRATEU/H| E)N AU)TAI=S TH\N KALH\N STRATEI/AN,
```

### 2TI 1:6 · `accents-breathings`

Text:

```
Δι' ἣν αἰτίαν [-ἀναμιμνήσκω-]{+ἀναμιμνῄσκω+} σε ἀναζωπυρεῖν τὸ χάρισμα τοῦ θεοῦ, ὅ ἐστιν ἐν σοὶ διὰ τῆς ἐπιθέσεως τῶν χειρῶν μου.
```

Source (Beta code):

```
*DI' H(\N AI)TI/AN [-A)NAMIMNH/SKW-]{+A)NAMIMNH|/SKW+} SE A)NAZWPUREI=N TO\ XA/RISMA TOU= QEOU=, O(/ E)STIN E)N SOI\ DIA\ TH=S E)PIQE/SEWS TW=N XEIRW=N MOU.
```

### 2TI 2:14 · `accents-breathings`

Text:

```
Ταῦτα [-ὑπομίμνησκε,-]{+ὑπομίμνῃσκε,+} διαμαρτυρόμενος ἐνώπιον τοῦ κυρίου μὴ λογομαχεῖν εἰς οὐδὲν χρήσιμον, ἐπὶ καταστροφῇ τῶν ἀκουόντων.
```

Source (Beta code):

```
? *TAU=TA [-U(POMI/MNHSKE,-]{+U(POMI/MNHS|KE,+} DIAMARTURO/MENOS E)NW/PION TOU= KURI/OU {N KURI/OU > QEOU= } MH\ LOGOMAXEI=N EI)S {N EI)S > E)P' } OU)DE\N XRH/SIMON, E)PI\ KATASTROFH=| TW=N A)KOUO/NTWN.
```

### TIT 3:1 · `accents-breathings`

Text:

```
[-Ὑπομίμνησκε-]{+Ὑπομίμνῃσκε+} αὐτοὺς ἀρχαῖς καὶ ἐξουσίαις ὑποτάσσεσθαι, πειθαρχεῖν, πρὸς πᾶν ἔργον ἀγαθὸν ἑτοίμους εἶναι,
```

Source (Beta code):

```
[-*(UPOMI/MNHSKE-]{+*(UPOMI/MNHS|KE+} AU)TOU\S A)RXAI=S KAI\ {N KAI\ > - } E)COUSI/AIS U(POTA/SSESQAI, PEIQARXEI=N, PRO\S PA=N E)/RGON A)GAQO\N E(TOI/MOUS EI)=NAI,
```

### HEB 2:6 · `accents-breathings`

Text:

```
Διεμαρτύρατο δέ πού τις λέγων, Τί ἐστιν ἄνθρωπος, ὅτι [-μιμνήσκῃ-]{+μιμνῄσκῃ+} αὐτοῦ; Ἢ υἱὸς ἀνθρώπου, ὅτι ἐπισκέπτῃ αὐτόν;
```

Source (Beta code):

```
*DIEMARTU/RATO DE/ POU/ TIS LE/GWN, *TI/ E)STIN A)/NQRWPOS, O(/TI [-MIMNH/SKH|-]{+MIMNH|/SKH|+} AU)TOU=; *)\H UI(O\S A)NQRW/POU, O(/TI E)PISKE/PTH| AU)TO/N;
```

### HEB 13:3 · `accents-breathings`

Text:

```
[-Μιμνήσκεσθε-]{+Μιμνῄσκεσθε+} τῶν δεσμίων, ὡς συνδεδεμένοι· τῶν κακουχουμένων, ὡς καὶ αὐτοὶ ὄντες ἐν σώματι.
```

Source (Beta code):

```
[-*MIMNH/SKESQE-]{+*MIMNH|/SKESQE+} TW=N DESMI/WN, W(S SUNDEDEME/NOI: TW=N KAKOUXOUME/NWN, W(S KAI\ AU)TOI\ O)/NTES E)N SW/MATI.
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

### REV 21:6 · `punctuation`

Text:

```
Καὶ εἶπέν μοι, [-Γέγονα·-]{+Γέγονα+} τὸ Ἄλφα καὶ τὸ Ὦ, ἡ ἀρχὴ καὶ τὸ τέλος. Ἐγὼ τῷ διψῶντι δώσω ἐκ τῆς πηγῆς τοῦ ὕδατος τῆς ζωῆς δωρεάν.
```

Source (Beta code):

```
*KAI\ EI)=PE/N MOI, [-*GE/GONA:-]{+*GE/GONA+} {B [-*GE/GONA:-]{+*GE/GONA+} TO\ > [-*GE/GONA:-]{+*GE/GONA+} E)GW\ TO\ } {N [-*GE/GONA:-]{+*GE/GONA+} > *GE/GONAN. *)EGW/ [EI)MI] } TO\ *)/ALFA KAI\ TO\ *)=W, H( A)RXH\ KAI\ TO\ TE/LOS. *)EGW\ TW=| DIYW=NTI DW/SW {B DW/SW > DW/SW AU)TW=| } E)K TH=S PHGH=S TOU= U(/DATOS TH=S ZWH=S DWREA/N.
```

## Apparatus-only changes

Every entry here has the same normalised derived text; the category
names which source-tier value changed. It does not mean the source
main text is unchanged: a `capitalization` row can also land here
when the derived Unicode text carries no corresponding difference.

- `ROM 1:27` · `variant`
  - Apparatus (Unicode): `ὁμοίως τε {+{Byz τε > δε }+} καὶ οἱ ἄρρενες, {NA ἄρρενες > ἄρσενες } ἀφέντες τὴν φυσικὴν χρῆσιν τῆς θηλείας, ἐξεκαύθησαν ἐν τῇ ὀρέξει αὐτῶν εἰς ἀλλήλους, ἄρσενες ἐν ἄρσεσιν τὴν ἀσχημοσύνην κατεργαζόμενοι, καὶ τὴν ἀντιμισθίαν ἣν ἔδει τῆς πλάνης αὐτῶν ἐν ἑαυτοῖς ἀπολαμβάνοντες.`
  - Apparatus (Beta code): `O(MOI/WS TE {+{B TE > DE }+} KAI\ OI( A)/RRENES, {N A)/RRENES > A)/RSENES } A)FE/NTES TH\N FUSIKH\N XRH=SIN TH=S QHLEI/AS, E)CEKAU/QHSAN E)N TH=| O)RE/CEI AU)TW=N EI)S A)LLH/LOUS, A)/RSENES E)N A)/RSESIN TH\N A)SXHMOSU/NHN KATERGAZO/MENOI, KAI\ TH\N A)NTIMISQI/AN H(\N E)/DEI TH=S PLA/NHS AU)TW=N E)N E(AUTOI=S A)POLAMBA/NONTES.`
- `ROM 2:16` · `variant`
  - Apparatus (Unicode): `ἐν ἡμέρᾳ ὅτε κρινεῖ {+{NA κρινεῖ > κρίνεἰ}+} ὁ θεὸς τὰ κρυπτὰ τῶν ἀνθρώπων, κατὰ τὸ εὐαγγέλιόν μου, διὰ Ἰησοῦ {NA Ἰησοῦ χριστοῦ > χριστοῦ Ἰησοῦ } χριστοῦ.`
  - Apparatus (Beta code): `E)N H(ME/RA| O(/TE KRINEI= {+{N KRINEI= > KRI/NEI)}+} O( QEO\S TA\ KRUPTA\ TW=N A)NQRW/PWN, KATA\ TO\ EU)AGGE/LIO/N MOU, DIA\ *)IHSOU= {N *)IHSOU= XRISTOU= > XRISTOU= *)IHSOU= } XRISTOU=.`
- `ROM 4:12` · `variant`
  - Apparatus (Unicode): `καὶ πατέρα περιτομῆς τοῖς οὐκ ἐκ περιτομῆς μόνον, ἀλλὰ καὶ τοῖς στοιχοῦσιν τοῖς ἴχνεσιν τῆς πίστεως {NA πίστεως τῆς ἐν τῇ ἀκροβυστίᾳ > ἐν ἀκροβυστίᾳ πίστεως } τῆς ἐν τῇ {+{Byz τῇ > - - }+} ἀκροβυστίᾳ τοῦ πατρὸς ἡμῶν Ἀβραάμ.`
  - Apparatus (Beta code): `KAI\ PATE/RA PERITOMH=S TOI=S OU)K E)K PERITOMH=S MO/NON, A)LLA\ KAI\ TOI=S STOIXOU=SIN TOI=S I)/XNESIN TH=S PI/STEWS {N PI/STEWS TH=S E)N TH=| A)KROBUSTI/A| > E)N A)KROBUSTI/A| PI/STEWS } TH=S E)N TH=| {+{B TH=| > - - }+} A)KROBUSTI/A| TOU= PATRO\S H(MW=N *)ABRAA/M.`
- `ROM 16:7` · `variant`
  - Apparatus (Unicode): `Ἀσπάσασθε Ἀνδρόνικον καὶ Ἰουνίαν {+{NA Ἰουνίαν > Ἰουνιᾶν }+} τοὺς συγγενεῖς μου καὶ συναιχμαλώτους μου, οἵτινές εἰσιν ἐπίσημοι ἐν τοῖς ἀποστόλοις, οἳ καὶ πρὸ ἐμοῦ γεγόνασιν {NA γεγόνασιν > γέγοναν } ἐν χριστῷ.`
  - Apparatus (Beta code): `*)ASPA/SASQE *)ANDRO/NIKON KAI\ *)IOUNI/AN {+{N *)IOUNI/AN > *)IOUNIA=N }+} TOU\S SUGGENEI=S MOU KAI\ SUNAIXMALW/TOUS MOU, OI(/TINE/S EI)SIN E)PI/SHMOI E)N TOI=S A)POSTO/LOIS, OI(\ KAI\ PRO\ E)MOU= GEGO/NASIN {N GEGO/NASIN > GE/GONAN } E)N XRISTW=|.`
- `1CO 3:14` · `variant`
  - Apparatus (Unicode): `Εἴ τινος τὸ ἔργον μένει {+{NA μένει > μενεῖ }+} ὃ ἐποικοδόμησεν, μισθὸν λήψεται. {NA λήψεται > λήμψεται }`
  - Apparatus (Beta code): `*EI)/ TINOS TO\ E)/RGON ME/NEI {+{N ME/NEI > MENEI= }+} O(\ E)POIKODO/MHSEN, MISQO\N LH/YETAI. {N LH/YETAI > LH/MYETAI }`
- `EPH 1:17` · `variant`
  - Apparatus (Unicode): `ἵνα ὁ θεὸς τοῦ κυρίου ἡμῶν Ἰησοῦ χριστοῦ, ὁ πατὴρ τῆς δόξης, δῴη {+{NA δῴη > δώῃ }+} ὑμῖν πνεῦμα σοφίας καὶ ἀποκαλύψεως, ἐν ἐπιγνώσει αὐτοῦ·`
  - Apparatus (Beta code): `I(/NA O( QEO\S TOU= KURI/OU H(MW=N *)IHSOU= XRISTOU=, O( PATH\R TH=S DO/CHS, DW/H| {+{N DW/H| > DW/H| }+} U(MI=N PNEU=MA SOFI/AS KAI\ A)POKALU/YEWS, E)N E)PIGNW/SEI AU)TOU=:`
- `PHP 3:5` · `variant`
  - Apparatus (Unicode): `περιτομὴ {+{NA περιτομὴ > περιτομῇ }+} ὀκταήμερος, ἐκ γένους Ἰσραήλ, φυλῆς Βενιαμίν, Ἑβραῖος ἐξ Ἑβραίων, κατὰ νόμον Φαρισαῖος,`
  - Apparatus (Beta code): `PERITOMH\ {+{N PERITOMH\ > PERITOMH=| }+} O)KTAH/MEROS, E)K GE/NOUS *)ISRAH/L, FULH=S *BENIAMI/N, *(EBRAI=OS E)C *(EBRAI/WN, KATA\ NO/MON *FARISAI=OS,`
- `2PE 1:12` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `? *DIO\ OU)K {N OU)K A)MELH/SW > MELLH/SW } A)MELH/SW A)EI\ U(MA=S [-U(POMIMNH/S|KEIN-]{+U(POMIMNH|/SKEIN+} PERI\ TOU/TWN, KAI/PER EI)DO/TAS, KAI\ E)STHRIGME/NOUS E)N TH=| PAROU/SH| A)LHQEI/A|.`

## Derived-only differences

None: every derived-text difference is also a source-tier
difference.
