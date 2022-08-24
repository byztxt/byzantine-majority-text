# -*- coding: utf-8 -*-
# beta2GalatiaAndUnicode.py
#
# Version 2004-11-23 with changes by ulrikp 2005-03-19
#
# James Tauber
# http://jtauber.com/
#
# You are free to redistribute this, but please inform me of any errors
#
#
# Modified by Ulrik Sandborg-Petersen to do BETA to SIL Galatia as
# well as a number of other encodings.
#
# Ulrik has a website here, where contact details can be found:
# http://ulrikp.org
#
# SIL Galatia is a beautiful Greek font, freely available here:
# http://http://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&item_id=SILGrk_home
#
# Ulrik Sandborg-Petersen makes his changes available under the same
# conditions as James Tauber did above.
#
# USAGE:
#
# trie = beta2unicodeTrie()
# beta = "LO/GOS\n";
# unicode, remainder = trie.convert(beta)
#
# - to get final sigma, string must end in \n
# - remainder will contain rest of beta if not all can be converted
from __future__ import unicode_literals, print_function

import string
import re
import sys


#
# From:
# https://stackoverflow.com/questions/6628306/attributeerror-module-object-has-no-attribute-maketrans
#
try:
    maketrans = ''.maketrans
except AttributeError:
    # fallback for Python 2
    from string import maketrans


class Trie:
    def __init__(self):
        self.root = [None, {}]

    def add(self, key, value):
        curr_node = self.root
        for ch in key:
            curr_node = curr_node[1].setdefault(ch, [None, {}])
        curr_node[0] = value

    def find(self, key):
        curr_node = self.root
        for ch in key:
            try:
                curr_node = curr_node[1][ch]
            except KeyError:
                return None
        return curr_node[0]

    def findp(self, key):
        curr_node = self.root
        remainder = key
        for ch in key:
            try:
                curr_node = curr_node[1][ch]
            except KeyError:
                return (curr_node[0], remainder)
            remainder = remainder[1:]
        return (curr_node[0], remainder)

    def convert(self, keystring):
        valuestring = ""
        key = keystring
        while key:
            value, key = self.findp(key)
            if not value:
                return (valuestring, key)
            valuestring += value
        return (valuestring, key)

def beta2unicodeTrie():
    t = Trie()

    t.add("%2",      "\u002a") # Asterisk
    t.add("%13",     "\u2021") # Double Dagger
    t.add("%30",     "\u02bc") # Modifier Letter Apostrophe
    t.add("\"",      "\u201c")
    t.add("*A",      "\u0391")
    t.add("*B",      "\u0392")
    t.add("*G",      "\u0393")
    t.add("*D",      "\u0394")
    t.add("*E",      "\u0395")
    t.add("*Z",      "\u0396")
    t.add("*H",      "\u0397")
    t.add("*Q",      "\u0398")
    t.add("*I",      "\u0399")
    t.add("*K",      "\u039A")
    t.add("*L",      "\u039B")
    t.add("*M",      "\u039C")
    t.add("*N",      "\u039D")
    t.add("*C",      "\u039E")
    t.add("*O",      "\u039F")
    t.add("*P",      "\u03A0")
    t.add("*R",      "\u03A1")
    t.add("*S",      "\u03A3")
    t.add("*T",      "\u03A4")
    t.add("*U",      "\u03A5")
    t.add("*F",      "\u03A6")
    t.add("*X",      "\u03A7")
    t.add("*Y",      "\u03A8")
    t.add("*W",      "\u03A9")

    t.add("A",      "\u03B1")
    t.add("B",      "\u03B2")
    t.add("G",      "\u03B3")
    t.add("D",      "\u03B4")
    t.add("E",      "\u03B5")
    t.add("Z",      "\u03B6")
    t.add("H",      "\u03B7")
    t.add("Q",      "\u03B8")
    t.add("Q)",     "\u03B8\u2019") # Occurs in BDB Unabridged from Bible Soft, as KAQ) (KAQ'))
    t.add("I",      "\u03B9")
    t.add("K",      "\u03BA")
    t.add("L",      "\u03BB")
    t.add("M",      "\u03BC")
    t.add("M)",     "\u03BC\u2019") # Occurs in BDB Unabridged from Bible Soft, as *RAEM) (*RAEM')
    t.add("N",      "\u03BD")
    t.add("C",      "\u03BE")
    t.add("O",      "\u03BF")
    t.add("P",      "\u03C0")
    t.add("P)",     "\u03C0\u2019") # Occurs in BDB Unabridged from Bible Soft, as A)P) (A)P')
    t.add("R",      "\u03C1")

    t.add("J#17",    "\u03C2\u002F")
    t.add("S#17",    "\u03C2\u002F")
    t.add("S#30",    "\u03C2\u02bc")
    t.add("J\n",    "\u03C2")
    t.add("S\n",    "\u03C2")
    t.add("J ",     "\u03C2\u0020")
    t.add("S ",     "\u03C2\u0020")
    t.add("J'",     "\u03C2\u2019")
    t.add("S'",     "\u03C2\u2019")
    t.add("J,",     "\u03C2,")
    t.add("S,",     "\u03C2,")
    t.add("J!",     "\u03C2!")
    t.add("S!",     "\u03C2!")
    t.add("J.",     "\u03C2.")
    t.add("S.",     "\u03C2.")
    t.add("J:",     "\u03C2\u0387")
    t.add("S:",     "\u03C2\u0387")
    t.add("J;",     "\u03C2\u037E")
    t.add("S;",     "\u03C2\u037E")
    t.add("J]1",    "\u03C2)")  
    t.add("S]16",   "\u03C2\u27e7") # Double square brackets in one glyph
    t.add("S]1",    "\u03C2)")
    t.add("J]",     "\u03C2]")
    t.add("S]",     "\u03C2]")
    t.add("J[",     "\u03C2[")
    t.add("S[",     "\u03C2[")
    t.add("J[1",    "\u03C2(")
    t.add("S[1",    "\u03C2(")
    t.add("JS",     "\u03C2\u03C3")  # NOTE : This doesn't make sense, but it occurs in AGNT '81
    t.add("J@",     "\u03C2@")
    t.add("S@",     "\u03C2@")
    t.add("J_",     "\u03C2\u2014") # Sigma finalis + Em-dash
    t.add("S_",     "\u03C2\u2014") # Sigma finalis + Em-dash
    t.add("S",      "\u03C3")
    t.add("S)",     "\u03C3\u2019") # Occurs in BDB Unabridged from Bible Soft, as S) (S')

    t.add("T",      "\u03C4")
    t.add("T)",     "\u03C4\u2019") # Occurs in BDB Unabridged from Bible Soft, as KAT) (KAT'))
    t.add("U",      "\u03C5")
    t.add("F",      "\u03C6")
    t.add("F)",     "\u03C6\u2019") # Occurs in BDB Unabridged from Bible Soft, as E)F) (E)F')
    t.add("X",      "\u03C7")
    t.add("Y",      "\u03C8")
    t.add("W",      "\u03C9")

    t.add("I+",     "\u03CA")
    t.add("U+",     "\u03CB")

    t.add("A)",     "\u1F00")
    t.add("A(",     "\u1F01")
    t.add("A)\\",   "\u1F02")
    t.add("A(\\",   "\u1F03")
    t.add("A)/",    "\u1F04")
    t.add("A(/",    "\u1F05")
    t.add("E)",     "\u1F10")
    t.add("E(",     "\u1F11")
    t.add("E)\\",   "\u1F12")
    t.add("E(\\",   "\u1F13")
    t.add("E)/",    "\u1F14")
    t.add("E/)",    "\u1F14")
    t.add("E(/",    "\u1F15")
    t.add("H)",     "\u1F20")
    t.add("H(",     "\u1F21")
    t.add("H)\\",   "\u1F22")
    t.add("H\\)",   "\u1F22")
    t.add("H(\\",   "\u1F23")
    t.add("H)/",    "\u1F24")
    t.add("H(/",    "\u1F25")
    t.add("I)",     "\u1F30")
    t.add("I(",     "\u1F31")
    t.add("I)\\",   "\u1F32")
    t.add("I(\\",   "\u1F33")
    t.add("I)/",    "\u1F34")
    t.add("I(/",    "\u1F35")
    t.add("O)",     "\u1F40")
    t.add("O(",     "\u1F41")
    t.add("O)\\",   "\u1F42")
    t.add("O(\\",   "\u1F43")
    t.add("O)/",    "\u1F44")
    t.add("O/)",    "\u1F44")
    t.add("O(/",    "\u1F45")
    t.add("U)",     "\u1F50")
    t.add("U(",     "\u1F51")
    t.add("U)\\",   "\u1F52")
    t.add("U(\\",   "\u1F53")
    t.add("U)/",    "\u1F54")
    t.add("U(/",    "\u1F55")
    t.add("W)",     "\u1F60")
    t.add("W(",     "\u1F61")
    t.add("W)\\",   "\u1F62")
    t.add("W(\\",   "\u1F63")
    t.add("W)/",    "\u1F64")
    t.add("W(/",    "\u1F65")

    t.add("A)=",    "\u1F06")
    t.add("A(=",    "\u1F07")
    t.add("H)=",    "\u1F26")
    t.add("H(=",    "\u1F27")
    t.add("I)=",    "\u1F36")
    t.add("I(=",    "\u1F37")
    t.add("U)=",    "\u1F56")
    t.add("U(=",    "\u1F57")
    t.add("W)=",    "\u1F66")
    t.add("W(=",    "\u1F67")

    t.add("*A)",     "\u1F08")
    t.add("*)A",     "\u1F08")
    t.add(")*A",    "\u1F08")
    t.add("*A(",     "\u1F09")
    t.add("*(A",     "\u1F09")
    t.add("(*A",     "\u1F09")
    t.add("*)\\A",   "\u1F0A")
    t.add("*(\\A",   "\u1F0B")
    t.add("(\\*A",   "\u1F0B")
    t.add("*A)/",    "\u1F0C")
    t.add("*)/A",    "\u1F0C")
    t.add(")/*A",    "\u1F0C")
    t.add("*A(/",    "\u1F0D")
    t.add("*(/A",    "\u1F0D")
    t.add("*A)=",    "\u1F0E")
    t.add("*)=A",    "\u1F0E")
    t.add("*A(=",    "\u1F0F")
    t.add("*(=A",    "\u1F0F")
    t.add("(/|*A",   "\u1F0D\u0345")
    t.add("(/|*A",   "\u1F0D\u0345")
    t.add("*(/A|",   "\u1F0D\u0345")
    #
    t.add("*E)",     "\u1F18")
    t.add("*)E",     "\u1F18")
    t.add(")*E",     "\u1F18")
    t.add("*E(",     "\u1F19")
    t.add("*(E",     "\u1F19")
    t.add("(*E",     "\u1F19")
    t.add("*)\\E",   "\u1F1A")
    t.add(")\\*E",   "\u1F1A")
    t.add("*(\\E",   "\u1F1B")
    t.add("(\\*E",   "\u1F1B")
    t.add("*E)/",    "\u1F1C")
    t.add("*)/E",    "\u1F1C")
    t.add(")/*E",    "\u1F1C")
    t.add("*E(/",    "\u1F1D")
    t.add("*(/E",    "\u1F1D")

    t.add("*H)",     "\u1F28")
    t.add("*)H",     "\u1F28")
    t.add(")*H",     "\u1F28")
    t.add("*H(",     "\u1F29")
    t.add("*(H",     "\u1F29")
    t.add("(*H",     "\u1F29")
    t.add("*H)\\",   "\u1F2A")
    t.add(")\\*H",   "\u1F2A")
    t.add("*)\\H",   "\u1F2A")
    t.add("(\\*H",   "\u1F2B")
    t.add("*(\\H",   "\u1F2B")
    t.add(")/|*H",   "\u1F2C\u0345")
    t.add("*)/H|",   "\u1F2C\u0345")
    #
    t.add("*H)/",    "\u1F2C")
    t.add("*)/H",    "\u1F2C")
    t.add(")/*H",    "\u1F2C")
    t.add("*H(/",    "\u1F2D")
    t.add("*(/H",    "\u1F2D")
    #
    t.add("*)=H",    "\u1F2E")
    t.add("(=*H",    "\u1F2F")
    t.add("*(=H",    "\u1F2F")
    t.add("*I)",     "\u1F38")
    t.add("*)I",     "\u1F38")
    t.add(")*I",     "\u1F38")
    t.add("*I(",     "\u1F39")
    t.add("*(I",     "\u1F39")
    t.add("(*I",     "\u1F39")
    t.add("*I)\\",   "\u1F3A")
    t.add("*)\\I",   "\u1F3A")
    t.add("*I(/",    "\u1F3B")
    t.add("*(/I",    "\u1F3B")
    t.add("*I)/",    "\u1F3C")
    t.add("*)/I",    "\u1F3C")
    t.add("*I(/",    "\u1F3D")
    t.add("*(/I",    "\u1F3D")
    t.add("*I)=",    "\u1F3E")
    t.add("*)=I",    "\u1F3E")
    t.add("*I(=",    "\u1F3F")
    t.add("*(=I",    "\u1F3F")
    #
    t.add("*O)",     "\u1F48")
    t.add("*)O",     "\u1F48")
    t.add(")*O",     "\u1F48")
    t.add("*O(",     "\u1F49")
    t.add("*(O",     "\u1F49")
    #
    #
    t.add("*O)\\",   "\u1F4A")
    t.add("*)\\O",   "\u1F4A")
    t.add("*O(\\",   "\u1F4B")
    t.add("*(\\O",   "\u1F4B")
    t.add("*O)/",    "\u1F4C")
    t.add("*)/O",    "\u1F4C")
    t.add("*O(/",    "\u1F4D")
    t.add("*(/O",    "\u1F4D")
    #
    t.add("*U(",     "\u1F59")
    t.add("*(U",     "\u1F59")
    t.add("(*U",     "\u1F59")
    t.add("*U(\\",   "\u1F5B")
    t.add("*(\\U",   "\u1F5B")
    #
    t.add("*(/U",    "\u1F5D")
    t.add("*U(/",    "\u1F5D")
    #
    t.add("*(=U",    "\u1F5F")
    t.add("*U(=",    "\u1F5F")
    
    t.add("*W)",     "\u1F68")
    t.add("*)W",     "\u1F68")
    t.add(")*W",     "\u1F68")
    t.add("*W(",     "\u1F69")
    t.add("*(W",     "\u1F69")
    t.add("(*W",     "\u1F69")
    #
    #
    t.add("*W)\\",   "\u1F6A")
    t.add("*)\\W",   "\u1F6A")
    t.add("*W(\\",   "\u1F6B")
    t.add("*(\\W",   "\u1F6B")
    t.add("*W)/",    "\u1F6C")
    t.add("*)/W",    "\u1F6C")
    t.add("*W(/",    "\u1F6D")
    t.add("*(/W",    "\u1F6D")
    t.add("*W)=",    "\u1F6E")
    t.add("*)=W",    "\u1F6E")
    t.add("*W(=",    "\u1F6F")
    t.add("*(=W",    "\u1F6F")

    t.add("(=|*W",   "\u1F6F\u0345")
    t.add("*(=W|",   "\u1F6F\u0345")

    t.add("A\\",    "\u1F70")
    t.add("A/",     "\u1F71")
    t.add("E\\",    "\u1F72")
    t.add("E/",     "\u1F73")
    t.add("H\\",    "\u1F74")
    t.add("H/",     "\u1F75")
    t.add("I\\",    "\u1F76")
    t.add("I/",     "\u1F77")
    t.add("O\\",    "\u1F78")
    t.add("O/",     "\u1F79")
    t.add("U\\",    "\u1F7A")
    t.add("U/",     "\u1F7B")
    t.add("W\\",    "\u1F7C")
    t.add("W/",     "\u1F7D")

    t.add("A)/|",   "\u1F84")
    t.add("A|)/",   "\u1F84")
    t.add("A(/|",   "\u1F85")
    t.add("A|(/",   "\u1F85")
    t.add("A)=|",   "\u1F86")
    t.add("H)|",    "\u1F90")
    t.add("H(|",    "\u1F91")
    t.add("H)/|",   "\u1F94")
    t.add("H)=|",   "\u1F96")
    t.add("H(=|",   "\u1F97")
    t.add("W)|",    "\u1FA0")
    t.add("W|)",    "\u1FA0")
    t.add("W(=|",   "\u1FA7")

    t.add("A=",     "\u1FB6")
    t.add("H=",     "\u1FC6")
    t.add("I=",     "\u1FD6")
    t.add("U=",     "\u1FE6")
    t.add("W=",     "\u1FF6")

    t.add("I\\+",   "\u1FD2")
    t.add("I/+",    "\u1FD3")
    t.add("I+/",    "\u1FD3")
    t.add("U\\+",   "\u1FE2")
    t.add("U/+",    "\u1FE3")
    t.add("U+/",    "\u1FE3")

    t.add("A|",     "\u1FB3")
    t.add("A/|",    "\u1FB4")
    t.add("A|/",    "\u1FB4")
    t.add("H|",     "\u1FC3")
    t.add("H/|",    "\u1FC4")
    t.add("H|/",    "\u1FC4")
    t.add("W|",     "\u1FF3")
    t.add("W|/",    "\u1FF4")
    t.add("W/|",    "\u1FF4")

    t.add("A=|",    "\u1FB7")
    t.add("H=|",    "\u1FC7")
    t.add("H|=",    "\u1FC7")
    t.add("W=|",    "\u1FF7")
    t.add("W|=",    "\u1FF7")

    t.add("R(",     "\u1FE5")
    t.add("*R(",    "\u1FEC")
    t.add("*(R",    "\u1FEC")
    t.add("(*R",    "\u1FEC")

    t.add("R)",     "\u1FE4")
    t.add("*R)",    "\u03A1\u0313") # @@@
    t.add("*)R",    "\u03A1\u0313") # @@@
    t.add(")*R",    "\u03A1\u0313")


