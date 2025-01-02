"""An Eater of Meaning mangles text, or converts it into
superficially similar text."""

# Technically speaking, an Eater is just a callable that takes maps one
# string onto another.

import argparse
from bs4 import BeautifulSoup
from bs4.formatter import Formatter
import requests
from collections import defaultdict
import inspect
import random
import re
import string
import sys

import corpora

class Eater:

    DESCRIPTION = "Abstract base class; does not change input"

    IMPLEMENTATIONS = dict()

    SPLIT_RE = re.compile("(\w+)")
    WORD_RE = re.compile("\w", re.I)

    def __call__(self, s):
        if isinstance(s, bytes):
            s = s.decode("utf8")
        if not s:
            return s
        return self.eat(s)

    def eat(self, s):
        eaten = []
        for word in self.SPLIT_RE.split(s):
            if not word:
                continue
            if self.WORD_RE.match(word):
                eaten += self.eat_word(word)
            else:
                eaten += self.eat_punctuation(word)
        return "".join(eaten)

    def match_capitalization(self, src, dest):
        i = ''
        l = len(src)
        mapped = []
        for i, source_char in enumerate(src):
            if i >= len(dest):
                break
            dest_char = dest[i]
            if source_char == source_char.upper():
                final = dest_char.upper()
            elif source_char == source_char.lower():
                final = dest_char.lower()
            else:
                final = dest_char
            mapped += final
        return "".join(mapped) + dest[i+1:]

    def eat_word(self, word):
        return word

    def eat_punctuation(self, punc):
        return punc

    def string_of_length(self, l):
        return "".join(random.choice(string.ascii_lowercase) for i in range(l))

    def number_of_length(self, l):
        return "".join(random.choice(string.digits) for i in range(l))

class NeedsWordList(Eater):
    """An eater that requires a word list to operate."""
    def __init__(self, words=None):
        if not words:
            words = self._load_corpus("english_words", "words")
        self.word_list = words
        self.words = self.process_word_list(self.word_list)

    def process_word_list(self, word_list):
        return word_list

    @classmethod
    def from_file(cls, filename):
        words = [i.strip() for i in open(filename)]
        return cls(words)

    @classmethod
    def _load_corpus(cls, corpus_name, key=None):
        data = corpora.load(corpus_name)
        keys = set(data.keys()) - set(["description"])
        if key is None and len(keys) > 1:
            raise ValueError("I don't know which key to use for this corpus: choose among %s", ",".join(keys))
        key = key or list(keys)[0]
        words = data[key]
        return [x.lower() for x in words]
    
    @classmethod
    def from_corpus(cls, corpus_name, key=None):
        return cls(cls._load_corpus(corpus_name, key))

class EatCharacters(Eater):
    """The character eater returns None for None and the empty string
    for the empty string.

    It replaces each letter it encounters with a random letter with
    the same capitalization status. It replaces vowels with vowels,
    and consonants with consonants.

    It replaces each digit it encounters with a random digit.

    It retains all non-alphanumeric characters."""

    DESCRIPTION = "Eat characters"
    KEY = "character"

    VOWELS = 'aeiou'
    VOWELS_U = 'AEIOU'
    CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
    CONSONANTS_U = 'BCDFGHJKLMNPQRSTVWXYZ'
    DIGITS = string.digits

    def eat_word(self, s):
        if not s:
            return s
        eaten = ''
        for char in s:
            eaten += self.eat_char(char)
        return eaten

    def eat_char(self, char):
        if len(char) > 1:
            raise ValueError(f"char was called with long string {char}")
        for l in self.VOWELS, self.VOWELS_U, self.CONSONANTS, self.CONSONANTS_U, self.DIGITS:
            if char in l:
                return random.choice(l)
        return char

class ScrambleWords(Eater):
    """The word scrambling eater scrambles the characters in every
    word it encounters, preserving the capitalization pattern of the
    original word in the new word.
    """

    DESCRIPTION = "Scramble words"
    KEY = "scramble"

    def eat_word(self, word):
        if not word:
            return word

        w = list(word)
        random.shuffle(w)

        return self.match_capitalization(word, "".join(w))


class ScrambleWordCenters(Eater):
    """The word center scrambling eater scrambles the characters in every
    word it encounters, but leaves the first and last characters intact
    for better readability.

    Original implementation by Aaron Swartz. R.I.P.
    """
    DESCRIPTION = "Scramble word centers"
    KEY = "scramble-center"

    def eat_word(self, word):
        if not word:
            return word
        if len(word) < 3:
            scrambled = word
        if len(word) == 4:
            scrambled = word[0] + word[2] + word[1] + word[3]
        else:
            middle = list(word[1:-1])
            random.shuffle(middle)
            scrambled = word[0] + "".join(middle) + word[-1]
        return self.match_capitalization(word, scrambled)

