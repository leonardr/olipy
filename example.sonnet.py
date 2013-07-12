import json
from queneau import Assembler
import textwrap
corpus = Assembler.load(open("data/shakespeare_sonnets.json"), tokens_in='lines')

print "\n".join(line for line, source in corpus.assemble())
