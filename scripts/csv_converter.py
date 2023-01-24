#!/usr/bin/env python
# coding: utf-8

# This file has been tested on Ubuntu 20.04 and Python 3.8
import beta_code
import re
import pandas as pd
import os
import copy
import beta_to_unicode_custom.beta_to_unicode_custom as buc

book_list = [
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
]

################################
################################
##### VERSION WITH ACCENTS #####
################################
################################

# Creating the CSV folders
path_accents_no_variants = "../csv-unicode/accents/no-variants"
path_accents_with_variants = "../csv-unicode/accents/with-variants"

if not os.path.exists(path_accents_no_variants):
    os.makedirs(path_accents_no_variants)

if not os.path.exists(path_accents_with_variants):
    os.makedirs(path_accents_with_variants)


###################################
###################################
##### VERSION WITHOUT ACCENTS #####
###################################
###################################


# Creating the CSV folders
path_no_accents = "../csv-unicode/no-accents"

if not os.path.exists(path_no_accents):
    os.makedirs(path_no_accents)


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


def make_one_verse_one_line(book_text):
    """
    Convert the text so that each verse takes only one line.

    In the original .ASC files, each verse can take several lines.
    """
    book_text = book_text.replace("\n", " ")
    separator = "     "  # Verses are all preceded by this in the original .ASC files
    separated_list = book_text.split(separator)  # Splitting the text into a list
    separated_list = [
        item for item in separated_list if item != ""
    ]  # Removing the empty elements of the list
    # resulting_text = "\n".join(separated_list) # Merging the list into a single text string
    return separated_list


def read_book_lines(path, accents):
    """
    Reads and splits up the text of a book into a list of lines, each containing one verse.
    """
    with open(path, "r") as file:
        if accents:
            # The .CCT files use one line for each verse
            lines = file.readlines()
        else:
            # In the original .ASC files, each verse can take several lines.
            book_text = file.read()
            lines = make_one_verse_one_line(book_text)
    return lines


def convert_book(path, accents, drop_variants, book):
    """
    Converts an individual book into Unicode.
    """
    # Opening the file
    lines = read_book_lines(path, accents)

    # Converting the text
    result = []
    for line in lines:
        chap, verse, clean_line = extract_verse_chapter(line)
        beta_line = buc.standardise_beta_code(clean_line, drop_variants)
        if accents:
            unicode_line = buc.convert_beta_to_unicode(beta_line)
        else:
            unicode_line = buc.convert_asc_to_unicode(beta_line)
        result.append([chap, verse, unicode_line])
        # print("     ",chap, verse, beta_line, unicode_line)

    # Converting to DataFrame and fixing the table format
    result = pd.DataFrame(result)
    result = result.replace("", pd.NA).dropna()
    result.columns = ["chapter", "verse", "text"]
    result["chapter"] = result["chapter"].astype(int)
    result["verse"] = result["verse"].astype(int)

    # Saving to disk
    if accents:
        if drop_variants:
            save_to = path_accents_no_variants + "/" + book + ".csv"
        else:
            save_to = path_accents_with_variants + "/" + book + ".csv"
    else:
        save_to = path_no_accents + "/" + book + ".csv"
    result.to_csv(save_to, index=False)


def convert_all_books_to_unicode(book_list, accents, drop_variants=True):
    """
    Convenience function to convert all books in the same batch.

    Set drop_variants=False if you want to keep textual variants
    in the output file.
    """
    list_of_all_books = copy.deepcopy(book_list)
    if accents:
        # Acts 24 and the Pericope Adulterae - the accented texts store these in separate files
        list_of_all_books.append("AC24")
        list_of_all_books.append("PA")

    for book in list_of_all_books:
        if accents:
            # Use .CCT files as a source
            if drop_variants:
                print("     Converting " + book + " and dropping variants")
            else:
                print("     Converting " + book + " and keeping variants")
            path = "../textonly-beta-code/" + book + ".CCT"
        else:
            # Use .ASC files as a source
            print("     Converting " + book + " (no accents)")
            path = "../textonly-online-bible/" + book + "05.ASC"

        converted_book = convert_book(
            path=path, accents=accents, drop_variants=drop_variants, book=book
        )


######## Converting all books
print(
    "CONVERTING ALL BOOKS (WITH ACCENTS) AND KEEPING TEXTUAL VARIANTS - SAVING TO THE with-accents/with-variants FOLDER"
)
convert_all_books_to_unicode(book_list, accents=True, drop_variants=False)
print("Done.")
print("\n---\n")

print(
    "CONVERTING ALL BOOKS (WITH ACCENTS) AND DROPPING TEXTUAL VARIANTS - SAVING TO THE with-accents/no-variants FOLDER"
)
convert_all_books_to_unicode(book_list, accents=True, drop_variants=True)
print("Done.")
print("\n---\n")

print("CONVERTING ALL BOOKS (NO ACCENTS) - SAVING TO THE no-accents FOLDER")
convert_all_books_to_unicode(book_list, accents=False)
print("Done.")
print("\n---\n")
