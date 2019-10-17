#!/usr/bin/env python

import argparse
import json
import sys

from lucina.generate import generate_cells


parser = argparse.ArgumentParser()
parser.add_argument('files', metavar='file', nargs='+', help='Files to compute')
parser.add_argument('-o', '--output', default=None)
parser.add_argument('--no-autolaunch', dest='autolaunch', action='store_false')

title_split = {1: 'slide', 2: 'subslide'}
title_split_after = {}


def main():
    args = parser.parse_args()

    doc = {
        'cells': generate_cells(args.files, title_split, title_split_after),
        'metadata': {
            'celltoolbar': 'Slideshow',
            'kernelspec': {
                'display_name': 'Python 3',
                'language': 'python',
                'name': 'python3'
            },
            'language_info': {
                'codemirror_mode': {
                    'name': 'ipython',
                    'version': 3
                },
                'file_extension': '.py',
                'mimetype': 'text/x-python',
                'name': 'python',
                'nbconvert_exporter': 'python',
                'pygments_lexer': 'ipython3',
                'version': '3.6.5'
            },
            "livereveal": {
                "autolaunch": args.autolaunch,
            }
        },
        'nbformat': 4,
        'nbformat_minor': 2,
    }

    if args.output:
        f = open(args.output, 'w')
    else:
        f = sys.stdout

    with f:
        json.dump(doc, f, indent=4)


if __name__ == '__main__':
    main()
