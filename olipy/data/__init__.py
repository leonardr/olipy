import json
import os

def load_json(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    return json.load(open(path))
