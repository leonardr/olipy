import json
import os

dir = os.path.split(__file__)[0]

BLACKLIST = json.load(open(os.path.join(dir, "data", "word-lists", "badwords.json")))['badwords']

def is_blacklisted(string, blacklist=BLACKLIST):
    s = string.lower()
    for slur in blacklist:
        if slur in s:
            return True
    return False
