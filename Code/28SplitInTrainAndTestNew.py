
import sys
import pickle
from random import shuffle
import random
import json
import numpy
from gensim.models import Word2Vec, KeyedVectors





mode = "command_injection"
#modelw2v = "word2vec_withoutString.model"
modelw2v = "word2vecinterlaken.model"

if (len(sys.argv) > 1):
  mode = sys.argv[1]
  if (len(sys.argv) > 2):
    modelw2v = sys.argv[2]
    

w2v_model = Word2Vec.load(modelw2v)
word_vectors = w2v_model.wv

print("finished loading w2v")


keywords = ["command_injection"]
allowedKeywords = ["command injection"] 


if mode == "command_injection":
  keywords = ["command_injection"]
  allowedKeywords = ["command injection"] 

if mode == "function_injection":
  keywords = ["function_injection"]
  allowedKeywords = ["function injection"] 

if mode == "sql":
  keywords = ["sql"]
  allowedKeywords = ["sql injection"] 


if mode == "xsrf":
  keywords = ["xsrf"]
  allowedKeywords = ["xsrf", "cross site request forgery"] 


if mode == "xss":
  keywords = ["xss"]
  allowedKeywords = ["xss", "cross site scripting"] 


if mode == "replay_attack":
  keywords = ["replay_attack"]
  allowedKeywords = ["replay attack"] 



if mode == "unauthorized":
  keywords = ["unauthorized"]
  allowedKeywords = ["unauthorized", "unauthorised"]
  
  
if mode == "brute_force":
  keywords = ["brute_force"]
  allowedKeywords = ["brute force"]
  
  
if mode == "flooding":
  keywords = ["flooding"]
  allowedKeywords = ["flooding"]


#allowedKeywords = ["session fixation", "command injection", "session hijacking", "replay attack", "man-in-the-middle", "sql injection", "tampering", "XSS", "cross site", "remote code execution", "XSRF", "cross site request forgery", "path traversal", "directory traversal", "hijack"]

#allowedKeywords = ["session fixation", "command injection", "sql injection", "XSS", "cross site", "remote code execution", "XSRF", "cross site request forgery", "hijack"]
#keywords = ["sql"]
#allowedKeywords=["sql"]


print("doing things in mode " + mode)

 
data = {}
for m in keywords:
  with open('data3/' + m + '-onlyWithRepSuccess', 'r') as infile:
      datanew = json.load(infile)
      for r in datanew:
        data[r] = datanew[r]
      

print("finished loading data.")

print("Repositories in data: " + str(len(data)))
c = 0
clean = 0

datanew = {}
counter = 0 
counter2 = 0
actualdata = {}

changedict = {}

for r in data:
  for c in data[r]:
    
    if c in changedict:
      if changedict[c] > 10:
        changedict[c] = changedict[c] + 1
        print(" we already have more than ten. Skip.")
        continue
      if changedict[c] > 1:
        for u in datanew:
          for v in datanew[u]:
            for w in datanew[u][v]:
              if w == c and (v != r) and (len(datanew[u][v][w]["changes"]) == len(datanew[counter][r][c]["changes"])):
                    #print(r + "/" + c)
                    if (len(datanew[counter][r][c]["clean"]) > 0 and len(datanew[u][v][w]["clean"]) > 0):
                      if(datanew[counter][r][c]["clean"][0]["source"][:20] != datanew[u][v][w]["clean"][0]["source"][:20]):
                        print("They are different after all!")
                        sys.exit()
                    if(datanew[counter][r][c]["changes"][0]["previous"][:20] != datanew[u][v][w]["changes"][0]["previous"][:20]):
                      print("They are different after all!")
                      sys.exit()
    else:
      changedict[c] = 1
    
    #print(commit)
    if ("changes" in data[r][c] and "clean" in data[r][c]):
      datanew[counter] = {}
      datanew[counter][r] = {}
      datanew[counter][r][c] = data[r][c]
      
      
      changeIsFine = True
      for changenr in range(0,len(datanew[counter][r][c]["changes"])):
      
        #print(datanew[counter][r][c]["changes"][changenr].keys())
        #print("Change nr. " + str(changenr))
        #print("Len: " + str(len(datanew[counter][r][c]["changes"][changenr]["previous-token"])))

        #previous - this is vulnerable
        token = datanew[counter][r][c]["changes"][changenr]["previous-token"]              
        vectorlist = []
        for t in token:
          if t in word_vectors.vocab and t != " ":
             vector = w2v_model[t]
             vectorlist.append(vector.tolist())      
        datanew[counter][r][c]["changes"][changenr]["previous-vectorlist"] = vectorlist
        
        
        
        a = len(datanew[counter][r][c]["changes"][changenr]["previous-vectorlist"])
        if (a == 0):
         # print("ZERO known prev token")
         # print(datanew[counter][r][c]["changes"][changenr]["previous-token"])
         # print("\n\n")
          changeIsFine = False
        
        
        #after - this is clean
        token = datanew[counter][r][c]["changes"][changenr]["after-token"]                
        vectorlist = []
        for t in token:
          if t in word_vectors.vocab and t != " ":
             vector = w2v_model[t]
             vectorlist.append(vector.tolist())
             
        datanew[counter][r][c]["changes"][changenr]["after-vectorlist"] = vectorlist
        
        b = len(datanew[counter][r][c]["changes"][changenr]["after-vectorlist"])
        if (b == 0):
          #print("ZERO known after token")
          #print(datanew[counter][r][c]["changes"][changenr]["after-token"])
          #print("\n\n")
          changeIsFine = False
        


      if (len(datanew[counter][r][c]["clean"]) == 0):
       # print("0")
        changeIsFine = False


      for cleannr in range(0,len(datanew[counter][r][c]["clean"])):
        token = datanew[counter][r][c]["clean"][cleannr]["source"]
        vectorlist = []
        for t in token:
            if t in word_vectors.vocab and t != " ":
              vector = w2v_model[t]
              vectorlist.append(vector.tolist())
        
        datanew[counter][r][c]["clean"][cleannr]["vectorlist"] = vectorlist    
        if (len(datanew[counter][r][c]["clean"][cleannr]["vectorlist"]) == 0):
            #print("ZERO known token in this clean block")
            #print(datanew[counter][r][c]["clean"][cleannr]["source"])
            #print("\n\n")
            changeIsFine = False
      
      
      if changeIsFine:
        
        
        actualdata[counter2] = {}
        actualdata[counter2][r] = {}
        actualdata[counter2][r][c] = datanew[counter][r][c]
        
        if len(actualdata[counter2][r][c]["clean"]) == 0:
          print("???????????")
          print(len(datanew[counter][r][c]["clean"]))
        counter2 = counter2 + 1
        
      else:
        o = 1 #noop
       # print("nope, this change was not fine.")

      counter = counter +1
      
      
    else:
      o = 0 #noop
