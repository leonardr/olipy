import os
import json
import random

data = json.load(open(os.path.join("data", "unicode_code_sheets.json")))
by_name = {}
for top in data:
    for middle in top['child']:
        by_name[middle['name']] = middle
        for bottom in middle.get('child', []):
            by_name[bottom['name']] = bottom

by_name["ASCII"] = by_name["Basic Latin (ASCII)"]

alphabets = [
    ["Armenian", "Armenian Ligatures"],
    "Coptic",
    "Cyrillic",
    ["Cyrillic", "Cyrillic Supplement", "Cyrillic Extended-A", "Cyrillic Extended-B"],
    "Georgian",
    ["Georgian", "Georgian Supplement"],
    "Glagolitic",
    "Gothic",
    "Greek",
    ["Greek", "Greek Extended"],
    "Basic Latin (ASCII)",
    ["Basic Latin (ASCII)", "Latin-1 Supplement"],
    ["Basic Latin (ASCII)", "Latin-1 Supplement", "Latin Extended-A", "Latin Extended-B", "Latin Extended-C", "Latin Extended-D", "Latin Extended Additional", "Latin Ligatures"],
    "Fullwidth Latin Letters",
    ["Basic Latin (ASCII)", "Fullwidth Latin Letters"],
    "Ogham",
    "Old Italic",
    ["Old Italic", "Basic Latin (ASCII)"],
    "Runic",
    ["Basic Latin (ASCII)", "IPA Extensions"],
    ["Basic Latin (ASCII)", "Phonetic Extensions", "Phonetic Extensions Supplement"],
    ["Basic Latin (ASCII)", "Modifier Tone Letters", "Spacing Modifier Letters", "Superscripts and Subscripts"],
    ["Basic Latin (ASCII)", "Fullwidth Latin Letters", "Superscripts and Subscripts", "Super and Subscripts"],
    ["Basic Latin (ASCII)", "Fullwidth Latin Letters", "Combining Diacritical Marks", "Combining Diacritical Marks Supplement", "Combining Half Marks"],


    # African Scripts

    "Ethiopic",
    ["Ethiopic", "Ethiopic Supplement", "Ethiopic Extended", "Ethiopic Extended-A"],
    "N'Ko",
    "Osmanya",
    "Tifinagh",
    "Vai",

    # Middle Eastern Scripts
    "Arabic",
    ["Arabic", "Arabic Supplement"],
    ["Arabic", "Arabic Presentation Forms-B"],
    "Old Persian",
    "Ugaritic",
    "Hebrew",
    ["Hebrew", "Hebrew Presentation Forms"],
    "Phoenician",
    "Syriac",

    # Central Asian Scripts
    "Tibetan",

    # South Asian Scripts
    "Bengali and Assamese",
    "Devanagari",
    ["Devanagari", "Devanagari Extended"],
    "Gujarati",
    "Gurmukhi",
    "Kannada",
    "Malayalam",
    "Oriya",
    "Sinhala",
    "Tamil",
    "Telugu",
    "Thaana",

    # Southeast Asian Scripts
    "Buginese",
    "Kayah Li",
    "Khmer",
    ["Khmer", "Khmer Symbols"],
    "Lao",
    "Myanmar",
    ["Myanmar", "Myanmar Extended-A"],
    "Tai Le",
    "Thai",

    # Philippine Scripts
    "Hanunoo",

    # East Asian Scripts
    "Bopomofo",
    "CJK Unified Ideographs (Han)",
    "CJK Compatibility Ideographs",
    # "CJK Radicals / KangXi Radicals",
    "Hangul Jamo",
    ["Hangul Jamo", "Hangul Compatibility Jamo"],
    "Hangul Syllables",
    "Hiragana",
    "Katakana",
    ["Katakana", "Katakana Phonetic Extensions", "Halfwidth Katakana"],
    ["Hiragana", "Katakana"],

    # American Scripts
    "Cherokee",
    "Deseret",
    "Unified Canadian Aboriginal Syllabics",
    ["Unified Canadian Aboriginal Syllabics", "UCAS Extended"],

    # Other
    "Halfwidth and Fullwidth Forms",

    # Misc. weird-looking Latin text.
    ["ASCII", "Latin-1 Punctuation", "Small Form Variants", "CJK Symbols and Punctuation", "CJK Compatibility Forms",],
    ["Mathematical Alphanumeric Symbols", "Combining Diacritical Marks"],
    ["Halfwidth and Fullwidth Forms", "Latin-1 Punctuation", "Small Form Variants", "CJK Symbols and Punctuation", "CJK Compatibility Forms",],
    ["Fullwidth ASCII Digits", "Combining Diacritical Marks for Symbols"],
    ["ASCII", "Arrows"],

    # Alphanumeric Symbols
    ["ASCII", "Letterlike Symbols"],
    ["Mathematical Alphanumeric Symbols", "Letterlike Symbols"],
    ["ASCII", "Enclosed Alphanumerics"],
    ["Halfwidth and Fullwidth Forms", "Enclosed CJK Letters and Months"],

    # Technical Symbols
    "APL symbols",
    ["ASCII", "Control Pictures"],
    ["ASCII", "Miscellaneous Technical"],
    "Optical Character Recognition (OCR)",

    ["ASCII", "Combining Diacritical Marks for Symbols"],
    ["ASCII Digits", "Fullwidth ASCII Digits", "Number Forms", "Super and Subscripts"],
   "Arrows",
    ["Arrows", "Supplemental Arrows-A", "Supplemental Arrows-B", "Additional Arrows"],
    "Additional Arrows",
    "Mathematical Alphanumeric Symbols",

    ["ASCII Digits", "Fullwidth ASCII Digits", "Mathematical Alphanumeric Symbols", "Supplemental Mathematical Operators"],
    ["ASCII Digits", "Fullwidth ASCII Digits", "Mathematical Alphanumeric Symbols", "Miscellaneous Mathematical Symbols-A", "Miscellaneous Mathematical Symbols-B"],
    ["ASCII Digits", "Fullwidth ASCII Digits", "Floors and Ceilings"],
    "Geometric Shapes",
    ["Geometric Shapes", "Additional Shapes"],
    ["Geometric Shapes", "Additional Shapes", "Box Drawing", "Block Elements"],
    "Box Drawing",
    "Block Elements",
    ["Box Drawing", "Block Elements"],
    ["Box Drawing", "Block Elements", "Optical Character Recognition (OCR)"],

    # Other Symbols

    "Braille Patterns",
    ["Braille Patterns", "Optical Character Recognition (OCR)"],
    ["ASCII Digits", "Fullwidth ASCII Digits", "Currency Symbols", "Dollar Sign", "Yen, Pound and Cent", "Rial Sign"],
    ["Dingbats", "Miscellaneous Symbols"],
    ["Dingbats", "Emoticons", "Miscellaneous Symbols"],
    ["Dingbats", "Emoticons", "Miscellaneous Symbols", "Miscellaneous Symbols and Arrows"],
    ["ASCII", "Emoticons"],

    # Game Symbols
    "Chess, Checkers/Draughts",
    "Domino Tiles",
    "Playing Cards",
    "Mahjong Tiles",
    ["Playing Cards", "Card suits"],

    "Musical Symbols",
    "Byzantine Musical Symbols",
    "Yijing Mono-, Di- and Trigrams",
    "Yijing Hexagram Symbols",
    "Tai Xuan Jing Symbols",
    ["Yijing Mono-, Di- and Trigrams", "Yijing Hexagram Symbols", "Tai Xuan Jing Symbols"],
    ["Yijing Mono-, Di- and Trigrams", "Yijing Hexagram Symbols", "Tai Xuan Jing Symbols", "Braille Patterns", "Optical Character Recognition (OCR)"],

    ]

def load_character_set(alphabets):
    character_set = []
    if isinstance(alphabets, basestring):
        alphabets = (alphabets,)
    for alphabet in alphabets:
        character_set.append(by_name[alphabet]['characters'])
    return "".join(character_set)

def tweet(alphabets):
    character_set = load_character_set(alphabets)
    t = []
    for i in range(140):
        t.append(random.choice(character_set))
    return ''.join(t)

print "<html>"
print "<head>"
print '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'
print "</head>"
print "<body>"

for alphabet in alphabets:
    print "<p><b>%r</b>: %s</p>" % (alphabet, tweet(alphabet).encode("utf8"))
print "</body></html>"


