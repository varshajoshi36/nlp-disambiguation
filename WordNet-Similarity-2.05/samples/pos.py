#! /usr/bin/python
import nltk
from nltk.corpus import wordnet

def get_wordnet_pos(treebank_tag):
	if treebank_tag.startswith('J'):
		return 'a'
	elif treebank_tag.startswith('V'):
		return 'v'
	elif treebank_tag.startswith('N'):
		return 'n'
	elif treebank_tag.startswith('R'):
		return 'r'

text = "palm is centre of hand"
text1 = nltk.word_tokenize(text)
treebank_tag = nltk.pos_tag(text1)
final = []
words = []
tags = []
for s1 in text1:
	words.append(s1)

for s2 in treebank_tag:
	tags.append(s2[1])

for s3 in tags:
	result = get_wordnet_pos(s3)
	final.append(result)

print zip(words,final)




