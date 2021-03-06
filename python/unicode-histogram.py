#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
try:
    import simplejson as json
except:
    import json

from collections import Counter
import unicodedata

from time import strftime, gmtime

"""
12 December 2014
for each of {body, title}:
  the unicodeSignature is the sequence of >ascii codepoints, in order, space-separated
  the unicodeCatalog is the bag of >ascii codepoints, sorted/agglomerated using space, comma-separated
  the unicodeHistogram is a json-encoded python dict/json object mapping codepoint to count

  the unicodeBlockSignature is the sequence of block descriptors (of all >ascii), in order, space-separated
  the unicodeBlockCatalog is the bag of block descriptors, sorted/agglomerated using space, comma-separated
  the unicodeBlockHistogram is a json-encoded python dict/json object mapping block descriptor to count

  the unicodeCategorySignature is the sequence of category descriptors (of all >ascii), in order, space-separated
  the unicodeCategoryCatalog is the bag of category descriptors, sorted/agglomerated using space, comma-separated
  the unicodeCategoryHistogram is a json-encoded python dict/json object mapping category descriptor to count

  where block and category descriptors are defined via
    # From http://stackoverflow.com/a/245072
    # retrieved from http://unicode.org/Public/UNIDATA/Blocks.txt
    # Blocks-5.1.0.txt
    # Date: 2008-03-20, 17:41:00 PDT [KW]
  and is formatted to using _ rather than ,/space/-
"""

def isAscii(c):
    try:
        return ord(c) <= 127
    except:
        return False

def gentime():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def fmtCodepoint(codepoint, style):
    return codepoint

def fmtMetadatum(metadatum, style):
    def fmtValue(s):
        return re.sub("[ -]", "_", re.sub(",", "", unicode(s)))

    if style=="category":
        category = categoryCodeDescription(unicodedata.category(metadatum))
        # return "category:" + fmtValue(category)
        return fmtValue(category)
    elif style=="block":
        # return "block:" + fmtValue(block(metadatum))
        return fmtValue(block(metadatum))
    else:
        return None

# From http://stackoverflow.com/a/245072

_blocks = []

def _initBlocks(text):
    pattern = re.compile(r'([0-9A-F]+)\.\.([0-9A-F]+);\ (\S.*\S)')
    for line in text.splitlines():
        m = pattern.match(line)
        if m:
            start, end, name = m.groups()
            _blocks.append((int(start, 16), int(end, 16), name))

