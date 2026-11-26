<!-- generated-file: do not edit by hand -->
> **Generated file. Do not edit by hand.**
> See the "Generated files" section of the repository README for the command
> that regenerates it.

# Diff: rp2018 -> rp2018-2023

- **Left:** `rp2018` (official; Published in print by VTR, Nuremberg)
- **Right:** `rp2018-2023` (released; Current maintained source; 2018 edition plus 2023 adjustments)
- **Source-tier differing verses:** 161
- **Derived-text differing verses (normalised):** 97
- **Apparatus-only changes (source differs, main text identical):** 156
- **Apparatus-only changes shown in Unicode:** 120
- **Apparatus-only changes with no Unicode difference (Beta-code encoding only):** 36
- **Derived-only differences (text differs, source-tier comparison unchanged):** 92

## Notation

- **Text** is the Unicode accented main text from
  `editions/rp2018/csv/accented/no-variants/` and
  `editions/rp2018-2023/csv/accented/no-variants/`.
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
  `editions/rp2018/csv/accented/with-variants/` and
  `editions/rp2018-2023/csv/accented/with-variants/`.

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
| `accents-breathings` | The main text differs only in accents or breathings. | 23 |
| `apparatus-code` | Only the apparatus code letters changed; the reading is identical. | 45 |
| `capitalization` | The main text differs only in capitalisation. | 2 |
| `punctuation` | The main text differs in punctuation (capitalisation is not considered here). | 2 |
| `variant` | The apparatus reading or note changed; the main text is identical. | 89 |

Category meanings and worked examples: [`../README.md#categories`](../README.md#categories).

## Books (source tier)

| Book | Differing verses |
| --- | ---: |
| `MAT` | 6 |
| `MAR` | 7 |
| `LUK` | 6 |
| `JOH` | 4 |
| `ACT` | 52 |
| `ROM` | 10 |
| `1CO` | 2 |
| `PHP` | 1 |
| `2TI` | 1 |
| `HEB` | 2 |
| `JAM` | 5 |
| `1PE` | 9 |
| `2PE` | 10 |
| `1JO` | 4 |
| `2JO` | 2 |
| `3JO` | 1 |
| `JUD` | 2 |
| `REV` | 37 |

## Main-text changes (derived text differs)

The sections are grouped by the derived Unicode text; the category
is the source-tier classification. So a row can appear here while
its category names an apparatus change: the apparatus tag moved
while only the derived typography differs.

### LUK 11:18 · `punctuation`

Text:

```
Εἰ δὲ καὶ ὁ Σατανᾶς ἐφ' ἑαυτὸν διεμερίσθη, πῶς σταθήσεται ἡ βασιλεία αὐτοῦ; Ὅτι [-λέγετε,-]{+λέγετε+} [-Ἐν-]{+ἐν+} Βεελζεβοὺλ ἐκβάλλειν με τὰ δαιμόνια.
```

Source (Beta code):

```
*EI) DE\ KAI\ O( *SATANA=S E)F' E(AUTO\N DIEMERI/SQH, PW=S STAQH/SETAI H( BASILEI/A AU)TOU=; *(/OTI [-LE/GETE,-]{+LE/GETE+} [-*)EN-]{+E)N+} *BEELZEBOU\L E)KBA/LLEIN ME TA\ DAIMO/NIA.
```

### ACT 1:15 · `apparatus-code`

Apparatus code: `N` -> `C` (the reading is unchanged)

Text (derived; typographic only, not part of the source-tier change):

```
Καὶ ἐν ταῖς ἡμέραις ταύταις ἀναστὰς Πέτρος ἐν μέσῳ τῶν μαθητῶν [-εἶπεν --]{+εἶπεν-+} ἦν τε ὄχλος ὀνομάτων ἐπὶ τὸ αὐτὸ ὡς ἑκατὸν [-εἴκοσι --]{+εἴκοσι-+}
```

Source (Beta code):

```
? *KAI\ E)N TAI=S H(ME/RAIS TAU/TAIS A)NASTA\S *PE/TROS E)N ME/SW| TW=N MAQHTW=N {N MAQHTW=N > A)DELFW=N } EI)=PEN - H)=N TE O)/XLOS O)NOMA/TWN E)PI\ TO\ AU)TO\ W(S [-{N-]{+{C+} W(S > W(SEI\ } E(KATO\N EI)/KOSI -
```

Apparatus (Unicode):

```
Καὶ ἐν ταῖς ἡμέραις ταύταις ἀναστὰς Πέτρος ἐν μέσῳ τῶν μαθητῶν {NA μαθητῶν > ἀδελφῶν } [-εἶπεν --]{+εἶπεν-+} ἦν τε ὄχλος ὀνομάτων ἐπὶ τὸ αὐτὸ ὡς [-{NA-]{+{NA27/28+} ὡς > ὡσεὶ } ἑκατὸν [-εἴκοσι --]{+εἴκοσι-+}
```

### ROM 11:22 · `accents-breathings`

Text:

```
Ἴδε οὖν χρηστότητα καὶ ἀποτομίαν θεοῦ· ἐπὶ μὲν τοὺς πεσόντας, ἀποτομίαν· ἐπὶ [-δὲ-]{+δέ+} [-σὲ,-]{+σε,+} χρηστότητα, ἐὰν ἐπιμείνῃς τῇ χρηστότητι· ἐπεὶ καὶ σὺ ἐκκοπήσῃ.
```

Source (Beta code):

```
*)/IDE OU)=N XRHSTO/THTA KAI\ A)POTOMI/AN QEOU=: E)PI\ ME\N TOU\S PESO/NTAS, A)POTOMI/AN: {N A)POTOMI/AN E)PI\ > A)POTOMI/A E)PI\ } E)PI\ [-DE\-]{+DE/+} [-SE\,-]{+SE,+} XRHSTO/THTA, {N XRHSTO/THTA E)A\N E)PIMEI/NHS| > XRHSTO/THS QEOU= E)A\N E)PIME/NHS| } E)A\N E)PIMEI/NHS| TH=| XRHSTO/THTI: E)PEI\ KAI\ SU\ E)KKOPH/SH|.
```

### 1CO 14:7 · `accents-breathings`

Text:

```
Ὅμως τὰ ἄψυχα φωνὴν διδόντα, εἴτε αὐλός, εἴτε κιθάρα, ἐὰν διαστολὴν τοῖς φθόγγοις μὴ [-διδῶ,-]{+διδῷ,+} πῶς γνωσθήσεται τὸ αὐλούμενον ἢ τὸ κιθαριζόμενον;
```

Source (Beta code):

```
*(/OMWS TA\ A)/YUXA FWNH\N DIDO/NTA, EI)/TE AU)LO/S, EI)/TE KIQA/RA, E)A\N DIASTOLH\N TOI=S FQO/GGOIS MH\ [-DIDW=,-]{+DIDW=|,+} {N [-DIDW=-]{+DIDW=|+} > DW=| } PW=S GNWSQH/SETAI TO\ AU)LOU/MENON H)\ TO\ KIQARIZO/MENON;
```

### REV 21:18 · `punctuation`

Text:

```
Καὶ ἦν ἡ ἐνδόμησις τοῦ τείχους [-αὐτῆς,-]{+αὐτῆς+} ἴασπις· καὶ ἡ πόλις χρυσίον καθαρόν, ὅμοιον ὑέλῳ καθαρῷ.
```

Source (Beta code):

```
*KAI\ H)=N {N H)=N > - } H( E)NDO/MHSIS {N E)NDO/MHSIS > E)NDW/MHSIS } TOU= TEI/XOUS [-AU)TH=S,-]{+AU)TH=S+} I)/ASPIS: KAI\ H( PO/LIS XRUSI/ON KAQARO/N, O(/MOION U(E/LW| {B U(E/LW| > U(A/LW| } {N U(E/LW| > U(A/LW| } KAQARW=|.
```

## Apparatus-only changes

Every entry here has the same normalised derived text; the category
names which source-tier value changed. It does not mean the source
main text is unchanged: a `capitalization` row can also land here
when the derived Unicode text carries no corresponding difference.

- `MAT 11:23` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*KAI\ SU/, *KAPERNAOU/M, {N *KAPERNAOU/M H( > *KAFARNAOU/M MH\ } H( E(/WS TOU= {N TOU= > - } OU)RANOU= U(YWQEI=SA, {B U(YWQEI=SA > U(YWQH=S| } {N U(YWQEI=SA > U(YWQH/SH| } E(/WS [-*(/A|DOU-]{+*(/AD|OU+} KATABIBASQH/SH|: {N KATABIBASQH/SH| > KATABH/SH| } O(/TI EI) E)N *SODO/MOIS E)GE/NONTO {N E)GE/NONTO > E)GENH/QHSAN } AI( DUNA/MEIS AI( GENO/MENAI E)N SOI/, E)/MEINAN {N E)/MEINAN > E)/MEINEN } A)\N ME/XRI TH=S SH/MERON.`
- `MAT 16:18` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*KA)GW\ DE/ SOI LE/GW, O(/TI SU\ EI)= *PE/TROS, KAI\ E)PI\ TAU/TH| TH=| PE/TRA| OI)KODOMH/SW MOU TH\N E)KKLHSI/AN, KAI\ PU/LAI [-*(/A|DOU-]{+*(/AD|OU+} OU) KATISXU/SOUSIN AU)TH=S.`
- `MAT 17:21` · `variant`
  - Apparatus (Unicode): `Τοῦτο δὲ τὸ γένος οὐκ ἐκπορεύεται εἰ μὴ ἐν προσευχῇ καὶ νηστείᾳ. {NA [---]{+~+} }`
  - Apparatus (Beta code): `*TOU=TO DE\ TO\ GE/NOS OU)K E)KPOREU/ETAI EI) MH\ E)N PROSEUXH=| KAI\ NHSTEI/A|. {N [---]{+~+} }`
- `MAT 18:11` · `variant`
  - Apparatus (Unicode): `Ἦλθεν γὰρ ὁ υἱὸς τοῦ ἀνθρώπου σῶσαι τὸ ἀπολωλός. {NA [---]{+~+} }`
  - Apparatus (Beta code): `*)=HLQEN GA\R O( UI(O\S TOU= A)NQRW/POU SW=SAI TO\ A)POLWLO/S. {N [---]{+~+} }`
- `MAT 26:60` · `variant`
  - Apparatus (Unicode): `καὶ οὐχ εὗρον. Καὶ {NA [-καὶ-]{+Καὶ+} πολλῶν > πολλῶν } πολλῶν ψευδομαρτύρων {NA ψευδομαρτύρων προσελθόντων οὐχ εὗρον > προσελθόντων ψευδομαρτύρων } προσελθόντων, οὐχ εὗρον.`
  - Apparatus (Beta code): `KAI\ OU)X EU(=RON. *KAI\ {N [-KAI\-]{+*KAI\+} POLLW=N > POLLW=N } POLLW=N YEUDOMARTU/RWN {N YEUDOMARTU/RWN PROSELQO/NTWN OU)X EU(=RON > PROSELQO/NTWN YEUDOMARTU/RWN } PROSELQO/NTWN, OU)X EU(=RON.`
- `MAT 27:18` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `[-*)/H|DEI-]{+*)/HD|EI+} GA\R O(/TI DIA\ FQO/NON PARE/DWKAN AU)TO/N.`
- `MAR 7:16` · `variant`
  - Apparatus (Unicode): `Εἴ τις ἔχει ὦτα ἀκούειν ἀκουέτω. {NA [---]{+~+} }`
  - Apparatus (Beta code): `*EI)/ TIS E)/XEI W)=TA A)KOU/EIN A)KOUE/TW. {N [---]{+~+} }`
- `MAR 9:44` · `variant`
  - Apparatus (Unicode): `ὅπου ὁ σκώληξ αὐτῶν οὐ τελευτᾷ, καὶ τὸ πῦρ οὐ σβέννυται. {NA [---]{+~+} }`
  - Apparatus (Beta code): `O(/POU O( SKW/LHC AU)TW=N OU) TELEUTA=|, KAI\ TO\ PU=R OU) SBE/NNUTAI. {N [---]{+~+} }`
- `MAR 9:46` · `variant`
  - Apparatus (Unicode): `ὅπου ὁ σκώληξ αὐτῶν οὐ τελευτᾷ, καὶ τὸ πῦρ οὐ σβέννυται. {NA [---]{+~+} }`
  - Apparatus (Beta code): `O(/POU O( SKW/LHC AU)TW=N OU) TELEUTA=|, KAI\ TO\ PU=R OU) SBE/NNUTAI. {N [---]{+~+} }`
- `MAR 11:26` · `variant`
  - Apparatus (Unicode): `Εἰ δὲ ὑμεῖς οὐκ ἀφίετε, οὐδὲ ὁ πατὴρ ὑμῶν ὁ ἐν τοῖς οὐρανοῖς ἀφήσει τὰ παραπτώματα ὑμῶν. {NA [---]{+~+} }`
  - Apparatus (Beta code): `*EI) DE\ U(MEI=S OU)K A)FI/ETE, OU)DE\ O( PATH\R U(MW=N O( E)N TOI=S OU)RANOI=S A)FH/SEI TA\ PARAPTW/MATA U(MW=N. {N [---]{+~+} }`
- `MAR 14:65` · `capitalization`
  - Apparatus (Unicode): `Καὶ ἤρξαντό τινες ἐμπτύειν αὐτῷ, καὶ περικαλύπτειν τὸ {NA τὸ πρόσωπον αὐτοῦ > αὐτοῦ τὸ πρόσωπον } πρόσωπον αὐτοῦ, καὶ κολαφίζειν αὐτόν, καὶ λέγειν αὐτῷ, Προφήτευσον. Καὶ οἱ ὑπηρέται ῥαπίσμασιν αὐτὸν [-ἔβαλλον.{Byz-]{+ἔβαλλον. {Byz+} ἔβαλλον > ἔβαλον } {NA ἔβαλλον > ἔλαβον }`
  - Apparatus (Beta code): `*KAI\ H)/RCANTO/ TINES E)MPTU/EIN AU)TW=|, KAI\ PERIKALU/PTEIN TO\ {N TO\ PRO/SWPON AU)TOU= > AU)TOU= TO\ PRO/SWPON } PRO/SWPON AU)TOU=, KAI\ KOLAFI/ZEIN AU)TO/N, KAI\ LE/GEIN AU)TW=|, *PROFH/TEUSON. *KAI\ OI( U(PHRE/TAI R(API/SMASIN AU)TO\N [-*E)/BALLON.{B-]{+E)/BALLON. {B+} E)/BALLON > E)/BALON } {N E)/BALLON > E)/LABON }`
- `MAR 15:28` · `variant`
  - Apparatus (Unicode): `Καὶ ἐπληρώθη ἡ γραφὴ ἡ λέγουσα, Καὶ μετὰ ἀνόμων ἐλογίσθη. {NA [---]{+~+} }`
  - Apparatus (Beta code): `*KAI\ E)PLHRW/QH H( GRAFH\ H( LE/GOUSA, *KAI\ META\ A)NO/MWN E)LOGI/SQH. {N [---]{+~+} }`
- `MAR 16:8` · `variant`
  - Apparatus (Unicode): `Καὶ ἐξελθοῦσαι ἔφυγον ἀπὸ τοῦ μνημείου· εἶχεν δὲ {NA δὲ > γὰρ } αὐτὰς τρόμος καὶ ἔκστασις· καὶ οὐδενὶ οὐδὲν εἶπον, {NA εἶπον > εἶπαν } ἐφοβοῦντο γάρ. {NA γάρ > γάρ "+" [-[[-]{+[["SHORTER+} [-"shorter-]{+ENDING"]]+} [-ending" ]]}-]{+}+}`
  - Apparatus (Beta code): `*KAI\ E)CELQOU=SAI E)/FUGON A)PO\ TOU= MNHMEI/OU: EI)=XEN DE\ {N DE\ > GA\R } AU)TA\S TRO/MOS KAI\ E)/KSTASIS: KAI\ OU)DENI\ OU)DE\N EI)=PON, {N EI)=PON > EI)=PAN } E)FOBOU=NTO GA/R. {N GA/R > GA/R "+" [["SHORTER [-ENDING"]]}-]{+ENDING"]] }+}`
- `LUK 9:22` · `capitalization`
  - Apparatus (Unicode): `εἰπὼν ὅτι Δεῖ τὸν υἱὸν τοῦ ἀνθρώπου πολλὰ παθεῖν, καὶ ἀποδοκιμασθῆναι ἀπὸ τῶν πρεσβυτέρων καὶ ἀρχιερέων καὶ γραμματέων, καὶ ἀποκτανθῆναι, καὶ τῇ τρίτῃ ἡμέρᾳ [-ἀναστῆναι.{Byz-]{+ἀναστῆναι. {Byz+} ἀναστῆναι > ἐγερθῆναι } {NA ἀναστῆναι > ἐγερθῆναι }`
  - Apparatus (Beta code): `EI)PW\N O(/TI *DEI= TO\N UI(O\N TOU= A)NQRW/POU POLLA\ PAQEI=N, KAI\ A)PODOKIMASQH=NAI A)PO\ TW=N PRESBUTE/RWN KAI\ A)RXIERE/WN KAI\ GRAMMATE/WN, KAI\ A)POKTANQH=NAI, KAI\ TH=| TRI/TH| H(ME/RA| [-*A)NASTH=NAI.{B-]{+A)NASTH=NAI. {B+} A)NASTH=NAI > E)GERQH=NAI } {N A)NASTH=NAI > E)GERQH=NAI }`
- `LUK 10:15` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*KAI\ SU/, *KAPERNAOU/M, {N *KAPERNAOU/M H( > *KAFARNAOU/M MH\ } H( E(/WS TOU= {N TOU= OU)RANOU= U(YWQEI=SA > OU)RANOU= U(YWQH/SH| } OU)RANOU= U(YWQEI=SA, E(/WS [-*(/A|DOU-]{+*(/AD|OU+} {N [-*(/A|DOU-]{+*(/AD|OU+} KATABIBASQH/SH| > TOU= [-*(/A|DOU-]{+*(/AD|OU+} KATABH/SH| } KATABIBASQH/SH|.`
- `LUK 16:23` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*KAI\ E)N TW=| [-*(/A|DH|-]{+*(/AD|H|+} E)PA/RAS TOU\S O)FQALMOU\S AU)TOU=, U(PA/RXWN E)N BASA/NOIS, O(RA=| TO\N {N TO\N > - } *)ABRAA\M A)PO\ MAKRO/QEN, KAI\ *LA/ZARON E)N TOI=S KO/LPOIS AU)TOU=.`
- `LUK 19:22` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*LE/GEI DE\ {N DE\ > - } AU)TW=|, *)EK TOU= STO/MATO/S SOU KRINW= SE, PONHRE\ DOU=LE. [-*)/H|DEIS-]{+*)/HD|EIS+} O(/TI E)GW\ A)/NQRWPOS AU)STHRO/S EI)MI, AI)/RWN O(\ OU)K E)/QHKA, KAI\ QERI/ZWN O(\ OU)K E)/SPEIRA:`
- `LUK 23:17` · `variant`
  - Apparatus (Unicode): `Ἀνάγκην δὲ εἶχεν ἀπολύειν αὐτοῖς κατὰ ἑορτὴν ἕνα. {NA [---]{+~+} }`
  - Apparatus (Beta code): `*)ANA/GKHN DE\ EI)=XEN A)POLU/EIN AU)TOI=S KATA\ E(ORTH\N E(/NA. {N [---]{+~+} }`
- `JOH 5:4` · `variant`
  - Apparatus (Unicode): `Ἄγγελος γὰρ κατὰ καιρὸν κατέβαινεν ἐν τῇ κολυμβήθρᾳ, καὶ ἐτάρασσεν τὸ ὕδωρ· ὁ οὖν πρῶτος ἐμβὰς μετὰ τὴν ταραχὴν τοῦ ὕδατος, ὑγιὴς ἐγίνετο, ᾧ δήποτε κατείχετο νοσήματι. {NA [---]{+~+} }`
  - Apparatus (Beta code): `*)/AGGELOS GA\R KATA\ KAIRO\N KATE/BAINEN E)N TH=| KOLUMBH/QRA|, KAI\ E)TA/RASSEN TO\ U(/DWR: O( OU)=N PRW=TOS E)MBA\S META\ TH\N TARAXH\N TOU= U(/DATOS, U(GIH\S E)GI/NETO, W(=| DH/POTE KATEI/XETO NOSH/MATI. {N [---]{+~+} }`
- `JOH 6:64` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*)ALL' EI)SI\N E)C U(MW=N TINES OI(\ OU) PISTEU/OUSIN. [-*)/H|DEI-]{+*)/HD|EI+} GA\R E)C A)RXH=S O( *)IHSOU=S, TI/NES EI)SI\N OI( MH\ PISTEU/ONTES, KAI\ TI/S E)STIN O( PARADW/SWN AU)TO/N.`
- `JOH 13:11` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `[-*)/H|DEI-]{+*)/HD|EI+} GA\R TO\N PARADIDO/NTA AU)TO/N: DIA\ TOU=TO EI)=PEN, *OU)XI\ {N *OU)XI\ > O(/TI *OU)XI\ } PA/NTES KAQAROI/ E)STE.`
- `JOH 18:2` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `[-*)/H|DEI-]{+*)/HD|EI+} DE\ KAI\ *)IOU/DAS, O( PARADIDOU\S AU)TO/N, TO\N TO/PON: O(/TI POLLA/KIS SUNH/XQH {B SUNH/XQH > SUNH/XQH KAI\ } O( *)IHSOU=S {N O( *)IHSOU=S > *)IHSOU=S } E)KEI= META\ TW=N MAQHTW=N AU)TOU=.`
- `ACT 1:10` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Καὶ ὡς ἀτενίζοντες ἦσαν εἰς τὸν οὐρανόν, πορευομένου αὐτοῦ, καὶ ἰδοὺ ἄνδρες δύο παρειστήκεισαν αὐτοῖς ἐν ἐσθῆτι [-{NA-]{+{NA27/28+} ἐσθῆτι λευκῇ > ἐσθήσεσιν λευκαῖς } λευκῇ,`
  - Apparatus (Beta code): `*KAI\ W(S A)TENI/ZONTES H)=SAN EI)S TO\N OU)RANO/N, POREUOME/NOU AU)TOU=, KAI\ I)DOU\ A)/NDRES DU/O PAREISTH/KEISAN AU)TOI=S E)N E)SQH=TI [-{N-]{+{C+} E)SQH=TI LEUKH=| > E)SQH/SESIN LEUKAI=S } LEUKH=|,`
- `ACT 1:26` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Καὶ ἔδωκαν κλήρους αὐτῶν, [-{NA-]{+{NA27/28+} αὐτῶν > αὐτοῖς } καὶ ἔπεσεν ὁ κλῆρος ἐπὶ Ματθίαν, {NA Ματθίαν > Μαθθίαν } καὶ συγκατεψηφίσθη μετὰ τῶν ἕνδεκα ἀποστόλων.`
  - Apparatus (Beta code): `*KAI\ E)/DWKAN KLH/ROUS AU)TW=N, [-{N-]{+{C+} AU)TW=N > AU)TOI=S } KAI\ E)/PESEN O( KLH=ROS E)PI\ *MATQI/AN, {N *MATQI/AN > *MAQQI/AN } KAI\ SUGKATEYHFI/SQH META\ TW=N E(/NDEKA A)POSTO/LWN.`
