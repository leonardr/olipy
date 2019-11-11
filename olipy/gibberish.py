# coding=utf-8
"""Create gibberish from source alphabets."""

from pdb import set_trace
import os
import json
import random
import sys
import unicodedata
from olipy.randomness import Gradient, WanderingMonsterTable, COMMON, UNCOMMON, RARE, VERY_RARE

from olipy.alphabet import *
from olipy.letterforms import alternate_spelling

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

    minimum_length = 3
    can_truncate = True
    end_with = None

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
        for i in range(int(length)):
            t.append(random.choice(self.charset))
        return unicodedata.normalize("NFC", u''.join(t))

    def words(self, length):
        words = ''
        i = 0
        attempts = 0
        default_length = length
        while attempts < 1000:
            word_length = None
            if self.word_length is None:
                word_length = default_length
            word = self.word(word_length)
            if not word:
                default_length = int(default_length * 0.85)
            if not words:
                words = word
            else:
                new_words = words + self.word_separator + word
                if len(new_words) > length and not self.can_truncate:
                    break
                words = new_words
            i += 1
            if len(words) >= length or (self.num_words is not None and i > self.num_words):
                break
            attempts += 1
        return words[:int(length)]

    def tweet(self):
        if random.randint(0,4) == 0:
            length = 140
        else:
            if random.randint(0,4) == 0:
                # Short
                mean = 30
                dev = 10
                m = 5
            else:
                # Long
                mean = 90
                dev = 30
                m = 15
            length = int(max(m, min(random.gauss(mean, dev), 140)))
        if self.end_with:
            length -= len(self.end_with)
        length = max(self.minimum_length, length)
        tweet = None
        while not tweet:
            tweet = self.words(length)
            if not tweet:
                length = int(length * 1.15)
            if length > 140:
                break
        if self.end_with:
            tweet += self.end_with
        if not tweet:
            # Apparently it's just not possible.
            return None
        if not tweet[0].strip():
            # This tweet starts with whitespace. Use COMBINING
            # GRAPHEME JOINER to get Twitter to preserve the whitespace.
            tweet = u"\N{COMBINING GRAPHEME JOINER}" + tweet
        if len(tweet) > 140:
            tweet = tweet[:140]
        return tweet

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
        if isinstance(base_alphabets, list):
            letters = Alphabet.random_choice(*base_alphabets)
        else:
            # The base alphabet is a literal string
            letters = base_alphabets

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

            if choices != base_alphabets or isinstance(base_alphabets, list):
                letters += Alphabet.random_choice(*choices)
            else:
                # Again, the base alphabet is a literal string
                letters += base_alphabets

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
            if not isinstance(c, list):
                c = [c]
            foreign_alphabet = Alphabet.random_choice(*c)
            f = ''
            while len(f) < approximate_size_of_foreign_alphabet:
                f += foreign_alphabet
            alphabet += f

        return Gibberish(alphabet)

    @classmethod
    def limited_vocabulary(cls, how_many_characters=None, include_whitespace=None):
        full = Alphabet.random_choice_no_modifiers()
        limited = Alphabet.subset(full, how_many_characters)
        if include_whitespace is None:
            include_whitespace = random.random() < 0.33
        if include_whitespace:
            limited += random.choice(Alphabet.WHITESPACE)
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

class SamplerGibberish(Gibberish):
    def __init__(self, alphabet=None):
        self.rows = random.randint(1,3)
        self.per_row = random.randint(3,4)
        if self.rows == 1:
            self.per_row += 3
        self.total_size = self.rows * self.per_row
        while not (alphabet and len(alphabet) > self.total_size):
            alphabet = Alphabet.random_choice()
        self.alphabet = alphabet

    def tweet(self):
        whitespace = Alphabet.random_whitespace()
        rows = []
        sample = random.sample(self.alphabet, self.total_size)
        for i in range(self.rows):
            row = ''
            for i in range(self.per_row):
                row += sample.pop()
            rows.append(whitespace.join(row))
        value = "\n".join(rows)
        return value

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

class AlternateSpellingGibberish(Gibberish):
    """The same string every time, but with a different variant of each
    character every time.
    """
    def __init__(self, base_string):
        self.base_string = base_string

    def tweet(self):
        return alternate_spelling(self.base_string)
        
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

class LimitedModifierGibberish(Gibberish):
    def __init__(self, table, num_modifiers=None):
        self.other_generator = table.choice(None)
        self.modifiers = ''
        if num_modifiers is None:
            num_modifiers = int(max(1, random.gauss(1,3)))
        for i in range(num_modifiers):
            modifier_charset = Alphabet.random_choice(*Alphabet.MODIFIERS)
            self.modifiers += random.choice(modifier_charset)

    def tweet(self):
        tweet = self.other_generator.tweet()
        new_tweet = []
        if not tweet:
            return None
        for i in tweet:
            new_tweet += i + random.choice(self.modifiers)
        new_tweet = unicodedata.normalize("NFC", "".join(new_tweet))
        return new_tweet[:140]

