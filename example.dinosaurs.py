from olipy.queneau import WordAssembler
from olipy import corpora
assembler = WordAssembler(corpora.animals.dinosaurs['dinosaurs'])

dinos = []
for i in range(2):
    dino = assembler.assemble_word()
    if dino[0] in 'AEIO':
        dino = "an " + dino
    else:
        dino = "a " + dino
    dinos.append(dino)

print "Look! Behind that ridge! It's %s fighting %s!" % tuple(dinos)
