import re
import logging
import os
import zipfile

class ProjectGutenbergText(object):
    """Class for dealing with Project Gutenberg texts."""

    START = [re.compile("Start[^\n]*Project Gutenberg.*", re.I),
             re.compile("\*END\*THE SMALL PRINT!.*", re.I)]

    END = re.compile("End[^\n]*Project Gutenberg.*", re.I)
    LANGUAGE = re.compile("Language: ([\w -()]+)", re.I)
    ENCODING = re.compile("C.*set encoding: ([\w -]+)", re.I)

    def __init__(self, text, name=None):
        header, text, footer = self.extract_header_and_footer(text)
        if name is None:
            name = text[:20]
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

        m = self.LANGUAGE.search(header)
        if m is None:
            # Who knows?
            logging.warn("%s specifies no language, assuming English." % name)
            self.language = "English"
        else:
            self.language = m.groups()[0]

        check_encoding = self.original_encoding or 'ascii'
        self.text = None
        try:
            self.text = unicode(text, check_encoding)
        except Exception, e:
            specified_encoding_is_wrong = ( self.original_encoding is not None)
            for try_encoding in ('utf-8', 'iso-8859-1', 'latin-1'):
                try:
                    self.text = unicode(text, try_encoding)
                    if specified_encoding_is_wrong:
                        logging.warn("%s claims encoding is %s, but it's actually %s. Original error: %s" % (
                                name, self.original_encoding, try_encoding, e))
                    break
                except UnicodeDecodeError, f:
                    pass
        if self.text is None:
            log.error("Can't determine encoding for %s (specified encoding is %s)" % (
                    name, self.original_encoding))

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
        else:
            start, start2 = m.span()
        m = cls.END.search(text, start2+100)
        if m is None:
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
        deny_formats=["h", "t", "x", "m", "r", "pdf", "lit", "doc", "pub"]):
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
        year_directories = ['etext06']
        numbered_directories = list(str(x) for x in range(1,10))

        if None in allow_formats:
            for directory in year_directories:
                # Early PG texts. Bunch of texts in one directory, all
                # can be assumed to be ASCII for performance reasons.
                books_path =  os.path.join(mount_path, str(directory))
                for dirpath, dirnames, filenames in os.walk(books_path):
                    for name in filenames:
                        if name.endswith('.zip'):
                            yield os.path.join(dirpath, name)

        for directory in numbered_directories:
            # Later PG texts. Each text in one directory, potentially in several
            # formats.
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
                        yield os.path.join(dirpath, formats[format])
                        break

    @classmethod
    def texts_on_media(
        cls, mount_path,
        allow_languages=["English"],
        allow_formats=["0", "8", None,], 
        deny_formats=None):
        """Yield ProjectGutenbergText objects from a mounted Gutenberg CD or DVD.

        Yields a given text in at most one format. By default, only
        English texts are included. UTF-8 is prioritized over
        ISO-8859-1, which is prioritized over ASCII, and no other
        format is allowed.

        The best way to get Project Gutenberg ISOs is via BitTorrent:
        http://www.gutenberg.org/wiki/Gutenberg:The_CD_and_DVD_Project#Downloading_Via_BitTorrent
        """
        deny_formats = list(deny_formats or [])
        # We're not set up to handle any of these formats.
        deny_formats.extend(["h", "t", "x", "m", "r", "pdf", "lit", "doc", "pub"])
        for path in cls.files_on_media(mount_path, allow_formats, deny_formats):
            try:
                text = cls.text_from_zip(path, allow_languages)
                if text.language in allow_languages:
                    yield text
            except Exception, e:
                logging.error("%s: %s" % (path, e))

    @classmethod
    def text_from_zip(cls, path, allow_languages=["English"]):
        """Return a ProjectGutenbergText object from a zip file."""
        archive = zipfile.ZipFile(path)
        inside = archive.filelist
        filenames = [x.filename for x in inside]
        if len(inside) != 1:
            logging.warn("Supposedly plain-text %s has %d files in zip: %s" % (
                    path, len(inside), ", ".join(filenames)))
        possibilities = [x for x in filenames if x.lower().endswith(".txt")]
        data = archive.read(possibilities[0])
        return ProjectGutenbergText(data, path)

    @property
    def paragraphs(self):
        return self.text.split("\r\n\r\n")

