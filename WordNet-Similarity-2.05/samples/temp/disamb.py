#! /usr/bin/python
import nltk
from nltk.corpus import wordnet as wn

flag = 0
import subprocess



#this function goes to perl and gives max similarity for two inputs
def disamb(l1,l2):
	a = list()
	print str(l1)
	set1 = str(l1)
	set2 = str(l2)
	cmd = ['perl', 'disamb.pl', set1, set2]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	for line in proc.stdout:
		print line;
	
def disamb1(l1):
	print str(l1)
	set1 = str(l1)
	
	cmd = ['perl', 'disamb.pl', set1]
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
	
	
def list_format1(ls1):
	
	l1 = list()
	temp = list()
	for i in range(0,len(ls1)):
		for j in range (0,len(ls1[i])):
			
			l1.append((str(ls1[i][j]).replace('Synset(\'','').replace('.','#').replace('\')','').replace('#s','#a')))
	
	disamb1(l1)
#write all the functions above , all inpus should be taken here on
word1 = raw_input().lower();
word2 = raw_input().lower();

det_synsets1 = dict()
det_synsets2 = dict()
i = 0
b = list()
pos_list = ['n', 'v', 'a', 'r']
for a in pos_list:
	det_synsets1[i] = wn.synsets(word1, pos = a)
	i += 1
print det_synsets1
i = 0;
for a in pos_list:
	det_synsets2[i] = wn.synsets(word2, pos = a)
	i += 1

list_format(det_synsets1,det_synsets2)


	
