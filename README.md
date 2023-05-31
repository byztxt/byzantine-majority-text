# The New Testament in the original Greek: Byzantine textform

![GitHub release (latest by date)](https://img.shields.io/github/v/release/ByzTxt/byzantine-majority-text?style=for-the-badge)

Welcome to the official GitHub home of [Dr. Maurice A. Robinson](https://en.wikipedia.org/wiki/Maurice_A._Robinson)'s Greek
texts with variants, morphological parsing, and Strong's numbers.

This repository contains the Robinson-Pierpont edition of the Greek New Testament in the Original Greek, Byzantine Majority Text. The current form of the text is up-to-date as of May 29, 2023. 

The 2005 edition of the text can be freely downloaded as a PDF file from The Internet Archive [here](https://archive.org/details/newtestamentrobinsonpierpontbyzantine/). This and other editions of the text, as well as additional resources, can be downloaded from [https://www.byzantinetext.com](https://www.byzantinetext.com).

You can read professor Robinson's essay proposing the superiority of the Byzantine textform [here](https://byzantinetext.com/wp-content/uploads/2016/11/editions-rp-11-appendix.pdf) (a Spanish translation is available for free download [here](https://archive.org/details/libro-robinson-traducido/LIBRO%20ROBINSON%20TRADUCIDO/)).

Four versions are available:

1. A parsed version in BETA format, without accents (in the `source/Strongs` folder).

2. A full version in BETA format, with accents, breathings, diarheses, iota subscripts, and an apparatus containing Byzantine variants and Nestle-Aland and *Editio Critica Maior* divergences (in the `source/CCAT` folder).

3. Unicode versions in CSV format. These files can be found in the `csv-unicode` folder (see the `README` file there for more information.)

4. TEI-XML versions (in the `tei-xml-unicode` folder) created according to the [IGNTP guidelines for XML transcriptions of New Testament manuscripts using the TEI P5 (version 1.5)](http://epapers.bham.ac.uk/1892/5/IGNTP_XML_guidelines_1-5.pdf) (see the `README` file in the folder for more information). These files are directly collatable, using the [CollateX](https://collatex.net/) software, with the [Münster INTF transcriptions](https://ntvmr.uni-muenster.de/home) of the manuscripts used in the *Editio Critica Maior*.

The official files produced by Professor Robinson are (1) and (2). The other versions have been generated using the utilities that can be found in the `scripts` folder. Professor Robinson's files are the source of truth.

Should you have a question or find any errors, please inform the maintainers by opening a Github issue or pull request. The maintainers will assess each situation and then correspond with Dr. Robinson if needed.


## Copyright

All the code and text contained in this folder is in the Public Domain.