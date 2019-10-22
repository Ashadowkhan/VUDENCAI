

import json
import numpy
import pickle
from pydriller import RepositoryMining
from gensim.models import Word2Vec, KeyedVectors
from keras.preprocessing import sequence
from keras.models import load_model
import sys
import time


def findpositions(badparts,sourcecode):
  
  positions = []
  
  for bad in badparts:
    place = findposition(bad,sourcecode)
    positions.append(place)
#    if -1 in place:
#      print(sourcecode)
#      print("-------------------------")
#      print(bad)
#      sys.exit()
    
    
  return positions
  
  
def findcomments(sourcecode):
  
  commentareas = []
  
  inacomment = False
  bigcomment = False
  bigcomment2 = False
  commentstart = -1
  commentend = -1
  bigcommentstart = -1
  bigcommentend = -1
  bigcomment2start = -1
  bigcomment2end = -1
  
  
  for pos in range(len(sourcecode)):
    
    if sourcecode[pos] == "#":
      if not inacomment:
        commentstart = pos 
        inacomment = True
    
    if sourcecode[pos] == "\n":
      if inacomment:
        commentend = pos
        inacomment = False
  
    if commentstart > 0 and commentend > 0:
      t = [commentstart, commentend]
      commentareas.append(t)
      commentstart = -1
      commentend = -1

    if sourcecode[pos] == "'":      
      if pos < len(sourcecode) + 2:
        if sourcecode[pos+1] == "'" and sourcecode[pos+2] == "'":
          if not bigcomment:
            bigcomment = True
            bigcommentstart = pos 
          else:
            bigcomment = False
            bigcommentend = pos
    if bigcommentstart > 0 and bigcommentend > 0:
      t = [bigcommentstart, bigcommentend]
      commentareas.append(t)
      bigcommentstart = -1
      bigcommentend = -1

    if sourcecode[pos] == '"':      
      if pos < len(sourcecode) + 2:
        if sourcecode[pos+1] == '"' and sourcecode[pos+2] == '"':
          if not bigcomment2:
            bigcomment2 = True
            bigcomment2start = pos 
          else:
            bigcomment2 = False
            bigcommend2end = pos
    if bigcomment2start > 0 and bigcomment2end > 0:
      t = [bigcomment2start, bigcomment2end]
      commentareas.append(t)
      bigcomment2start = -1
      bigcomment2end = -1

      
  return commentareas









def findposition(badpart,sourcecode):
  pos = 0
  matchindex = 0
  inacomment = False
  bigcomment = False
  bigcomment2 = False
  startfound = -1
  endfound = -1
  position = []
  end = False
  
  while(not end):


    if sourcecode[pos] == "\n":
      inacomment = False
      
    if sourcecode[pos] == "\n" and (sourcecode[pos-1] == "\n" or sourcecode[pos-1] == " "):
      pos = pos +1
      continue
      
    if sourcecode[pos] == " " and (sourcecode[pos-1] == " " or sourcecode[pos-1] == "\n"):
      pos = pos +1
      continue
      
    if sourcecode[pos] == "#":
      inacomment = True
    

    if sourcecode[pos] == "'":      
      if pos < len(sourcecode) + 2:
        if sourcecode[pos+1] == "'" and sourcecode[pos+2] == "'":
          if not bigcomment:
            pos = pos+3
            bigcomment = True
        #    print(">>> BIGCOMMENT")
            continue
          else:
            pos = pos+3
            bigcomment = False
         #   print(">>> BIGCOMMENT END")
            continue

    if sourcecode[pos] == '"':      
      if pos < len(sourcecode) + 2:
        if sourcecode[pos+1] == '"' and sourcecode[pos+2] == '"':
          if not bigcomment2:
            pos = pos+3
            bigcomment2 = True
          #  print(">>> BIGCOMMENT")
            continue
          else:
            pos = pos+3
            bigcomment2 = False
           # print(">>> BIGCOMMENT END")
            continue
      
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
  

    if not inacomment and not bigcomment and not bigcomment2:
      a = sourcecode[pos]
      if a == "\n":
        a = " "
      b = badpart[matchindex]
      
      if a == b:
          if matchindex == 0:
            startfound = pos
         # print("\n>>match: " + badpart[matchindex] + "(" + str(matchindex) + "/" + str(len(badpart)) + ")\n\n")
          matchindex = matchindex + 1
          
      else:
          matchindex = 0
          startfound = -1
          #print("\n>>no match\n\n")
          
      if matchindex == len(badpart):
        endfound = pos
        #print("FOUND at pos "+ str(startfound) + ":" + str(endfound))
        break
        
    pos = pos + 1
    if pos == len(sourcecode):
      end = True
  
  position.append(startfound)
  position.append(endfound)
  return position

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
   
    
  while ('r"""') in change:
    position1 = change.find('"""')
    before = change[:position1]
    if change[position1+4:].find('"""') == -1:
      change = before  
    else:
      position2 = change[position1+4:].find('"""')+position1+8
      after = change[position2:]
      change = before+after
  
  while ('"""') in change:
    position1 = change.find('"""')
    before = change[:position1]
    if change[position1+3:].find('"""') == -1:
      change = before  
    else:
      position2 = change[position1+3:].find('"""')+position1+7
      after = change[position2:]
      change = before+after
    
  while ("'''") in change:
    position1 = change.find("'''")
    before = change[:position1]
    if change[position1+3:].find("'''") == -1:
      change = before  
    else:
      position2 = change[position1+3:].find("'''")+position1+7
      after = change[position2:]
      change = before+after
  
  withoutComments = change

  return withoutComments










