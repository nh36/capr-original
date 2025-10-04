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
        doculect = doculect_translation[fields[2].strip()]
        if doculect == 'Achang':
            # two core Achang dialects in Huang, need to distinguish
            if ':c29' in bibref:
                doculect = 'Xiandao'
            elif ':c28' in bibref:
                doculect = 'Achang_Longchuan'
            else:
                eprint('ERROR: Unrecognized Ngochang variant')
                quit()
            
        form = fields[6].strip()

        gloss = fields[3].strip()

        formid = new_id(ids_taken)

        glossid = 0
        if gloss not in glossid_of_concept:
            eprint('Created new glossID for:', gloss)
            glossid = new_id(glossids_taken)
            glossid_of_concept[gloss] = glossid
        else:
            glossid = glossid_of_concept[gloss]

        print('{}\t{}\t{}\t{}\t{}'.format(formid, doculect, gloss, glossid, form))
