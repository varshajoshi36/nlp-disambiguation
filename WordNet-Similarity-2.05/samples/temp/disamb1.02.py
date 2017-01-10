#! /usr/bin/python
import nltk
from nltk.corpus import wordnet as wn

flag = 0
import subprocess



#this function goes to perl and gives all the input
def disamb1(l1):
	#print str(l1)
	set1 = str(l1)
	
	cmd = ['perl', 'disamb1.02.pl', set1]
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

stop_words = set(["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another","anyhow","anyone","anything","anyway", "anywhere", "are", "around",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "former", "formerly", "forty", "found", "four", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie","is","inc", "indeed", "interest", "into",  "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"])

line = raw_input().lower()
line = line.split(" ")
for word in line:
	if word not in stop_words:
		querry.append(word)

print querry
data_synsets = dict()
j = 0
pos_list = ['n', 'v', 'a', 'r']
ab = list()
#print len(querry)
for i in range(0,(len(querry))):
	for a in pos_list:
		data_synsets[j] = wn.synsets(querry[i],pos = a)
		j += 1
		
list_format1(data_synsets)





	
