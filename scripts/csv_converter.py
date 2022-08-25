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


def convert_book_accents(path, drop_variants, book):
    """
    Converts an individual book into Unicode (accents).
    """
    # Opening the file
    with open(path) as f:
        lines = f.readlines()

    # Converting the text
    result = []
    for line in lines:
        chap, verse, clean_line = extract_verse_chapter(line)
        beta_line = buc.standardise_beta_code(clean_line, drop_variants)
        unicode_line = buc.convert_beta_to_unicode(beta_line)
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
        save_to = path_accents_no_variants + "/" + book + ".csv"
    else:
        save_to = path_accents_with_variants + "/" + book + ".csv"
    result.to_csv(save_to, index=False)


def convert_all_books_to_unicode_accents(book_list, drop_variants=True):
    """
    Convenience function to convert all books in the same batch.

    Set drop_variants=False if you want to keep textual variants
    in the output file.
    """
    list_of_all_books = copy.deepcopy(book_list)
    list_of_all_books.append("AC24")  # Acts 24 and the Pericope Adulterae
    list_of_all_books.append("PA")

    for book in list_of_all_books:
        if drop_variants:
            print("     Converting " + book + " and dropping variants")
        else:
            print("     Converting " + book + " and keeping variants")
        path = "../textonly-beta-code/" + book + ".CCT"
        converted_book = convert_book_accents(
            path=path, drop_variants=drop_variants, book=book
        )


######## Converting all books
print(
    "CONVERTING ALL BOOKS (WITH ACCENTS) AND KEEPING TEXTUAL VARIANTS - SAVING TO THE with-accents/with-variants FOLDER"
)
convert_all_books_to_unicode_accents(book_list, drop_variants=False)
print("Done.")
print("\n---\n")
print(
    "CONVERTING ALL BOOKS (WITH ACCENTS) AND DROPPING TEXTUAL VARIANTS - SAVING TO THE with-accents/no-variants FOLDER"
)
convert_all_books_to_unicode_accents(book_list, drop_variants=True)
print("Done.")


###################################
###################################
##### VERSION WITHOUT ACCENTS #####
###################################
###################################


# Creating the CSV folders
path_no_accents = "../csv-unicode/no-accents"

if not os.path.exists(path_no_accents):
    os.makedirs(path_no_accents)


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


def convert_book_no_accents(path, book):
    """
    Converts an individual book into Unicode (no accents).
    """
    # Opening the file
    with open(path, "r") as file:
        book_text = file.read()

    # Making each verse take only one line
    one_line_verses_list = make_one_verse_one_line(book_text)

    # Converting the text
    result = []
    for line in one_line_verses_list:
        chap, verse, clean_line = extract_verse_chapter(line)
        # beta_line = buc.standardise_beta_code(clean_line, False)
        unicode_line = buc.convert_asc_to_unicode(clean_line)
        result.append([chap, verse, unicode_line])
        # print("     ",chap, verse, beta_line, unicode_line)

    # Converting to DataFrame and fixing the table format
    result = pd.DataFrame(result)
    result = result.replace("", pd.NA).dropna()
    result.columns = ["chapter", "verse", "text"]
    result["chapter"] = result["chapter"].astype(int)
    result["verse"] = result["verse"].astype(int)

    save_to = path_no_accents + "/" + book + ".csv"
    result.to_csv(save_to, index=False)


def convert_all_books_to_unicode_no_accents(book_list):
    """
    Convenience function to convert all books in the same batch.
    """
    list_of_all_books = copy.deepcopy(book_list)

    for book in list_of_all_books:
        print("     Converting " + book + " (no accents)")
        path = "../textonly-online-bible/" + book + "05.ASC"
        converted_book = convert_book_no_accents(path=path, book=book)


######## Converting all books
print("CONVERTING ALL BOOKS (NO ACCENTS) - SAVING TO THE no-accents FOLDER")
convert_all_books_to_unicode_no_accents(book_list)
print("Done.")
print("\n---\n")
