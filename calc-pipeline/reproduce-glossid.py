#!/usr/bin/python

# Basic imports
import sys
import re
import parsy
import csv
from functools import reduce

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Parse arguments with argparse
import argparse
parser = argparse.ArgumentParser(description='Convert Huang tsv from Dougland to TSV file.', add_help=True)
parser.add_argument('huang', metavar='filename', nargs=1, help='Dougland Huang TSV file')

args = parser.parse_args()

ids_taken = set([])
glossids_taken = set([])
glossid_of_concept = dict([])
glossid_of_row = dict([])

def new_id(id_set):
    i = 1
    while i in id_set:
        i = i + 1
    id_set.add(i)
    return i

eprint('Processing TSV rows...')

print('ID\tDOCULECT\tCONCEPT\tGLOSSID\tIPA')

doculect_translation = {
        'Burmese': 'Rangoon',
        'Achang': 'Achang',
        'Zaiwa': 'Atsi',
        'Lhaovo': 'Maru',
        'Pela': 'Bola',
        'Lashi': 'Lashi'}

with open(args.huang[0]) as fp:
    for line in fp:
        fields = line.split('\t')

        bibref = fields[0].strip()
        row = bibref.split('.')[1]

        gloss = fields[3].strip()

        formid = new_id(ids_taken)

        glossid = 0
        if gloss not in glossid_of_concept:
            eprint('Created new glossID for:', gloss)
            glossid = new_id(glossids_taken)
            glossid_of_concept[gloss] = glossid
            glossid_of_row[row] = glossid
        else:
            glossid = glossid_of_concept[gloss]

for row in sorted(glossid_of_row.keys()):
    print('%s\t%d' % (row, glossid_of_row[row]))
