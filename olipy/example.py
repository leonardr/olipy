import argparse
import json
import logging
import re
import sys
import textwrap
from olipy import corpora
from olipy.ebooks import EbooksQuotes
from olipy.gibberish import (
    Corruptor,
    Gibberish,
)
from olipy.gutenberg import ProjectGutenbergText
from olipy.queneau import (
    Assembler,
    CompositeAssembler,
    DialogueAssembler,
    WordAssembler,
)
from olipy.typewriter import Typewriter

def apollo():
    transcript = corpora.words.literature.nonfiction.apollo_11['transcript']
    d = DialogueAssembler.loadlist(transcript)
    last_speaker = None
    for i in range(1, 100):
        speaker, tokens = d.assemble(last_speaker)
        last_speaker = speaker
        print("%s: %s" % (speaker, " ".join(x for x, y in tokens)))

def board_games(how_many=10):
    corpus = Assembler.loadlist(
        corpora.games.bgg_board_games['board_games'], tokens_in='description'
    )

    no_punctuation_at_end = re.compile("[a-zA-Z0-9]$")
    whitespace = re.compile("\s+")

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
        print(separator.join([x for x, source in choice]))

        # Make assemblers for the game's genres and mechanics
        for name, l in (('Genres', genres), ('Mechanics', mechanics)):
            assembler = Assembler()
            for list in l:
                assembler.add(list)
            choices = [choice for choice, source in assembler.assemble()]
            print("%s: %s" % (name, ", ".join(choices)))
        print("")

        for s in textwrap.wrap(" ".join(sentences)):
            print(s)
        if i < how_many-1:
            print("-" * 80)

def corrupt():
    """Corrupts whatever you type by adding diacritical marks."""
    if sys.version_info.major == 3:
        i = input
    else:
        i = raw_input

    go = True
    while go:
        data = i("> ")
        if data.strip() == '':
            break
        for corruption in range(10):
            print(Corruptor(corruption).corrupt(data) + "\n")
    
def dinosaurs():
    dinosaurs = corpora.animals.dinosaurs['dinosaurs']
    assembler = WordAssembler(dinosaurs)
    dinos = []
    for i in range(2):
        dino = assembler.assemble_word()
        if dino[0] in 'AEIO':
            dino = "an " + dino
        else:
            dino = "a " + dino
        dinos.append(dino)
    print("Look! Behind that ridge! It's %s fighting %s!" % tuple(dinos))

def ebooks():    
    parser = argparse.ArgumentParser(
        description="Generate pithy _ebooks quotes from Project Gutenberg texts.")
    parser.add_argument(
        '--path', help="The path to a mounted Project Gutenberg CD or DVD.",
        default=None)
    parser.add_argument(
        "keyword", nargs="*", help="Keywords to focus on when making selections.",
        default=["horse"])
    
    args = parser.parse_args()
    ebooks = EbooksQuotes(args.keyword)
    
    if args.path is None:
        default = corpora.words.literature.nonfiction.literary_shrines
        texts = [ProjectGutenbergText(default['text'])]
    else:
        texts = ProjectGutenbergText.texts_on_media(args.path)
    for text in texts:
        total = 0
        for para in text.paragraphs:
            for quote in ebooks.quotes_in(para):
                print(quote.encode("utf8"))
                total += 1
        logging.info("%d quotes found in text" % total)

def gibberish():
    print(Gibberish.random().tweet())
    
def mashteroids(how_many=10):
    import textwrap
    asteroids = corpora.science.minor_planet_details["minor_planets"]

    # Make an assembler to generate asteroid citations.
    corpus = Assembler.loadlist(asteroids, tokens_in='citation')

    for i in range(how_many):
        sentences = []
        names = []
        for sentence, source in corpus.assemble("f.l", min_length=3):
            sentences.append(sentence)
            names.append(source['name'])

        # Make a new assembler from the names of the asteroids that
        # were chosen, and use that to generate a new name
        name_assembler = WordAssembler(names)
        name = name_assembler.assemble_word()
        print(name)
        for s in textwrap.wrap(" ".join(sentences)):
            print(s)
        print("")

def sonnet():
    sonnets = corpora.words.literature.shakespeare_sonnets['sonnets']
    corpus = Assembler.loadlist(sonnets, tokens_in='lines')
    print("\n".join(line for line, source in corpus.assemble('0.l')))
        
def typewriter():
    print(Typewriter(3, 0.5).type(sys.stdin.read()))
    
def words():
    common = corpora.words.english_words['words']
    less_common = corpora.words.english_words['words']
    common_corpus = WordAssembler(common)
    full_corpus = WordAssembler(less_common)

    print('You know "%s", "%s", and "%s".' % tuple(common_corpus.assemble_word() for i in range(3)))
    print('But have you heard of "%s", "%s", or "%s"?' % tuple(full_corpus.assemble_word() for i in range(3)))


if __name__ == '__main__':
    func = sys
    module = sys.modules[__name__]
    getattr(module, sys.argv[1])()