- `ACT 2:3` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Καὶ ὤφθησαν αὐτοῖς διαμεριζόμεναι γλῶσσαι ὡσεὶ πυρός, ἐκάθισέν [-{NA-]{+{NA27/28+} ἐκάθισέν τε > καὶ ἐκάθισεν } τε ἐφ' ἕνα ἕκαστον αὐτῶν.`
  - Apparatus (Beta code): `*KAI\ W)/FQHSAN AU)TOI=S DIAMERIZO/MENAI GLW=SSAI W(SEI\ PURO/S, E)KA/QISE/N [-{N-]{+{C+} E)KA/QISE/N TE > KAI\ E)KA/QISEN } TE E)F' E(/NA E(/KASTON AU)TW=N.`
- `ACT 2:5` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Ἦσαν δὲ ἐν [-{NA-]{+{NA27/28+} ἐν > εἰς } Ἱερουσαλὴμ κατοικοῦντες Ἰουδαῖοι, ἄνδρες εὐλαβεῖς, ἀπὸ παντὸς ἔθνους τῶν ὑπὸ τὸν οὐρανόν.`
  - Apparatus (Beta code): `? *)=HSAN DE\ E)N [-{N-]{+{C+} E)N > EI)S } *(IEROUSALH\M KATOIKOU=NTES *)IOUDAI=OI, A)/NDRES EU)LABEI=S, A)PO\ PANTO\S E)/QNOUS TW=N U(PO\ TO\N OU)RANO/N.`
- `ACT 2:20` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `ὁ ἥλιος μεταστραφήσεται εἰς σκότος, καὶ ἡ σελήνη εἰς αἷμα, πρὶν ἢ [-{NA-]{+{NA27/28+} ἢ ἐλθεῖν τὴν > ἐλθεῖν } ἐλθεῖν τὴν ἡμέραν κυρίου τὴν μεγάλην καὶ ἐπιφανῆ·`
  - Apparatus (Beta code): `O( H(/LIOS METASTRAFH/SETAI EI)S SKO/TOS, KAI\ H( SELH/NH EI)S AI(=MA, PRI\N H)\ [-{N-]{+{C+} H)\ E)LQEI=N TH\N > E)LQEI=N } E)LQEI=N TH\N H(ME/RAN KURI/OU TH\N MEGA/LHN KAI\ E)PIFANH=:`
- `ACT 2:27` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `O(/TI OU)K E)GKATALEI/YEIS TH\N YUXH/N MOU EI)S [-*(/A|DOU,-]{+*(/AD|OU,+} {N [-*(/A|DOU-]{+*(/AD|OU+} > [-*(/A|DHN-]{+*(/AD|HN+} } OU)DE\ DW/SEIS TO\N O(/SIO/N SOU I)DEI=N DIAFQORA/N.`
- `ACT 2:31` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `PROI+DW\N E)LA/LHSEN PERI\ TH=S A)NASTA/SEWS TOU= XRISTOU=, O(/TI OU) {N OU) KATELEI/FQH > OU)/TE E)GKATELEI/FQH } KATELEI/FQH H( {N H( YUXH\ AU)TOU= > - } YUXH\ AU)TOU= EI)S [-*(/A|DOU,-]{+*(/AD|OU,+} {N [-*(/A|DOU-]{+*(/AD|OU+} OU)DE\ > [-*(/A|DHN-]{+*(/AD|HN+} OU)/TE } OU)DE\ H( SA\RC AU)TOU= EI)=DEN DIAFQORA/N.`
- `ACT 2:33` · `variant`
  - Apparatus (Unicode): `Τῇ δεξιᾷ οὖν τοῦ θεοῦ ὑψωθείς, τήν τε ἐπαγγελίαν τοῦ ἁγίου {NA ἁγίου πνεύματος > πνεύματος τοῦ ἁγίου } πνεύματος λαβὼν παρὰ τοῦ πατρός, ἐξέχεεν τοῦτο ὃ νῦν {NA νῦν {+> - } ὑμεῖς {NA27/28+} ὑμεῖς > ὑμεῖς [καὶ] } [-ὑμεῖς-] βλέπετε καὶ ἀκούετε.`
  - Apparatus (Beta code): `*TH=| DECIA=| OU)=N TOU= QEOU= U(YWQEI/S, TH/N TE E)PAGGELI/AN TOU= A(GI/OU {N A(GI/OU PNEU/MATOS > PNEU/MATOS TOU= A(GI/OU } PNEU/MATOS LABW\N PARA\ TOU= PATRO/S, E)CE/XEEN TOU=TO O(\ NU=N {N NU=N {+> - } U(MEI=S {C+} U(MEI=S > U(MEI=S [KAI\] } [-U(MEI=S-] BLE/PETE KAI\ A)KOU/ETE.`
- `ACT 3:13` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Ὁ θεὸς Ἀβραὰμ καὶ Ἰσαὰκ [-{NA-]{+{NA27/28+} Ἰσαὰκ καὶ > [ὁ θεὸς] Ἰσαὰκ καὶ [ὁ θεὸς] } καὶ Ἰακώβ, ὁ θεὸς τῶν πατέρων ἡμῶν, ἐδόξασεν τὸν παῖδα αὐτοῦ Ἰησοῦν· ὃν ὑμεῖς μὲν παρεδώκατε, καὶ ἠρνήσασθε αὐτὸν {NA αὐτὸν > - } κατὰ πρόσωπον Πιλάτου, κρίναντος ἐκείνου ἀπολύειν.`
  - Apparatus (Beta code): `*(O QEO\S *)ABRAA\M KAI\ *)ISAA\K [-{N-]{+{C+} *)ISAA\K KAI\ > [O( QEO\S] *)ISAA\K KAI\ [O( QEO\S] } KAI\ *)IAKW/B, O( QEO\S TW=N PATE/RWN H(MW=N, E)DO/CASEN TO\N PAI=DA AU)TOU= *)IHSOU=N: O(\N U(MEI=S ME\N PAREDW/KATE, KAI\ H)RNH/SASQE AU)TO\N {N AU)TO\N > - } KATA\ PRO/SWPON *PILA/TOU, KRI/NANTOS E)KEI/NOU A)POLU/EIN.`
- `ACT 4:4` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Πολλοὶ δὲ τῶν ἀκουσάντων τὸν λόγον ἐπίστευσαν· καὶ ἐγενήθη ὁ {NA ὁ > [ὁ] } ἀριθμὸς τῶν ἀνδρῶν ὡσεὶ [-{NA-]{+{NA27/28+} ὡσεὶ > [ὡς] } χιλιάδες πέντε.`
  - Apparatus (Beta code): `*POLLOI\ DE\ TW=N A)KOUSA/NTWN TO\N LO/GON E)PI/STEUSAN: KAI\ E)GENH/QH O( {N O( > [O(] } A)RIQMO\S TW=N A)NDRW=N W(SEI\ [-{N-]{+{C+} W(SEI\ > [W(S] } XILIA/DES PE/NTE.`
- `ACT 5:26` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Τότε ἀπελθὼν ὁ στρατηγὸς σὺν τοῖς ὑπηρέταις ἤγαγεν [-{NA-]{+{NA27/28+} ἤγαγεν > ἦγεν } αὐτούς, οὐ μετὰ βίας, ἐφοβοῦντο γὰρ τὸν λαόν, ἵνα {NA ἵνα > - } μὴ λιθασθῶσιν.`
  - Apparatus (Beta code): `*TO/TE A)PELQW\N O( STRATHGO\S SU\N TOI=S U(PHRE/TAIS H)/GAGEN [-{N-]{+{C+} H)/GAGEN > H)=GEN } AU)TOU/S, OU) META\ BI/AS, E)FOBOU=NTO GA\R TO\N LAO/N, I(/NA {N I(/NA > - } MH\ LIQASQW=SIN.`
- `ACT 5:31` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Τοῦτον ὁ θεὸς ἀρχηγὸν καὶ σωτῆρα ὕψωσεν τῇ δεξιᾷ αὐτοῦ, δοῦναι [-{NA-]{+{NA27/28+} δοῦναι > [τοῦ] δοῦναι } μετάνοιαν τῷ Ἰσραὴλ καὶ ἄφεσιν ἁμαρτιῶν.`
  - Apparatus (Beta code): `*TOU=TON O( QEO\S A)RXHGO\N KAI\ SWTH=RA U(/YWSEN TH=| DECIA=| AU)TOU=, DOU=NAI [-{N-]{+{C+} DOU=NAI > [TOU=] DOU=NAI } META/NOIAN TW=| *)ISRAH\L KAI\ A)/FESIN A(MARTIW=N.`
- `ACT 5:33` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Οἱ δὲ ἀκούοντες {Byz ἀκούοντες > ἀκούσαντες } {NA ἀκούοντες > ἀκούσαντες } διεπρίοντο, καὶ ἐβουλεύοντο [-{NA-]{+{NA27/28+} ἐβουλεύοντο > ἐβούλοντο } ἀνελεῖν αὐτούς.`
  - Apparatus (Beta code): `? *OI( DE\ A)KOU/ONTES {B A)KOU/ONTES > A)KOU/SANTES } {N A)KOU/ONTES > A)KOU/SANTES } DIEPRI/ONTO, KAI\ E)BOULEU/ONTO [-{N-]{+{C+} E)BOULEU/ONTO > E)BOU/LONTO } A)NELEI=N AU)TOU/S.`
- `ACT 7:7` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Καὶ τὸ ἔθνος, ᾧ ἐὰν δουλεύσωσιν, [-{NA-]{+{NA27/28+} δουλεύσωσιν > δουλεύσουσιν } κρινῶ ἐγώ, εἶπεν {NA εἶπεν ὁ θεός > ὁ θεὸς εἶπεν } ὁ θεός· καὶ μετὰ ταῦτα ἐξελεύσονται, καὶ λατρεύσουσίν μοι ἐν τῷ τόπῳ τούτῳ.`
  - Apparatus (Beta code): `*KAI\ TO\ E)/QNOS, W(=| E)A\N DOULEU/SWSIN, [-{N-]{+{C+} DOULEU/SWSIN > DOULEU/SOUSIN } KRINW= E)GW/, EI)=PEN {N EI)=PEN O( QEO/S > O( QEO\S EI)=PEN } O( QEO/S: KAI\ META\ TAU=TA E)CELEU/SONTAI, KAI\ LATREU/SOUSI/N MOI E)N TW=| TO/PW| TOU/TW|.`
- `ACT 7:22` · `variant`
  - Apparatus (Unicode): `Καὶ ἐπαιδεύθη Μωσῆς {NA Μωσῆς > Μωϋσῆς [-[ἐν]-] } πάσῃ {+{NA27/28 πάσῃ > [ἐν] πάσῃ }+} σοφίᾳ Αἰγυπτίων· ἦν δὲ δυνατὸς ἐν λόγοις καὶ ἔργοις. {NA ἔργοις > ἔργοις αὐτοῦ }`
  - Apparatus (Beta code): `*KAI\ E)PAIDEU/QH *MWSH=S {N *MWSH=S > *MWU+SH=S [-[E)N]-] } PA/SH| {+{C PA/SH| > [E)N] PA/SH| }+} SOFI/A| *AI)GUPTI/WN: H)=N DE\ DUNATO\S E)N LO/GOIS KAI\ E)/RGOIS. {N E)/RGOIS > E)/RGOIS AU)TOU= }`
- `ACT 8:31` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Ὁ δὲ εἶπεν, Πῶς γὰρ ἂν δυναίμην, ἐὰν μή τις ὁδηγήσῃ [-{NA-]{+{NA27/28+} ὁδηγήσῃ > ὁδηγήσει } με; Παρεκάλεσέν τε τὸν Φίλιππον ἀναβάντα καθίσαι σὺν αὐτῷ.`
  - Apparatus (Beta code): `*(O DE\ EI)=PEN, *PW=S GA\R A)\N DUNAI/MHN, E)A\N MH/ TIS O(DHGH/SH| [-{N-]{+{C+} O(DHGH/SH| > O(DHGH/SEI } ME; *PAREKA/LESE/N TE TO\N *FI/LIPPON A)NABA/NTA KAQI/SAI SU\N AU)TW=|.`
