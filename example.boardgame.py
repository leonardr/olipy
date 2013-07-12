import json
import random
import re
import textwrap

from queneau import Assembler, CompositeAssembler, WordAssembler
corpus = Assembler.loadlines(open("data/boardgames.txt"), tokens_in='description')

no_punctuation_at_end = re.compile("[a-zA-Z0-9]$")
whitespace = re.compile("\s+")

how_many = 10
for i in range(how_many):

    sentences = []
    names = []
    genres = []
    mechanics = []
    for line, source in corpus.assemble("0.l"):
        if no_punctuation_at_end.search(line):
            line += "."
        sentences.append(line)
        names.append(source['name'])
        genres.append([genre for id, genre in source.get('boardgamecategory', [])])
        mechanics.append([mechanic for id, mechanic in source.get('boardgamemechanic', [])])

    # Make assemblers for single- and multi-word names.
    single_word_assembler = WordAssembler()
    multi_word_assembler = Assembler()

    # Create a composite assembler that will choose single- and
    # multi-word names in appropriate proportion.
    name_assembler = CompositeAssembler([single_word_assembler, multi_word_assembler])
    for name in names:
        words = whitespace.split(name)
        if len(words) == 1:
            single_word_assembler.add(name)
        else:
            multi_word_assembler.add(words)
    assembler, choice = name_assembler.assemble()
    if assembler == single_word_assembler:
        separator = ''
    else:
        separator = ' '
    print separator.join([x for x, source in choice])

    # Make assemblers for the game's genres and mechanics
    for name, l in (('Genres', genres), ('Mechanics', mechanics)):
        assembler = Assembler()
        for list in l:
            assembler.add(list)
        choices = [choice for choice, source in assembler.assemble()]
        print "%s: %s" % (name, ", ".join(choices))
    print
    for s in textwrap.wrap(" ".join(sentences)):
        print s
    if i < how_many-1:
        print "-" * 80
