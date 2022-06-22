# -*- coding: utf-8 -*-
import sys
import os
import re

book_list_OLB = [
    "MT", "MR", "LU", "JOH", "AC", "RO", "1CO", "2CO",
    "GA", "EPH", "PHP", "COL", "1TH", "2TH", "1TI", "2TI",
    "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JO", "2JO", "3JO",
    "JUDE", "RE"]

number_re = re.compile(r'^\d+$')

olb_word_r = r'[<>a-z]+'
olb_word_re = re.compile(r'^%s$' % olb_word_r)
tag_re = re.compile(r'^\{([A-Z123-]+)\}$')

chapter_colon_verse_re = re.compile(r'^(\d+):(\d+)$')
chapter_colon_verse_in_parentheses_re = re.compile(r'^\((\d+):(\d+)\)$')


def classify_token(token_list, index):
    if index >= len(token_list):
        return "EOF"

    s = token_list[index]

    if olb_word_re.match(s) != None:
        return "OLB_WORD"
    elif tag_re.match(s) != None:
        return "ROBINSON_TAG"
    elif number_re.match(s) != None:
        n = int(s)
        if n == 0:
            return "STRONGS_IS_SPURIOUS"
        elif n <= 5624:
            return "STRONGS_NUMBER"
        else:
            return "TVM_NUMBER"
    elif chapter_colon_verse_re.match(s):
        return "CHAPTER_VERSE"
    elif chapter_colon_verse_in_parentheses_re.match(s):
        return "CHAPTER_VERSE_IN_PARENTHESES"
    elif s == '|':
        return "PIPE"
    elif s == 'VAR:':
        return "VAR_COLON"
    elif s == ':END':
        return "COLON_END"
    elif s == 'M5:':
        return "M5_COLON"
    elif s == ':M5':
        return "COLON_M5"
    elif s == 'M6:':
        return "M6_COLON"
    elif s == ':M6':
        return "COLON_M6"
    elif s == 'OMIT':
        return "OMIT"
    else:
        raise Exception("ERROR: Could not classify token: '%s'" % s)

def eat_expected_token(tokens, index, expected_token_class):
    if classify_token(tokens, index) == expected_token_class:
        index += 1
        return index
    else:
        raise Exception("ERROR: Expected token class '%s' got class '%s' for token '%s'" % (expected_token_class, classify_token(tokens, index), tokens[index]))

class ParsedWord:
    def __init__(self):
        self.OLB_surface = None
        self.StrongsNumberIsNotRight = False
        self.StrongsNumber = None
        self.TVMNumber = None
        self.parsing = None

    def parse_tokens(self, tokens, index):
        bContinue = True
        while bContinue:
            token_class = classify_token(tokens, index)
            if token_class == "OLB_WORD":
                self.OLB_surface = tokens[index]
                index += 1
            elif token_class == "STRONGS_IS_SPURIOUS":
                self.StrongsNumberIsNotRight = True
                index += 1
            elif token_class == "STRONGS_NUMBER":
                self.StrongsNumber = tokens[index]
                index += 1
            elif token_class == "TVM_NUMBER":
                self.TVMNumber = tokens[index]
                index += 1
            elif token_class == "ROBINSON_TAG":
                tag_mo = tag_re.match(tokens[index])
                tag = tag_mo.group(1)
                self.parsing = tag
                index += 1
            else:
                bContinue = False
                break

        # index is now at the first non-parsed-word token
        return index

POSSIBLE_VARIANT_READING_KINDS = ["VAR", "M5", "M6"]

class VariantReading:
    def __init__(self):
        self.kind = None # VAR, M5, M6
        self.quoted_maintext = [] # list of ParsedWord
        self.var_is_OMIT = False
        self.variant_words = [] # List of ParsedWord

    def parse_tokens(self, tokens, index):
        
        XXX
        
        