- `ACT 9:8` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Ἠγέρθη δὲ ὁ {NA ὁ > - } Σαῦλος ἀπὸ τῆς γῆς· ἀνεῳγμένων τε {NA τε > δὲ } τῶν ὀφθαλμῶν αὐτοῦ, οὐδένα [-{NA-]{+{NA27/28+} οὐδένα > οὐδὲν } ἔβλεπεν, χειραγωγοῦντες δὲ αὐτὸν εἰσήγαγον εἰς Δαμασκόν.`
  - Apparatus (Beta code): `*)HGE/RQH DE\ O( {N O( > - } *SAU=LOS A)PO\ TH=S GH=S: A)NEWG|ME/NWN TE {N TE > DE\ } TW=N O)FQALMW=N AU)TOU=, OU)DE/NA [-{N-]{+{C+} OU)DE/NA > OU)DE\N } E)/BLEPEN, XEIRAGWGOU=NTES DE\ AU)TO\N EI)SH/GAGON EI)S *DAMASKO/N.`
- `ACT 9:12` · `variant`
  - Apparatus (Unicode): `καὶ εἶδεν ἐν [-{NA-]{+{NA27/28+} ἐν ὁράματι ἄνδρα ὀνόματι Ἀνανίαν > ἄνδρα [ἐν ὁράματι] Ἁνανίαν ὀνόματι } {+{ECM ἐν ὁράματι ἄνδρα ὀνόματι Ἀνανίαν > ἄνδρα Ἁνανίαν ὀνόματι }+} ὁράματι ἄνδρα ὀνόματι Ἀνανίαν εἰσελθόντα καὶ ἐπιθέντα αὐτῷ χεῖρα, [-{NA-]{+{NA27/28+} χεῖρα > [τὰς] χεῖρας } {+{ECM χεῖρα > χεῖρας }+} ὅπως ἀναβλέψῃ.`
  - Apparatus (Beta code): `KAI\ EI)=DEN E)N [-{N-]{+{C+} E)N O(RA/MATI A)/NDRA O)NO/MATI *)ANANI/AN > A)/NDRA [E)N O(RA/MATI] *(ANANI/AN O)NO/MATI } {+{M E)N O(RA/MATI A)/NDRA O)NO/MATI *)ANANI/AN > A)/NDRA *(ANANI/AN O)NO/MATI }+} O(RA/MATI A)/NDRA O)NO/MATI *)ANANI/AN EI)SELQO/NTA KAI\ E)PIQE/NTA AU)TW=| XEI=RA, [-{N-]{+{C+} XEI=RA > [TA\S] XEI=RAS } {+{M XEI=RA > XEI=RAS }+} O(/PWS A)NABLE/YH|.`
- `ACT 9:21` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Ἐξίσταντο δὲ πάντες οἱ ἀκούοντες καὶ ἔλεγον, Οὐχ οὗτός ἐστιν ὁ πορθήσας ἐν [-{NA-]{+{NA27/28+} ἐν Ἱερουσαλὴμ > εἰς Ἰερουσαλὴμ } Ἱερουσαλὴμ τοὺς ἐπικαλουμένους τὸ ὄνομα τοῦτο, καὶ ὧδε εἰς τοῦτο ἐλήλυθεν {NA ἐλήλυθεν > ἐληλύθει } ἵνα δεδεμένους αὐτοὺς ἀγάγῃ ἐπὶ τοὺς ἀρχιερεῖς;`
  - Apparatus (Beta code): `*)ECI/STANTO DE\ PA/NTES OI( A)KOU/ONTES KAI\ E)/LEGON, *OU)X OU(=TO/S E)STIN O( PORQH/SAS E)N [-{N-]{+{C+} E)N *(IEROUSALH\M > EI)S *)IEROUSALH\M } *(IEROUSALH\M TOU\S E)PIKALOUME/NOUS TO\ O)/NOMA TOU=TO, KAI\ W(=DE EI)S TOU=TO E)LH/LUQEN {N E)LH/LUQEN > E)LHLU/QEI } I(/NA DEDEME/NOUS AU)TOU\S A)GA/GH| E)PI\ TOU\S A)RXIEREI=S;`
- `ACT 10:9` · `variant`
  - Apparatus (Unicode): `Τῇ δὲ ἐπαύριον, ὁδοιπορούντων ἐκείνων {+{ECM ἐκείνων > αὐτῶν }+} καὶ τῇ πόλει ἐγγιζόντων, ἀνέβη Πέτρος ἐπὶ τὸ δῶμα προσεύξασθαι, περὶ ὥραν ἕκτην·`
  - Apparatus (Beta code): `? *TH=| DE\ E)PAU/RION, O(DOIPOROU/NTWN E)KEI/NWN {+{M E)KEI/NWN > AU)TW=N }+} KAI\ TH=| PO/LEI E)GGIZO/NTWN, A)NE/BH *PE/TROS E)PI\ TO\ DW=MA PROSEU/CASQAI, PERI\ W(/RAN E(/KTHN:`
- `ACT 10:40` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Τοῦτον ὁ θεὸς ἤγειρεν τῇ [-{NA-]{+{NA27/28+} τῇ > [ἐν] τῇ } τρίτῃ ἡμέρᾳ, καὶ ἔδωκεν αὐτὸν ἐμφανῆ γενέσθαι,`
  - Apparatus (Beta code): `*TOU=TON O( QEO\S H)/GEIREN TH=| [-{N-]{+{C+} TH=| > [E)N] TH=| } TRI/TH| H(ME/RA|, KAI\ E)/DWKEN AU)TO\N E)MFANH= GENE/SQAI,`
- `ACT 11:22` · `variant`
  - Apparatus (Unicode): `Ἠκούσθη δὲ ὁ λόγος εἰς τὰ ὦτα τῆς ἐκκλησίας τῆς ἐν {NA ἐν Ἱεροσολύμοις > οὔσης ἐν Ἰερουσαλὴμ } Ἱεροσολύμοις περὶ αὐτῶν· καὶ ἐξαπέστειλαν Βαρνάβαν διελθεῖν [-{NA-]{+{NA27/28+} διελθεῖν > [διελθεῖν] } {+{ECM διελθεῖν > - }+} ἕως Ἀντιοχείας·`
  - Apparatus (Beta code): `*)HKOU/SQH DE\ O( LO/GOS EI)S TA\ W)=TA TH=S E)KKLHSI/AS TH=S E)N {N E)N *(IEROSOLU/MOIS > OU)/SHS E)N *)IEROUSALH\M } *(IEROSOLU/MOIS PERI\ AU)TW=N: KAI\ E)CAPE/STEILAN *BARNA/BAN DIELQEI=N [-{N-]{+{C+} DIELQEI=N > [DIELQEI=N] } {+{M DIELQEI=N > - }+} E(/WS *)ANTIOXEI/AS:`
- `ACT 12:11` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Καὶ ὁ Πέτρος, γενόμενος {NA γενόμενος ἐν ἑαυτῷ > ἐν ἑαυτῷ γενόμενος } ἐν ἑαυτῷ, εἶπεν, Νῦν οἶδα ἀληθῶς ὅτι ἐξαπέστειλεν κύριος [-{NA-]{+{NA27/28+} κύριος > [ὁ] κύριος } τὸν ἄγγελον αὐτοῦ, καὶ ἐξείλετό {NA ἐξείλετό > ἐξείλατό } με ἐκ χειρὸς Ἡρῴδου καὶ πάσης τῆς προσδοκίας τοῦ λαοῦ τῶν Ἰουδαίων.`
  - Apparatus (Beta code): `*KAI\ O( *PE/TROS, GENO/MENOS {N GENO/MENOS E)N E(AUTW=| > E)N E(AUTW=| GENO/MENOS } E)N E(AUTW=|, EI)=PEN, *NU=N OI)=DA A)LHQW=S O(/TI E)CAPE/STEILEN KU/RIOS [-{N-]{+{C+} KU/RIOS > [O(] KU/RIOS } TO\N A)/GGELON AU)TOU=, KAI\ E)CEI/LETO/ {N E)CEI/LETO/ > E)CEI/LATO/ } ME E)K XEIRO\S *(HRW/D|OU KAI\ PA/SHS TH=S PROSDOKI/AS TOU= LAOU= TW=N *)IOUDAI/WN.`
- `ACT 13:11` · `variant`
  - Apparatus (Unicode): `Καὶ νῦν ἰδού, χεὶρ κυρίου ἐπὶ σέ, καὶ ἔσῃ τυφλός, μὴ βλέπων τὸν ἥλιον ἄχρι καιροῦ. Παραχρῆμα δὲ [-{NA-]{+{NA27/28+} δὲ ἐπέπεσεν > τε ἔπεσεν {+} {ECM δὲ ἐπέπεσεν > τε ἐπέπεσεν+} } ἐπέπεσεν ἐπ' αὐτὸν ἀχλὺς καὶ σκότος, καὶ περιάγων ἐζήτει χειραγωγούς.`
  - Apparatus (Beta code): `*KAI\ NU=N I)DOU/, XEI\R KURI/OU E)PI\ SE/, KAI\ E)/SH| TUFLO/S, MH\ BLE/PWN TO\N H(/LION A)/XRI KAIROU=. *PARAXRH=MA DE\ [-{N-]{+{C+} DE\ E)PE/PESEN > TE E)/PESEN {+} {M DE\ E)PE/PESEN > TE E)PE/PESEN+} } E)PE/PESEN E)P' AU)TO\N A)XLU\S KAI\ SKO/TOS, KAI\ PERIA/GWN E)ZH/TEI XEIRAGWGOU/S.`
- `ACT 13:32` · `variant`
  - Apparatus (Unicode): `Καὶ ἡμεῖς ὑμᾶς εὐαγγελιζόμεθα τὴν πρὸς τοὺς πατέρας ἐπαγγελίαν γενομένην, ὅτι ταύτην ὁ θεὸς ἐκπεπλήρωκεν τοῖς τέκνοις αὐτῶν [-{NA-]{+ἡμῖν, {NA27/28 τέκνοις+} αὐτῶν {+ἡμῖν+} > {+τέκνοις+} [αὐτῶν] {+ἡμῖν+} } [-ἡμῖν,-]{+{ECM τέκνοις αὐτῶν ἡμῖν > τέκνοις ἡμῖν ʽξςʼ }+} ἀναστήσας Ἰησοῦν·`
  - Apparatus (Beta code): `*KAI\ H(MEI=S U(MA=S EU)AGGELIZO/MEQA TH\N PRO\S TOU\S PATE/RAS E)PAGGELI/AN GENOME/NHN, O(/TI TAU/THN O( QEO\S E)KPEPLH/RWKEN TOI=S TE/KNOIS AU)TW=N [-{N-]{+H(MI=N, {C TE/KNOIS+} AU)TW=N {+H(MI=N+} > {+TE/KNOIS+} [AU)TW=N] {+H(MI=N+} } [-H(MI=N,-]{+{M TE/KNOIS AU)TW=N H(MI=N > TE/KNOIS H(MI=N (cj) }+} A)NASTH/SAS *)IHSOU=N:`
- `ACT 14:3` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Ἱκανὸν μὲν οὖν χρόνον διέτριψαν παρρησιαζόμενοι ἐπὶ τῷ κυρίῳ τῷ μαρτυροῦντι τῷ [-{NA-]{+{NA27/28+} μαρτυροῦντι > μαρτυροῦντι [ἐπὶ] } λόγῳ τῆς χάριτος αὐτοῦ, διδόντι σημεῖα καὶ τέρατα γίνεσθαι διὰ τῶν χειρῶν αὐτῶν.`
  - Apparatus (Beta code): `*(IKANO\N ME\N OU)=N XRO/NON DIE/TRIYAN PARRHSIAZO/MENOI E)PI\ TW=| KURI/W| TW=| MARTUROU=NTI TW=| [-{N-]{+{C+} MARTUROU=NTI > MARTUROU=NTI [E)PI\] } LO/GW| TH=S XA/RITOS AU)TOU=, DIDO/NTI SHMEI=A KAI\ TE/RATA GI/NESQAI DIA\ TW=N XEIRW=N AU)TW=N.`
- `ACT 14:10` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `εἶπεν μεγάλῃ τῇ [-{NA-]{+{NA27/28+} τῇ > - } φωνῇ, Ἀνάστηθι ἐπὶ τοὺς πόδας σου ὀρθῶς. {Byz ὀρθῶς > ὀρθός } {NA ὀρθῶς > ὀρθός } Καὶ ἥλλετο {NA ἥλλετο > ἥλατο } καὶ περιεπάτει.`
  - Apparatus (Beta code): `EI)=PEN MEGA/LH| TH=| [-{N-]{+{C+} TH=| > - } FWNH=|, *)ANA/STHQI E)PI\ TOU\S PO/DAS SOU O)RQW=S. {B O)RQW=S > O)RQO/S } {N O)RQW=S > O)RQO/S } *KAI\ H(/LLETO {N H(/LLETO > H(/LATO } KAI\ PERIEPA/TEI.`
- `ACT 15:4` · `variant`
  - Apparatus (Unicode): `Παραγενόμενοι δὲ εἰς Ἱερουσαλήμ, ἀπεδέχθησαν [-{NA-]{+{NA27/28+} ἀπεδέχθησαν ὑπὸ > παρεδέχθησαν ἀπὸ {+} {ECM ἀπεδέχθησαν ὑπὸ > παρεδέχθησαν ὑπὸ+} } ὑπὸ τῆς ἐκκλησίας καὶ τῶν ἀποστόλων καὶ τῶν πρεσβυτέρων, ἀνήγγειλάν τε ὅσα ὁ θεὸς ἐποίησεν μετ' αὐτῶν.`
  - Apparatus (Beta code): `*PARAGENO/MENOI DE\ EI)S *(IEROUSALH/M, A)PEDE/XQHSAN [-{N-]{+{C+} A)PEDE/XQHSAN U(PO\ > PAREDE/XQHSAN A)PO\ {+} {M A)PEDE/XQHSAN U(PO\ > PAREDE/XQHSAN U(PO\+} } U(PO\ TH=S E)KKLHSI/AS KAI\ TW=N A)POSTO/LWN KAI\ TW=N PRESBUTE/RWN, A)NH/GGEILA/N TE O(/SA O( QEO\S E)POI/HSEN MET' AU)TW=N.`
- `ACT 15:17` · `variant`
  - Apparatus (Unicode): `ὅπως ἂν ἐκζητήσωσιν οἱ κατάλοιποι τῶν ἀνθρώπων τὸν κύριον, καὶ πάντα τὰ ἔθνη, ἐφ' οὓς ἐπικέκληται τὸ ὄνομά μου ἐπ' αὐτούς, λέγει κύριος ὁ [-{NA-]{+{NA27/28+} ὁ ποιῶν ταῦτα πάντα > ποιῶν ταῦτα } {+{ECM ὁ ποιῶν ταῦτα πάντα > ὁ ποιῶν ταῦτα }+} ποιῶν ταῦτα πάντα.`
  - Apparatus (Beta code): `O(/PWS A)\N E)KZHTH/SWSIN OI( KATA/LOIPOI TW=N A)NQRW/PWN TO\N KU/RION, KAI\ PA/NTA TA\ E)/QNH, E)F' OU(\S E)PIKE/KLHTAI TO\ O)/NOMA/ MOU E)P' AU)TOU/S, LE/GEI KU/RIOS O( [-{N-]{+{C+} O( POIW=N TAU=TA PA/NTA > POIW=N TAU=TA } {+{M O( POIW=N TAU=TA PA/NTA > O( POIW=N TAU=TA }+} POIW=N TAU=TA PA/NTA.`
- `ACT 15:37` · `variant`
  - Apparatus (Unicode): `Βαρνάβας δὲ ἐβουλεύσατο {NA ἐβουλεύσατο [-συμπαραλαβεῖν-] > ἐβούλετο [-συμπαραλαβεῖν καὶ-] } συμπαραλαβεῖν τὸν Ἰωάννην, {+{NA27/28 τὸν Ἰωάννην > καὶ τὸν Ἰωάννην } {ECM τὸν Ἰωάννην > καὶ Ἰωάννην }+} τὸν καλούμενον Μάρκον.`
  - Apparatus (Beta code): `*BARNA/BAS DE\ E)BOULEU/SATO {N E)BOULEU/SATO [-SUMPARALABEI=N-] > E)BOU/LETO [-SUMPARALABEI=N KAI\-] } SUMPARALABEI=N TO\N *)IWA/NNHN, {+{C TO\N *)IWA/NNHN > KAI\ TO\N *)IWA/NNHN } {M TO\N *)IWA/NNHN > KAI\ *)IWA/NNHN }+} TO\N KALOU/MENON *MA/RKON.`
- `ACT 15:41` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Διήρχετο δὲ τὴν Συρίαν καὶ Κιλικίαν, [-{NA-]{+{NA27/28+} Κιλικίαν > [τὴν] Κιλικίαν } ἐπιστηρίζων τὰς ἐκκλησίας.`
  - Apparatus (Beta code): `*DIH/RXETO DE\ TH\N *SURI/AN KAI\ *KILIKI/AN, [-{N-]{+{C+} *KILIKI/AN > [TH\N] *KILIKI/AN } E)PISTHRI/ZWN TA\S E)KKLHSI/AS.`
- `ACT 16:11` · `variant`
  - Apparatus (Unicode): `Ἀναχθέντες οὖν [-{NA-]{+{NA27/28+} οὖν ἀπὸ τῆς > δὲ {+ἀπὸ } {ECM οὖν ἀπὸ τῆς > οὖν+} ἀπὸ } ἀπὸ τῆς Τρῳάδος, εὐθυδρομήσαμεν εἰς Σαμοθρᾴκην, τῇ τε {NA τε > δὲ } ἐπιούσῃ εἰς Νεάπολιν, {NA Νεάπολιν > Νέαν Πόλιν }`
  - Apparatus (Beta code): `? *)ANAXQE/NTES OU)=N [-{N-]{+{C+} OU)=N A)PO\ TH=S > DE\ {+A)PO\ } {M OU)=N A)PO\ TH=S > OU)=N+} A)PO\ } A)PO\ TH=S *TRWA|/DOS, EU)QUDROMH/SAMEN EI)S *SAMOQRA/K|HN, TH=| TE {N TE > DE\ } E)PIOU/SH| EI)S *NEA/POLIN, {N *NEA/POLIN > *NE/AN *PO/LIN }`
- `ACT 16:12` · `variant`
  - Apparatus (Unicode): `ἐκεῖθέν {NA ἐκεῖθέν τε > κἀκεῖθεν } τε εἰς Φιλίππους, ἥτις ἐστὶν πρώτη [-{NA-]{+τῆς μερίδος τῆς {NA27/28+} πρώτη {+τῆς μερίδος+} τῆς > πρώτη[ς] {+μερίδος τῆς ʽξςʼ+} } {+{ECM πρώτη+} τῆς μερίδος τῆς {+> πρώτη τῆς μερίδος }+} Μακεδονίας πόλις, κολωνεία· {NA κολωνεία > κολωνία } ἦμεν δὲ ἐν αὐτῇ {NA αὐτῇ > ταύτῃ } τῇ πόλει διατρίβοντες ἡμέρας τινάς.`
  - Apparatus (Beta code): `E)KEI=QE/N {N E)KEI=QE/N TE > KA)KEI=QEN } TE EI)S *FILI/PPOUS, H(/TIS E)STI\N PRW/TH [-{N-]{+TH=S MERI/DOS TH=S {C+} PRW/TH {+TH=S MERI/DOS+} TH=S > PRW/TH[S] {+MERI/DOS TH=S (cj)+} } {+{M PRW/TH+} TH=S MERI/DOS TH=S {+> PRW/TH TH=S MERI/DOS }+} *MAKEDONI/AS PO/LIS, KOLWNEI/A: {N KOLWNEI/A > KOLWNI/A } H)=MEN DE\ E)N AU)TH=| {N AU)TH=| > TAU/TH| } TH=| PO/LEI DIATRI/BONTES H(ME/RAS TINA/S.`
- `ACT 16:13` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Τῇ τε ἡμέρᾳ τῶν σαββάτων ἐξήλθομεν ἔξω τῆς πόλεως {NA πόλεως > πύλης } παρὰ ποταμόν, οὗ ἐνομίζετο [-{NA-]{+{NA27/28+} ἐνομίζετο προσευχὴ > ἐνομίζομεν προσευχὴν } προσευχὴ εἶναι, καὶ καθίσαντες ἐλαλοῦμεν ταῖς συνελθούσαις γυναιξίν.`
  - Apparatus (Beta code): `*TH=| TE H(ME/RA| TW=N SABBA/TWN E)CH/LQOMEN E)/CW TH=S PO/LEWS {N PO/LEWS > PU/LHS } PARA\ POTAMO/N, OU(= E)NOMI/ZETO [-{N-]{+{C+} E)NOMI/ZETO PROSEUXH\ > E)NOMI/ZOMEN PROSEUXH\N } PROSEUXH\ EI)=NAI, KAI\ KAQI/SANTES E)LALOU=MEN TAI=S SUNELQOU/SAIS GUNAICI/N.`
- `ACT 16:17` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Αὕτη κατακολουθήσασα [-{NA-]{+{NA27/28+} κατακολουθήσασα > κατακολουθοῦσα } τῷ Παύλῳ καὶ ἡμῖν, {Byz καὶ ἡμῖν > καὶ τῷ Σίλᾳ } ἔκραζεν λέγουσα, Οὗτοι οἱ ἄνθρωποι δοῦλοι τοῦ θεοῦ τοῦ ὑψίστου εἰσίν, οἵτινες καταγγέλλουσιν ἡμῖν {NA ἡμῖν ὁδὸν > ὑμῖν ὁδὸν } ὁδὸν σωτηρίας.`
  - Apparatus (Beta code): `*AU(/TH KATAKOLOUQH/SASA [-{N-]{+{C+} KATAKOLOUQH/SASA > KATAKOLOUQOU=SA } TW=| *PAU/LW| KAI\ H(MI=N, {B KAI\ H(MI=N > KAI\ TW=| *SI/LA| } E)/KRAZEN LE/GOUSA, *OU(=TOI OI( A)/NQRWPOI DOU=LOI TOU= QEOU= TOU= U(YI/STOU EI)SI/N, OI(/TINES KATAGGE/LLOUSIN H(MI=N {N H(MI=N O(DO\N > U(MI=N O(DO\N } O(DO\N SWTHRI/AS.`
- `ACT 16:27` · `variant`
  - Apparatus (Unicode): `Ἔξυπνος δὲ γενόμενος ὁ δεσμοφύλαξ, καὶ ἰδὼν ἀνεῳγμένας τὰς θύρας τῆς φυλακῆς, σπασάμενος μάχαιραν, [-{NA-]{+{NA27/28+} μάχαιραν [-ἔμελλεν-] > [τὴν] μάχαιραν {+} ἔμελλεν {NA ἔμελλεν >+} ἤμελλεν } [-ἔμελλεν-] ἑαυτὸν ἀναιρεῖν, νομίζων ἐκπεφευγέναι τοὺς δεσμίους.`
  - Apparatus (Beta code): `*)/ECUPNOS DE\ GENO/MENOS O( DESMOFU/LAC, KAI\ I)DW\N A)NEWG|ME/NAS TA\S QU/RAS TH=S FULAKH=S, SPASA/MENOS MA/XAIRAN, [-{N-]{+{C+} MA/XAIRAN [-E)/MELLEN-] > [TH\N] MA/XAIRAN {+} E)/MELLEN {N E)/MELLEN >+} H)/MELLEN } [-E)/MELLEN-] E(AUTO\N A)NAIREI=N, NOMI/ZWN E)KPEFEUGE/NAI TOU\S DESMI/OUS.`
- `ACT 16:28` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Ἐφώνησεν δὲ φωνῇ [-{NA-]{+{NA27/28+} φωνῇ μεγάλῃ ὁ > μεγάλῃ φωνῇ [ὁ] } μεγάλῃ ὁ Παῦλος λέγων, Μηδὲν πράξῃς σεαυτῷ κακόν· ἅπαντες γάρ ἐσμεν ἐνθάδε.`
  - Apparatus (Beta code): `*)EFW/NHSEN DE\ FWNH=| [-{N-]{+{C+} FWNH=| MEGA/LH| O( > MEGA/LH| FWNH=| [O(] } MEGA/LH| O( *PAU=LOS LE/GWN, *MHDE\N PRA/CHS| SEAUTW=| KAKO/N: A(/PANTES GA/R E)SMEN E)NQA/DE.`
- `ACT 18:7` · `variant`
  - Apparatus (Unicode): `Καὶ μεταβὰς ἐκεῖθεν ἦλθεν {NA ἦλθεν > εἰσῆλθεν } εἰς οἰκίαν τινὸς ὀνόματι Ἰούστου, [-{NA-]{+{NA27/28+} Ἰούστου > Τιτίου {+Ἰούστου } {ECM Ἰούστου > Τίτου+} Ἰούστου } σεβομένου τὸν θεόν, οὗ ἡ οἰκία ἦν συνομοροῦσα τῇ συναγωγῇ.`
  - Apparatus (Beta code): `*KAI\ METABA\S E)KEI=QEN H)=LQEN {N H)=LQEN > EI)SH=LQEN } EI)S OI)KI/AN TINO\S O)NO/MATI *)IOU/STOU, [-{N-]{+{C+} *)IOU/STOU > *TITI/OU {+*)IOU/STOU } {M *)IOU/STOU > *TI/TOU+} *)IOU/STOU } SEBOME/NOU TO\N QEO/N, OU(= H( OI)KI/A H)=N SUNOMOROU=SA TH=| SUNAGWGH=|.`
- `ACT 19:14` · `variant`
  - Apparatus (Unicode): `Ἦσαν δέ τινες [-{NA-]{+{NA27/28+} τινες υἱοὶ Σκευᾶ > τινος {+Σκευᾶ } {ECM τινες υἱοὶ Σκευᾶ > τινες+} Σκευᾶ } υἱοὶ Σκευᾶ Ἰουδαίου ἀρχιερέως ἑπτὰ οἱ {NA οἱ > υἱοὶ } τοῦτο ποιοῦντες.`
  - Apparatus (Beta code): `*)=HSAN DE/ TINES [-{N-]{+{C+} TINES UI(OI\ *SKEUA= > TINOS {+*SKEUA= } {M TINES UI(OI\ *SKEUA= > TINES+} *SKEUA= } UI(OI\ *SKEUA= *)IOUDAI/OU A)RXIERE/WS E(PTA\ OI( {N OI( > UI(OI\ } TOU=TO POIOU=NTES.`
- `ACT 19:15` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Ἀποκριθὲν δὲ τὸ πνεῦμα τὸ πονηρὸν εἶπεν, {NA εἶπεν > εἶπεν αὐτοῖς } Τὸν Ἰησοῦν [-{NA-]{+{NA27/28+} Ἰησοῦν > [μὲν] Ἰησοῦν } γινώσκω, καὶ τὸν Παῦλον ἐπίσταμαι· ὑμεῖς δὲ τίνες ἐστέ;`
  - Apparatus (Beta code): `*)APOKRIQE\N DE\ TO\ PNEU=MA TO\ PONHRO\N EI)=PEN, {N EI)=PEN > EI)=PEN AU)TOI=S } *TO\N *)IHSOU=N [-{N-]{+{C+} *)IHSOU=N > [ME\N] *)IHSOU=N } GINW/SKW, KAI\ TO\N *PAU=LON E)PI/STAMAI: U(MEI=S DE\ TI/NES E)STE/;`
- `ACT 20:5` · `variant`
  - Apparatus (Unicode): `Οὗτοι προσελθόντες [-{NA-]{+{NA27/28+} προσελθόντες > δὲ προελθόντες } {+{ECM προσελθόντες > δὲ προσελθόντες }+} ἔμενον ἡμᾶς ἐν Τρῳάδι.`
  - Apparatus (Beta code): `*OU(=TOI PROSELQO/NTES [-{N-]{+{C+} PROSELQO/NTES > DE\ PROELQO/NTES } {+{M PROSELQO/NTES > DE\ PROSELQO/NTES }+} E)/MENON H(MA=S E)N *TRWA|/DI.`
- `ACT 20:6` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Ἡμεῖς δὲ ἐξεπλεύσαμεν μετὰ τὰς ἡμέρας τῶν ἀζύμων ἀπὸ Φιλίππων, καὶ ἤλθομεν πρὸς αὐτοὺς εἰς τὴν Τρῳάδα ἄχρι ἡμερῶν πέντε, οὗ [-{NA-]{+{NA27/28+} οὗ > ὅπου } διετρίψαμεν ἡμέρας ἑπτά.`
  - Apparatus (Beta code): `*(HMEI=S DE\ E)CEPLEU/SAMEN META\ TA\S H(ME/RAS TW=N A)ZU/MWN A)PO\ *FILI/PPWN, KAI\ H)/LQOMEN PRO\S AU)TOU\S EI)S TH\N *TRWA|/DA A)/XRI H(MERW=N PE/NTE, OU(= [-{N-]{+{C+} OU(= > O(/POU } DIETRI/YAMEN H(ME/RAS E(PTA/.`
- `ACT 20:21` · `variant`
  - Apparatus (Unicode): `διαμαρτυρόμενος Ἰουδαίοις τε καὶ Ἕλλησιν τὴν εἰς τὸν {NA τὸν θεὸν > θεὸν } θεὸν μετάνοιαν, καὶ πίστιν τὴν {NA πίστιν τὴν > πίστιν } εἰς τὸν κύριον ἡμῶν Ἰησοῦν. {+{ECM Ἰησοῦν > Ἰησοῦν Χριστόν }+}`
  - Apparatus (Beta code): `DIAMARTURO/MENOS *)IOUDAI/OIS TE KAI\ *(/ELLHSIN TH\N EI)S TO\N {N TO\N QEO\N > QEO\N } QEO\N META/NOIAN, KAI\ PI/STIN TH\N {N PI/STIN TH\N > PI/STIN } EI)S TO\N KU/RION H(MW=N *)IHSOU=N. {+{M *)IHSOU=N > *)IHSOU=N *XRISTO/N }+}`
- `ACT 23:1` · `variant`
  - Apparatus (Unicode): `Ἀτενίσας δὲ ὁ Παῦλος τῷ συνεδρίῳ {+{ECM ὁ Παῦλος τῷ συνεδρίῳ > τῷ συνεδρίῳ ὁ Παῦλος }+} εἶπεν, Ἄνδρες ἀδελφοί, ἐγὼ πάσῃ συνειδήσει ἀγαθῇ πεπολίτευμαι τῷ θεῷ ἄχρι ταύτης τῆς ἡμέρας.`
  - Apparatus (Beta code): `*)ATENI/SAS DE\ O( *PAU=LOS TW=| SUNEDRI/W| {+{M O( *PAU=LOS TW=| SUNEDRI/W| > TW=| SUNEDRI/W| O( *PAU=LOS }+} EI)=PEN, *)/ANDRES A)DELFOI/, E)GW\ PA/SH| SUNEIDH/SEI A)GAQH=| PEPOLI/TEUMAI TW=| QEW=| A)/XRI TAU/THS TH=S H(ME/RAS.`
- `ACT 23:5` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Ἔφη τε ὁ Παῦλος, Οὐκ ᾔδειν, ἀδελφοί, ὅτι ἐστὶν ἀρχιερεύς· γέγραπται γάρ, Ἄρχοντα [-{NA-]{+{NA27/28+} Ἄρχοντα > ὅτι Ἄρχοντα } τοῦ λαοῦ σου οὐκ ἐρεῖς κακῶς.`
  - Apparatus (Beta code): `*)/EFH TE O( *PAU=LOS, *OU)K H)/D|EIN, A)DELFOI/, O(/TI E)STI\N A)RXIEREU/S: GE/GRAPTAI GA/R, *)/ARXONTA [-{N-]{+{C+} *)/ARXONTA > O(/TI *)/ARXONTA } TOU= LAOU= SOU OU)K E)REI=S KAKW=S.`
- `ACT 23:10` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Πολλῆς δὲ γενομένης [-{NA-]{+{NA27/28+} γενομένης > γινομένης } στάσεως, εὐλαβηθεὶς {NA εὐλαβηθεὶς > φοβηθεὶς } ὁ χιλίαρχος μὴ διασπασθῇ ὁ Παῦλος ὑπ' αὐτῶν, ἐκέλευσεν τὸ στράτευμα καταβῆναι {NA καταβῆναι καὶ > καταβὰν } καὶ ἁρπάσαι αὐτὸν ἐκ μέσου αὐτῶν, ἄγειν τε εἰς τὴν παρεμβολήν.`
  - Apparatus (Beta code): `*POLLH=S DE\ GENOME/NHS [-{N-]{+{C+} GENOME/NHS > GINOME/NHS } STA/SEWS, EU)LABHQEI\S {N EU)LABHQEI\S > FOBHQEI\S } O( XILI/ARXOS MH\ DIASPASQH=| O( *PAU=LOS U(P' AU)TW=N, E)KE/LEUSEN TO\ STRA/TEUMA KATABH=NAI {N KATABH=NAI KAI\ > KATABA\N } KAI\ A(RPA/SAI AU)TO\N E)K ME/SOU AU)TW=N, A)/GEIN TE EI)S TH\N PAREMBOLH/N.`
