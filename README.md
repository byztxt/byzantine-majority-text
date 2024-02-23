# The New Testament in the original Greek: Byzantine textform

![GitHub release (latest by date)](https://img.shields.io/github/v/release/ByzTxt/byzantine-majority-text?style=for-the-badge)

Welcome to the official GitHub home of [Dr. Maurice A. Robinson](https://en.wikipedia.org/wiki/Maurice_A._Robinson)'s Greek
texts with variants, morphological parsing, and Strong's numbers.

This repository contains the Robinson-Pierpont edition of the Greek New Testament in the Original Greek, Byzantine Majority Text. The current form of the text is up-to-date as of July 20, 2023 and represents the 2018 Robinson Pierpont edition (with some minor adjustments to the critical apparatus). 

The 2005 edition of the text can be freely downloaded as a PDF file from The Internet Archive [here](https://archive.org/details/newtestamentrobinsonpierpontbyzantine/). The 2018 edition can be downloaded from [this link](https://archive.org/details/robinson-pierpont-2018-gnt-edition). RP2018 is recommended over RP2005 for all practical purposes (read details below). Additional resources can be downloaded from [https://www.byzantinetext.com](https://www.byzantinetext.com).

You can read professor Robinson's essay proposing the superiority of the Byzantine textform [here](https://byzantinetext.com/wp-content/uploads/2016/11/editions-rp-11-appendix.pdf) (a Spanish translation is available for free download [here](https://archive.org/details/libro-robinson-traducido/LIBRO%20ROBINSON%20TRADUCIDO/)). The essay can be found in a plain text format inside the `essay` folder.

Four versions are available:

1. A parsed version in BETA format, without accents (in the `source/Strongs` folder).

2. A full version in BETA format, with accents, breathings, diarheses, iota subscripts, and an apparatus containing Byzantine variants and Nestle-Aland and *Editio Critica Maior* divergences (in the `source/CCAT` folder).

3. Unicode versions in CSV format. These files can be found in the `csv-unicode` folder (see the `README` file there for more information.)

4. TEI-XML versions (in the `tei-xml-unicode` folder) created according to the [IGNTP guidelines for XML transcriptions of New Testament manuscripts using the TEI P5 (version 1.5)](http://epapers.bham.ac.uk/1892/5/IGNTP_XML_guidelines_1-5.pdf) (see the `README` file in the folder for more information). These files are directly collatable, using the [CollateX](https://collatex.net/) software, with the [Münster INTF transcriptions](https://ntvmr.uni-muenster.de/home) of the manuscripts used in the *Editio Critica Maior*.

The official files produced by Professor Robinson are (1) and (2). The other versions have been generated using the utilities that can be found in the `scripts` folder. Professor Robinson's files are the source of truth.

Should you have a question or find any errors, please inform the maintainers by opening a Github issue or pull request. The maintainers will assess each situation and then correspond with Dr. Robinson if needed.

## Versions

The two official printed editions of the Byzantine Textform are those of the years 2005 and 2018, both of which are widely available as PDFs and in print. This repository contains data from both. However, prior to the year 2022, this repository did not have a formal versioning system, and therefore recuperating the exact wordings of the 2005 and 2018 editions is not straightforward from the Git history.

It is strongly recommended that versions `3.x.x` be used instead of previous ones, for at least the following reasons:

* Previous to release 1.0.0 there was *no* Unicode version of the files. The source files (which were in a custom flavor of Beta code) *were* however in the repository and can be accessed by browsing the Git history.

* A Unicode converter was added in release 1.0.0, but its output unfortunately produced various misspellings. The errors were successfully fixed in release 2.0.3. Should anyone want to use a text closest to RP2005, the suggested Unicode files are those of release 2.0.3. Please do **not** use the Unicode files of releases prior to 2.0.3 as those contain conversion errors (the source Beta code files, however, did not change between releases 1.0.0 and 2.0.3 and are official as they came directly from Professor Robinson).

* Release 3.0.0 introduced the text of the RP2018 edition, with minor updates to the apparatus. By direct recommendation of professor Robinson, *the use of the RP2005 is discouraged in favor of RP2018*, as RP2005 had "numerous accent, breathing, and punctuation errors (caused by porting over an NA27 file, and then altering only where the Byz text differed)". Additionally, "the 2018 edition should be used, since those errors were corrected". The text was updated "in a very few places", and the apparatus was updated as well in order to "to reflect NA28 and ECM differences in the general epistles and Acts". Note that the *unaccented* text remained highly stable between RP2005 and RP2018.

## Archiving

A mirror of this repository is available at the [Software Heritage Archive](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/byztxt/byzantine-majority-text).

## Copyright

All the code and text contained in this folder is in the Public Domain.
