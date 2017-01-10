import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import string
import subprocess
global text
text = list()

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
'''
#create dictionary
def create_dictionary(ls1):
	#pos_list = ['n', 'v', 'a', 'r']
	dictionary = dict()
	i = 0
	for w in ls1:
		dictionary[i] = wn.synsets(ls1, pos = a)
		i = i + 1
	return dictionary
'''

#formating synset
def list_format(ls):
	l = list()
	for i in ls:
		l.append(str(i).replace('Synset(\'','').replace('.','#').replace('\')','').replace('#s','#a'))
	return l

#get appropriate sense
def get_sense(target,win1):
	#print "window argument is:"
	#print str(win)
	win = list()
	win = win1
	pos = get_pos(target)
	target_synset = wn.synsets(target, pos)
	target_syns = list_format(target_synset)
	#for w in win:
		#print w
	for w in win:
		w_synset = wn.synsets(w,pos = get_pos(w)) 
		if (w_synset == []):
			w_synset = wn.synsets(w)
			
		w_syns = list_format(w_synset)
		cmd = ['perl','disamb.pl',str(target_syns),str(w_syns)]
		proc = subprocess.Popen(cmd,stdout = subprocess.PIPE)
		for line in proc.stdout:
			print line;
	
		
#windowing mechanism
def window_elements(win,ind):
	global text
	if(len(text) == 1):
		return
	elif(ind == 0 and len(text) == 2):
		win.append(text[1][0])
	elif(ind == 1 and len(text) == 2):
		win.append(text[0][0])
	elif(ind == 0):
		win.append(text[index + 1][0])
		win.append(text[index + 2][0])
	elif(ind == (len(text) - 1)):
		win.append(text[index - 1][0])
		win.append(text[index - 2][0])
	elif(ind == 1 and len(text) < 4):
		win.append(text[index - 1][0])
		win.append(text[index + 1][0])
	elif(ind == (len(text) - 2) and len(text) >= 4):
		win.append(text[index + 1][0])
		win.append(text[index - 1][0])
		win.append(text[index - 2][0])
	elif(ind >= 2 or ind <= (len(text) - 3)):
		win.append(text[index + 1][0])
		win.append(text[index + 2][0])
		win.append(text[index - 1][0])
		win.append(text[index - 2][0])
	return win

print "enter input query"
sentence1 = raw_input().lower()

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

#polysemy detection
polysemy = list()
for w in text:
	if(len(wn.synsets(w[0],pos = w[1])) > 1):
		polysemy.append(w[0])
	else:
		continue
print "polysemy words are:"
print polysemy

for w in polysemy:
	window = list()
	#index = text.index(w)
	for s in text:
		if(s[0] == w):
			index = text.index(s)
		else:
			continue
	window = window_elements(window,index)
	sense = get_sense(w,window)
	
	
