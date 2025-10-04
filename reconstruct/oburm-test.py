#!/usr/bin/python
import sys
import re
from foma import FST

fst_burmese = FST.load('burmese.bin')

# Parse arguments with argparse
import argparse
parser = argparse.ArgumentParser(description='Test the Old Burmese transcription', add_help=True)
parser.add_argument('files', metavar='filename', nargs='*', help='files to be concatenated and sorted')

args = parser.parse_args()

# Use fileinput to imitate standard UNIX utility behaviour
import fileinput

for line in fileinput.input(files=args.files, mode='r'):
    burm_word = line.rstrip()
    burm_reconst = list(fst_burmese.apply_up(burm_word))
    print(burm_word, 'could <', ['*' + w for w in burm_reconst])
