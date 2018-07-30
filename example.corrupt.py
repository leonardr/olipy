# Corrupts whatever you type by adding diacritical marks.
import sys

if sys.version_info.major == 3:
    i = input
else:
    i = raw_input

from olipy.gibberish import Corruptor
go = True
while go:
    data = i("> ")
    if data.strip() == '':
        break
    for corruption in range(10):
        print(Corruptor(corruption).corrupt(data))