# retrieved from http://unicode.org/Public/UNIDATA/Blocks.txt
_initBlocks('''
# Blocks-5.1.0.txt
# Date: 2008-03-20, 17:41:00 PDT [KW]
#
# Unicode Character Database
# Copyright (c) 1991-2008 Unicode, Inc.
# For terms of use, see http://www.unicode.org/terms_of_use.html
# For documentation, see UCD.html
#
# Note:   The casing of block names is not normative.
#         For example, "Basic Latin" and "BASIC LATIN" are equivalent.
#
# Format:
# Start Code..End Code; Block Name

# ================================================

# Note:   When comparing block names, casing, whitespace, hyphens,
#         and underbars are ignored.
#         For example, "Latin Extended-A" and "latin extended a" are equivalent.
#         For more information on the comparison of property values, 
#            see UCD.html.
#
#  All code points not explicitly listed for Block
#  have the value No_Block.

# Property: Block
#
# @missing: 0000..10FFFF; No_Block

0000..007F; Basic Latin
0080..00FF; Latin-1 Supplement
0100..017F; Latin Extended-A
0180..024F; Latin Extended-B
0250..02AF; IPA Extensions
02B0..02FF; Spacing Modifier Letters
0300..036F; Combining Diacritical Marks
0370..03FF; Greek and Coptic
0400..04FF; Cyrillic
0500..052F; Cyrillic Supplement
0530..058F; Armenian
0590..05FF; Hebrew
0600..06FF; Arabic
0700..074F; Syriac
0750..077F; Arabic Supplement
0780..07BF; Thaana
07C0..07FF; NKo
0900..097F; Devanagari
0980..09FF; Bengali
0A00..0A7F; Gurmukhi
0A80..0AFF; Gujarati
0B00..0B7F; Oriya
0B80..0BFF; Tamil
0C00..0C7F; Telugu
0C80..0CFF; Kannada
0D00..0D7F; Malayalam
0D80..0DFF; Sinhala
0E00..0E7F; Thai
0E80..0EFF; Lao
0F00..0FFF; Tibetan
1000..109F; Myanmar
10A0..10FF; Georgian
1100..11FF; Hangul Jamo
1200..137F; Ethiopic
1380..139F; Ethiopic Supplement
13A0..13FF; Cherokee
1400..167F; Unified Canadian Aboriginal Syllabics
1680..169F; Ogham
16A0..16FF; Runic
1700..171F; Tagalog
1720..173F; Hanunoo
1740..175F; Buhid
1760..177F; Tagbanwa
1780..17FF; Khmer
1800..18AF; Mongolian
1900..194F; Limbu
1950..197F; Tai Le
1980..19DF; New Tai Lue
19E0..19FF; Khmer Symbols
1A00..1A1F; Buginese
1B00..1B7F; Balinese
1B80..1BBF; Sundanese
1C00..1C4F; Lepcha
1C50..1C7F; Ol Chiki
1D00..1D7F; Phonetic Extensions
1D80..1DBF; Phonetic Extensions Supplement
1DC0..1DFF; Combining Diacritical Marks Supplement
1E00..1EFF; Latin Extended Additional
1F00..1FFF; Greek Extended
2000..206F; General Punctuation
2070..209F; Superscripts and Subscripts
20A0..20CF; Currency Symbols
20D0..20FF; Combining Diacritical Marks for Symbols
2100..214F; Letterlike Symbols
2150..218F; Number Forms
2190..21FF; Arrows
2200..22FF; Mathematical Operators
2300..23FF; Miscellaneous Technical
2400..243F; Control Pictures
2440..245F; Optical Character Recognition
2460..24FF; Enclosed Alphanumerics
2500..257F; Box Drawing
2580..259F; Block Elements
25A0..25FF; Geometric Shapes
2600..26FF; Miscellaneous Symbols
2700..27BF; Dingbats
27C0..27EF; Miscellaneous Mathematical Symbols-A
27F0..27FF; Supplemental Arrows-A
2800..28FF; Braille Patterns
2900..297F; Supplemental Arrows-B
2980..29FF; Miscellaneous Mathematical Symbols-B
2A00..2AFF; Supplemental Mathematical Operators
2B00..2BFF; Miscellaneous Symbols and Arrows
2C00..2C5F; Glagolitic
2C60..2C7F; Latin Extended-C
2C80..2CFF; Coptic
2D00..2D2F; Georgian Supplement
2D30..2D7F; Tifinagh
2D80..2DDF; Ethiopic Extended
2DE0..2DFF; Cyrillic Extended-A
2E00..2E7F; Supplemental Punctuation
2E80..2EFF; CJK Radicals Supplement
2F00..2FDF; Kangxi Radicals
2FF0..2FFF; Ideographic Description Characters
3000..303F; CJK Symbols and Punctuation
3040..309F; Hiragana
30A0..30FF; Katakana
3100..312F; Bopomofo
3130..318F; Hangul Compatibility Jamo
3190..319F; Kanbun
31A0..31BF; Bopomofo Extended
31C0..31EF; CJK Strokes
31F0..31FF; Katakana Phonetic Extensions
3200..32FF; Enclosed CJK Letters and Months
3300..33FF; CJK Compatibility
3400..4DBF; CJK Unified Ideographs Extension A
4DC0..4DFF; Yijing Hexagram Symbols
4E00..9FFF; CJK Unified Ideographs
A000..A48F; Yi Syllables
A490..A4CF; Yi Radicals
A500..A63F; Vai
A640..A69F; Cyrillic Extended-B
A700..A71F; Modifier Tone Letters
A720..A7FF; Latin Extended-D
A800..A82F; Syloti Nagri
A840..A87F; Phags-pa
A880..A8DF; Saurashtra
A900..A92F; Kayah Li
A930..A95F; Rejang
AA00..AA5F; Cham
AC00..D7AF; Hangul Syllables
D800..DB7F; High Surrogates
DB80..DBFF; High Private Use Surrogates
DC00..DFFF; Low Surrogates
E000..F8FF; Private Use Area
F900..FAFF; CJK Compatibility Ideographs
FB00..FB4F; Alphabetic Presentation Forms
FB50..FDFF; Arabic Presentation Forms-A
FE00..FE0F; Variation Selectors
FE10..FE1F; Vertical Forms
FE20..FE2F; Combining Half Marks
FE30..FE4F; CJK Compatibility Forms
FE50..FE6F; Small Form Variants
FE70..FEFF; Arabic Presentation Forms-B
FF00..FFEF; Halfwidth and Fullwidth Forms
FFF0..FFFF; Specials
10000..1007F; Linear B Syllabary
10080..100FF; Linear B Ideograms
10100..1013F; Aegean Numbers
10140..1018F; Ancient Greek Numbers
10190..101CF; Ancient Symbols
101D0..101FF; Phaistos Disc
10280..1029F; Lycian
102A0..102DF; Carian
10300..1032F; Old Italic
10330..1034F; Gothic
10380..1039F; Ugaritic
103A0..103DF; Old Persian
10400..1044F; Deseret
10450..1047F; Shavian
10480..104AF; Osmanya
10800..1083F; Cypriot Syllabary
10900..1091F; Phoenician
10920..1093F; Lydian
10A00..10A5F; Kharoshthi
12000..123FF; Cuneiform
12400..1247F; Cuneiform Numbers and Punctuation
1D000..1D0FF; Byzantine Musical Symbols
1D100..1D1FF; Musical Symbols
1D200..1D24F; Ancient Greek Musical Notation
1D300..1D35F; Tai Xuan Jing Symbols
1D360..1D37F; Counting Rod Numerals
1D400..1D7FF; Mathematical Alphanumeric Symbols
1F000..1F02F; Mahjong Tiles
1F030..1F09F; Domino Tiles
20000..2A6DF; CJK Unified Ideographs Extension B
2F800..2FA1F; CJK Compatibility Ideographs Supplement
E0000..E007F; Tags
E0100..E01EF; Variation Selectors Supplement
F0000..FFFFF; Supplementary Private Use Area-A
100000..10FFFF; Supplementary Private Use Area-B

# EOF
''')

