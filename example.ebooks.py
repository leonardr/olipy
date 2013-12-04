import argparse
import logging
import os
import sys
from gutenberg import ProjectGutenbergText
from ebooks import EbooksQuotes

parser = argparse.ArgumentParser(
    description="Generate pithy _ebooks quotes from Project Gutenberg texts.")
parser.add_argument(
    '--path', help="The path to a mounted Project Gutenberg CD or DVD.",
    default=None)
parser.add_argument(
    "keyword", nargs="*", help="Keywords to focus on when making selections.",
    default=["horse"])

args = parser.parse_args()
ebooks = EbooksQuotes(args.keyword)
if args.path is None:
    texts = [ProjectGutenbergText(open("data/44269.txt.utf-8").read(), "44269.txt.utf-8")]
else:
    texts = ProjectGutenbergText.texts_on_media(args.path)
for text in texts:
    total = 0
    for para in text.paragraphs:
        for quote in ebooks.quotes_in(para):
            print quote.encode("utf8")
            total += 1
    logging.warn("%d quotes found in %s" % (total, text.name))
