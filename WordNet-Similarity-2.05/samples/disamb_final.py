#!/usr/bin/env python
import solr
# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import string
import time
import sys
global text
global flg_list
global temp_final
global final_op;
global flg_list_to_disamb_perl
global q_size
global q_words
flg_list_to_disamb_perl = list()
final_op = list()
temp_final = list()
flg_list  = list()
text = list()
q_words = list()
flag = 0
import subprocess
def weighing_fun(l):
	l2 = sorted(l, key = lambda x: int(x[1]))
	l2.reverse()
	a = ((len(l2))/2) + 1 
	for i in range(0,a):
		if(l2[i][0] not in final_op):
			final_op.append(l2[i][0])
		
	
	
def ouput_to_solr(words,value):
	wv_arr = list()
	global temp_final
	wv_arr = zip(words,value[0])
	ip_to_weighing_fun = list()
	#q_words = list();
	for w in text:
		q_words.append(w[0])

	q_size = len(q_words)
	for w in q_words:
		final_op.append(w)
	cnt = 0;	
	for i in range(1,len(flg_list[0])):
		if ((flg_list[0][i]) == "0"):
			continue
		else:
			for w in wv_arr :
				if(w[0] == '%$#'):
					weighing_fun(ip_to_weighing_fun)
					for k in range(0,len(ip_to_weighing_fun)):
						ip_to_weighing_fun.pop(0)
					break
				else:
					ip_to_weighing_fun.append(w)
				cnt = cnt + 1			
			for j in range(0,cnt+1):
				wv_arr.pop(0)
			cnt = 0	
	temp_final = final_op	
	"""
	for i in range(0 , q_size):
		final_op[i] = final_op[i]+"^2"			
	#print final_op
	"""
	
def disamb2(l2,temp):
	temp1 = list()
	set1 = str(l2)
	cmd = ['perl', 'perl2.pl', set1]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	for line in proc.stdout:
		if 'val array =' in line:
			val_array = line
			
	temp1.append((val_array.replace('val array =','')).split(' '))
	del temp1[0][0]
	ouput_to_solr(temp,temp1)
		
def output_format(op):
	l1 = list()
	final = list()
	temp = list()
	l1.append((op.replace('#','.').replace('Output to python =','').replace('\n','').split(' ')))
	data_sn = list()
	for i in range(1,len(l1[0])):
		data_sn.append(wn.synset(str(l1[0][i])))
	for i in range(0,len(data_sn)):
		temp.append(data_sn[i].definition)
	temp1 = list()
	temp2 = list()
	stop1 = stopwords.words('english')
	for j in range(0,len(temp)):
		temp2 = temp[j].split(' ')
		for i in temp2:
			if(i not in stop1):
				temp1.append(i)
			else:
				continue
		temp1.append('%$#')		
	
	ip_perl2 = list()
	temp2 = list() 
	prev = 0
	for i in range(1,len(l1[0])):
		if '.n' in l1[0][i]:
			ip_perl2.append(data_sn[i-1])
			for k in range(prev,len(temp1)):
				if '%$#' in (temp1[k]):
					 prev = k + 1
					 ip_perl2.append('%$#')
					 break
				else:
					ip_perl2.append(wn.synsets(str(temp1[k]),pos='n'))
					ip_perl2.append('+%')
		else:
			ip_perl2.append(data_sn[i-1])
			for k in range(prev,len(temp1)):
				if '%$#' in (temp1[k]):
					 prev = k + 1
					 ip_perl2.append('%$#')
					 break
				else:
					ip_perl2.append(wn.synsets(str(temp1[k])))
					ip_perl2.append('+%')
	for i in range (0,len(ip_perl2)):
		
		final.append((str(ip_perl2[i]).replace('Synset(\'','').replace('.','#').replace('\')','').replace('#s','#a').replace('[','').replace(']','')))		
	disamb2(final,temp1)
	
		
#get pos of particular word
def get_pos(pnt):
	global text
	for i in text:
		if(i[0] == pnt):
			return i[1]
		else:
			continue

#for wordnet part-of-speech tagging
def get_wordnet_pos(treebank_tag):
	if treebank_tag.startswith('J'):
		return 'a'
	elif treebank_tag.startswith('V'):
		return 'v'
	elif treebank_tag.startswith('N'):
		return 'n'
	elif treebank_tag.startswith('R'):
		return 'r'

#this function goes to perl and gives all the input
def disamb1(l1):
	set1 = str(l1)
	cmd = ['perl', 'disamb_final.pl', set1]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	for line in proc.stdout:
		print line
		if 'Flag_list =' in line:
			flg = line
			print line
		if 'Output to python' in line:
			op_perl = line
			print line
	flg_list.append(flg.replace('Flag_list =','').replace('\n','').split(' '))
	output_format(op_perl)		
#following code formats the list which makes it acceptable for perl computations 	
def list_format1(ls1):
	l1 = list()
	temp = list()
	
	for i in range(0,len(ls1)):
		
		for j in range (0,len(ls1[i])):
			l1.append((str(ls1[i][j]).replace('Synset(\'','').replace('.','#').replace('\')','').replace('#s','#a')))
		if(i%4 == 3):
			l1.append('%+')	
	l1.append(flg_list_to_disamb_perl)
	
	disamb1(l1)
#write all the functions above , all inpus should be taken here on

#take input as the query
querry = []


print "enter input query"
sentence1 = raw_input().lower()
file_n = sentence1

#punctuation mark removal
for c in string.punctuation:
	sentence1= sentence1.replace(c,"")

text1 = nltk.word_tokenize(sentence1)
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

sentence = zip(words,final)

#stopwords removal
stop = stopwords.words('english')
for i in sentence:
	if(i[0] not in stop):
		text.append(i)
	else:
		continue

print text
flag = 0
data_synsets = dict()
j = 0
pos_list = ['n', 'v', 'a', 'r']
for w in text:
	for a in pos_list:
		if(a == w[1]):
			data_synsets[j] = wn.synsets(w[0],pos = w[1])
			if(len(data_synsets[j]) == 0):
				flg_list_to_disamb_perl.append('%$#')
				flg_list_to_disamb_perl.append('1')
				flag = 1
				while(j%4 != 0):
					j -= 1
				for b in pos_list:
					data_synsets[j] = wn.synsets(w[0],pos = b)
					j += 1
			if(flag == 0):
				flg_list_to_disamb_perl.append('%$#')
				flg_list_to_disamb_perl.append('2')		
		else :
			data_synsets[j] = wn.synsets("asdf")
	   	j += 1
	   	if(flag == 1):
	   		j -= 1
	   		flag = 0
			break
list_format1(data_synsets)




# create a connection to a solr server
s = solr.SolrConnection('http://localhost:8080/solr-4.7.0/')

expanded_q = "features:" + (str(final_op).replace('[','').replace(']','').replace('\'','').replace(',',''))
print expanded_q
a = str(expanded_q)
# do a search
'''response = s.query(a,rows = 20)
fh = open(file_n,"w")
temp_l = list()
new_l = list()
print "temp_final",temp_final
print q_words
for hit in response.results:
	fh.write(hit['id'])
	fh.write("\n")
	#print hit['features']
	temp_l = str(hit['features'][0]).split(' ')
	#print final_op
	for w in temp_l:
		for k in temp_final:
			#print k
			if (k == w):
				w = "**"+w+"**"
		new_l.append(w)		
	lines = str(new_l).replace('\\n',' ').replace('\'','').replace(',','').replace('\\t',' ').replace('[','').replace(']','')
	fh.write(lines)
	del new_l[0:len(new_l)]
	fh.write("\n\n")
'''
	
