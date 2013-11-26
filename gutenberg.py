import re

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

    @property
    def paragraphs(self):
        return self.text.split("\r\n\r\n")