#    t.add("~",      "~")
#    t.add("-",      "-")
    
#    t.add("(null)", "(null)")
#    t.add("&", "&")
    
    t.add("0", "0")
    t.add("1", "1")
    t.add("2", "2")
    t.add("3", "3")
    t.add("4", "4")
    t.add("5", "5")
    t.add("6", "6")
    t.add("7", "7")
    t.add("8", "8")
    t.add("9", "9")
    
    t.add("@", "@")
    t.add("%3", "\u002f") # Solidus, "/"
    t.add("#17", "\u002f") # Solidus, "/"
    t.add("[80", "\u002f") # Solidus, "/"
    t.add("]80", "\u002f") # Solidus, "/"
    t.add("$", "$")
    
    t.add(" ", " ")
    
    t.add(".", ".")
    t.add(",", ",")
    t.add("#", "\u0374") # Kaira (numerical apostrophe)
    t.add("# ", "\u0374 ") # Kaira (numerical apostrophe)
    t.add("# \n", "\u0374 ") # Kaira (numerical apostrophe)
    t.add("%19", "\u2013") # En-dash
    t.add("'", "\u2019")
    t.add(":", "\u0387")
    t.add(";", "\u037e")
    t.add("_", "\u2014") # Em-dash
    t.add("-", "\u2010") # Hyphen
    t.add("!", "!")
    

    t.add("[", "[")
    t.add("]", "]")

    t.add("[1", "(")
    t.add("]1", ")")
    t.add("[16",u"\u27e6") # Double square bracket in one glyph - open
    t.add("]16",u"\u27e7") # Double square bracket in one glyph - close
    t.add("[1I]1",   "(I)")
    t.add("[1II]1",  "(II)")
    t.add("[11]1",   "(1)")
    t.add("[12]1",  "(2)")

    
    t.add("[2", "(")
    t.add("]2", ")")

    t.add("\n", "")

    t.add("*#2", "\u03da")  # GREEK (CAPITAL) LETTER STIGMA
    t.add("#2", "\u03db")   # GREEK SMALL LETTER STIGMA
    t.add("*V", "\u03dc")   # GREEK CAPITAL LETTER DIGAMMA
    t.add("V",  "\u03dd")   # GREEK SMALL LETTER DIGAMMA
    
    return t


