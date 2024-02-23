#!/usr/bin/env python
# coding: utf-8

import beta_code
import re


def standardise_beta_code(text, drop_variants=True):
    """
    Pre-process the beta code to make it compatible with the beta-code library.

    We use that library to do the actual conversion.
    You can find more information here: https://github.com/perseids-tools/beta-code-py

    The beta-code library requires that Dialytika and Tonos (/+) or Dialytika
    and Varia (\+) are written with the slash before the plus sign,
    while Prof. Robinson's text puts the plus first.

    This function also replaces apostrophes with right quotation marks
    in order to make the typography more consistent and aesthetically pleasing.

    It also adds a space after some final sigmas to avoid their conversion to medial sigmas.

    It has an option to remove textual variants.
    """

    # Removing variants and other metadata (everything between curly braces)
    if drop_variants:
        text = re.sub(
            r"{.+?}", "", text
        )  # See https://stackoverflow.com/a/8784436/6945498
        text = re.sub(" +", " ", text)  # Removing double spaces

    # Swapping the order of plus (+) followed by slash (/ or \)
    text = text.replace("+/", "/+")
    text = text.replace("+\\", "\\+")

    # Replacing apostrophes with quotation marks
    text = text.replace("'", "’")

    # Adding a space between final sigma and dash/bracket (if not done, final sigma is rendered as a medial sigma)
    text = text.replace("S-", "S -")
    text = text.replace("S]", "S ]")

    # Removing leading and trailing spaces
    text = text.strip()

    return text


def convert_beta_to_unicode(beta):
    """
    Converts the standardised beta code to Unicode.

    This function makes use of the beta_code_to_greek()
    function from the beta-code package.
    """
    beta = beta.replace(
        " = ", " ♦ "
    )  # This is to avoid the equals sign being converted to an accent, see issue #33
    word_tokenised_beta = beta.split(" ")
    beta_line = " ".join(word_tokenised_beta)
    unicode_line = beta_code.beta_code_to_greek(beta_line)

    # The following lines replace the apparatus codes
    # These codes are explained in the README.md file that is inside the `source` folder.
    # The codes are originally capital Latin letters, but they are converted to Greek letters by the converter
    # In consequence, we replace the respective Greek letters in the converted Greek text
    unicode_line = unicode_line.replace("{ν", "{NA")
    unicode_line = unicode_line.replace("{β", "{Byz")
    unicode_line = unicode_line.replace("{ξ", "{NA27/28")
    unicode_line = unicode_line.replace("{μ", "{ECM")
    unicode_line = unicode_line.replace("{ς", "{NA27")
    unicode_line = unicode_line.replace("{ε", "{NA28")
    unicode_line = unicode_line.replace(
        "ς -", "ς-"
    )  # Removing the extra space between final sigmas and dashes/brackets that was added by the standardise_beta_code() function
    unicode_line = unicode_line.replace("ς ]", "ς]")
    unicode_line = unicode_line.replace(" ♦ ", " = ")  # Placing the equals sign back
    return unicode_line


def convert_beta_to_unicode_strongs(beta, drop_parsing):
    """
    Converts the standardised beta code to Unicode.

    This function makes use of the beta_code_to_greek()
    function from the beta-code package.
    """
    word_tokenised_beta = beta.split(" ")

    unicode_word_list = []

    for word in word_tokenised_beta:
        if len(word) == 0:
            continue
        elif word.isdigit():
            if drop_parsing:
                continue
            else:
                unicode_word_list.append(word)
        elif word[0] == "{" and word[-1] == "}":
            if drop_parsing:
                continue
            else:
                unicode_word_list.append(word)
        else:
            unicode_word_list.append(beta_code.beta_code_to_greek(word))

    unicode_line = " ".join(unicode_word_list)
    return unicode_line