- `ACT 25:18` · `variant`
  - Apparatus (Unicode): `περὶ οὗ σταθέντες οἱ κατήγοροι οὐδεμίαν αἰτίαν ἐπέφερον {NA ἐπέφερον > ἔφερον } ὧν ὑπενόουν [-{NA-]{+{NA27/28+} ὑπενόουν ἐγώ > ἐγὼ ὑπενόουν πονηρῶν } {+{ECM ὑπενόουν ἐγώ > ἐγὼ ὑπενόουν πονηράν }+} ἐγώ,`
  - Apparatus (Beta code): `PERI\ OU(= STAQE/NTES OI( KATH/GOROI OU)DEMI/AN AI)TI/AN E)PE/FERON {N E)PE/FERON > E)/FERON } W(=N U(PENO/OUN [-{N-]{+{C+} U(PENO/OUN E)GW/ > E)GW\ U(PENO/OUN PONHRW=N } {+{M U(PENO/OUN E)GW/ > E)GW\ U(PENO/OUN PONHRA/N }+} E)GW/,`
- `ACT 27:8` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `μόλις τε παραλεγόμενοι αὐτὴν ἤλθομεν εἰς τόπον τινὰ καλούμενον Καλοὺς Λιμένας, ᾧ ἐγγὺς ἦν [-{NA-]{+{NA27/28+} ἦν πόλις > πόλις ἦν } πόλις Λασαία.`
  - Apparatus (Beta code): `MO/LIS TE PARALEGO/MENOI AU)TH\N H)/LQOMEN EI)S TO/PON TINA\ KALOU/MENON *KALOU\S *LIME/NAS, W(=| E)GGU\S H)=N [-{N-]{+{C+} H)=N PO/LIS > PO/LIS H)=N } PO/LIS *LASAI/A.`
- `ACT 27:23` · `apparatus-code`
  - Apparatus code: `N` -> `C` (the reading is unchanged)
  - Apparatus (Unicode): `Παρέστη γάρ μοι ταύτῃ τῇ νυκτὶ ἄγγελος {NA ἄγγελος > - } τοῦ θεοῦ, οὗ εἰμι, ᾧ [-{NA-]{+{NA27/28+} ᾧ > [ἐγὼ] ᾧ } καὶ λατρεύω, {NA λατρεύω > λατρεύω ἄγγελος }`
  - Apparatus (Beta code): `*PARE/STH GA/R MOI TAU/TH| TH=| NUKTI\ A)/GGELOS {N A)/GGELOS > - } TOU= QEOU=, OU(= EI)MI, W(=| [-{N-]{+{C+} W(=| > [E)GW\] W(=| } KAI\ LATREU/W, {N LATREU/W > LATREU/W A)/GGELOS }`
- `ACT 28:5` · `variant`
  - Apparatus (Unicode): `Ὁ μὲν οὖν, ἀποτινάξας {+{ECM ἀποτινάξας > ἀποτιναξάμενος }+} τὸ θηρίον εἰς τὸ πῦρ, ἔπαθεν οὐδὲν κακόν.`
  - Apparatus (Beta code): `*(O ME\N OU)=N, A)POTINA/CAS {+{M A)POTINA/CAS > A)POTINACA/MENOS }+} TO\ QHRI/ON EI)S TO\ PU=R, E)/PAQEN OU)DE\N KAKO/N.`
- `ACT 28:29` · `variant`
  - Apparatus (Unicode): `Καὶ ταῦτα αὐτοῦ εἰπόντος, ἀπῆλθον οἱ Ἰουδαῖοι, πολλὴν ἔχοντες ἐν ἑαυτοῖς συζήτησιν. {NA [---]{+~+} }`
  - Apparatus (Beta code): `*KAI\ TAU=TA AU)TOU= EI)PO/NTOS, A)PH=LQON OI( *)IOUDAI=OI, POLLH\N E)/XONTES E)N E(AUTOI=S SUZH/THSIN. {N [---]{+~+} }`
- `ROM 2:16` · `variant`
  - Apparatus (Unicode): `ἐν ἡμέρᾳ ὅτε κρινεῖ {NA κρινεῖ > [-κρίνεἰ}-]{+κρίνει }+} ὁ θεὸς τὰ κρυπτὰ τῶν ἀνθρώπων, κατὰ τὸ εὐαγγέλιόν μου, διὰ Ἰησοῦ {NA Ἰησοῦ χριστοῦ > χριστοῦ Ἰησοῦ } χριστοῦ.`
  - Apparatus (Beta code): `E)N H(ME/RA| O(/TE KRINEI= {N KRINEI= > [-KRI/NEI)}-]{+KRI/NEI }+} O( QEO\S TA\ KRUPTA\ TW=N A)NQRW/PWN, KATA\ TO\ EU)AGGE/LIO/N MOU, DIA\ *)IHSOU= {N *)IHSOU= XRISTOU= > XRISTOU= *)IHSOU= } XRISTOU=.`
- `ROM 4:12` · `variant`
  - Apparatus (Unicode): `καὶ πατέρα περιτομῆς τοῖς οὐκ ἐκ περιτομῆς μόνον, ἀλλὰ καὶ τοῖς στοιχοῦσιν τοῖς ἴχνεσιν τῆς πίστεως {NA πίστεως τῆς ἐν τῇ ἀκροβυστίᾳ > ἐν ἀκροβυστίᾳ πίστεως } τῆς ἐν τῇ {Byz τῇ > - [---] } ἀκροβυστίᾳ τοῦ πατρὸς ἡμῶν Ἀβραάμ.`
  - Apparatus (Beta code): `KAI\ PATE/RA PERITOMH=S TOI=S OU)K E)K PERITOMH=S MO/NON, A)LLA\ KAI\ TOI=S STOIXOU=SIN TOI=S I)/XNESIN TH=S PI/STEWS {N PI/STEWS TH=S E)N TH=| A)KROBUSTI/A| > E)N A)KROBUSTI/A| PI/STEWS } TH=S E)N TH=| {B TH=| > - [---] } A)KROBUSTI/A| TOU= PATRO\S H(MW=N *)ABRAA/M.`
- `ROM 14:24` · `variant`
  - Apparatus (Unicode): `Τῷ δὲ δυναμένῳ ὑμᾶς στηρίξαι κατὰ τὸ εὐαγγέλιόν μου καὶ τὸ κήρυγμα Ἰησοῦ χριστοῦ, κατὰ ἀποκάλυψιν μυστηρίου χρόνοις αἰωνίοις σεσιγημένου, [-{NA - }-]`
  - Apparatus (Beta code): `? *TW=| DE\ DUNAME/NW| U(MA=S STHRI/CAI KATA\ TO\ EU)AGGE/LIO/N MOU KAI\ TO\ KH/RUGMA *)IHSOU= XRISTOU=, KATA\ A)POKA/LUYIN MUSTHRI/OU XRO/NOIS AI)WNI/OIS SESIGHME/NOU, [-{N - }-]`
- `ROM 14:25` · `variant`
  - Apparatus (Unicode): `φανερωθέντος δὲ νῦν, διά τε γραφῶν προφητικῶν, κατ' ἐπιταγὴν τοῦ αἰωνίου θεοῦ, εἰς ὑπακοὴν πίστεως εἰς πάντα τὰ ἔθνη γνωρισθέντος, [-{NA - }-]`
  - Apparatus (Beta code): `FANERWQE/NTOS DE\ NU=N, DIA/ TE GRAFW=N PROFHTIKW=N, KAT' E)PITAGH\N TOU= AI)WNI/OU QEOU=, EI)S U(PAKOH\N PI/STEWS EI)S PA/NTA TA\ E)/QNH GNWRISQE/NTOS, [-{N - }-]`
- `ROM 14:26` · `variant`
  - Apparatus (Unicode): `μόνῳ σοφῷ θεῷ, διὰ Ἰησοῦ χριστοῦ, ᾧ ἡ δόξα εἰς τοὺς αἰῶνας. Ἀμήν. {NA [---]{+14.24--26 > ~+} }`
  - Apparatus (Beta code): `MO/NW| SOFW=| QEW=|, DIA\ *)IHSOU= XRISTOU=, W(=| H( DO/CA EI)S TOU\S AI)W=NAS. *)AMH/N. {N {+14.24+} - {+- 26 > ~+} }`