def beta2SBLTransliterationTrie():
    t = Trie()

    t.add("\"",      "\u201c")
    t.add("\"",      "\u201d")
    t.add("%2",      "\u002a")  # Asterisk
    t.add("%13",     "\u2021") # Double Dagger
    t.add("%19",     "\u2013") # En-dash
    t.add("%30",     "\u02bc") # Modifier Letter Apostrophe
    t.add("*A",      "A")
    t.add("*B",      "B")
    t.add("*G*A*L*A*T*A*S",    "GALATAS")
    t.add("*G*G",    "NG")
    t.add("*G*H*S",  "GĒS")
    t.add("*G*K",    "NK")
    t.add("*G*C",    "NX")
    t.add("*G*X",    "NCH")
    t.add("*G",      "G")
    t.add("*D",      "D")
    t.add("*E",      "E")
    t.add("*EU)=",   "Eû")
    t.add("*EU)\\",  "Eù")
    t.add("*EU)/",   "Eú")
    t.add("*EU)",    "Eu")
    t.add("*EU(=",   "Heû")
    t.add("*EU(\\",  "Heù")
    t.add("*EU(/",   "Heú")
    t.add("*EU(",    "Heu")
    t.add("*E*F*E*S*I*O*U*S",    "EFESIOUS")
    t.add("*E*N",    "EN")
    t.add("*E*W*N",  "EŌN")
    t.add("*Z",      "Z")
    t.add("*H",      "Ē")
    t.add("*HU)/",   "Ēú")
    t.add("*HU)=",   "û")
    t.add("*HU)\\",  "Ēù")
    t.add("*HU)",    "Ēu")
    t.add("*Q",      "Th")
    t.add("*I",      "I")
    t.add("*I\n",    "I")
    t.add("*K",      "K")
    t.add("*L",      "L")
    t.add("*M",      "M")
    t.add("*N",      "N")
    t.add("*C",      "X")
    t.add("*O",      "O")
    t.add("*P",      "P")
    t.add("*R",      "R")
    t.add("*S",      "S")
    t.add("*S\n",    "S")
    t.add("*T",      "T")
    t.add("*A*U",    "AU") 
    t.add("*AU(=",    "HAû") 
    t.add("*AU(\\",    "HAù") 
    t.add("*A*B*U*L*W*N",    "ABYLŌN") 
    t.add("*A*G*N*W*S*T*W",    "AGNŌSTŌ")
    t.add("*A*Z*W*R*A*I*O*S",    "AZŌRAIOS")
    t.add("*A*P*O",  "APO")
    t.add("*A*Q*Q*A*I*O*N",  "ATHTHAION")
    t.add("*A*P*O*K*A*L*U*Y*I*S",  "APOKALYPSIS")
    t.add("*A*P*O*S*T*O*L*W*N",  "APOSTOLŌN")
    t.add("*A*P'",  "AP'")
    t.add("*A*I\n",  "AI")
    t.add("*A*I*W*N",  "AIŌN")
    t.add("*A*I*O*U*S",  "AIOUS")
    t.add("*A*I*S",  "AIS")
    t.add("*A*N*A*Q*E*M*A",  "ANATHEMA")
    t.add("*A*N*N*O*U",  "ANNOU")
    t.add("*A*N*N*H*N",  "ANNĒN")
    t.add("*A*N*H*S",  "ANĒS")
    t.add("*A*S*I*L*E*U*S",  "ASILEUS")
    t.add("*A*S*I*L*E*W*N",  "ASILEŌN")
    t.add("*A*S*X*A",  "ASCHA")
    t.add("*A*T*A",  "ATA")
    t.add("*A*T*E*L*Q*O*N*T*E*S",  "ATELTHONTES")
    t.add("*A*R*X*H",  "ARCHĒ")
    t.add("*A*R*K*O*N",  "ARKON")
    t.add("*A*K*A*R*I*O*I",  "AKARIOI")
    t.add("*A*K*W*B*O*S",  "AKŌBOS")
    t.add("*A*K*W*B*O*U",  "AKŌBOU")
    t.add("*A*C*E*I*S",  "AXEIS")
    t.add("*E*B*R*A*I*O*U*S",    "BRAIOUS") 
    t.add("*E*G*A*L*H",  "EGALĒ") 
    t.add("*E*G*E*N*E*T*O",  "EGENETO") 
    t.add("*E*L*U*G*M*A*T*W*N",  "ELYGMATŌN") 
    t.add("*E*U",    "EU")
    t.add("*E*S",    "ES")
    t.add("*E*R*A",    "ERA")
    t.add("*E*T*A",    "ETA")
    t.add("*E*T*E*I",    "ETEI")
    t.add("*E*T*R*O*N",    "ETRON")
    t.add("*E*T*R*O*S",    "ETROS")
    t.add("*E*T*R*O*U",    "ETROU")
    t.add("*E*W",    "EŌ")
    t.add("*E*O*R*T*H*S",    "HEORTĒS")
    t.add("*E*P*I*S*T*O*L*H",    "EPISTOLĒ")
    t.add("*E*P*E*I*D*H*P*E*R",    "EPEIDĒPER")
    t.add("*E*P*L*H*R*W*Q*H",    "EPLĒRŌTHĒ")
    t.add("*E*P*O*R*E*U*Q*H*S*A*N",    "EPOREUTHĒSAN")
    t.add("*E*S*B*U*T*E*R*O*S",    "ESBYTEROS")
    t.add("*E*S*T*I*N",    "ESTIN")
    t.add("*E*S*S*A*L*O*N*I*K*E*I*S",    "ESSALONIKEIS")
    t.add("*H*G*G*I*Z*E*N",    "ĒNGIZEN")
    t.add("*H*U",    "ĒU") 
    t.add("*H*N", "ĒN")
    t.add("*H*M*O*N*A", "ĒMONA")
    t.add("*H*M*E*R*A*I*S", "HĒMERAIS")
    t.add("*H*S\n", "ĒS")
    t.add("*H*S*O*U", "ĒSOU")
    t.add("*H*S*O*U]", "ĒSOU]")
    t.add("*H*S*O*U*S", "ĒSOUS")
    t.add("*H*S*I*O*U*S", "ĒSIOUS")
    t.add("*H*T*H*R", "ĒTĒR")
    t.add("*O*T*E",  "OTE")
    t.add("*O*L*L*O*I",    "OLLOI")
    t.add("*O*L*O*S*S*A*E*I*S",    "OLOSSAEIS")
    t.add("*O*L*U*M*E*R*W*S",    "OLYMERŌS")
    t.add("*O*L*U*T*R*O*P*W*S",    "OLYTROPŌS")
    t.add("*O*U",    "OU")
    t.add("*O*N",    "ON")
    t.add("*O*G*O*N",    "OGON")
    t.add("*O*Q*E*O*S",    "OTHEOS")
    t.add("*O*Q*E*O*N",    "OTHEON")
    t.add("*O*R*I*N*Q*I*O*U*S",    "ORINTHIOUS")
    t.add("*O*R*N*W*N",    "ORNŌN")
    t.add("*O*U*K*A*N",    "OUKAN")
    t.add("*O*U*D*A",    "OUDA")
    t.add("*O*U*D*A*S",    "OUDAS")
    t.add("*O*U*D*A*I*W*N",    "OUDAIŌN")
    t.add("*O*U*A*N*O*S",    "OUANOS")
    t.add("*O*U*T*O",    "OUTO")
    t.add("*O*U*T*O*S",    "HOUTOS")
    t.add("*O*S\n",  "OS")
    t.add("*O*S \n",  "OS ")
    t.add("*U*I",    "UI")
    t.add("*U*R*I*O*S",    "YRIOS")
    t.add("*U*R*I*W*N",    "YRIŌN")
    t.add("*AU",     "Au")
    t.add("*AU(/",   "HAú")
    t.add("*AU)",    "Au")
    t.add("*AU)/",   "Aú")
    t.add("*EU",     "Eu")
    t.add("*HU",     "Ēu")
    t.add("*OU)",    "Ou")
    t.add("*OU)/",   "Oú")
    t.add("*OU)\\",   "Où")
    t.add("*OU(/",   "HOú")
    t.add("*OU(\\",  "HOù")
    t.add("*OU(=",   "HOû")
    t.add("OU(\\",   "hoù")
    t.add("*OU",     "Ou")
    t.add("*UI",     "Ui")
    t.add("*UI(",     "HUi")
    t.add("*U",      "Y")
    t.add("*F",      "Ph")
    t.add("*X",      "Ch")
    t.add("*Y",      "Ps")
    t.add("*W",      "Ō")
    
    t.add("A",      "a")
    t.add("B",      "b")
    t.add("GG",     "ng")
    t.add("GK",     "nk")
    t.add("GC",     "nx")
    t.add("GX",     "nch")
    t.add("G",      "g")
    t.add("D",      "d")
    t.add("E",      "e")
    t.add("Z",      "z")
    t.add("H",      "ē")
    t.add("Q",      "th")
    t.add("AI",     "ai")
    t.add("EI",     "ei")
    t.add("HI",     "ēi")
    t.add("OI",     "oi")
    t.add("OI+",    "oï")
    t.add("OI\\+",  "oï")
    t.add("I",      "i")
    t.add("K",      "k")
    t.add("L",      "l")
    t.add("M",      "m")
    t.add("N",      "n")
    t.add("C",      "x")
    t.add("O",      "o")
    t.add("P",      "p")
    t.add("R",      "r")
    t.add("V",      "v")

    t.add("S\n",    "s")
    t.add("S ",     "s ")
    t.add("S'",     "s\u2019")
    t.add("S,",     "s,")
    t.add("S.",     "s.")
    t.add("S:",     "s\u0387")
    t.add("S;",     "s\u037E")
    t.add("S]1",    "s)")
    t.add("S]",     "s]")
    t.add("S@",     "s@")
    t.add("S_",     "s_")
    t.add("S",      "s")

    t.add("T",      "t")
    t.add("AU",     "au")
    t.add("EU",     "eu")
    t.add("HU",     "ēu")
    t.add("OU",     "ou")
    t.add("UI",     "ui")
    t.add("UI/",    "uí")
    t.add("UI/+",    "uï")
    t.add("UI\\",    "uì")
    t.add("UI=",    "uî")
    t.add("UI(",    "hui")
    t.add("U",      "y")
    t.add("F",      "ph")
    t.add("X",      "ch")
    t.add("Y",      "ps")
    t.add("W",      "ō")

    t.add("AI+",    "aï")
    t.add("AI\\+",  "aï")
    t.add("EI\\+",  "eï")
    t.add("EI+",    "eï")
    t.add("HI+",    "ēï")
    t.add("OI+",    "oï")
    t.add("UI+",    "uï")
    t.add("I+",     "ï")
    t.add("AU+",    "aÿ")
    t.add("EU+",    "eÿ")
    t.add("HU+",    "ēÿ")
    t.add("OU+",    "oÿ")
    t.add("U+",     "ÿ")

    t.add("A)",     "a")
    t.add("A)|",    "ai")
    t.add("A(",     "ha")
    t.add("A)\\",   "à")
    t.add("A(\\",   "hà")
    t.add("A)/",    "á")
    t.add("A(/",    "há")
    t.add("E)",     "e")
    t.add("E(",     "he")
    t.add("E)\\",   "è")
    t.add("E(\\",   "hè")
    t.add("E)/",    "é")
    t.add("E(/",    "hé")
    t.add("H)",     "ē")
    t.add("H(",     "hē")
    t.add("H)\\",   "ḕ")
    t.add("H(\\",   "hḕ")
    t.add("H)/",    "ḗ")
    t.add("H(/",    "hḗ")
    t.add("AI)",    "ai")
    t.add("EI)",    "ei")
    t.add("HI)",    "ēi")
    t.add("OI)",    "oi")
    t.add("I)",     "i")
    t.add("AI(",    "hai")
    t.add("EI(",    "hei")
    t.add("HI(",    "hēi")
    t.add("OI(",    "hoi")
    t.add("I(",     "hi")
    t.add("AI)\\",  "aì")
    t.add("EI)\\",  "eì")
    t.add("OI)\\",  "oì")
    t.add("I)\\",   "ì")
    t.add("AI(\\",  "haì")
    t.add("EI(\\",  "heì")
    t.add("HI(\\",  "hēì")
    t.add("OI(\\",  "hoì")
    t.add("I(\\",   "hì")
    t.add("AI)/",   "aí")
    t.add("EI)/",   "eí")
    t.add("HI)/",   "ēí")
    t.add("OI)/",   "oí")
    t.add("I)/",    "í")
    t.add("AI(/",   "haí")
    t.add("EI(/",   "heí")
    t.add("HI(/",   "hēí")
    t.add("OI(/",   "hoí")
    t.add("I(/",    "hí")
    t.add("O)",     "o")
    t.add("O(",     "ho")
    t.add("O)\\",   "ò")
    t.add("O(\\",   "hò")
    t.add("O)/",    "ó")
    t.add("O(/",    "hó")
    t.add("AU)",    "au")
    t.add("EU)",    "eu")
    t.add("HU)",    "ēu")
    t.add("OU)",    "ou")
    t.add("U)",     "y")
    t.add("U(I",    "hui")
    t.add("AU(",    "hau")
    t.add("EU(",    "heu")
    t.add("HU(",    "hēu")
    t.add("OU(",    "hou")
    t.add("U(",     "hy")
    t.add("AU)\\",  "aù")
    t.add("EU)\\",  "eù")
    t.add("HU)\\",  "ēù")
    t.add("OU)\\",  "où")
    t.add("U(\\",   "hỳ")
    t.add("AU)/",   "aú")
    t.add("EU)/",   "eú")
    t.add("HU)/",   "ēú")
    t.add("OU)/",   "oú")
    t.add("U)/",    "ý")
    t.add("AU(/",   "haú")
    t.add("AU(\\",   "haù")
    t.add("EU(/",   "heú")
    t.add("HU(/",   "hēú")
    t.add("OU(/",   "hoú")
    t.add("U(/",    "hý")
    t.add("W)",     "ō")
    t.add("W)/|",   "ōi")
    t.add("W)=|",   "ōi")
    t.add("W(",     "hō")

    t.add("W)\\",   "ṑ")
    t.add("W(\\",   "hṑ")
    t.add("W)/",    "ṓ")
    t.add("W(/",    "hṓ")

    t.add("A)=",    "â")
    t.add("A)=|",   "âi")
    t.add("A(=",    "hâ")
    t.add("H)=",    "ē") # FIXME: Should have cirum flex accent, ^ 
    t.add("H(=",    "hē") # FIXME: Should have cirum flex accent, ^ 
    t.add("AI)=",   "aî")
    t.add("EI)=",   "eî")
    t.add("HI)=",   "ēî")
    t.add("OI)=",   "oî")
    t.add("I)=",    "î")
    t.add("AI(=",   "haî")
    t.add("EI(=",   "heî")
    t.add("HI(=",   "hēî")
    t.add("OI(=",   "hoî")
    t.add("I(=",    "hî")
    t.add("AU)=",   "aû")
    t.add("EU)=",   "eû")
    t.add("HU)=",   "ēû")
    t.add("OU)=",   "oû")
    t.add("U)=",    "ŷ")
    t.add("AU(=",   "haû")
    t.add("EU(=",   "heû")
    t.add("HU(=",   "hēû")
    t.add("OU(=",   "hoû")
    t.add("U(=",    "hŷ")
    t.add("W)=",    "ō") # FIXME: Should have cirum flex accent, ^ 
    t.add("W(=",    "hō") # FIXME: Should have cirum flex accent, ^ 

    t.add("*A)",     "A")
    t.add("*)A",     "A")
    t.add("*A(",     "Ha")
    t.add("*(A",     "Ha")
    t.add("*(\A",    "Ha")
    t.add("*A)/",    "Á")
    t.add("*)/A",    "Á")
    t.add("*A(/",    "Há")
    t.add("*(/A",    "Há")
    t.add("*A)=",    "Â")
    t.add("*)=A",    "Â")
    t.add("*A(=",    "Hâ")
    t.add("*(=A",    "Hâ")
    t.add("(/|*A",   "Hai")
    t.add("*(/A|",   "Hai")
    #
    t.add("*E)",     "E")
    t.add("*)E",     "E")
    t.add("*E(",     "He")
    t.add("*(E",     "He")
    #
    t.add("*)\E",    "È")
    t.add("*(\E",    "Hè")
    t.add("*E)/",    "É")
    t.add("*)/E",    "É")
    t.add("*E(/",    "Hé")
    t.add("*(/E",    "Hé")

    t.add("*H)",     "Ē")
    t.add("*)H",     "Ē")
    t.add("*H(",     "Hē")
    t.add("*(H",     "Hē")
    t.add("*H)\\",   "Ḕ")
    t.add(")\\*H",   "Ḕ")
    t.add("*)\\H",   "Ḕ")
    t.add("(\\*H",   "Hḕ")
    t.add("*(\\H",   "Hḕ")
    t.add(")/|*H",   "Ḗi")
    #
    t.add("*H)/",    "Ḗ")
    t.add("*)/H",    "Ḗ")
    t.add("*H(/",    "Hḗ")
    t.add("*(/H",    "Hḗ")
    #
    t.add("*)=H",    "Ē") # FIXME
    t.add("(=*H",    "Hē")# FIXME
    t.add("*(=H",    "Hē")# FIXME
    #
    t.add("*I)",     "I")
    t.add("*)I",     "I")
    t.add("*I(",     "Hi")
    t.add("*(I",     "Hi")
    t.add("*I)\\",   "Hì")
    t.add("*)\\I",   "Hì")
    t.add("*I(/",    "Hí")
    t.add("*(/I",    "Hí")
    t.add("*I)/",    "Í")
    t.add("*)/I",    "Í")
    t.add("*I(/",    "Hí")
    t.add("*(/I",    "Hí")
    t.add("*I)=",    "Î")
    t.add("*)=I",    "Î")
    t.add("*I(=",    "Hî")
    t.add("*(=I",    "Hî")
    #
    t.add("*O)",     "O")
    t.add("*)O",     "O")
    t.add("*O(",     "Ho")
    t.add("*O( ",     "Ho")
    t.add("*(O",     "Ho")
    #
    #
    t.add("*O)\\",   "Ò")
    t.add("*)\\O",   "Ò")
    t.add("*O(\\",   "Hò")
    t.add("*(\\O",   "Hò")
    t.add("*O)/",    "Ó")
    t.add("*)/O",    "Ó")
    t.add("*O(/",    "Hó")
    t.add("*(/O",    "Hó")
    #
    t.add("*U(I",    "Hui")
    t.add("*U(*I",   "HUI")
    t.add("*U(",     "Hy")
    t.add("*(U",     "Hy")
    t.add("*U(\\",   "Hỳ")
    t.add("*(\\U",   "Hỳ")
    #
    t.add("*(/U",    "Hý")
    t.add("*U(/",    "Hý")
    
    #
    t.add("*(=U",    "Hŷ")
    t.add("*U(=",    "Hŷ")
    
    t.add("*W)",     "Ō")
    t.add("*)W",     "Ō")
    t.add("*W(",     "Hō")
    t.add("*(W",     "Hō")
    #
    #
    t.add("*W)\\",   "Ṑ")
    t.add("*)\\W",   "Ṑ")
    t.add("*W(\\",   "Hṑ")
    t.add("*(\\W",   "Hṑ")
    t.add("*W)/",    "Ṓ")
    t.add("*)/W",    "Ṓ")
    t.add("*W(/",    "Hṓ")
    t.add("*(/W",    "Hṓ")
    t.add("*W)=",    "Ō")  # FIXME: Add ^
    t.add("*)=W",    "Ō")  # FIXME: Add ^
    t.add("*W(=",    "Hō") # FIXME: Add ^
    t.add("*(=W",    "Hō") # FIXME: Add ^

    t.add("(=|*W",   "Hōi")

    t.add("A\\",    "à")
    t.add("A/",     "á")
    t.add("E\\",    "è")
    t.add("E/",     "é")
    t.add("H\\",    "ḕ")
    t.add("H/",     "ḗ")
    t.add("AI\\",   "aì")
    t.add("EI\\",   "eì")
    t.add("HI\\",   "ēì")
    t.add("OI\\",   "oì")
    t.add("I\\",    "ì")
    t.add("AI/",    "aí")
    t.add("EI/",    "eí")
    t.add("HI/",    "ēí")
    t.add("OI/",    "oí")
    t.add("I/",     "í")
    t.add("O\\",    "ò")
    t.add("O/",     "ó")
    t.add("AU\\",   "aù")
    t.add("EU\\",   "eù")
    t.add("HU\\",   "ēù")
    t.add("OU\\",   "où")
    t.add("U\\",    "ỳ")
    t.add("AU/",    "aú")
    t.add("EU/",    "eú")
    t.add("HU/",    "ēú")
    t.add("OU/",    "oú")
    t.add("U/",     "ý")
    t.add("AU/+",   "aÿ") # FIXME: Add '
    t.add("EU/+",   "eÿ") # FIXME: Add '
    t.add("HU/+",   "ēÿ") # FIXME: Add '
    t.add("OU/+",   "oÿ") # FIXME: Add '
    t.add("W\\",    "ṑ")
    t.add("W/",     "ṓ")

    t.add("A)/|",   "ái")
    t.add("A(/|",   "hái")
    t.add("H)|",    "ēi")
    t.add("H(|",    "hēi")
    t.add("H)/|",   "ḗi")
    t.add("H)=|",   "ēi") # FIXME: Add ^
    t.add("H(=|",   "hēi")
    t.add("W)|",    "ōi")
    t.add("W(=|",   "hōi") # FIXME: Add ^ 

    t.add("A=",     "â")
    t.add("H=",     "ē") # FIXME: Add ^
    t.add("AI=",    "aî")
    t.add("EI=",    "eî")
    t.add("HI=",    "ēî")
    t.add("OI=",    "oî")
    t.add("I=",     "î")
    t.add("AU=",    "aû")
    t.add("AU=+",   "aü")
    t.add("EU=",    "eû")
    t.add("HU=",    "ēû")
    t.add("OU=",    "oû")
    t.add("U=",     "ŷ")
    t.add("W=",     "ō") # FIXME: Add ^

    t.add("I\\+",   "ï") # FIXME: Add ` 
    t.add("AI/+",   "aḯ")
    t.add("EI/+",   "eḯ")
    t.add("HI/+",   "ēḯ")
    t.add("OI/+",   "oḯ")
    t.add("I/+",    "ḯ")
    t.add("AI+/",   "aḯ")
    t.add("EI+/",   "eḯ")
    t.add("HI+/",   "ēḯ")
    t.add("I+/",    "ḯ")
    t.add("AU\\+",  "aÿ") # FIXNE: Add `
    t.add("EU\\+",  "eÿ") # FIXME: Add `
    t.add("HU\\+",  "ēÿ") # FIXME: add `
    t.add("OU\\+",  "oÿ")
    t.add("U\\+",   "ÿ") # FIXME: Add `
    t.add("U/+",    "ÿ") # FIXME: Add '

    t.add("A|",     "ai")
    t.add("A/|",    "ái")
    t.add("H|",     "ēi")
    t.add("H/|",    "ḗi")
    t.add("W|",     "ōi")
    t.add("W|/",    "ṓi")
    t.add("W/|",    "ṓi")

    t.add("A=|",    "âi")
    t.add("H=|",    "ēi") # FIXME: Add ^
    t.add("W=|",    "ōi") # FIXME: Add ^

    t.add("R(",     "rh")
    t.add("*R(",    "Rh")
    t.add("*(R",    "Rh")

    t.add("R)",     "r")
    t.add("*R)",    "R")
    t.add("*)R",    "R")

    t.add("*V",     "V")

#    t.add("~",      "~")
#    t.add("-",      "-")
    
#    t.add("(null)", "(null)")
#    t.add("&", "&")
    
    t.add("0", "0")
    t.add("1", "1")
    t.add("2", "2")
    t.add("3", "3")
    t.add("4", "4")
    t.add("5", "5")
    t.add("6", "6")
    t.add("7", "7")
    t.add("8", "8")
    t.add("9", "9")
    
    t.add("@", "@")
    t.add("$", "$")
    
    t.add(" ", " ")
    
    t.add(".", ".")
    t.add(",", ",")
    t.add("#", "\u0374") # Kaira (numerical apostrophe)
    t.add("'", "\u2019")
    t.add(":", "\u0387")
    t.add(";", "\u037e")
    t.add("_", "_")
    t.add("-", "-")
    t.add("!", "!")
    

    t.add("[", "[")
    t.add("]", "]")

    t.add("[1", "(")
    t.add("]1", ")")
    t.add("[1I]1",   "(1)")
    t.add("[1II]1",  "(2)")

    
    t.add("[2", "<")
    t.add("]2", ">")

    t.add("\n", "")

    t.add("*#2", " Stigma")  # GREEK (CAPITAL) LETTER STIGMA
    t.add("#2", " stigma")   # GREEK SMALL LETTER STIGMA
    
    return t


