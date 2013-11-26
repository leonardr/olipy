import sys
from gutenberg import ProjectGutenbergText
from ebooks import EbooksQuotes


keywords = sys.argv[1:] or ['hook']

t = ProjectGutenbergText(open("data/44269.txt.utf-8").read())
ebooks = EbooksQuotes(keywords)
for para in t.paragraphs:
    for quote in ebooks.quotes_in(para):
        print quote