- `ROM 15:15` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*TOLMHRO/TERON DE\ E)/GRAYA U(MI=N, A)DELFOI/, {N A)DELFOI/ > - } A)PO\ ME/ROUS, W(S [-E)PANAMIMNH|/SKWN-]{+E)PANAMIMNH/S|KWN+} U(MA=S, DIA\ TH\N XA/RIN TH\N DOQEI=SA/N MOI U(PO\ TOU= QEOU=,`
- `ROM 16:7` · `variant`
  - Apparatus (Unicode): `Ἀσπάσασθε Ἀνδρόνικον καὶ Ἰουνίαν [-{NA Ἰουνίαν > Ἰουνιᾶν }-] τοὺς συγγενεῖς μου καὶ συναιχμαλώτους μου, οἵτινές εἰσιν ἐπίσημοι ἐν τοῖς ἀποστόλοις, οἳ καὶ πρὸ ἐμοῦ γεγόνασιν {NA γεγόνασιν > γέγοναν } ἐν χριστῷ.`
  - Apparatus (Beta code): `*)ASPA/SASQE *)ANDRO/NIKON KAI\ *)IOUNI/AN [-{N *)IOUNI/AN > *)IOUNIA=N }-] TOU\S SUGGENEI=S MOU KAI\ SUNAIXMALW/TOUS MOU, OI(/TINE/S EI)SIN E)PI/SHMOI E)N TOI=S A)POSTO/LOIS, OI(\ KAI\ PRO\ E)MOU= GEGO/NASIN {N GEGO/NASIN > GE/GONAN } E)N XRISTW=|.`
- `ROM 16:23` · `variant`
  - Apparatus (Unicode): `Ἀσπάζεται ὑμᾶς Γάϊος ὁ ξένος μου καὶ τῆς {NA τῆς ἐκκλησίας ὅλης > ὅλης τῆς ἐκκλησίας } ἐκκλησίας ὅλης. Ἀσπάζεται ὑμᾶς Ἔραστος ὁ οἰκονόμος τῆς πόλεως, καὶ Κούαρτος ὁ ἀδελφός. {NA ἀδελφός > ἀδελφός " ̈ [-[14.24 - 26]"-]{+[14.24--26]"+} }`
  - Apparatus (Beta code): `*)ASPA/ZETAI U(MA=S *GA/I+OS O( CE/NOS MOU KAI\ TH=S {N TH=S E)KKLHSI/AS O(/LHS > O(/LHS TH=S E)KKLHSI/AS } E)KKLHSI/AS O(/LHS. *)ASPA/ZETAI U(MA=S *)/ERASTOS O( OI)KONO/MOS TH=S PO/LEWS, KAI\ *KOU/ARTOS O( A)DELFO/S. {N A)DELFO/S > A)DELFO/S "+ [14.24 - {+-+} 26]" }`
- `ROM 16:24` · `variant`
  - Apparatus (Unicode): `Ἡ χάρις τοῦ κυρίου ἡμῶν Ἰησοῦ χριστοῦ μετὰ πάντων ὑμῶν. Ἀμήν. {NA [---]{+~+} }`
  - Apparatus (Beta code): `*(H XA/RIS TOU= KURI/OU H(MW=N *)IHSOU= XRISTOU= META\ PA/NTWN U(MW=N. *)AMH/N. {N [---]{+~+} }`
- `1CO 15:55` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*POU= SOU, *QA/NATE, TO\ KE/NTRON; {N KE/NTRON *POU= SOU [-*(/A|DH-]{+*(/AD|H+} TO\ NI=KOS > NI=KOS *POU= SOU *QA/NATE TO\ KE/NTRON } *POU= SOU, [-*(/A|DH,-]{+*(/AD|H,+} TO\ NI=KOS;`
- `PHP 4:23` · `variant`
  - Apparatus (Unicode): `Ἡ χάρις τοῦ κυρίου Ἰησοῦ χριστοῦ μετὰ πάντων {+ὑμῶν. Ἀμήν.+} {NA πάντων ὑμῶν. [-Ἀμην.-]{+Ἀμήν.+} > τοῦ πνεύματος ὑμῶν. } [-ὑμῶν. Ἀμήν.-]`
  - Apparatus (Beta code): `? *(H XA/RIS TOU= KURI/OU *)IHSOU= XRISTOU= META\ PA/NTWN {+U(MW=N. *)AMH/N.+} {N PA/NTWN U(MW=N. [-*)AMHN.-]{+*)AMH/N.+} > TOU= PNEU/MATOS U(MW=N. } [-U(MW=N. *)AMH/N.-]`
- `2TI 1:6` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*DI' H(\N AI)TI/AN [-A)NAMIMNH|/SKW-]{+A)NAMIMNH/S|KW+} SE A)NAZWPUREI=N TO\ XA/RISMA TOU= QEOU=, O(/ E)STIN E)N SOI\ DIA\ TH=S E)PIQE/SEWS TW=N XEIRW=N MOU.`
- `HEB 2:6` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*DIEMARTU/RATO DE/ POU/ TIS LE/GWN, *TI/ E)STIN A)/NQRWPOS, O(/TI [-MIMNH|/SKH|-]{+MIMNH/S|KH|+} AU)TOU=; *)\H UI(O\S A)NQRW/POU, O(/TI E)PISKE/PTH| AU)TO/N;`
- `HEB 13:3` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `[-*MIMNH|/SKESQE-]{+*MIMNH/S|KESQE+} TW=N DESMI/WN, W(S SUNDEDEME/NOI: TW=N KAKOUXOUME/NWN, W(S KAI\ AU)TOI\ O)/NTES E)N SW/MATI.`
- `JAM 1:20` · `apparatus-code`
  - Apparatus code: `N` -> `S` (the reading is unchanged)
  - Apparatus (Unicode): `ὀργὴ γὰρ ἀνδρὸς δικαιοσύνην θεοῦ οὐ [-{NA-]{+{NA27+} οὐ κατεργάζεται > οὐκ ἐργάζεται } κατεργάζεται.`
  - Apparatus (Beta code): `O)RGH\ GA\R A)NDRO\S DIKAIOSU/NHN QEOU= OU) [-{N-]{+{S+} OU) KATERGA/ZETAI > OU)K E)RGA/ZETAI } KATERGA/ZETAI.`
- `JAM 2:3` · `variant`
  - Apparatus (Unicode): `καὶ {NA καὶ ἐπιβλέψητε > ἐπιβλέψητε δὲ } ἐπιβλέψητε ἐπὶ τὸν φοροῦντα τὴν ἐσθῆτα τὴν λαμπράν, καὶ εἴπητε αὐτῷ, {NA αὐτῷ > - } Σὺ κάθου ὧδε καλῶς, καὶ τῷ πτωχῷ εἴπητε, Σὺ στῆθι ἐκεῖ, ἢ κάθου {+{NA28 ἐκεῖ ἢ κάθου > ἢ κάθου ἐκεῖ }+} ὧδε {NA ὧδε ὑπὸ > ὑπὸ } ὑπὸ τὸ ὑποπόδιόν μου·`
  - Apparatus (Beta code): `KAI\ {N KAI\ E)PIBLE/YHTE > E)PIBLE/YHTE DE\ } E)PIBLE/YHTE E)PI\ TO\N FOROU=NTA TH\N E)SQH=TA TH\N LAMPRA/N, KAI\ EI)/PHTE AU)TW=|, {N AU)TW=| > - } *SU\ KA/QOU W(=DE KALW=S, KAI\ TW=| PTWXW=| EI)/PHTE, *SU\ STH=QI E)KEI=, H)\ KA/QOU {+{E E)KEI= H)\ KA/QOU > H)\ KA/QOU E)KEI= }+} W(=DE {N W(=DE U(PO\ > U(PO\ } U(PO\ TO\ U(POPO/DIO/N MOU:`
- `JAM 2:4` · `apparatus-code`
  - Apparatus code: `N` -> `S` (the reading is unchanged)
  - Apparatus (Unicode): `καὶ [-{NA-]{+{NA27+} καὶ οὐ > οὐ } οὐ διεκρίθητε ἐν ἑαυτοῖς, καὶ ἐγένεσθε κριταὶ διαλογισμῶν πονηρῶν;`
  - Apparatus (Beta code): `KAI\ [-{N-]{+{S+} KAI\ OU) > OU) } OU) DIEKRI/QHTE E)N E(AUTOI=S, KAI\ E)GE/NESQE KRITAI\ DIALOGISMW=N PONHRW=N;`
- `JAM 2:15` · `apparatus-code`
  - Apparatus code: `N` -> `S` (the reading is unchanged)
  - Apparatus (Unicode): `Ἐὰν δὲ {NA δὲ > - } ἀδελφὸς ἢ ἀδελφὴ γυμνοὶ ὑπάρχωσιν καὶ λειπόμενοι ὦσιν [-{NA-]{+{NA27+} ὦσιν > - } τῆς ἐφημέρου τροφῆς,`
  - Apparatus (Beta code): `*)EA\N DE\ {N DE\ > - } A)DELFO\S H)\ A)DELFH\ GUMNOI\ U(PA/RXWSIN KAI\ LEIPO/MENOI W)=SIN [-{N-]{+{S+} W)=SIN > - } TH=S E)FHME/ROU TROFH=S,`
- `JAM 4:10` · `apparatus-code`
  - Apparatus code: `N` -> `S` (the reading is unchanged)
  - Apparatus (Unicode): `Ταπεινώθητε ἐνώπιον τοῦ [-{NA-]{+{NA27+} τοῦ > - } κυρίου, καὶ ὑψώσει ὑμᾶς.`
  - Apparatus (Beta code): `*TAPEINW/QHTE E)NW/PION TOU= [-{N-]{+{S+} TOU= > - } KURI/OU, KAI\ U(YW/SEI U(MA=S.`
- `1PE 1:6` · `variant`
  - Apparatus (Unicode): `Ἐν ᾧ ἀγαλλιᾶσθε, ὀλίγον ἄρτι, εἰ δέον ἐστίν, [-{NA-]{+{NA27+} ἐστίν > [ἐστίν] } λυπηθέντες {+{NA28 λυπηθέντες > λυπηθέντας }+} ἐν ποικίλοις πειρασμοῖς,`
  - Apparatus (Beta code): `*)EN W(=| A)GALLIA=SQE, O)LI/GON A)/RTI, EI) DE/ON E)STI/N, [-{N-]{+{S+} E)STI/N > [E)STI/N] } LUPHQE/NTES {+{E LUPHQE/NTES > LUPHQE/NTAS }+} E)N POIKI/LOIS PEIRASMOI=S,`
- `1PE 1:16` · `variant`
  - Apparatus (Unicode): `διότι γέγραπται, Ἅγιοι [-{NA-]{+{NA27+} Ἅγιοι γίνεσθε > [ὅτι] {+Ἅγιοι ἔσεσθε } {NA28 Ἅγιοι γίνεσθε >+} Ἅγιοι ἔσεσθε } γίνεσθε, ὅτι ἐγὼ ἅγιός εἰμι. [-{NA-]{+{NA27+} εἰμι > [εἰμι] } {+{NA28 εἰμι > - }+}`
  - Apparatus (Beta code): `DIO/TI GE/GRAPTAI, *(/AGIOI [-{N-]{+{S+} *(/AGIOI GI/NESQE > [O(/TI] {+*(/AGIOI E)/SESQE } {E *(/AGIOI GI/NESQE >+} *(/AGIOI E)/SESQE } GI/NESQE, O(/TI E)GW\ A(/GIO/S EI)MI. [-{N-]{+{S+} EI)MI > [EI)MI] } {+{E EI)MI > - }+}`
- `1PE 2:5` · `variant`
  - Apparatus (Unicode): `καὶ αὐτοὶ ὡς λίθοι ζῶντες οἰκοδομεῖσθε οἶκος πνευματικός, ἱεράτευμα {NA ἱεράτευμα > εἰς ἱεράτευμα } ἅγιον, ἀνενέγκαι πνευματικὰς θυσίας εὐπροσδέκτους τῷ [-{NA-]{+{NA27+} τῷ > [τῷ] {+} {NA28 τῷ > -+} } θεῷ διὰ Ἰησοῦ χριστοῦ.`
  - Apparatus (Beta code): `KAI\ AU)TOI\ W(S LI/QOI ZW=NTES OI)KODOMEI=SQE OI)=KOS PNEUMATIKO/S, I(ERA/TEUMA {N I(ERA/TEUMA > EI)S I(ERA/TEUMA } A(/GION, A)NENE/GKAI PNEUMATIKA\S QUSI/AS EU)PROSDE/KTOUS TW=| [-{N-]{+{S+} TW=| > [TW=|] {+} {E TW=| > -+} } QEW=| DIA\ *)IHSOU= XRISTOU=.`
- `1PE 2:10` · `variant`
  - Apparatus (Unicode): `οἱ ποτὲ {+{NA οἱ ποτὲ > οἵ ποτε }+} οὐ λαός, νῦν δὲ λαὸς θεοῦ· οἱ οὐκ ἠλεημένοι, νῦν δὲ ἐλεηθέντες.`
  - Apparatus (Beta code): `OI( POTE\ {+{N OI( POTE\ > OI(/ POTE }+} OU) LAO/S, NU=N DE\ LAO\S QEOU=: OI( OU)K H)LEHME/NOI, NU=N DE\ E)LEHQE/NTES.`
- `1PE 2:25` · `variant`
  - Apparatus (Unicode): `Ἦτε γὰρ ὡς πρόβατα πλανώμενα· {NA πλανώμενα {+> πλανώμενοι } ἀλλ' {NA27+} ἀλλ' > [-πλανώμενοι-] ἀλλὰ } [-ἀλλ'-] ἐπεστράφητε νῦν ἐπὶ τὸν ποιμένα καὶ ἐπίσκοπον τῶν ψυχῶν ὑμῶν.`
  - Apparatus (Beta code): `*)=HTE GA\R W(S PRO/BATA PLANW/MENA: {N PLANW/MENA {+> PLANW/MENOI } A)LL' {S+} A)LL' > [-PLANW/MENOI-] A)LLA\ } [-A)LL'-] E)PESTRA/FHTE NU=N E)PI\ TO\N POIME/NA KAI\ E)PI/SKOPON TW=N YUXW=N U(MW=N.`
- `1PE 4:16` · `apparatus-code`
  - Apparatus code: `N` -> `S` (the reading is unchanged)
  - Apparatus (Unicode): `εἰ δὲ ὡς Χριστιανός, μὴ αἰσχυνέσθω, δοξαζέτω δὲ τὸν θεὸν ἐν τῷ μέρει [-{NA-]{+{NA27+} μέρει > ὀνόματι } τούτῳ.`
  - Apparatus (Beta code): `EI) DE\ W(S *XRISTIANO/S, MH\ AI)SXUNE/SQW, DOCAZE/TW DE\ TO\N QEO\N E)N TW=| ME/REI [-{N-]{+{S+} ME/REI > O)NO/MATI } TOU/TW|.`
- `1PE 5:1` · `apparatus-code`
  - Apparatus code: `N` -> `S` (the reading is unchanged)
  - Apparatus (Unicode): `Πρεσβυτέρους τοὺς [-{NA-]{+{NA27+} τοὺς > οὖν } ἐν ὑμῖν παρακαλῶ ὁ συμπρεσβύτερος καὶ μάρτυς τῶν τοῦ χριστοῦ παθημάτων, ὁ καὶ τῆς μελλούσης ἀποκαλύπτεσθαι δόξης κοινωνός·`
  - Apparatus (Beta code): `*PRESBUTE/ROUS TOU\S [-{N-]{+{S+} TOU\S > OU)=N } E)N U(MI=N PARAKALW= O( SUMPRESBU/TEROS KAI\ MA/RTUS TW=N TOU= XRISTOU= PAQHMA/TWN, O( KAI\ TH=S MELLOU/SHS A)POKALU/PTESQAI DO/CHS KOINWNO/S:`
- `1PE 5:9` · `apparatus-code`
  - Apparatus code: `N` -> `S` (the reading is unchanged)
  - Apparatus (Unicode): `ᾧ ἀντίστητε στερεοὶ τῇ πίστει, εἰδότες τὰ αὐτὰ τῶν παθημάτων τῇ ἐν κόσμῳ [-{NA-]{+{NA27+} κόσμῳ > [τῷ] κόσμῳ } ὑμῶν ἀδελφότητι ἐπιτελεῖσθαι.`
  - Apparatus (Beta code): `W(=| A)NTI/STHTE STEREOI\ TH=| PI/STEI, EI)DO/TES TA\ AU)TA\ TW=N PAQHMA/TWN TH=| E)N KO/SMW| [-{N-]{+{S+} KO/SMW| > [TW=|] KO/SMW| } U(MW=N A)DELFO/THTI E)PITELEI=SQAI.`
- `1PE 5:10` · `variant`
  - Apparatus (Unicode): `Ὁ δὲ θεὸς πάσης χάριτος, ὁ καλέσας ὑμᾶς εἰς τὴν αἰώνιον αὐτοῦ δόξαν ἐν χριστῷ Ἰησοῦ, [-{NA-]{+{NA27+} Ἰησοῦ > [Ἰησοῦ] {+} {NA28 Ἰησοῦ > -+} } ὀλίγον παθόντας αὐτὸς καταρτίσαι {NA καταρτίσαι ὑμᾶς > καταρτίσει } ὑμᾶς, στηρίξει, σθενώσει, θεμελιώσει.`
  - Apparatus (Beta code): `*(O DE\ QEO\S PA/SHS XA/RITOS, O( KALE/SAS U(MA=S EI)S TH\N AI)W/NION AU)TOU= DO/CAN E)N XRISTW=| *)IHSOU=, [-{N-]{+{S+} *)IHSOU= > [*)IHSOU=] {+} {E *)IHSOU= > -+} } O)LI/GON PAQO/NTAS AU)TO\S KATARTI/SAI {N KATARTI/SAI U(MA=S > KATARTI/SEI } U(MA=S, STHRI/CEI, SQENW/SEI, QEMELIW/SEI.`
- `2PE 1:12` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `? *DIO\ OU)K {N OU)K A)MELH/SW > MELLH/SW } A)MELH/SW A)EI\ U(MA=S [-U(POMIMNH|/SKEIN-]{+U(POMIMNH/S|KEIN+} PERI\ TOU/TWN, KAI/PER EI)DO/TAS, KAI\ E)STHRIGME/NOUS E)N TH=| PAROU/SH| A)LHQEI/A|.`
- `2PE 2:6` · `apparatus-code`
  - Apparatus code: `N` -> `S` (the reading is unchanged)
  - Apparatus (Unicode): `καὶ πόλεις Σοδόμων καὶ Γομόρρας τεφρώσας καταστροφῇ [-{NA-]{+{NA27+} καταστροφῇ > [καταστροφῇ] } κατέκρινεν, ὑπόδειγμα μελλόντων ἀσεβεῖν [-{NA-]{+{NA27+} ἀσεβεῖν > ἀσεβέ[ς]ιν } τεθεικώς·`
  - Apparatus (Beta code): `KAI\ PO/LEIS *SODO/MWN KAI\ *GOMO/RRAS TEFRW/SAS KATASTROFH=| [-{N-]{+{S+} KATASTROFH=| > [KATASTROFH=|] } KATE/KRINEN, U(PO/DEIGMA MELLO/NTWN A)SEBEI=N [-{N-]{+{S+} A)SEBEI=N > A)SEBE/[S]IN } TEQEIKW/S:`
- `2PE 2:11` · `apparatus-code`
  - Apparatus code: `N` -> `S` (the reading is unchanged)
  - Apparatus (Unicode): `ὅπου ἄγγελοι, ἰσχύϊ καὶ δυνάμει μείζονες ὄντες, οὐ φέρουσιν κατ' αὐτῶν παρὰ κυρίῳ [-{NA-]{+{NA27+} κυρίῳ > κυρίου } βλάσφημον κρίσιν.`
  - Apparatus (Beta code): `O(/POU A)/GGELOI, I)SXU/I+ KAI\ DUNA/MEI MEI/ZONES O)/NTES, OU) FE/ROUSIN KAT' AU)TW=N PARA\ KURI/W| [-{N-]{+{S+} KURI/W| > KURI/OU } BLA/SFHMON KRI/SIN.`
- `2PE 2:15` · `apparatus-code`
  - Apparatus code: `N` -> `S` (the reading is unchanged)
  - Apparatus (Unicode): `καταλιπόντες [-{NA-]{+{NA27+} καταλιπόντες > καταλείποντες } εὐθεῖαν ὁδὸν ἐπλανήθησαν, ἐξακολουθήσαντες τῇ ὁδῷ τοῦ Βαλαὰμ τοῦ Βοσόρ, ὃς μισθὸν ἀδικίας ἠγάπησεν,`
  - Apparatus (Beta code): `KATALIPO/NTES [-{N-]{+{S+} KATALIPO/NTES > KATALEI/PONTES } EU)QEI=AN O(DO\N E)PLANH/QHSAN, E)CAKOLOUQH/SANTES TH=| O(DW=| TOU= *BALAA\M TOU= *BOSO/R, O(\S MISQO\N A)DIKI/AS H)GA/PHSEN,`
- `2PE 2:18` · `variant`
  - Apparatus (Unicode): `Ὑπέρογκα γὰρ ματαιότητος φθεγγόμενοι, δελεάζουσιν ἐν ἐπιθυμίαις σαρκός, ἀσελγείαις, τοὺς ὄντως [-{NA-]{+{NA27+} ὄντως {+> ὀλίγως } ἀποφυγόντας {NA+} ἀποφυγόντας > [-ὀλίγως-] ἀποφεύγοντας } [-ἀποφυγόντας-] τοὺς ἐν πλάνῃ ἀναστρεφομένους,`
  - Apparatus (Beta code): `*(UPE/ROGKA GA\R MATAIO/THTOS FQEGGO/MENOI, DELEA/ZOUSIN E)N E)PIQUMI/AIS SARKO/S, A)SELGEI/AIS, TOU\S O)/NTWS [-{N-]{+{S+} O)/NTWS {+> O)LI/GWS } A)POFUGO/NTAS {N+} A)POFUGO/NTAS > [-O)LI/GWS-] A)POFEU/GONTAS } [-A)POFUGO/NTAS-] TOU\S E)N PLA/NH| A)NASTREFOME/NOUS,`
- `2PE 2:20` · `apparatus-code`
  - Apparatus code: `N` -> `S` (the reading is unchanged)
  - Apparatus (Unicode): `Εἰ γὰρ ἀποφυγόντες τὰ μιάσματα τοῦ κόσμου ἐν ἐπιγνώσει τοῦ κυρίου [-{NA-]{+{NA27+} κυρίου > κυρίου [ἡμῶν] } καὶ σωτῆρος Ἰησοῦ χριστοῦ, τούτοις δὲ πάλιν ἐμπλακέντες ἡττῶνται, γέγονεν αὐτοῖς τὰ ἔσχατα χείρονα τῶν πρώτων.`
  - Apparatus (Beta code): `*EI) GA\R A)POFUGO/NTES TA\ MIA/SMATA TOU= KO/SMOU E)N E)PIGNW/SEI TOU= KURI/OU [-{N-]{+{S+} KURI/OU > KURI/OU [H(MW=N] } KAI\ SWTH=ROS *)IHSOU= XRISTOU=, TOU/TOIS DE\ PA/LIN E)MPLAKE/NTES H(TTW=NTAI, GE/GONEN AU)TOI=S TA\ E)/SXATA XEI/RONA TW=N PRW/TWN.`
- `2PE 3:6` · `variant`
  - Apparatus (Unicode): `δι' ὧν {+{NA28 ὧν > ὃν }+} ὁ τότε κόσμος ὕδατι κατακλυσθεὶς ἀπώλετο·`
  - Apparatus (Beta code): `DI' W(=N {+{E W(=N > O(\N }+} O( TO/TE KO/SMOS U(/DATI KATAKLUSQEI\S A)PW/LETO:`
- `2PE 3:10` · `variant`
  - Apparatus (Unicode): `Ἥξει δὲ ἡ {NA ἡ ἡμέρα > ἡμέρα } ἡμέρα κυρίου ὡς κλέπτης ἐν {NA ἐν νυκτί > - } νυκτί, ἐν ᾗ οἱ οὐρανοὶ ῥοιζηδὸν παρελεύσονται, στοιχεῖα δὲ καυσούμενα λυθήσονται, {NA λυθήσονται > λυθήσεται } καὶ γῆ καὶ τὰ ἐν αὐτῇ ἔργα κατακαήσεται. [-{NA-]{+{NA27+} κατακαήσεται > εὑρεθήσεται } {+{NA28 κατακαήσεται > οὐχ εὑρεθήσεται ʽξςʼ }+}`
  - Apparatus (Beta code): `*(/HCEI DE\ H( {N H( H(ME/RA > H(ME/RA } H(ME/RA KURI/OU W(S KLE/PTHS E)N {N E)N NUKTI/ > - } NUKTI/, E)N H(=| OI( OU)RANOI\ R(OIZHDO\N PARELEU/SONTAI, STOIXEI=A DE\ KAUSOU/MENA LUQH/SONTAI, {N LUQH/SONTAI > LUQH/SETAI } KAI\ GH= KAI\ TA\ E)N AU)TH=| E)/RGA KATAKAH/SETAI. [-{N-]{+{S+} KATAKAH/SETAI > EU(REQH/SETAI } {+{E KATAKAH/SETAI > OU)X EU(REQH/SETAI (cj) }+}`
- `2PE 3:16` · `variant`
  - Apparatus (Unicode): `ὡς καὶ ἐν πάσαις ταῖς [-{NA-]{+{NA27+} ταῖς > - } ἐπιστολαῖς, λαλῶν ἐν αὐταῖς περὶ τούτων· ἐν οἷς {NA οἷς > αἷς } ἔστιν δυσνόητά τινα, ἃ οἱ ἀμαθεῖς καὶ ἀστήρικτοι στρεβλοῦσιν, {+{NA28 στρεβλοῦσιν > στρεβλώσουσιν }+} ὡς καὶ τὰς λοιπὰς γραφάς, πρὸς τὴν ἰδίαν αὐτῶν ἀπώλειαν.`
  - Apparatus (Beta code): `W(S KAI\ E)N PA/SAIS TAI=S [-{N-]{+{S+} TAI=S > - } E)PISTOLAI=S, LALW=N E)N AU)TAI=S PERI\ TOU/TWN: E)N OI(=S {N OI(=S > AI(=S } E)/STIN DUSNO/HTA/ TINA, A(\ OI( A)MAQEI=S KAI\ A)STH/RIKTOI STREBLOU=SIN, {+{E STREBLOU=SIN > STREBLW/SOUSIN }+} W(S KAI\ TA\S LOIPA\S GRAFA/S, PRO\S TH\N I)DI/AN AU)TW=N A)PW/LEIAN.`
- `2PE 3:18` · `variant`
  - Apparatus (Unicode): `Αὐξάνετε δὲ ἐν χάριτι καὶ γνώσει τοῦ κυρίου ἡμῶν καὶ σωτῆρος Ἰησοῦ χριστοῦ. Αὐτῷ ἡ δόξα καὶ νῦν καὶ εἰς ἡμέραν αἰῶνος. Ἀμήν. [-{NA-]{+{NA27+} Ἀμήν > [Ἀμήν] } {+{NA28 Ἀμήν > - }+}`
  - Apparatus (Beta code): `*AU)CA/NETE DE\ E)N XA/RITI KAI\ GNW/SEI TOU= KURI/OU H(MW=N KAI\ SWTH=ROS *)IHSOU= XRISTOU=. *AU)TW=| H( DO/CA KAI\ NU=N KAI\ EI)S H(ME/RAN AI)W=NOS. *)AMH/N. [-{N-]{+{S+} *)AMH/N > [*)AMH/N] } {+{E *)AMH/N > - }+}`
- `1JO 1:7` · `variant`
  - Apparatus (Unicode): `ἐὰν δὲ {+{NA28 δὲ > - }+} ἐν τῷ φωτὶ περιπατῶμεν, ὡς αὐτός ἐστιν ἐν τῷ φωτί, κοινωνίαν ἔχομεν μετ' ἀλλήλων, καὶ τὸ αἷμα Ἰησοῦ χριστοῦ {NA χριστοῦ > - } τοῦ υἱοῦ αὐτοῦ καθαρίζει ἡμᾶς ἀπὸ πάσης ἁμαρτίας.`
  - Apparatus (Beta code): `E)A\N DE\ {+{E DE\ > - }+} E)N TW=| FWTI\ PERIPATW=MEN, W(S AU)TO/S E)STIN E)N TW=| FWTI/, KOINWNI/AN E)/XOMEN MET' A)LLH/LWN, KAI\ TO\ AI(=MA *)IHSOU= XRISTOU= {N XRISTOU= > - } TOU= UI(OU= AU)TOU= KAQARI/ZEI H(MA=S A)PO\ PA/SHS A(MARTI/AS.`
- `1JO 3:7` · `variant`
  - Apparatus (Unicode): `Τεκνία, {+{NA28 Τεκνία > Παιδία }+} μηδεὶς πλανάτω ὑμᾶς· ὁ ποιῶν τὴν δικαιοσύνην δίκαιός ἐστιν, καθὼς ἐκεῖνος δίκαιός ἐστιν·`
  - Apparatus (Beta code): `*TEKNI/A, {+{E *TEKNI/A > *PAIDI/A }+} MHDEI\S PLANA/TW U(MA=S: O( POIW=N TH\N DIKAIOSU/NHN DI/KAIO/S E)STIN, KAQW\S E)KEI=NOS DI/KAIO/S E)STIN:`
- `1JO 5:10` · `apparatus-code`
  - Apparatus code: `N` -> `S` (the reading is unchanged)
  - Apparatus (Unicode): `Ὁ πιστεύων εἰς τὸν υἱὸν τοῦ θεοῦ ἔχει τὴν μαρτυρίαν ἐν αὐτῷ· [-{NA-]{+{NA27+} αὐτῷ > ἑαυτῷ } ὁ μὴ πιστεύων τῷ θεῷ ψεύστην πεποίηκεν αὐτόν, ὅτι οὐ πεπίστευκεν εἰς τὴν μαρτυρίαν, ἣν μεμαρτύρηκεν ὁ θεὸς περὶ τοῦ υἱοῦ αὐτοῦ.`
  - Apparatus (Beta code): `*(O PISTEU/WN EI)S TO\N UI(O\N TOU= QEOU= E)/XEI TH\N MARTURI/AN E)N AU)TW=|: [-{N-]{+{S+} AU)TW=| > E(AUTW=| } O( MH\ PISTEU/WN TW=| QEW=| YEU/STHN PEPOI/HKEN AU)TO/N, O(/TI OU) PEPI/STEUKEN EI)S TH\N MARTURI/AN, H(\N MEMARTU/RHKEN O( QEO\S PERI\ TOU= UI(OU= AU)TOU=.`
- `1JO 5:18` · `apparatus-code`
  - Apparatus code: `N` -> `S` (the reading is unchanged)
  - Apparatus (Unicode): `Οἴδαμεν ὅτι πᾶς ὁ γεγεννημένος ἐκ τοῦ θεοῦ οὐχ ἁμαρτάνει· ἀλλ' ὁ γεννηθεὶς ἐκ τοῦ θεοῦ τηρεῖ ἑαυτόν, [-{NA-]{+{NA27+} ἑαυτόν > αὐτόν } καὶ ὁ πονηρὸς οὐχ ἅπτεται αὐτοῦ.`
  - Apparatus (Beta code): `? *OI)/DAMEN O(/TI PA=S O( GEGENNHME/NOS E)K TOU= QEOU= OU)X A(MARTA/NEI: A)LL' O( GENNHQEI\S E)K TOU= QEOU= THREI= E(AUTO/N, [-{N-]{+{S+} E(AUTO/N > AU)TO/N } KAI\ O( PONHRO\S OU)X A(/PTETAI AU)TOU=.`
- `2JO 1:5` · `apparatus-code`
  - Apparatus code: `N` -> `S` (the reading is unchanged)
  - Apparatus (Unicode): `Καὶ νῦν ἐρωτῶ σε, κυρία, οὐχ ὡς ἐντολὴν γράφων [-{NA-]{+{NA27+} γράφων σοι καινήν > καινὴν γράφων σοι } σοι καινήν, ἀλλὰ ἣν εἴχομεν ἀπ' ἀρχῆς, ἵνα ἀγαπῶμεν ἀλλήλους.`
  - Apparatus (Beta code): `*KAI\ NU=N E)RWTW= SE, KURI/A, OU)X W(S E)NTOLH\N GRA/FWN [-{N-]{+{S+} GRA/FWN SOI KAINH/N > KAINH\N GRA/FWN SOI } SOI KAINH/N, A)LLA\ H(\N EI)/XOMEN A)P' A)RXH=S, I(/NA A)GAPW=MEN A)LLH/LOUS.`
- `2JO 1:12` · `apparatus-code`
  - Apparatus code: `N` -> `S` (the reading is unchanged)
  - Apparatus (Unicode): `Πολλὰ ἔχων ὑμῖν γράφειν, οὐκ ἐβουλήθην διὰ χάρτου καὶ μέλανος· ἀλλὰ ἐλπίζω ἐλθεῖν {NA ἐλθεῖν > γενέσθαι } πρὸς ὑμᾶς, καὶ στόμα πρὸς στόμα λαλῆσαι, ἵνα ἡ χαρὰ ἡμῶν ᾖ [-{NA-]{+{NA27+} ᾖ πεπληρωμένη > πεπληρωμένη ᾖ } πεπληρωμένη.`
  - Apparatus (Beta code): `? *POLLA\ E)/XWN U(MI=N GRA/FEIN, OU)K E)BOULH/QHN DIA\ XA/RTOU KAI\ ME/LANOS: A)LLA\ E)LPI/ZW E)LQEI=N {N E)LQEI=N > GENE/SQAI } PRO\S U(MA=S, KAI\ STO/MA PRO\S STO/MA LALH=SAI, I(/NA H( XARA\ H(MW=N H)=| [-{N-]{+{S+} H)=| PEPLHRWME/NH > PEPLHRWME/NH H)=| } PEPLHRWME/NH.`
- `3JO 1:4` · `apparatus-code`
  - Apparatus code: `N` -> `S` (the reading is unchanged)
  - Apparatus (Unicode): `Μειζοτέραν τούτων οὐκ ἔχω χαράν, ἵνα ἀκούω τὰ ἐμὰ τέκνα ἐν ἀληθείᾳ [-{NA-]{+{NA27+} ἀληθείᾳ > τῇ ἀληθείᾳ } περιπατοῦντα.`
  - Apparatus (Beta code): `*MEIZOTE/RAN TOU/TWN OU)K E)/XW XARA/N, I(/NA A)KOU/W TA\ E)MA\ TE/KNA E)N A)LHQEI/A| [-{N-]{+{S+} A)LHQEI/A| > TH=| A)LHQEI/A| } PERIPATOU=NTA.`
- `JUD 1:5` · `variant`
  - Apparatus (Unicode): `Ὑπομνῆσαι δὲ ὑμᾶς βούλομαι, εἰδότας ὑμᾶς [-{NA-]{+{NA27+} ὑμᾶς ἅπαξ τοῦτο ὅτι ὁ κύριος > [ὑμᾶς] πάντα ὅτι [ὁ] κύριος ἅπαξ {+} {NA28 ὑμᾶς ἅπαξ τοῦτο ὅτι ὁ κύριος > ὑμᾶς ἅπαξ πάντα ὅτι Ἰησοῦς+} } ἅπαξ τοῦτο, ὅτι ὁ κύριος, λαὸν ἐκ γῆς Αἰγύπτου σώσας, τὸ δεύτερον τοὺς μὴ πιστεύσαντας ἀπώλεσεν.`
  - Apparatus (Beta code): `? *(UPOMNH=SAI DE\ U(MA=S BOU/LOMAI, EI)DO/TAS U(MA=S [-{N-]{+{S+} U(MA=S A(/PAC TOU=TO O(/TI O( KU/RIOS > [U(MA=S] PA/NTA O(/TI [O(] KU/RIOS A(/PAC {+} {E U(MA=S A(/PAC TOU=TO O(/TI O( KU/RIOS > U(MA=S A(/PAC PA/NTA O(/TI *)IHSOU=S+} } A(/PAC TOU=TO, O(/TI O( KU/RIOS, LAO\N E)K GH=S *AI)GU/PTOU SW/SAS, TO\ DEU/TERON TOU\S MH\ PISTEU/SANTAS A)PW/LESEN.`
- `JUD 1:18` · `variant`
  - Apparatus (Unicode): `ὅτι ἔλεγον ὑμῖν ὅτι [-{NA-]{+{NA27+} ὅτι ἐν ἐσχάτῳ χρόνῳ > [ὅτι] ἐπ' ἐσχάτου [τοῦ] {+χρόνου } {NA28 ὅτι ἐν ἐσχάτῳ χρόνῳ > ἐπ' ἐσχάτου+} χρόνου } ἐν ἐσχάτῳ χρόνῳ ἔσονται ἐμπαῖκται, κατὰ τὰς ἑαυτῶν ἐπιθυμίας πορευόμενοι τῶν ἀσεβειῶν.`
  - Apparatus (Beta code): `O(/TI E)/LEGON U(MI=N O(/TI [-{N-]{+{S+} O(/TI E)N E)SXA/TW| XRO/NW| > [O(/TI] E)P' E)SXA/TOU [TOU=] {+XRO/NOU } {E O(/TI E)N E)SXA/TW| XRO/NW| > E)P' E)SXA/TOU+} XRO/NOU } E)N E)SXA/TW| XRO/NW| E)/SONTAI E)MPAI=KTAI, KATA\ TA\S E(AUTW=N E)PIQUMI/AS POREUO/MENOI TW=N A)SEBEIW=N.`
- `REV 1:18` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `KAI\ O( ZW=N, KAI\ E)GENO/MHN NEKRO/S, KAI\ I)DOU/, ZW=N EI)MI\ EI)S TOU\S AI)W=NAS TW=N AI)W/NWN, A)MH/N: {N A)MH/N > - } KAI\ E)/XW TA\S KLEI=S {B KLEI=S > KLEI=DAS } TOU= QANA/TOU KAI\ TOU= [-*(/A|DOU.-]{+*(/AD|OU.+}`
- `REV 3:2` · `variant`
  - Apparatus (Unicode): `Γίνου γρηγορῶν, καὶ στήρισον {Byz στήρισον > στήριξον = τήρησον } τὰ λοιπὰ ἃ ἔμελλες {Byz ἔμελλες {+ἀποβάλλειν+} > [-ἔμελλον-]{+ἠμελλες ἀποβάλλειν+} = [-ἤμελλες-]{+ἐμέλλον ἀποθάνειν+} } {NA ἔμελλες ἀποβάλλειν > ἔμελλον ἀποθανεῖν } ἀποβάλλειν· οὐ γὰρ εὕρηκά σου τὰ ἔργα πεπληρωμένα ἐνώπιον τοῦ θεοῦ μου.`
  - Apparatus (Beta code): `*GI/NOU GRHGORW=N, KAI\ STH/RISON {B STH/RISON > STH/RICON = TH/RHSON } TA\ LOIPA\ A(\ E)/MELLES {B E)/MELLES {+A)POBA/LLEIN+} > [-E)/MELLON-]{+H)MELLES A)POBA/LLEIN+} = [-H)/MELLES-]{+E)ME/LLON A)POQA/NEIN+} } {N E)/MELLES A)POBA/LLEIN > E)/MELLON A)POQANEI=N } A)POBA/LLEIN: OU) GA\R EU(/RHKA/ SOU TA\ E)/RGA PEPLHRWME/NA E)NW/PION TOU= QEOU= MOU.`
- `REV 3:7` · `variant`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `? *KAI\ TW=| A)GGE/LW| TH=S E)N *FILADELFEI/A| E)KKLHSI/AS GRA/YON, ? *TA/DE LE/GEI O( A(/GIOS, O( A)LHQINO/S, O( E)/XWN TH\N KLEI=N TOU= {N TOU= > - } *DAUI/D, {B *DAUI/D > [-*_DAD-]{+_*D*A*D+} } O( A)NOI/GWN KAI\ OU)DEI\S KLEI/SEI AU)TH/N, {B AU)TH/N EI) MH\ O( A)NOI/GWN > KAI\ KLEI/WN } {N AU)TH/N EI) MH\ O( A)NOI/GWN > KAI\ KLEI/WN } EI) MH\ O( A)NOI/GWN: KAI\ OU)DEI\S A)NOI/CEI. {N A)NOI/CEI > A)NOI/GEI }`
- `REV 4:4` · `variant`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*KAI\ KUKLO/QEN TOU= QRO/NOU QRO/NOI {N QRO/NOI > QRO/NOUS } EI)/KOSI {B EI)/KOSI TE/SSARES > [-*_KD-]{+_*K*D+} } TE/SSARES: KAI\ E)PI\ TOU\S QRO/NOUS {N QRO/NOUS TOU\S > QRO/NOUS } TOU\S EI)/KOSI {B EI)/KOSI TE/SSARAS > [-*_KD-]{+_*K*D+} } TE/SSARAS PRESBUTE/ROUS KAQHME/NOUS, PERIBEBLHME/NOUS E)N I(MATI/OIS LEUKOI=S, KAI\ E)PI\ TA\S KEFALA\S AU)TW=N STEFA/NOUS XRUSOU=S.`
- `REV 4:10` · `variant`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `PESOU=NTAI OI( EI)/KOSI {B EI)/KOSI TE/SSARES > [-*_KD-]{+_*K*D+} } TE/SSARES PRESBU/TEROI E)NW/PION TOU= KAQHME/NOU E)PI\ TOU= QRO/NOU, KAI\ PROSKUNH/SOUSIN TW=| ZW=NTI EI)S TOU\S AI)W=NAS TW=N AI)W/NWN, KAI\ BALOU=SIN TOU\S STEFA/NOUS AU)TW=N E)NW/PION TOU= QRO/NOU, LE/GONTES,`
- `REV 5:5` · `variant`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*KAI\ EI(=S E)K TW=N PRESBUTE/RWN LE/GEI MOI, *MH\ KLAI=E: I)DOU/, E)NI/KHSEN O( LE/WN O( E)K TH=S FULH=S *)IOU/DA, H( R(I/ZA *DAUI/D, {B *DAUI/D > [-*_DAD-]{+_*D*A*D+} } O( A)NOI/GWN {B O( A)NOI/GWN > A)NOI=CAI } {N O( A)NOI/GWN > A)NOI=CAI } TO\ BIBLI/ON KAI\ TA\S E(PTA\ SFRAGI=DAS AU)TOU=.`
- `REV 5:8` · `variant`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*KAI\ O(/TE E)/LABEN TO\ BIBLI/ON, TA\ TE/SSARA ZW=A| KAI\ OI( EI)/KOSI {B EI)/KOSI TE/SSARES > [-*_KD-]{+_*K*D+} } TE/SSARES PRESBU/TEROI E)/PESON {N E)/PESON > E)/PESAN } E)NW/PION TOU= A)RNI/OU, E)/XONTES E(/KASTOS KIQA/RAN, {B KIQA/RAN > KIQA/RAS } KAI\ FIA/LAS XRUSA=S GEMOU/SAS QUMIAMA/TWN, AI(/ EI)SIN PROSEUXAI\ {B PROSEUXAI\ > AI( PROSEUXAI\ } {N PROSEUXAI\ > AI( PROSEUXAI\ } TW=N A(GI/WN.`
- `REV 5:10` · `variant`
  - Apparatus (Unicode): `καὶ ἐποίησας αὐτοὺς τῷ θεῷ ἡμῶν βασιλεῖς {NA βασιλεῖς > βασιλείαν } καὶ ἱερεῖς, καὶ βασιλεύσουσιν {+{Byz βασιλεύσουσιν > βασιλεύουσιν }+} ἐπὶ τῆς γῆς.`
  - Apparatus (Beta code): `KAI\ E)POI/HSAS AU)TOU\S TW=| QEW=| H(MW=N BASILEI=S {N BASILEI=S > BASILEI/AN } KAI\ I(EREI=S, KAI\ BASILEU/SOUSIN {+{B BASILEU/SOUSIN > BASILEU/OUSIN }+} E)PI\ TH=S GH=S.`
- `REV 6:8` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*KAI\ I)DOU/, {B I)DOU/ > EI)=DON KAI\ I)DOU/ } {N I)DOU/ > EI)=DON KAI\ I)DOU/ } I(/PPOS XLWRO/S, KAI\ O( KAQH/MENOS E)PA/NW AU)TOU=, O)/NOMA AU)TW=| O( {N O( *QA/NATOS > [O(] *QA/NATOS } *QA/NATOS, KAI\ O( [-*(/A|DHS-]{+*(/AD|HS+} H)KOLOU/QEI {B H)KOLOU/QEI AU)TW=| > H)KOLOU/QEI MET' AU)TOU= } {N H)KOLOU/QEI AU)TW=| > H)KOLOU/QEI MET' AU)TOU= } AU)TW=|. *KAI\ E)DO/QH {N E)DO/QH AU)TW=| > E)DO/QH AU)TOI=S } AU)TW=| E)COUSI/A E)PI\ TO\ TE/TARTON TH=S GH=S A)POKTEI=NAI E)N R(OMFAI/A| KAI\ E)N LIMW=| KAI\ E)N QANA/TW|, KAI\ U(PO\ TW=N QHRI/WN TH=S GH=S.`
- `REV 6:9` · `variant`
  - Apparatus (Unicode): `Καὶ ὅτε ἤνοιξεν τὴν πέμπτην σφραγῖδα, εἶδον ὑποκάτω τοῦ θυσιαστηρίου τὰς ψυχὰς {+{Byz ψυχὰς > ψυχὰς τῶν ἀνθρώπων }+} τῶν ἐσφαγμένων διὰ τὸν λόγον τοῦ θεοῦ, καὶ διὰ τὴν μαρτυρίαν τοῦ {NA τοῦ ἀρνίου > - } ἀρνίου ἣν εἶχον,`
  - Apparatus (Beta code): `? *KAI\ O(/TE H)/NOICEN TH\N PE/MPTHN SFRAGI=DA, EI)=DON U(POKA/TW TOU= QUSIASTHRI/OU TA\S YUXA\S {+{B YUXA\S > YUXA\S TW=N A)NQRW/PWN }+} TW=N E)SFAGME/NWN DIA\ TO\N LO/GON TOU= QEOU=, KAI\ DIA\ TH\N MARTURI/AN TOU= {N TOU= A)RNI/OU > - } A)RNI/OU H(\N EI)=XON,`
- `REV 6:10` · `variant`
  - Apparatus (Unicode): `καὶ ἔκραξαν {+{Byz ἔκραξαν > ἔκραζον }+} φωνῇ {Byz φωνῇ μεγάλῃ > φωνὴν μεγάλην } μεγάλῃ, λέγοντες, Ἕως πότε, ὁ δεσπότης, ὁ ἅγιος καὶ ἀληθινός, οὐ κρίνεις καὶ ἐκδικεῖς τὸ αἷμα ἡμῶν ἐκ τῶν κατοικούντων ἐπὶ τῆς γῆς;`
  - Apparatus (Beta code): `KAI\ E)/KRACAN {+{B E)/KRACAN > E)/KRAZON }+} FWNH=| {B FWNH=| MEGA/LH| > FWNH\N MEGA/LHN } MEGA/LH|, LE/GONTES, *(/EWS PO/TE, O( DESPO/THS, O( A(/GIOS KAI\ A)LHQINO/S, OU) KRI/NEIS KAI\ E)KDIKEI=S TO\ AI(=MA H(MW=N E)K TW=N KATOIKOU/NTWN E)PI\ TH=S GH=S;`
- `REV 7:5` · `variant`
  - Apparatus (Unicode): `Ἐκ φυλῆς Ἰούδα, δώδεκα {Byz δώδεκα > —ΙΒ } χιλιάδες ἐσφραγισμέναι· {Byz ἐσφραγισμέναι > [-- =-] ἐσφραγισμένοι } {NA ἐσφραγισμέναι > ἐσφραγισμένοι } ἐκ φυλῆς Ῥουβίμ, {NA Ῥουβίμ > Ῥουβήν } δώδεκα {Byz δώδεκα > —ΙΒ } χιλιάδες· ἐκ φυλῆς Γάδ, δώδεκα {Byz δώδεκα > —ΙΒ } χιλιάδες·`
  - Apparatus (Beta code): `? *)EK FULH=S *)IOU/DA, DW/DEKA {B DW/DEKA > [-*_IB-]{+_*I*B+} } XILIA/DES E)SFRAGISME/NAI: {B E)SFRAGISME/NAI > [-- =-] E)SFRAGISME/NOI } {N E)SFRAGISME/NAI > E)SFRAGISME/NOI } ? E)K FULH=S *(ROUBI/M, {N *(ROUBI/M > *(ROUBH/N } DW/DEKA {B DW/DEKA > [-*_IB-]{+_*I*B+} } XILIA/DES: ? E)K FULH=S *GA/D, DW/DEKA {B DW/DEKA > [-*_IB-]{+_*I*B+} } XILIA/DES:`
- `REV 7:6` · `variant`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `? E)K FULH=S *)ASH/R, DW/DEKA {B DW/DEKA > [-*_IB-]{+_*I*B+} } XILIA/DES: ? E)K FULH=S *NEFQALEI/M, {N *NEFQALEI/M > *NEFQALI/M } DW/DEKA {B DW/DEKA > [-*_IB-]{+_*I*B+} } XILIA/DES: ? E)K FULH=S *MANASSH=, DW/DEKA {B DW/DEKA > [-*_IB-]{+_*I*B+} } XILIA/DES:`
- `REV 7:7` · `variant`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `? E)K FULH=S *SUMEW/N, DW/DEKA {B DW/DEKA > [-*_IB-]{+_*I*B+} } XILIA/DES: ? E)K FULH=S *LEUI+/, DW/DEKA {B DW/DEKA > [-*_IB-]{+_*I*B+} } XILIA/DES: ? E)K FULH=S *)ISAXA/R, {N *)ISAXA/R > *)ISSAXA/R } DW/DEKA {B DW/DEKA > [-*_IB-]{+_*I*B+} } XILIA/DES:`
- `REV 7:8` · `variant`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `? E)K FULH=S *ZABOULW/N, DW/DEKA {B DW/DEKA > [-*_IB-]{+_*I*B+} } XILIA/DES: ? E)K FULH=S *)IWSH/F, DW/DEKA {B DW/DEKA > [-*_IB-]{+_*I*B+} } XILIA/DES: ? E)K FULH=S *BENIAMI/N, DW/DEKA {B DW/DEKA > [-*_IB-]{+_*I*B+} } XILIA/DES E)SFRAGISME/NAI. {B E)SFRAGISME/NAI > E)SFRAGISME/NOI } {N E)SFRAGISME/NAI > E)SFRAGISME/NOI }`
- `REV 9:10` · `variant`
  - Apparatus (Unicode): `Καὶ ἔχουσιν οὐρὰς ὁμοίας σκορπίοις, καὶ κέντρα. Καὶ {Byz Καὶ ἐν > Ἐν } ἐν ταῖς οὐραῖς αὐτῶν ἐξουσίαν {Byz ἐξουσίαν ἔχουσιν τοῦ > {+καὶ+} ἡ ἐξουσία αὐτῶν } {NA ἐξουσίαν ἔχουσιν τοῦ > ἡ ἐξουσία αὐτῶν } ἔχουσιν τοῦ ἀδικῆσαι τοὺς ἀνθρώπους μῆνας πέντε.`
  - Apparatus (Beta code): `*KAI\ E)/XOUSIN OU)RA\S O(MOI/AS SKORPI/OIS, KAI\ KE/NTRA. *KAI\ {B *KAI\ E)N > *)EN } E)N TAI=S OU)RAI=S AU)TW=N E)COUSI/AN {B E)COUSI/AN E)/XOUSIN TOU= > {+KAI\+} H( E)COUSI/A AU)TW=N } {N E)COUSI/AN E)/XOUSIN TOU= > H( E)COUSI/A AU)TW=N } E)/XOUSIN TOU= A)DIKH=SAI TOU\S A)NQRW/POUS MH=NAS PE/NTE.`
- `REV 11:2` · `variant`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*KAI\ TH\N AU)LH\N TH\N E)/CWQEN TOU= NAOU= E)/KBALE E)/CW, {B E)/CW > E)/CWQEN } {N E)/CW > E)/CWQEN } KAI\ MH\ AU)TH\N METRH/SHS|, O(/TI E)DO/QH TOI=S E)/QNESIN: KAI\ TH\N PO/LIN TH\N A(GI/AN PATH/SOUSIN MH=NAS TESSARA/KONTA {B TESSARA/KONTA KAI\ DU/O > TESSARA/KONTA DU/O = [-*_MB-]{+_*M*B+} } {N TESSARA/KONTA KAI\ > TESSERA/KONTA [KAI\] } KAI\ DU/O.`
- `REV 11:16` · `variant`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*KAI\ OI( EI)/KOSI {B EI)/KOSI TE/SSARES > [-*_KD-]{+_*K*D+} } TE/SSARES PRESBU/TEROI OI( {N OI( E)NW/PION TOU= QRO/NOU > [OI(] E)NW/PION } E)NW/PION TOU= {B TOU= QRO/NOU > - } QRO/NOU TOU= QEOU= KAQH/MENOI {B KAQH/MENOI > OI(\ KA/QHNTAI } E)PI\ TOU\S QRO/NOUS AU)TW=N, E)/PESON {N E)/PESON > E)/PESAN } E)PI\ TA\ PRO/SWPA AU)TW=N, KAI\ PROSEKU/NHSAN TW=| QEW=|,`
- `REV 13:3` · `variant`
  - Apparatus (Unicode): `Καὶ μίαν ἐκ τῶν κεφαλῶν αὐτοῦ ὡσεὶ {+{Byz ὡσεὶ > ὡς }+} {NA ὡσεὶ > ὡς } ἐσφαγμένην εἰς θάνατον· καὶ ἡ πληγὴ τοῦ θανάτου αὐτοῦ ἐθεραπεύθη· καὶ ἐθαύμασεν {NA ἐθαύμασεν > ἐθαυμάσθη } ὅλη ἡ γῆ ὀπίσω τοῦ θηρίου·`
  - Apparatus (Beta code): `*KAI\ MI/AN E)K TW=N KEFALW=N AU)TOU= W(SEI\ {+{B W(SEI\ > W(S }+} {N W(SEI\ > W(S } E)SFAGME/NHN EI)S QA/NATON: KAI\ H( PLHGH\ TOU= QANA/TOU AU)TOU= E)QERAPEU/QH: KAI\ E)QAU/MASEN {N E)QAU/MASEN > E)QAUMA/SQH } O(/LH H( GH= O)PI/SW TOU= QHRI/OU:`
- `REV 13:18` · `variant`
  - Apparatus (Unicode): `Ὧδε ἡ σοφία ἐστίν. Ὁ ἔχων νοῦν ψηφισάτω τὸν ἀριθμὸν τοῦ θηρίου· ἀριθμὸς γὰρ ἀνθρώπου ἐστίν, καὶ {Byz καὶ > - } ὁ ἀριθμὸς αὐτοῦ {Byz αὐτοῦ ἐστὶν > αὐτοῦ } {NA αὐτοῦ ἐστὶν > αὐτοῦ } ἐστὶν ἑξακόσια {Byz ἑξακόσια ἑξήκοντα ἕξ > [-—ΧΞ$-]{+—ΧΞ*$+} } {NA ἑξακόσια > ἑξακόσιοι } ἑξήκοντα ἕξ.`
  - Apparatus (Beta code): `*(=WDE H( SOFI/A E)STI/N. *(O E)/XWN NOU=N YHFISA/TW TO\N A)RIQMO\N TOU= QHRI/OU: A)RIQMO\S GA\R A)NQRW/POU E)STI/N, KAI\ {B KAI\ > - } O( A)RIQMO\S AU)TOU= {B AU)TOU= E)STI\N > AU)TOU= } {N AU)TOU= E)STI\N > AU)TOU= } E)STI\N E(CAKO/SIA {B E(CAKO/SIA E(CH/KONTA E(/C > [-*_XC$-]{+_*X*C*$+} } {N E(CAKO/SIA > E(CAKO/SIOI } E(CH/KONTA E(/C.`
- `REV 14:1` · `variant`
  - Apparatus (Unicode): `Καὶ εἶδον, καὶ ἰδού, τὸ {Byz τὸ ἀρνίον > ἀρνίον } ἀρνίον ἑστηκὸς {+{Byz ἑστηκὸς > ἑστὼς }+} {NA ἑστηκὸς > ἑστὸς } ἐπὶ τὸ ὄρος Σιών, καὶ μετ' αὐτοῦ ἀριθμὸς {Byz ἀριθμὸς > - } {NA ἀριθμὸς > - } ἑκατὸν {Byz ἑκατὸν τεσσαράκοντα τέσσαρες > —ΡΜΔ } τεσσαράκοντα {NA τεσσαράκοντα > τεσσεράκοντα } τέσσαρες χιλιάδες, ἔχουσαι τὸ ὄνομα αὐτοῦ καὶ τὸ ὄνομα τοῦ πατρὸς αὐτοῦ γεγραμμένον ἐπὶ τῶν μετώπων αὐτῶν.`
  - Apparatus (Beta code): `*KAI\ EI)=DON, KAI\ I)DOU/, TO\ {B TO\ A)RNI/ON > A)RNI/ON } A)RNI/ON E(STHKO\S {+{B E(STHKO\S > E(STW\S }+} {N E(STHKO\S > E(STO\S } E)PI\ TO\ O)/ROS *SIW/N, KAI\ MET' AU)TOU= A)RIQMO\S {B A)RIQMO\S > - } {N A)RIQMO\S > - } E(KATO\N {B E(KATO\N TESSARA/KONTA TE/SSARES > [-*_RMD-]{+_*R*M*D+} } TESSARA/KONTA {N TESSARA/KONTA > TESSERA/KONTA } TE/SSARES XILIA/DES, E)/XOUSAI TO\ O)/NOMA AU)TOU= KAI\ TO\ O)/NOMA TOU= PATRO\S AU)TOU= GEGRAMME/NON E)PI\ TW=N METW/PWN AU)TW=N.`
- `REV 14:3` · `variant`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*KAI\ A)/D|OUSIN {N A)/D|OUSIN > A)/D|OUSIN [W(S] } W)D|H\N KAINH\N E)NW/PION TOU= QRO/NOU, KAI\ E)NW/PION TW=N TESSA/RWN ZW/W|N KAI\ TW=N PRESBUTE/RWN: KAI\ OU)DEI\S E)DU/NATO {B E)DU/NATO > H)DU/NATO } MAQEI=N TH\N W)D|H/N, EI) MH\ AI( E(KATO\N {B E(KATO\N TESSARA/KONTA TE/SSARES > [-*_RMD-]{+_*R*M*D+} } TESSARA/KONTA {N TESSARA/KONTA > TESSERA/KONTA } TE/SSARES XILIA/DES, OI( H)GORASME/NOI A)PO\ TH=S GH=S.`
- `REV 14:4` · `variant`
  - Apparatus (Unicode): `Οὗτοί εἰσιν οἳ μετὰ γυναικῶν οὐκ ἐμολύνθησαν· παρθένοι γάρ εἰσιν. Οὗτοί εἰσιν {NA εἰσιν οἱ ἀκολουθοῦντες > οἱ ἀκολουθοῦντες } οἱ ἀκολουθοῦντες τῷ ἀρνίῳ ὅπου ἂν {Byz ἂν > ἐὰν } ὑπάγῃ. Οὗτοι ὑπὸ {+{Byz ὑπὸ Ἰησοῦ > - }+} {NA ὑπὸ Ἰησοῦ > - } Ἰησοῦ ἠγοράσθησαν ἀπὸ τῶν ἀνθρώπων, ἀπαρχὴ τῷ θεῷ καὶ τῷ ἀρνίῳ.`
  - Apparatus (Beta code): `*OU(=TOI/ EI)SIN OI(\ META\ GUNAIKW=N OU)K E)MOLU/NQHSAN: PARQE/NOI GA/R EI)SIN. *OU(=TOI/ EI)SIN {N EI)SIN OI( A)KOLOUQOU=NTES > OI( A)KOLOUQOU=NTES } OI( A)KOLOUQOU=NTES TW=| A)RNI/W| O(/POU A)\N {B A)\N > E)A\N } U(PA/GH|. *OU(=TOI U(PO\ {+{B U(PO\ *)IHSOU= > - }+} {N U(PO\ *)IHSOU= > - } *)IHSOU= H)GORA/SQHSAN A)PO\ TW=N A)NQRW/PWN, A)PARXH\ TW=| QEW=| KAI\ TW=| A)RNI/W|.`
- `REV 14:6` · `variant`
  - Apparatus (Unicode): `Καὶ εἶδον ἄγγελον {+{Byz ἄγγελον > ἄλλον ἄγγελον }+} {NA ἄγγελον > ἄλλον ἄγγελον } πετόμενον ἐν μεσουρανήματι, ἔχοντα εὐαγγέλιον αἰώνιον, εὐαγγελίσαι τοὺς {NA τοὺς > ἐπὶ τοὺς } καθημένους ἐπὶ τῆς γῆς, καὶ ἐπὶ πᾶν ἔθνος καὶ φυλὴν καὶ γλῶσσαν καὶ λαόν,`
  - Apparatus (Beta code): `? *KAI\ EI)=DON A)/GGELON {+{B A)/GGELON > A)/LLON A)/GGELON }+} {N A)/GGELON > A)/LLON A)/GGELON } PETO/MENON E)N MESOURANH/MATI, E)/XONTA EU)AGGE/LION AI)W/NION, EU)AGGELI/SAI TOU\S {N TOU\S > E)PI\ TOU\S } KAQHME/NOUS E)PI\ TH=S GH=S, KAI\ E)PI\ PA=N E)/QNOS KAI\ FULH\N KAI\ GLW=SSAN KAI\ LAO/N,`
- `REV 14:19` · `variant`
  - Apparatus (Unicode): `Καὶ {Byz Καὶ ἔβαλεν > Καὶ ἐξέβαλεν } ἔβαλεν ὁ ἄγγελος τὸ δρέπανον αὐτοῦ εἰς τὴν γῆν, καὶ ἐτρύγησεν τὴν ἄμπελον τῆς γῆς, καὶ ἔβαλεν εἰς τὴν ληνὸν τοῦ θυμοῦ τοῦ θεοῦ τὸν μέγαν. {+{Byz τὸν μέγαν > τὴν μεγάλην }+}`
  - Apparatus (Beta code): `*KAI\ {B *KAI\ E)/BALEN > *KAI\ E)CE/BALEN } E)/BALEN O( A)/GGELOS TO\ DRE/PANON AU)TOU= EI)S TH\N GH=N, KAI\ E)TRU/GHSEN TH\N A)/MPELON TH=S GH=S, KAI\ E)/BALEN EI)S TH\N LHNO\N TOU= QUMOU= TOU= QEOU= TO\N ME/GAN. {+{B TO\N ME/GAN > TH\N MEGA/LHN }+}`
- `REV 14:20` · `variant`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*KAI\ E)PATH/QH H( LHNO\S E)/CWQEN TH=S PO/LEWS, KAI\ E)CH=LQEN AI(=MA E)K TH=S LHNOU= A)/XRI TW=N XALINW=N TW=N I(/PPWN, A)PO\ STADI/WN XILI/WN {B XILI/WN E(CAKOSI/WN > [-*_AX-]{+_*A*X+} } E(CAKOSI/WN.`
- `REV 18:3` · `variant`
  - Apparatus (Unicode): `Ὅτι ἐκ τοῦ οἴνου {Byz οἴνου τοῦ θυμοῦ > θυμοῦ τοῦ οἴνου } τοῦ θυμοῦ τῆς πορνείας αὐτῆς πεπτώκασιν {+{Byz πεπτώκασιν > πέπωκεν = πεπώκασιν }+} {NA πεπτώκασιν > πέπωκαν } πάντα τὰ ἔθνη, καὶ οἱ βασιλεῖς τῆς γῆς μετ' αὐτῆς ἐπόρνευσαν, καὶ οἱ ἔμποροι τῆς γῆς ἐκ τῆς δυνάμεως τοῦ στρήνους αὐτῆς ἐπλούτησαν.`
  - Apparatus (Beta code): `*(/OTI E)K TOU= OI)/NOU {B OI)/NOU TOU= QUMOU= > QUMOU= TOU= OI)/NOU } TOU= QUMOU= TH=S PORNEI/AS AU)TH=S PEPTW/KASIN {+{B PEPTW/KASIN > PE/PWKEN = PEPW/KASIN }+} {N PEPTW/KASIN > PE/PWKAN } PA/NTA TA\ E)/QNH, KAI\ OI( BASILEI=S TH=S GH=S MET' AU)TH=S E)PO/RNEUSAN, KAI\ OI( E)/MPOROI TH=S GH=S E)K TH=S DUNA/MEWS TOU= STRH/NOUS AU)TH=S E)PLOU/THSAN.`
