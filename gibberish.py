# coding=utf-8
"""Create gibberish from source alphabets."""

import os
import json
import random
import sys
import unicodedata
from randomness import WanderingMonsterTable, COMMON, UNCOMMON, RARE, VERY_RARE

import data

CUSTOM_ALPHABETS = {
    "Dice": u"\N{Die Face-1}\N{Die Face-2}\N{Die Face-3}\N{Die Face-4}\N{Die Face-5}\N{Die Face-6}",
    "Circled Letters": u"⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
    "Circled Alphanumerics": u"①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ⓪⓫⓬⓭⓮⓯⓰⓱⓲⓳⓴⓵⓶⓷⓸⓹⓺⓻⓼⓽⓾❶❷❸❹❺❻❼❽❾❿➀➁➂➃➄➅➆➇➈➉➊➋➌➍➎➏➐➑➒➓㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚㉛㉜㉝㉞㉟㊱㊲㊳㊴㊵㊶㊷㊸㊹㊺㊻㊼㊽㊾㊿♳♴♵♶♷♸♹",
    "Stars": u"✢✣✤✥✦✧✨✩✪✫✬✭✮✯✰✱✲✳✴✵✶✷✸✹✺✻✼✽✾✿❀❁❂❃❄❅❆❇❈❉❊❋*͙⁎⁑⃰∗⊛⧆﹡＊٭≛⋆⍟⍣★☆☪⚝✡✦✧⭐⭑⭒",
    "Symbology": u"☀☁☂☃☄★☆☎☏☔☕☚☛☠☢☤☭☮☯☹☺☻☼♫⚐⚑⚒⚓⚔⚕⚖♻✄✌✍✏♀♂⌚",
    "Crossouts": u"Xxˣ͓̽ͯᶍẊẋẌẍₓ⒳Ⓧⓧ☒✕✖✗✘Ｘｘ𝁪𝅃𝅅𝐗𝐱𝑋𝑥𝑿𝒙𝒳𝓍𝓧𝔁𝔛𝔵𝕏𝕩𝖃𝖝𝖷𝗑𝗫𝘅𝘟𝘹𝙓𝙭𝚇𝚡×⨯ⵝ᙭Ҳ⚔⤧ҳ⤩᙮ⅹⅩ⤨⤪⨉⤫⤬",
    }

