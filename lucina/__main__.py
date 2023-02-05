#!/usr/bin/env python

import argparse
import json
import sys

from minimd.tokenizer import Token
from minimd.tokenizer import tokenize_files
from minimd.utils import open_files

from lucina import format_doc
from lucina import parse_cells
from lucina.cell import SlideType


parser = argparse.ArgumentParser()
parser.add_argument(
    'files', metavar='file', nargs='+', help='Files to compute',
)
parser.add_argument('-o', '--output', default=None)
parser.add_argument('--no-autolaunch', dest='autolaunch', action='store_false')

split_rules = {
    SlideType.SLIDE: [Token.TITLE(level=1)],
    SlideType.SUBSLIDE: [Token.TITLE(level=2)],
    SlideType.CONTINUE: [Token.START_CODE(), Token.END_CODE()],
    SlideType.FRAGMENT: [Token.SPLIT()],
    SlideType.SKIP: [Token.START_CODE(skip=True)],
}


def run(args):
    with open_files(args.files, 'r') as files:
        tokens = tokenize_files(files)
        cells = parse_cells(tokens, split_rules)
        doc = format_doc(cells, args.autolaunch)

    if args.output:
        f = open(args.output, 'w')
    else:
        f = sys.stdout

    with f:
        json.dump(doc, f, indent=4)


def main():
    run(parser.parse_args())


if __name__ == '__main__':
    main()
