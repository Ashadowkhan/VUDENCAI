import json
import sys
from pydriller import RepositoryMining
import requests
import time
import requests
import sys
import json
import datetime

from gensim.models import Word2Vec, KeyedVectors
import numpy
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import LSTM
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.layers import Bidirectional
from keras.preprocessing import sequence
from tokenizer import tokenize
import builtins
import keyword
import pickle

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

from keras.models import load_model
from matplotlib import pyplot 

def improve(change):
  while ('"""') in change:
    position1 = change.find('"""')+1
    position2 = change[position1:].find('"""')+position1+4
    before = change[:position1]
    after = change[position2:]
    change = before+after
  while ("'''") in change:
    position1 = change.find("'''")+1
    position2 = change[position1:].find("'''")+position1+4
    before = change[:position1]
    after = change[position2:]
    change = before+after
  change = change.split("\n")
  withoutComments = ""
  therewasacomment = False
  for c in change:
    if "#" in c:
      therewasacomment = True
      position = c.find("#")
      c = c[:position]
    withoutComments = withoutComments + c + "\n"
  change = withoutComments
  return change

def getTokens(change):
  tokens = []  
  while ('"""') in change:
    position1 = change.find('"""')+1
    position2 = change[position1:].find('"""')+position1+4
    before = change[:position1]
    after = change[position2:]
    change = before+after
  while ("'''") in change:
    position1 = change.find("'''")+1
    position2 = change[position1:].find("'''")+position1+4
    before = change[:position1]
    after = change[position2:]
    change = before+after
  change = change.split("\n")
  withoutComments = ""
  therewasacomment = False
  for c in change:
    if "#" in c:
      therewasacomment = True
      position = c.find("#")
      c = c[:position]
    withoutComments = withoutComments + c + "\n"
  change = withoutComments
 # if therewasacomment:
 #   print(change)
 #   print("-------------")
 #   time.sleep(2)
  change = change.replace(" .",".")
  change = change.replace(" ,",",")
  change = change.replace(" )",")")
  change = change.replace(" (","(")
  change = change.replace(" ]","]")
  change = change.replace(" [","[")
  change = change.replace(" {","{")
  change = change.replace(" }","}")
  change = change.replace(" :",":")
  change = change.replace("- ","-")
  change = change.replace("+ ","+")
  change = change.replace(" =","=")
  change = change.replace("= ","=")
  splitchars = [" ","\t","\n", ".", ":", "(", ")", "[", "]", "<", ">", "+", "-", "=","\"", "\'","*", "/","\\","~","{","}","!","?","*",";",",","%","&"]
  start = 0
  end = 0
  for i in range(0, len(change)):
    if change[i] in splitchars:
      if i > start:
        start = start+1
        end = i
        if start == 1:
          token = change[:end]
        else:
          token = change[start:end]
        if len(token) > 0:
          tokens.append(token)
        tokens.append(change[i])
        start = i
  return(tokens)






#mode = "Self-X"
#mode = "Self-XVAR"
#mode = "Self-XwithoutStrings"
#mode = "interlaken"
mode = "sql"

model = load_model('LSTM-'+mode+'.h5')
print("finished loading lstm model LSTM-"+mode+".h5")



w2v_model = Word2Vec.load("word2vecinterlaken.model")
word_vectors = w2v_model.wv

print("finished loading w2v")


repos = []




#subset = ""
subset = "SUBSET-"
#subset = "BIG-SUBSET-"


myheaders = {'Authorization': 'token ' + '62b91a7aab880263d42d98159b3dcac407891972'}




with open('data/' + mode + '_dataset-validate-X', 'rb') as fp:
    X_test =  numpy.array(pickle.load(fp))

with open('data/' + mode + '_dataset-validate-Y', 'rb') as fp:
    y_test = numpy.array(pickle.load(fp))

with open('finaltestset-'+mode+'.json', 'r') as infile:
    finaltestset = json.load(infile)


with open('data/' + mode+'-onlyWithRepSuccess', 'r') as infile:
    data = json.load(infile)
    
pythontraining = ""

print("loaded data")



repositorycounter = {}

if (False):
  for r in data:
    for c in data[r]:
      if "sql" in data[r][c]["keyword"]:
        if not r in repositorycounter:
          repositorycounter[r] = 0
        repositorycounter[r] = repositorycounter[r]+1
     # else:
     #   print("??")
     #   sys.exit()
  a= sorted(repositorycounter.items(), key = lambda x : x[1])
  #print(a[-20:])
  #print("\n\n")
  #print(a[:20])

  b = a[-20:]
  print(b)
  l = []
  for x in b:
    l.append(x[0])

  print(l)




