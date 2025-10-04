#!/usr/bin/python
"""
git pull https://github.com/lingpy/lexibase.git
git pull https://github.com/lingpy/lingpy.git
git pull https://github.com/lingpy/lingrex.git

python setup.py develop
"""
from lingrex.copar import *
from lingrex.util import align_by_structure
from lingpy import *
from lexibase.lexibase import *
from collections import defaultdict
from tabulate import tabulate
from burmtools import *
from merge_phonemes import merge_phonemes
from copy import copy

# languages = cop.cols
languages = ['Old_Burmese', 'Achang_Longchuan', 'Maru', 'Bola']
languages_title = ['OBurm', 'Acha-LC', 'Maru', 'Bola']
#languages = ['Old_Burmese', 'Achang_Longchuan', 'Maru']
#languages_title = ['OBurm', 'Acha-LC', 'Maru']
number_of_languages = len(languages)

# Replace unicode diacritics with ASCII equivalents for sending to the transducers
UNICODE_MACRON_UNDER = " ̱ "[1]
UNICODE_TILDE_OVER = " ̃"[1]
def replace_diacritics(s):
    return s.replace(UNICODE_MACRON_UNDER, '_').replace(UNICODE_TILDE_OVER, '~').replace('_~', '~_')


# fetch_syllable("mi ma mu", 1) → "ma"
def fetch_syllable(text, syllable_index):
    syllables = syllabize(text)
    return syllables[syllable_index]

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
columns.remove('alignment')
columns.remove('structure')
columns.remove('tokens')
wl.output('tsv', filename='burmish-stage2-tmp-merged', subset=True, rows={"doculect": " in " + str(languages)}, cols=columns)

cop = CoPaR('burmish-stage2-tmp-merged.tsv', ref='crossids', segments='tmp_tokens', fuzzy=True,
        structure='tmp_structure')

cop.get_sites()
cop.cluster_sites()
cop.sites_to_pattern()
cop.add_patterns()
#cop.load_patterns()

# dirty output in markdown
# get index for proto-burmish
bidx = cop.cols.index('Old_Burmese')

# sort the pattern output by Burmish rec
# get the patterns firstt into sorter
pburm = defaultdict(list)
for pattern, sites in cop.clusters.items():
    pburm[pattern[1][bidx]] += [(pattern, sites)]