def block(ch):
    '''
    Return the Unicode block name for ch, or None if ch has no block.
    
    >>> block(u'a')
    'Basic Latin'
    >>> block(unichr(0x0b80))
    'Tamil'
    >>> block(unichr(0xe0080))
    
    '''

    assert isinstance(ch, unicode) and len(ch) == 1, repr(ch)
    cp = ord(ch)
    for start, end, name in _blocks:
        if start <= cp <= end:
            return name

categoryCodeDescriptions = {'Cc': "Other, Control",
                            'Cf': "Other, Format",
                            # 'Cn': "Other, Not Assigned (no characters in the file have this property)",
                            'Cn': "Other, Not Assigned",
                            'Co': "Other, Private Use",
                            'Cs': "Other, Surrogate",
                            'LC': "Letter, Cased",
                            'Ll': "Letter, Lowercase",
                            'Lm': "Letter, Modifier",
                            'Lo': "Letter, Other",
                            'Lt': "Letter, Titlecase",
                            'Lu': "Letter, Uppercase",
                            'Mc': "Mark, Spacing Combining",
                            'Me': "Mark, Enclosing",
                            'Mn': "Mark, Nonspacing",
                            'Nd': "Number, Decimal Digit",
                            'Nl': "Number, Letter",
                            'No': "Number, Other",
                            'Pc': "Punctuation, Connector",
                            'Pd': "Punctuation, Dash",
                            'Pe': "Punctuation, Close",
                            # 'Pf': "Punctuation, Final quote (may behave like Ps or Pe depending on usage)",
                            # 'Pi': "Punctuation, Initial quote (may behave like Ps or Pe depending on usage)",
                            'Pf': "Punctuation, Final quote",
                            'Pi': "Punctuation, Initial quote",
                            'Po': "Punctuation, Other",
                            'Ps': "Punctuation, Open",
                            'Sc': "Symbol, Currency",
                            'Sk': "Symbol, Modifier",
                            'Sm': "Symbol, Math",
                            'So': "Symbol, Other",
                            'Zl': "Separator, Line",
                            'Zp': "Separator, Paragraph",
                            'Zs': "Separator, Space"}

def categoryCodeDescription(category):
    return categoryCodeDescriptions.get(category, "Not Available")

