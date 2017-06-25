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

queneau.py
----------

_Dependencies:_ `TextBlob`

A module for Queneau assembly, a technique pioneered by Raymond
Queneau in his 1961 book "Cent mille milliards de poèmes" ("One
hundred million million poems"). Queneau assembly randomly creates new
texts from a collection of existing texts with identical structure.

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

ebooks.py
---------

_Dependencies:_ `TextBlob`

A module for incongruously sampling texts in the style of the infamous
[https://twitter.com/horse_ebooks](@horse_ebooks). Based on the
[https://twitter.com/zzt_ebooks](@zzt_ebooks) algorithm by Allison
Parrish.

Example scripts for ebooks.py:

* example.horse_ebooks.py: Selects some lines from a Project Gutenberg
  text, with a bias towards the keywords you give it as command-line
  arguments.

markov.py
---------

_Dependencies:_ None

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

corpora.py
----------

_Dependencies:_ corpora (run `git submodule init` within the olipy directory)

A simple wrapper that makes it easy to load datasets from Darius
Kazemi's `corpora` project, as well as additional corpora (mostly
large word lists) specific to olipy.

Example scripts for corpora.py:

* example.corpora.py: List and display available datasets.

gibberish.py
------------

_Dependencies:_ None

A module for those interested in the appearance of Unicode
glyphs. Its main use is generating aesthetically pleasing gibberish
using selected combinations of Unicode code charts.

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

A module for dealing with texts from Project Gutenberg.

integration.py
--------------

_Dependencies:_ python-twitter

A module for integrating Olipy with other pieces of software (notably
the Twitter API).

typewriter.py
-------------

Simulates the Adler Universal 39 typewriter used in "The Shining" and
the sorts of typos that are commonly made on that
typewriter. Originally written for @a_dull_bot.

Example scripts for gibberish.py:

* example.typewriter.py: Retypes standard input on the Adler Universal
  39, with about 10 typos per 100 characters.

wordfilter.py
-------------

_Dependencies:_ None

A Python port of [Darius Kazemi's word
filter](https://npmjs.org/package/wordfilter), for finding strings
that contain racial slurs and the like.

Extra corpora
-------------

The data/more-corpora/ directory contains several word lists and
datasets that aren't in the dariusk/corpora module. These datasets (as
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

* abstract_nouns.txt - The 4000 most common abstract concepts, like
  "work" and "love".

* adjectival_nouns.txt - The top 1000 nouns that can also act as
  adjectives.

* adjectives.txt - The 5000 most common adjectives.

* english_words.json - A consolidated list of English words from the
  FRELI project. (http://www.nkuitse.com/freli/)

* english_words.common.json - A subset of the list of words in
  english_words, focusing on relatively common words shorter than 10
  characters.

* concrete_nouns.txt - The opposite of abstract_nouns.txt. These nouns
  refer to more concrete things like "hometown" and
  "masterpiece". (But see scribblenauts_words.txt to get even more
  concrete.)

* gerunds.txt - The 3000 most common gerunds.

* past_tense.txt - The 3000 most common past tense verbs.

* present_tense.txt - The 2000 most common present tense verbs.

* scribblenauts_words.txt - The top 4000 nouns that were 'concrete'
  enough to be summonable in the game Scribblenauts.

**Large datasets**

_apollo_11.ndjson_

Transcripts of the Apollo 11 mission, presented as dialogue, tokenized
into sentences using NLTK's Punkt tokenizer. One JSON object per line.

Data sources:
 The Apollo 11 Flight Journal: http://history.nasa.gov/ap11fj/
 The Apollo 11 Surface Journal: http://history.nasa.gov/alsj/
 "Intended to be a resource for all those interested in the Apollo
  program, whether in a passing or scholarly capacity."

_boardgames.txt_

Information about board games, collected from BoardGameGeek in July
2013. One JSON object per line.

Data source:
 http://boardgamegeek.com/wiki/page/BGG_XML_API2

_minor_planets.json_

'name', 'number' and IAU 'citation' for named minor planets
(e.g. asteroids) as of July 2013. The 'discovery' field contains
discovery circumstances. The 'suggested_by' field, when present, has
been split out from the end of the original IAU citation with a simple
heuristic. The 'citation' field has then been tokenized into sentences
using NLTK's Punkt tokenizer and a set of custom abbreviations.

Data sources: 
 http://www.minorplanetcenter.net/iau/lists/NumberedMPs.html
 http://ssd.jpl.nasa.gov/sbdb.cgi

_shakespeare_sonnets.json_

The sonnets of William Shakespeare. Data source: http://www.gutenberg.org/ebooks/1041

**Small datasets**

* large_cities.json - Large U.S. and world cities
* languages.json - ISO-639-1 languages
* slurs.json - Racial slurs, used in wordfilter
* stopwords.json - Stopwords as defined by MySQL
* us_states.json - U.S. states (just the 50)
* unicode_code_sheets.json - Lists of the Unicode characters on various code sheets.

data/
-----

This directory contains data files used by the example scripts, as
well as some miscellaneous datasets useful in text generation
projects. These aren't 'corpora' per se.

* ids_for_old_gutenberg_filenames.json: Maps old-style (pre-2007)
  Project Gutenberg filenames to the new-style ebook IDs. For example,
  "/etext95/3boat10.zip" is mapped to the number 308 (see
  http://www.gutenberg.org/ebooks/308).

* 44269.txt.utf-8: The complete text of a public domain book
  ("Famous Houses and Literary Shrines of London" by A. St. John
  Adcock).

