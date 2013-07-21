import json
from queneau import DialogueAssembler

d = DialogueAssembler.loadlines(open("data/apollo_11.txt"))
last_speaker = None
for i in range(1, 100):
    speaker, tokens = d.assemble(last_speaker)
    last_speaker = speaker
    print "%s: %s" % (speaker, " ".join(x for x, y in tokens))
    print
