import json
import os

from corpus import Corpus

BLACKLIST = Corpus.load("slurs")['badwords']

def is_blacklisted(string, blacklist=BLACKLIST):
    s = string.lower()
    for slur in blacklist:
        if slur in s:
            return True
    return False