def beta2GalatiaTrie():
    t = Trie()

    t.add("*A",      "A")
    t.add("*B",      "B")
    t.add("*G",      "G")
    t.add("*D",      "D")
    t.add("*E",      "E")
    t.add("*Z",      "Z")
    t.add("*H",      "J")
    t.add("*Q",      "Q")
    t.add("*I",      "I")
    t.add("*K",      "K")
    t.add("*L",      "L")
    t.add("*M",      "M")
    t.add("*N",      "N")
    t.add("*C",      "X")
    t.add("*O",      "O")
    t.add("*P",      "P")
    t.add("*R",      "R")
    t.add("*S",      "S")
    t.add("*T",      "T")
    t.add("*U",      "U")
    t.add("*F",      "F")
    t.add("*X",      "C")
    t.add("*Y",      "Y")
    t.add("*W",      "W")

    t.add("A",      "a")
    t.add("B",      "b")
    t.add("G",      "g")
    t.add("D",      "d")
    t.add("E",      "e")
    t.add("Z",      "z")
    t.add("H",      "j")
    t.add("Q",      "q")
    t.add("I",      "i")
    t.add("K",      "k")
    t.add("L",      "l")
    t.add("M",      "m")
    t.add("N",      "n")
    t.add("C",      "x")
    t.add("O",      "o")
    t.add("P",      "p")
    t.add("R",      "r")

    t.add("S\n",    "v")
    t.add("S,",     "v,")
    t.add("S'",     "v'")
    t.add("S@",     "v@")
    t.add("S.",     "v.")
    t.add("S:",     "v:")
    t.add("S;",     "v;")
    t.add("S]1",    "v)")
    t.add("S]",     "v]")
    t.add("S",      "s")

    t.add("T",      "t")
    t.add("U",      "u")
    t.add("F",      "f")
    t.add("X",      "c")
    t.add("Y",      "y")
    t.add("W",      "w")

    t.add("I+",     "\xbb")
    t.add("U+",     "\xcb")

    t.add("A)",     "\x87")
    t.add("A(",     "\x83")
    t.add("A)\\",   "\x89")
    t.add("A(\\",   "\x85")
    t.add("A)/",    "\x88")
    t.add("A(/",    "\x84")
    t.add("E)",     "\x9d")
    t.add("E(",     "\x9b")
    t.add("E(\\",   "\x9f")
    t.add("E)/",    "\x9e")
    t.add("E(/",    "\x9c")
    t.add("H)",     "\xd7")
    t.add("H(",     "\xd3")
    t.add("H)\\",   "\xd9")
    t.add("H(\\",   "\xd5")
    t.add("H)/",    "\xd8")
    t.add("H(/",    "\xd4")
    t.add("I)",     "\xb8")
    t.add("I(",     "\xb3")
    t.add("I(\\",   "\xbe")
    #t.add("I)\\",   "i\xae")    # NOTE: This is a hack! iota + smooth-grave...
    t.add("I)/",    "\xb9")
    t.add("I(/",    "\xb4")
    t.add("O)",     "\xec")
    t.add("O(",     "\xe9")
    t.add("O)\\",   "\xce")
    t.add("O(\\",   "\xeb")
    t.add("O)/",    "\xed")
    t.add("O(/",    "\xea")
    t.add("U)",     "\xc7")
    t.add("U(",     "\xc3")
    t.add("U)\\",   "\xc9")
    t.add("U(\\",   "\xc5")
    t.add("U)/",    "\xc8")
    t.add("U(/",    "\xc4")
    t.add("W)",     "\xf7")
    t.add("W(",     "\xf3")
    t.add("W)\\",   "\xf9")
    t.add("W(\\",   "\xf5")
    t.add("W)/",    "\xf8")
    t.add("W(/",    "\xf4")

    t.add("A)=",    "\x8a")
    t.add("A(=",    "\x86")
    t.add("H)=",    "\xda")
    t.add("H(=",    "\xd6")
    t.add("I)=",    "\xba")
    t.add("I(=",    "\xb5")
    t.add("U)=",    "\xca")
    t.add("U(=",    "\xc6")
    t.add("W)=",    "\xfa")
    t.add("W(=",    "\xf6")

    t.add("*A)",     "HA")
    t.add("*)A",     "HA")
    t.add("*A(",     "hA")
    t.add("*(A",     "hA")
    #
    t.add("*(\\A",   "\xaaA")
    t.add("*A)/",    "\xadA")
    t.add("*)/A",    "\xadA")
    t.add("*A(/",    "\xa9A")
    t.add("*(/A",    "\xa9A")

    #
    t.add("*E)",     "HE")
    t.add("*)E",     "HE")
    t.add("*E(",     "hE")
    t.add("*(E",     "hE")
    #
    t.add("*(\\E",   "\xaaE")
    t.add("*E)/",    "\xadE")
    t.add("*)/E",    "\xadE")
    t.add("*E(/",    "\xa9E")
    t.add("*(/E",    "\xa9E")

    t.add("*H)",     "HJ")
    t.add("*)H",     "HJ")
    t.add("*H(",     "hJ")
    t.add("*(H",     "hJ")

    #
    t.add("*H)\\",   "\xaeJ")
    t.add(")\\*H",   "\xaeJ")
    t.add("*)\\H",   "\xaeJ")
    #
    t.add("*H)/",    "\xadJ")
    t.add("*)/H",    "\xadJ")
    #
    t.add("*)=H",    "\xafJ")
    t.add("(/*H",    "\xa9J")
    t.add("*(/H",    "\xa9J")

    #
    t.add("*I)",     "HI")
    t.add("*)I",     "HI")
    t.add("*I(",     "hI")
    t.add("*(I",     "hI")
    #
    #
    t.add("*I)/",    "\xadI")
    t.add("*)/I",    "\xadI")
    t.add("*I(/",    "\xa9I")
    t.add("*(/I",    "\xa9I")
    #
    t.add("*O)",     "HO")
    t.add("*)O",     "HO")
    t.add("*O(",     "hO")
    t.add("*(O",     "hO")

    #
    t.add("*(\\O",   "\xaaO")
    t.add("*O)/",    "\xadO")
    t.add("*)/O",    "\xadO")
    t.add("*O(/",    "\xa9O")
    t.add("*(/O",    "\xa9O")

    #
    t.add("*)U",     "HU")
    t.add("*U)",     "HU")
    t.add("*(U",     "hU")
    t.add("*U(",     "hU")
    #
    t.add("*(/U",    "\xa9U")
    t.add("*U(/",    "\xa9U")
    #
    t.add("*(=U",    "\xabU")
    t.add("*U(=",    "\xabU")
    
    t.add("*W)",     "HW")
    t.add("*)W",     "HW")
    t.add("*W(",     "hW")
    t.add("*(W",     "hW")
    #
    #
    t.add("*W)/",    "\xadW")
    t.add("*)/W",    "\xadW")
    t.add("*W(/",    "\xa9W")
    t.add("*(/W",    "\xa9W")

    t.add("*A)=",    "\xafA")
    t.add("*)=A",    "\xafA")
    t.add("*A(=",    "\xabA")
    t.add("*W)=",    "\xafW")
    t.add("*)=W",    "\xafW")
    t.add("*W(=",    "\xabW")
    t.add("*(=W",    "\xabW")

    t.add("A\\",    "\x81")
    t.add("A/",     "\x80")
    t.add("E\\",    "\x9a")
    t.add("E/",     "\x99")
    t.add("H\\",    "\xd1")
    t.add("H/",     "\xd0")
    t.add("I\\",    "\xb1")
    t.add("I/",     "\xb0")
    t.add("O\\",    "\xe8")
    t.add("O/",     "\xe7")
    t.add("U\\",    "\xc1")
    t.add("U/",     "\xc0")
    t.add("W\\",    "\xf1")
    t.add("W/",     "\xf0")

    t.add("A(/|",   "\x90")
    t.add("A(=|",   "\x92")
    t.add("A(\\|",  "\x91")
    t.add("A(|",    "\x8f")
    t.add("A)|",    "\x93")
    t.add("A)/|",   "\x94")
    t.add("A)=|",   "\x98")
    t.add("A)\\|",  "\x95")
    t.add("H)|",    "\xe3")
    t.add("H(|",    "\xdf")
    t.add("H)/|",   "\xe4")
    t.add("H)=|",   "\xe6")
    t.add("H)\\|",  "\xe5")
    t.add("H(/|",   "\xe0")
    t.add("H(=|",   "\xe2")
    t.add("H(\\|",  "\xe1")
    t.add("W)|",    "\xa5")
    t.add("W(/|",   "\xa1")
    t.add("W(=|",   "\xa3")
    t.add("W(\\|",  "\xa2")
    t.add("W)/|",   "\xa6")
    t.add("W)=|",   "\xa8")
    t.add("W)\\|",  "\xa7")

    t.add("A=",     "\x82")
    t.add("H=",     "\xd2")
    t.add("I=",     "\xb2")
    t.add("U=",     "\xc2")
    t.add("W=",     "\xf2")

    t.add("I\\+",   "\xbd")
    t.add("I+\\",   "\xbd")
    t.add("I/+",    "\xbc")
    t.add("I+/",    "\xbc")
    t.add("U\\+",   "\xcd")
    t.add("U+\\",   "\xcd")
    t.add("U/+",    "\xcc")
    t.add("U+/",    "\xcc")

    t.add("A|",     "\x8b")
    t.add("A/|",    "\x8c")
    t.add("A\\|",   "\x8d")
    t.add("H|",     "\xdb")
    t.add("H/|",    "\xdc")
    t.add("H\\|",   "\xdd")
    t.add("W|",     "\xfb")
    t.add("W/|",    "\xfc")
    t.add("W|/",    "\xfc")
    t.add("W\\|",   "\xfd")
    t.add("W|\\",   "\xfd")

    t.add("A=|",    "\x8e")
    t.add("H=|",    "\xde")
    t.add("W=|",    "\xfe")

    t.add("R(",     "\xbf")
    t.add("*R(",    "hR")
    t.add("*(R",    "hR")

    t.add("R)",     "\xcf")
    t.add("*R)",    "HR")
    t.add("*)R",    "HR")

#    t.add("~",      "~")
#    t.add("-",      "-")
    
#    t.add("(null)", "(null)")
#    t.add("&", "&")
    
    t.add("0", "0")
    t.add("1", "1")
    t.add("2", "2")
    t.add("3", "3")
    t.add("4", "4")
    t.add("5", "5")
    t.add("6", "6")
    t.add("7", "7")
    t.add("8", "8")
    t.add("9", "9")
    
    t.add("@", "@")
    t.add("$", "$")
    
    t.add(" ", " ")
    
    t.add(".", ".")
    t.add(",", ",")
    t.add("'", "'")
    t.add("#", "'") # FIXME: Kaira (numerical apostrophical marker) should not be simply '
    t.add(":", ":")
    t.add(";", ";")
    t.add("_", "_")
    t.add("-", "-")

    t.add("[", "[")
    t.add("]", "]")

    t.add("[1", "(")
    t.add("]1", ")")
    
    t.add("[2", "<")
    t.add("]2", ">")
    t.add("!", "!")
    
    t.add("\n", "")

    t.add("*#2", "v")  # GREEK (CAPITAL) LETTER STIGMA  # FIXME: This is not supposed to be final sigma, but there is no stigma in Galatia.
    t.add("#2", "v")   # GREEK SMALL LETTER STIGMA  # FIXME: This is not supposed to be final sigma, but there is no stigma in Galatia.

    
    return t


def galatia2BetaTrie():
    t = Trie()

    t.add("A",      "*A")
    t.add("B",      "*B")
    t.add("G",      "*G")
    t.add("D",      "*D")
    t.add("E",      "*E")
    t.add("Z",      "*Z")
    t.add("J",      "*H")
    t.add("Q",      "*Q")
    t.add("I",      "*I")
    t.add("K",      "*K")
    t.add("L",      "*L")
    t.add("M",      "*M")
    t.add("N",      "*N")
    t.add("X",      "*C")
    t.add("O",      "*O")
    t.add("P",      "*P")
    t.add("R",      "*R")
    t.add("S",      "*S")
    t.add("T",      "*T")
    t.add("U",      "*U")
    t.add("F",      "*F")
    t.add("C",      "*X")
    t.add("Y",      "*Y")
    t.add("W",      "*W")

    t.add("a",      "A")
    t.add("b",      "B")
    t.add("g",      "G")
    t.add("d",      "D")
    t.add("e",      "E")
    t.add("z",      "Z")
    t.add("j",      "H")
    t.add("q",      "Q")
    t.add("i",      "I")
    t.add("k",      "K")
    t.add("l",      "L")
    t.add("m",      "M")
    t.add("n",      "N")
    t.add("x",      "C")
    t.add("o",      "O")
    t.add("p",      "P")
    t.add("r",      "R")

    t.add("v/",     "J#17")
    t.add("v\n",    "S")
    t.add("v,",     "S,")
    t.add("v'",     "S'") # Sigma Finalis + Apostrophe
    t.add("v@",     "S'") # Sigma Finalis + Apostrophe
    t.add("v.",     "S.")
    t.add("v:",     "S:")
    t.add("v;",     "S;")
    t.add("v)",     "S]1")
    t.add("v]",     "S]")
    t.add("s",      "S")

    t.add("t",      "T")
    t.add("u",      "U")
    t.add("f",      "F")
    t.add("c",      "X")
    t.add("y",      "Y")
    t.add("w",      "W")

    t.add("HA",     "*)A")
    t.add("hA",     "*(A")

    #
    t.add("HE",     "*)E")
    t.add("hE",     "*(E")

    #
    t.add("HJ",     "*)H")
    t.add("hJ",     "*(H")

    #
    t.add("HI",     "*)I")
    t.add("hI",     "*(I")
    t.add("HO",     "*)O")
    t.add("hO",     "*(O")

    #
    t.add("HU",     "*)U")
    t.add("hU",     "*(U")
    #
    
    t.add("HW",     "*)W")
    t.add("hW",     "*(W")

    #
    t.add("hR",     "*(R")
    t.add("HR",     "*)R")

    t.add("\x80",     "A/")
    t.add("\x81",     "A\\")
    t.add("\x82",     "A=")
    t.add("\x83",     "A(")
    t.add("\x84",     "A(/")
    t.add("\x85",     "A(\\")
    t.add("\x86",     "A(=")
    t.add("\x87",     "A)")
    t.add("\x88",     "A)/")
    t.add("\x89",     "A)\\")
    t.add("\x8a",     "A)=")
    t.add("\x8b",     "A|")
    t.add("\x8c",     "A/|")
    t.add("\x8d",     "A\\|")
    t.add("\x8e",     "A=|")
    t.add("\x8f",     "A(|")
    t.add("\x90",     "A(/|")
    t.add("\x91",     "A(\\|")
    t.add("\x92",     "A(=|")
    t.add("\x93",     "A)|")
    t.add("\x94",     "A)/|")
    t.add("\x95",     "A)\\|")
    #t.add("\x96,"     "???")  # n-dash --
    #t.add("\x97,"     "???")  # m-dash ---
    t.add("\x98",     "A)=|")
    t.add("\x99",     "E/")
    t.add("\x9a",     "E\\")
    t.add("\x9b",     "E(")
    t.add("\x9c",     "E(/")
    t.add("\x9d",     "E)")
    t.add("\x9e",     "E)/")
    t.add("\x9f",     "E(\\")
    t.add("\xa1",     "W(/|")
    t.add("\xa2",     "W(\\|")
    t.add("\xa3",     "W(=|")
    t.add("\xa5",     "W)|")
    t.add("\xa6",     "W)/|")
    t.add("\xa7",     "W)\\|")
    t.add("\xa8",     "W)=|")
    t.add("\xa9A",    "*(/A")
    t.add("\xa9E",    "*(/E")
    t.add("\xa9I",    "*(/I")
    t.add("\xa9J",    "*(/H")
    t.add("\xa9O",    "*(/O")
    t.add("\xa9U",    "*(/U")
    t.add("\xa9W",    "*(/W")
    t.add("\xaaA",    "*(\\A")
    t.add("\xaaE",    "*(\\E")
    t.add("\xaaI",    "*(\\I")
    t.add("\xaaJ",    "*(\\H")
    t.add("\xaaO",    "*(\\O")
    t.add("\xaaU",    "*(\\U")
    t.add("\xaaW",    "*(\\W")
    t.add("\xabA",    "*(=A")
    t.add("\xabE",    "*(=E")
    t.add("\xabI",    "*(=I")
    t.add("\xabJ",    "*(=H")
    t.add("\xabO",    "*(=O")
    t.add("\xabU",    "*(=U")
    t.add("\xabW",    "*(=W")
    t.add("\xadA",    "*)/A")
    t.add("\xadE",    "*)/E")
    t.add("\xadI",    "*)/I")
    t.add("\xadJ",    "*)/H")
    t.add("\xadO",    "*)/O")
    t.add("\xadW",    "*)/W")
    t.add("\xaeA",    "*)\\A")
    t.add("\xaeE",    "*)\\E")
    t.add("\xaeI",    "*)\\I")
    t.add("\xaeJ",    "*)\\H")
    t.add("\xaeO",    "*)\\O")
    t.add("\xaeU",    "*)\\U")
    t.add("\xaeW",    "*)\\W")
    t.add("\xafA",    "*)=A")
    t.add("\xafJ",    "*)=H")
    t.add("\xafW",    "*)=W")
    t.add("\xb0",     "I/")
    t.add("\xb1",     "I\\")
    t.add("\xb2",     "I=")
    t.add("\xb3",     "I(")
    t.add("\xb4",     "I(/")
    t.add("\xb5",     "I(=")
    t.add("\xb8",     "I)")
    t.add("\xb9",     "I)/")
    t.add("\xba",     "I)=")
    t.add("\xbb",     "I+")
    t.add("\xbc",     "I/+")
    t.add("\xbd",     "I\\+")
    t.add("\xbe",     "I(\\")
    t.add("\xbf",     "R(")
    t.add("\xc0",     "U/")
    t.add("\xc1",     "U\\")
    t.add("\xc2",     "U=")
    t.add("\xc3",     "U(")
    t.add("\xc4",     "U(/")
    t.add("\xc5",     "U(\\")
    t.add("\xc6",     "U(=")
    t.add("\xc7",     "U)")
    t.add("\xc8",     "U)/")
    t.add("\xc9",     "U)\\")
    t.add("\xca",     "U)=")
    t.add("\xcb",     "U+")
    t.add("\xcc",     "U/+")
    t.add("\xcd",     "U\\+")
    t.add("\xce",     "O)\\")
    t.add("\xcf",     "R)")
    t.add("\xd0",     "H/")
    t.add("\xd1",     "H\\")
    t.add("\xd2",     "H=")
    t.add("\xd3",     "H(")
    t.add("\xd4",     "H(/")
    t.add("\xd5",     "H(\\")
    t.add("\xd6",     "H(=")
    t.add("\xd7",     "H)")
    t.add("\xd8",     "H)/")
    t.add("\xd9",     "H)\\")
    t.add("\xda",     "H)=")
    t.add("\xdb",     "H|")
    t.add("\xdc",     "H/|")
    t.add("\xdd",     "H\\|")
    t.add("\xde",     "H=|")
    t.add("\xdf",     "H(|")
    t.add("\xe0",     "H(/|")
    t.add("\xe1",     "H(\\|")
    t.add("\xe2",     "H(=|")
    t.add("\xe3",     "H)|")
    t.add("\xe4",     "H)/|")
    t.add("\xe5",     "H)\\|")
    t.add("\xe6",     "H)=|")
    t.add("\xe7",     "O/")
    t.add("\xe8",     "O\\")
    t.add("\xe9",     "O(")
    t.add("\xea",     "O(/")
    t.add("\xeb",     "O(\\")
    t.add("\xec",     "O)")
    t.add("\xed",     "O)/")
    t.add("\xf0",     "W/")
    t.add("\xf1",     "W\\")
    t.add("\xf2",     "W=")
    t.add("\xf3",     "W(")
    t.add("\xf4",     "W(/")
    t.add("\xf5",     "W(\\")
    t.add("\xf6",     "W(=")
    t.add("\xf7",     "W)")
    t.add("\xf8",     "W)/")
    t.add("\xf9",     "W)\\")
    t.add("\xfa",     "W)=")
    t.add("\xfb",     "W|")
    t.add("\xfc",     "W/|")
    t.add("\xfd",     "W\\|")
    t.add("\xfe",     "W=|")
    t.add("\xff",     "W(|")


