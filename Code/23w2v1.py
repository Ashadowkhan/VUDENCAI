import bs4 as bs  
import urllib.request  
import re  
import nltk
from gensim.models import Word2Vec, KeyedVectors
import sys
import pickle



#mode = "Self-X"
#mode = "Self-XVAR"

#mode = "Self-XwithoutStrings"
#mode = "interlaken"
all_words = []
    

#mode = "withString"
mode = "withoutString"    
f = "_long"
f = ""
#with open('alldata-w2v-'+mode, 'rb') as fp:
#    all_words = pickle.load(fp)


#print (all_words[:100])
    
with open('w2v/pythontraining4' + f + '_'+mode+"_X", 'r') as file:
    pythondata = file.read().lower().replace('\n', ' ')
print(len(pythondata))
print(str(pythondata.count(" ")) + " token")
print(pythondata.count("\n"))
print("done with reading")

#if ("#" in pythondata):
# pos = pythondata.find("#")
# print(pythondata[pos-10:pos+20])

#sys.exit()

processed = pythondata.lower()  
#Preparing the dataset
all_sentences = nltk.sent_tokenize(processed)
all_words = [nltk.word_tokenize(sent) for sent in all_sentences]

print("model")

model = Word2Vec(all_words, min_count=200, iter=2000)  
#model.build_vocab(all_sentences, update=False)


#print("1")

vocabulary = model.wv.vocab  

#print("2")

print("saving")

model.save("word2vec_"+mode+"200-2000.model")

print("loading")
model = Word2Vec.load("word2vec_"+mode+"200-2000.model")

words = ["[", "import", "print", "=","none", "for", "x", "if", "while", "try", "+", "i", "k", "{", ":", "in", "while", "import", "return", "true", "false"]
for similar in words:
  try:
    print("\n")
    print(similar)
    sim_words = model.wv.most_similar(similar)  
    print(sim_words)
    print("\n\n")
  except Exception as e:
    print(e)
    print("\n")
