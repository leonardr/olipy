# Olipy

Olipy is a Python library for artistic text generation. It includes useful datasets and algorithms for using characters, words, and texts to create aesthetic effects.

# Setup

`pip install olipy`

Olipy uses the [`TextBlob`](https://textblob.readthedocs.org/) library
to parse text. Installing Olipy through `pip` will install
TextBlob as a dependency, but `TextBlob` has extra dependencies (text corpora) which
are _not_ installed by `pip`.  Instructions for installing the extra
dependencies are on the `TextBlob` site, but they boil down to running
[this Python
script](https://raw.github.com/sloria/TextBlob/master/download_corpora.py).

# Module guide

## alphabet.py

A list of interesting groups of Unicode characters -- alphabets, shapes, and so on.

```
from olipy.alphabet import Alphabet
print(Alphabet.default().random_choice())
# 𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷
print(Alphabet.default().random_choice())
# ┌┐└┘├┤┬┴┼═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬╴╵╶╷
```

This module is used heavily by gibberish.py.

## alternate_letterforms.py

Translates from letters of the English alphabet to similar-looking
characters.

```
from olipy.alternate_letterforms import alternate_spelling
print(alternate_spelling("I love alternate letterforms."))
# ヱ 𝑳𝖮Ⓥ𝙀 𝚊𝓵┯⒠┌𝐍ａ⫪𝖊 𝐋𝖾ߙ𝓉ᥱ𝙧ߓ𝕠┍ጠ𝑆.
```

# corpora.py

This module makes it easy to load datasets from Darius
Kazemi's [Corpora Project](https://github.com/dariusk/corpora), as
well as additional datasets specific to Olipy -- mostly large word
lists which the Corpora Project considers out of scope. (These new
datasets are discussed at the end of this document.)

Olipy is packaged with a complete copy of the data from the Corpora
Project, so you don't have to install anything extra. However,
installing the Corpora Project data some other way can give you
datasets created since the Olipy package was updated.

The interface of the `corpora` module is that used by Allison Parrish's
[`pycorpora`](https://github.com/aparrish/pycorpora/) project. The
datasets show up as Python modules which contain Python data
structures:

```
from olipy import corpora
for city in corpora.geography.large_cities['cities']:
    print(city)
# Akron
# Albequerque
# Anchorage
# ...
```

You can use `from corpora import` ... to import a particular Corpora
Project category:

```
from olipy.corpora import governments
print(governments.nsa_projects["codenames"][0] # prints "ARTIFICE")

from olipy.pycorpora import humans
print(humans.occupations["occupations"][0] # prints "accountant")
```

Additionally, corpora supports an API similar to that provided by the Corpora Project node package:

```
from olipy import corpora

# get a list of all categories
corpora.get_categories() # ["animals", "archetypes"...]

# get a list of subcategories for a particular category
corpora.get_categories("words") # ["literature", "word_clues"...]

# get a list of all files in a particular category
corpora.get_files("animals") # ["birds_antarctica", "birds_uk", ...]

# get data deserialized from the JSON data in a particular file
corpora.get_file("animals", "birds_antarctica") # returns dict w/data

# get file in a subcategory
corpora.get_file("words/literature", "shakespeare_words")
```

## ebooks.py

A module for incongruously sampling texts in the style of the infamous
[https://twitter.com/horse_ebooks](@horse_ebooks). Based on the
[https://twitter.com/zzt_ebooks](@zzt_ebooks) algorithm by Allison
Parrish.

```
from olipy.ebooks import EbooksQuotes
from olipy import corpora
data = corpora.words.literature.fiction.pride_and_prejudice
for quote in EbooksQuotes().quotes_in(data['text']):
    print(quote)
# They attacked him  in various ways--with barefaced
# An invitation to dinner
# Mrs. Bennet
# ...
```

Example scripts for ebooks.py:

* example.ebooks.py: Selects some lines from a Project Gutenberg
  text, with a bias towards the keywords you give it as command-line
  arguments.

## gibberish.py

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

## gutenberg.py

A module for dealing with texts from Project Gutenberg. Strips headers
and footers, and parses the text.

```
from olipy.gutenberg import ProjectGutenbergText
text = corpora.words.literature.nonfiction.literary_shrines['text']
text = ProjectGutenbergText(text)
print(len(text.paragraphs))
# 1258
```

Example scripts for gutenberg.py:

* example.ebooks.py: Selects some lines from a Project Gutenberg
  text, with a bias towards the keywords you give it as command-line
  arguments.

## markov.py

A module for generating new token lists from old token lists using a
Markov chain.

Olipy's primary purpose is to promote alternatives to
Markov chains (such as Queneau assembly and the ebooks algorithm),
but sometimes you really do want a Markov chain. Queneau assembly is
usually better than a Markov chain above the word level (constructing
paragraphs from sentences) and below the word level (constructing
words from phonemes), but Markov chains are usually better when
assembling sequences of words.

markov.py was originally written by Allison "A. A." Parrish.

```
from olipy.markov import MarkovGenerator
from olipy import corpora
text = corpora.words.literature.nonfiction.literary_shrines['text']
g = MarkovGenerator(order=1, max=100)
g.add(text)
print(" ".join(g.assemble()))
# The Project Gutenberg-tm trademark.                    Canst thou, e'en thus, thy own savings, went as the gardens, the club. The quarrel occurred between
# him and his essay on the tea-table. In these that, in Lamb's day, for a stray
# relic or four years ago, taken with only Adam and _The
# Corsair_. Writing to his home on his new purple and the young man you might
# mean nothing on Christmas sports and art seriously instead of references to
# the heart'--allowed--yet I got out and more convenient.... Mr.
```

## mosaic.py

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

## queneau.py

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

The original purpose of Olipy was to promote Queneau assembly, and there are many scripts
which show what it's capable of:

* example.words.py: Generates common-looking and obscure-looking English
words. Demonstrates Queneau assembly on parts of a word.
* example.mashteroids.py: Generates names and IAU citations for minor
planets. Demonstrates Queneau assembly on sentences.
* example.apollo.py: Generates dialogue between astronauts and Mission
Control. Demonstrates Queneau assembly on dialogue.
* example.boardgame.py: Generates board game names and descriptions.
* example.sonnet.py: Generates Shakespearean sonnets.
* example.dinosaurs.py: Generates dinosaur names.

## randomness.py

Techniques for generating random patterns that are more sophisticated `random.choice`.

### `Gradient`

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

### `WanderingMonsterTable`

The `WanderingMonsterTable` class lets you make a weighted random selection from 
one of four buckets. A random selection from the "common" bucket will show up 65% of the time, a 
selection from the "uncommon" bucket 20% of the time, "rare" 11% of the time, and "very rare" 4% of 
the time. (It uses the same probabilities as the first edition of Advanced Dungeons & Dragons.)

```
from olipy.randomness import WanderingMonsterTable

monsters = WanderingMonsterTable(
         common=["Giant rat", "Alligator"],
         uncommon=["Orc", "Hobgoblin"],
         rare=["Mind flayer", "Neo-otyugh"],
         very_rare=["Flumph", "Ygorl, Lord of Entropy"],
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

```
>>> from nltk.tokenize.treebank import TreebankWordTokenizer
>>> s = '''Good muffins cost $3.88\\nin New York. Email: muffins@example.com'''
>>> TreebankWordTokenizer().tokenize(s)
# ['Good', 'muffins', 'cost', '$', '3.88', 'in', 'New', 'York.', 'Email', ':', 'muffins', '@', 'example.com']
>>> WordTokenizer().tokenize(s)
# ['Good', 'muffins', 'cost', '$', '3.88', 'in', 'New', 'York.', 'Email:', 'muffins@example.com']
```

typewriter.py
-------------

Simulates the Adler Universal 39 typewriter used in "The Shining" and
the sorts of typos that would be made on that typewriter. Originally
written for [@a_dull_bot](https://botsin.space/@adullbot).

```
from olipy.typewriter import Typewriter
typewriter = Typewriter()
typewriter.type("All work and no play makes Jack a dull boy.")
# 'All work and no play makes Jack a dull bo6.'
```

Example scripts for gibberish.py:

* example.typewriter.py: Retypes standard input on the Adler Universal
  39, with about 10 typos per 100 characters.

# Extra corpora

Olipy makes available several word lists and datasets that aren't in
the Corpora Project. These datasets (as well as the standard Corpora
Project datasets) can be accessed through the `corpora` module. Just
write code like this:

```
from olipy import corpora
nouns = corpora.words.common_nouns['abstract_nouns']
```

### `corpora.geography.large_cities`

Names of large U.S. and world cities.

### `corpora.geography.us_states`

The fifty U.S. states.

### `corpora.language.languages`

Names of languages defined in ISO-639-1

### `corpora.language.unicode_code_sheets`

The name of every Unicode code sheet, each with the characters found on that sheet.

### `corpora.science.minor_planets`

'name', 'number' and IAU 'citation' for named minor planets
(e.g. asteroids) as of July 2013. The 'discovery' field contains
discovery circumstances. The 'suggested_by' field, when present, has
been split out from the end of the original IAU citation with a simple
heuristic. The 'citation' field has then been tokenized into sentences
using NLTK's Punkt tokenizer and a set of custom abbreviations.

Data sources: 
 http://www.minorplanetcenter.net/iau/lists/NumberedMPs.html
 http://ssd.jpl.nasa.gov/sbdb.cgi

This overrides the Corpora Project's list of the names of the first
1000 minor planets.

### `corpora.words.adjectives`

About 5000 English adjectives, sorted roughly by frequency of occurrence.

### `corpora.words.common_nouns`

Lists of English nouns, sorted roughly by frequency of occurrence.

Includes:

* `abstract_nouns` like "work" and "love".
* `concrete_nouns` like "face" and "house".
* `adjectival_nouns` -- nouns that can also act as adjectives -- like "chance" and "light".

### `corpora.words.common_verbs`

Lists of English verbs, sorted roughly by frequency of occurrence.

* `present_tense` verbs like "get" and "want".
* `past_tense` verbs like "said" and "found".
* `gerund` forms like "holding" and "leaving".

### `corpora.words.english_words`

A consolidated list of about 73,000 English words from the FRELI
project. (http://www.nkuitse.com/freli/)

### `corpora.words.scribblenauts`

The top 4000 nouns that were 'concrete' enough to be summonable in the
2009 game _Scribblenauts_. As always, this list is ordered with more common
words towards the front.

### `corpora.words.literature.board_games`

Information about board games, collected from BoardGameGeek in July
2013. One JSON object per line.

Data source:
 http://boardgamegeek.com/wiki/page/BGG_XML_API2


### `corpora.words.literature.fiction.pride_and_prejudice`

The complete text of a public domain novel ("Pride and Prejudice"
by Jane Austen).

### `corpora.words.literature.nonfiction.apollo_11`

Transcripts of the Apollo 11 mission, presented as dialogue, tokenized
into sentences using NLTK's Punkt tokenizer. One JSON object per line.

Data sources:
 The Apollo 11 Flight Journal: http://history.nasa.gov/ap11fj/
 The Apollo 11 Surface Journal: http://history.nasa.gov/alsj/
 "Intended to be a resource for all those interested in the Apollo
  program, whether in a passing or scholarly capacity."

### `corpora.words.literature.nonfiction.literary_shrines`

The complete text of a public domain nonfiction book ("Famous Houses
and Literary Shrines of London" by A. St. John Adcock).

### `corpora.words.literature.gutenberg_id_mapping`

Maps old-style (pre-2007) Project Gutenberg filenames to the new-style
ebook IDs. For example, "/etext95/3boat10.zip" is mapped to the
number 308 (see http://www.gutenberg.org/ebooks/308). Pretty much
nobody needs this.

### `corpora.words.literature.shakespeare_sonnets`

The sonnets of William Shakespeare. Data source: http://www.gutenberg.org/ebooks/1041