#    t.add("~",      "~")
#    t.add("-",      "-")
    
#    t.add("(null, "(null)")")
#    t.add("&", "&")
    
    t.add("0", "0")
    t.add("1", "1")
    t.add("2", "2")
    t.add("3", "3")
    t.add("4", "4")
    t.add("5", "5")
    t.add("6", "6")
    t.add("7", "7")
    t.add("8", "8")
    t.add("9", "9")

    t.add("/", "#17") # Solidus / Obelus, "/"
    
    t.add("@", "'") # apostrophe
    t.add("$", "$")
    
    t.add(" ", " ")
    
    t.add(".", ".")
    t.add(",", ",")
    t.add("'", "'")  # apostrophe

    t.add(":", ":")
    t.add(";", ";")
    t.add("_", "_")
    t.add("-", "-")

    t.add("[", "[")
    t.add("]", "]")

    t.add("(", "[1")
    t.add(")", "]1")
    
    t.add("<", "[2")
    t.add(">", "]2")
    t.add("!", "!")
    
    t.add("\n", "")

    return t


def symbol2BetaTrie():
    t = Trie()

    t.add(u"\uf04a",      "*F")
    t.add(u"\uf050",      "*P")


    t.add(u"\uf061",      "A")
    t.add(u"\uf062",      "B")
    t.add(u"\uf067",      "G")
    t.add(u"\uf064",      "D")
    t.add(u"\uf065",      "E")
    t.add(u"\uf07a",      "Z")
    t.add(u"\uf068",      "H")
    t.add(u"\uf071",      "Q")
    t.add(u"\uf069",      "I")
    t.add(u"\uf06b",      "K")
    t.add(u"\uf06c",      "L")
    t.add(u"\uf06d",      "M")
    t.add(u"\uf06e",      "N")
    t.add(u"\uf078",      "C")
    t.add(u"\uf06f",      "O")
    t.add(u"\uf070",      "P")
    t.add(u"\uf072",      "R")

    t.add(u"\uf056",      "S") # Final sigma
    t.add(u"\uf056",      "S") # Final sigma
    t.add(u"\uf073",      "S")
    t.add(u"\uf073",      "S")

    t.add(u"\uf074",      "T")
    t.add(u"\uf075",      "U")
    t.add(u"\uf066",      "F") # Alternate phi
    t.add(u"\uf06a",      "F") # Real phi
    t.add(u"\uf063",      "X")
    t.add(u"\uf079",      "Y")
    t.add(u"\uf077",      "W")

    t.add(u"\uf020",      " ")
    t.add(u"\uf02c",      ",")
    t.add(u"\uf02d",      "-")
    t.add(u"(",           "[1")
    t.add(u")",           "]1")

    t.add(u"?",      "###?###")
    t.add(u"s",      "###s###")
    t.add(u"p",      "###p###")

  
    t.add(u"\n", "")

    return t




#t = beta2unicodeTrie()

#import sys

#for line in file(sys.argv[1]):
#    a, b = t.convert(line)
#    if b:
#        print a.encode("utf-8"), b
#        raise Exception
#    print(a.encode("utf-8"))

