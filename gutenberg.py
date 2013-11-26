import re
import os

class ProjectGutenbergText(object):
    """Class for dealing with Project Gutenberg texts."""

    START = re.compile("Start[^\n]*Project Gutenberg.*", re.I)
    END = re.compile("End[^\n]*Project Gutenberg.*", re.I)

    def __init__(self, text):
        self.text = self.strip_header_and_footer(text)

    @classmethod
    def strip_header_and_footer(self, text):
        """Strip the header and footer information, leaving only the text."""
        m = self.START.search(text)
        start, start2 = m.span()
        m = self.END.search(text, start2+100)
        end, end2 = m.span()
        return text[start2:end]

    FORMAT = re.compile("_([^_]+).zip")

    @classmethod
    def files_on_media(self, mount_path,
                       allow=[None, "8", "0"], 
                       deny=["h", "t", "x", "m", "r",
                             "pdf", "lit", "doc", "pub"]):
        """Yields paths to zip files on a mounted Gutenberg CD or DVD.

        Yields a given text in at most one format.

        The best way to get Project Gutenberg ISOs is via BitTorrent:
        http://www.gutenberg.org/wiki/Gutenberg:The_CD_and_DVD_Project#Downloading_Via_BitTorrent
        """
        for num in range(1,10):
            books_path =  os.path.join(mount_path, str(num))
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
                    m = self.FORMAT.search(name)
                    if m is None:
                        format = None # ASCII text.
                    else:
                        format = m.groups()[0]
                    if format not in deny:
                        formats[format] = name
                # We now have this text in a variety of formats. Yield
                # the highest-priority one.
                for format in allow:
                    if format in formats:
                        yield os.path.join(dirpath, formats[format])
                        break

    @property
    def paragraphs(self):
        return self.text.split("\r\n\r\n")

