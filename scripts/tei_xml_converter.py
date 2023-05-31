#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os

book_dict = {
    7: ["1CO", "First Corinthians"],
    23: ["1JO", "First John"],
    21: ["1PE", "First Peter"],
    13: ["1TH", "First Thessalonians"],
    15: ["1TI", "First Timothy"],
    8: ["2CO", "Second Corinthians"],
    24: ["2JO", "Second John"],
    22: ["2PE", "Second Peter"],
    14: ["2TH", "Second Thessalonians"],
    16: ["2TI", "Second Timoty"],
    25: ["3JO", "Third John"],
    5: ["ACT", "Acts"],
    12: ["COL", "Colossians"],
    10: ["EPH", "Ephesians"],
    9: ["GAL", "Galatians"],
    19: ["HEB", "Hebrews"],
    20: ["JAM", "James"],
    4: ["JOH", "John"],
    26: ["JUD", "Jude"],
    3: ["LUK", "Luke"],
    2: ["MAR", "Mark"],
    1: ["MAT", "Matthew"],
    18: ["PHM", "Philemon"],
    11: ["PHP", "Phillipians"],
    27: ["REV", "Revelation"],
    6: ["ROM", "Romans"],
    17: ["TIT", "Titus"],
}

# Creating the XML folders
path_no_accents_xml = "../tei-xml-unicode/no-accents"

# Defining the path where to find the CSVs
path_no_accents_csv = "../csv-unicode/strongs/no-parsing"

if not os.path.exists(path_no_accents_xml):
    os.makedirs(path_no_accents_xml)

if not os.path.exists(path_no_accents_xml + "/BYZ"):
    os.makedirs(path_no_accents_xml + "/BYZ")


def convert_verse(verse_text, book_id, chapter_id, verse_number):
    """
    Converts a verse to the TEX-XML format.
    """
    verse_prefix = (
        '\t\t\t\t\t<ab n="' + book_id + chapter_id + "V" + str(verse_number) + '">\n'
    )
    verse_suffix = "\n\t\t\t\t\t</ab>"

    verse_xml = []
    for word in verse_text.split(" "):
        verse_xml.append("\t\t\t\t\t\t<w>" + word + "</w>")

    verse_xml = "\n".join(verse_xml)
    verse_xml = verse_prefix + verse_xml + verse_suffix

    return verse_xml


def convert_chapter(book_df, book_id, chapter_number):
    """
    Converts an entire chapter of a given book to the TEI-XML format
    """
    chapter_df = book_df[book_df["chapter"] == chapter_number]
    chapter_id = "K" + str(chapter_number)
    chapter_prefix = '\t\t\t\t<div type="chapter" n="' + book_id + chapter_id + '">\n'
    chapter_suffix = "\n\t\t\t\t</div>"

    verse_list = chapter_df["verse"].unique()

    converted_verses = []
    for verse_number in verse_list:
        verse_text = chapter_df[chapter_df["verse"] == verse_number]["text"].iloc[0]
        converted_verses.append(
            convert_verse(verse_text, book_id, chapter_id, verse_number)
        )

    chapter_xml = "\n".join(converted_verses)

    chapter_xml = chapter_prefix + chapter_xml + chapter_suffix

    return chapter_xml


def convert_book(path, book_abbr, book_id):
    """
    Converts a given book to the TEI-XML format.
    """
    book_df = pd.read_csv(path)
    book_prefix = '\t\t\t<div type="book" n="' + book_id + '">\n'
    book_suffix = "\n\t\t\t</div>"

    chapter_list = book_df["chapter"].unique()

    converted_chapters = []
    for chapter_number in chapter_list:
        converted_chapters.append(convert_chapter(book_df, book_id, chapter_number))

    book_xml = "\n".join(converted_chapters)

    book_xml = book_prefix + book_xml + book_suffix
    return book_xml


def convert_byz(path_no_accents_csv):
    """
    Converts all books to the TEI-XML format.
    """
    byzantine_text = []
    for book_number in sorted(book_dict.keys()):
        path_to_csv_book = (
            path_no_accents_csv + "/" + book_dict[book_number][0] + ".csv"
        )
        book_id = "B" + str(book_number).zfill(2)
        byzantine_text.append(
            convert_book(path_to_csv_book, book_dict[book_number][0], book_id)
        )

    with open("tei_xml_header.xml", "r") as file:
        byzantine_text_prefix = file.read()

    byzantine_text_prefix = byzantine_text_prefix.replace(
        "BOOK_METADATA_PLACEHOLDER", ""
    )
    byzantine_text = "\n".join(byzantine_text)
    byzantine_text = (
        byzantine_text_prefix + byzantine_text + "\n\t\t</body>\n\t</text>\n</TEI>"
    )
    text_file = open(path_no_accents_xml + "/BYZ/byz.xml", "w")
    n = text_file.write(byzantine_text)
    text_file.close()


def convert_save_book_byz(path_no_accents_csv):
    """
    This function saves an XML file for each book.
    """
    for book_number in sorted(book_dict.keys()):
        path_to_csv_book = (
            path_no_accents_csv + "/" + book_dict[book_number][0] + ".csv"
        )
        book_id = "B" + str(book_number).zfill(2)
        book_byzantine_text = convert_book(
            path_to_csv_book, book_dict[book_number][0], book_id
        )

        book_metadata = """\n\t\t\t\t<title type="work" level="m" xml:lang="en" n="{}">{}</title>\n\t\t\t\t<title type="short" level="m" xml:lang="en" n="{}">{}</title>""".format(
            str(book_number).zfill(2),
            book_dict[book_number][1],
            str(book_number).zfill(2),
            book_dict[book_number][0],
        )
        with open("tei_xml_header.xml", "r") as file:
            book_byzantine_text_prefix = file.read()

        book_byzantine_text_prefix = book_byzantine_text_prefix.replace(
            "BOOK_METADATA_PLACEHOLDER", book_metadata
        )

        book_byzantine_text = (
            book_byzantine_text_prefix
            + book_byzantine_text
            + "\n\t\t</body>\n\t</text>\n</TEI>"
        )
        text_file = open(
            path_no_accents_xml + "/" + book_dict[book_number][0] + ".xml", "w"
        )
        n = text_file.write(book_byzantine_text)
        text_file.close()


convert_byz(path_no_accents_csv)
convert_save_book_byz(path_no_accents_csv)
print("Done!")
