# The New Testament in the original Greek: Byzantine textform

![GitHub release (latest by date)](https://img.shields.io/github/v/release/ByzTxt/byzantine-majority-text?style=for-the-badge)

## What is this?

This is the official GitHub home for [Dr. Maurice A. Robinson](https://en.wikipedia.org/wiki/Maurice_A._Robinson)'s Greek
texts with morphological parsing and Strong's numbers.

This repo contains the Robinson-Pierpont edition of the Greek New
Testament in the Original Greek, Byzantine Majority Text. The 2005 edition of the text can be freely downloaded as a PDF file from The Internet Archive [here](https://archive.org/details/newtestamentrobinsonpierpontbyzantine/).

Five versions are available:

1. A parsed version in Online Bible format with morphological parsing codes, Strong's numbers, and tense-voice-mood numbers.

2. A "text only" version in Online Bible ASCII format.

3. A "text only" version in something akin to BETA Code, with accents, breathings, diarheses, iota subscripts, Byzantine variants, and
a Nestle-Aland 27 collation.

4. Unicode versions in CSV format. These files can be found in the `csv-unicode` folder (see the `README` file there for more information.)

5. TEI-XML versions (in the `tei-xml-unicode` folder) created according to the [IGNTP guidelines for XML transcriptions of New Testament manuscripts using the TEI P5 (version 1.5)](http://epapers.bham.ac.uk/1892/5/IGNTP_XML_guidelines_1-5.pdf) (see the `README` file in the folder for more information). These files are directly collatable, using the [CollateX](https://collatex.net/) software, with the [Münster INTF transcriptions](https://ntvmr.uni-muenster.de/home) of the manuscripts used in the *Editio Critica Maior*.

# Update status?

Versions (1) and (3) were last updated in mid-August, 2019, with Dr. Robinson's latest versions of his files.  The date of each file as
received from Dr. Robinson is stated in the git commit message of the given file.

Version (2) has not been updated since 2017.

The CSV files of the accented version are derived from (3).

The CSV files of the unaccented version are derived from (2). These files served as the basis for the TEI-XML version.

## Internet addresses?

1. [https://www.byzantinetext.com](https://www.byzantinetext.com)

2. [https://github.com/byztxt/](https://github.com/byztxt/)

## License?

Public Domain. Copy freely.

## Responsible parties?

- Dr. Maurice A. Robinson, Wake Forest, North Carolina, USA is the
  primary author.

- Dr. Ulrik Sandborg-Petersen, Scripture Systems ApS, Denmark, is the
  maintainer of this repo.

## Maintenance?

Yes.

1. Dr. Robinson sometimes sends updates to Ulrik.

2. Should you find any errors, please inform Ulrik via email or a
Github issue or pull request. Ulrik will then correspond with Dr. Robinson to resolve any issues in his upstream version, and then publish a new drop here.


## Contact?

Please write to Ulrik Sandborg-Petersen via
ulrikp-write-the-sign-scripturesys-dot-com.