def analyze(part):
    content = part["text"]
    codepointSeq = []
    categorySeq = []
    blockSeq = []
    codepointHisto = Counter()
    categoryHisto = Counter()
    blockHisto = Counter()
    for c in content:
        if not isAscii(c):
            codepointHisto[c] += 1
            codepointSeq.append(c)
            cat = fmtMetadatum(c, 'category')
            blk = fmtMetadatum(c, 'block')
            if cat:
                categoryHisto[cat] += 1
                categorySeq.append(cat)
            if blk:
                blockHisto[blk] += 1
                blockSeq.append(blk)
            # Normal form KD
            # presumed of minor importance: omitted for now
            # categoryHisto["normalized:" + unicodedata.normalize(c.decode('utf-8'),'NFKD')] += 1
    contentElements = codepointSeq
    # Histogram: JSON-encoded string repn of the dict
    part["unicodeHistogram"] = json.dumps(codepointHisto)
    # Signature: sequence of codepoints
    part["unicodeSignature"] = " ".join(codepointSeq)
    # Catalog: bag of codepoints
    codepointCatalogElements = []
    for k in sorted(codepointHisto.keys()):
        v = codepointHisto[k]
        # v copies of this key
        codepointCatalogElements.append(" ".join([k for _ in xrange(v)]))
    part["unicodeCatalog"] = ", ".join(codepointCatalogElements)

    # Histogram: JSON-encoded string repn of the dict
    part["unicodeCategoryHistogram"] = json.dumps(categoryHisto)
    # Signature: sequence of codepoints
    part["unicodeCategorySignature"] = " ".join(categorySeq)
    # Catalog: bag of categories
    categoryCatalogElements = []
    for k in sorted(categoryHisto.keys()):
        v = categoryHisto[k]
        # v copies of this key
        categoryCatalogElements.append(" ".join([k for _ in xrange(v)]))
    part["unicodeCategoryCatalog"] = ", ".join(categoryCatalogElements)

    # Histogram: JSON-encoded string repn of the dict
    part["unicodeBlockHistogram"] = json.dumps(blockHisto)
    # Signature: sequence of codepoints
    part["unicodeBlockSignature"] = " ".join(blockSeq)
    # Catalog: bag of blocks
    blockCatalogElements = []
    for k in sorted(blockHisto.keys()):
        v = blockHisto[k]
        # v copies of this key
        blockCatalogElements.append(" ".join([k for _ in xrange(v)]))
    part["unicodeBlockCatalog"] = ", ".join(blockCatalogElements)

    return part

# Test data
# HEART = u'\u2665'
# SMILY = u'\u263a'
# TSU = u'\u30C4'
# LEFT = u'\u27E8'
# RIGHT = u'\u27E9'
# EURO = u'\u20AC'

# if True:

#    TESTUNICODE = LEFT + "h" + EURO + "llo " + HEART + HEART + SMILY + TSU + " goodby" + EURO + " " + SMILY + TSU + HEART + HEART + HEART + HEART + RIGHT

#    print len(TESTUNICODE)
#    print json.dumps(TESTUNICODE)

#    TESTDOC = {"@context": "http://localhost:8080/publish/JSON/WSP1WS6-select unix_timestamp(a_importtime)*1000 as timestamp, a_* from ads a join sample s on a_id=s_id limit 50-context.json","schema:provider": {"a": "Organization", "uri": "http://memex.zapto.org/data/organization/1"}, "snapshotUri": "http://memex.zapto.org/data/page/850753E7323B188B93E6E28F730F2BFBFB1CE00B/1396493689000/raw","a": "WebPage","dateCreated": "2013-09-24T18:28:00","hasBodyPart": {"text": TESTUNICODE, "a": "WebPageElement"}, "hasTitlePart": {"text": "\u270b\u270b\u270bOnly Best \u270c\u270c\u270c Forget The Rest \u270b\u270b\u270b Outcall Specials TONIGHT \u270c\ud83d\udc8b\ud83d\udc45 Sexy Blonde is UP LATE \ud83d\udc9c\ud83d\udc9b\u270b\u270c - 25", "a": "WebPageElement"}, "uri": "http://memex.zapto.org/data/page/850753E7323B188B93E6E28F730F2BFBFB1CE00B/1396493689000/processed"}

#    analyze(TESTDOC["hasBodyPart"])
#    json.dump(TESTDOC, sys.stdout, indent=4);
#    exit(0)

for line in sys.stdin:
    try:
        (url, jrep) = line.split('\t')
        d = json.loads(jrep)

        analyze(d["hasBodyPart"])
        analyze(d["hasTitlePart"])
        # insert gmtime
        # ensure it doesn't collide with any other gentime
        d["unicodeGentime"] = gentime()

        print url + "\t",
        json.dump(d, sys.stdout, sort_keys=True)
        print
    except ValueError as e:
        print >> sys.stderr, e
        pass