class Alphabet:

    @classmethod
    def _fill_by_name(cls, data=None):
        for c in data:
            name = c['name']
            if 'characters' in c and len(c['characters']) > 0:
                cls.by_name[name] = c
            if 'child' in c:
                cls._fill_by_name(c['child'])

        # Also add in custom alphabets
        for name, chars in CUSTOM_ALPHABETS.items():
            cls.by_name[name] = dict(characters=chars)

    by_name = {}

    @classmethod
    def random_choice(cls, *alphabets):
        """A random choice among alphabets"""
        if not alphabets:
            alphabets = cls.by_name.keys()
        choice = random.choice(alphabets)
        return cls.characters([choice])

    @classmethod
    def random_choice_no_modifiers(cls):
        """A completely random choice among non-modifier alphabets."""
        choice = None
        while choice is None:
            choice = random.choice(Alphabet.by_name.keys())
            if choice in Alphabet.MODIFIERS:
                choice = None
        # print "Choice: %s, len: %s" % (choice, len(cls.characters(choice)))
        return cls.characters(choice)

    @classmethod
    def characters(cls, alphabets):
        char = []
        if isinstance(alphabets, basestring):
            alphabets = [alphabets]
        # print "Character lookup for %r" % alphabets
        for alphabet in alphabets:
            # print "Looking up %s" % alphabet
            if isinstance(alphabet, list):
                char.extend(cls.characters(alphabet))
            else:
                char.extend(cls.by_name[alphabet]['characters'])
        return ''.join(char)

    # Some combination European alphabets
    ASCII = "Basic Latin (ASCII)"
    LATIN_1 = [ASCII, "Latin-1 Supplement"]
    LATIN_EXTRAS = [
        "Latin Extended-A", "Latin Extended-B",
        "Latin Extended-C", "Latin Extended-D",
        "Latin Extended Additional", "Latin Ligatures"]
    LATIN_FULL = LATIN_1 + LATIN_EXTRAS
    CYRILLIC = ["Cyrillic"]
    CYRILLIC_FULL = ["Cyrillic", "Cyrillic Supplement", "Cyrillic Extended-A", "Cyrillic Extended-B"]

    LATIN_S = [ASCII, LATIN_1, LATIN_FULL, "Circled Letters", "Circled Alphanumerics"]

    CYRILLIC_S = [CYRILLIC, CYRILLIC_FULL]

    # A set of European alphabets.
    EUROPEAN_S = [
        ASCII, LATIN_1, LATIN_FULL, CYRILLIC, CYRILLIC_FULL,
        ["Armenian", "Armenian Ligatures"],
        ["Coptic"],        
        ["Georgian"],
        ["Georgian", "Georgian Supplement"],
        ["Glagolitic"],
        ["Gothic"],
        ["Greek"],
        ["Greek", "Greek Extended"],
        ["Ogham"],
        ["Old Italic"],
        ["Runic"]
        ]

    # Some combination African alphabets.
    ETHIOPIC = ["Ethiopic"]
    ETHIOPIC_FULL = ["Ethiopic", "Ethiopic Supplement", "Ethiopic Extended", "Ethiopic Extended-A"]

    # A set of African alphabets.
    AFRICAN_S = [ETHIOPIC_FULL, "N'Ko", "Osmanya", "Tifinagh", "Vai"]

    # Some combination Middle Eastern alphabets.
    ARABIC = ["Arabic"]
    ARABIC_FULL = ARABIC + ["Arabic Supplement"]
    ARABIC_WITH_PRESENTATION_FORMS = ARABIC + ["Arabic Presentation Forms-B"]
    HEBREW = ["Hebrew"]
    HEBREW_WITH_PRESENTATION_FORMS = HEBREW + ["Hebrew Presentation Forms"]

    # A set of Middle Eastern alphabets.
    MIDDLE_EASTERN_S = [
        ARABIC, ARABIC_FULL, ARABIC_WITH_PRESENTATION_FORMS,
        HEBREW, HEBREW_WITH_PRESENTATION_FORMS,
        "Old Persian",
        "Ugaritic",
        "Phoenician",
        "Syriac"
        ]

    # A set of Central Asian alphabets.
    CENTRAL_ASIAN_S = [
        "Tibetan",
        ]

    # Some combination South Asian alphabets
    DEVANAGARI = ["Devanagari"]
    DEVANAGARI_EXTENDED = DEVANAGARI + ["Devanagari Extended"]

    # A set of South Asian alphabets
    SOUTH_ASIAN_S = [
        DEVANAGARI,
        DEVANAGARI_EXTENDED,
        "Bengali and Assamese",
        "Gujarati",
        "Gurmukhi",
        "Kannada",
        "Malayalam",
        "Oriya",
        "Sinhala",
        "Tamil",
        "Telugu",
        "Thaana"
        ]

    # Some combination Southeast Asian alphabets
    KHMER = ["Khmer"]
    KHMER_WITH_SYMBOLS = KHMER + ["Khmer Symbols"]
    MYANMAR = ["Myanmar"]
    MYANMAR_EXTENDED = MYANMAR + ["Myanmar Extended-A"]

    # A set of Southeast Asian alphabets
    SOUTHEAST_ASIAN_S = [
        KHMER,
        KHMER_WITH_SYMBOLS,
        MYANMAR,
        MYANMAR_EXTENDED,
        "Buginese",
        "Kayah Li",
        "Lao",
        "Tai Le",
        "Thai",
        ]

    # A set of Phillipine alphabets
    PHILLIPINE_S = [
        "Hanunoo",
        ]

    # Some combination East Asian alphabets.
    HANGUL_JAMO = ["Hangul Jamo"]
    HANGUL_JAMO_WITH_COMPATIBILITY = HANGUL_JAMO + ["Hangul Compatibility Jamo"]
    KATAKANA = ["Katakana"]
    KATAKANA_ALL = KATAKANA + ["Katakana Phonetic Extensions"]

    # A set of East Asian alphabets
    EAST_ASIAN_S = [
        "Bopomofo",
        "CJK Unified Ideographs (Han)",
        "CJK Compatibility Ideographs",
        # "CJK Radicals  KangXi Radicals", # Name is weird
        "Hangul Syllables",
        "Hiragana",
        HANGUL_JAMO,
        HANGUL_JAMO_WITH_COMPATIBILITY,
        KATAKANA,
        KATAKANA_ALL,
        ]

    # Some combination American alphabets
    UCAS = "Unified Canadian Aboriginal Syllabics"
    UCAS_ALL = ["Unified Canadian Aboriginal Syllabics", "UCAS Extended"]

    # A set of American alphabets
    AMERICAN_S = ["Cherokee",
                  "Deseret",
                  UCAS,
                  UCAS_ALL]

    # All available alphabets that are used to convey human language.
    ALL_LANGUAGE_ALPHABETS_S = (EUROPEAN_S + AFRICAN_S + MIDDLE_EASTERN_S
                                + CENTRAL_ASIAN_S + SOUTH_ASIAN_S
                                + SOUTHEAST_ASIAN_S + PHILLIPINE_S
                                + EAST_ASIAN_S + AMERICAN_S)

    # Ways to modify characters.
    DIACRITICAL = ["Combining Diacritical Marks"]
    DIACRITICAL_FULL = DIACRITICAL + [
        "Combining Diacritical Marks Supplement",
        "Combining Half Marks",
        "Combining Diacritical Marks for Symbols"]
    MODIFIERS = DIACRITICAL_FULL

    # "Weird Twitter" versions of Latin characters
    WEIRD_TWITTER_LATIN = [
        "Fullwidth ASCII Punctuation",
        "Superscripts and Subscripts",
        "Mathematical Alphanumeric Symbols",
        "Letterlike Symbols",
        "Enclosed Alphanumerics",
        "Enclosed Alphanumeric Supplement",
        "Additional Squared Symbols",
        "Control Pictures",
        "Braille Patterns",
        "IPA Extensions",
        "Phonetic Extensions",
        "Phonetic Extensions Supplement",
        "Old Italic",
        "Circled Letters",
        "Circled Alphanumerics",
        ]

    # "Weird Twitter" mixins for Latin characters.
    WEIRD_TWITTER_LATIN_MIXINS = [
        "Alphabetic Presentation Forms",
        "General Punctuation",
        "Latin-1 Punctuation",
        "Small Form Variants",
        "Currency Symbols",
        "Dollar Sign",
        "Yen, Pound and Cent",
        "Rial Sign",
        "Vertical Forms",
        "Number Forms",
        "Fullwidth ASCII Digits",
        "Modifier Tone Letters",
        "Spacing Modifier Letters",
        "CJK Compatibility",
        ]

    # "Weird Twitter" versions of Japanese characters
    WEIRD_TWITTER_JAPANESE = [
        "Halfwidth and Fullwidth Forms",
        "Fullwidth ASCII Digits",
        "Halfwidth Katakana",
        ]

    # "Weird Twitter" mixins for Japanese characters
    WEIRD_TWITTER_JAPANESE_MIXINS = [
        "CJK Compatibility Ideographs",
        "Fullwidth ASCII Punctuation",
        "Vertical Forms",
        "CJK Symbols and Punctuation",
        "CJK Compatibility Forms",
        "Enclosed CJK Letters and Months",
        ]

    # "Weird Twitter" for the Han unification plane
    WEIRD_TWITTER_CJK = [
        "Bopomofo",
        "CJK Compatibility Ideographs",
        "CJK Radicals / KangXi Radicals"
        ]

    # "Weird Twitter" mixins for the Han unification plane
    WEIRD_TWITTER_CJK_MIXINS = WEIRD_TWITTER_JAPANESE_MIXINS + [
        "CJK Compatibility"]

    # "Weird Twitter" math glyphs
    WEIRD_TWITTER_MATH = [
        "Number Forms",
        "Fullwidth ASCII Digits",
        "Superscripts and Subscripts",
        ]

    WEIRD_TWITTER_MATH_MIXINS = [
        "Mathematical Operators",
        "Supplemental Mathematical Operators",
        "Miscellaneous Mathematical Symbols-A",
        "Floors and Ceilings",
        ]

    # Symbolic glyphs
    SYMBOLIC_ALPHABETS = [
        "APL symbols",
        "Miscellaneous Technical",
        "Optical Character Recognition (OCR)",
        "Arrows",
        "Supplemental Arrows-A",
        "Supplemental Arrows-B",
        "Additional Arrows",
        "Dingbats",
        "Emoticons",
        "Musical Symbols",
        "Byzantine Musical Symbols",
        ]

    # Gaming glyphs
    GAMING_ALPHABETS = [
        "Chess, Checkers/Draughts",
        "Dice",
        "Domino Tiles",
        "Japanese Chess",
        "Mahjong Tiles",
        "Playing Cards",
        "Card suits",
        ]

    # Geometric glyphs, and glyphs designed for other purposes that
    # have geometric appeal
    GEOMETRIC_ALPHABETS = [
        "Geometric Shapes",
        # "CJK Compatibility Forms",
        "Additional Shapes",
        "Box Drawing",
        "Block Elements",
        "Braille Patterns",
        "Yijing Mono-, Di- and Trigrams",
        "Stars",
        ]

    # Yijing symbols
    YIJING = [
        "Yijing Mono-, Di- and Trigrams",
        "Yijing Hexagram Symbols",
        "Tai Xuan Jing Symbols",
        ]

    # Small glitchy alphabets that can be tossed in almost anywhere.
    GLITCHES = [
        "Optical Character Recognition (OCR)",
        "Floors and Ceilings",
        "Shading Mosaic", # Custom alphabet
        "One Dot", # Custom alphabet
        "Fill Mosaic", # Custom alphabet
        ]

    # Custom alphabets 
    CUSTOM_S = [
        "Geometric Shapes",
        ["Geometric Shapes", "Arrows"],
        ["Geometric Shapes", "Additional Shapes"],
        ["Geometric Shapes", "Additional Shapes", "Box Drawing", "Block Elements"],
        "Box Drawing",
        "Block Elements",
        ["Box Drawing", "Block Elements"],
        ["Box Drawing", "Block Elements", "Optical Character Recognition (OCR)"],
        "Optical Character Recognition (OCR)",
        "Braille Patterns",
        ["Braille Patterns", "Optical Character Recognition (OCR)"],
        ["Dingbats", "Miscellaneous Symbols"],
        ["Dingbats", "Emoticons", "Miscellaneous Symbols"],
        ["Dingbats", "Emoticons", "Miscellaneous Symbols", "Miscellaneous Symbols and Arrows"],
        ["Basic Latin (ASCII)", "Emoticons"],
        "Chess, Checkers/Draughts",
        "Domino Tiles",
        "Playing Cards",
        "Mahjong Tiles",
        "Dice",
        ["Dice", "Domino Tiles"],
        ["Playing Cards", "Card suits"],
        "Yijing Mono-, Di- and Trigrams",
        "Yijing Hexagram Symbols",
        "Tai Xuan Jing Symbols",
        ["Yijing Mono-, Di- and Trigrams", "Yijing Hexagram Symbols", "Tai Xuan Jing Symbols"],
        ["Yijing Mono-, Di- and Trigrams", "Yijing Hexagram Symbols", "Tai Xuan Jing Symbols", "Braille Patterns", "Optical Character Recognition (OCR)"],
        ["Hiragana", "Katakana"],
        ]

    def unicode_charset(name, *chrs):
        charset = "".join(map(unicodedata.lookup, chrs))
        CUSTOM_ALPHABETS[name] = charset
        return charset

    # Custom alphabets
    UP_POINTING_TRIANGLES = unicode_charset("Up-Pointing Triangles",
        "Apl functional symbol delta stile",
        "Black lower left triangle",
        "Black lower right triangle",
        "Black up-pointing small triangle",
        "Black up-pointing triangle",
        "Canadian syllabics glottal stop",
        "Canadian syllabics i",
        "Combining enclosing upward pointing triangle",
        "Coptic capital letter dalda",
        "Coptic small letter dalda",
        "Cyrillic capital letter closed little yus",
        "Cyrillic small letter little yus",
        "Greek capital letter delta",
        "Increment",
        "Mathematical bold capital delta",
        "Mathematical bold italic capital delta",
        "Minus sign in triangle",
        "Segment",
        "Tifinagh letter yav",
        "Triangle with dot above",
        "Triangle with serifs at bottom",
        "Triangle with underbar",
        "Up-pointing triangle with left half black",
        "Up-pointing triangle with right half black",
        "Lower left triangle",
        "Lower right triangle",
        "White trapezium",
        "White up-pointing small triangle",
        "White up-pointing small triangle",
        "White up-pointing triangle",
        #            "Alchemical symbol for fire",
        )

    DOWN_POINTING_TRIANGLES = unicode_charset("Down-Pointing Triangles",
        "Apl functional symbol del stile",
        "Black down-pointing small triangle",
        "Black down-pointing triangle",
        "Canadian syllabics carrier ru",
        "Canadian syllabics e",
        "Canadian syllabics pe",
        "Down-pointing triangle with left half black",
        "Down-pointing triangle with right half black",
        "For all",
        "Latin capital letter v",
        "Mathematical bold capital v",
        "Mathematical bold italic nabla",
        "Mathematical bold nabla",
        "Mathematical bold small v",
        "Mathematical italic nabla",
        "Mathematical monospace capital v",
        "Mathematical monospace small v",
        "Mathematical sans-serif bold nabla",
        "Mathematical sans-serif capital v",
        "Nabla",
        "Tifinagh letter yadh",
        "Vai symbol kung",
        "White down-pointing small triangle",
        "White down-pointing triangle",
        #            "Alchemical symbol for aquafortis"
        #            "Alchemical symbol for dissolve-2",
        #            "Alchemical symbol for water",
        #            "Greek vocal notation symbol-21",
        #            "Heavy white down-pointing triangle",
        )

    LEFT_POINTING_TRIANGLES = unicode_charset("Left-Pointing Triangles",
        "Apl functional symbol quad less-than",
        "Black left-pointing pointer",
        "Black left-pointing small triangle",
        "Black left-pointing triangle",
        "Canadian syllabics a",
        "Canadian syllabics carrier ra",
        "Canadian syllabics p",
        "Canadian syllabics pa",
        "Normal subgroup of",
        "Spherical angle",
        "Lower right triangle",
        "Upper right triangle",
        "Black upper right triangle",
        "Black lower right triangle",
        "Vai syllable gboo",
        "White left-pointing pointer",
        "White left-pointing small triangle",
        "White left-pointing triangle",
        # "Closed subset",
        # "Greek instrumental notation symbol-38",
        # "Large left triangle operator",
        # "Less-than closed by curve",
        #"Z notation domain antirestriction",
        )

    RIGHT_POINTING_TRIANGLES = unicode_charset("Right-Pointing Triangles",
        "Apl functional symbol quad greater-than",
        "Black lower right triangle",
        "Black right-pointing small triangle",
        "Black right-pointing triangle",
        "Black upper left triangle",
        "Canadian syllabics carrier hwee",
        "Canadian syllabics carrier i",
        "Canadian syllabics carrier re",
        "Canadian syllabics carrier we",
        "Canadian syllabics fo",
        "Canadian syllabics o",
        "Contains as normal subgroup",
        "Greater-than sign",
        "Lower right triangle",
        "Spherical angle opening left",
        "Succeeds",
        "Triangular bullet",
        "Upper left triangle",
        "White right-pointing pointer",
        "White right-pointing small triangle",
        "White right-pointing triangle",
        # "Closed superset",
        # "Conical taper",
        # "Greater-than closed by curve",
        # "Greek instrumental notation symbol-37",
        # "Z notation range antirestriction",
        )

    TRIANGLES = UP_POINTING_TRIANGLES + DOWN_POINTING_TRIANGLES + LEFT_POINTING_TRIANGLES + RIGHT_POINTING_TRIANGLES

    QUADRILATERALS = unicode_charset("Quadrilaterals",
        "Apl functional symbol quad backslash",
        "Apl functional symbol quad slash",
        "Apl functional symbol quad",
        "Apl functional symbol quote quad",
        "Apl functional symbol squish quad",
        "Ballot box",
        "Black large square",
        "Black medium small square",
        "Black medium square",
        "Black parallelogram",
        "Black small square",
        "Black square",
        "Combining enclosing screen",
        "Combining enclosing square",
        "Flatness",
        "Hebrew letter wide final mem",
        "Katakana letter ro",
        "Lower right drop-shadowed white square",
        "Lower right shadowed white square",
        "Square lozenge",
        "Upper right drop-shadowed white square",
        "Upper right shadowed white square",
        "Viewdata square",
        "White large square",
        "White medium small square",
        "White medium square",
        "White parallelogram",
        "White small square",
        "White square with rounded corners",
        "White square",
        "White trapezium",
        "X in a rectangle box",
        #"Square with contoured outline",
        #"Ticket",
        "BALLOT BOX WITH CHECK", #☑
        "BALLOT BOX WITH X", #☒
        "MUSICAL SYMBOL SQUARE NOTEHEAD WHITE", #𝅆
        "MUSICAL SYMBOL SQUARE NOTEHEAD BLACK", #𝅇
        "SQUARE WITH TOP HALF BLACK", #⬒
        "SQUARE WITH BOTTOM HALF BLACK", #⬓
        "SQUARE WITH UPPER RIGHT DIAGONAL HALF BLACK", #⬔
        "SQUARE WITH LOWER LEFT DIAGONAL HALF BLACK", #⬕
        "DOTTED SQUARE", #⬚
        "TWO JOINED SQUARES", #⧉
        "WHITE SQUARE WITH LEFTWARDS TICK", #⟤
        "WHITE SQUARE WITH RIGHTWARDS TICK", #⟥
        "SQUARE WITH LEFT HALF BLACK", #◧
        "SQUARE WITH RIGHT HALF BLACK", #◨
        "SQUARE WITH UPPER LEFT DIAGONAL HALF BLACK", #◩
        "SQUARE WITH LOWER RIGHT DIAGONAL HALF BLACK", #◪
        "WHITE SQUARE CONTAINING BLACK SMALL SQUARE", #▣
        "SQUARE WITH HORIZONTAL FILL", #▤
        "SQUARE WITH VERTICAL FILL", #▥
        "SQUARE WITH ORTHOGONAL CROSSHATCH FILL", #▦
        "SQUARE WITH UPPER LEFT TO LOWER RIGHT FILL", #▧
        "SQUARE WITH UPPER RIGHT TO LOWER LEFT FILL", #▨
        "SQUARE WITH DIAGONAL CROSSHATCH FILL", #▩
        "WHITE SQUARE WITH CENTRE VERTICAL LINE", #⎅
        "SQUARE FOOT", #⏍
        "BLACK RECTANGLE", #▬
        "WHITE RECTANGLE", #▭
        "BLACK VERTICAL RECTANGLE", #▮
        "WHITE VERTICAL RECTANGLE", #▯
        )

    PENTAGONS_AND_LARGER_POLYGONS = unicode_charset("Miscellaneous Polygons",
        "Benzene ring with circle",
        "Benzene ring",
        "Black horizontal ellipse",
        "Black shogi piece",
        "Canadian syllabics carrier tho",
        "House",
        "Software-function symbol",
        "White horizontal ellipse",
        "White shogi piece",
        "BLACK PENTAGON", #⬟
        "WHITE PENTAGON", #⬠
        "WHITE HEXAGON", #⬡
        "BLACK HEXAGON", #⬢
        "HORIZONTAL BLACK HEXAGON", #⬣
        "BLACK RIGHT-POINTING PENTAGON", #⭓
        "WHITE RIGHT-POINTING PENTAGON", #⭔
        # "Chestnut",
        )

    CIRCLES = unicode_charset("Circles",
        "UGARITIC LETTER THANNA", #𐎘
        "HEBREW MARK MASORA CIRCLE", #֯
        "ARABIC END OF AYAH", #۝
        "COMBINING ENCLOSING CIRCLE", #⃝
        "COMBINING ENCLOSING CIRCLE BACKSLASH", #⃠
        "APL FUNCTIONAL SYMBOL CIRCLE STILE", #⌽
        "APL FUNCTIONAL SYMBOL CIRCLE JOT", #⌾
        "APL FUNCTIONAL SYMBOL CIRCLE BACKSLASH", #⍉
        "APL FUNCTIONAL SYMBOL CIRCLE UNDERBAR", #⍜
        "APL FUNCTIONAL SYMBOL CIRCLE STAR", #⍟
        "APL FUNCTIONAL SYMBOL CIRCLE DIAERESIS", #⍥
        "BROKEN CIRCLE WITH NORTHWEST ARROW", #⎋
        "DENTISTRY SYMBOL LIGHT VERTICAL WITH CIRCLE", #⏀
        "DENTISTRY SYMBOL LIGHT DOWN AND HORIZONTAL WITH CIRCLE", #⏁
        "DENTISTRY SYMBOL LIGHT UP AND HORIZONTAL WITH CIRCLE", #⏂
        "BENZENE RING WITH CIRCLE", #⏣
        "WHITE CIRCLE", #○
        "DOTTED CIRCLE", #◌
        "CIRCLE WITH VERTICAL FILL", #◍
        "BLACK CIRCLE", #●
        "CIRCLE WITH LEFT HALF BLACK", #◐
        "CIRCLE WITH RIGHT HALF BLACK", #◑
        "CIRCLE WITH LOWER HALF BLACK", #◒
        "CIRCLE WITH UPPER HALF BLACK", #◓
        "CIRCLE WITH UPPER RIGHT QUADRANT BLACK", #◔
        "CIRCLE WITH ALL BUT UPPER LEFT QUADRANT BLACK", #◕
        "INVERSE WHITE CIRCLE", #◙
        "LARGE CIRCLE", #◯
        "WHITE CIRCLE WITH UPPER LEFT QUADRANT", #◴
        "WHITE CIRCLE WITH LOWER LEFT QUADRANT", #◵
        "WHITE CIRCLE WITH LOWER RIGHT QUADRANT", #◶
        "WHITE CIRCLE WITH UPPER RIGHT QUADRANT", #◷
        "WHITE CIRCLE WITH DOT RIGHT", #⚆
        "WHITE CIRCLE WITH TWO DOTS", #⚇
        "BLACK CIRCLE WITH WHITE DOT RIGHT", #⚈
        "BLACK CIRCLE WITH TWO WHITE DOTS", #⚉
        "MEDIUM WHITE CIRCLE", #⚪
        "MEDIUM BLACK CIRCLE", #⚫
        "MEDIUM SMALL WHITE CIRCLE", #⚬
        "SHADOWED WHITE CIRCLE", #❍
        "ANTICLOCKWISE GAPPED CIRCLE ARROW", #⟲
        "CLOCKWISE GAPPED CIRCLE ARROW", #⟳
        "ANTICLOCKWISE CLOSED CIRCLE ARROW", #⥀
        "CLOCKWISE CLOSED CIRCLE ARROW", #⥁
        "EMPTY SET WITH SMALL CIRCLE ABOVE", #⦲
        "CIRCLE WITH HORIZONTAL BAR", #⦵
        "CIRCLE WITH SMALL CIRCLE TO THE RIGHT", #⧂
        "CIRCLE WITH TWO HORIZONTAL STROKES TO THE RIGHT", #⧃
        "BLACK LARGE CIRCLE", #⬤
        )

    SHAPE_CHARSET_S = [UP_POINTING_TRIANGLES, DOWN_POINTING_TRIANGLES, LEFT_POINTING_TRIANGLES, RIGHT_POINTING_TRIANGLES, PENTAGONS_AND_LARGER_POLYGONS, QUADRILATERALS, CIRCLES]

    ONE_DOT = unicode_charset("One Dot",
        "Braille pattern dots-3",
        "Braille pattern dots-7",
        "Bullet operator",
        "Bullet",
        "Canadian syllabics final middle dot",
        "Canadian syllabics y-cree w",
        "Combining dot above right",
        "Combining dot above",
        "Combining dot below",
        "Dot above",
        "Full stop",
        "Greek ano teleia",
        "Hebrew mark lower dot",
        "Hebrew point dagesh or mapiq",
        "Hebrew point holam haser for vav",
        "Hebrew point sin dot",
        "Hyphenation point",
        "Medium black circle",
        "Middle dot",
        "Nko combining nasalization mark",
        "Nko combining short rising tone",
        "One dot leader",
        "Syriac feminine dot",
        "Syriac hbasa-esasa dotted",
        "Syriac qushshaya",
        "Syriac rukkakha",
        #"Raised dot",
        )

    TWO_DOTS_HORIZONTAL = unicode_charset("Two Dots Horizontal",
        "Braille pattern dots-14",
        "Braille pattern dots-25",
        "Braille pattern dots-36",
        "Braille pattern dots-78",
        "Byzantine musical symbol dipli",
        "Byzantine musical symbol isakia telous ichimatos",
        "Combining diaeresis below",
        "Combining diaeresis",
        "Diaeresis",
        "Double prime",
        "Double low-9 quotation mark",
        "Hebrew point tsere",
        "Hebrew punctuation gershayim",
        "Left double quotation mark",
        "Nko combining double dot above",
        "Right double quotation mark",
        "Syriac dotted zlama angular",
        "Syriac dotted zlama horizontal",
        "Syriac horizontal colon",
        "Two dot leader",
        )

    TWO_DOTS_VERTICAL = unicode_charset("Two Dots Vertical",
        "Arabic semicolon",
        "Armenian full stop",
        "Braille pattern dots-13",
        "Braille pattern dots-17",
        "Braille pattern dots-27",
        "Braille pattern dots-46",
        "Braille pattern dots-48",
        "Braille pattern dots-58",
        "Colon",
        "Greek question mark",
        "Hebrew punctuation sof pasuq",
        "Modifier letter colon",
        "Modifier letter raised colon",
        "Modifier letter triangular colon",
        "Musical symbol repeat dots",
        "Ratio",
        "Reversed semicolon",
        "Semicolon",
        "Syriac pthaha dotted",
        "Syriac sublinear colon",
        "Syriac supralinear colon",
        "Two dot punctuation",
        )

    TWO_DOTS_DIAGONAL = unicode_charset("Two Dots Diagonal",
        "Braille pattern dots-15",
        "Braille pattern dots-15",
        "Braille pattern dots-15",
        "Braille pattern dots-15",
        "Braille pattern dots-16",
        "Braille pattern dots-18",
        "Braille pattern dots-24",
        "Braille pattern dots-26",
        "Braille pattern dots-28",
        "Braille pattern dots-34",
        "Braille pattern dots-35",
        "Braille pattern dots-38",
        "Braille pattern dots-47",
        "Braille pattern dots-57",
        "Braille pattern dots-67",
        "Syriac colon skewed left",
        "Syriac sublinear colon skewed right",
        # "Syriac supralinear colon skewed left ",
        )

    TWO_DOTS = TWO_DOTS_HORIZONTAL + TWO_DOTS_VERTICAL + TWO_DOTS_DIAGONAL

    MULTI_DOTS_VERTICAL = unicode_charset("Many Dots Vertical",
        "Vertical ellipsis",
        "Tifinagh letter tuareg yagh",
        "Braille pattern dots-458",
        # "Triple colon operator",
        "Braille pattern dots-137",
        "Braille pattern dots-127",
        "Braille pattern dots-468",
        "Tricolon",
        "Latin small letter i with dot below",
        "Braille pattern dots-237",
        "Ethiopic question mark",
        "Braille pattern dots-456",
        "Braille pattern dots-568",
        "Braille pattern dots-123",
        "Dotted fence",
        "Tifinagh letter tuareg yah",
        )

    MULTI_DOTS_HORIZONTAL = unicode_charset("Many Dots Horizontal",
        "Horizontal ellipsis",
        "Midline horizontal ellipsis",
        "Monogram for earth",
        "Box drawings light triple dash horizontal",
        "Combining three dots above",
        "Tifinagh letter tuareg yaq",
        "Byzantine musical symbol saximata",
        "Box drawings heavy triple dash horizontal",
        "Combining triple underdot",
        "Byzantine musical symbol tripli",
        "Box drawings light quadruple dash horizontal",
        "Combining four dots above",
        "Ocr customer account number",
        "Box drawings heavy quadruple dash horizontal",
        "Byzantine musical symbol tetrapli",
        "Triple prime",
        "Vai syllable di",
        )

    MULTI_DOTS_DIAGONAL = unicode_charset("Many Dots Diagonal",
        "Down right diagonal ellipsis",
        "Hebrew point qubuts",
        "Buginese pallawa",
        "Up right diagonal ellipsis",
        "Ocr amount of check",
        "Braille pattern dots-347",
        "Braille pattern dots-457",
        "Byzantine musical symbol dyo"
        )

    MULTI_DOTS_MISC = unicode_charset("Many Dots Miscellaneous",
        # "Drive slow sign",
        "Proportion",
        "Tifinagh letter tuareg yakh",
        "Braille pattern dots-1346",
        "Squared four dot punctuation",
        "Braille pattern dots-2578",
        "Braille pattern dots-1478",
        "Braille pattern dots-1467",
        "Braille pattern dots-1245",
        "Ethiopic full stop",
        "Tifinagh letter ayer yagh",
        "Braille pattern dots-1358",
        "Braille pattern dots-13456",
        "Braille pattern dots-23578",
        "Digram for earth",
        "Combining cyrillic ten millions sign",
        )

    MULTI_DOTS = MULTI_DOTS_HORIZONTAL + MULTI_DOTS_VERTICAL + MULTI_DOTS_DIAGONAL + MULTI_DOTS_MISC

    DOTS = ONE_DOT + TWO_DOTS + MULTI_DOTS

    DOT_CHARSET_S = [ONE_DOT, TWO_DOTS, DOTS]

    # Small custom charsets that make nice mosaics when combined.
    TRIANGLE_MOSAIC = unicode_charset("Triangle Mosaic",
            "Black lower left triangle",
            "Black lower right triangle",
            "Black upper left triangle",
            "Black upper right triangle",
            )

    BLOCK_MOSAIC = unicode_charset("Block Mosaic",
            "UPPER HALF BLOCK",
            "LOWER HALF BLOCK",
            "FULL BLOCK",
            "LEFT HALF BLOCK",
            "RIGHT HALF BLOCK",
            )

    VERTICAL_BLOCK_MOSAIC = unicode_charset("Vertical Block Mosaic",
            "UPPER HALF BLOCK",
            "LOWER HALF BLOCK",
            "FULL BLOCK",
            )

    HORIZONTAL_BLOCK_MOSAIC = unicode_charset("Horizontal Block Mosaic",
            "LEFT HALF BLOCK",
            "RIGHT HALF BLOCK",
            "FULL BLOCK",
            )

    TERMINAL_GRAPHIC_MOSAIC = unicode_charset("Terminal Graphic Mosaic",
            "QUADRANT LOWER LEFT",
            "QUADRANT LOWER RIGHT",
            "QUADRANT UPPER LEFT",
            "QUADRANT UPPER LEFT AND LOWER LEFT AND LOWER RIGHT",
            "QUADRANT UPPER LEFT AND LOWER RIGHT",
            "QUADRANT UPPER LEFT AND UPPER RIGHT AND LOWER LEFT",
            "QUADRANT UPPER LEFT AND UPPER RIGHT AND LOWER RIGHT",
            "QUADRANT UPPER RIGHT",
            "QUADRANT UPPER RIGHT AND LOWER LEFT",
            "QUADRANT UPPER RIGHT AND LOWER LEFT AND LOWER RIGHT",
            )

    SHADING_MOSAIC = unicode_charset("Shading Mosaic",
            "LIGHT SHADE",
            "MEDIUM SHADE",
            "DARK SHADE",
            "FULL BLOCK",
            )

    FILL_MOSAIC = unicode_charset("Fill Mosaic",
        "SQUARE WITH HORIZONTAL FILL", #▤
        "SQUARE WITH VERTICAL FILL", #▥
        "SQUARE WITH ORTHOGONAL CROSSHATCH FILL", #▦
        "SQUARE WITH UPPER LEFT TO LOWER RIGHT FILL", #▧
        "SQUARE WITH UPPER RIGHT TO LOWER LEFT FILL", #▨
        "SQUARE WITH DIAGONAL CROSSHATCH FILL", #▩
        )

    BOX_DRAWING_MOSAIC = unicode_charset("Box Drawing Light Mosaic",
            "BOX DRAWINGS LIGHT DOWN AND RIGHT",
            "BOX DRAWINGS LIGHT DOWN AND LEFT",
            "BOX DRAWINGS LIGHT UP AND LEFT",
            "BOX DRAWINGS LIGHT UP AND RIGHT",
            )

    BOX_DRAWING_HEAVY_MOSAIC = unicode_charset("Box Drawing Heavy Mosaic",
        "BOX DRAWINGS HEAVY HORIZONTAL", #━
        "BOX DRAWINGS HEAVY VERTICAL", #┃
        "BOX DRAWINGS HEAVY TRIPLE DASH HORIZONTAL", #┅
        "BOX DRAWINGS HEAVY TRIPLE DASH VERTICAL", #┇
        "BOX DRAWINGS HEAVY QUADRUPLE DASH HORIZONTAL", #┉
        "BOX DRAWINGS HEAVY QUADRUPLE DASH VERTICAL", #┋
        "BOX DRAWINGS HEAVY DOWN AND RIGHT", #┏
        "BOX DRAWINGS HEAVY DOWN AND LEFT", #┓
        "BOX DRAWINGS HEAVY UP AND RIGHT", #┗
        "BOX DRAWINGS HEAVY UP AND LEFT", #┛
        "BOX DRAWINGS HEAVY VERTICAL AND RIGHT", #┣
        "BOX DRAWINGS HEAVY VERTICAL AND LEFT", #┫
        "BOX DRAWINGS HEAVY DOWN AND HORIZONTAL", #┳
        "BOX DRAWINGS HEAVY UP AND HORIZONTAL", #┻
        "BOX DRAWINGS HEAVY VERTICAL AND HORIZONTAL", #╋
        "BOX DRAWINGS HEAVY DOUBLE DASH HORIZONTAL", #╍
        "BOX DRAWINGS HEAVY DOUBLE DASH VERTICAL", #╏
        "BOX DRAWINGS HEAVY LEFT", #╸
        "BOX DRAWINGS HEAVY UP", #╹
        "BOX DRAWINGS HEAVY RIGHT", #╺
        "BOX DRAWINGS HEAVY DOWN", #╻
        )

    BOX_DRAWING_ARC_MOSAIC = unicode_charset("Box Drawing Arc Mosaic",
            "BOX DRAWINGS LIGHT ARC DOWN AND RIGHT",
            "BOX DRAWINGS LIGHT ARC DOWN AND LEFT",
            "BOX DRAWINGS LIGHT ARC UP AND LEFT",
            "BOX DRAWINGS LIGHT ARC UP AND RIGHT",
            )

    CHARACTER_CELL_DIAGONAL_MOSAIC = unicode_charset("Character Cell Diagonal Mosaic",
            "BOX DRAWINGS LIGHT DIAGONAL UPPER RIGHT TO LOWER LEFT",
            "BOX DRAWINGS LIGHT DIAGONAL UPPER LEFT TO LOWER RIGHT",
            "BOX DRAWINGS LIGHT DIAGONAL CROSS",
            )

    PARTIALLY_FILLED_SQUARE_MOSAIC_DIAGONALS_ONLY = unicode_charset("Partially Filled Square Mosaic (Diagonals Only)",
        "SQUARE WITH UPPER RIGHT DIAGONAL HALF BLACK", #⬔
        "SQUARE WITH LOWER LEFT DIAGONAL HALF BLACK", #⬕
        "SQUARE WITH UPPER RIGHT DIAGONAL HALF BLACK", #⬔
        "SQUARE WITH LOWER LEFT DIAGONAL HALF BLACK", #⬕
        )

    PARTIALLY_FILLED_SQUARE_MOSAIC = unicode_charset(
        "Partially Filled Square Mosaic",
        "SQUARE WITH UPPER RIGHT DIAGONAL HALF BLACK", #⬔
        "SQUARE WITH LOWER LEFT DIAGONAL HALF BLACK", #⬕
        "SQUARE WITH UPPER RIGHT DIAGONAL HALF BLACK", #⬔
        "SQUARE WITH LOWER LEFT DIAGONAL HALF BLACK", #⬕
        "SQUARE WITH LEFT HALF BLACK", #◧
        "SQUARE WITH RIGHT HALF BLACK", #◨
        "SQUARE WITH TOP HALF BLACK", #⬒
        "SQUARE WITH BOTTOM HALF BLACK", #⬓
        )

    PARTIALLY_FILLED_CIRCLE_MOSAIC = unicode_charset("Partially Filled Circle Mosaic",
        "BLACK CIRCLE", #●
        "CIRCLE WITH LEFT HALF BLACK", #◐
        "CIRCLE WITH RIGHT HALF BLACK", #◑
        "CIRCLE WITH LOWER HALF BLACK", #◒
        "CIRCLE WITH UPPER HALF BLACK", #◓
        "CIRCLE WITH UPPER RIGHT QUADRANT BLACK", #◔
        "CIRCLE WITH ALL BUT UPPER LEFT QUADRANT BLACK", #◕
        )

    MOSAIC_CHARSET_S = [
        BLOCK_MOSAIC,
        BOX_DRAWING_ARC_MOSAIC,
        BOX_DRAWING_HEAVY_MOSAIC,
        BOX_DRAWING_MOSAIC,
        CHARACTER_CELL_DIAGONAL_MOSAIC,
        FILL_MOSAIC,
        HORIZONTAL_BLOCK_MOSAIC,
        PARTIALLY_FILLED_CIRCLE_MOSAIC,
        PARTIALLY_FILLED_SQUARE_MOSAIC,
        SHADING_MOSAIC,
        TERMINAL_GRAPHIC_MOSAIC,
        VERTICAL_BLOCK_MOSAIC,
        TRIANGLES,
        ]

