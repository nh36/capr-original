from foma import FST
fst_greek = FST.load('grk.bin')
fst_sanskrit = FST.load('skt.bin')

grk_word = input('Enter a "Greek" word: ')
skt_word = input('Enter a "Sanskrit" word: ')

grk_reconst = list(fst_greek.apply_up(grk_word))
print(grk_word, 'could <', ['*' + w for w in grk_reconst])

skt_reconst = list(fst_sanskrit.apply_up(skt_word))
print(skt_word, 'could <', ['*' + w for w in skt_reconst])

reconstruction = set(grk_reconst) & set(skt_reconst)
print('Result:', ['*' + w for w in reconstruction])
