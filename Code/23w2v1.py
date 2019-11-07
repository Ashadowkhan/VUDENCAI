import nltk
from gensim.models import Word2Vec, KeyedVectors

all_words = []
    

#mode = "withString"
mode = "withoutString"   

    
with open('w2v/pythontraining' + '_'+mode+"_X", 'r') as file:
    pythondata = file.read().lower().replace('\n', ' ')
print("Length of the training file: " + str(len(pythondata)) + ".")
print("It contains " + str(pythondata.count(" ")) + " individual code tokens.")
print("\n")


processed = pythondata.lower()  


#Preparing the dataset
all_sentences = nltk.sent_tokenize(processed)
all_words = [nltk.word_tokenize(sent) for sent in all_sentences]


for mode in ["withString","withoutString"]:
  for mincount in [300,500,5000]:
    for iterationen in [100]:
      for s in [200]:
        model = Word2Vec(all_words, size=s, min_count=mincount, iter=iterationen)  

        vocabulary = model.wv.vocab  


        print("\n\n" + mode + " W2V model with min count " + str(mincount) + " and " + str(iterationen) + " Iterationen and size " + str(s))

        words = ["import", "true", "while", "if", "try", "in", "+", "x", "=", ":", "[", "print", "str", "count", "len", "where", "join", "split", "==", "raw_input"]
        for similar in words:
          try:
            print("\n")
            print(similar)
            sim_words = model.wv.most_similar(similar)  
            print(sim_words)
            print("\n")
          except Exception as e:
            print(e)
            print("\n")
            
        model.save("w2v/word2vec_"+mode+str(mincount) + "-" + str(iterationen) +"-" + str(s)+ ".model")

  #print("loading")
#model = Word2Vec.load("w2v/word2vec_"+mode+"100-1000.model")