- `REV 18:6` · `variant`
  - Apparatus (Unicode): `Ἀπόδοτε αὐτῇ ὡς καὶ αὐτὴ ἀπέδωκεν, {Byz ἀπέδωκεν > ἀπέδωκεν ὑμῖν } καὶ διπλώσατε αὐτῇ {+διπλᾶ {Byz αὐτῇ διπλᾶ > τὰ διπλᾶ }+} {NA αὐτῇ διπλᾶ > τὰ διπλᾶ } [-διπλᾶ-]{+κατὰ {Byz+} κατὰ {+> ὡς καὶ αὐτὴ καὶ κατὰ }+} τὰ ἔργα αὐτῆς· ἐν τῷ ποτηρίῳ {Byz ποτηρίῳ > ποτηρίῳ αὐτῆς } ᾧ ἐκέρασεν κεράσατε αὐτῇ διπλοῦν.`
  - Apparatus (Beta code): `*)APO/DOTE AU)TH=| W(S KAI\ AU)TH\ A)PE/DWKEN, {B A)PE/DWKEN > A)PE/DWKEN U(MI=N } KAI\ DIPLW/SATE AU)TH=| {+DIPLA= {B AU)TH=| DIPLA= > TA\ DIPLA= }+} {N AU)TH=| DIPLA= > TA\ DIPLA= } [-DIPLA=-]{+KATA\ {B+} KATA\ {+> W(S KAI\ AU)TH\ KAI\ KATA\ }+} TA\ E)/RGA AU)TH=S: E)N TW=| POTHRI/W| {B POTHRI/W| > POTHRI/W| AU)TH=S } W(=| E)KE/RASEN KERA/SATE AU)TH=| DIPLOU=N.`
