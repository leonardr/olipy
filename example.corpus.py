import sys
import argparse
from corpus import Corpus

parser = argparse.ArgumentParser()
parser.add_argument(
    '--list', 
    help='List all available corpora.',
    action="store_true"
)
parser.add_argument(
    '--print-all', 
    help='Load and print all available corpora.',
    action="store_true"
)
parser.add_argument(
    'corpus',
    nargs='*',
    help='Load and display the given corpus.'
)
args = parser.parse_args()

if not args.list and not args.corpus and not args.print_all:
    parser.print_usage()
    sys.exit()

if args.list:
    for key in Corpus.keys():
        print key
elif args.print_all:
    for key in Corpus.keys():
        print key
        print Corpus.load(key)
else:
    for corpus in args.corpus:
        print Corpus.load(corpus)
