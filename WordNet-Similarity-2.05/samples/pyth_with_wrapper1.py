#! /usr/bin/python
import nltk
from nltk.corpus import wordnet as wn

flag = 0
import subprocess

def checkpoly(l1):
	n = len(l1)
	a = list()
	cmd = ['perl', 'test.pl', l1]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	print proc
	#print a		
	no = len(a)
	for i in range (0, no):
		if(a[i] < 0.9900):
			flag = 1
	
l = dict()
def list_format(l):
	
	l1 = list()
	for i in range(0,len(l)):
		for j in range (0,len(l[i])):
			l1.append((str(l[i][j]).replace('Synset(\'','').replace('.','#').replace('\')','').replace('#s','#a')))	
	#print l1	
	checkpoly(l1)
	


pos_list = ['n', 'v', 'a', 'r']
det_synsets = dict()
i = 0
b = list()
for a in pos_list:
	det_synsets[i] = wn.synsets("full", pos = a)
	i += 1


list_format(det_synsets)

for i in range(0,3):
	if(len(det_synsets[i]) > 1):
		checkpoly(det_synsets[i])	
