
import sys
import pickle
from random import shuffle
import random
import json
from gensim.models import Word2Vec, KeyedVectors


things = []
finaltestset = {}
finaltestset["things"] = things

w2v_model = Word2Vec.load("word2vec_withoutString.model")
word_vectors = w2v_model.wv

print("finished loading w2v")
mode = "full"





keywords = ["full"]
#allowedKeywords = ["session fixation", "command injection", "session hijacking", "replay attack", "man-in-the-middle", "sql injection", "tampering", "XSS", "cross site", "remote code execution", "XSRF", "cross site request forgery", "path traversal", "directory traversal", "hijack"]

allowedKeywords = ["session fixation", "command injection", "sql injection", "XSS", "cross site", "remote code execution", "XSRF", "cross site request forgery", "hijack"]
#keywords = ["sql"]
#allowedKeywords=["sql"]
 
data = {}
for m in keywords:
  with open('data2/' + m + '-onlyWithRepSuccess', 'r') as infile:
      datanew = json.load(infile)
      for r in datanew:
        data[r] = datanew[r]
      
    
print("finished loading data.")

print(len(data))
c = 0
clean = 0
for r in data:
  #print(r)
  for commit in data[r]:
    #print(commit)
    if "changes" in data[r][commit]:
      if len(data[r][commit]["changes"]) > 0:
        c = c + len(data[r][commit]["changes"])
    if "clean" in data[r][commit]:
      if len(data[r][commit]["clean"]) > 0:
        clean = clean + len(data[r][commit]["clean"])
        
      
print(str(c) + " changes.")
print(str(clean) + " clean blocks.")
print("finished loading")


print("doing things in mode " + mode)

shuffleme = []
for r in data:
  for c in data[r]:
#      for key in allowedKeywords:
#        if key in data[r][c]["keyword"]:
          if "changes" in data[r][c]:
            commitobj = {}
            commitobj["r"] = r
            commitobj["c"] = c
            if "changes" in data[r][c]:       
              commitobj["changes"] = data[r][c]["changes"]
              commitobj["clean"] = []
              if "clean" in data[r][c]:
                commitobj["clean"] = data[r][c]["clean"]
            shuffleme.append(commitobj)
            break

print(str(len(shuffleme)) + " is the length of shuffleme.")          
random.shuffle(shuffleme)


cutoff = round(0.7 * len(shuffleme))
cutoff2 = round(0.85 * len(shuffleme))


train = shuffleme[:cutoff]
test = shuffleme[cutoff:cutoff2]
finaltest = shuffleme[cutoff2:]

TrainX = []
TrainY = []

ValidateX = []
ValidateY = []

FinaltestX = []
FinaltestY = []

for commit in train:
  for change in commit["changes"]:
    token = change["previous-token"]              
    vectorlist = []
    for t in token:
        if t in word_vectors.vocab and t != " ":
          vector = w2v_model[t]
          vectorlist.append(vector)
      
    TrainX.append(vectorlist)
    TrainY.append(0)
    
    
    token = change["after-token"]                
    vectorlist = []
    for t in token:
        if t in word_vectors.vocab and t != " ":
          vector = w2v_model[t]
          vectorlist.append(vector)
      
    TrainX.append(vectorlist)
    TrainY.append(1)
      
  for clean in commit["clean"]:
    
    token = clean["source"]
    vectorlist = []
    for t in token:
        if t in word_vectors.vocab and t != " ":
          vector = w2v_model[t]
          vectorlist.append(vector)
      
    TrainX.append(vectorlist)
    TrainY.append(1)
    
    
    


for commit in test:
  for change in commit["changes"]:
    
    token = change["previous-token"]              
    vectorlist = []
    for t in token:
        if t in word_vectors.vocab and t != " ":
          vector = w2v_model[t]
          vectorlist.append(vector)
      
    ValidateX.append(vectorlist)
    ValidateY.append(0)
    
    
    token = change["after-token"]                
    vectorlist = []
    for t in token:
        if t in word_vectors.vocab and t != " ":
          vector = w2v_model[t]
          vectorlist.append(vector)
      
    ValidateX.append(vectorlist)
    ValidateY.append(1)
      
  for clean in commit["clean"]:
    
    token = clean["source"]
    vectorlist = []
    for t in token:
        if t in word_vectors.vocab and t != " ":
          vector = w2v_model[t]
          vectorlist.append(vector)
      
    ValidateX.append(vectorlist)
    ValidateY.append(1)



