#!/usr/bin/env python
# coding: utf-8

# This file has been tested on Ubuntu 20.04 and Python 3.8
import beta_code
import re
import pandas as pd


def extract_verse_chapter(line):
    """
    Extract the verse and chapter numbers from the string.
    """
    # Removing leading and trailing spaces
    line = line.strip()

    # Marking empty lines
    if len(line) == 0:
        return "", "", ""

    # Removing file metadata
    if line[0] == "#":
        return "", "", ""

    # Finding the chapter and verse
    chap_verse_patt = (
        r"[0-9]+:[0-9]+"  # The chapter and verse come in this format: "XX:XX"
    )
    matches = re.search(chap_verse_patt, line)
    chap_verse = matches.group(0)
    chap = chap_verse.split(":")[0]
    verse = chap_verse.split(":")[1]

    # Removing the chapter and verse information from the text
    clean_line = re.sub(chap_verse_patt, "", line).strip()

    return chap, verse, clean_line


def standardise_beta_code(text, drop_variants=True):
    """
    Pre-process the beta code to make it compatible with the beta-code library.

    We use that library to do the actual conversion.
    You can find more information here: https://github.com/perseids-tools/beta-code-py

    The beta-code library requires that the subscripted iota character (|) and the accents are placed
    after the uppercase letter, not before, as in Prof. Robinson's text.

    It also requires that uppercase Greek letters
    begin with an asterisk, which Prof. Robinson's text doesn't do.

    It also requires that Dialytika and Tonos (/+) or Dialytika and Varia (\+) are written with the
    slash before the plus sign, while Prof. Robinson's text puts the plus first.

    Circumflex accents are represented with the = sign in the beta-code library,
    while Prof. Robinson's text represents them with the character ^

    It removes paragraph markers ({P}) and has an option to remove textual variants
    """

    # Removing paragraph markers
    text = text.replace("{P}", "")

    # Removing variants and other metadata (everything between curly braces)
    if drop_variants:
        text = re.sub(
            r"{.+?}", "", text
        )  # See https://stackoverflow.com/a/8784436/6945498
        text = re.sub(" +", " ", text)  # Removing double spaces

    # Replacing uppercase letters with asterisked letters
    asterisked_dict = {
        "A": "*A",
        "B": "*B",
        "G": "*G",
        "D": "*D",
        "E": "*E",
        "V": "*V",
        "Z": "*Z",
        "H": "*H",
        "Q": "*Q",
        "I": "*I",
        "K": "*K",
        "L": "*L",
        "M": "*M",
        "N": "*N",
        "C": "*C",
        "O": "*O",
        "P": "*P",
        "R": "*R",
        "S": "*S",
        "T": "*T",
        "U": "*U",
        "F": "*F",
        "X": "*X",
        "Y": "*Y",
        "W": "*W",
    }

    for key, value in asterisked_dict.items():
        text = text.replace(key, value)

    # Swapping the order of plus (+) followed by slash (/ or \)
    text = text.replace("+/", "/+")
    text = text.replace("+\\", "\\+")

    # Replacing carets (^) with equals signs (=)
    text = text.replace("^", "=")

    # Moving subscripted iotas (|) to after the character when uppercase
    iota_dict = {
        "|*A": "*A|",
        "|*B": "*B|",
        "|*G": "*G|",
        "|*D": "*D|",
        "|*E": "*E|",
        "|*V": "*V|",
        "|*Z": "*Z|",
        "|*H": "*H|",
        "|*Q": "*Q|",
        "|*I": "*I|",
        "|*K": "*K|",
        "|*L": "*L|",
        "|*M": "*M|",
        "|*N": "*N|",
        "|*C": "*C|",
        "|*O": "*O|",
        "|*P": "*P|",
        "|*R": "*R|",
        "|*S": "*S|",
        "|*T": "*T|",
        "|*U": "*U|",
        "|*F": "*F|",
        "|*X": "*X|",
        "|*Y": "*Y|",
        "|*W": "*W|",
    }

    for key, value in iota_dict.items():
        text = text.replace(key, value)

    # Moving accents (\, = and /) to after the star when uppercase
    accents_dict = {
        "/*A": "*/A",
        "\*A": "*\A",
        "=*A": "*=A",
        "/*B": "*/B",
        "\*B": "*\B",
        "=*B": "*=B",
        "/*G": "*/G",
        "\*G": "*\G",
        "=*G": "*=G",
        "/*D": "*/D",
        "\*D": "*\D",
        "=*D": "*=D",
        "/*E": "*/E",
        "\*E": "*\E",
        "=*E": "*=E",
        "/*V": "*/V",
        "\*V": "*\V",
        "=*V": "*=V",
        "/*Z": "*/Z",
        "\*Z": "*\Z",
        "=*Z": "*=Z",
        "/*H": "*/H",
        "\*H": "*\H",
        "=*H": "*=H",
        "/*Q": "*/Q",
        "\*Q": "*\Q",
        "=*Q": "*=Q",
        "/*I": "*/I",
        "\*I": "*\I",
        "=*I": "*=I",
        "/*K": "*/K",
        "\*K": "*\K",
        "=*K": "*=K",
        "/*L": "*/L",
        "\*L": "*\L",
        "=*L": "*=L",
        "/*M": "*/M",
        "\*M": "*\M",
        "=*M": "*=M",
        "/*N": "*/N",
        "\*N": "*\A",
        "=*N": "*=N",
        "/*C": "*/C",
        "\*C": "*\C",
        "=*C": "*=C",
        "/*O": "*/O",
        "\*O": "*\O",
        "=*O": "*=O",
        "/*P": "*/P",
        "\*P": "*\P",
        "=*P": "*=P",
        "/*R": "*/R",
        "\*R": "*\R",
        "=*R": "*=R",
        "/*S": "*/S",
        "\*S": "*\S",
        "=*S": "*=S",
        "/*T": "*/T",
        "\*T": "*\T",
        "=*T": "*=T",
        "/*U": "*/U",
        "\*U": "*\\U",
        "=*U": "*=U",
        "/*F": "*/F",
        "\*F": "*\F",
        "=*F": "*=F",
        "/*X": "*/X",
        "\*X": "*\X",
        "=*X": "*=X",
        "/*Y": "*/Y",
        "\*Y": "*\Y",
        "=*Y": "*=Y",
        "/*W": "*/W",
        "\*W": "*\W",
        "=*W": "*=W",
    }

    for key, value in accents_dict.items():
        text = text.replace(key, value)

    # Moving breathings ( ( and ) ) to after the star when uppercase
    breathings_dict = {
        "(/*": "*(/",
        ")/*": "*)/",
        "(\*": "*(\\",
        ")\*": "*)\\",
        "(=*": "*(=",
        ")=*": "*)=",
        "(*": "*(",
        ")*": "*)",
    }

    for key, value in breathings_dict.items():
        text = text.replace(key, value)

    # Removing leading and trailing spaces
    text = text.strip()

    return text