#      print("something was not present")

print("\n\n")      
sortedchangedict = sorted(changedict.items(), key = lambda x : x[1])

#print(sortedchangedict)

print("\n\n")
print("unique: " + str(len(sortedchangedict)))
print("\n\n")
print("Datanew length: " +str(len(datanew)))
print("Actualdata length: " + str(len(actualdata)))

      

keys = list(actualdata.keys())

cutoff = round(0.7 * len(keys))
cutoff2 = round(0.85 * len(keys))

random.shuffle(keys)

keystrain = keys[:cutoff]
keystest = keys[cutoff:cutoff2]
keysfinaltest = keys[cutoff2:]

print(keys)
print("\n\n")
print(keystrain)
print("\n\n")
print(keystest)
print("\n\n")
print(keysfinaltest)
print("\n\n")



trainingset = {}
testset = {}
finaltestset = {}

TrainX = []
TrainY = []
ValidateX = []
ValidateY = []
FinaltestX = []
FinaltestY = []


r = ""
c = ""

for k in keystrain:
  trainingset[k] = actualdata[k]

  for r in trainingset[k]:
    for c in trainingset[k][r]:
      for changenr in range(len(trainingset[k][r][c]["changes"])):
         TrainX.append(trainingset[k][r][c]["changes"][changenr]["after-vectorlist"])
         TrainY.append(1)
         TrainX.append(trainingset[k][r][c]["changes"][changenr]["previous-vectorlist"])
         TrainY.append(0)
      for cleannr in range(len(trainingset[k][r][c]["clean"])):
         TrainX.append(trainingset[k][r][c]["clean"][cleannr]["vectorlist"])
         TrainY.append(1)
                                 
  
  
for k in keystest:
  testset[k] = actualdata[k]
  
  for r in testset[k]:
    for c in testset[k][r]:
      for changenr in range(len(testset[k][r][c]["changes"])):
         ValidateX.append(testset[k][r][c]["changes"][changenr]["after-vectorlist"])
         ValidateY.append(1)
         ValidateX.append(testset[k][r][c]["changes"][changenr]["previous-vectorlist"])
         ValidateY.append(0)
      for cleannr in range(len(testset[k][r][c]["clean"])):
         ValidateX.append(testset[k][r][c]["clean"][cleannr]["vectorlist"])
         ValidateY.append(1)

for k in keysfinaltest:
  finaltestset[k] = actualdata[k]
  for r in finaltestset[k]:
    for c in finaltestset[k][r]:
      
      
   #   print("-------------------")
   #   for x in range(len(finaltestset[k][r][c]["clean"])):
   #     print(x)
   #     print(finaltestset[k][r][c]["clean"][x]["file"])
   #     print(len(finaltestset[k][r][c]["clean"][x]["vectorlist"]))
        
   #     print(type(finaltestset[k][r][c]["clean"][x]["vectorlist"]))
        
   #     with open('data3/blob', 'w') as outfile:
   #       obj = {}
   #       listv = finaltestset[k][r][c]["clean"][x]["vectorlist"]
   #       print(type(listv))
   #       obj[x] = []
   #       for y in listv:
   #         print(y)
   #         print(type(y))
   #         obj[x].append(y.tolist())
   #         
   #       json.dump(obj, outfile)
   #     print("----")
   #     sys.exit()
   #   print("-------------------")


