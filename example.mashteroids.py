from olipy.queneau import Assembler, WordAssembler
import textwrap
from olipy import corpora
corpus = Assembler.loadlist(
    corpora.science.minor_planet_details["minor_planets"],
    tokens_in='citation'
)

how_many = 100
for i in range(how_many):

    sentences = []
    names = []
    for sentence, source in corpus.assemble("f.l", min_length=3):
        sentences.append(sentence)
        names.append(source['name'])

    # Make a new assembler from the names of the asteroids that were chosen.
    name_assembler = WordAssembler(names)
    name = name_assembler.assemble_word()
    print(name)
    for s in textwrap.wrap(" ".join(sentences)):
        print(s)

    if i < how_many-1:
        print("")
