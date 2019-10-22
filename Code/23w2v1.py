import nltk
from gensim.models import Word2Vec, KeyedVectors

all_words = []
    

mode = "withString"
#mode = "withoutString"   

    
with open('w2v/pythontraining' + '_'+mode+"_X", 'r') as file:
    pythondata = file.read().lower().replace('\n', ' ')
print("Length of the training file: " + str(len(pythondata)) + ".")
print("It contains " + str(pythondata.count(" ")) + " individual code tokens.")
print("\n")


processed = pythondata.lower()  


#Preparing the dataset
all_sentences = nltk.sent_tokenize(processed)
all_words = [nltk.word_tokenize(sent) for sent in all_sentences]

print("model")

model = Word2Vec(all_words, min_count=100, iter=1000)  

vocabulary = model.wv.vocab  

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

print("saving")

model.save("w2v/word2vec_"+mode+"100-1000.model")

#print("loading")
#model = Word2Vec.load("w2v/word2vec_"+mode+"100-1000.model")


