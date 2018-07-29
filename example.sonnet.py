from olipy.queneau import Assembler
from olipy import corpora
corpus = Assembler.loadlist(
    corpora.words.literature.shakespeare_sonnets['sonnets'], tokens_in='lines'
)

print "\n".join(line for line, source in corpus.assemble('0.l'))