class MosaicGibberish(Gibberish):

    def __init__(self, alphabet=None, include_whitespace=None):
        if not alphabet:
            alphabet = random.choice(Alphabet.MOSAIC_CHARSET_S)
        l = int(random.gauss(8,3))
        if include_whitespace is None:
            include_whitespace = random.random() < 0.25
        if include_whitespace:
            choice = random.choice(Alphabet.WHITESPACE)
            size = random.randint(1, len(alphabet)*2)
            alphabet += (choice * size)
        word_length = lambda: l
        word_separator = '\n'
        num_words = None
        self.can_truncate = False
        super(MosaicGibberish, self).__init__(
            alphabet, word_length, word_separator, num_words)

Alphabet.default()

class GibberishGradient(Gibberish):

    minimum_length = 140
    gradient_method = Gradient.gradient

    def __init__(self):
        super(GibberishGradient, self).__init__(None)

    def words(self, length):
        alpha1 = Alphabet.random_choice_no_modifiers()
        alpha2 = Alphabet.random_choice_no_modifiers()
        a = "".join(x for x in self.gradient_method(alpha1, alpha2, length))
        return a

class ModifierGradientGibberish(Gibberish):
    """The alphabet stays the same throughout the tweet, but the modifier
    used slowly changes from one to another.
    """

    minimum_length = 140

    def __init__(self):
        super(ModifierGradientGibberish, self).__init__(None)
        mod1 = Alphabet.random_modifier()
        mod2 = None
        while mod2 is None or mod2 == mod1:
            mod2 = Alphabet.random_modifier()

        alphabet = Alphabet.random_choice_no_modifiers()
        self.a1 = [char + mod1 for char in alphabet]
        self.a2 = [char + mod2 for char in alphabet]

    def words(self, length):
        a = "".join(x for x in Gradient.gradient(self.a1, self.a2, length/2))
        return a

class GibberishRainbowGradient(GibberishGradient):

    minimum_length = 140
    gradient_method = Gradient.rainbow_gradient

class CompositeGibberish(Gibberish):

    def __init__(self, table):
        self.table = table
        super(CompositeGibberish, self).__init__(None)

    SEPARATORS = u"     /\-=#:.,|_⏟"

    def words(self, length):
        num_gibberish = random.randint(2,5)
        size_of_each = (length-num_gibberish) / num_gibberish
        gibberishes = []
        for i in range(int(min(2, size_of_each))):
            g = None
            while g is None or not hasattr(g, 'word_length') or g.word_separator == '\n':
                g = self.table.choice(None)

            gibberishes.append(g.words(size_of_each))
        return random.choice(self.SEPARATORS).join(gibberishes)

class RosettaStoneGibberish(CompositeGibberish):
    """A number of small gibberishes, one per line."""
    SEPARATORS = u"\n"

