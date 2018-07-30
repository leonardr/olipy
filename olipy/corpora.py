"""A port of Allison Parrish's pycorpora module.

This was necessary to a) add extra stuff like word lists using the
same mechanism defined by pycorpora and b) include an actual copy of
the Corpora Project with a packaged Python module.
"""
import os
import sys
import json

cache = dict()
loaders = []

this_dir = os.path.split(__file__)[0]
data_path = os.path.join(this_dir, "data")
components = [
    (data_path, "corpora-original", "data"),
    (data_path, "corpora-olipy")
]
data_directories = [os.path.join(*x) for x in components]

def _read(path):
    if not path in cache:
        if not os.path.exists(path):
            return
        data = json.load(open(path))
        cache[path] = data
    return cache[path]

def fetch_resource(name, *directories):
    directories = directories or data_directories
    result = None
    for directory in reversed(directories):
        path = os.path.join(directory, name)
        result = _read(path)
        if not result:
            continue
    return result

def get_categories(name=None, *directories):
    categories = []
    directories = directories or data_directories
    for directory in directories:
        if name:
            directory = os.path.join(directory, name)
        if not os.path.isdir(directory):
            continue
        for x in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, x)):
                categories.append(x)
        return categories

def get_files(name=None, *directories):
    files = []
    directories = directories or data_directories
    for directory in directories:
        if name:
            directory = os.path.join(directory, name)
        if not os.path.isdir(directory):
            continue
        for x in os.listdir(directory):
            path = os.path.join(directory, x)
            if (not os.path.isdir(path) and path.endswith(".json")):
                files.append(x[:-5])
    return files

def get_file(*components):
    return fetch_resource(os.path.join(*components) + ".json")

def load(name):
    """Find the first corpus with the given name and load it from disk."""
    for loader in loaders:
        value = loader.search(name)
        if value:
            return value

def names():
    """Generate a list of all corpus names."""
    for loader in loaders:
        for name in loader.names:
            yield name

class CorpusLoader(object):
    def __init__(self, *directories):
        self.directories = list(directories)

    def __getitem__(self, key):
        return self.__getattr__(key)

    @property
    def children(self):
        by_filename = {}
        for directory in self.directories:
            for filename in sorted(os.listdir(directory)):
                path = os.path.join(directory, filename)
                if not os.path.isdir(path):
                    continue
                loader = by_filename.get(filename)
                if not loader:
                    loader = CorpusLoader()
                    by_filename[filename] = loader
                loader.directories.append(path)

        return by_filename.values()

    @property
    def names(self):
        for directory in self.directories:
            for filename in sorted(os.listdir(directory)):
                path = os.path.join(directory, filename)
                if os.path.isdir(path):
                    continue
                if not path.endswith(".json"):
                    continue
                yield filename[:-5]

    def search(self, name):
        for filename in self.names:
            if name == filename:
                return self.__getattr__(name)
        for loader in self.children:
            value = loader.search(name)
            if value:
                return value

    def __getattr__(self, attr):
        """If `attr` designates a file, load it as JSON and return it."""
        loader = None
        for directory in self.directories:
            file_loc =os.path.join(directory, attr + '.json')
            dir_loc = os.path.join(directory, attr)
            if os.path.exists(file_loc):
                return _read(file_loc)
            elif os.path.isdir(dir_loc):
                if not loader:
                    loader = CorpusLoader()
                loader.directories.append(dir_loc)
        if loader:
            return loader
        raise AttributeError("no resource named " + attr)

    def get_categories(self):
        return get_categories(None, *self.directories)

    def get_files(self):
        return get_files(None, *self.directories)

    def get_file(self, *components):
        path = os.path.join(*components)
        return _read(path)

# Load the standard corpora data from corpora-original/data and the
# olipy extensions from corpora-more.
module = sys.modules[__name__]
for subdir in data_directories:
    for resource_type in sorted(os.listdir(subdir)):
        directory = os.path.join(subdir, resource_type)
        if not os.path.isdir(directory):
            continue
        var = resource_type.replace("-", "_")
        loader = getattr(module, var, None)
        if not loader:
            loader = CorpusLoader()
            loaders.append(loader)
            setattr(module, var, loader)
        loader.directories.append(directory)