latex_header = r"""\documentclass[11pt,a4paper]{memoir}

\usepackage{graphicx}
\usepackage{pgfkeys}
\usepackage{etoolbox}
\usepackage{pdfpages}
\usepackage{refcount}
\usepackage{xunicode}
\usepackage{titletoc}
\usepackage{amssymb}
\usepackage{amsmath}
\usepackage{xspace}
\usepackage{fontspec}
\usepackage{longtable}
\usepackage{tabu}
\usepackage{xunicode}
\usepackage{tikz}
\usepackage{forest}
\usepackage{pifont}
\usepackage{colortbl}
\usepackage{soul}
\usepackage{multirow}
\usepackage{multicol}
\usepackage{wrapfig}
\usepackage{endnotes}
\usepackage{relsize}
\usepackage{rotating}
\usepackage[round,authoryear]{natbib}
\usepackage{gb4e}

\usetikzlibrary{tikzmark}

\XeTeXlinebreaklocale ``zh''

% Page settings
%\settypeblocksize{160mm}{110mm}{*} % A5
\settypeblocksize{213mm}{180mm}{*}
\setlrmargins{*}{*}{1}
\setulmargins{*}{*}{1}
\checkandfixthelayout

% Font setup
\setmainfont[Mapping=tex-text]{Brill}
\setsansfont[Mapping=tex-text, Scale=0.87]{DejaVu Sans}
\setmonofont[Scale=0.773]{DejaVu Sans Mono}

\newcommand{\zh}[1]{{\fontspec[BoldFont=SimHei, ItalicFont=Adobe Kaiti
Std, Scale=0.84]{NSimSun}#1}}
\newcommand{\wenyan}[1]{{\fontspec{WenyueType GutiFangsong (Noncommercial Use)}#1}}
\newcommand{\superwen}[1]{{\fontspec[Scale=1.08]{舊活字明 Beta}#1}}


\newcommand{\dia}[1]{{\protect\fontspec[Scale=0.91,FakeSlant=0.15,Mapping=tex-text]{Charis SIL}\textup{#1}}}
\newcommand{\diabold}[1]{{\textbf{\protect\fontspec[Scale=0.91,FakeSlant=0.15,Mapping=tex-text]{Charis SIL}\textup{#1}}}}
\newcommand{\diasmall}[1]{{\protect\fontspec[Scale=0.7,Mapping=tex-text]{Charis SIL}\textup{#1}}}


% external png as character
\newcommand{\png}[1]{\includegraphics[width=1.15em]{images/#1.png}}


% Memoir settings
\midsloppy
\tightlists
\nopartblankpage
\openany

% Style
\headstyles{bringhurst}
\setsecheadstyle{\normalfont\large\memRTLraggedright\textit}%
\chapterstyle{dash}
\setlength\beforechapskip{-\baselineskip}
\nouppercaseheads % Pour pas que latex bogue

\makepagestyle{mystyle}
\makeevenhead{mystyle}{\thepage}{}{}
\makeoddhead{mystyle}{}{}{\itshape\leftmark}
\makeevenfoot{mystyle}{}{}{}
\makeoddfoot{mystyle}{}{}{}
\makepsmarks{mystyle}{%
  \createmark{chapter}{left}{nonumber}{}{}}

\pagestyle{mystyle}

% Todos
\definecolor{Doubtful}{rgb}{0,0.4,0.2}
\definecolor{lightyellow}{rgb}{1,1,0.9}
\newcommand{\todo}[1]{\textsf{\colorbox{lightyellow}{\textbf{*}#1\textbf{*}}}}
\newcommand{\TODO}[1]{\marginpar{\textsf{\colorbox{lightyellow}{\textbf{*}}
{\footnotesize #1}}}}
\newcommand{\douteux}[1]{\tss{??}\textsf{\color{Doubtful}{#1}}}
\sethlcolor{lightyellow}
\newcommand{\OUT}[1]{\hl{$\star$ \protect\fontspec[Scale=0.70]{Droid Sans Fallback} #1}}

\begin{document}
"""

latex_footer = """
\end{document}
"""

text = ''
latex = latex_header


from foma import FST
fst_burmese = FST.load('../reconstruct/burmese.bin')
fst_achang = FST.load('../reconstruct/ngochang.bin')
fst_maru = FST.load('../reconstruct/maru.bin')
fsts = {'Old_Burmese': fst_burmese, 'Achang_Longchuan': fst_achang, 'Maru': fst_maru}

# Index from index in languages to index in cop.cols
languages_index = [cop.cols.index(l_name) for l_name in languages]

def convert_list_from_copcols_to_languages(l):
    return [l[languages_index[i]] for i in range(len(languages))]

