import json
from olipy.queneau import WordAssembler
from olipy.corpus import Corpus
import textwrap
common_corpus = WordAssembler(Corpus.load("english_words.common"))
full_corpus = WordAssembler(Corpus.load("english_words"))

print 'You know "%s", "%s", and "%s".' % tuple(common_corpus.assemble_word() for i in range(3))
print 'But have you heard of "%s", "%s", or "%s"?' % tuple(full_corpus.assemble_word() for i in range(3))