class SortWords(Eater):
    """The word sorting eater puts the characters in every word
    it encounters into alphabetical order, preserving the
    capitalization pattern of the original word in the new word.

    It retains all non-alphanumeric characters."""
    KEY = 'sort'
    DESCRIPTION = "Sort characters in words"

    def eat_word(self, word):
        l = list(word)
        l.sort()
        return self.match_capitalization(word, "".join(l))
    
class EatWords(NeedsWordList):
    DESCRIPTION = "Replace a word with another word of the same length."
    KEY = "word"

    def process_word_list(self, word_list):
        words_by_length = defaultdict(list)
        for i in word_list:
            words_by_length[len(i)].append(i)
        return words_by_length

    def eat_word(self, word):
        l = len(word)
        if word[0] in string.digits:
            return self.number_of_length(l)
        if l not in self.words:
            return word
        new = random.choice(self.words[l])
        return self.match_capitalization(word, new)

class EatWordEndings(NeedsWordList):
    DESCRIPTION = "Eat word endings"
    KEY = "word-endings"

    def process_word_list(self, word_list):
        self.words_by_prefix = defaultdict(list)
        for word in word_list:
            if len(word) <= 3:
                continue
            prefix = word[:3].lower()
            self.words_by_prefix[prefix].append(word)

    def eat_word(self, word):
        if not word:
            return word
        if word[0] in string.digits:
            return self.number_of_length(len(word))
        if len(word) < 3:
            return word
        newWord = ''
        prefix = word[:3].lower()

        choices = self.words_by_prefix[prefix]
        if not choices:
            return word
        return self.match_capitalization(word, random.choice(choices))


class EatSyllables(NeedsWordList):
    DESCRIPTION = "Eat syllables"
    KEY = "syllable"

    def __init__(self):
        self.words_by_syllable_count = corpora.load("by_syllable_count")["words_by_syllable_count"]
        self.syllables_for_word = dict()
        for count, words in self.words_by_syllable_count.items():
            for w in words:
                self.syllables_for_word[w] = count

    def eat_word(self, word):
        count = self.syllables(word)
        choices = self.words_by_syllable_count.get(count)
        if choices:
            return self.match_capitalization(word, random.choice(choices))
        else:
            return word

    def syllables(self, word):
        word = word.lower()
        return self.syllables_for_word.get(word, None) or self.guess_sy_count(word)

    # Code below this point is heavily based on Greg Fast's Perl
    # module Lingua::EN::Syllables. I chose not to bring in the
    # Python 'syllables' package for licensing reasons.
    def guess_sy_count(self, word):
        mungedword = re.sub('e$','',word.lower())
        splitword = re.split(r'[^aeiouy]+', mungedword)
        splitword = [ x for x in splitword if (x != '') ] # hmm
        syllables = 0
        for i in self.SUBTRACT_ONE:
            if re.search(i,mungedword):
                syllables -= 1
        for i in self.ADD_ONE:
            if re.search(i,mungedword):
                syllables += 1
        if len(mungedword) == 1: syllables =+ 1
        syllables += len(splitword)
        if syllables == 0: syllables = 1
        return syllables

    SUBTRACT_ONE = [
        'cial',
        'tia',
        'cius',
        'cious',
        'giu',              # belgium!
        'ion',
        'iou',
        'sia$',
        '.ely$',             # absolutely! (but not ely!)
        ]

    ADD_ONE = [
        'ia',
        'riet',
        'dien',
        'iu',
        'io',
        'ii',
        '[aeiouym]bl$',     # -Vble, plus -mble
        '[aeiou]{3}',       # agreeable
        '^mc',
        'ism$',             # -isms
        '([^aeiouy])\1l$',  # middle twiddle battle bottle, etc.
        '[^l]lien',         # alien, salient [1]
        '^coa[dglx].',      # [2]
        '[^gq]ua[^auieo]',  # i think this fixes more than it breaks
        'dnt$',           # couldn't
        ]

    def ensurePrefixLoaded(self, prefix):
        if prefix and not self.loadedPrefixes.get(prefix):
            self.loadedPrefixes[prefix] = True
            path = os.path.join(self.syllable_dir, prefix)
            if os.path.exists(path):
                syllables = 0
                for line in open(path):
                    syllables += 1
                    words = line.split(' ')
                    if words and words[-1][-1] == "\n":
                        words[-1] = words[-1][:-1]
                    for word in words:
                        self.syllableCountsByWord[word] = syllables

