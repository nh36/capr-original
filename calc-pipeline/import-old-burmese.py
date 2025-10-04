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
parser = argparse.ArgumentParser(description='Add my Old Burmese to the Doug-to-Huang file.', add_help=True)
parser.add_argument('base', metavar='filename', nargs=1, help='original TSV file')
parser.add_argument('new_language', metavar='filename', nargs=1, help='OB data')

args = parser.parse_args()


fp = open(args.base[0])
csvreader = csv.DictReader(filter(lambda row: row.strip() and row[0]!='#', fp), dialect='excel-tab')

ids_taken = set([])
glossids_taken = set([])
glossid_of_concept = dict([])

eprint('Processing TSV rows...')
for row in csvreader:
    ids_taken.add(int(row['ID']))
    glossids_taken.add(int(row['GLOSSID']))
    glossid_of_concept[row['CONCEPT']] = int(row['GLOSSID'])

def new_id(id_set):
    i = 1
    while i in id_set:
        i = i + 1
    id_set.add(i)
    return i

# Load concept translator
concept_transl = {}
with open('REF-concept-correspondence') as fp:
    for line in fp:
        fields = line.split('\t')
        mattisland_concept = fields[0].strip()
        original_concept = fields[1].strip()
        concept_transl[mattisland_concept] = original_concept

# 从新的文件里面打开一行，搜索一下glossid_of_concept，分配一下大ID，然后就好了！
with open(args.new_language[0]) as fp:
    for line in fp:
        fields = line.split('\t')
        form = fields[0].strip()
        gloss = concept_transl[fields[1].strip()]

        glossid = 0
        if gloss not in glossid_of_concept:
            eprint('Created new glossID for:', gloss)
            glossid = new_id(glossids_taken)
            glossid_of_concept[gloss] = glossid
        else:
            glossid = glossid_of_concept[gloss]

        rootid = new_id(ids_taken)
        print ('{}\t{}\t{}\t{}\t{}'.format(rootid, 'Old_Burmese', gloss, glossid, form))