def removeDoubleSeperators(tokenlist):
    last = ""
    newtokens = []
    for token in tokenlist:
      if token == "\n":
        token = " "
      if len(token) > 0:
        if ((last == " ") and (token == " ")):
          o = 1 #noop
          #print("too many \\n.")
        else:
          newtokens.append(token)
          
        last = token
        
    return(newtokens)



def removeDoubleSeperatorsString(string):
  return ("".join(removeDoubleSeperators(getTokens(string))))





def getwords(sourcecode):
  
  splitchars = [" ","\t","\n", ".", ":", "(", ")", "[", "]", "<", ">", "+", "-", "=","\"", "\'","*", "/","\\","~","{","}","!","?","*",";",",","%","&"]
  
  words = []
  word = ""
  
  for char in sourcecode:
    if char in splitchars:
      if len(word) > 0:
        words.append(word)
      words.append(char)
      word = ""
    else:
      word = word + char
  
  words.append(word)
  
  return(words)


def predict(context): 
  
  
  
  vectorlist = []
  for t in context:
      if t in word_vectors.vocab and t != " ":
        vector = w2v_model[t]
        vectorlist.append(vector)
        
  if (len(vectorlist) > 0):
    one = []
    one.append(vectorlist)
    one = numpy.array(one)
    max_length = 200
    one = sequence.pad_sequences(one, maxlen=max_length)
    yhat_probs = model.predict(one, verbose=0)
    prediction = int(yhat_probs[0][0] * 100000)
    prediction = 0.00001 * prediction 
    print(prediction)
    return prediction
  else:
    return -1




def getcontext(sourcecode,focus):
  
  splitchars = [" ","\t","\n", ".", ":", "(", ")", "[", "]", "<", ">", "+", "-", "=","\"", "\'","*", "/","\\","~","{","}","!","?","*",";",",","%","&"]
  startcontext = max(1,focus-20)
  endcontext = min(len(sourcecode)-1,focus+20)
  
  while(True):
    if startcontext >= focus:
      return None
    if not sourcecode[startcontext-1] in splitchars:
      startcontext = startcontext +1
    else:
      break
    
  while(True):
    if endcontext >= len(sourcecode):
      return None
    if not sourcecode[endcontext] in splitchars:
      endcontext = endcontext + 1
    else:
      break

  return sourcecode[startcontext:endcontext]
      
    
  




#==============================================


sourcecode = """ a
#b c
d e
#f g
ere asd
# sd # 
# sdsd
erer e """

print(findcomments(sourcecode))




sys.exit()



mode = "command_injection"
modelw2v = "word2vecinterlaken.model"

if (len(sys.argv) > 1):
  mode = sys.argv[1]
  if (len(sys.argv) > 2):
    modelw2v = sys.argv[2]
    
model = load_model('LSTM-'+mode+'-Dup.h5')

w2v_model = Word2Vec.load(modelw2v)
word_vectors = w2v_model.wv



print("\n\n\n")
print("finished loading lstm model LSTM-"+mode + "-Dup.h5")
print("finished loading w2v model " + modelw2v)



with open('data3/finaltestset-'+mode, 'r') as infile:
    datafinal = json.load(infile)

print("loaded data.")

cutoff = 0.5




for x in datafinal:

  
  for r in datafinal[x]:    
    print(r)
      
    for c in datafinal[x][r]:

              if not "changes" in datafinal[x][r][c]:
                print("  no changes, continue")
                sys.exit()
                continue
              
                
              ### writing down the files and their code

            
              for change in datafinal[x][r][c]["changes"]:
                
                print(change["filename"])
                
                notthischange = False
                
                for commit in RepositoryMining(r).traverse_commits():
                  if notthischange:
                    continue
                  
                  if commit.hash == c:
                    found = True
                    print("  found the commit " + c)

                    for m in commit.modifications:
                      if notthischange:
                        break

                      if m.old_path == change["filename"]:
                        print("     found the change.")
                        sourcecode = m.source_code_before
                        
                        badparts = []
                        for filename in datafinal[x][r][c]["badparts_just"]:
                          if filename == change["filename"]:
                            badparts = datafinal[x][r][c]["badparts_just"][filename]

                        positions = findpositions(badparts,sourcecode)
                        
                        for p in positions:
                          if -1 in p:
                            notthischange = True
                            break
                        
                        
                        focus = 0
                          
                        splitchars = [" ","\t","\n", ".", ":", "(", ")", "[", "]", "<", ">", "+", "-", "=","\"", "\'","*", "/","\\","~","{","}","!","?","*",";",",","%","&"]
                        
                          
                        commentareas = findComments(sourcecode)
                        while (True):
                          
                          comment = False
                          for area in commentareas:
                            if focus > area[0] and focus < area[1]:
                              comment = True
                              break
                              #it's in a comment
                              
                          if comment:
                            focus = focus+1
                            continue
                          
                          while not sourcecode[focus] in splitchars:
                            focus = focus + 1
                            
                          print(str(focus) + "   " + sourcecode[focus:focus+9])
                          #do something
                          
                          focus = focus + 1
                          
                          if focus >= len(sourcecode) - 10:
                            break
                          
                          context = getcontext(sourcecode,focus)

                          
                          print("-----------------------------")
                          print("\n\n\n")
                          print(context)
                          


                          print("\n\n\n")

#                          if context is not None:
#                            print(predict(context))
#                            
                sys.exit()
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                        
                        
                        
                        
                
                
                

                  
                  
                  
              
              
              
              
              
              
              
              
              
              
