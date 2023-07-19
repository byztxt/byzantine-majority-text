# Source files

This folder contains the source files of the Byzantine Texform as created and maintained by Dr. Maurice A. Robinson. These files are the ultimate source of truth should any question arise regarding the derivative Unicode files provided in this repository.

These files are written in Beta code. The Beta code of the files differs from the standard used by the `beta-code` library (which is used for the conversion to Unicode) as explained in the docstring and code of the `standardise_beta_code()` function in the `scripts/beta_to_unicode_custom/beta_to_unicode_custom.py` script.

The files in the `CCAT` folder contain accents and variants, while the files in the `Strongs` folder contain Strong's numbers and parsing codes.

## Variant codes

The files in the `CCAT` folder include the variants following the below convention:

* `N`: Nestle-Aland variant.
* `B`: Byzantine variant.
* `C`: NA27/28 variant.
* `M`: ECM (*Editio Critica Maior*) variant.
* `S`: NA27 variant.
* `E`: NA28 variant.

## Parsing codes and Strong's numbers

The files in the `Strongs` folder contain parsing codes and Strong numbers according to the below convention, which was designed by Dr. Robinson (the original source of the convention was [this 2009 document](https://github.com/byztxt/robinson-documentation/blob/master/doc/PARSING.COD)).

### Parsing codes

The codes which follow reflect an original abridgment and correction of the data presented in "The Analytical Greek Lexicon" (London: Samuel Bagster and Sons, 1859).

Comparison also has been made against the revised updating of that lexicon by Wesley J. Perschbacher in his "The New Analytical Greek Lexicon" (Peabody, MA: Hendrickson, 1990). The Perschbacher revision failed to adjust over 600 parsing or declensional errors in the original Bagster edition; these now have been corrected.

The abbreviation system was developed independently. Its features are similar to those in Timothy and Barbara Friberg "The Analytical Greek New Testament" (Grand Rapids: Baker, 1981), and can be used readily by anyone familiar with the Bagster lexicon, Perschbacher, or Friberg.

Many Greek New Testament verbal forms can be parsed in more than one manner. The parsings given reflect a normal interpretation of those forms which actually occur in the Greek New Testament. Every NT occurrence is covered, and the parsings reflect the totality of Greek NT verbal forms.

The data presented are not claimed to be free from error; the editor may be notified of any problem regarding the parsing, declension, or Strong's number assigned to any word.

All Greek verbs are listed in one of three various forms (where V = "Verb"):

1. V-tense-voice-mood
2. V-tense-voice-mood-person-number
3. V-tense-voice-mood-case-number-gender

The abbreviations which pertain to each of these categories are the following:

| Tense             | Abbreviation |
| ----------------- | ------------ |
| Present           | P            |
| Imperfect         | I            |
| Future            | F            |
| Second Future     | 2F           |
| Aorist            | A            |
| Second Aorist     | 2A           |
| Perfect           | R            |
| Second Perfect    | 2R           |
| Pluperfect        | L            |
| Second Pluperfect | 2L           |

**Special note:** the so-called "Second" forms of the Aorist, Future, Perfect and Pluperfect are respectively designated as 2A, 2F, 2P and 2L, preceding the voice and mood designations. Functionally, these forms are equivalent to the undesignated (First) Aorist, Future, Perfect, and Pluperfect forms.

| Voice                      | Abbreviation |
| -------------------------- | ------------ |
| Active                     | A            |
| Middle                     | M            |
| Passive                    | P            |
| Either middle or passive   | E            |
| middle Deponent            | D            |
| passive Deponent           | O            |
| middle or passive Deponent | N            |

| Mood        | Abbreviation |
| ----------- | ------------ |
| Indicative  | I            |
| Subjunctive | S            |
| Optative    | O            |
| Imperative  | M            |
| Infinitive  | N            |
| Participle  | P            |

| Extra            | Abbreviation |
| ---------------- | ------------ |
| Attic Greek form | -ATT         |

| Person        | Abbreviation |
| ------------- | ------------ |
| First person  | 1            |
| Second person | 2            |
| Third person  | 3            |

| Number   | Abbreviation |
| -------- | ------------ |
| Singular | S            |
| Plural   | P            |

| Gender    | Abbreviation |
| --------- | ------------ |
| Masculine | M            |
| Feminine  | F            |
| Neuter    | N            |

| Case (5-case system only; no Vocative in verbal forms) | Abbreviation |
| ------------------------------------------------------ | ------------ |
| Nominative                                             | N            |
| Genitive                                               | G            |
| Dative                                                 | D            |
| Accusative                                             | A            |

### Strong's numbers

To access the lexical root form definition of any Greek word, the appropriate Strong's concordance number immediately follows each Greek word. The definition then can be obtained by the normal routine for definitions as used for English texts.

The Strong's numbers used for the Greek New Testament do NOT always coincide with those used in the English texts. Strong clearly assisted the lay reader of the Authorized Version by assigning numbers to each unique root word form; however, he also attempted further to aid the reader by subdividing some root forms into separately numbered entries.

The result of such subdivision can be seen in the multiple forms of the verb "to be" (each of which ultimately derives from Strong's 1510). The same policy of separate numerical entries also was applied to various comparative and superlative forms of some adjectives and adverbs, as well as to the adverbial use of some noun forms.

Conversely, rather than treating each word separately (as would have been proper for anyone able to read the Greek), Strong assigned a single unique number to certain multiple-word expressions (e.g., "ou mh" or "ei de mhge"). Such a number no longer was reflective of the individual root forms. Once more, this action was taken by Strong in order to assist the lay English reader who knew no Greek; in practice this policy becomes a severe hindrance to those who know and seek to read and understand the New Testament in its original Koine Greek.

Thus, the Strong's numbers -- well-suited as they may be for the lay reader of the English text -- in places become confusing and detrimental to those reading the Greek New Testament who would use those numbers when searching for or classifying the ultimate lexical root forms of various Greek words.

The present Greek edition often alters Strong's Greek word numbers so that they relate directly to their ultimate practical root form where possible. For example, all forms of the irregular second aorist root "eipon" (Strong's 2036) now are assigned to the root "legw" (Strong's 3004), to which "eipon" functions as the practical aorist. Similarly, all derived forms of "eidon" (originally included within Strong's 1492) now are related appropriately to either "oraw" (Strong's 3708) or "oida" (Strong's 1492), in accordance with their particular meaning. However, in some cases (e. g., mhge), a Strong's original phrase-based number has been retained to identify the particular single word that otherwise would have no unique Strong's number.

In some cases, new words exist within the Koine Greek text that had not appeared in the Textus Receptus upon which Strong's numbering system had been based. In such cases, the new word is prefixed by a <0> entry, and located either under a relatively appropriate Strong's number, or has been assigned a Strong's number that otherwise would no longer exist, due to root consolidation. One case in particular is that of "ekperissou" and "ekperisswv," neither of which exist separately in the TR: these have been assigned the Strong's numbers 4053 and 4057, thus retaining a single common root, and that in close relation to other words containing some form of "periss-".

The revision of the Strong's numbers within the Greek NT text is an ongoing process. Ultimately all Strong's numbers in the Greek text will agree with the Greek lexical root form.

Note that it is ASSUMED that all Strong's numbers are correct; these have not been verified, although many errors have been noted and corrected.

### Additional notes

THE VARIOUS FORMS OF THE VERB "TO BE":

Although the analytical lexicons state no voice for the various forms of "to be" (including compound verbs in which "-eimi" is an element), for the purposes of the current parsing data ALL such forms are considered to be in the ACTIVE voice.

In addition, Strong's Concordance gives unique numbers to many separate forms of the verb "to be", even though all these properly derive from "eimi" (1510) alone. Perschbacher gives both numbers: the particular Strong's number in the left margin and the root number 1510 in the right margin. In the present electronic Greek NT texts, ALL forms of "eimi" reflect the single number 1510.

Since accents and breathings are not provided in these Greek texts, some word forms will appear identical although possessing distinct parsings or declensions. The following specifically should be noted:

* The form "h" occurs infrequently as part of the verb "to be" (V-PAS-3S of 1510, numbered 5600 by Strong); the same form reflecting the definite article (3588), relative pronoun (3739), and disjunctive particle (2228, 2229) dominates within the Greek NT.
* The form "ei" also occurs infrequently as part of the verb "to be" (V-PAI-2S of 1510, numbered 1488 by Strong); the same form (in the absence of accents and breathings) occurs most frequently as a conditional particle (1487).
* The form "hn" is frequent as a verb form in the Greek NT (V-IAI-3S of 1510, numbered 2258 by Strong); it also occurs frequently as a relative pronoun (3739).
* The subjunctive verb form "wsin" (V-PAS-3P of 1510) is incorrectly cited by Strong as participial (5607). Note also that the same form may be a plural noun from 3775.
* The verb form "hv" can be either a present subjunctive (PAS-2S, Strong 1510) or an imperfect indicative (V-IAI-2S, Strong 2229). Both forms derive from the root 1510; the parsing information following each form makes the distinction clear.

### Sample of current coding as applied

| Perschbacher:                                     | Robinson:      |
| ------------------------------------------------- | -------------- |
| agayopoihsai    (15) aor. act. inf.               | V-AAN     <15> |
| agayopoihte     (15) 2 pers. pl. pres. act. subj. | V-PAS-2P  <15> |
| agayopoiountav  (17) acc. pl. m. pres. act. part. | V-PAP-APM <17> |