def unicode2BetaTrie():
    t = Trie()

    t.add(u"\n",        "")

    t.add(u"\u02bc",    "%30") # Modifier Letter Apostrophe
    t.add(u"\u2021",    "%13") # Double Dagger
    t.add(u"\u00b4",    "'")
    t.add(u"\u201c",    "\"")
    t.add(u"\u201d",    "\"")
    t.add(u"\u2003",    " ")
    t.add(u"\u002d",    "-") # Normal hyphen
    t.add(u"\u0391",    "*A")
    t.add(u"\u0392",    "*B")
    t.add(u"\u0393",    "*G")
    t.add(u"\u0394",    "*D")
    t.add(u"\u0395",    "*E")
    t.add(u"\u0396",    "*Z")
    t.add(u"\u0397",    "*H")
    t.add(u"\u0398",    "*Q")
    t.add(u"\u0399",    "*I")
    t.add(u"\u039A",    "*K")
    t.add(u"\u039B",    "*L")
    t.add(u"\u039C",    "*M")
    t.add(u"\u039D",    "*N")
    t.add(u"\u039E",    "*C")
    t.add(u"\u039F",    "*O")
    t.add(u"\u03A0",    "*P")
    t.add(u"\u03A1",    "*R")
    t.add(u"\u03A3",    "*S")
    t.add(u"\u03A4",    "*T")
    t.add(u"\u03A5",    "*U")
    t.add(u"\u03A6",    "*F")
    t.add(u"\u03A7",    "*X")
    t.add(u"\u03A8",    "*Y")
    t.add(u"\u03A9",    "*W")

    t.add(u"\u03B1",    "A")
    t.add(u"\u03B2",    "B")
    t.add(u"\u03B3",    "G")
    t.add(u"\u03B4",    "D")
    t.add(u"\u03B5",    "E")
    t.add(u"\u03B6",    "Z")
    t.add(u"\u03B7",    "H")
    t.add(u"\u03B8",    "Q")
    t.add(u"\u03B9",    "I")
    t.add(u"\u03BA",    "K")
    t.add(u"\u03BB",    "L")
    t.add(u"\u03BC",    "M")
    t.add(u"\u03BD",    "N")
    t.add(u"\u03BE",    "C")
    t.add(u"\u03BF",    "O")
    t.add(u"\u03C0",    "P")
    t.add(u"\u03C1",    "R")

    t.add(u"\u002a",    "%2")  # Asterisk
    t.add(u"\u03C2\n",    "S")
    t.add(u"\u03C2\u0020",    "S ")
    t.add(u"\u03C2\u002F",    "S%3")
    t.add(u"\u03C2\u02b9",    "S#")
    t.add(u"\u03C2\u02bc",    "S%30")
    t.add(u"\u03C2\u03bc",    "SM") # Occurs in some stray word in Ulrik's Textus Receptus
    t.add(u"\u03C2\u2019",    "S'")
    t.add(u"\u03C2\u0374",    "S#") # final sigma + Kaira
    t.add(u"\u03C2!",    "S!")
    t.add(u"\u03C2,",    "S,")
    t.add(u"\u03C2.",    "S.")
    t.add(u"\u03C2\u00b7",    "S:")
    t.add(u"\u03C2\u0387",    "S:")
    t.add(u"\u03C2;",         "S;") # NOTE: This is not correct Greek encoding!
    t.add(u"\u03C2\u037E",    "S;")
    t.add(u"\u03C2\u2014",    "S_") # m-dash
    t.add(u"\u03C2\u201d",    "S\"") # double quotation mark right
    t.add(u"\u03C2]",    "S]")
    t.add(u"\u03C2)",    "S]1")
    t.add(u"\u03C2\u27e7",    "S]16")
    t.add(u"\u03C2[",    "S[")
    t.add(u"\u03C2-",    "S-")
    t.add(u"\u03C2(",    "S[1")
    t.add(u"\u03C2@",    "S@")
    t.add(u"\u03C2_",    "S_")
    t.add(u"\u03C2 (I)",    "S [1I]1")
    t.add(u"\u03C2 (II)",    "S [1II]1")
    t.add(u"\u03C2 (\u03b9)",    "S [1I]1")
    t.add(u"\u03C2 (\u03b9\u03b9)",    "S [1II]1")
    t.add(u"\u03C2 (1)",    "S [11]1")
    t.add(u"\u03C2 (2)",    "S [12]1")
    t.add(u"\u03C2_(I)",    "S_[1I]1")
    t.add(u"\u03C2_(II)",    "S_[1II]1")
    t.add(u"\u03C3",    "S")

    t.add(u"\u03C4",    "T")
    t.add(u"\u03C5",    "U")
    t.add(u"\u03C6",    "F")
    t.add(u"\u03C7",    "X")
    t.add(u"\u03C8",    "Y")
    t.add(u"\u03C9",    "W")

    t.add(U"\u03CA",    "I+")
    t.add(U"\u03CB",    "U+")


    t.add(u"\u1F00",    "A)")
    t.add(u"\u1F01",    "A(")
    t.add(u"\u1F02",    "A)\\")
    t.add(u"\u1F03",    "A(\\")
    t.add(u"\u1F04",    "A)/")
    t.add(u"\u1F05",    "A(/")
    t.add(u"\u1F10",    "E)")
    t.add(u"\u1F11",    "E(")
    t.add(u"\u1F12",    "E)\\")
    t.add(u"\u1F13",    "E(\\")
    t.add(u"\u1F14",    "E)/")
    t.add(u"\u1F15",    "E(/")
    t.add(u"\u1F20",    "H)")
    t.add(u"\u1F21",    "H(")
    t.add(u"\u1F22",    "H)\\")
    t.add(u"\u1F23",    "H(\\")
    t.add(u"\u1F24",    "H)/")
    t.add(u"\u1F25",    "H(/")
    t.add(u"\u03B7\u0303", "H=") # U+0303 is the combining tilde...
    t.add(u"\u1F30",    "I)")
    t.add(u"\u1F31",    "I(")
    t.add(u"\u1F32",    "I)\\")
    t.add(u"\u1F33",    "I(\\")
    t.add(u"\u1F34",    "I)/")
    t.add(u"\u1F35",    "I(/")
    t.add(u"\u1F40",    "O)")
    t.add(u"\u1F41",    "O(")
    t.add(u"\u1F42",    "O)\\")
    t.add(u"\u1F43",    "O(\\")
    t.add(u"\u1F43 ",    "O(\\ ")
    t.add(u"\u1F44",    "O)/")
    t.add(u"\u1F45",    "O(/")
    t.add(u"\u1F50",    "U)")
    t.add(u"\u1F51",    "U(")
    t.add(u"\u1F52",    "U)\\")
    t.add(u"\u1F53",    "U(\\")
    t.add(u"\u1F54",    "U)/")
    t.add(u"\u1F55",    "U(/")
    t.add(u"\u1F60",    "W)")
    t.add(u"\u1F61",    "W(")
    t.add(u"\u1F62",    "W)\\")
    t.add(u"\u1F63",    "W(\\")
    t.add(u"\u1F64",    "W)/")
    t.add(u"\u1F65",    "W(/")

    t.add(u"\u1F06",    "A)=")
    t.add(u"\u1F07",    "A(=")
    t.add(u"\u1F26",    "H)=")
    t.add(u"\u1F27",    "H(=")
    t.add(u"\u1F36",    "I)=")
    t.add(u"\u1F37",    "I(=")
    t.add(u"\u1F56",    "U)=")
    t.add(u"\u1F57",    "U(=")
    t.add(u"\u1F66",    "W)=")
    t.add(u"\u1F67",    "W(=")

    t.add(u"\u1F08",    "*)A")
    t.add(u"\u1F09",    "*(A")
    t.add(u"\u1F0B",    "*(\A")  
    t.add(u"\u1FCE\u0391",    "*)/A")
    t.add(u"\u1F0C",    "*)/A")
    t.add(u"\u1F0D",    "*(/A")
    t.add(u"\u1F80",        "A)|")
    t.add(u"\u1F8D",        "*(/A|")
    t.add(u"\u1F0D\u0345",        "*(/A|")
    t.add(u"\u1F09\u0301\u0345",  "*(/A|")
    t.add(u"\u1F0E",    "*)=A")
    t.add(u"\u1FCE\u0391",    "*)/A")
    t.add(u"\u1FCF\u0391", "*)=A")
    t.add(u"\u1FDD\u0391",    "*(\\A")
    t.add(u"\u1FDE\u0391",    "*(/A")
    t.add(u"\u1FDF\u0391",    "*(=A")
    t.add(u"\u1F0F",    "*(=A")
    t.add(u"\u1F18",    "*)E")
    t.add(u"\u1F19",    "*(E")
    #
    t.add(u"\u1F1A",    "*)\E")
    t.add(u"\u1F1B",    "*(\E")
    t.add(u"\u1F1C",    "*)/E")
    t.add(u"\u1F1D",    "*(/E")
    t.add(u"\u1FCE\u0395",    "*)/E")
    t.add(u"\u1FDE\u0395",    "*(/E")
    t.add(u"\u1FDD\u0395",    "*(\\E")

    t.add(u"\u1F28",    "*)H")
    t.add(u"\u1F29",    "*(H")
    t.add(u"\u1F2A",    "*)\\H")
    t.add(u"\u1F2B",    "*(\\H")
    #
    t.add(u"\u1FCE\u0397",    "*)/H")
    t.add(u"\u1FDF\u0397",    "*(=H")
    t.add(u"\u1FDE\u0397",    "*(/H")
    t.add(u"\u1F2C",    "*)/H")
    t.add(u"\u1F9C",    "*)/H|")
    t.add(u"\u1F2C\u0345",          "*)/H|")
    t.add(u"\u1F28\u0301\u0345",    "*)/H|")
    t.add(u"\u1F2D",    "*(/H")
    #
    t.add(u"\u1F2E",    "*)=H")
    t.add(u"\u1F2F",    "*(=H")
    t.add(u"\u1FCE\u0397",    "*)/H")
    t.add(u"\u1FCF\u0397", "*)=H")
    t.add(u"\u1FCE\u0399",    "*)/I")
    t.add(u"\u1F38",    "*)I")
    t.add(u"\u1F39",    "*(I")
    t.add(u"\u1F3A",    "*)\\I")
    t.add(u"\u1F3B",    "*(/I")
    t.add(u"\u1F3C",    "*)/I")  
    t.add(u"\u1F3D",    "*(/I")
    t.add(u"\u1FDE\u0399",    "*(/I")
    t.add(u"\u1F3E",    "*)=I")
    t.add(u"\u1F3F",    "*(=I")
    #
    t.add(u"\u1F48",    "*)O")
    t.add(u"\u1F49",    "*(O")
    t.add(u"\u1FCE\u039f",    "*)/O")
    t.add(u"\u1FDD\u039F",    "*(\\O")
    t.add(u"\u1FDE\u039F",    "*(/O")
    #
    #
    t.add(u"\u1F4A",    "*)\\O")
    t.add(u"\u1F4B",    "*(\\O")
    t.add(u"\u1F4C",    "*)/O")
    t.add(u"\u1F4D",    "*(/O")
    #
    t.add(u"\u1F59",    "*(U")
    t.add(u"\u1F59",    "*(U")
    t.add(u"\u1F5B",    "*(\\U")
    t.add(u"\u1F5D",    "*(/U")
    t.add(u"\u1FDE\u03a5",    "*(/U")
    #
    t.add(u"\u1F5F",    "*(=U")
    
    t.add(u"\u1F68",    "*)W")
    t.add(u"\u1F69",    "*(W")
    #
    #
    t.add(u"\u1F6A",    "*)\\W")
    t.add(u"\u1F6B",    "*(\\W")
    t.add(u"\u1F6C",    "*)/W")
    t.add(u"\u1F6D",    "*(/W")
    t.add(u"\u1FDE\u03a9", "*(/W")
    t.add(u"\u1F6E",    "*)=W")
    t.add(u"\u1FCD\u03a9",    "*)\\W")
    t.add(u"\u1FCE\u03a9",    "*)/W")
    t.add(u"\u1FCF\u03a9", "*)=W")
    t.add(u"\u1F6F",    "*(=W")
    t.add(u"\u1FDF\u03a9",    "*(=W")
    t.add(u"\u1FA4",              "W)/|")
    t.add(u"\u1FA6",              "W)=|")
    t.add(u"\u1FAF",              "*(=W|")
    t.add(u"\u1F6F\u0345",        "*(=W|")
    t.add(u"\u1F69\u0342\u0345",  "*(=W|")

    t.add(u"\u1F6E",    "*)=W")
    t.add(u"\u1F6F",    "*(=W")

    t.add(u"\u1F70",    "A\\")
    t.add(u"\u03AC",    "A/") # NOTE: Is monotonic Greek
    t.add(u"\u1F71",    "A/")
    t.add(u"\u1F72",    "E\\")
    t.add(u"\u03AD",    "E/") # NOTE: Is monotonic Greek
    t.add(u"\u1F73",    "E/")
    t.add(u"\u1F74",    "H\\")
    t.add(u"\u03AE",    "H/") # NOTE: Is monotonic Greek
    t.add(u"\u1F75",    "H/")
    t.add(u"\u1F76",    "I\\")
    t.add(u"\u03AF",    "I/") # NOTE: Is monotonic Greek
    t.add(u"\u1F77",    "I/")
    t.add(u"\u1F78",    "O\\")
    t.add(u"\u03CC",    "O/") # NOTE: Is monotonic Greek
    t.add(u"\u1F79",    "O/")
    t.add(u"\u1F7A",    "U\\")
    t.add(u"\u03CD",    "U/") # NOTE: Is monotonic Greek
    t.add(u"\u1F7B",    "U/")
    t.add(u"\u1F7C",    "W\\") 
    t.add(u"\u03CE",    "W/") # NOTE: Is monotonic Greek
    t.add(u"\u1F7D",    "W/")

    t.add(u"\u1F84",    "A)/|")
    t.add(u"\u1F85",    "A(/|")
    t.add(u"\u1F86",    "A)=|")
    t.add(u"\u1F90",    "H)|")
    t.add(u"\u1F91",    "H(|")
    t.add(u"\u1F94",    "H)/|")
    t.add(u"\u1F96",    "H)=|")
    t.add(u"\u1F97",    "H(=|")
    t.add(u"\u1FA0",    "W)|")
    t.add(u"\u1FA7",    "W(=|")

    t.add(u"\u1FB6",    "A=")
    t.add(u"\u1FC6",    "H=")
    t.add(u"\u1FD6",    "I=")
    t.add(u"\u1FE6",    "U=")
    t.add(u"\u1FE7",    "U=+")
    t.add(u"\u1FF6",    "W=")

    t.add(u"\u1FD2",    "I\\+")
    t.add(u"\u0390",    "I/+") # Note: This is monotonic Greek
    t.add(u"\u1FD3",    "I/+")
    t.add(u"\u1FE2",    "U\\+")
    t.add(u"\u03B0",    "U/+") # Note: This is monotonic Greek
    t.add(u"\u1FE3",    "U/+")

    t.add(u"\u1FB3",    "A|")
    t.add(u"\u1FB4",    "A/|")
    t.add(u"\u1FC3",    "H|")
    t.add(u"\u1FC4",    "H/|")
    t.add(u"\u1FF3",    "W|")
    t.add(u"\u1FF4",    "W/|")

    t.add(u"\u1FB7",    "A=|")
    t.add(u"\u1FC7",    "H=|")
    t.add(u"\u1FF7",    "W=|")

    t.add(u"\u1FE5",    "R(")
    t.add(u"\u1FEC",    "*(R")

    t.add(u"\u1FE4",    "R)")
    t.add(u"\u03A1\u0313",    "*R)")
    t.add(u"\u03A1\u0313",    "*)R")

    t.add(u" (I)", " [1I]1")
    t.add(u" (II)", " [1II]1")
    t.add(u" (\u1f43 ", " [1O(\\ ")
    t.add(u" (\u03b9)", " [1I]1")
    t.add(u" (\u03b9\u03b9)", " [1II]1")
    t.add(u" (1)", " [11]1")
    t.add(u" (2)", " [12]1")
    t.add(u" (", " [1")

    t.add(u"\u00a0", " ")


    #    t.add(u"~",    "~")
    #    t.add(u"-",    "-")

    # Hyphen is U+2010, according to the TLG BETA code manual quick
    # reference (footnote 13 on page 4).
    t.add(u"\u2010", "-")

    # But we should also treat the normal hyphen (U+002D)
    t.add(u"-", "-")
    
    
    t.add(u"0",    "0")
    t.add(u"1",    "1")
    t.add(u"2",    "2")
    t.add(u"3",    "3")
    t.add(u"4",    "4")
    t.add(u"5",    "5")
    t.add(u"6",    "6")
    t.add(u"7",    "7")
    t.add(u"8",    "8")
    t.add(u"9",    "9")
    
    t.add(u"@",    "@")
    t.add(u"$",    "$")
    
    t.add(u"\u002f",    "%3") # Solidus ‣ Slash

    
    t.add(u" ",    " ")
    
    t.add(u".",    ".")
    t.add(u",",    ",")
    t.add(u"\u1ffe", "(") # GREEK DASIA
    t.add(u"\u1ffe\u0391", "*(A") # GREEK DASIA + GREEK CAPITAL ALPHA
    t.add(u"\u1ffe\u0395", "*(E") # GREEK DASIA + GREEK CAPITAL EPSILON
    t.add(u"\u1ffe\u0397", "*(H") # GREEK DASIA + GREEK CAPITAL ETA
    t.add(u"\u1ffe\u0399", "*(I") # GREEK DASIA + GREEK CAPITAL IOTA
    t.add(u"\u1ffe\u039F", "*(O") # GREEK DASIA + GREEK CAPITAL OMICRON
    t.add(u"\u1ffe\u03A5", "*(U") # GREEK DASIA + GREEK CAPITAL UPSILON
    t.add(u"\u1ffe\u03A1", "*(R") # GREEK DASIA + GREEK CAPITAL RHO
    t.add(u"\u1ffe\u03A9", "*(W") # GREEK DASIA + GREEK CAPITAL OMEGA
    t.add(u"\u1FBF",    "'") # GREEK PSILI # NOTE: It could also denote PSILI, but it is used in AGNT to refer to apostrophe
    t.add(u"\u0315",    "'") # COMBINING COMMA ABOVE RIGHT
    t.add(u"'",    "'")
    t.add(u"\u02B9",    "#") # Kaira (numerical apostrophe) (from MODIFIER LETTER PRIME)
    t.add(u"\u0374",    "#") # Kaira (numerical apostrophe)
    t.add(u"\u2013",    "%19") # en-dash
    t.add(u"\u2014",    "_") # em-dash
    t.add(u"\u2019",    "'") # right quotation mark
    t.add(u"\u1FBD",    "'") # koronis
    t.add(u"\u00b7",    ":") # NOTE: This is not correct Greek encoding!
    t.add(u"\u0387",    ":")
    t.add(u"\u037e",    ";")
    t.add(u";",         ";") # NOTE: This is not correct Greek encoding!
    t.add(u"\u0313",    "'") # Combining breathing... used in ANLEX for apostrophe... FIXME: Do it right!
    t.add(u"\u0314",    "(") # COMBINING REVERSED COMMA ABOVE ... used in AGNT for something which it shouldn't be used for.
    t.add(u"_",    "_")
    t.add(u"-",    "-")
    t.add(u"!",    "!")
    t.add(u"\u0028", "[1")
    

    t.add(u"[",    "[")
    t.add(u"]",    "]")

    # Double square brackets in one glyph
    t.add(u"\u301a", "[16")
    t.add(u"\u27e6", "[16")
    t.add(u"\u301b", "]16")
    t.add(u"\u27e7", "]16")

    t.add(u")",    "]1")
    t.add(u"<",    "[2")
    t.add(u">",    "]2")
    t.add(u"(1)",    "[1I]1")
    t.add(u"(2)",    "[1II]1")
    t.add(u"(",    "[1")

    t.add(u"\u03da",    "*#2")  # GREEK (CAPITAL) LETTER STIGMA
    t.add(u"\u03db",    "#2")   # GREEK SMALL LETTER STIGMA
    t.add(u"\u03dc",    "*V")   # GREEK CAPITAL LETTER DIGAMMA
    t.add(u"\u03dd",    "V")    # GREEK SMALL LETTER DIGAMMA
    
    
    return t


