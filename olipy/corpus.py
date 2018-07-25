import json
import os

class Corpus(object):
    """Load a corpus of data from Darius Kazemi's corpora project or
    from the corpora-more directory included with olipy.
    """
    base_path = os.path.split(__file__)[0]
    corpora_dirs = ['data/corpora-more', 'data/corpora-original']
    
    extensions = ['.txt', '.json', '.ndjson']

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
        for corpora_dir in cls.corpora_dirs:
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
        if filename.endswith(".ndjson"):
            # Assume one JSON object per line.
            return [json.loads(i.strip()) for i in open(filename)]
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


class CorpusLoader(object):
    def __init__(self, directories=None):
        """Constructor.

        :param directories: A list of directories to use when looking for
        data. If this is not provided, olipy will use its built-in data, which includes
        a copy of the original corpora project.
        """
        olipy_root = os.path.split(__file__)[0]
        data_root = os.path.join(olipy_root, 'data')
        def data_path(x):
            return os.path.join(data_root, x)
        directory = directory or data_path('corpora-original')

        # Whether we're using the built-in corpora or a custom one,
        # the data is located in the 'data' subdirectory
        directory = os.path.join(directory, 'data')
        self.path = [directory, data_path('corpora-more')]

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __getattr__(self, attr):
        for d in self.path:
            path = os.path.join(d, attr)
            corpus = self.load(path)
            if corpus:
                return corpus
        raise AttributeError("no resource named " + attr)

    def load(self, path):
        """Try to load a file 

        :return: A CorpusLoader if `path` is a directory; otherwise
        """
        if not os.path.exists(path):
            return None
        if os.path.isdir(path):
            return CorpusLoader(
        
        
        file_loc = "data/" + self.directory + "/" + attr + ".json"
        dir_loc = "data/" + self.directory + "/" + attr
        if resource_exists(__name__, file_loc):
            return fetch_resource(file_loc)
        elif resource_exists(__name__, dir_loc) and \
                resource_isdir(__name__, dir_loc):
            return CorpusLoader(self.directory + "/" + attr)
        else:
            

    def get_categories(self):
        return get_categories(self.directory)

    def get_files(self):
        return get_files(self.directory)

    def get_file(self, *components):
        return get_file(self.directory, *components)
