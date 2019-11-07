

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




def findposition(badpart,sourcecode):
  splitchars = ["\t", "\n", " ", ".", ":", "(", ")", "[", "]", "<", ">", "+", "-", "=","\"", "\'","*", "/","\\","~","{","}","!","?","*",";",",","%","&"]
  pos = 0
  matchindex = 0
  inacomment = False
  bigcomment = False
  bigcomment2 = False
  startfound = -1
  endfound = -1
  position = []
  end = False
  last = 0
  
  while(not end):
    #print("position : " + str(pos))
    
    if not inacomment:
      last = pos-1
    
    if pos >= len(sourcecode):
      end = True
      break
    
    if sourcecode[pos] == "\n":
 #     print("end of comment")
 #     print("[" + sourcecode[last]+ "]")
      inacomment = False
      
    if sourcecode[pos] == "\n" and (sourcecode[pos-1] == "\n" or sourcecode[last] == " "):
      #print("one further")
      pos = pos +1
      continue
      
    if sourcecode[pos] == " " and (sourcecode[pos-1] == " " or sourcecode[last] == "\n"):
     # print("one further")
      pos = pos +1
      continue
      
    if sourcecode[pos] == "#":
      
      inacomment = True
      

#    if sourcecode[pos] == "'":      
#      if pos+2 < len(sourcecode):
#        if sourcecode[pos+1] == "'" and sourcecode[pos+2] == "'":
#          if not bigcomment:
#            pos = pos+3
#            bigcomment = True
#        #    print(">>> BIGCOMMENT")
#            continue
#          else:
#            pos = pos+3
#            bigcomment = False
#         #   print(">>> BIGCOMMENT END")
#            continue

#    if sourcecode[pos] == '"':      
#      if pos+2 < len(sourcecode):
#        if sourcecode[pos+1] == '"' and sourcecode[pos+2] == '"':
#          if not bigcomment2:
#            pos = pos+3
#            bigcomment2 = True
#          #  print(">>> BIGCOMMENT")
#            continue
#          else:
#            pos = pos+3
#            bigcomment2 = False
#           # print(">>> BIGCOMMENT END")
#            continue
      
    if (False):
      
                      print("---------------------------------")
                      string1 = ""
                      string2 = ""
                      for i in range(0,pos):
                        string1 = string1 + sourcecode[i]

                      for i in range(pos+1,len(sourcecode)):
                        string2 = string2 + sourcecode[i]
                        
                      print(string1 + "[" + sourcecode[pos] + "]" + string2)
                      print("---------------------------------")


                      string1 = ""
                      string2 = ""
                      
                      for i in range(0,matchindex):
                        string1 = string1 + badpart[i]

                      for i in range(matchindex+1,len(badpart)):
                        string2 = string2 + badpart[i]
                        
                      print(string1 + "[" + badpart[matchindex] + "]" + string2)
  
                      print("---------------------------------")
                

    if not inacomment: # and not bigcomment and not bigcomment2:
      a = sourcecode[pos]
      if a == "\n":
        a = " "
      b = badpart[matchindex]
      
      c = ""
      if matchindex > 0:
        c = badpart[matchindex-1]
      
      d = ""
      if matchindex < len(badpart)-2:
        d = badpart[matchindex+1]
        
      if (a != b) and (a == " " or a == "\n") and ((b in splitchars) or (c in splitchars)):
        pos = pos+1
        continue
      
      if (a != b) and (b == " " or b == "\n"):
        #print("here")
        if (c in splitchars or d in splitchars):
          #print("here2")
          if (matchindex < len(badpart)-1):
            matchindex = matchindex + 1
            continue
        
      if a == b:
          if matchindex == 0:
            startfound = pos
         # print("\n>>match: " + badpart[matchindex] + "(" + str(matchindex) + "/" + str(len(badpart)) + ")\n\n")
          matchindex = matchindex + 1
          
      else:
          #print("\n>>no match" )
          matchindex = 0
          startfound = -1
        
      if matchindex == len(badpart):
        endfound = pos
    #    print("FOUND at pos "+ str(startfound) + ":" + str(endfound))
        break
        
    if pos == len(sourcecode):
      end = True
    pos = pos + 1
  
  position.append(startfound)
  position.append(endfound)
  
  if endfound < 0:
    startfound = -1
    
  if endfound < 0 and startfound < 0: #and not "#" in badpart and not '"""' in badpart and not "'''" in badpart:
#    print(sourcecode)
#    print(":::::::::::")
#    print(badpart)
#    print("-----------------")
    return[-1,-1]
  return position