#      print(finaltestset[k][r][c]["clean"][0].keys())#
#
#      for k in finaltestset[k][r][c]["clean"][0]:
#        with open('data3/blob', 'w') as outfile:
#          
#          print(finaltestset[k][r][c]["clean"])
#          x = finaltestset[k][r][c]["clean"][0][k]
#          print(k)
#          json.dump(x, outfile)
        
        
        
      
        
        
     # with open('data3/blob', 'w') as outfile:
     #   json.dump(finaltestset[k][r][c]["message"], outfile)
        
     # with open('data3/blob', 'w') as outfile:
     #   json.dump(finaltestset[k][r][c]["clean"], outfile)
      
      for changenr in range(len(finaltestset[k][r][c]["changes"])):
         FinaltestX.append(finaltestset[k][r][c]["changes"][changenr]["after-vectorlist"])
         FinaltestY.append(1)
         FinaltestX.append(finaltestset[k][r][c]["changes"][changenr]["previous-vectorlist"])
         FinaltestY.append(0)
      for cleannr in range(len(finaltestset[k][r][c]["clean"])):
         FinaltestX.append(finaltestset[k][r][c]["clean"][cleannr]["vectorlist"])
         FinaltestY.append(1)








    
print("\n\n")
print("Train length: " + str(len(TrainX)))
print("Test length: " + str(len(ValidateX)))
print("Finaltesting length: " + str(len(FinaltestX)))


        
        

with open('data3/' + mode + '_dataset-train-X-withDuplicates', 'wb') as fp:
  pickle.dump(TrainX, fp)
with open('data3/' + mode + '_dataset-train-Y-withDuplicates', 'wb') as fp:
  pickle.dump(TrainY, fp)
with open('data3/' + mode + '_dataset-validate-X-withDuplicates', 'wb') as fp:
  pickle.dump(ValidateX, fp)
with open('data3/' + mode + '_dataset-validate-Y-withDuplicates', 'wb') as fp:
  pickle.dump(ValidateY, fp)
with open('data3/' + mode + '_dataset-finaltest-X-withDuplicates', 'wb') as fp:
  pickle.dump(FinaltestX, fp)
with open('data3/' + mode + '_dataset-finaltest-Y-withDuplicates', 'wb') as fp:
  pickle.dump(FinaltestY, fp)

#with open('data3/trainingset-'+mode, 'w') as outfile:
#  json.dump(trainingset, outfile)
  
#with open('data3/testset-'+mode, 'w') as outfile:
#  json.dump(testset, outfile)
  
with open('data3/finaltestset-'+mode, 'w') as outfile:
  json.dump(finaltestset, outfile)
  
























sys.exit()



cutoff = round(0.7 * len(shuffleme))
cutoff2 = round(0.85 * len(shuffleme))

train = shuffleme[:cutoff]
test = shuffleme[cutoff:cutoff2]
finaltest = shuffleme[cutoff2:]


for commit in train:

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



print(finaltest)


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
    

    token = change["after-token"]                
    vectorlist = []    
    for t in token:
        if t in word_vectors.vocab and t != " ":
          vector = w2v_model[t]
          vectorlist.append(vector)
    FinaltestX.append(vectorlist)
    FinaltestY.append(1) 

      
  for clean in commit["clean"]:
    token = clean["source"]
    vectorlist = []
    for t in token:
        if t in word_vectors.vocab and t != " ":
          vector = w2v_model[t]
          vectorlist.append(vector)
    FinaltestX.append(vectorlist)
    FinaltestY.append(1)
    

    
print("\n\n")
print("Train length: " + str(len(TrainX)))
print("Test length: " + str(len(ValidateX)))
print("Finaltesting length: " + str(len(FinaltestX)))

with open('data3/' + mode + '_dataset-train-X-new', 'wb') as fp:
  pickle.dump(TrainX, fp)
with open('data3/' + mode + '_dataset-train-Y-new', 'wb') as fp:
  pickle.dump(TrainY, fp)
with open('data3/' + mode + '_dataset-validate-X-new', 'wb') as fp:
  pickle.dump(ValidateX, fp)
with open('data3/' + mode + '_dataset-validate-Y-new', 'wb') as fp:
  pickle.dump(ValidateY, fp)
with open('data3/' + mode + '_dataset-finaltest-X-new', 'wb') as fp:
  pickle.dump(FinaltestX, fp)
with open('data3/' + mode + '_dataset-finaltest-Y-new', 'wb') as fp:
  pickle.dump(FinaltestY, fp)

with open('data3/finaltest-'+mode+'.json', 'w') as outfile:
  json.dump(finaltest, outfile)
  