- `REV 18:13` · `variant`
  - Apparatus (Unicode): `καὶ κινάμωμον, {NA κινάμωμον > κιννάμωμον } καὶ θυμιάματα, {NA θυμιάματα > ἄμωμον καὶ θυμιάματα } καὶ μύρον, καὶ λίβανον, καὶ οἶνον, {+{Byz καὶ οἶνον > - }+} καὶ ἔλαιον, καὶ σεμίδαλιν, καὶ σῖτον, καὶ πρόβατα, {Byz πρόβατα καὶ κτήνη > κτήνη καὶ πρόβατα } {NA πρόβατα καὶ κτήνη > κτήνη καὶ πρόβατα } καὶ κτήνη· καὶ ἵππων, καὶ ῥαιδῶν, {Byz ῥαιδῶν > ῥεδῶν } {NA ῥαιδῶν > ῥεδῶν } καὶ σωμάτων, καὶ ψυχὰς ἀνθρώπων.`
  - Apparatus (Beta code): `KAI\ KINA/MWMON, {N KINA/MWMON > KINNA/MWMON } KAI\ QUMIA/MATA, {N QUMIA/MATA > A)/MWMON KAI\ QUMIA/MATA } KAI\ MU/RON, KAI\ LI/BANON, KAI\ OI)=NON, {+{B KAI\ OI)=NON > - }+} KAI\ E)/LAION, KAI\ SEMI/DALIN, KAI\ SI=TON, KAI\ PRO/BATA, {B PRO/BATA KAI\ KTH/NH > KTH/NH KAI\ PRO/BATA } {N PRO/BATA KAI\ KTH/NH > KTH/NH KAI\ PRO/BATA } KAI\ KTH/NH: KAI\ I(/PPWN, KAI\ R(AIDW=N, {B R(AIDW=N > R(EDW=N } {N R(AIDW=N > R(EDW=N } KAI\ SWMA/TWN, KAI\ YUXA\S A)NQRW/PWN.`