class GibberishTable(WanderingMonsterTable):

    def __init__(self):
        super(GibberishTable, self).__init__()

        # Populate the table. An entry may be:
        #  * The name of an alphabet, or a list of names.
        #  * A Gibberish object.
        #  * A function that returns a Gibberish object.

        # One of the Cyrillic alphabets.
        self.add(self.choice_among_alphabets(Alphabet.CYRILLIC_S), RARE)

        # One of the Latin alphabets.
        self.add(self.choice_among_alphabets(Alphabet.LATIN_S), UNCOMMON)

        # One of the linguistic alphabets.
        self.add(self.choice_among_alphabets(Alphabet.ALL_LANGUAGE_ALPHABETS_S), COMMON)

        all_but_large_cjk = list(Alphabet.ALL_LANGUAGE_ALPHABETS_S)
        for i in ("CJK Unified Ideographs (Han)", "Hangul Syllables",
                  "CJK Compatibility Ideographs",):
            all_but_large_cjk.remove(i)

        # ALL of the non-huge linguistic alphabets.
        self.add(self.charset_from_alphabets(all_but_large_cjk), VERY_RARE)

        # Some combination of the non-huge linguistic alphabets.
        self.add(self.combination_of_alphabets(all_but_large_cjk), UNCOMMON)

        # A gradient between two alphabets.
        self.add(GibberishGradient, COMMON)
        self.add(GibberishRainbowGradient, UNCOMMON)
        self.add(ModifierGradientGibberish, UNCOMMON)

        # A mirrored mosaic
        from olipy.mosaic import MirroredMosaicGibberish
        self.add(MirroredMosaicGibberish, COMMON)

        # A mirrored mosaic from an untilable alphabet
        def untilable_mirror():
            alphabet = None
            while not alphabet or alphabet in Alphabet.TILABLE_CHARSET_S:
                alphabet = Alphabet.random_choice_no_modifiers()
            limited = Alphabet.subset(alphabet)
            gibberish = MirroredMosaicGibberish(limited)
            return gibberish
        self.add(untilable_mirror, UNCOMMON)

        # One of the geometric alphabets.
        self.add(self.choice_among_alphabets(Alphabet.GEOMETRIC_ALPHABETS), UNCOMMON)

        # One of the custom scripts.
        self.add(self.choice_among_alphabets(Alphabet.CUSTOM_S), UNCOMMON)

        # The combination of all geometric alphabets.
        self.add(Alphabet.GEOMETRIC_ALPHABETS, VERY_RARE)

        # A limited subset of one script.
        self.add(Gibberish.limited_vocabulary, COMMON)

        # A less limited subset of one script.
        self.add(lambda: Gibberish.limited_vocabulary(how_many_characters=3+int(random.gauss(4,2))), UNCOMMON)

        # A limited subset of one script, including whitespace
        self.add(lambda: Gibberish.limited_vocabulary(include_whitespace=True),
                 UNCOMMON)

        # A mosaic charset.
        self.add(MosaicGibberish, UNCOMMON)

        # Some other kind of gibberish with a modifier (chosen from a
        # small subset) applied to every character.
        self.add(lambda: LimitedModifierGibberish(self), COMMON)

        # Composite gibberish
        self.add(lambda: CompositeGibberish(self), UNCOMMON)

        # Composite gibberish, newline-separated
        self.add(lambda: RosettaStoneGibberish(self), UNCOMMON)

        # A game board charset.
        self.add(GameBoardGibberish, VERY_RARE)
        
        # A sampler from a charset.
        self.add(SamplerGibberish, RARE)

        # A shape-based charset
        self.add(self.choice_among_charsets(Alphabet.SHAPE_CHARSET_S), VERY_RARE)

        # A dot-based charset
        self.add(self.choice_among_charsets(Alphabet.DOT_CHARSET_S), UNCOMMON)

        # Weird Latin Twitter
        def weird_latin_twitter():
            return self.weird_twitter(
                [Alphabet.ASCII, Alphabet.LATIN_1],
                Alphabet.WEIRD_TWITTER_LATIN,
                Alphabet.WEIRD_TWITTER_LATIN_MIXINS)
        self.add(weird_latin_twitter, COMMON)

        # Nothing but emoji!
        def nothing_but_emoji():
            self.add(self.choice_among_charsets(Alphabet.EMOJI_S), RARE)

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
            if not isinstance(alphabet, list):
                alphabet = [alphabet]
            charset += Alphabet.characters(alphabet)
        gibberish = Gibberish(charset)
        gibberish.original_alphabets = alphabets
        return gibberish

    def choice_among_alphabets(self, alphabets):
        """Returns a function that chooses an alphabet from a list.

        There is a 33% chance that the charset will be weirded a bit.
        """
        def c():
            alphabet = random.choice(alphabets)
            if not isinstance(alphabet, list):
                alphabet = [alphabet]
            charset = Alphabet.characters(alphabet)
            if random.randint(0,2) == 0:
                # 33% chance to make it a little weirder.
                gibberish = Gibberish.a_little_weirder_than(charset)
            else:
                gibberish = Gibberish(charset)
            gibberish.original_alphabets = alphabets
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
            gibberish.original_alphabets = alphabets
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
        gibberish = super(GibberishTable, self).choice(freq)
        if isinstance(gibberish, Gibberish):
            pass
        elif callable(gibberish):
            gibberish = gibberish()
        elif not isinstance(gibberish, list):
            gibberish = [gibberish]
        if isinstance(gibberish, list):
            gibberish = Gibberish.from_alphabets(gibberish)
        if not isinstance(gibberish, Gibberish):
            raise Exception("Cannot turn %r into Gibberish object!", gibberish)

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
        if random.randint(0, 10) == 1:
            glitches = ''
            glitch_charset = Alphabet.random_choice(Alphabet.GLITCHES)
            max_glitches = len(gibberish.charset) / 10
            glitch_characters = ''
            while len(glitch_characters) < max_glitches:
                glitch_characters += random.choice(glitch_charset)
            gibberish.charset += glitch_characters

        # Blanket 10% chance to add an emoji on the end.
        if random.randint(0, 10) == 1:
            gibberish.end_with = " " + random.choice(Alphabet.characters('Emoji'))
        return gibberish

class GlyphNames(object):
    """I know the names of glyphs."""

    def __init__(self):
        self.inverse = dict()
        # self.missing = []
        # self.max_present = None
        for i in range(1, 1000000):
            c = unichr(i)
            try:
                glyph_name = unicodedata.name(c)
                self.inverse[glyph_name] = c
                # self.max_present = i
            except ValueError as e:
                # self.missing.append(i)
                continue

    @classmethod
    def names(self, s):
        """Yield the name of every glyph in the given string."""
        for glyph in s:
            try:
                yield glyph, unicodedata.name(glyph)
            except ValueError as e:
                yield glyph, None

    def matching(self, exp):
        """Yield all name-glyph pairs where the name matches a regexp."""
        for name, value in self.inverse.keys():
            if exp.search(name):
                yield name, value

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
    table = GibberishTable()
    for i in range(1000):
        if not alphabets:
            gibberish = Gibberish.random(freq)
        print(gibberish.tweet().encode("utf8"))
        print('---')
