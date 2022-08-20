#!/usr/bin/env python
# coding: utf-8

# This file has been tested on Ubuntu 20.04 and Python 3.8
import beta_code
import re
import pandas as pd
import os
import beta_to_unicode_custom.beta_to_unicode_custom as buc

# Creating the CSV folders
if not os.path.exists('../csv-unicode/no-variants'):
    os.makedirs('../csv-unicode/no-variants')
    
if not os.path.exists('../csv-unicode/with-variants'):
    os.makedirs('../csv-unicode/with-variants')


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
        save_to = "../csv-unicode/no-variants/" + book + ".csv"
    else:
        save_to = "../csv-unicode/with-variants/" + book + ".csv"
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
