import nltk
from gensim.models import Word2Vec, KeyedVectors
import os.path
import pickle
all_words = []
    




for mode in ["withString","withoutString"]:
#for mode in ["withoutString","withString"]:
#for mode in ["withString"]:


  print("Loading " + mode)  
  with open('w2v/pythontraining' + '_'+mode+"_X", 'r') as file:
      pythondata = file.read().lower().replace('\n', ' ')
  print("Length of the training file: " + str(len(pythondata)) + ".")
  print("It contains " + str(pythondata.count(" ")) + " individual code tokens.")

# processed = pythondata.lower()  
# Preparing the dataset


  if (os.path.isfile('data/pythontraining_processed_' + mode)):
    with open ('data/pythontraining_processed_' + mode, 'rb') as fp:
      all_words = pickle.load(fp)
    print("loaded processed model.")
  else:  
    print("now processing...")
    processed = pythondata
    all_sentences = nltk.sent_tokenize(processed)
    all_words = [nltk.word_tokenize(sent) for sent in all_sentences]
    print("saving")
    with open('data/pythontraining_processed_' + mode, 'wb') as fp:
      pickle.dump(all_words, fp)
    

  print("processed.\n")

  
  #for mincount in [5000,500,300,100,50,30,10]:
  for mincount in [10,30,50,100,300,500,5000]:
#  for mincount in [10,100,5000]:
#    for iterationen in [1,10,30]:
    for iterationen in [1,5,10,30,50,100]:

#    for iterationen in [100,50,30,10,5,1]:
#     for iterationen in [1]:
#      for s in [5,10,15,30,50,75,100,200,300]:
      for s in [200]:
        
          
        print("\n\n" + mode + " W2V model with min count " + str(mincount) + " and " + str(iterationen) + " Iterationen and size " + str(s))
        fname = "w2v/word2vec_"+mode+str(mincount) + "-" + str(iterationen) +"-" + str(s)+ ".model"
        
        
        if (os.path.isfile(fname)):
          print("model already exists.")
          continue
        
        else:
          print("calculating model...")
          model = Word2Vec(all_words, size=s, min_count=mincount, iter=iterationen, workers = 4)  
          vocabulary = model.wv.vocab  
          #words = ["import", "true", "while", "if", "try", "in", "+", "x", "=", ":", "[", "print", "str", "count", "len", "where", "join", "split", "==", "raw_input"]
          #for similar in words:
          #  try:
          #    print("\n")
          #    print(similar)
          #    sim_words = model.wv.most_similar(similar)  
          #    print(sim_words)
          #    print("\n")
          #  except Exception as e:
          #    print(e)
          #    print("\n")
          print("done. Saving.")
          model.save(fname)

  #print("loading")
#model = Word2Vec.load("w2v/word2vec_"+mode+"100-1000.model")


