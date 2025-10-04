#!/usr/bin/python
from foma import FST
fst_burmese = FST.load('burmese.bin')
fst_achang = FST.load('ngochang.bin')
fst_maru = FST.load('maru.bin')

burm_word = input('Enter a Burmese word: ')
achang_word = input('Enter a Achang word: ')
maru_word = input('Enter a Maru word: ')

burm_reconst = list(fst_burmese.apply_up(burm_word))
print(burm_word, 'could <', ['*' + w for w in burm_reconst])

achang_reconst = list(fst_achang.apply_up(achang_word))
print(achang_word, 'could <', ['*' + w for w in achang_reconst])

maru_reconst = list(fst_maru.apply_up(maru_word))
print(maru_word, 'could <', ['*' + w for w in maru_reconst])

reconstruction = set(burm_reconst) & set(achang_reconst) & set(maru_reconst)
print('Result:', ['*' + w for w in reconstruction])
