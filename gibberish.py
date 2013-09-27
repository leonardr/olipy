"""Create gibberish from source alphabets."""

import os
import json
import random
import string

class Alphabet:

    @classmethod
    def _fill_by_name(cls, data=None):
        for c in data:
            name = c['name']
            cls.by_name[name] = c
            if 'child' in c:
                cls._fill_by_name(c['child'])

    by_name = {}

    @classmethod
    def random_choice(cls, *alphabets):
        """A random choice between alphabets"""
        return cls.characters(random.choice(alphabets))

    @classmethod
    def characters(cls, alphabets):
        char = []
        if isinstance(alphabets, basestring):
            alphabets = [alphabets]
        # print "Character lookup for %r" % alphabets
        for alphabet in alphabets:
            # print "Looking up %s" % alphabet
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
    UCAS = "Unified Canadian Aboriginal Syllabics",
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
        "Combining Diacritical Marks Supplement", "Combining Half Marks",
        "Combining Diacritical Marks for Symbols"]
    MODIFIERS = DIACRITICAL + DIACRITICAL_FULL

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

    # "Weird Twitter" versions of, and mixins for, CJK characters
    WEIRD_TWITTER_CJK = [
        "Halfwidth and Fullwidth Forms",
        "Halfwidth Katakana",
        "CJK Symbols and Punctuation",
        "CJK Compatibility Forms",
        "CJK Compatibility",
        "Enclosed CJK Letters and Months",
        ]

    # "Weird Twitter" math glyphs
    WEIRD_TWITTER_MATH = [
        "Number Forms",
        "Fullwidth ASCII Digits",
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
        "CJK Compatibility Forms",
        "Additional Shapes",
        "Box Drawing",
        "Block Elements",
        "Braille Patterns",
        "Yijing Mono-, Di- and Trigrams",
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
        ]

    # Custom alphabets 
    CUSTOM_S = [
        "Geometric Shapes",
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
        ["Playing Cards", "Card suits"],
        "Yijing Mono-, Di- and Trigrams",
        "Yijing Hexagram Symbols",
        "Tai Xuan Jing Symbols",
        ["Yijing Mono-, Di- and Trigrams", "Yijing Hexagram Symbols", "Tai Xuan Jing Symbols"],
        ["Yijing Mono-, Di- and Trigrams", "Yijing Hexagram Symbols", "Tai Xuan Jing Symbols", "Braille Patterns", "Optical Character Recognition (OCR)"],
        ["Hiragana", "Katakana"],
        ]

class Gibberish(object):

    @classmethod
    def from_alphabets(cls, alphabets):
        return cls("".join(Alphabet.characters(alphabets)))

    @classmethod
    def weird_twitter_latin(cls, how_weird=1):
        """Create a "Weird Twitter" type alphabet based on Latin characters.

        0 is not weird at all. Higher numbers are weirder.
        """

        letters = Alphabet.random_choice(Alphabet.ASCII, Alphabet.LATIN_1)

        if how_weird <= 0:
            return Gibberish(letters)

        # Choose a random number of mixins.
        mixins = ''
        for i in range(1, random.randint(1, how_weird+1)):
            mixins += Alphabet.random_choice(
                *Alphabet.WEIRD_TWITTER_LATIN_MIXINS)

        # Add either normal-looking Latin-1 letters or weird alternate
        # letters, until the size of the letters matches the size of
        # the mixins.
        while len(letters) < len(mixins):
            if random.randint(0, how_weird) == 0:
                choices = (Alphabet.ASCII, Alphabet.LATIN_1)
            else:
                choices = Alphabet.WEIRD_TWITTER_LATIN
            letters += Alphabet.random_choice(*choices)

        alphabet = letters + mixins
        # Possibly throw in some diacritical marks.
        count = 0
        while random.random() * how_weird > 1 and count < 3:
            alphabet += Alphabet.random_choice(*Alphabet.MODIFIERS)
            count += 1
        return Gibberish(alphabet)

    def default_word_length_distribution():
        return random.choice([1,2,2,3,3,3,4,4,4,5,5,5,5,6,6,6,7,7,8,8,9,9,10,10,11])

    def __init__(self, charset,
                 word_length_distribution=default_word_length_distribution):
        self.charset = charset
        self.word_length_distribution = word_length_distribution

    def word(self, length=None):
        length = length or self.word_length_distribution()
        t = []
        for i in range(length):
            t.append(random.choice(self.charset))
        return ''.join(t)

    def words(self, length, exact=False):
        t = ''
        while True:
            word = self.word()
            potential = t + ' ' + word
            if exact:
                if len(potential) >= length:
                    return potential[:length]
            else:
                if len(potential) > length:
                    return t
            t = potential

    def tweet(self):
        return self.words(140)

data = json.load(open(os.path.join("data", "unicode_code_sheets.json")))
Alphabet._fill_by_name(data)

for i in 0, 1, 2, 4, 8, 16:
    print i, Gibberish.weird_twitter_latin(i).tweet()