def findpositions(badparts,sourcecode):
  
  positions = []
  
  
  for bad in badparts:
    
    if "#" in bad:
      find = bad.find("#")
      bad = bad[:find]
      
    place = findposition(bad,sourcecode)
    if place != [-1,-1]:
      positions.append(place)
    
    
  return positions
  

  


def stripComments(code):
    
  withoutComments = ""
  lines = code.split("\n")
  withoutComments = ""
  therewasacomment = False
  for c in lines:
    if "#" in c:
      therewasacomment = True
      position = c.find("#")
      c = c[:position]
    withoutComments = withoutComments + c + "\n"
  
  
  change = withoutComments
   
    
#  while ('r"""') in change:
#    position1 = change.find('"""')
#    before = change[:position1]
#    if change[position1+4:].find('"""') == -1:
#      change = before  
#    else:
#      position2 = change[position1+4:].find('"""')+position1+8
#      after = change[position2:]
#      change = before+after
  
#  while ('"""') in change:
#    position1 = change.find('"""')
#    before = change[:position1]
#    if change[position1+3:].find('"""') == -1:
#      change = before  
#    else:
#      position2 = change[position1+3:].find('"""')+position1+7
#      after = change[position2:]
#      change = before+after
#    
#  while ("'''") in change:
#    position1 = change.find("'''")
#    before = change[:position1]
#    if change[position1+3:].find("'''") == -1:
#      change = before  
#    else:
#      position2 = change[position1+3:].find("'''")+position1+7
#      after = change[position2:]
#      change = before+after
  
  withoutComments = change

  return withoutComments




  
def getTokens(change):
  tokens = []  
  
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
  




def getBadpart(change):
  
  #print("\n")
  removal = False
  lines = change.split("\n")
  
#  if (len(lines) > 10 and len(change) > 800):
   # print("tooo long")
#    return None
  
  
  
  for l in lines:
    if len(l) > 0:
      if l[0] == "-":
        #print("a line is removed")
        removal = True
      
  
  if not removal:
    #print("There is no removal.")
    return None
  
  
  
 # print(change)
 # time.sleep(5)
  
  pairs = []
  
  badexamples = []
  goodexamples = []

  for l in range(len(lines)):
    
    line = lines[l]
    line = line.lstrip()
    if len(line.replace(" ","")) > 1:
        if line[0] == "-":
          if not "#" in line[1:].lstrip()[:3] and not "import os" in line:
            badexamples.append(line[1:])
        if line[0] == "+":
          if not "#" in line[1:].lstrip()[:3] and not "import os" in line:
            goodexamples.append(line[1:])
    
  if len(badexamples) == 0:
#    print("removed lines were empty or comments")
    return None
  
  return [badexamples,goodexamples]
    
  

  
def isEmpty(code):
  token = getTokens(stripComments(code))
  for t in token:
    if (t != "\n" and t != " "):
      return False
  return True

def is_builtin(name):
    return name in builtins.__dict__
def is_keyword(name):
      return name in keyword.kwlist



def nextsplit(sourcecode,focus):
  splitchars = [" ","\t","\n", ".", ":", "(", ")", "[", "]", "<", ">", "+", "-", "=","\"", "\'","*", "/","\\","~","{","}","!","?","*",";",",","%","&"]
  for pos in range(focus+1, len(sourcecode)):
      if sourcecode[pos] in splitchars:
        return pos
  return -1

def previoussplit(sourcecode,focus):
  splitchars = [" ","\t","\n", ".", ":", "(", ")", "[", "]", "<", ">", "+", "-", "=","\"", "\'","*", "/","\\","~","{","}","!","?","*",";",",","%","&"]
  pos = focus-1
  while(pos >= 0):
      if sourcecode[pos] in splitchars:
        return pos
      pos = pos-1
  return -1

def getcontextPos(sourcecode,focus,fulllength):

  
  startcontext = focus
  endcontext = focus
  if focus > len(sourcecode)-1:
    return None

  start = True
  
      
  while not len(sourcecode[startcontext:endcontext]) > fulllength:
   # print(str(startcontext) + ":" + str(endcontext))
   # print(len(sourcecode[startcontext:endcontext]))
    
    if previoussplit(sourcecode,startcontext) == -1 and nextsplit(sourcecode,endcontext) == -1:
   #   print("NONE!")
      return None
    
    if start:
      if previoussplit(sourcecode,startcontext) > -1:
        startcontext = previoussplit(sourcecode,startcontext)
      #print("new start: " + str(startcontext))
      start = False
    else:
      if nextsplit(sourcecode,endcontext) > -1:
        endcontext = nextsplit(sourcecode,endcontext)
      #print("new end: " + str(endcontext))
      start = True

        
#  print("focus: " + str(focus))
#  print("start: " + str(startcontext))
#  print("end: " + str(endcontext))
  return [startcontext,endcontext]