class ReplaceWords(NeedsWordList):

    DESCRIPTION = 'Replace with words from another text'
    KEY = 'replacing'

    LOREM_IPSUM = 'lorem ipsum dolor sit amet consetetur sadipscing elitr sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat sed diam voluptua at vero eos et accusam et justo duo dolores et ea rebum stet clita kasd gubergren no sea takimata sanctus est lorem ipsum dolor sit amet lorem ipsum dolor sit amet consetetur sadipscing elitr sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat sed diam voluptua at vero eos et accusam et justo duo dolores et ea rebum stet clita kasd gubergren no sea takimata sanctus est lorem ipsum dolor sit amet lorem ipsum dolor sit amet consetetur sadipscing elitr sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat sed diam voluptua at vero eos et accusam et justo duo dolores et ea rebum stet clita kasd gubergren no sea takimata sanctus est lorem ipsum dolor sit amet duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi lorem ipsum dolor sit amet consectetuer adipiscing elit sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat ut wisi enim ad minim veniam quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum lorem ipsum dolor sit amet consectetuer adipiscing elit sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat ut wisi enim ad minim veniam quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat'.split()

    def __init__(self, words=None):
        if not words:
            words = self.LOREM_IPSUM
        words = [self.clean(x) for x in words]
        self.counter = 0
        return super(ReplaceWords, self).__init__(words)

    def clean(self, s):
        "Cleans a string for use in a word list."
        s = s.lower()
        s = re.compile('[^a-zA-Z0-9 ]').sub('', s)
        s = re.compile('\W+').sub(' ', s)
        return s

    def eat_word(self, word):
        if not word:
            return ''

        new_word = self.word_list[self.counter % len(self.word_list)]
        self.counter += 1
        m = self.match_capitalization(word, new_word)
        if m is None:
            m = self.match_capitalization(word, new_word)
        return m

class PirateEater(Eater):
    """The pirate eater replaces every instance of "ar" with
    "arrrr". Written especially for Riana Pfefferkorn.
    """
    DESCRIPTION = "Convert to pirate-speak."
    KEY = "pirate"
    RE = re.compile('ar', re.I)

    def __init__(self, how_many_rs=5):
        self.arr = "a" + ('r' * how_many_rs)

    def eat(self, s):
        if not s:
            return s
        return self.RE.sub(self.arr, s)

#import typewriter
#class Retype(Eater):
#    def eat(self, s):
#        return typewriter.Typewriter(type(s))

# SpamEater and GOPACEater are not ported because they're both more
# complicated than the other eaters, and woefully out of date with the
# many improvements in the deceiving-people field made over the last
# 20 years.

class HTMLEater(Eater):
    """Wraps another eater and uses it to eat all of the text (but not
    the markup) of an HTML document."""

    def __init__(self, eater):
        self.eater = eater

        self.formatter = Formatter(
            void_element_close_prefix='',
            empty_attributes_are_booleans=True,
            entity_substitution=self.eater
        )

    def eat(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        return soup.decode(formatter=self.formatter)

class URLEater(Eater):
    """Wraps another eater and uses it to eat all of the text (but not
    the markup) of the HTML document found at a given URL."""

    def __init__(self, eater):
        self.eater = HTMLEater(eater)

    def eat(self, text):
        # The "text" is a URL.
        response = requests.get(text)
        return self.eater.eat(response.content)

this_module = sys.modules[__name__]
for k, v in sorted(inspect.getmembers(this_module)):
    if not inspect.isclass(v) or not issubclass(v, Eater) or not hasattr(v, 'KEY'):
        continue
    Eater.IMPLEMENTATIONS[v.KEY] = v

class EaterCommandLine:

    def parser(self):
        parser = argparse.ArgumentParser(
            description="An Eater of Meaning mangles text, or converts it into superficially similar text.")
        parser.add_argument(
            "--demo", help="Demonstrate all eaters on the same piece of input text.",
            type=bool, default=False
        )
        parser.add_argument(
            '--eater', help="Which eater to use.",
            choices=Eater.IMPLEMENTATIONS.keys(),
            default=EatWordEndings.KEY
        )
        parser.add_argument(
            "--url", help="Treat the text input as a URL to a web page rather than text.",
            default=None,
        )
        parser.add_argument(
            "text", nargs="*", help="Text to consume",
            default=['Now is the time for all good men to come to the aid of their party.'],
        )
        return parser

    def __call__(self):
        args = self.parser().parse_args()
        self.text = " ".join(args.text)
        self.url = args.url

        if args.demo:
            self.url = self.url or "https://www.example.com/"
            return self.demo()

        eater = Eater.IMPLEMENTATIONS[args.eater]()

        if self.url:
            eater = URLEater(eater)
            result = eater.eat(self.url)
        else:
            result = eater.eat(self.text)
        print(result)

    def demo(self):
        print("Demo mode activated.")
        print(f"Demo text: {self.text}")
        print("Each eater will be demonstrated on this input text.\n")
        for key, eater, in Eater.IMPLEMENTATIONS.items():
            print(f"{key}: {eater.DESCRIPTION}")
            print("", eater()(self.text))

        print(f"\nURL test: eating {self.url} with {EatWordEndings.KEY}")
        print("", URLEater(EatWordEndings())(self.url))


if __name__ == '__main__':
    EaterCommandLine()()
