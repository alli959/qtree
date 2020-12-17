import nltk
from nltk.corpus import treebank
nltk.download('treebank')
t = treebank.parsed_sents('wsj_0001.mrg')[1]
print(t)
t.draw()