class WordLength:

    @classmethod
    def random(cls):
        c = random.choice([cls.natural_word_length, cls.completely_random,
                             cls.ten_characters, cls.twenty_characters,
                             cls.short_words, cls.long_words])
        return c

    @classmethod
    def natural_word_length(cls):
        return random.choice([1,2,2,3,3,3,4,4,4,5,5,5,5,6,6,6,7,7,8,8,9,9,10,10,11])

    @classmethod
    def completely_random(cls):
        return random.randint(1, 140)

    @classmethod
    def ten_characters(cls):
        return 10

    @classmethod
    def twenty_characters(cls):
        return 20

    @classmethod
    def short_words(cls):
        return int(random.gauss(5, 2))

    @classmethod
    def long_words(cls):
        return int(random.gauss(50,20))

class Corruptor(object):
    """Corrupt text by adding diacritical marks."""
    def __init__(self, factor=2):
        """`factor` is the mean number of diacritical marks to be
        added to each character."""
        if factor == 0:
            self.factor = 0
        else:
            self.factor = 1.0/factor
        self.diacritics = Alphabet.characters(
            [Alphabet.DIACRITICAL[0], Alphabet.DIACRITICAL[0],
            "Combining Diacritical Marks for Symbols"])

    def corrupt(self, text):
        if self.factor == 0:
            return text
        new_chars = []
        for i in text:
            new_chars.append(i)
            for j in range(int(random.expovariate(self.factor))):
                new_chars.append(random.choice(self.diacritics))
        return ''.join(new_chars)