def accordance2UnicodeTrie():
    t = Trie()
    
    t.add(u"A",     "\u0391")  # *A
    t.add(u"B",     "\u0392")  # *B
    t.add(u"G",     "\u0393")  # *G
    t.add(u"D",     "\u0394")  # *D
    t.add(u"E",     "\u0395")  # *E
    t.add(u"Z",     "\u0396")  # *Z
    t.add(u"Q",     "\u0398")  # *Q
    t.add(u"K",     "\u039A")  # *K
    t.add(u"L",     "\u039B")  # *L
    t.add(u"M",     "\u039C")  # *M
    t.add(u"N",     "\u039D")  # *N
    t.add(u"X",     "\u039E")  # *C
    t.add(u"O",     "\u039F")  # *O
    t.add(u"P",     "\u03A0")  # *P
    t.add(u"S",     "\u03A3")  # *S
    t.add(u"T",     "\u03A4")  # *T
    t.add(u"F",     "\u03A6")  # *F
    t.add(u"C",     "\u03A7")  # *X
    
    #t.add(u"\u03A8",    "*Y")
    #t.add(u"\u03A9",    "*W")
    
    t.add(u"a",     "\u03B1")  # A
    t.add(u"b",     "\u03B2")  # B
    t.add(u"g",     "\u03B3")  # G
    t.add(u"d",     "\u03B4")  # D
    t.add(u"e",     "\u03B5")  # E
    t.add(u"z",     "\u03B6")  # Z
    t.add(u"h",     "\u03B7")  # H
    t.add(u"q",     "\u03B8")  # Q
    t.add(u"i",     "\u03B9")  # I
    t.add(u"k",     "\u03BA")  # K
    t.add(u"l",     "\u03BB")  # L
    t.add(u"m",     "\u03BC")  # M
    t.add(u"n",     "\u03BD")  # N
    t.add(u"x",     "\u03BE")  # C
    t.add(u"o",     "\u03BF")  # O
    t.add(u"p",     "\u03C0")  # P
    t.add(u"r",     "\u03C1")  # R
    t.add(u"§",     "\u03C2")  # S final
    t.add(u"s",     "\u03C3")  # S
    t.add(u"t",     "\u03C4")  # T
    t.add(u"u",     "\u03C5")  # U
    t.add(u"f",     "\u03C6")  # F
    t.add(u"c",     "\u03C7")  # X
    t.add(u"y",     "\u03C8")  # Y
    t.add(u"w",     "\u03C9")  # W
    
    t.add(u"aî",    "\u1F00")  # A)
    t.add(u"að",    "\u1F01")  # A(
    t.add(u"aà",    "\u1F04")  # A)/
    t.add(u"aâ",    "\u1F05")  # A(/
    t.add(u"a¡",    "\u1F06")  # A)=
    t.add(u"ÆA",    "\u1F08")  # )*A
    t.add(u"ïA",    "\u1F09")  # (*A
    t.add(u"ÚA",    "\u1F0C")  # )/*A
    t.add(u"ÝA",    "\u1F0D")  # (/*A
    t.add(u"ÆAv",   "\u1F0E")  # *)=A
    t.add(u"eú",    "\u1F10")  # E)
    t.add(u"eû",    "\u1F11")  # E(
    t.add(u"e¦",    "\u1F14")  # E)/
    t.add(u"e¼",    "\u1F15")  # E(/
    t.add(u"ÆE",    "\u1F18")  # *)E
    t.add(u"ïE",    "\u1F19")  # *(E
    t.add(u"EÁ",    "\u1F1C")  # *)/E
    t.add(u"ÝE",    "\u1F1D")  # *(/E
    t.add(u"hj",    "\u1F20")  # H)
    t.add(u"hJ",    "\u1F21")  # H(
    t.add(u"hÁ",    "\u1F24")  # H)/
    t.add(u"h¢",    "\u1F25")  # H(/
    t.add(u"hª",    "\u1F26")  # H)=
    t.add(u"h°",    "\u1F27")  # H(=
    t.add(u"ÆH",    "\u1F28")  # *H)
    t.add(u"ïH",    "\u1F29")  # *H(
    t.add(u"HÁ",    "\u1F2C")  # *)/H
    t.add(u"iú",    "\u1F30")  # I)
    t.add(u"iû",    "\u1F31")  # I(
    t.add(u"i¦",    "\u1F34")  # I)/
    t.add(u"i¼",    "\u1F35")  # I(/
    t.add(u"i¥",    "\u1F36")  # I)=
    t.add(u"iÐ",    "\u1F37")  # I(=
    t.add(u"ÆI",    "\u1F38")  # *)I
    t.add(u"ïI",    "\u1F39")  # *(I
    t.add(u"oj",    "\u1F40")  # O)
    t.add(u"oJ",    "\u1F41")  # O(
    t.add(u"oÁ",    "\u1F44")  # O)/
    t.add(u"o¢",    "\u1F45")  # O(/
    t.add(u"ÆO",    "\u1F48")  # *)O
    t.add(u"uj",    "\u1F50")  # U)
    t.add(u"uJ",    "\u1F51")  # U(
    t.add(u"uÁ",    "\u1F54")  # U)/
    t.add(u"u¢",    "\u1F55")  # U(/
    t.add(u"uª",    "\u1F56")  # U)=
    t.add(u"u°",    "\u1F57")  # U(=
    t.add(u"ïU",    "\u1F59")  # *U(
    t.add(u"wî",    "\u1F60")  # W)
    t.add(u"wð",    "\u1F61")  # W(
    t.add(u"wà",    "\u1F65")  # W(/
    t.add(u"wâ",    "\u1F65")  # W(/
    t.add(u"w¡",    "\u1F66")  # W)=
    t.add(u"wðv",   "\u1F67")  # W(=
    t.add(u"ÆW",    "\u1F68")  # *)W
    t.add(u"ïW",    "\u1F69")  # *(W
    t.add(u"aÀ",    "\u1F71")  # A/
    t.add(u"eÖ",    "\u1F73")  # E/
    t.add(u"h/",    "\u1F75")  # H/
    t.add(u"iÖ",    "\u1F77")  # I/
    t.add(u"o/",    "\u1F79")  # O/
    t.add(u"u/",    "\u1F7B")  # U/
    t.add(u"wÀ",    "\u1F7D")  # W/
    t.add(u"aàö",   "\u1F84")  # A)/|
    t.add(u"aâö",   "\u1F85")  # A(/|
    t.add(u"wîö",   "\u1FA0")  # W)|
    t.add(u"aö",    "\u1FB3")  # A|
    t.add(u"aÀö",   "\u1FB4")  # A/|
    t.add(u"a×",    "\u1FB6")  # A=
    t.add(u"hö",    "\u1FC3")  # H|
    t.add(u"h/ö",   "\u1FC4")  # H/|
    t.add(u"hö/",   "\u1FC4")  # H/|
    t.add(u"hv",    "\u1FC6")  # H=
    t.add(u"höv",   "\u1FC7")  # H=|
    t.add(u"hvö",   "\u1FC7")  # H=|
    t.add(u"iÃ",    "\u1FD6")  # I=
    t.add(u"rJ",    "\u1FE5")  # R(
    t.add(u"uv",    "\u1FE6")  # U=
    t.add(u"ïR",    "\u1FEC")  # *(R
    t.add(u"wö",    "\u1FF3")  # W|
    t.add(u"wö/",   "\u1FF4")  # W/|
    t.add(u"wÀö",   "\u1FF4")  # W/|
    t.add(u"w×",    "\u1FF6")  # W=
    t.add(u"wöv",   "\u1FF7")  # W=|
    t.add(u"wö×",   "\u1FF7")  # W=|
    
    t.add(u",",     ",")       # ,
    t.add(u" ",     " ")       # space
    t.add(u"\t",    "\t")      # tab
    
    # especially for greenlee
    t.add(u"=",     "=")       # indeclinable
    t.add(u"-",     "-")       # affix
    t.add(u"&",     "&")       # &
    t.add(u"*",     "*")       # irregular form
    t.add(u"(1)",   "(1)")     # lexeme differentiation
    t.add(u"(2)",   "(2)")     # lexeme differentiation
    t.add(u"(3)",   "(3)")     # lexeme differentiation
    t.add(u"___",   "___")     # ???
    
    return t


def beta2DiscoveryBibleTransliterationTrie():
    t = Trie()

    t.add("*A",      "A")
    t.add("*AU)",    "Au")
    t.add("*B",      "B")
    t.add("*G*G",    "NG")
    t.add("*G*K",    "NK")
    t.add("*G*C",    "NKS")
    t.add("*G*X",    "NX")
    t.add("*G",      "G")
    t.add("*D",      "D")
    t.add("*E",      "E")
    t.add("*EU)=",   "Eú")
    t.add("*EU)\\",  "Eú")
    t.add("*EU)/",   "Eú")
    t.add("*EU)",    "Eu")
    t.add("*EU(=",   "Heú")
    t.add("*EU(\\",  "Heú")
    t.add("*EU(/",   "Heú")
    t.add("*EU(",    "Heu")
    t.add("*Z",      "Z")
    t.add("*H",      "Ē")
    t.add("*HU)=",   "Ēý")
    t.add("*HU)",    "Ēy")
    t.add("*Q",      "Th")
    t.add("*I",      "I")
    t.add("*K",      "K")
    t.add("*L",      "L")
    t.add("*M",      "M")
    t.add("*N",      "N")
    t.add("*C",      "KS")
    t.add("*O",      "O")
    t.add("*P",      "P")
    t.add("*R)",     "R")
    t.add("*R(",     "Rh")
    t.add("*R",      "R")
    t.add("*S",      "S")
    t.add("*T",      "T")
    t.add("*A*U",    "AU")
    t.add("*E*U",    "EU")
    t.add("*H*U",    "ĒY")
    t.add("*O*U",    "OU")
    t.add("*U*I",    "YI")
    t.add("*AU",     "Au")
    t.add("*EU",     "Eu")
    t.add("*HU",     "Ēy")
    t.add("*OU)",    "Ou")
    t.add("*OU",     "Ou")
    t.add("*UI",     "Yi")
    t.add("*U",      "Y")
    t.add("*F",      "Ph")
    t.add("*X",      "X")
    t.add("*Y",      "Ps")
    t.add("*W",      "Ō")

    t.add("A",      "a")
    t.add("B",      "b")
    t.add("GG",     "gg")
    t.add("GK",     "gk")
    t.add("GC",     "gks")
    t.add("GX",     "gx")
    t.add("G",      "g")
    t.add("D",      "d")
    t.add("E",      "e")
    t.add("Z",      "z")
    t.add("H",      "ē")
    t.add("Q",      "th")
    t.add("AI",     "ai")
    t.add("EI",     "ei")
    t.add("HI",     "ēi")
    t.add("OI",     "oi")
    t.add("I",      "i")
    t.add("K",      "k")
    t.add("L",      "l")
    t.add("M",      "m")
    t.add("N",      "n")
    t.add("C",      "ks")
    t.add("O",      "o")
    t.add("P",      "p")
    t.add("R",      "r")
    t.add("R)",     "r")
    t.add("R(",     "rh")

    t.add("S\n",    "s")
    t.add("S ",     "s ")
    t.add("S'",     "s\u2019")
    t.add("S,",     "s,")
    t.add("S.",     "s.")
    t.add("S:",     "s\u0387")
    t.add("S;",     "s\u037E")  
    t.add("S]16",   "s\u27e6") # Double square brackets in one glyph
    t.add("S]1",    "s)")
    t.add("S]",     "s]")
    t.add("S@",     "s@")
    t.add("S_",     "s_")
    t.add("S",      "s")
    t.add("T",      "t")

    t.add("AU",     "au")
    t.add("EU",     "eu")
    t.add("HU",     "ēy")
    t.add("OU",     "ou")
    t.add("UI",     "yi")
    t.add("UI=",    "yí")
    t.add("UI(",    "hyi")
    t.add("U",      "y")
    t.add("F",      "ph")
    t.add("X",      "x")
    t.add("Y",      "ps")
    t.add("W",      "ō")

    t.add("AI+",    "ai")
    t.add("EI+",    "ei")
    t.add("HI+",    "ēi")
    t.add("OI+",    "oi")
    t.add("I+",     "i")
    t.add("AU+",    "ay")
    t.add("EU+",    "ey")
    t.add("HU+",    "ēy")
    t.add("OU+",    "oy")
    t.add("U+",     "y")

    t.add("A)",     "a")
    t.add("A(",     "ha")
    t.add("A)\\",   "á")
    t.add("A(\\",   "há")
    t.add("A)/",    "á")
    t.add("A(/",    "há")
    t.add("E)",     "e")
    t.add("E(",     "he")
    t.add("E)\\",   "é")
    t.add("E(\\",   "hé")
    t.add("E)/",    "é")
    t.add("E(/",    "hé")
    t.add("H)",     "ē")
    t.add("H(",     "hē")
    t.add("H)\\",   "ḗ")
    t.add("H(\\",   "hḗ")
    t.add("H)/",    "ḗ")
    t.add("H(/",    "hḗ")
    t.add("AI)",    "ai")
    t.add("EI)",    "ei")
    t.add("HI)",    "ēi")
    t.add("OI)",    "oi")
    t.add("I)",     "i")
    t.add("AI(",    "hai")
    t.add("EI(",    "hei")
    t.add("HI(",    "hēi")
    t.add("OI(",    "hoi")
    t.add("I(",     "hi")
    t.add("AI)\\",  "aí")
    t.add("EI)\\",  "eí")
    t.add("OI)\\",  "oí")
    t.add("I)\\",   "í")
    t.add("AI(\\",  "haí")
    t.add("EI(\\",  "heí")
    t.add("HI(\\",  "hēí")
    t.add("OI(\\",  "hoí")
    t.add("I(\\",   "hí")
    t.add("AI)/",   "aí")
    t.add("EI)/",   "eí")
    t.add("HI)/",   "ēí")
    t.add("OI)/",   "oí")
    t.add("I)/",    "í")
    t.add("AI(/",   "haí")
    t.add("EI(/",   "heí")
    t.add("HI(/",   "hēí")
    t.add("OI(/",   "hoí")
    t.add("I(/",    "hí")
    t.add("O)",     "o")
    t.add("O(",     "ho")
    t.add("O)\\",   "ó")
    t.add("O(\\",   "hó")
    t.add("O)/",    "ó")
    t.add("O(/",    "hó")
    t.add("AU)",    "au")
    t.add("EU)",    "eu")
    t.add("HU)",    "ēy")
    t.add("OU)",    "ou")
    t.add("U)",     "y")
    t.add("U(I",    "hyi")
    t.add("AU(",    "hau")
    t.add("EU(",    "heu")
    t.add("HU(",    "hēy")
    t.add("OU(",    "hou")
    t.add("U(",     "hy")
    t.add("AU)\\",  "aú")
    t.add("EU)\\",  "eú")
    t.add("HU)\\",  "ēý")
    t.add("OU)\\",  "oú")
    t.add("U(\\",   "hý")
    t.add("AU)/",   "aú")
    t.add("EU)/",   "eú")
    t.add("HU)/",   "ēý")
    t.add("OU)/",   "oú")
    t.add("U)/",    "ý")
    t.add("AU(/",   "haú")
    t.add("EU(/",   "heú")
    t.add("HU(/",   "hēý")
    t.add("OU(/",   "hoú")
    t.add("U(/",    "hý")
    t.add("W)",     "ō")
    t.add("W(",     "hō")
    t.add("W)\\",   "ṑ")
    t.add("W(\\",   "hṑ")
    t.add("W)/",    "ṓ")
    t.add("W(/",    "hṓ")

    t.add("A)=",    "á")
    t.add("A(=",    "há")
    t.add("H)=",    "ē") # FIXME: Should have cirum flex accent, ^ 
    t.add("H(=",    "hē") # FIXME: Should have cirum flex accent, ^ 
    t.add("AI)=",   "aí")
    t.add("EI)=",   "eí")
    t.add("HI)=",   "ēí")
    t.add("OI)=",   "oí")
    t.add("I)=",    "í")
    t.add("AI(=",   "haí")
    t.add("EI(=",   "heí")
    t.add("HI(=",   "hēí")
    t.add("OI(=",   "hoí")
    t.add("I(=",    "hí")
    t.add("AU)=",   "aú")
    t.add("EU)=",   "eú")
    t.add("HU)=",   "ēý")
    t.add("OU)=",   "oú")
    t.add("U)=",    "ý")
    t.add("AU(=",   "haú")
    t.add("EU(=",   "heú")
    t.add("HU(=",   "hēý")
    t.add("OU(=",   "hoú")
    t.add("U(=",    "hý")
    t.add("W)=",    "ō") # FIXME: Should have circumflex accent, ^ 
    t.add("W(=",    "hō") # FIXME: Should have circumflex accent, ^ 

    t.add("*A)",     "A")
    t.add("*)A",     "A")
    t.add("*A(",     "Ha")
    t.add("*(A",     "Ha")
    t.add("*(\A",    "Ha")
    t.add("*A)/",    "Á")
    t.add("*)/A",    "Á")
    t.add("*A(/",    "Há")
    t.add("*(/A",    "Há")
    t.add("*A)=",    "Á")
    t.add("*)=A",    "Á")
    t.add("*A(=",    "Há")
    t.add("*(=A",    "Há")
    t.add("(/|*A",   "Hai")
    t.add("*(/A|",   "Hai")
    #
    t.add("*E)",     "E")
    t.add("*)E",     "E")
    t.add("*E(",     "He")
    t.add("*(E",     "He")
    #
    t.add("*)\E",    "É")
    t.add("*(\E",    "Hé")
    t.add("*E)/",    "É")
    t.add("*)/E",    "É")
    t.add("*E(/",    "Hé")
    t.add("*(/E",    "Hé")

    t.add("*H)",     "Ē")
    t.add("*)H",     "Ē")
    t.add("*H(",     "Hē")
    t.add("*(H",     "Hē")
    t.add("*H)\\",   "Ḗ")
    t.add(")\\*H",   "Ḗ")
    t.add("*)\\H",   "Ḗ")
    t.add("(\\*H",   "Hḗ")
    t.add("*(\\H",   "Hḗ")
    t.add(")/|*H",   "Ḗi")
    #
    t.add("*H)/",    "Ḗ")
    t.add("*)/H",    "Ḗ")
    t.add("*H(/",    "Hḗ")
    t.add("*(/H",    "Hḗ")
    #
    t.add("*)=H",    "Ē") # FIXME
    t.add("(=*H",    "Hē")# FIXME
    t.add("*(=H",    "Hē")# FIXME
    #
    t.add("*I)",     "I")
    t.add("*)I",     "I")
    t.add("*I(",     "Hi")
    t.add("*(I",     "Hi")
    t.add("*I)\\",   "Hí")
    t.add("*)\\I",   "Hí")
    t.add("*I(/",    "Hí")
    t.add("*(/I",    "Hí")
    t.add("*I)/",    "Í")
    t.add("*)/I",    "Í")
    t.add("*I(/",    "Hí")
    t.add("*(/I",    "Hí")
    t.add("*I)=",    "Í")
    t.add("*)=I",    "Í")
    t.add("*I(=",    "Hí")
    t.add("*(=I",    "Hí")
    #
    t.add("*O)",     "O")
    t.add("*)O",     "O")
    t.add("*O(",     "Ho")
    t.add("*(O",     "Ho")
    #
    #
    t.add("*O)\\",   "Ó")
    t.add("*)\\O",   "Ó")
    t.add("*O(\\",   "Hó")
    t.add("*(\\O",   "Hó")
    t.add("*O)/",    "Ó")
    t.add("*)/O",    "Ó")
    t.add("*O(/",    "Hó")
    t.add("*(/O",    "Hó")
    #
    t.add("*U(I",    "Hyi")
    t.add("*U(*I",   "HUI")
    t.add("*U(",     "Hy")
    t.add("*(U",     "Hy")
    t.add("*U(\\",   "Hý")
    t.add("*(\\U",   "Hý")
    #
    t.add("*(/U",    "Hý")
    t.add("*U(/",    "Hý")
    
    #
    t.add("*(=U",    "Hý")
    t.add("*U(=",    "Hý")
    
    t.add("*W)",     "Ō")
    t.add("*)W",     "Ō")
    t.add("*W(",     "Hō")
    t.add("*(W",     "Hō")
    #
    #
    t.add("*W)\\",   "Ṑ")
    t.add("*)\\W",   "Ṑ")
    t.add("*W(\\",   "Hṑ")
    t.add("*(\\W",   "Hṑ")
    t.add("*W)/",    "Ṓ")
    t.add("*)/W",    "Ṓ")
    t.add("*W(/",    "Hṓ")
    t.add("*(/W",    "Hṓ")
    t.add("*W)=",    "Ō")  # FIXME: Add ^
    t.add("*)=W",    "Ō")  # FIXME: Add ^
    t.add("*W(=",    "Hō") # FIXME: Add ^
    t.add("*(=W",    "Hō") # FIXME: Add ^

    t.add("(=|*W",   "Hōi")

    t.add("A\\",    "á")
    t.add("A/",     "á")
    t.add("E\\",    "é")
    t.add("E/",     "é")
    t.add("H\\",    "ḗ")
    t.add("H/",     "ḗ")
    t.add("AI\\",   "aí")
    t.add("EI\\",   "eí")
    t.add("HI\\",   "ēí")
    t.add("OI\\",   "oí")
    t.add("I\\",    "í")
    t.add("AI/",    "aí")
    t.add("EI/",    "eí")
    t.add("HI/",    "ēí")
    t.add("OI/",    "oí")
    t.add("I/",     "í")
    t.add("O\\",    "ó")
    t.add("O/",     "ó")
    t.add("AU\\",   "aú")
    t.add("EU\\",   "eú")
    t.add("HU\\",   "ēú")
    t.add("OU\\",   "oú")
    t.add("U\\",    "ý")
    t.add("AU/",    "aú")
    t.add("EU/",    "eú")
    t.add("HU/",    "ēý")
    t.add("OU/",    "oú")
    t.add("U/",     "ý")
    t.add("AU/+",   "aý")
    t.add("EU/+",   "eý")
    t.add("HU/+",   "ēý")
    t.add("OU/+",   "oý")
    t.add("W\\",    "ṓ")
    t.add("W/",     "ṓ")

    t.add("A)/|",   "á")
    t.add("A(/|",   "há")
    t.add("H)|",    "ē")
    t.add("H(|",    "hē")
    t.add("H)/|",   "ḗ")
    t.add("H)=|",   "ḗ")
    t.add("H(=|",   "hḗ")
    t.add("W)|",    "ō")
    t.add("W(=|",   "hṓ")

    t.add("A=",     "á")
    t.add("H=",     "ḗ")
    t.add("AI=",    "aí")
    t.add("EI=",    "eí")
    t.add("HI=",    "ēí")
    t.add("OI=",    "oí")
    t.add("I=",     "í")
    t.add("AU=",    "aú")
    t.add("EU=",    "eú")
    t.add("HU=",    "ēý")
    t.add("OU=",    "oú")
    t.add("U=",     "ý")
    t.add("W=",     "ṓ")

    t.add("I\\+",   "í")
    t.add("AI/+",   "aí")
    t.add("EI/+",   "eí")
    t.add("HI/+",   "ēí")
    t.add("OI/+",   "oí")
    t.add("I/+",    "í")
    t.add("AI+/",   "aí")
    t.add("EI+/",   "eí")
    t.add("HI+/",   "ēí")
    t.add("I+/",    "í")
    t.add("AU\\+",  "aý")
    t.add("EU\\+",  "eý")
    t.add("HU\\+",  "ēý")
    t.add("OU\\+",  "oý")
    t.add("U\\+",   "ý")
    t.add("U/+",    "ý")

    t.add("A|",     "a")
    t.add("A/|",    "á")
    t.add("H|",     "ē")
    t.add("H/|",    "ḗ")
    t.add("W|",     "ō")
    t.add("W|/",    "ṓ")
    t.add("W/|",    "ṓ")

    t.add("A=|",    "á")
    t.add("H=|",    "ḗ")
    t.add("W=|",    "ṓ")

    t.add("R(",     "rh")
    t.add("*R(",    "Rh")
    t.add("*(R",    "Rh")

    t.add("R)",     "r")
    t.add("*R)",    "R")
    t.add("*)R",    "R")


