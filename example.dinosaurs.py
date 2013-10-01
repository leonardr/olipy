import json
from queneau import WordAssembler
from data import load_json
import textwrap
assembler = WordAssembler(load_json("dinosaurs.json"))

dinos = []
for i in range(2):
    dino = assembler.assemble_word()
    if dino[0] in 'AEIO':
        dino = "an " + dino
    else:
        dino = "a " + dino
    dinos.append(dino)

print "Look! Behind that ridge! It's %s fighting %s!" % tuple(dinos)