class Gibberish(object):

    @classmethod
    def from_alphabets(cls, alphabets):
        return cls("".join(Alphabet.characters(alphabets)))

    @classmethod
    def random(self, freq=None):
        return GibberishTable().choice(freq)

    def __init__(self, charset, word_length=None, word_separator=' ', num_words=None):
        self.charset = charset
        self.word_length = word_length
        self.word_separator = word_separator
        self.num_words = num_words

    @classmethod
    def characters_from_set(cls, choices, characters):
        chosen = ''
        for i in range(choices):
            chosen += random.choice(characters)
        return cls(chosen)

    def word(self, length=None):
        length = length or self.word_length()
        t = []
        for i in range(length):
            t.append(random.choice(self.charset))
        return unicodedata.normalize("NFC", u''.join(t))

    def words(self, length):
        words = ''
        i = 0
        while True:
            word_length = None
            if self.word_length is None:
                word_length = length
            word = self.word(word_length)
            if not words:
                words = word
            else:
                words += self.word_separator + word
            i += 1
            if len(words) >= length or (self.num_words is not None and i > self.num_words):
                break

        return words[:length]

    def tweet(self):
        if random.randint(0,4) == 0:
            length = 140
        else:
            if random.randint(0,4) != 0:
                # Short
                mean = 20
                dev = 10
                m = 5
            else:
                # Long
                mean = 90
                dev = 30
                m = 15
            length = int(max(m, min(random.gauss(mean, dev), 140)))
        return self.words(length)

    @classmethod
    def weird_twitter(cls, base_alphabets, alternate_alphabets,
                      mixin_alphabets, how_weird=1):
        """Give an alphabet the "Weird Twitter" treatment.

        A technique borrowed from the namesake Twitter community, in
        which an alphabet's glyphs are replaced by similar glyphs
        and/or junk glyphs.

        `base_alphabets` is a set of alphabets used in normal
        communcation. One of them will be chosen as the base alphabet.

        `alternate_alphabets` is a set of alphabets providing
        strange-looking versions of the glyphs in the base alphabets.

        `mixin alphabets` is a set of alphabets providing unusual
        glyphs that are thematically related to the base alphabet, but
        not normally used.

        `how_weird` is a way to weight the base alphabets against the
        "weird" alphabets. how_weird=0 is not weird at all. Higher
        numbers are weirder.

        Higher numbers for `how_weird` will also tend to introduce
        diacritical marks, symbolic characters, and completely random
        scripts into the alphabet.
        """
        if isinstance(base_alphabets, basestring):
            # The base alphabet is a literal string
            letters = base_alphabets
        else:
            letters = Alphabet.random_choice(*base_alphabets)

        if how_weird <= 0:
            return Gibberish(letters)

        # Choose a random number of mixins.
        mixins = ''
        for i in range(1, random.randint(1, how_weird+1)):
            mixins += Alphabet.random_choice(*mixin_alphabets)

        # Add either normal-looking letters or weird alternate
        # letters, until the size of the letters matches the size of
        # the mixins.
        while len(letters) < len(mixins):
            if random.randint(0, how_weird) == 0:
                choices = base_alphabets
            else:
                choices = alternate_alphabets

            if choices == base_alphabets and isinstance(base_alphabets, basestring):
                # Again, the base alphabet is a literal string
                letters += base_alphabets
            else:
                letters += Alphabet.random_choice(*choices)

        alphabet = letters + mixins

        # Possibly throw in some diacritical marks.
        marks = ''
        while random.random() * how_weird > 0.5:
            marks += Alphabet.random_choice(*Alphabet.MODIFIERS)
        alphabet += marks

        # There is a very small chance that a random symbolic or geometric
        # alphabet will be included.
        approximate_size_of_symbolic_alphabet = len(alphabet) / 10
        symbols = ''
        if random.random() * how_weird > 5:
            s = Alphabet.random_choice(*(Alphabet.SYMBOLIC_ALPHABETS + Alphabet.GEOMETRIC_ALPHABETS))
            while len(symbols) < approximate_size_of_symbolic_alphabet:
                symbols += s
        alphabet += symbols

        # And an even smaller chance that part of a random linguistic
        # alphabet will be included. If a large alphabet like "Hangul
        # Syllables" is chosen, this may dominate the rest of the
        # character set!
        approximate_size_of_foreign_alphabet = len(alphabet) / 5
        if random.random() * how_weird > 7:
            c = random.choice(Alphabet.ALL_LANGUAGE_ALPHABETS_S)
            if isinstance(c, basestring):
                c = [c]
            foreign_alphabet = Alphabet.random_choice(*c)
            f = ''
            while len(f) < approximate_size_of_foreign_alphabet:
                f += foreign_alphabet
            alphabet += f

        return Gibberish(alphabet)

    @classmethod
    def limited_vocabulary(cls, how_many_characters=None):
        full = Alphabet.random_choice_no_modifiers()
        limited = ''
        if not how_many_characters:
            how_many_characters = max(2, int(random.gauss(4, 2)))
        for i in range(how_many_characters):
            limited += random.choice(full)
        return cls(limited)

    @classmethod
    def a_little_weirder_than(self, base_charset):
        """Make the given charset a little more weird."""
        choices = (Alphabet.CUSTOM_S + [Alphabet.YIJING]
                   + [Alphabet.GEOMETRIC_ALPHABETS]
                   + [Alphabet.GAMING_ALPHABETS]
                   + [Alphabet.SYMBOLIC_ALPHABETS]
                   + [Alphabet.WEIRD_TWITTER_MATH_MIXINS]
                   + [Alphabet.DIACRITICAL]
                   + [Alphabet.DIACRITICAL_FULL])
        choice = random.choice(choices)
        extra = Alphabet.characters(choice)

        destination = len(extra) * 3
        multiplied_base_charset = base_charset
        while len(multiplied_base_charset) < destination:
            multiplied_base_charset += base_charset
        return Gibberish(multiplied_base_charset + extra)


