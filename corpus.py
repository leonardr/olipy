import json
import os

class Corpus(object):
    """Load a corpus of data from Darius Kazemi's corpora project or
    from the more-corpora directory included with olipy.
    """
    base_path = os.path.split(__file__)[0]

    extensions = '.txt', '.json'

    @classmethod
    def load(cls, target):
        """Load a corpus by name.

        Does its best to just return the data.
        """
        for full_key, key, path in cls._paths():
            if key == target or full_key == target:
                return cls._load_corpus(path)
        raise ValueError("No such corpus: %s" % target)
            
    @classmethod
    def keys(cls):
        """Return the names of all available corpora."""
        for full_key, key, filename in cls._paths():
            yield full_key

    @classmethod
    def _paths(cls):
        for corpora_dir in ('more-corpora', 'corpora/data'):
            full_path = os.path.join(cls.base_path, corpora_dir)
            for (dirpath, dirnames, filenames) in os.walk(full_path):
                thisdir = os.path.split(dirpath)[-1]
                if thisdir == corpora_dir:
                    thisdir = ''
                for filename in filenames:
                    for extension in cls.extensions:
                        if filename.endswith(extension):
                            key = filename[:filename.rindex(extension)]
                            if thisdir:
                                full_key = os.path.join(thisdir, key)
                            else:
                                full_key = key
                            path = os.path.join(dirpath, filename)
                            yield full_key, key, path
                            break
                    else:
                        # A random junk file that shouldn't be there.
                        continue
        
    @classmethod
    def _load_corpus(cls, filename):
        if filename.endswith(".json"):
            # Assume a corpora-style JSON format.
            data = json.load(open(filename))
            if not isinstance(data, dict):
                # Probably an unadorned list. Just return it.
                return data
            keys = data.keys()
            if len(keys) == 2 and 'description' in keys:
                # The corpora files are like this. We want the actual
                # data, not the enclosing object that includes the
                # description.
                [remaining_key] = [x for x in keys if x != 'description']
                return data[remaining_key]
            else:
                # We don't know what to do. Return the whole thing.
                return data

        # It's not JSON, so assume it's a text file.
        return [x.strip() for x in open(filename)]

def load(*args, **kwargs):
    return Corpus.load(*args, **kwargs)
