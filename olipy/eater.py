import argparse
from bs4 import BeautifulSoup
from bs4.formatter import Formatter
import requests
import syllables
from collections import defaultdict
import inspect
import random
import re
import string
import sys

from olipy.gibberish import Corruptor
from olipy.letterforms import alternate_spelling
from olipy import corpora
from olipy import typewriter

class Eater:
    """An Eater of Meaning mangles text, or converts it into
    superficially similar text.

    Technically speaking, an Eater is just a callable that takes maps one
    string onto another.
    """

    DESCRIPTION = "Abstract base class; does not change input"

    IMPLEMENTATIONS = dict()

    SPLIT_RE = re.compile(r"(\w+)")
    WORD_RE = re.compile(r"\w", re.I)

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
        choices = self.words_by_syllable_count.get(str(count))
        if choices:
            return self.match_capitalization(word, random.choice(choices))
        else:
            return word

    def syllables(self, word):
        word = word.lower()
        return syllables.estimate(word)


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
        s = re.compile(r'[^a-zA-Z0-9 ]').sub('', s)
        s = re.compile(r'\W+').sub(' ', s)
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

# Provide an Eater interface to some other features of olipy.

class Retype(Eater):
    DESCRIPTION = "Retype on an old typewriter"
    KEY = "typewriter"
    def eat(self, s):
        return typewriter.Typewriter().type(s)

class Corrupt(Eater):
    DESCRIPTION = "Corrupt text by adding diacritical marks"
    KEY = "corrupt"
    def eat(self, s):
        return Corruptor(5).corrupt(s)

class Reletter(Eater):
    DESCRIPTION = "Change the shape of letterforms"
    KEY = "reletter"
    def eat(self, s):
        return alternate_spelling(s)


# Note to those who remember the old Eater of Meaning: SpamEater and
# GOPACEater are not ported because they're both more complicated than
# the other eaters, and woefully out of date with the many
# improvements in mass-scale deception made over the last 20 years.

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
        )
        return parser

    def __call__(self):
        args = self.parser().parse_args()
        self.text = " ".join(args.text)
        self.url = args.url
        default_text = 'Now is the time for all good men to come to the aid of their party.'
        if args.demo or (not self.text and not self.url):
            self.url = self.url or "https://www.example.com/"
            self.text = self.text or default_text
            return self.demo()

        if not self.text:
            self.text = default_text

        eater = Eater.IMPLEMENTATIONS[args.eater]()

        if self.url:
            eater = URLEater(eater)
            result = eater.eat(self.url)
        else:
            result = eater.eat(self.text)
        print(result)

    def demo(self):
        print("Demo mode activated, use --help to see options.\n")
        print(f"Demo text: {self.text}")
        print("Each eater will be demonstrated on this input text.\n")
        for key, eater, in Eater.IMPLEMENTATIONS.items():
            print(f"{key}: {eater.DESCRIPTION}")
            print("", eater()(self.text))

        print(f"\nURL test: eating {self.url} with {EatWordEndings.KEY}")
        print("", URLEater(EatWordEndings())(self.url))


if __name__ == '__main__':
    EaterCommandLine()()
