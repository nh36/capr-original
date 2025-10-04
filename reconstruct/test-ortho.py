#!/usr/bin/python
import sys
import re
from foma import FST

UNICODE_MACRON_UNDER = " ̱ "[1]
def replace_diacritics(s):
    return s.replace(UNICODE_MACRON_UNDER, '_')

# Parse arguments with argparse
import argparse
parser = argparse.ArgumentParser(description='Test the Old Burmese transcription', add_help=True)
parser.add_argument('language', choices=['achang', 'burm', 'maru'], help='type to compile into')
parser.add_argument('files', metavar='filename', nargs='*', help='files to be concatenated and sorted')

args = parser.parse_args()

language = {'achang':'ngochang', 'burm':'burmese', 'maru': 'maru'}[args.language]

fst_burmese = FST.load(language + '-ortho.bin')

# Use fileinput to imitate standard UNIX utility behaviour
import fileinput

for line in fileinput.input(files=args.files, mode='r'):
    burm_word = replace_diacritics(line.rstrip())
    burm_reconst = list(fst_burmese.apply_down(burm_word))
    if not burm_reconst:
        print(burm_word)