class Variant:
    def __init__(self):
        self.maintext = [] # List of ParsedWord
        self.variant_readings = []

    def parse_tokens(self, tokens, index):
        index = eat_expected_token(tokens, index, "PIPE")
        index = self.parse_maintext_tokens(tokens, index)
        index = eat_expected_token(tokens, index, "PIPE")
        index = self.parse_variant_readings(tokens, index)
        index = eat_expected_token(tokens, index, "PIPE")


    def parse_maintext_tokens(self, tokens, index):
        while classify_token(tokens, index) == "OLB_WORD":
            parsed_word = ParsedWord()
            self.maintext.append(parsed_word)
            index = parsed_word.parse_tokens(tokens, index)
        return index

    def parse_variant_readings(self, tokens, index):
        token_class = classify_tokens(tokens, index)
        if token_class == "M5_COLON":
            index = eat_expected_token(tokens, index, "M5_COLON")
            index = self.parse_variant_reading(tokens, index)
            index = eat_expected_token(tokens, index, "COLON_M5")
            index = eat_expected_token(tokens, index, "M6_COLON")
            index = self.parse_variant_reading(tokens, index)
            index = eat_expected_token(tokens, index, "COLON_M6")
        elif token_class == "OLB_WORD":
            index = self.parse_variant_reading(tokens, index)
        else:
            assert False

        index = eat_expected_token(tokens, index, "PIPE")

        return index

    def parse_variant_reading(self, tokens, index):
        index = self.parse_quoted_maintext(tokens, index)
        index = self.parse_variant_words(tokens, index)
        
        index = eat_expected_token(tokens, index, variant_end_token)
    
        return index
    
    def read_parsed_word(self, tokens, index):
        parsed_word_obj = ParsedWord()
        self.verse_parts.append(parsed_word_obj)
        index = parsed_word_obj.parse_tokens(tokens, index)
        return index
    
    def parse_quoted_maintext(self, tokens, index):
        index = eat_expected_token(tokens, index, "PIPE")
        while classify_token(tokens, index) == "OLB_WORD":
            parsed_word = ParsedWord()
            self.maintext.append(parsed_word)
            index = parsed_word.parse_tokens(tokens, index)
        return index
    
    def parse_variant_words(self, tokens, index):
        if classify_token(tokens, index) == "OMIT":
            self.is_OMIT = True
            index += 1

        while classify_token(tokens, index) == "OLB_WORD":
            parsed_word = ParsedWord()
            self.maintext.append(parsed_word)
            index = parsed_word.parse_tokens(tokens, index)

        return index
        
class Verse:
    def __init__(self, chapter, verse):
        self.chapter = chapter
        self.verse = verse
        self.verse_parts = [] # ParsedWord | Variant

    def parse_tokens(self, tokens, index):
        while index < len(tokens):
            token_class = classify_token(tokens, index)
            if token_class == "OLB_WORD":
                index = self.read_parsed_word(tokens, index)
            elif token_class == "PIPE":
                index = self.read_variant(tokens, index)
            elif token_class == "CHAPTER_VERSE_IN_PARENTHESES":
                # @@@ FIXME: Do something with the parenthesized (chapter:verse)
                index += 1
            elif token_class == "CHAPTER_VERSE":
                # Return, for we have found the next chapter/verse
                break
            else:
                raise Exception("ERROR: I don't know how to deal with token_class '%s' for token '%s'." % (token_class, tokens[index]))

        return index
            

    def read_parsed_word(self, tokens, index):
        parsed_word_obj = ParsedWord()
        self.verse_parts.append(parsed_word_obj)
        index = parsed_word_obj.parse_tokens(tokens, index)
        return index

    def read_variant(self, tokens, index):
        variant_obj = Variant()
        self.verse_parts.append(variant_obj)
        index = variant_obj.parse_tokens(tokens, index)
        return index

    
class Book:
    def __init__(self, dirname, OLB_book, extension):
        self.dirname = dirname
        self.OLB_book = OLB_book
        self.extension = extension
        self.verse_dict = {} # chapter-int -> verse-number-int -> Verse-object
        self.cur_verse = None # Verse-object

    def read_book(self):
        filename = "%s/%s.%s" % (self.dirname, self.OLB_book, self.extension)

        sys.stderr.write("... Reading: %s\n" % filename)

        udoc = "".join(open(filename, "rb")).decode('utf-8')

        tokens = udoc.strip().split()

        sys.stderr.write("... Parsing: %s\n" % filename)

        self.parse_tokens(tokens)

        sys.stderr.write("... Done: %s\n\n" % filename)

    def parse_tokens(self, tokens):
        index = 0
        while index < len(tokens):
            token_class = classify_token(tokens, index)

            sys.stderr.write("UP200: token_class = '%s' token = '%s'\n" % (token_class, tokens[index]))
    
            
            if token_class == "CHAPTER_VERSE":
                self.create_verse(tokens, index)
                index += 1
            else:
                index = self.verse_obj.parse_tokens(tokens, index)


    def create_verse(self, tokens, index):
        ch_vs = tokens[index]
        ch_vs_mo = chapter_colon_verse_re.match(ch_vs)
        assert ch_vs_mo != None, "ERROR: chater_verse did not parse: '%s'" % ch_vs
        chapter_number = int(ch_vs_mo.group(1))
        verse_number = int(ch_vs_mo.group(2))

        self.verse_obj = Verse(chapter_number, verse_number)

        self.verse_dict.setdefault(chapter_number, {})
        assert verse_number not in self.verse_dict[chapter_number], "ERROR: %s %d:%d exists already" % (self.OLB_book, chapter_number, verse_number)
        self.verse_dict[chapter_number][verse_number] = self.verse_obj
        

class ParsedRobinsonReader:
    def __init__(self, dirname, extension):
        self.dirname = dirname
        self.extension = extension
        self.book_dict = {}

    def read_all_books(self):
        for OLB_book in book_list_OLB:
            self.read_book(OLB_book)

    def read_book(self, OLB_book):
        book_obj = Book(self.dirname, OLB_book, self.extension)
        book_obj.read_book()
        self.book_dict[OLB_book] = book_obj
        
        
if __name__ == '__main__':
    reader = ParsedRobinsonReader("../parsed", "UB5")
    reader.read_all_books()
    