- `REV 18:23` · `variant`
  - Apparatus (Unicode): `καὶ φῶς λύχνου οὐ μὴ φανῇ {+{NA φανῇ > φάνῃ }+} ἐν σοὶ ἔτι, καὶ φωνὴ νυμφίου καὶ νύμφης οὐ μὴ ἀκουσθῇ ἐν σοὶ ἔτι· ὅτι οἱ ἔμποροί σου ἦσαν οἱ μεγιστᾶνες τῆς γῆς· ὅτι ἐν τῇ φαρμακείᾳ σου ἐπλανήθησαν πάντα τὰ ἔθνη.`
  - Apparatus (Beta code): `KAI\ FW=S LU/XNOU OU) MH\ FANH=| {+{N FANH=| > FA/NH| }+} E)N SOI\ E)/TI, KAI\ FWNH\ NUMFI/OU KAI\ NU/MFHS OU) MH\ A)KOUSQH=| E)N SOI\ E)/TI: O(/TI OI( E)/MPOROI/ SOU H)=SAN OI( MEGISTA=NES TH=S GH=S: O(/TI E)N TH=| FARMAKEI/A| SOU E)PLANH/QHSAN PA/NTA TA\ E)/QNH.`
- `REV 19:4` · `variant`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*KAI\ E)/PESON {B E)/PESON > E)/PESAN } {N E)/PESON > E)/PESAN } OI( PRESBU/TEROI OI( EI)/KOSI {B EI)/KOSI TE/SSARES > [-*_KD-]{+_*K*D+} } TE/SSARES, KAI\ TA\ TE/SSARA ZW=A|, KAI\ PROSEKU/NHSAN TW=| QEW=| TW=| KAQHME/NW| E)PI\ TOU= {B TOU= QRO/NOU > TW=| QRO/NW| } {N TOU= QRO/NOU > TW=| QRO/NW| } QRO/NOU, LE/GONTES, *)AMH/N: *(ALLHLOU/I+A.`
- `REV 20:13` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*KAI\ E)/DWKEN H( QA/LASSA TOU\S NEKROU\S {B NEKROU\S TOU\S E)N AU)TH=| > E)N AU)TH=| NEKROU/S } TOU\S E)N AU)TH=|, KAI\ O( *QA/NATOS KAI\ O( [-*(/A|DHS-]{+*(/AD|HS+} E)/DWKAN TOU\S NEKROU\S {B NEKROU\S TOU\S E)N AU)TOI=S > E)N AU)TOI=S NEKROU/S } TOU\S E)N AU)TOI=S: KAI\ E)KRI/QHSAN E(/KASTOS KATA\ TA\ E)/RGA AU)TW=N.`
- `REV 20:14` · `accents-breathings`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*KAI\ O( *QA/NATOS KAI\ O( [-*(/A|DHS-]{+*(/AD|HS+} E)BLH/QHSAN EI)S TH\N LI/MNHN TOU= PURO/S: OU(=TOS O( QA/NATOS O( DEU/TERO/S E)STIN, H( LI/MNH TOU= PURO/S.`
- `REV 21:6` · `variant`
  - Apparatus (Unicode): `Καὶ εἶπέν μοι, Γέγονα {+{NA Γέγονα > Γέγοναν. Ἐγώ [εἰμι] } τὸ+} {Byz Γέγονα τὸ > Γέγονα ἐγὼ τὸ } [-{NA Γέγονα > Γέγοναν. Ἐγώ [εἰμι] } τὸ-] Ἄλφα καὶ τὸ Ὦ, ἡ ἀρχὴ καὶ τὸ τέλος. {+{Byz ἡ ἀρχὴ καὶ τὸ τέλος > ἀρχὴ καὶ τέλος = καὶ ἡ ἀρχὴ καὶ τὸ τέλος }+} Ἐγὼ τῷ διψῶντι δώσω {Byz δώσω > δώσω αὐτῷ } ἐκ τῆς πηγῆς τοῦ ὕδατος τῆς ζωῆς δωρεάν.`
  - Apparatus (Beta code): `*KAI\ EI)=PE/N MOI, *GE/GONA {+{N *GE/GONA > *GE/GONAN. *)EGW/ [EI)MI] } TO\+} {B *GE/GONA TO\ > *GE/GONA E)GW\ TO\ } [-{N *GE/GONA > *GE/GONAN. *)EGW/ [EI)MI] } TO\-] *)/ALFA KAI\ TO\ *)=W, H( A)RXH\ KAI\ TO\ TE/LOS. {+{B H( A)RXH\ KAI\ TO\ TE/LOS > A)RXH\ KAI\ TE/LOS = KAI\ H( A)RXH\ KAI\ TO\ TE/LOS }+} *)EGW\ TW=| DIYW=NTI DW/SW {B DW/SW > DW/SW AU)TW=| } E)K TH=S PHGH=S TOU= U(/DATOS TH=S ZWH=S DWREA/N.`
- `REV 21:17` · `variant`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `*KAI\ E)ME/TRHSEN {B E)ME/TRHSEN > - } TO\ TEI=XOS AU)TH=S E(KATO\N {B E(KATO\N TESSARA/KONTA TESSA/RWN > [-*_RMD-]{+_*R*M*D+} } TESSARA/KONTA {N TESSARA/KONTA > TESSERA/KONTA } TESSA/RWN PHXW=N, ME/TRON A)NQRW/POU, O(/ E)STIN A)GGE/LOU.`
- `REV 22:16` · `variant`
  - Apparatus (Unicode): no difference after conversion to Unicode (Beta-code encoding only)
  - Apparatus (Beta code): `? *)EGW\ *)IHSOU=S E)/PEMYA TO\N A)/GGELO/N MOU MARTURH=SAI U(MI=N TAU=TA E)PI\ TAI=S E)KKLHSI/AIS. *)EGW/ EI)MI H( R(I/ZA KAI\ TO\ GE/NOS *DAUI/D, {B *DAUI/D > [-*_DAD-]{+_*D*A*D+} } O( A)STH\R O( LAMPRO\S O( PRWI+NO/S.`

## Derived-only differences

The source-tier comparison canonicalises dash spacing (`-` ↔ ` - `), so raw
dash-spacing differences are invisible there but survive in the derived
text. All current derived-only cases are attached-vs-spaced dashes.

They are listed in full in `derived.diff`.

- `MAT`: 9:6, 24:15
- `MAR`: 2:10, 13:14
- `LUK`: 1:69, 1:70, 2:22, 2:23, 2:36, 2:37, 3:23, 5:24, 23:50, 23:51
- `JOH`: 1:14, 1:38, 1:41, 1:42, 2:9, 4:1, 4:2, 4:9, 4:25, 6:22, 6:23, 7:22, 7:50, 9:7, 10:35, 19:31, 20:16, 21:7, 21:8
- `ACT`: 1:17, 1:19, 4:36, 5:17, 10:36, 12:3, 13:8, 17:20
- `ROM`: 1:13, 3:5, 3:8, 4:16, 4:17, 4:19, 5:12, 7:1, 7:13, 9:10, 10:6, 10:7
- `1CO`: 7:11, 16:15
- `2CO`: 2:5, 5:6, 5:7, 6:1, 6:2, 6:13, 9:4, 10:3, 10:4, 10:8, 11:21, 11:23, 12:2, 12:3
- `GAL`: 2:6, 2:7, 2:8
- `EPH`: 2:5, 5:8, 5:9
- `COL`: 2:21, 2:22, 4:10
- `2TI`: 1:17, 1:18
- `HEB`: 7:2, 7:3, 7:11, 7:20, 7:21, 10:7, 10:8, 11:37, 11:38
- `REV`: 16:14, 16:15, 21:25
