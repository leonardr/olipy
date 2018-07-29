import json
from olipy.queneau import WordAssembler
from olipy import corpora
import textwrap

common = corpora.words.english_words['words']
less_common = corpora.words.english_words['words']
common_corpus = WordAssembler(common)
full_corpus = WordAssembler(less_common)

print 'You know "%s", "%s", and "%s".' % tuple(common_corpus.assemble_word() for i in range(3))
print 'But have you heard of "%s", "%s", or "%s"?' % tuple(full_corpus.assemble_word() for i in range(3))

