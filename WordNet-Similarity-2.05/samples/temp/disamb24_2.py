#! /usr/bin/python
import nltk
from nltk.corpus import wordnet as wn

flag = 0
import subprocess



#this function goes to perl and gives max similarity for two inputs
def disamb(l1,l2):
	a = list()
	print l1
	set1 = str(l1)
	set2 = str(l2)
	cmd = ['perl', 'disamb_24_2.pl', set1, set2]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	for line in proc.stdout:
		print line;
	
#following code formats the list which makes it acceptable for perl computations 	
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
	

#write all the functions above , all inpus should be taken here on

#take input as the query




#the following code is just get max similarity between two given words
pos_list = ['n', 'v', 'a', 'r']
det_synsets1 = dict()
det_synsets2 = dict()
i = 0
b = list()
for a in pos_list:
	det_synsets1[i] = wn.synsets("summary", pos = a)
	i += 1
i = 0;
for a in pos_list:
	det_synsets2[i] = wn.synsets("abstract", pos = a)
	i += 1

list_format(det_synsets1,det_synsets2)


	
