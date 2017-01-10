#! /usr/bin/python
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import string

global text
text = list()
flag = 0
import subprocess

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
	#print str(l1)
	set1 = str(l1)
	
	cmd = ['perl', 'disamb_final.pl', set1]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	for line in proc.stdout:
		print line
			
#following code formats the list which makes it acceptable for perl computations 	
def list_format1(ls1):
	
	l1 = list()
	temp = list()
	for i in range(0,len(ls1)):
		
		for j in range (0,len(ls1[i])):
			l1.append((str(ls1[i][j]).replace('Synset(\'','').replace('.','#').replace('\')','').replace('#s','#a')))
		if(i%4 == 3):
			l1.append('%+')	
	disamb1(l1)
#write all the functions above , all inpus should be taken here on

#take input as the query
querry = []

stop_words = set(["i","a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another","anyhow","anyone","anything","anyway", "anywhere", "are", "around",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "former", "formerly", "forty", "found", "four", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie","is","inc", "indeed", "interest", "into",  "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"])

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




flag = 0
data_synsets = dict()
j = 0
pos_list = ['n', 'v', 'a', 'r']
for w in text:
	for a in pos_list:
		if(a == w[1]):
			data_synsets[j] = wn.synsets(w[0],pos = w[1])
			if(len(data_synsets[j]) == 0):
				flag = 1
				while(j%4 != 0):
					j -= 1
				for b in pos_list:
					data_synsets[j] = wn.synsets(w[0],pos = b)
					j += 1
		else :
			data_synsets[j] = wn.synsets("asdf")
	   	j += 1
	   	if(flag == 1):
	   		j -= 1
	   		flag = 0
			break

		
list_format1(data_synsets)





	
