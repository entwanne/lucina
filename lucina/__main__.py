#!/usr/bin/env python

import argparse
import json
import sys

from lucina import format_doc
from lucina import parse_cells
from lucina import tokenize_files
from lucina.cell import SlideType
from lucina.utils import open_files


parser = argparse.ArgumentParser()
parser.add_argument(
    'files', metavar='file', nargs='+', help='Files to compute',
)
parser.add_argument('-o', '--output', default=None)
parser.add_argument('--no-autolaunch', dest='autolaunch', action='store_false')

title_split = {1: SlideType.SLIDE, 2: SlideType.SUBSLIDE}
title_split_after = {}


def run(args):
    with open_files(args.files, 'r') as files:
        tokens = tokenize_files(files)
        cells = parse_cells(tokens, title_split, title_split_after)
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
