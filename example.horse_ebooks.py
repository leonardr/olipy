import sys
from gutenberg import ProjectGutenbergText
from ebooks import EbooksQuotes

keywords = sys.argv[1:] or ['horse']

t = ProjectGutenbergText(open("data/44269.txt.utf-8").read(), "44269.txt.utf-8")
ebooks = EbooksQuotes(keywords)
for para in t.paragraphs:
    for quote in ebooks.quotes_in(para):
        print quote
        print
