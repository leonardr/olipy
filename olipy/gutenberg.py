import json
import re
import logging
import os
import zipfile
import random
NS = dict()
try:
    import rdflib
    from rdflib.namespace import Namespace
    NS['dcterms'] = Namespace("http://purl.org/dc/terms/")
    NS['dcam'] = Namespace("http://purl.org/dc/dcam/")
    NS['rdf'] = Namespace(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    NS['gutenberg'] = Namespace("http://www.gutenberg.org/2009/pgterms/")
except ImportError as e:
    rdflib = None

class ProjectGutenbergText(object):
    """Class for dealing with Project Gutenberg texts."""

    ids_for_old_filenames = None

    ETEXT_ID = re.compile("^([0-9]+)")
    START = [re.compile("Start[^\n]*Project Gutenberg.*", re.I),
             re.compile("END.THE SMALL PRINT!.*", re.I),
             re.compile("SMALL PRINT!.*\*END\*", re.I),
             re.compile('\["Small Print" V.*', re.I),
             ]

    END = [re.compile("End[^\n]*Project Gutenberg.*", re.I),
           re.compile("of the Project Gutenberg", re.I),
           re.compile("End of this Etext", re.I),
           re.compile("End of\W+Project Gutenberg", re.M),
           re.compile("Ende dieses Projekt Gutenberg Etextes", re.I),
           re.compile("^The Project Gutenberg Etext", re.I),
           re.compile("The Project Gutenberg Etext", re.I),
           ]
    LANGUAGE = re.compile("Language: ([\w -()]+)", re.I)
    ENCODING = re.compile("C.*set encoding: ([\w -]+)", re.I)

    def __init__(self, text, name=None, rdf_catalog_path=None):
        header, text, footer = self.extract_header_and_footer(text)
        self.rdf_catalog_path= rdf_catalog_path
        self._graph = None
        if name is None:
            name = text[:20]   
            self.etext_id = None
        else:
            self.etext_id = self.etext_id_from_filename(name)
        self.name = name

        m = self.ENCODING.search(header)
        if m is None:
            if name.endswith(".utf-8"):
                self.original_encoding = 'utf-8'
            else:
                # Who knows?
                logging.warn("%s specifies no encoding, assuming ASCII." % name)
                self.original_encoding = None
        else:
            enc = m.groups()[0].strip()
            if enc == 'ISO Latin-1':
                enc = 'iso-8859-1'
            elif enc == 'ISO-646-US':
                enc = 'ascii'
            elif enc in 'Unicode UTF-8':
                enc = 'UTF-8'
            elif enc == 'CP-1251':
                enc = 'windows-1251'
            elif enc == 'CP-1252':
                enc = 'windows-1252'

            self.original_encoding = enc

        # Figure out which language(s) the text is in.
        if self.graph is not None:
            # The most reliable source is an RDF graph. If we have one, use it.
            self.languages = set(
                [unicode(x[2]) for x in self.graph.triples((None, NS['dcterms'].language, None))])
        else:
            # Look for a "Language: Foo" bit of text in the header.
            m = self.LANGUAGE.search(header)
            if m is None:
                logging.warn("%s specifies no language." % name)
                self.languages = set([])
            else:
                self.languages = set([m.groups()[0]])

        check_encoding = self.original_encoding or 'ascii'
        self.text = None
        try:
            self.text = unicode(text, check_encoding)
        except Exception as e:
            specified_encoding_is_wrong = ( self.original_encoding is not None)
            for try_encoding in ('utf-8', 'iso-8859-1', 'latin-1'):
                try:
                    if isinstance(text, bytes):
                        self.text = unicode(text, try_encoding)
                    else:
                        self.text = text
                    if specified_encoding_is_wrong:
                        logging.warn("%s claims encoding is %s, but it's actually %s. Original error: %s" % (
                                name, self.original_encoding, try_encoding, e))
                    break
                except UnicodeDecodeError as f:
                    pass
        if self.text is None:
            log.error("Can't determine encoding for %s (specified encoding is %s)" % (
                    name, self.original_encoding))

    def etext_uri(self):
        return "http://www.gutenberg.org/ebooks/%s" % self.etext_id

    @property
    def graph(self):
        if rdflib is None or self.rdf_catalog_path is None:
            return None
        if self._graph is None:
            self._graph = rdflib.Graph()
            self._graph.load(open(self.rdf_path))
        return self._graph

    @property
    def rdf_path(self):
        return os.path.join(
            self.rdf_catalog_path, "cache", "epub",
            str(self.etext_id), "pg%s.rdf" % self.etext_id)

    def etext_id_from_filename(self, path):
        if self.ids_for_old_filenames is None:
            # Load the mapping from JSON.
            this_dir = os.path.split(__file__)[0]
            mapping_file = os.path.join(
                this_dir, 'data', 'ids_for_old_project_gutenberg_filenames.json')
            self.ids_for_old_filenames = json.load(open(mapping_file))

        path_part, filename = os.path.split(path)
        ignore, directory_part = os.path.split(path_part)
        if "etext" in directory_part:
            unique_filename = os.path.join(directory_part, filename)
            return self.ids_for_old_filenames[unique_filename]
        else:
            return int(self.ETEXT_ID.search(filename).groups()[0])

    @classmethod
    def extract_header_and_footer(cls, text):
        """Split a PG document into (header, text, footer) tuple."""
        for s in cls.START:
            m = s.search(text)
            if m is not None:
                break
        if m is None:
            # Make a wild guess.
            start, start2 = 0, 1000
            # import pdb; pdb.set_trace()
        else:
            start, start2 = m.span()
        for s in cls.END:
            m = s.search(text, start2+100)
            if m is not None:
                break
        if m is None:
            # import pdb; pdb.set_trace()
            end =len(text)
            end2 = end
        else:
            end, end2 = m.span()
        return text[:start2], text[start2:end], text[end:]

    FORMAT = re.compile("_([^_]+).zip")

    @classmethod
    def files_on_media(
        cls, mount_path,
        allow_formats=["0", "8", None,], 
        deny_formats=["h", "t", "x", "m", "r", "pdf", "lit", "doc", "pub"],
        start_at=None):
        """Yields paths to zip files on a mounted Gutenberg CD or DVD.

        Yields a given text in at most one format. By default, UTF-8
        is prioritized over ISO-8859-1, which is prioritized over
        ASCII, and no other format is allowed.

        The best way to get Project Gutenberg ISOs is via BitTorrent:
        http://www.gutenberg.org/wiki/Gutenberg:The_CD_and_DVD_Project#Downloading_Via_BitTorrent
        """

        year_directories = ['etext' + x for x in (
                '90',' 91', '92', '93', '94', '95', '96', '97', '98', '99',
                '00', '01', '02', '03', '04', '05', '06')]
        numbered_directories = list(str(x) for x in range(1,10))

        started = (start_at is None)
        # if None in allow_formats:
        #     for directory in year_directories:
        #         # Early PG texts. One directory per year, one format per text.
        #         books_path =  os.path.join(mount_path, str(directory))
        #         for dirpath, dirnames, filenames in os.walk(books_path):
        #             for name in filenames:
        #                 if name.endswith('.zip'):
        #                     if not started and name.startswith(start_at):
        #                         started = True
        #                     if (started and not name.endswith('h.zip')
        #                         and not name.endswith('l.zip')):
        #                         yield os.path.join(dirpath, name)

        for directory in numbered_directories:
            # Later PG texts. One directory per text, each text
            # potentially in several formats.
            books_path =  os.path.join(mount_path, str(directory))
            for dirpath, dirnames, filenames in os.walk(books_path):
                # Does this directory contain a text?
                contains_text = False
                for name in filenames:
                    if name.endswith('.zip'):
                        contains_text = True

                if not contains_text:
                    continue

                formats = {}
                for name in filenames:
                    if not name.endswith('.zip'):
                        continue
                    m = cls.FORMAT.search(name)
                    if m is None:
                        format = None # ASCII text.
                    else:
                        format = m.groups()[0]
                    if format not in deny_formats:
                        formats[format] = name
                # We now have this text in a variety of formats. Yield
                # the highest-priority one.
                for format in allow_formats:
                    if format in formats:
                        if not started and name.startswith(start_at):
                            started = True
                        if started:
                            yield os.path.join(dirpath, formats[format])
                        break

    @classmethod
    def texts_on_media(
        cls, mount_path,
        rdf_catalog_path=None,
        allow_languages=["en", "English"],
        allow_formats=["0", "8", None,], 
        deny_formats=None,
        start_at=None):
        """Yield ProjectGutenbergText objects from a mounted Gutenberg CD or DVD.

        Yields a given text in at most one format. By default, only
        English texts are included. UTF-8 is prioritized over
        ISO-8859-1, which is prioritized over ASCII, and no other
        format is allowed.

        The best way to get Project Gutenberg ISOs is via BitTorrent:
        http://www.gutenberg.org/wiki/Gutenberg:The_CD_and_DVD_Project#Downloading_Via_BitTorrent
        """
        allow_languages = set(allow_languages)
        deny_formats = list(deny_formats or [])
        # We're not set up to handle any of these formats.
        deny_formats.extend(["h", "t", "x", "m", "r", "pdf", "lit", "doc", "pub"])
        for path in cls.files_on_media(mount_path, allow_formats, deny_formats, start_at):
            try:
                text = cls.text_from_zip(path, rdf_catalog_path)
                if not allow_languages or len(text.languages.intersection(allow_languages)) > 0:
                    yield text
            except Exception as e:
                logging.error("%s: %s" % (path, e))
                # raise e

    @classmethod
    def text_from_zip(cls, path, rdf_catalog_path=None):
        """Return a ProjectGutenbergText object from a zip file."""
        archive = zipfile.ZipFile(path)
        inside = archive.filelist
        filenames = [x.filename for x in inside]
        if len(inside) != 1:
            logging.warn("Supposedly plain-text %s has %d files in zip: %s" % (
                    path, len(inside), ", ".join(filenames)))
        possibilities = [x for x in filenames if x.lower().endswith(".txt")]
        data = archive.read(possibilities[0])
        return ProjectGutenbergText(data, path, rdf_catalog_path)

    @property
    def paragraphs(self):
        return self.text.split("\r\n\r\n")

