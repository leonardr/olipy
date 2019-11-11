import random
import re
import textwrap
from textblob import TextBlob, Sentence
from olipy import corpora
stopwords = corpora.words.stopwords.en

from olipy.tokenizer import WordTokenizer

class EbooksQuotes(object):

    def __init__(
        self, keywords=None, probability=0.001,
        minimum_quote_size=8, maximum_quote_size=140,
        wrap_at=30, truncate_chance=1.0/4):
        keywords = keywords or []
        self.keywords = [x.lower() for x in keywords]
        self.probability = probability
        self.minimum_quote_size = minimum_quote_size
        self.maximum_quote_size = maximum_quote_size
        self.wrap_at = wrap_at
        self.truncate_chance = truncate_chance
        self._blobs = {}

    COMMON_STARTING_WORDS= [
        "I","How","The","You","What","A","Why",
        "And","This","It","Do","In","We","Learn","If",
        "But","Don't","Your","When","Discover",
        "Are","Get","There","My","Have","To","That",
        "As","Make","Let","One"]

    # Quotes that end in certain parts of speech get higher ratings.
    PART_OF_SPEECH_SCORE_MULTIPLIERS = {
        "NNP": 3.2,
        "NNS": 2.7,
        "NN": 2.5,
        "VGD": 1.9,
        "VBG": 1.9,
        "PRP": 1.8,
        "VB": 1.6,
        "JJR": 1.3,
        "CD": 1.2,
        "RB": 1.2,
        "VBP": 1}

    PUNCTUATION_AND_COMMON_STARTING_WORD = re.compile('[.!?"] (%s) ' % (
            "|".join(COMMON_STARTING_WORDS)))

    SEVERAL_CAPITALIZED_WORDS = re.compile("(([A-Z][a-zA-Z]+,? ){2,}[A-Z][a-zA-Z]+[!?.]?)")

    ONE_LETTER = re.compile("[A-Za-z]")
    ONE_WORD = re.compile("\W+")

    data = ['" ', "' ", "--", '\)', ']', ',', '\.', '-']
    BEGINNING_CRUFT = re.compile("^(%s)" % "|".join(data))

    TOKENIZER = WordTokenizer()

    @classmethod
    def rate(cls, s, base_score=1.0, frequencies=None, obscurity_cutoff=None):
        "Rate a string's suitability as an _ebook quote."
        s = s.strip()
        score = float(base_score)
        # print s
        # print " Starting rating: %.2f" % score

        # People like very short or very long quotes.
        # if len(s) < 40:
        #    score *= 2
        if len(s) > 128:
            score *= 2
            # print " Length bonus: %.2f" % score

        blob = TextBlob(s.decode("utf8"))
        try:
            words = blob.words
        except Exception as e:
            # TODO: I'm sick of trying to get TextBlob to parse
            # strings that include things like ". . . ". Just return
            # the current score.
            return score

        if frequencies:
            contains_known_word = False
            contains_obscure_word = False
            for word in words:
                l = word.lower()
                if l in frequencies:
                    contains_known_word = True
                    if frequencies[l] < obscurity_cutoff:
                        contains_obscure_word = True
                if contains_known_word and contains_obscure_word:
                    break

            # A string that contains no words that appear in the
            # frequency list is heavily penalized. It's probably
            # gibberish.
            if not contains_known_word:
                score *= 0.1
                # print " No known word: %.2f" % score

            # A string that contains no obscure words is even more
            # heavily penalized. It's almost certainly boring.
            if not contains_obscure_word:
                score *= 0.01
                # print " No obscure word: %.2f" % score

        if s[0].upper() == s[0]:
            # We like quotes that start with uppercase letters.
            score *= 2.5
            # print " Starts with uppercase letter: %.2f" % score

        # Let's take a look at the first and last words.
        first_word, ignore = blob.tags[0]
        if first_word.capitalize() in cls.COMMON_STARTING_WORDS:
            score *= 2.5
            # print " Starts with common starting word: %.2f" % score

        last_word, last_tag = blob.tags[-1]
        if last_tag in cls.PART_OF_SPEECH_SCORE_MULTIPLIERS:
            score *= cls.PART_OF_SPEECH_SCORE_MULTIPLIERS[last_tag]
            # print " Bonus for part of speech %s: %.2f" % (last_tag, score)

        if last_tag != 'NNP' and last_word[0].upper() == last_word[0]:
            score *= 1.25
            # print " Bonus for ending with a capitalized word: %.2f" % score
        # print "Final score: %.2f" % score
        return score

    # Ways of further tweaking a quote.
    def one_sentence_from(self, quote):
        """Reduce the given quote to a single sentence.

        The choice is biased against the first sentence, which is less likely
        to be the start of a real in-text sentence.
        """
        blob = TextBlob(quote)
        try:
            sentences = blob.sentences
        except Exception as e:
            # TextBlob can't parse this. Just return the whole string
            return quote
        if len(sentences) > 1 and len(sentences[-1]) < 10:
            # Don't choose a very short sentence if it's at the end of a chunk.
            sentences = sentences[:-1]
        s = random.choice(sentences)
        if s == sentences[0]:
            s = random.choice(sentences)
            if s == sentences[0]:
                s = random.choice(sentences)

        return s

    def remove_beginning_punctuation(self, string):
        old_string = None
        while string != old_string:
            old_string = string
            string = self.BEGINNING_CRUFT.sub("", string)
        return string

    def remove_ending_punctuation(self, string):
        # Notably absent: dash and colon, which make a quote
        # funnier.
        if isinstance(string, Sentence):
            string = string.string
        if string.count('"') == 1:
            string = string.replace('"', "")
        string = string.replace("_", "")
        while string and string[-1] in ',; ':
            string = string[:-1]
        return string

    def truncate_to_common_word(self, text):
        m = self.PUNCTUATION_AND_COMMON_STARTING_WORD.search(text)
        if m is None:
            return text
        new_text = text[m.span()[0]+2:]
        if len(new_text) < len(text) / 2:
            return text
        return new_text

    def truncate_at_stopword(self, string):
        # Truncate a string at the last stopword not preceded by
        # another stopword.
        # print "%s =>" % string

        if isinstance(string, Sentence):
            words = string.words
        else:
            try:
                words = TextBlob(string).sentences
            except Exception as e:
                # TextBlob can't parse this. Just return the whole string
                return string

        reversed_words = list(reversed(words[2:]))
        for i, w in enumerate(reversed_words):
            if (w in stopwords
                and i != len(reversed_words)-1 and
                not reversed_words[i+1] in stopwords):
                # print "Stopword %s (previous) %s" % (w, reversed_words[i+1])
                r = re.compile(r".*\b(%s)\b" % w)
                string = unicode(string)
                m = r.search(string)
                if m is not None:
                    string = string[:m.span(1)[0]]
                # print "=> %s" % string
                # print "---"
                break
        return string


    def quotes_in(self, paragraph):
        para = textwrap.wrap(paragraph, self.wrap_at)
        if len(para) == 0:
            return

        probability = self.probability
        if para[0][0].upper() == para[0][0]:
            # We greatly prefer lines that start with capital letters.
            probability *= 5
        else:
            probability /= 4

        gathering = False
        in_progress = None
        last_yield = None
        for i in range(len(para)):
            line = para[i]
            if gathering:
                # We are currently putting together a quote.
                done = False
                if (random.random() < self.truncate_chance
                    and len(in_progress) >= self.minimum_quote_size):
                    # Yield a truncated quote.
                    done = True
                else:
                    potential = in_progress + ' ' + line.strip()
                    if len(potential) >= self.maximum_quote_size:
                        # That would be too long. We're done.
                        done = True
                    else:
                        in_progress = potential

                if done:
                    quote = in_progress
                    in_progress = None
                    gathering = done = False

                    # Miscellaneous tweaks to increase the chance that
                    # the quote will be funny.
                    if random.random() < 0.6:
                        quote = self.one_sentence_from(quote)

                    if random.random() < 0.4:
                        quote = self.truncate_at_stopword(quote)

                    # Quotes that end with two consecutive stopwords
                    # are not funny. It would be best to parse every
                    # single quote and make sure it doesn't end with
                    # two consecutive stopwords. But in practice it's
                    # much faster to just check for the biggest
                    # offenders, which all end in 'the', and then trim
                    # the 'the'.
                    low = quote.lower()
                    for stopwords in ('of the', 'in the', 'and the',
                                      'in the', 'on the', 'for the'):
                        if low.endswith(stopwords):
                            quote = quote[:len(" the")-1]
                            break

                    if isinstance(quote, bytes):
                        quote = quote.decode("utf8")
                    quote = self.remove_ending_punctuation(quote)
                    quote = self.remove_beginning_punctuation(quote)

                    if random.random() > 0.75:
                        quote = self.truncate_to_common_word(quote)

                    if (len(quote) >= self.minimum_quote_size
                        and len(quote) <= self.maximum_quote_size
                        and self.ONE_LETTER.search(quote)):
                        yield quote
                        last_yield = quote
                        continue
            else:
                # We are not currently gathering a quote. Should we
                # be?
                r = random.random()
                if random.random() < probability:
                    # Run the regular expression and see if it matches.
                    m = self.SEVERAL_CAPITALIZED_WORDS.search(line)
                    if m is not None:
                        phrase = m.groups()[0]
                        if "Gutenberg" in phrase or "Proofreader" in phrase:
                            # Part of the meta, not part of text.
                            continue
                        # Tag the text to see if it's a proper noun.
                        blob = TextBlob(phrase)
                        tags = blob.tags
                        proper_nouns = [x for x, tag in tags if tag.startswith('NNP')]
                        if len(proper_nouns) < len(tags) / 3.0:
                            # We're good.
                            yield phrase
                            continue

                matches = self._line_matches(line)
                if matches or random.random() < probability:
                    gathering = True
                    if matches:
                        # A keyword match! Start gathering a quote either
                        # at this line or some earlier line.
                        maximum_backtrack = int(
                            self.maximum_quote_size / self.wrap_at) - 1
                        backtrack = random.randint(0, maximum_backtrack)
                        start_at = max(0, i - backtrack)
                        in_progress = " ".join(
                            [x.strip() for x in para[start_at:i+1]])
                    else:
                        in_progress = line.strip()

    def _line_matches(self, line):
        l = line.lower()
        for keyword in self.keywords:
            if keyword in l:
                return True
        return False

