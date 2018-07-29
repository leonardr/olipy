olipy
=====

Olipy is a Python library for artistic text generation. It has many
useful modules.

Setup
-----

Olipy uses the [`TextBlob`](https://textblob.readthedocs.org/) library
to parse text. Note that `TextBlob` has extra dependencies (text
corpora) which are not installed as part of the Python package.
Instructions for installing the extra dependencies are on the `TextBlob`
site, but they boil down to running [this Python
script](https://raw.github.com/sloria/TextBlob/master/download_corpora.py).

alphabet.py
-----------

A list of interesting groups of Unicode characters -- alphabets, shapes, and so on.

```
from olipy.alphabet import Alphabet
print(Alphabet.default().random_choice())
# 𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷
print(Alphabet.default().random_choice())
# ┌┐└┘├┤┬┴┼═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬╴╵╶╷
```

This module is used heavily by gibberish.py.

alternate_letterforms.py
------------------------

Translates from letters of the English alphabet to similar-looking
characters.

```
from olipy.alternate_letterforms import alternate_spelling
print(alternate_spelling("I love alternate letterforms."))
# ヱ 𝑳𝖮Ⓥ𝙀 𝚊𝓵┯⒠┌𝐍ａ⫪𝖊 𝐋𝖾ߙ𝓉ᥱ𝙧ߓ𝕠┍ጠ𝑆.
```

corpus.py
---------

A simple wrapper that makes it easy to load datasets from Darius
Kazemi's [`corpora`](https://github.com/dariusk/corpora) project, as
well as additional corpora specific to Olipy -- mostly large word
lists which `corpora` considers out of scope.

Olipy is packaged with a complete copy of the data from the `corpora`
project, so you don't have to install anything extra. However,
installing `corpora` some other way can give you

```
from olipy.corpus import Corpus
for city in Corpus.load("large_cities"):
    print(city)
# Akron
# Albequerque
# Anchorage
# ...
```

TODO: compatibility with pycorpora project

TODO: needs some work in general

Example scripts for corpus.py:

* example.corpus.py: List and display available datasets.

ebooks.py
---------

A module for incongruously sampling texts in the style of the infamous
[https://twitter.com/horse_ebooks](@horse_ebooks). Based on the
[https://twitter.com/zzt_ebooks](@zzt_ebooks) algorithm by Allison
Parrish.

```
from olipy.ebooks import EbooksQuotes
data = open("olipy/data/44269.txt.utf-8").read().decode("utf8")
for quote in EbooksQuotes().quotes_in(data):
    print(quote)
# informed his audience that not many men  eminent in literature have been born
# acquired an unnatural preference for the country, and not only held
# scarcely  greater than that.
# Otherwise, except
# ...
```

Example scripts for ebooks.py:

* example.ebooks.py: Selects some lines from a Project Gutenberg
  text, with a bias towards the keywords you give it as command-line
  arguments.

gibberish.py
------------

A module for those interested in the appearance of Unicode
glyphs. Its main use is generating aesthetically pleasing gibberish
using selected combinations of Unicode code charts.

```
from olipy.gibberish import Gibberish
print(Gibberish.random().tweet().encode("utf8"))
# ৠ𐒧𐒇দ𐒔𐒜ৗ𐒃𐒝𐒓আ৭৭উ𐒇৶০ধপ𐒤৯ৰ৪ড়ঐবননত৲ফঌ𐒓৴ৄু০েএঠৰ𐒔𐒥গনি৶ঘ𐒋উঙ𐒤ঙছতাৃীফ৮৬৸উকফ𐒘ইমঢ৭ূণঌঊ𐒇𐒋ীঁিৃ𐒌𐒒৺𐒤৺ভ𐒖৭𐒤ৡৰল𐒊ঢ়ৎ𐒅যথখৱঌ
# ঈঔ৫ঽ𐒔৩়দ𐒋ৠসুয়ঊশ𐒆𐒖𐒁ঔৰসঈ𐒆অ𐒋𐒑𐒨়দ৯ৄ৫ 😘
```

Example scripts for gibberish.py:

* example.gibberish.py: Prints out a 140-character string of gibberish.

* example.corrupt.py: "Corrupts" whatever text is typed in by adding
increasing numbers of diacritical marks.

gutenberg.py
------------

_Dependencies:_ `rdflib` (Only necessary if you have a copy of [Project
Gutenberg's RDF
catalog](http://www.gutenberg.org/wiki/Gutenberg:Feeds#Current_RDF_Format)
and you want to get extra metadata from it.)

A module for dealing with texts from Project Gutenberg. Strips headers
and footers, and parses the text.

```
from olipy.gutenberg import ProjectGutenbergText
text = ProjectGutenbergText(open("olipy/data/44269.txt.utf-8").read())
print(len(text.paragraphs))
# 1258
```

Example scripts for gutenberg.py:

* example.ebooks.py: Selects some lines from a Project Gutenberg
  text, with a bias towards the keywords you give it as command-line
  arguments.

markov.py
---------

A module for generating new token lists from old token lists using a
Markov chain.

The primary purpose of the olipy library is to promote alternatives to
Markov chains (such as Queneau assembly and the _ebooks algorithm),
but sometimes you really do want a Markov chain. Queneau assembly is
usually better than a Markov chain above the word level (constructing
paragraphs from sentences) and below the word level (constructing
words from phonemes), but Markov chains are usually better when
assembling sequences of words.

markov.py was originally written by Allison "A. A." Parrish.

```
from olipy.markov import MarkovGenerator
g = MarkovGenerator.load(open("olipy/data/44269.txt.utf-8"), order=1, max=100)
print(" ".join(g.assemble()))
# The Project Gutenberg-tm depends upon her
# husband, whose writings never knew,
# and to get up in
# theatrical circles two that "he was a compilation copyright in 1809, many men
# eminent in his
# _Prothalamion_ speaks of obtaining of course; and the
# ...
```

mosaic.py
---------

Tiles Unicode characters together to create symmetrical mosaics.
gibberish.py uses this module as one of its techniques. Includes
information on Unicode characters whose glyphs appear to be mirror
images.

```
from olipy.mosaic import MirroredMosaicGibberish
mosaic = MirroredMosaicGibberish()
print(mosaic.tweet())
# ▛▞ ▙▞▙▟▚▟ ▚▜
# ▛▞▞ ▞▛▜▚ ▚▚▜
#  ▞▙  ▞▚  ▟▚ 
# ▙▚▚ ▚▙▟▞ ▞▞▟
# ▙▚ ▛▚▛▜▞▜ ▞▟

print(gibberish.tweet())
# 🙌🙌😯📶🙌👍👍🙌📶😯🙌🙌
#  📶🙌😯🙌🕠🕠🙌😯🙌📶 
# 🚂💈🎈🔒🚲🕃🕃🚲🔒🎈💈🚂
#  📶🙌😯🙌🕠🕠🙌😯🙌📶 
# 🙌🙌😯📶🙌👍👍🙌📶😯🙌🙌

```

queneau.py
----------

A module for Queneau assembly, a technique pioneered by Raymond
Queneau in his 1961 book "Cent mille milliards de poèmes" ("One
hundred million million poems"). Queneau assembly randomly creates new
texts from a collection of existing texts with identical structure.

```
from olipy.queneau import WordAssembler
from olipy.corpus import Corpus
assembler = WordAssembler(Corpus.load("dinosaurs"))
print(assembler.assemble_word())
# Trilusmiasunaus
```

Example scripts for queneau.py:

* example.words.py: Generates common-looking and obscure-looking English
words. Demonstrates Queneau assembly on parts of a word.

* example.mashteroids.py: Generates names and IAU citations for minor
planets. Demonstrates Queneau assembly on sentences.

* example.apollo.py: Generates dialogue between astronauts and Mission
Control. Demonstrates Queneau assembly on dialogue.

* example.boardgame.py: Generates board game names and descriptions.

* example.sonnet.py: Generates Shakespearean sonnets.

* example.dinosaurs.py: Generates dinosaur names.

randomness.py
-------------

Techniques for generating random patterns that are more sophisticated than
simple selection.

The `Gradient` class generates a string of random choices that are
weighted towards one set of options near the start, and weighted
towards another set of options near the end.

Here's a gradient from lowercase letters to uppercase letters:

```
from olipy.randomness import Gradient
import string
print("".join(Gradient.gradient(string.lowercase, string.uppercase, 40)))
# rkwyobijqQOzKfdcSHIhYINGrQkBRddEWPHYtORB
```

The `WanderingMonsterTable` class lets you make random choices from
roughly weighted lists of options.

```
from olipy.randomness import WanderingMonsterTable

monsters = WanderingMonsterTable(
         common=["Giant rat", "Alligator"],
         uncommon=["Orc", "Hobgoblin"],
         rare=["Beholder", "Neo-otyugh"],
         very_rare=["Flump", "Ygorl, Lord of Entropy"],
)
for i in range(5):
    print monsters.choice()
# Giant rat
# Alligator
# Alligator
# Orc
# Giant rat
```

tokenizer.py
------------

A word tokenizer that performs better than NLTK's default tokenizers
on some common types of English.

>>> from nltk.tokenize.treebank import TreebankWordTokenizer
>>> s = '''Good muffins cost $3.88\\nin New York. Email: muffins@example.com'''
>>> TreebankWordTokenizer().tokenize(s)
# ['Good', 'muffins', 'cost', '$', '3.88', 'in', 'New', 'York.', 'Email', ':', 'muffins', '@', 'example.com']
>>> WordTokenizer().tokenize(s)
# ['Good', 'muffins', 'cost', '$', '3.88', 'in', 'New', 'York.', 'Email:', 'muffins@example.com']

typewriter.py
-------------

Simulates the Adler Universal 39 typewriter used in "The Shining" and
the sorts of typos that would be made on that typewriter. Originally
written for @a_dull_bot.

```
from olipy.typewriter import Typewriter
typewriter = Typewriter()
typewriter.type("All work and no play makes Jack a dull boy.")
# 'All work and no play makes Jack a dull bo6.'
```

Example scripts for gibberish.py:

* example.typewriter.py: Retypes standard input on the Adler Universal
  39, with about 10 typos per 100 characters.

Extra corpora
-------------

The data/corpora-more/ directory contains several word lists and
datasets that aren't in the the Corpora project. These datasets (as
well as the ones in dariusk/corpora) can be accessed through the
`corpus` module. Just write code like this:

```
from corpus import Corpus
Corpus.load("abstract_nouns")
```

**Word lists**

Most of these lists are lists of words sorted by frequency of
occurance in English. In general, these word lists are too large to
fit in the corpora project. Some of them have been manually edited to
minimize the risk of embarrassing or offensive output. (But it's
ultimately up to you.)

_geography/large_cities.json_

Names of large U.S. and world cities.

_geography/us_states.json_

The fifty U.S. states.

Names of large U.S. and world cities.

_language/languages.json_

Names of languages defined in ISO-639-1

_language/unicode_code_sheets.json_

The name of every Unicode code sheet, with the characters found on that sheet.

_science/minor_planets.json_

'name', 'number' and IAU 'citation' for named minor planets
(e.g. asteroids) as of July 2013. The 'discovery' field contains
discovery circumstances. The 'suggested_by' field, when present, has
been split out from the end of the original IAU citation with a simple
heuristic. The 'citation' field has then been tokenized into sentences
using NLTK's Punkt tokenizer and a set of custom abbreviations.

Data sources: 
 http://www.minorplanetcenter.net/iau/lists/NumberedMPs.html
 http://ssd.jpl.nasa.gov/sbdb.cgi

_words/adjectives.json_

About 5000 English adjectives, sorted roughly by frequency of occurrence.

_words/common_nouns.json_

Lists of English nouns, sorted roughly by frequency of occurrence.

Includes:

* `abstract_nouns` like "work" and "love".
* `concrete_nouns` like "face" and "house".
* `adjectival_nouns` -- nouns that can also act as adjectives -- like "chance" and "light".

_words/common_verbs.json_

Lists of English verbs, sorted roughly by frequency of occurrence.

* `present_tense` verbs like "get" and "want".
* `past_tense` verbs like "said" and "found".
* `gerund` forms like "holding" and "leaving".

_words/english_words.json_

A consolidated list of about 73,000 English words from the FRELI
project. (http://www.nkuitse.com/freli/)

_words/scribblenauts.json_

The top 4000 nouns that were 'concrete' enough to be summonable in the
2009 game Scribblenauts. As always, this list is ordered with more common
words towards the front.

_words/literature/apollo_11.json__

Transcripts of the Apollo 11 mission, presented as dialogue, tokenized
into sentences using NLTK's Punkt tokenizer. One JSON object per line.

Data sources:
 The Apollo 11 Flight Journal: http://history.nasa.gov/ap11fj/
 The Apollo 11 Surface Journal: http://history.nasa.gov/alsj/
 "Intended to be a resource for all those interested in the Apollo
  program, whether in a passing or scholarly capacity."

_words/literature/boardgames.json_

Information about board games, collected from BoardGameGeek in July
2013. One JSON object per line.

Data source:
 http://boardgamegeek.com/wiki/page/BGG_XML_API2

_words/literature/shakespeare_sonnets.json_

The sonnets of William Shakespeare. Data source: http://www.gutenberg.org/ebooks/1041

data/
-----

This directory contains data files used by the example scripts, as
well as some miscellaneous datasets useful in text generation
projects. These aren't 'corpora' per se and you probably won't need to
use them.

* 44269.txt.utf-8: The complete text of a public domain book
  ("Famous Houses and Literary Shrines of London" by A. St. John
  Adcock). This is included so you can test your project against a
  real book-length text without downloading anything extra.

* ids_for_old_gutenberg_filenames.json: Maps old-style (pre-2007)
  Project Gutenberg filenames to the new-style ebook IDs. For example,
  "/etext95/3boat10.zip" is mapped to the number 308 (see
  http://www.gutenberg.org/ebooks/308).
