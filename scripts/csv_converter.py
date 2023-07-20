#!/usr/bin/env python
# coding: utf-8

# This file has been tested on Ubuntu 22.04 and Python 3.10
import beta_code
import re
import pandas as pd
import os
import copy
import beta_to_unicode_custom.beta_to_unicode_custom as buc

book_dict = {
    "01": "MAT",
    "02": "MAR",
    "03": "LUK",
    "04": "JOH",
    "04a": "PA",
    "05": "ACT",
    "05a": "ACT24",
    "06": "ROM",
    "07": "1CO",
    "08": "2CO",
    "09": "GAL",
    "10": "EPH",
    "11": "PHP",
    "12": "COL",
    "13": "1TH",
    "14": "2TH",
    "15": "1TI",
    "16": "2TI",
    "17": "TIT",
    "18": "PHM",
    "19": "HEB",
    "20": "JAM",
    "21": "1PE",
    "22": "2PE",
    "23": "1JO",
    "24": "2JO",
    "25": "3JO",
    "26": "JUD",
    "27": "REV",
}


################################
################################
######### CCAT VERSION #########
################################
################################

# Creating the CSV folders
path_ccat_no_variants = "../csv-unicode/ccat/no-variants"
path_ccat_with_variants = "../csv-unicode/ccat/with-variants"

if not os.path.exists(path_ccat_no_variants):
    os.makedirs(path_ccat_no_variants)

if not os.path.exists(path_ccat_with_variants):
    os.makedirs(path_ccat_with_variants)


###################################
###################################
######### STRONGS VERSION #########
###################################
###################################


# Creating the CSV folders
path_strongs_with_parsing = "../csv-unicode/strongs/with-parsing"
path_strongs_no_parsing = "../csv-unicode/strongs/no-parsing"

if not os.path.exists(path_strongs_with_parsing):
    os.makedirs(path_strongs_with_parsing)

if not os.path.exists(path_strongs_no_parsing):
    os.makedirs(path_strongs_no_parsing)


def extract_verse_chapter(line, input_format):
    """
    Extract the verse and chapter numbers from the string.
    """
    # Removing leading and trailing spaces
    line = line.strip()

    # Marking empty lines
    if len(line) == 0:
        return "", "", ""

    # Finding the chapter and verse
    if input_format == "CCAT":
        chap_verse_patt = (
            r"[0-9]+:[0-9]+"  # The chapter and verse come in this format: "XX:XX"
        )
        matches = re.search(chap_verse_patt, line)
        chap_verse = matches.group(0)
        chap = chap_verse.split(":")[0]
        verse = chap_verse.split(":")[1]
    elif input_format == "Strongs":
        chap_verse_patt = (
            r"[0-9]+\.[0-9]+"  # The chapter and verse come in this format: "XX.XX"
        )
        matches = re.search(chap_verse_patt, line)
        chap_verse = matches.group(0)
        chap = chap_verse.split(".")[0]
        verse = chap_verse.split(".")[1]

    # Removing the chapter and verse information from the text
    clean_line = re.sub(chap_verse_patt, "", line).strip()

    return chap, verse, clean_line


def read_book_lines(path):
    """
    Reads and splits up the text of a book into a list of lines, each containing one verse.
    """
    with open(path, "r") as file:
        return file.readlines()


def convert_book(path, input_format, drop_variants, drop_parsing, book):
    """
    Converts an individual book into Unicode.
    """
    # Opening the file
    lines = read_book_lines(path)

    # Converting the text
    result = []
    for line in lines:
        chap, verse, clean_line = extract_verse_chapter(line, input_format)
        if input_format == "CCAT":
            beta_line = buc.standardise_beta_code(clean_line, drop_variants)
            unicode_line = buc.convert_beta_to_unicode(beta_line)
        elif input_format == "Strongs":
            unicode_line = buc.convert_beta_to_unicode_strongs(clean_line, drop_parsing)
        result.append([chap, verse, unicode_line])

    # Converting to DataFrame and fixing the table format
    result = pd.DataFrame(result)
    result = result.replace("", pd.NA).dropna()
    result.columns = ["chapter", "verse", "text"]
    result["chapter"] = result["chapter"].astype(int)
    result["verse"] = result["verse"].astype(int)

    # Saving to disk
    if input_format == "CCAT":
        # Lines that start with '? ' are new paragraphs.
        result["text"] = result["text"].str.replace("? ", "\n", regex=False)
        if drop_variants:
            save_to = path_ccat_no_variants + "/" + book + ".csv"
        else:
            save_to = path_ccat_with_variants + "/" + book + ".csv"
    elif input_format == "Strongs":
        if drop_parsing:
            save_to = path_strongs_no_parsing + "/" + book + ".csv"
        else:
            save_to = path_strongs_with_parsing + "/" + book + ".csv"
    result.to_csv(save_to, index=False)


def convert_all_books_to_unicode(
    book_dict, input_format, drop_parsing=True, drop_variants=True
):
    """
    Convenience function to convert all books in the same batch.

    Set drop_variants=False if you want to keep textual variants
    in the output file.
    """
    dict_of_all_books = copy.deepcopy(book_dict)

    for booknum in dict_of_all_books:
        if input_format == "CCAT":
            # Use .CCAT files as a source
            if drop_variants:
                print(
                    "     Converting "
                    + dict_of_all_books[booknum]
                    + " and dropping variants"
                )
            else:
                print(
                    "     Converting "
                    + dict_of_all_books[booknum]
                    + " and keeping variants"
                )
            path = (
                "../source/CCAT/" + booknum + "_" + dict_of_all_books[booknum] + ".TXT"
            )
        elif (input_format == "Strongs") and (
            "a" not in booknum
        ):  # If letter a is in booknum, then it is the CCAT of the PA or ACTS24 (Byzantine variants) and file doesn't have Strong's equivalent
            # Use .BP5 files as a source
            print("     Converting " + dict_of_all_books[booknum] + " (no accents)")
            path = (
                "../source/Strongs/"
                + booknum
                + "_"
                + dict_of_all_books[booknum]
                + ".BP5"
            )
        if (input_format == "Strongs") and (
            "a" in booknum
        ):  # If letter a is in booknum, then it is the CCAT of the PA or ACTS24 (Byzantine variants) and file doesn't have Strong's equivalent
            pass
        else:
            converted_book = convert_book(
                path=path,
                input_format=input_format,
                drop_variants=drop_variants,
                drop_parsing=drop_parsing,
                book=dict_of_all_books[booknum],
            )


######## Converting all books
print("CONVERTING ALL BOOKS (CCAT) AND KEEPING TEXTUAL VARIANTS")
convert_all_books_to_unicode(book_dict, input_format="CCAT", drop_variants=False)
print("Done.")
print("\n---\n")

print("CONVERTING ALL BOOKS (CCAT) AND DROPPING TEXTUAL VARIANTS")
convert_all_books_to_unicode(book_dict, input_format="CCAT", drop_variants=True)
print("Done.")
print("\n---\n")

print("CONVERTING ALL BOOKS (STRONG'S) AND KEEPING PARSING")
convert_all_books_to_unicode(book_dict, input_format="Strongs", drop_parsing=False)
print("Done.")
print("\n---\n")

print("CONVERTING ALL BOOKS (STRONG'S) AND DROPPING PARSING")
convert_all_books_to_unicode(book_dict, input_format="Strongs", drop_parsing=True)
print("Done.")
print("\n---\n")
