import utils

import time
import sys
import json
#import StringIO
#from io import StringIO
import subprocess
from datetime import datetime
import bs4 as bs  
import urllib.request  
import re  
import nltk
import builtins
import requests 
import keyword
from random import shuffle
import random
import pickle
from pydriller import RepositoryMining
from gensim.models import Word2Vec, KeyedVectors

import os.path



#===========================================================================













sourcecode= """uery): text_query_str=str(text_query) a"""
badpart = """text_query_str = str(text_query) # SQLObject chokes on unicode.\na"""

print(utils.findposition(badpart,sourcecode))


sys.exit()















mode = "sql"


if (len(sys.argv) > 1):
  mode = sys.argv[1]

                
                
  


now = datetime.now() # current date and time
nowformat = now.strftime("%H:%M")
print("time:", nowformat)



with open('data/plain_' + mode, 'r') as infile:
  data = json.load(infile)

print("finished loading")

print("\n\n")

count = 0


progress = 0
count = 0


for param in [[5,200]]:
  for mincount in [10]:
#  for mincount in [5000,500,300,100,30,10]:
    #for iterationen in [1,5,10,30,50,100,500]:
    for iterationen in [300]:
  #    for s in [5,10,15,30,50,75,100,200,300]:
      for s in [200]:
        for w in ["withString"]:



                print("\n")
                print("=================Blocks======================================")

                w2v = "word2vec_"+w+str(mincount) + "-" + str(iterationen) +"-" + str(s)
                w2vmodel = "w2v/" + w2v + ".model"
                step = param[0]
                fulllength = param[1]
                mode2 = str(step)+"_"+str(fulllength)

                print(mode)
                print(w2vmodel)
                print(mode2)
                
                filename = 'data/plain_' + mode + '_dataset-train-X_'+w2v + "__" + mode2
                
                
               # if(os.path.isfile(filename)):
               #   print("dataset already exists")
               #   continue
                
                
                if not (os.path.isfile(w2vmodel)):
                  print("word2vec model is still being created...")
                  continue
                
                
                w2v_model = Word2Vec.load(w2vmodel)
                word_vectors = w2v_model.wv

                
                allblocks = []


                
                for r in data:

                  progress = progress + 1
                  for c in data[r]:
                    
                    if "files" in data[r][c]:
                      for f in data[r][c]["files"]:
                        
                        if "source" in data[r][c]["files"][f]:
                          
                          sourcecode = data[r][c]["files"][f]["source"]
                          #print("\n\n" + r + "/commit/" + c)
                          #print("    " + f)
                          
                          if len(sourcecode) > 14000:
                            continue
                          
                          allbadparts = []
                          
                          foundMeaningful = False
                          
                          for change in data[r][c]["files"][f]["changes"]:
                            badparts = change["badparts"]
                            
                            
                            if (len(badparts) < 20):
                              count = count + len(badparts)
                              for bad in badparts:
                                pos = utils.findposition(bad,sourcecode)
                                
                                if not -1 in pos:
                                
                                  if "print" in bad:
                                    o=1
                             #       print("print in there.")
                                  elif "import" in bad:
                                    o=1
                              #      print("import in there.")
                                  elif "def" in bad:
                                    o=1
                               #     print("def in there.")
                                  else:
                                    allbadparts.append(bad)
                                    #print(str(pos) + "   "  + bad.replace("\n"," ").lstrip())
                                
                            
                              
                        
                          if(len(allbadparts) > 0):
                            #print(str(len(allbadparts)) + " bad parts in source code of length " + str(len(sourcecode)))
                            if len(allbadparts) < 8:
                              positions = utils.findpositions(allbadparts,sourcecode)
                              blocks = utils.getblocks(sourcecode, positions, step,fulllength)
                              
                              for b in blocks:
                                  #print(b)
                                  allblocks.append(b)
                #          time.sleep(0.5)

                vulcount = 0
                for b in allblocks:
                  if b[1] == 0:
                    vulcount = vulcount + 1
                            
                print("badparts: " + str(count))
                print("step length: "  + str(step))
                print("full length: " + str(fulllength))
                print("Blocks: "+str(len(allblocks)))
                print("vulnerable blocks: " + str(vulcount))
                print("\n\n\n")


                keys = []

                for i in range(len(allblocks)):
                  keys.append(i)
                  


                random.shuffle(keys)


                cutoff = round(0.7 * len(keys))
                cutoff2 = round(0.85 * len(keys))


                keystrain = keys[:cutoff]
                keystest = keys[cutoff:cutoff2]
                keysfinaltest = keys[cutoff2:]

