olipy
=====

Olipy is a Python library for artistic text generation. It has two
main modules.

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

gibberish.py
------------

A module for those interested in the appearance of Unicode
glyphs. Its main use is generating aesthetically pleasing gibberish
using selected combinations of Unicode code charts.

Example scripts for gibberish.py:

* example.gibberish.py: Prints out a 140-character string of gibberish.

* example.corrupt.py: "Corrupts" whatever text is typed in by adding
increasing numbers of diacritical marks.

integration.py
--------------

A module for integrating Olipy with other pieces of software (notably
the Twitter API).

data/
-----

This directory contains data files used by the example scripts.
