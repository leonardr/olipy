# Corrupts whatever you type by adding diacritical marks.
import sys

from gibberish import Corruptor
go = True
while go:
    input = raw_input("> ")
    if input.strip() == '':
        break
    for corruption in range(10):
        print Corruptor(corruption).corrupt(input)