class EmoticonGibberish(Gibberish):

    def __init__(self, charsets=None):
        if charsets is None:
            charsets = Alphabet.random_choice_no_modifiers()
        self.charsets = charsets
        self.mouths = u'____⁔𝁛ᨓ⏟‿⏝ω'
        super(EmoticonGibberish, self).__init__(None)

    def word(self, word_length=None):
        charset = random.choice(self.charsets)
        eye = random.choice(charset)

        return eye + random.choice(self.mouths) + eye

    def tweet(self):
        num_words = random.randint(1,3)
        return ' '.join(self.word() for word in range(num_words))

class GameBoardGibberish(Gibberish):
    def __init__(self, charset=None):
        choices = list(Alphabet.GAMING_ALPHABETS)
        choices.remove("Japanese Chess") # Not enough distinct characters.
        alphabet = random.choice(choices)
        charset = Alphabet.characters(alphabet)
        word_separator = "\n"
        l = random.randint(5, 9)
        num_words = l
        word_length = lambda: l
        super(GameBoardGibberish, self).__init__(
            charset, word_length, word_separator, num_words)

class CheatCodeGibberish(Gibberish):
    "Video game input codes."

    def __init__(self):
        self.base_charset = u'←↑→↓'
        self.fighting_game_charset = self.base_charset + u'↖↗↘↙↺↻PK'
        self.nes_charset = self.base_charset + u'AB'

    def tweet(self):
        num_words = random.randint(5,10)
        if random.randint(0,2) == 0:
            charset = self.fighting_game_charset
        else:
            charset = self.nes_charset
        return ' '.join(random.choice(charset) for word in range(num_words))

