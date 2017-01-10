#! /usr/bin/python
import nltk
from nltk.corpus import wordnet as wn

flag = 0
import subprocess


def disamb(l1,l2):
	a = list()
	
	set1 = str(l1)
	set2 = str(l2)
	cmd = ['perl', 'disamb.pl', set1, set2]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	for line in proc.stdout:
		print line;
	
	
l = dict()
def list_format(ls1,ls2):
	
	l1 = list()
	l2 = list()
	for i in range(0,len(ls1)):
		for j in range (0,len(ls1[i])):
			l1.append((str(ls1[i][j]).replace('Synset(\'','').replace('.','#').replace('\')','').replace('#s','#a')))
	for i in range(0,len(ls2)):
		for j in range (0,len(ls2[i])):
			l2.append((str(ls2[i][j]).replace('Synset(\'','').replace('.','#').replace('\')','').replace('#s','#a')))	
	disamb(l1,l2)
	


pos_list = ['n', 'v', 'a', 'r']
det_synsets1 = dict()
det_synsets2 = dict()
i = 0
b = list()
for a in pos_list:
	det_synsets1[i] = wn.synsets("code", pos = a)
	i += 1
i = 0;
for a in pos_list:
	det_synsets2[i] = wn.synsets("architecture", pos = a)
	i += 1

list_format(det_synsets1,det_synsets2)


	
