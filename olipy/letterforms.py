# coding=utf-8
"""Unicode glyphs that resemble other glyphs."""
import random
import string

alternates = {
    "a" : "",
    "b" : "",
    "c" : "ϲᒼᑦсϚⅽ꜀꜂ℂ℃⊏",
    "d" : "",
    "e" : "💶ᥱ",    
    "f" : "ſʄ",
    "g" : "",    
    "h" : "ℌᑋ",
    "i" : "",    
    "j" : "",
    "k" : "ⱪ",    
    "l" : "",
    "m" : "ϻ⩋ᨓოጦጠᶬ₥ෆ",
    "n" : "⩏സﬨヘ",
    "o" : "",    
    "p" : "ᕵᑭᑭⲢ",
    "q" : "",    
    "r" : "╭┌ɼᒋᒥ꜒Γᖋ┍ᒋℾᒋɼґᣘ𝝘ⲅ𝈬꜓⦧",
    "s" : "",    
    "t" : "†Ϯϯ┼┽┿╀⍭┾╇+ⵜ╁╪╈╅╅╆╄⨨╂╃╉╊╋╉ߙ⁺ᚐႵ⍖Էէヒナヒモ",
    "u" : "Цυսᥙɥᐡ",
    "v" : "",
    "w" : "ᐜ",    
    "x" : "☒",
    "y" : "ʮկ",    
    "z" : "",

    "A" : "⍍ᐃ",
    "B" : "β3",
    "C" : "ᑕϹСʗⅭⵎᥴⲤƇᑕ",    
    "D" : "ᐅᑓᑔ",
    "E" : "⪡ΕꗋΕƐЄᎬⴹЕĘɛℇᙓミ",
    "F" : "ҒϜғƑߓ𝟋₣ᖴ╒𐌅℉",
    "G" : "",    
    "H" : "╫⩆",
    "I" : "エェヱ",
    "J" : "",
    "K" : "ΚƘKК𐌊ҚкⱩⲔκᏦϏҜ𝝟₭ꗪ",    
    "L" : "レ",
    "M" : "ΜМϺ𐌑ⅯмⱮӍ𝝡ӎ",
    "N" : "₪Иⵍи",
    "O" : "🝕▣⌻⏣⧈0ロ",
    "P" : "ꝒР♇ҏРΡᏢ⛿ᕈ𐌛Ᵽ𐌓ǷⲢ℗アァ",
    "Q" : "",    
    "R" : "𝈖ᎡƦɌⴽᖇ",
    "S" : "⑀",    
    "T" : "⊤┬ΤТ⟙ꔋ𝖳┰┯т𝍮⫪┮Ƭ🝨⥡┭Ţ⏉ᚁᎢ┳╥𝝩Ꞇィイフヮワᐪ",
    "U" : "⋃⨆ᑌ∪ՍⵡŲ∐⌴ᓑԱ⊔𝈈பVリᑌ",
    "V" : "ᐺ",
    "W" : "",    
    "X" : "⪥",
    "Y" : "߂ЏЦ💴",
    "Z" : "",
    "-" : "ー",
}

multi_character_alternates = {
    "B" : ["]3", "|3"],
    "H" : ["|-|", "|=|"],
    "K" : ["]<", ")<", "|<"],
    "O" : ["()", "[]", "{}"],
    "U" : ["|_|"],
    "V" : ["\/"],
}

from olipy.alphabet import CUSTOM_ALPHABETS

alternate_letterforms = {}
for k, v in list(alternates.items()):
    alternate_letterforms[k] = set(v)
for k, v in list(multi_character_alternates.items()):
    alternate_letterforms[k].update(v)

full_alphabet_mapping = string.ascii_uppercase + string.ascii_lowercase
lowercase_alphabet_mapping = string.ascii_lowercase
def map_alphabet(alphabet, mapping=full_alphabet_mapping):
    for i, char in enumerate(alphabet):
        if not char.strip():
            continue
        map_to = mapping[i]
        alternate_letterforms[map_to].add(char)
    
# Incorporate some strings that map the alphabet onto alternate 'fonts'.
for alphabet_name in [
        "Completely Circled Alphabetics",
        "Fullwidth Alphabetics" ,
        "Bold Alphabetics" ,
        "Italic Alphabetics" ,
        "Bold Italic Alphabetics" ,
        "Script Alphabetics" ,
        "Script Bold Alphabetics" ,
        "Fraktur Alphabetics" ,
        "Doublestruck Alphabetics" ,
        "Fraktur Bold Alphabetics" ,
        "Sans Alphabetics" ,
        "Sans Bold Alphabetics" ,
        "Sans Italic Alphabetics" ,
        "Sans Bold Italic Alphabetics" ,
        "Monospace Alphabetics" ,
#        "Alphabetics with Umlaut" ,
]:
    alphabet = CUSTOM_ALPHABETS[alphabet_name]
    map_alphabet(alphabet)

full_alphabets = [
    "ᴬᴮʿᴰᴱ ᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾ ᴿ ᵀᵁⱽᵂ   ₐᵇ ᵈᵉᶠᵍʰᶤʲᵏˡᵐᵑᵒᵖ ʳˢᵗᵤᵛʷˣʸᶻ",
    "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘ ʀꜱᴛᴜᴠᴡ ʏᴢₐ   ₑ  ₕᵢⱼₖₗₘₙₒₚ ᵣₛₜᵤᵥ ₓ  ",
]
for alphabet in full_alphabets:
    map_alphabet(alphabet)
    
lowercase_alphabets = ["⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵"]
for alphabet in lowercase_alphabets:
    map_alphabet(alphabet, lowercase_alphabet_mapping)
    
# Finally, construct a case-insensitive version of alternate_letterforms.
alternate_letterforms_case_insensitive = dict()
for lower in string.ascii_lowercase:
    upper = lower.upper()
    combined = alternate_letterforms[lower].union(alternate_letterforms[upper])
    for destination in (lower, upper):
        alternate_letterforms_case_insensitive[destination] = combined

def alternate_spelling(string, case_sensitive=False):
    new_string = ""
    if case_sensitive:
        source = alternate_letterforms
    else:
        source = alternate_letterforms_case_insensitive
    for char in string:
        if char in source and source[char]:
            char = random.choice(list(source[char]))
        new_string += char
    return new_string