for i, (sound, patterns) in enumerate(sorted(pburm.items())):
    text += '=== {1}: Old Burmese <<{0}>> ===\n'.format(sound, i+1)
    latex += r"\chapter{Old Burmese ``\textbf{\dia{%s}}''}" % (sound) + '\n'

    # in order to have some kind of conspectus table, you need to collect them in tables before doing the actual output
    latex_patterns = []
    
    counter = 1
    for pattern, sites in patterns:
        conspectus_item = dict() # for LaTeX displaying

        pattern = pattern[1]
        try:
            displaypattern = convert_list_from_copcols_to_languages(list(pattern))
        except:
            raise ValueError(str(list(pattern)))
        
        text += '== Pattern {1}: {0} ==\n'.format(':'.join(displaypattern), str(counter))
        conspectus_item['id'] = counter
        conspectus_item['pattern'] = displaypattern

        counter += 1

        table = [[''] + displaypattern]
        latex_table = []

        examples = 0

        # iterate over sites
        for site in sites:
            examples += 1
            crossid = site[0]
            if crossid in cop.msa['crossids']:
                # site[0] is crossid
                msa = cop.msa['crossids'][crossid]
                # make a taxon dictionary
                tmp = {t: i for i, t in enumerate(msa['taxa'])}
                evidence = [msa['seq_id']]
                latex_row = [msa['seq_id'].replace('("', "(``").replace('")', "'')")]
                latex_row_reconstr = ['']

                for t in languages:
                    if t in tmp:
                        # look for the syllalle id from the crossid
                        crossids = cop[msa['ID'][tmp[t]], 'crossids']
                        ipa = cop[msa['ID'][tmp[t]], 'ipa']
                        location = crossids.index(crossid)
                        evidence += [emphasize_syllable(ipa, location)]
                        latex_row += [emphasize_syllable(ipa, location, r'%s\hspace{0pt}', r"\textbf{%s}\hspace{0pt}")]

                        the_syl = replace_diacritics(fetch_syllable(ipa, location))
                        if t in fsts:
                            reconst = list(fsts[t].apply_up(the_syl))
                            reconst = ['*' + w for w in reconst]
                            reconst_join = r'{\small ' + ', '.join(reconst) + r'}'
                        else:
                            reconst_join = ''
                        latex_row_reconstr += [reconst_join]
                    else:
                        evidence += ['Ø']
                        latex_row += [r'$\varnothing$']
                        latex_row_reconstr += ['']
                table += [evidence]
                latex_table += [latex_row, latex_row_reconstr]
            else:
                print('!!! Something bad happened with site', site[0])
                print([site[0] for x in languages])
                # table += [[site[0] for x in languages]]

        text += tabulate(table, headers=['ID'] + languages_title, tablefmt='github')
        text += "\n\n"
        conspectus_item['table'] = latex_table
        conspectus_item['count'] = examples
        latex_patterns += [conspectus_item]

    # output the actual latex tables
    # first: the conspectus
    latex += r'\begin{center}' + '\n'
    latex += r'\begin{tabular}{l%sl}' % ('c' * number_of_languages)
    latex += '\n'
    latex += r'\hline' + '\n'
    latex += ' & ' + ' & '.join(languages_title) + r' \\' + '\n'
    latex += r'\hline' + '\n'
    for conspectus_item in latex_patterns:
        row = r'\#' + str(conspectus_item['id']) + ' & '
        row += ' & '.join([r'\textbf{%s}' % s for s in conspectus_item['pattern']])
        row += ' & '
        row += '(%d ex%s.)' % (conspectus_item['count'], 'x' if conspectus_item['count'] > 1 else '')
        row += r' \\'
        latex += row + '\n'
    latex += r'\hline' + '\n'
    latex += r'\end{tabular}' + '\n'
    latex += r'\end{center}' + '\n'

    # second: the actual tables
    for conspectus_item in latex_patterns:
        latex += r'\section{\textbf{\dia{%s}}}' % (':'.join(conspectus_item['pattern']))
        latex += '\n'
        latex += r'\begin{longtabu} to \textwidth {X[1.75,l]%s}'  % ('X[1,c]' * number_of_languages)
        latex += '\n'
        latex += r'\hline' + '\n'
        latex += ' & ' + ' & '.join(languages_title) + r' \\' + '\n'
        latex += r'\hline' + '\n'
        latex += r'\endhead' + '\n'
        latex += r'\hline' + '\n'
        latex += r'\endfoot' + '\n'
        for row in conspectus_item['table']:
            latex += ' & '.join(row)
            latex += r' \\' + '\n'
        latex += r'\end{longtabu}' + '\n'

with open('burmish-patterns.txt', 'w') as f:
    f.write(text)

with open('burmish-patterns.tex', 'w') as f:
    f.write(latex + latex_footer)
