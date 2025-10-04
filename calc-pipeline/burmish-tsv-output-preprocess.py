"""
git pull https://github.com/lingpy/lexibase.git
git pull https://github.com/lingpy/lingpy.git
git pull https://github.com/lingpy/lingrex.git

python setup.py develop
"""
from lingpy import *
from collections import defaultdict
from tabulate import tabulate
from burmtools import *
from merge_phonemes import merge_phonemes
from copy import copy

# Settings
languages_to_remove = ["Proto-Burmish", "Lashi"]

def merge_phonemes_burmish(old_schema, old_tokens, debug=None):
    try:
        out = [merge_phonemes(str(sch), str(tk), 'i m r t', {'i': 'im', 'm':'m', 'r':'mnc', 't':'t'}) for sch, tk in zip(basictypes.lists(old_schema).n, basictypes.lists(old_tokens).n)]
        return (' + '.join([i for i,j in out]), ' + '.join([j for i,j in out]))
    except:
        print(debug)
        return ('','')

wl = Wordlist('burmish-stage2-2-aligned.tsv')
wl.add_entries('tmp_structure', 'structure,tokens', lambda x, y: merge_phonemes_burmish(x[y[0]], ' '.join(x[y[1]]), x)[0])
wl.add_entries('tmp_tokens', 'structure,tokens', lambda x, y: merge_phonemes_burmish(x[y[0]], ' '.join(x[y[1]]), x)[1])

columns = copy(wl.columns)
# columns.remove('patterns')
columns.remove('structure')
columns.remove('tokens')
wl.output('tsv', filename='burmish-tmp', subset=True, rows={"doculect": "not in " + str(languages_to_remove)}, cols=columns)