for commit in finaltest:
  for change in commit["changes"]:
    
    token = change["previous-token"]              
    vectorlist = []
    for t in token:
        if t in word_vectors.vocab and t != " ":
          vector = w2v_model[t]
          vectorlist.append(vector)
      
    FinaltestX.append(vectorlist)
    FinaltestY.append(0)
    
    obj = {}
    obj["previous"] = change["previous"]
    obj["after"] = change["after"]
    obj["previous-token"] = change["previous-token"]
    obj["after-token"] = change["after-token"]
    obj["keyword"] = change["keyword"]
    obj["value"] = 0
    #obj["vectorlist"] = vectorlist
    obj["repository"] = commit["r"]
    obj["commit"] = commit["c"]
    finaltestset["things"].append(obj)
    
    
    ### AFTER - CLEAN - NOT VULNERABLE - 1
    
    token = change["after-token"]                
    vectorlist = []
    
    for t in token:
        if t in word_vectors.vocab and t != " ":
          vector = w2v_model[t]
          vectorlist.append(vector)
      
    obj = {}
    obj["previous-token"] = change["previous-token"]
    obj["after-token"] = change["after-token"]
    obj["previous"] = change["previous"]
    obj["after"] = change["after"]
    obj["keyword"] = change["keyword"]
    obj["value"] = 1
    #obj["vectorlist"] = vectorlist
    obj["repository"] = commit["r"]
    obj["commit"] = commit["c"]
    finaltestset["things"].append(obj)

      
  for clean in commit["clean"]:
    
    token = clean["source"]
    vectorlist = []
    for t in token:
        if t in word_vectors.vocab and t != " ":
          vector = w2v_model[t]
          vectorlist.append(vector)
    
    
    
    obj = {}
    obj["previous-token"] = clean["source"]
    obj["after-token"] = clean["source"]
    obj["previous"] = clean["source"]
    obj["after"] = clean["source"]
    obj["keyword"] = clean["keyword"]
    obj["value"] = 1
    #obj["vectorlist"] = vectorlist
    obj["repository"] = commit["r"]
    obj["commit"] = commit["c"]
    finaltestset["things"].append(obj)
    

    
print("\n\n")
#print("Finaltesting length (changes): " + str(len(finaltesting)))

with open('data2/' + mode + '_dataset-train-X', 'wb') as fp:
  pickle.dump(TrainX, fp)
with open('data2/' + mode + '_dataset-train-Y', 'wb') as fp:
  pickle.dump(TrainY, fp)
with open('data2/' + mode + '_dataset-validate-X', 'wb') as fp:
  pickle.dump(ValidateX, fp)
with open('data2/' + mode + '_dataset-validate-Y', 'wb') as fp:
  pickle.dump(ValidateY, fp)
with open('data2/' + mode + '_dataset-finaltest-X', 'wb') as fp:
  pickle.dump(FinaltestX, fp)
with open('data2/' + mode + '_dataset-finaltest-Y', 'wb') as fp:
  pickle.dump(FinaltestY, fp)
  

#with open('data/' + mode + "_origPre", 'wb') as fp:
#  pickle.dump(origPre, fp)

#with open('data/' + mode + "_origAfter", 'wb') as fp:
#  pickle.dump(origAfter, fp)

#with open('data/' + mode + "_origKey", 'wb') as fp:
#    pickle.dump(origKey, fp)
    
#with open('data/' + mode + "_origVectorlist", 'wb') as fp:
#    pickle.dump(origVectorlist, fp)
    
#with open('data/' + mode + "_origValue", 'wb') as fp:
#    pickle.dump(origValue, fp)

with open('data2/finaltestset-'+mode+'.json', 'w') as outfile:
  json.dump(finaltestset, outfile)
  

  
#with open('everything-'+mode, 'w') as outfile:
#  json.dump(shuffleme, outfile)
  
  