class MosaicGibberish(Gibberish):
    def __init__(self, charset=None):
        charset = random.choice(Alphabet.MOSAIC_CHARSET_S)
        if random.randint(0, 2) == 0:
            # Linear mosaic
            word_length = None
            word_separator = ' '
            num_words = None
        else:
            # Two-dimensional mosaic
            size = random.randint(3, 11)
            num_words = size + random.randint(-2,2)
            word_length = lambda: size
            word_separator = '\n'
        super(MosaicGibberish, self).__init__(charset, word_length, word_separator, num_words)

Alphabet._fill_by_name(data.load_json("unicode_code_sheets.json"))

class GibberishTable(WanderingMonsterTable):

    def __init__(self):
        super(GibberishTable, self).__init__()

        # Populate the table. An entry may be:
        #  * The name of an alphabet, or a list of names.
        #  * A Gibberish object.
        #  * A function that returns a Gibberish object.

        # One of the Cyrillic alphabets.
        self.add(self.choice_among_alphabets(Alphabet.CYRILLIC_S), RARE)

        # One of the linguistic alphabets.
        self.add(self.charset_from_alphabets(Alphabet.ALL_LANGUAGE_ALPHABETS_S), COMMON)

        # ALL of the non-huge linguistic alphabets.

        all_but_large_cjk = list(Alphabet.ALL_LANGUAGE_ALPHABETS_S)
        for i in ("CJK Unified Ideographs (Han)", "Hangul Syllables"):
            all_but_large_cjk.remove(i)

        self.add(self.charset_from_alphabets(all_but_large_cjk), RARE)

        # Some combination of the non-huge linguistic alphabets.
        self.add(self.combination_of_alphabets(all_but_large_cjk), COMMON)

        # One of the geometric alphabets.
        self.add(self.choice_among_alphabets(Alphabet.GEOMETRIC_ALPHABETS), UNCOMMON)

        # One of the custom scripts.
        self.add(self.choice_among_alphabets(Alphabet.CUSTOM_S), UNCOMMON)

        # The combination of all geometric alphabets.
        self.add(Alphabet.GEOMETRIC_ALPHABETS, VERY_RARE)

        # Circled letters
        self.add("Circled Letters", VERY_RARE)

        # A limited subset of one script.
        self.add(Gibberish.limited_vocabulary, UNCOMMON)

        # A mosaic charset.
        self.add(MosaicGibberish, COMMON)

        # A game board charset.
        self.add(GameBoardGibberish, VERY_RARE)

        # A shape-based charset
        self.add(self.choice_among_charsets(Alphabet.SHAPE_CHARSET_S), VERY_RARE)

        # A dot-based charset
        self.add(self.choice_among_charsets(Alphabet.DOT_CHARSET_S), RARE)

        # Weird Latin Twitter
        def weird_latin_twitter():
            return self.weird_twitter(
                [Alphabet.ASCII, Alphabet.LATIN_1],
                Alphabet.WEIRD_TWITTER_LATIN,
                Alphabet.WEIRD_TWITTER_LATIN_MIXINS)
        self.add(weird_latin_twitter, COMMON)

        # Weird Japanese Twitter
        def weird_japanese_twitter():
            return self.weird_twitter(
                ["Hiragana", Alphabet.KATAKANA, Alphabet.KATAKANA_ALL],
                Alphabet.WEIRD_TWITTER_CJK,
                Alphabet.WEIRD_TWITTER_CJK_MIXINS)
        self.add(weird_japanese_twitter, UNCOMMON)

        # Weird CJK Twitter
        def weird_cjk_twitter():
            return self.weird_twitter(
                ["CJK Unified Ideographs (Han)"],
                Alphabet.WEIRD_TWITTER_CJK,
                Alphabet.WEIRD_TWITTER_CJK_MIXINS, None, 10)
        self.add(weird_japanese_twitter, RARE)

        # Weird Math Twitter
        def weird_math_twitter():
            def math_word_length():
                return random.choice([1,1,1,1,1,1,2,2,2,3,3,3,4,4,5])
            return self.weird_twitter(
                "1234567890", Alphabet.WEIRD_TWITTER_MATH,
                Alphabet.WEIRD_TWITTER_MATH_MIXINS, math_word_length)
        self.add(weird_math_twitter, RARE)

        # Emoticons
        self.add(EmoticonGibberish, VERY_RARE)

        # Video game cheat codes.
        self.add(CheatCodeGibberish, VERY_RARE)

    def weird_twitter(self, base, weird, mixins, word_length=None,
                      weird_multiplier=1):
        how_weird = int(random.expovariate(1.0/6)) * weird_multiplier
        gibberish = Gibberish.weird_twitter(
            base, weird, mixins, how_weird)
        gibberish.word_length = word_length
        return gibberish

    def charset_from_alphabets(self, alphabets):
        charset = ''
        for alphabet in alphabets:
            if isinstance(alphabet, basestring):
                alphabet = [alphabet]
            charset += Alphabet.characters(alphabet)
        return Gibberish(charset)

    def choice_among_alphabets(self, alphabets):
        """Returns a function that chooses an alphabet from a list.

        There is a 33% chance that the charset will be weirded a bit.
        """
        def c():
            alphabet = random.choice(alphabets)
            if isinstance(alphabet, basestring):
                alphabet = [alphabet]
            charset = Alphabet.characters(alphabet)
            if random.randint(0,2) == 0:
                # 33% chance to make it a little weirder.
                gibberish = Gibberish.a_little_weirder_than(charset)
            else:
                gibberish = Gibberish(charset)
            return gibberish
        return c

    def combination_of_alphabets(self, alphabets, num=None):
        """Returns a function that chooses a number of alphabets from a list."""
        def combo():
            how_many = num or max(2, int(random.gauss(4,2)))
            if len(alphabets) <= how_many:
                choices = alphabets
            else:
                choices = random.sample(alphabets, how_many)
            gibberish = self.charset_from_alphabets(choices)
            if random.randint(1,10) == 1:
                # 10% chance to make it a little weirder.
                gibberish = Gibberish.a_little_weirder_than(gibberish.charset)
            return gibberish
        return combo

    def choice_among_charsets(self, charsets):
        """Returns a function that chooses a charset from a list.

        There is a 10% chance that the charset will be weirded a bit.
        """
        def c():
            charset = random.choice(charsets)
            if random.randint(1,10) == 1:
                gibberish = Gibberish.a_little_weirder_than(charset)
            else:
                gibberish = Gibberish(charset)
            return gibberish
        return c

    def choice(self, freq):
        choice = super(GibberishTable, self).choice(freq)
        if isinstance(choice, basestring):
            choice = [choice]
        if isinstance(choice, list):
            gibberish = Gibberish.from_alphabets(choice)
        elif isinstance(choice, Gibberish):
            gibberish = choice
        elif callable(choice):
            gibberish = choice()
        else:
            raise Exception("Cannot turn %r into Gibberish object!", choice)

        if gibberish.__class__ != Gibberish:
            # Custom logic. Leave it alone.
            return gibberish

        # 75% chance to add some kind of word boundary algorithm.
        if random.randint(0,100) < 75:
            gibberish.word_length = WordLength.random()

        # Chance to use newline instead of space as word separator
        if (gibberish.word_length is not None
            and gibberish.word_length() >= 15
            and random.randint(0,3) == 0):
            gibberish.word_separator = '\n'

        # Blanket 10% chance to add 10% glitches
        if random.randint(0, 10) >= 0:
            glitches = ''
            glitch_charset = Alphabet.random_choice(Alphabet.GLITCHES)
            max_glitches = len(gibberish.charset) / 10
            glitch_characters = ''
            while len(glitch_characters) < max_glitches:
                glitch_characters += random.choice(glitch_charset)
            gibberish.charset += glitch_characters
        return gibberish

if __name__ == '__main__':
    freq = None
    alphabets = None
    if len(sys.argv) == 2 and sys.argv[1] in (COMMON, UNCOMMON, RARE, VERY_RARE, None):
        freq = sys.argv[1]
    else:
        alphabets = sys.argv[1:]

    gibberish = None
    if alphabets:
        gibberish = Gibberish.from_alphabets(alphabets)
    for i in range(100):
        if not alphabets:
            gibberish = Gibberish.random(freq)
        print gibberish.tweet().encode("utf8")
        print '---'
