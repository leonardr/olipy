olipy
=====

Olipy is a Python library for artistic text generation. It has many
useful modules.

queneau.py
----------

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

A module for incongruously sampling texts in the style of the infamous
@horse_ebooks. Based on the @zzt_ebooks algorithm by Adam Parrish.

Example scripts for ebooks.py:

* example.horse_ebooks.py: Selects some lines from a Project Gutenberg
  text, with a bias towards the keywords you give it as command-line
  arguments.

markov.py
---------

A module for generating new strings of tokens from old strings of
tokens using a Markov chains. The primary purpose of the olipy library
is to promote alternatives to Markov chains (such as Queneau assembly
and the _ebooks algorithm), but sometimes you really do want a Markov
chain.

Queneau assembly is usually better than a Markov chain above the word
level (constructing paragraphs from sentences) and below the word
level (constructing words from phonemes), but Markov chains are
usually better when assembling sequences of words.

markov.py was originally written by Adam "A. A." Parrish.

gibberish.py
------------

A module for those interested in the appearance of Unicode
glyphs. Its main use is generating aesthetically pleasing gibberish
using selected combinations of Unicode code charts.

Example scripts for gibberish.py:

* example.gibberish.py: Prints out a 140-character string of gibberish.

* example.corrupt.py: "Corrupts" whatever text is typed in by adding
increasing numbers of diacritical marks.

gutenberg.py
------------

A module for dealing with texts from Project Gutenberg.

integration.py
--------------

A module for integrating Olipy with other pieces of software (notably
the Twitter API).

wordfilter.py
-------------

A Python port of Darius Kazemi's word filter
(https://npmjs.org/package/wordfilter), for finding strings that
contain racial slurs and the like.

data/
-----

This directory contains data files used by the example scripts, as
well as some miscellaneous datasets useful in text generation projects.

* ids_for_old_gutenberg_filenames.json: Maps old-style (pre-2007)
  Project Gutenberg filenames to the new-style ebook IDs. For example,
  "/etext95/3boat10.zip" is mapped to the number 308 (see
  http://www.gutenberg.org/ebooks/308).
