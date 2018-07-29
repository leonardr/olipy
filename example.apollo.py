import json
from olipy.queneau import DialogueAssembler
from olipy import corpora
d = DialogueAssembler.loadlist(corpora.words.literature.nonfiction.apollo_11['transcript'])
last_speaker = None
for i in range(1, 100):
    speaker, tokens = d.assemble(last_speaker)
    last_speaker = speaker
    print "%s: %s" % (speaker, " ".join(x for x, y in tokens))
    print
