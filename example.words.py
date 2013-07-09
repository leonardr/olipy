import json
from queneau import WordAssembler
import textwrap
common_corpus = WordAssembler(json.load(open("data/english_words.common.json")))
full_corpus = WordAssembler(json.load(open("data/english_words.json")))

print 'You know "%s", "%s", and "%s".' % tuple(common_corpus.assemble_word() for i in range(3))
print 'But have you heard of "%s", "%s", or "%s"?' % tuple(full_corpus.assemble_word() for i in range(3))

