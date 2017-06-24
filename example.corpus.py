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
    'corpus',
    nargs='*',
    help='Load and display the given corpus.'
)
args = parser.parse_args()

if not args.list and not args.corpus:
    parser.print_usage()
    sys.exit()

if args.list:
    for key in Corpus.keys():
        print key
else:
    for corpus in args.corpus:
        print Corpus.load(corpus)