if(False):
    print(len(X_test))

    falsePos = 0
    falseNeg = 0
    truePos = 0
    trueNeg = 0


    for ix in range(0,len(X_test)):
      


      one = []
      one.append(X_test[ix])
      one = numpy.array(one)      
      max_length = 200
      one = sequence.pad_sequences(one, maxlen=max_length)
      try:
        yhat_probs = model.predict(one, verbose=0)
        yhat_classes = model.predict_classes(one, verbose=0)
        
      #  print (str(y_test[ix]) + " " + str(float(0.01* (int(yhat_probs[0][0]*100)))))
        
        if (y_test[ix] == 0):
          #vulnerable
          if yhat_probs[0][0] < 0.5:
            truePos = truePos + 1
          else:
            falseNeg = falseNeg + 1
        else:
          if yhat_probs[0][0] < 0.5:
            falsePos = falsePos +1
          else:
            trueNeg = trueNeg + 1
      except:
        continue
      

    print("50")
    print("true pos: " + str(truePos))
    print("false pos: " + str(falsePos))
    print("true neg: " + str(trueNeg))
    print("false neg: " + str(falseNeg))
    print("\n\n")
    
    print("Accuracy: " + str(100 * (truePos + trueNeg)/(truePos + trueNeg + falsePos + falseNeg)))
    
    precision = truePos / (truePos + falsePos)
    recall = truePos / (truePos + falseNeg)
    
    print("Precision: " + str(100 * precision))
    print("Recall: " + str(100 * recall))
    
    print("F1: " + str(100 * 2 * (precision * recall) / (precision + recall)))
        
    print("\n\n")

if(True):
  
  falsePos = 0
  falseNeg = 0
  truePos = 0
  trueNeg = 0
  
  for r in data:
    
    if(trueNeg > 0):

      print("true pos: " + str(truePos))
      print("false pos: " + str(falsePos))
      print("true neg: " + str(trueNeg))
      print("false neg: " + str(falseNeg))
      print("\n\n")
      
      print("Accuracy: " + str(100 * (truePos + trueNeg)/(truePos + trueNeg + falsePos + falseNeg)))
      
      precision = truePos / (truePos + falsePos)
      recall = truePos / (truePos + falseNeg)
      
      print("Precision: " + str(100 * precision))
      print("Recall: " + str(100 * recall))
      
      print("F1: " + str(100 * 2 * (precision * recall) / (precision + recall)))
          
      print("\n\n") 

    for c in data[r]:
      allchanges = []
      for change in data[r][c]["changes"]:
        p = change["previous"]
        p = p.replace("\n"," ")
        p = p.replace("\t"," ")
        p = p.lower()          
        while("  " in p):
          p = p.replace("  "," ")
        p = p[2:-2]
        allchanges.append(p)
        
    
      print("\n\n" + r + "/commit/" + c)
      #print(str(len(allchanges)) + " changes.")
      for commit in RepositoryMining(r).traverse_commits():
        if (commit.hash == c):
          #print("This is the commit.")
          
          
          for mod in commit.modifications:
            #print("modification")
            sourcecode = mod.source_code_before
            if sourcecode is not None:
                sourcecode = sourcecode.lower()
                sourcecode = sourcecode.replace("\n"," ")
                sourcecode = sourcecode.replace("\t", " ")
                while("  " in sourcecode):
                  sourcecode = sourcecode.replace("  ", " ")
            
                
                sourcecodeclean = sourcecode
                
                positions = []
                
                for ac in allchanges:
                  
                  if ac in sourcecodeclean:
                    pos = sourcecodeclean.find(ac)
                #    print("here " + str(pos))
                    position = []
                    position.append(pos)
                    position.append(pos+len(ac))
                    positions.append(position)
                #  else:
                #    print("not here")
                #    print(ac)
                #    print("\n\n")
                #    print(sourcecode)

                x = 0


                while(x < len(sourcecode)):
                    
                    
                  y = min(x+200, len(sourcecode))
                  
                  jud = str(x) + ":" + str(y) + "   "
                  
                  for p in positions:
                    if p[0] > x and p[0] < y:
                      y = p[0]
                    
                  window = sourcecode[x:y]
                  
                  vectorlist = []
                  token = getTokens(window)
                
                  for t in token:
                    if t in word_vectors.vocab and t != " ":
                      vector = w2v_model[t]
                      vectorlist.append(vector)
                
                  
                  if (len(vectorlist) > 10):
                    
                    one = []
                    one.append(vectorlist)
                    one = numpy.array(one)
                    max_length = 200
                    one = sequence.pad_sequences(one, maxlen=max_length)

                    yhat_probs = model.predict(one, verbose=0)
                    yhat_classes = model.predict_classes(one, verbose=0)
                    
                    if (yhat_probs[0][0] < 0.2):
                      falsePos = falsePos + 1
                      #jud = jud + " False Positive! " + str(yhat_probs[0][0])
                    else:
                      trueNeg = trueNeg + 1
                      #jud = jud + " "

                    
                    print(jud)

                    y = min(x+200, len(sourcecode))
                    for p in positions:
                      if p[0] < y and p[0] > x:
                        x = p[0]
                        y = p[1]
                        window = sourcecode[x:y]
                        vectorlist = []
                        token = getTokens(window)
                        for t in token:
                          if t in word_vectors.vocab and t != " ":
                            vector = w2v_model[t]
                            vectorlist.append(vector)

                        if(len(vectorlist) > 10):
                          one = []
                          one.append(vectorlist)
                          one = numpy.array(one)
                          max_length = 200
                          one = sequence.pad_sequences(one, maxlen=max_length)

                          yhat_probs = model.predict(one, verbose=0)
                          yhat_classes = model.predict_classes(one, verbose=0)

                          if (yhat_probs[0][0] < 0.2):
                            print("Found Vulnerability! True Positive. "  + str(yhat_probs[0][0]))
                            truePos = truePos + 1
                          else:
                            print("Missed Vulnerabilty :( False Negative. "  + str(yhat_probs[0][0]))
                            falseNeg = falseNeg + 1
                        x = p[1]

                  goon = 200
                  for g in range(200,400):
                    if g > len(window)-1:
                      goon = len(window)
                      break
                    if window[g] == ' ':
                      goon = g
                      break
                  
                  #print(goon)
                  x = x + goon
                  #print("new x: " + str(x))
                  
                

        

  #==================================================================





                
                
                
                
                
                
                
                
                
                
                
                
                















