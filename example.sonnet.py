import json
from olipy.queneau import Assembler
import textwrap
from olipy.corpus import Corpus
corpus = Assembler.loadlist(
    Corpus.load("shakespeare_sonnets"), tokens_in='lines'
)

print "\n".join(line for line, source in corpus.assemble('0.l'))
