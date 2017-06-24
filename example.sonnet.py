import json
from queneau import Assembler
import textwrap
from corpus import Corpus
corpus = Assembler.loadlist(
    Corpus.load("shakespeare_sonnets"), tokens_in='lines'
)

print "\n".join(line for line, source in corpus.assemble('0.l'))