#                newcutoff = round(0.8 * len(keys))
#                keystrain = keys[:cutoff]
#                keystest = keys[cutoff:]




                TrainX = []
                TrainY = []
                ValidateX = []
                ValidateY = []
                FinaltestX = []
                FinaltestY = []


                      



                print("\nTraining\n")
                for k in keystrain:
                  block = allblocks[k]
                  
                  code = block[0]
                  #if block[1] == 0:
                  #  code = "if if if if if if if if if if if if if if if if if if if if if if if if if if if if if if if if if if"
                #    code = code[:10] + " if if if if if if if " + code[10:]
                  token = getTokens(code)
                  vectorlist = []
                  for t in token:
                    if t in word_vectors.vocab and t != " ":
                      vector = w2v_model[t]
                      vectorlist.append(vector.tolist()) 
                  TrainX.append(vectorlist)
                  TrainY.append(block[1])


                print("\nTest\n")
                for k in keystest:
                  block = allblocks[k]
                  code = block[0]
                  #if block[1] == 0:
                  #  code = "if if if if if if if if if if if if if if if if if if if if if if if if if if if if if if if if if if"
                  token = getTokens(code)
                  vectorlist = []
                  for t in token:
                    if t in word_vectors.vocab and t != " ":
                      vector = w2v_model[t]
                      vectorlist.append(vector.tolist()) 
                  ValidateX.append(vectorlist)
                  ValidateY.append(block[1])


                print("\nFinaltest\n")
                for k in keysfinaltest:
                  block = allblocks[k]  
                  code = block[0]
                # if block[1] == 0:
                #   code = "if if if if if if if if if if if if if if if if if if if if if if if if if if if if if if if if if if"
                  token = getTokens(code)
                  vectorlist = []
                  for t in token:
                    if t in word_vectors.vocab and t != " ":
                      vector = w2v_model[t]
                      vectorlist.append(vector.tolist()) 
                  FinaltestX.append(vectorlist)
                  FinaltestY.append(block[1])





                    
                print("Train length: " + str(len(TrainX)))
                print("Train length: " + str(len(TrainY)))
                print("Test length: " + str(len(ValidateX)))
                print("Test length: " + str(len(ValidateY)))
                print("Finaltesting length: " + str(len(FinaltestX)))
                print("Finaltesting length: " + str(len(FinaltestY)))


                #for index in range(3):
                #  print(TrainX[index])
                #  print(TrainY[index])
                #  print("\n")
                  
                  
                print("\n\n")



                with open('data/plain_' + mode + '_dataset-train-X_'+w2v + "__" + mode2, 'wb') as fp:
                  pickle.dump(TrainX, fp)
                with open('data/plain_' + mode + '_dataset-train-Y_'+w2v + "__" + mode2, 'wb') as fp:
                  pickle.dump(TrainY, fp)
                with open('data/plain_' + mode + '_dataset-validate-X_'+w2v + "__" + mode2, 'wb') as fp:
                  pickle.dump(ValidateX, fp)
                with open('data/plain_' + mode + '_dataset-validate-Y_'+w2v + "__" + mode2, 'wb') as fp:
                  pickle.dump(ValidateY, fp)
            #    with open('data/plain_' + mode + '_dataset-finaltest-X_'+w2v + "__" + mode2, 'wb') as fp:
            #      pickle.dump(FinaltestX, fp)
            #    with open('data/plain_' + mode + '_dataset-finaltest-Y_'+w2v  + "__" + mode2, 'wb') as fp:
            #      pickle.dump(FinaltestY, fp)
    
                       

  #              with open('data/plain_' + mode + '_dataset-train-X'+mode2+"_"+mode3, 'wb') as fp:
#                  pickle.dump(TrainX, fp)
 #               with open('data/plain_' + mode + '_dataset-train-Y'+mode2+"_"+mode3, 'wb') as fp:
 #                 pickle.dump(TrainY, fp)
#                with open('data/plain_' + mode + '_dataset-validate-X'+mode2+"_"+mode3, 'wb') as fp:
#                  pickle.dump(ValidateX, fp)
#                with open('data/plain_' + mode + '_dataset-validate-Y'+mode2+"_"+mode3, 'wb') as fp:
#                  pickle.dump(ValidateY, fp)
#                with open('data/plain_' + mode + '_dataset-finaltest-X'+mode2+"_"+mode3, 'wb') as fp:
#                  pickle.dump(FinaltestX, fp)
#                with open('data/plain_' + mode + '_dataset-finaltest-Y'+mode2+"_"+mode3, 'wb') as fp:
#                  pickle.dump(FinaltestY, fp)
    