#    t.add("~",      "~")
#    t.add("-",      "-")
    
#    t.add("(null)", "(null)")
#    t.add("&", "&")
    
    t.add("0", "0")
    t.add("1", "1")
    t.add("2", "2")
    t.add("3", "3")
    t.add("4", "4")
    t.add("5", "5")
    t.add("6", "6")
    t.add("7", "7")
    t.add("8", "8")
    t.add("9", "9")
    
    t.add("@", "@")
    t.add("$", "$")
    
    t.add(" ", " ")
    
    t.add(".", ".")
    t.add(",", ",")
    t.add("#", "\u0374") # Kaira (numerical apostrophe)
    t.add("'", "\u2019")
    t.add(":", "\u0387")
    t.add(";", "\u037e")
    t.add("_", "_")
    t.add("-", "-")
    t.add("!", "!")
    

    t.add("[", "[")
    t.add("]", "]")

    t.add("[1", "(")
    t.add("]1", ")")
    t.add("[1I]1",   "(1)")
    t.add("[1II]1",  "(2)")

    
    t.add("[2", "<")
    t.add("]2", ">")

    t.add("\n", "")

    t.add("*#2", " Stigma")  # GREEK (CAPITAL) LETTER STIGMA
    t.add("#2", " stigma")   # GREEK SMALL LETTER STIGMA
    
    return t




def beta2unicode(beta_string):
    # note that this adds \n to ensure correct handling of final sigma
    unicode_string, remainder = beta2unicodetrie.convert(beta_string + "\n")
    if remainder:
        raise ValueError("unknown sequence %s in %s" % (remainder, beta_string))
    return unicode_string


def galatia2beta(galatia_string):
    # note that this adds \n to ensure correct handling of final sigma
    beta_string, remainder = galatia2betatrie.convert(galatia_string + "\n")
    if remainder:
        raise ValueError("unknown sequence %s in %s" % (remainder, galatia_string))
    return beta_string

def symbol2beta(symbol_string):
    # note that this adds \n to ensure correct handling of final sigma
    beta_string, remainder = symbol2betatrie.convert(symbol_string + "\n")
    if remainder:
        raise Exception(("unknown sequence %s in %s" % (repr(remainder), repr(symbol_string))).encode('utf-8'))
    return beta_string

def accordance2unicode(accordance_string):
    unicode_string, remainder = accordance2unicodetrie.convert(accordance_string)
    if remainder:
        raise ValueError("unknown sequence %s in %s" % (remainder.encode("utf-8"), accordance_string.encode("utf-8")))
    return unicode_string

def beta2sbl(beta_string):
    # note that this adds \n to ensure correct handling of final sigma
    unicode_string, remainder = beta2sbltransliterationtrie.convert(beta_string + "\n")
    if remainder:
        raise ValueError("unknown sequence %s in '%s'" % (repr(remainder), beta_string))
    return unicode_string

def beta2discoverybibletransliteration(beta_string):
    # note that this adds \n to ensure correct handling of final sigma
    unicode_string, remainder = beta2sbltransliterationtrie.convert(beta_string + "\n")
    if remainder:
        raise ValueError("unknown sequence %s in %s" % (remainder, beta_string))
    return unicode_string

def unicode2beta(unicode_string):
    # note that this adds \n to ensure correct handling of final sigma
    beta_string, remainder = unicode2betatrie.convert(unicode_string + "\n")
    if remainder:
        sys.stderr.write("unknown sequence '%s' in %s: U+%04X, %s" % (remainder, unicode_string, ord(remainder[0]), repr(unicode_string)))
        raise ValueError("unknown sequence '%s' in %s: U+%04X, %s" % (remainder, unicode_string, ord(remainder[0]), repr(unicode_string)))
    return beta_string


galatia2betatrie = galatia2BetaTrie()
symbol2betatrie = symbol2BetaTrie()
beta2galatiatrie = beta2GalatiaTrie()
beta2unicodetrie = beta2unicodeTrie()
beta2sbltransliterationtrie = beta2SBLTransliterationTrie()
unicode2betatrie = unicode2BetaTrie()
accordance2unicodetrie = accordance2UnicodeTrie()

# 
UMARtoBETAtrans = maketrans("abgdezhqiklmnxoprsvtufcyw", "ABGDEZHQIKLMNCOPRSSTUFXYW")
UMARtoGALATIAtrans = maketrans("abgdezqyiklmnxoprsvtufcyw", "abgdezjqiklmnxoprsvtufcyw")
BETAtoUMARtrans = maketrans("ABGDEZHQIKLMNCOPRSTUFXYW", "abgdezhqiklmnxoprstufcyw")


OLBtoBETAtrans = maketrans("abgdezhyiklmnxoprsvtufcqw", "ABGDEZHQIKLMNCOPRSSTUFXYW")
OLBtoGALATIAtrans = maketrans("abgdezhyiklmnxoprsvtufcqw", "abgdezjqiklmnxoprsvtufcyw")

TAGtoHELBETIKEtrans = maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "AB\x04\x05E\x06\x07HI\x08K\x0bMNO\x0c\x10\x11\x12T\x1b\x1c\x1d\x1e\x1fZ")

BETAtoGALATIAtrans = maketrans("ABGDEZHQIKLMNCOPRSSTUFXYW", "abgdezjqiklmnxoprsvtufcyw")
MixedCaseBETAtoBETAtrans = maketrans("AaBbGgDdEeZzHhQqIiKkLlMmNnCcOoPpRrSsJjTtUuFfXxYyWw", "AABBGGDDEEZZHHQQIIKKLLMMNNCCOOPPRRSSSSTTUUFFXXYYWW")

BETAtoOLBtrans = maketrans("ABGDEZHQIKLMNCOPRSTUFXYW", "abgdezhyiklmnxoprstufcqw")


reolbstrip = re.compile("[\\[\\]<>]+")
reaccentsstrip = re.compile("[/+\\|\\(\\)\\\\=,.;':\*]+")

reUpperCaseBETA = re.compile(r'([A-Z])')
reMoveDiacriticsBETA = re.compile(r'\*([AEHIOUW][IU]?)([\(\)][/=\\|]*)')
reMoveBreathingRhoBETA = re.compile(r'\*R([\(\)])')
reMoveBreathing2RhoBETA = re.compile(r'\*([\(\)])R')
reMoveStarBETA = re.compile(r'\*([\(\)][/=\\\|]*)([AEHIOUW][IU]?)')

def RemoveCasingBETA(beta_surface):
    newstr = beta_surface
    newstr = reMoveBreathingRhoBETA.sub(r'*\1R', newstr)
    newstr = reMoveDiacriticsBETA.sub(r'*\2\1', newstr)
    newstr = reMoveStarBETA.sub(r'\2\1', newstr)
    newstr = newstr.replace("(*", "*(").replace("(/*", "*(/").replace("(\\*", "*(\\").replace("(=*", "*(=").replace(")*", "*)").replace(")/*", "*)/").replace(")\\*", "*)\\").replace(")=*", "*)=")
    newstr = reMoveBreathing2RhoBETA.sub(r'*R\1', newstr)

    # This should come last.
    newstr = newstr.replace("*", "")

    return newstr

def RemovePunctuation(beta_surface):
    newstr = beta_surface.replace(".", "")
    newstr = newstr.replace(",", "")
    newstr = newstr.replace(":", "")
    newstr = newstr.replace(";", "")
    newstr = newstr.replace("'", "")
    return newstr

def RemoveLastAccentAndNormalize(beta_surface):
    newstr = beta_surface.replace("\\", "/")
    bHasMetAccent = False
    result = ""
    for index in xrange(len(newstr)-1, -1, -1):
        c = newstr[index]
        if not bHasMetAccent and c in ["/", "\\", "="]:
            pass
        else:
            result = c + result
    return result
            
    
    

def olbstrip(olbword):
    return reolbstrip.sub("", OLBtoBETAtranslate(olbword.surface))

def umartrip(olbword):
    return reolbstrip.sub("", OLBtoBETAtranslate(olbword.surface))

def RemoveAccents(surface):
    return reaccentsstrip.sub("", surface)

def OLBtoBETAtranslate(str):
    s1 = str.translate(OLBtoBETAtrans)
    return s1.replace("<", "[").replace(">", "]")


def UMARtoBETAtranslate(str):
    s1 = str.translate(OLBtoBETAtrans)
    return s1.replace("<", "[").replace(">", "]")


def BETAtoOLBtranslate(str):
    newstr = str.translate(BETAtoOLBtrans)
    if len(newstr) > 0 and newstr[-1] == "s":
        newstr = newstr[:-1] + "v"
    return newstr

def BETAtoUMARtranslate(str):
    newstr = str.translate(BETAtoUMARtrans)
    if len(newstr) > 0 and newstr[-1] == "s":
        newstr = newstr[:-1] + "v"
    return newstr

def UMARtoGALATIAtranslate(str):
    return str.translate(UMARtoGALATIAtrans)

def OLBtoGALATIAtranslate(str):
    return str.translate(OLBtoGALATIAtrans)

def BETAtoGALATIAtranslate(str):
    return str.translate(BETAtoGALATIAtrans)

def MixedCaseBETAtoBETAtranslate(str):
    return str.translate(MixedCaseBETAtoBETAtrans)

def MixedCaseBETAtoBETAtranslateWithStar(str):
    newstr = reUpperCaseBETA.sub(r'*\1', str)
    newstr = reMoveDiacriticsBETA.sub(r'*\2\1', newstr)
    newstr = reMoveBreathingRhoBETA.sub(r'*\1R', newstr)
    newstr = newstr.replace("(*", "*(").replace("(/*", "*(/").replace("(\\*", "*(\\").replace("(=*", "*(=").replace(")*", "*)").replace(")/*", "*)/").replace(")\\*", "*)\\").replace(")=*", "*)=")
    return newstr.translate(MixedCaseBETAtoBETAtrans)

def TAGtoHELBETIKEtranslate(str):
    return str.translate(TAGtoHELBETIKEtrans)

def mangleMQLString(str):
    return str.replace("\\", "\\\\").replace("\"", "\\\"")

unicode_punctuation_re = re.compile(r'[\u0387\u0373.,\u2014]')

def remove_punctuation_Unicode(unicode_greek):
    return unicode_punctuation_re.sub(r'', unicode_greek)