if (False):
  
  averageTruePositive = 0
  averageFalsePositive = 0
  averageTrueNegative = 0
  averageFalseNegative = 0

  numberTruePositive = 0
  numberFalsePositive = 0
  numberTrueNegative = 0
  numberFalseNegative = 0




  index = 0
  print(len(origVectorlist))
  for index in range(0,len(origVectorlist)):
    index = index+1
    try:
      one = []
      vector = origVectorlist[index]
      one.append(vector)
      one = numpy.array(one)      
      max_length = 200
      one = sequence.pad_sequences(one, maxlen=max_length)
      yhat_probs = model.predict(one, verbose=0)
      yhat_classes = model.predict_classes(one, verbose=0)
      
      if (int(yhat_classes[0][0]) == int(origValue[index])):
        if (int(origValue[index] == 0)):
          #True positive
          numberTruePositive = numberTruePositive + 1
          averageTruePositive = averageTruePositive + yhat_probs[0][0]
        if (int(origValue[index] == 1)):
          #True negative
          numberTrueNegative = numberTrueNegative + 1
          averageTrueNegative = averageTrueNegative + yhat_probs[0][0]
          
        print("correct!")
      if (int(yhat_classes[0][0]) != int(origValue[index])):
        if (origValue[index] == 0 and int(yhat_classes[0][0]) == 1):
          print("incorrect... it's a false negative / missed bug. " + str(yhat_probs))
          #False Negative
          numberFalseNegative = numberFalseNegative + 1
          averageFalseNegative = averageFalseNegative + yhat_probs[0][0]
        if (origValue[index] == 1 and int(yhat_classes[0][0]) == 0):
          print("incorrect... it's a false positive. " + str(yhat_probs))
          numberFalsePositive = numberFalsePositive + 1
          averageFalsePositive = averageFalsePositive + yhat_probs[0][0]
        #print(origKey[index])
        #print(''.join(origPre[index]))
        #print("\n\n")
        
          
    except Exception as e:
      print(e)


  print("True Positive: " + str(numberTruePositive) + " " + str( averageTruePositive / numberTruePositive  ))
  print("True Negative: " + str(numberTrueNegative) + " " + str ( averageTrueNegative / numberTrueNegative  ))
  print("False Positive: " + str(numberFalsePositive) + " " + str ( averageFalsePositive / numberFalsePositive  ))
  print("False Negative: " + str(numberFalseNegative) + " " + str ( averageFalseNegative / numberFalseNegative  ))



