# Prints a 140-character string of gibberish.
from olipy.gibberish import Gibberish
print(Gibberish.random().tweet().encode("utf8"))