def getcontext(sourcecode,focus,fulllength):

  
  startcontext = focus
  endcontext = focus
  if focus > len(sourcecode)-1:
    return None

  start = True
  
      
  while not len(sourcecode[startcontext:endcontext]) > fulllength:
   # print(str(startcontext) + ":" + str(endcontext))
   # print(len(sourcecode[startcontext:endcontext]))
    
    if previoussplit(sourcecode,startcontext) == -1 and nextsplit(sourcecode,endcontext) == -1:
   #   print("NONE!")
      return None
    
    if start:
      if previoussplit(sourcecode,startcontext) > -1:
        startcontext = previoussplit(sourcecode,startcontext)
      #print("new start: " + str(startcontext))
      start = False
    else:
      if nextsplit(sourcecode,endcontext) > -1:
        endcontext = nextsplit(sourcecode,endcontext)
      #print("new end: " + str(endcontext))
      start = True

        
#  print("focus: " + str(focus))
#  print("start: " + str(startcontext))
#  print("end: " + str(endcontext))
  return sourcecode[startcontext:endcontext]
  
def getgoodblocks(sourcecode,goodpositions,fullength):
  blocks = []
  if (len(goodpositions) > 0):
    for g in goodpositions:
     # print("g " + str(g))
      if g != []:
        focus = g[0]
        while (True):
          if focus >= g[1]:
            #print("  too far.")
            break

    #        print("Focus is on " + str(focus) + " " + sourcecode[focus])
            
          
          context = getcontext(sourcecode,focus,fulllength)
          
          if context is not None:
            singleblock = []
            singleblock.append(context)
            singleblock.append(1)
              
            already = False
            for b in blocks:
              if b[0] == singleblock[0]:
              #  print("already.")
                already = True
                  
            if not already:
              blocks.append(singleblock)
              
              
            if nextsplit(sourcecode,focus+15) > -1:
              focus = nextsplit(sourcecode,focus+15)
            else:
              break
      
#  if len(blocks) > 0:
#    print(blocks)
  return blocks



def getblocks(sourcecode, badpositions, fulllength):
      blocks = []
       
      focus = 0
      lastfocus = 0
      while (True):
        if focus > len(sourcecode):
          break
        
        focusarea = sourcecode[lastfocus:focus]
                
        if not (focusarea == "\n"):
              
            middle = lastfocus+round(0.5*(focus-lastfocus))              
            context = getcontextPos(sourcecode,middle,fulllength)
            #print([lastfocus,focus,len(sourcecode)])
            
            
            if context is not None:
              
              
                
              vulnerablePos = False
              for bad in badpositions:
                    
                  if (context[0] > bad[0] and context[0] <= bad[1]) or (context[1] > bad[0] and context[1] <= bad[1]) or (context[0] <= bad[0] and context[1] >= bad[1]):
                    vulnerablePos = True
            
                  
              q = -1
              if vulnerablePos:
                q = 0
              else:
                q = 1
              
              
              singleblock = []
              singleblock.append(sourcecode[context[0]:context[1]])
              singleblock.append(q)
                
              already = False
              for b in blocks:
                if b[0] == singleblock[0]:
                #  print("already.")
                  already = True
                  
              if not already:
                blocks.append(singleblock)


        if ("\n" in sourcecode[focus+1:focus+7]):
          lastfocus = focus
          focus = focus + sourcecode[focus+1:focus+7].find("\n")+1
        else:
          if nextsplit(sourcecode,focus+step) > -1:
            lastfocus = focus
            focus = nextsplit(sourcecode,focus+step)
          else:
            if focus < len(sourcecode):
              lastfocus = focus
              focus = len(sourcecode)
            else:
              break

      
      return blocks


  
  

#===========================================================================



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
  for mincount in [10,30,50,100,300,500,5000]:
    for iterationen in [1,5,10,30,50,100,500]:
    #for iterationen in [1,10,100,30]:
  #    for s in [5,10,15,30,50,75,100,200,300]:
      for s in [200]:
        for w in ["withoutString","withString"]:



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
                                pos = findposition(bad,sourcecode)
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
                              positions = findpositions(allbadparts,sourcecode)
                              blocks = getblocks(sourcecode, positions, fulllength)
                              
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
                with open('data/plain_' + mode + '_dataset-finaltest-X_'+w2v + "__" + mode2, 'wb') as fp:
                  pickle.dump(FinaltestX, fp)
                with open('data/plain_' + mode + '_dataset-finaltest-Y_'+w2v  + "__" + mode2, 'wb') as fp:
                  pickle.dump(FinaltestY, fp)
    
                       

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
    