def convert_beta_to_unicode(beta):
    """
    Converts the standardised beta code to Unicode.

    This function makes use of the beta_code_to_greek()
    function from the beta-code package.
    """
    word_tokenised_beta = beta.split(" ")
    for i in range(0, len(word_tokenised_beta)):
        if (
            word_tokenised_beta[i][-2:] == "s]"
        ):  # So that final sigmas that come before ] are properly converted (not made into medial sigmas)
            # Note that two spaces are needed, because ' ]' already appears in the beta code (Mark 16:8)
            word_tokenised_beta[i] = word_tokenised_beta[i].replace("]", "  ]")
    beta_line = " ".join(word_tokenised_beta)
    unicode_result = beta_code.beta_code_to_greek(beta_line)
    unicode_result = unicode_result.replace(
        "  ]", "]"
    )  # Removing the auxiliary spaces we added for the sigmas
    return unicode_result


def convert_book(path, drop_variants, book):
    """
    Converts an individual book into Unicode.
    """
    # Opening the file
    with open(path) as f:
        lines = f.readlines()

    # Converting the text
    result = []
    for line in lines:
        chap, verse, clean_line = extract_verse_chapter(line)
        beta_line = standardise_beta_code(clean_line, drop_variants)
        unicode_line = convert_beta_to_unicode(beta_line)
        result.append([chap, verse, unicode_line])
        # print("     ",chap, verse, beta_line, unicode_line)

    # Converting to DataFrame and fixing the table format
    result = pd.DataFrame(result)
    result = result.replace("", pd.NA).dropna()
    result.columns = ["chapter", "verse", "text"]
    result["chapter"] = result["chapter"].astype(int)
    result["verse"] = result["verse"].astype(int)

    # Saving to disk
    if drop_variants:
        save_to = "no-variants/" + book + ".csv"
    else:
        save_to = "with-variants/" + book + ".csv"
    result.to_csv(save_to, index=False)


def convert_all_books_to_unicode(drop_variants=True):
    """
    Convenience function to convert all books in the same batch.

    Set drop_variants=False if you want to keep textual variants
    in the output file.
    """
    list_of_all_books = [
        "1CO",
        "1JO",
        "1PE",
        "1TH",
        "1TI",
        "2CO",
        "2JO",
        "2PE",
        "2TH",
        "2TI",
        "3JO",
        "AC",
        "COL",
        "EPH",
        "GA",
        "HEB",
        "JAS",
        "JOH",
        "JUDE",
        "LU",
        "MR",
        "MT",
        "PHM",
        "PHP",
        "RE",
        "RO",
        "TIT",
        "AC24",  # Verses in chapter 24 of Acts
        "PA",  # Pericope adulterae
    ]

    for book in list_of_all_books:
        if drop_variants:
            print("     Converting " + book + " and dropping variants")
        else:
            print("     Converting " + book + " and keeping variants")
        path = "../textonly-beta-code/" + book + ".CCT"
        converted_book = convert_book(path=path, drop_variants=drop_variants, book=book)


######## Converting all books
print(
    "CONVERTING ALL BOOKS AND KEEPING TEXTUAL VARIANTS - SAVING TO THE with-variants FOLDER"
)
convert_all_books_to_unicode(drop_variants=False)
print("Done.")
print("\n---\n")
print(
    "CONVERTING ALL BOOKS AND DROPPING TEXTUAL VARIANTS - SAVING TO THE no-variants FOLDER"
)
convert_all_books_to_unicode(drop_variants=True)
print("Done.")
