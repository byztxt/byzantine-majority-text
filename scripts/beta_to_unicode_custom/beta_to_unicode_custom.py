#!/usr/bin/env python
# coding: utf-8

import beta_code
import re


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

    It also requires that the characters |/ are reversed, that is, like this: /|

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

    # Swapping the order of pipe followed by slash (|/)
    text = text.replace("|/", "/|")

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

    # Moving accents (\, =, and /) to after the star when uppercase
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


def convert_asc_to_unicode(text):
    """
    Pre-process Professor Robinson's ASC to make it compatible with the beta-code library.

    We use that library to do the actual conversion.
    You can find more information here: https://github.com/perseids-tools/beta-code-py
    """
    text = text.replace("v", "s")
    text = text.replace("y", "q")
    
    # This part is tricky. We need to replace c with x and viceverse
    # We add a temporary character to help us with that
    text = text.replace("c", "j") # j is the auxiliary character
    text = text.replace("x", "c")
    text = text.replace("j", "x") # Removing the auxiliary character
    text = beta_code.beta_code_to_greek(text)
    return text
