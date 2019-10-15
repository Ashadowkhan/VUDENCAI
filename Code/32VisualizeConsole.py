from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import json
import numpy
import pickle
import sys
from pydriller import RepositoryMining
from gensim.models import Word2Vec, KeyedVectors
from keras.preprocessing import sequence
from keras.models import load_model
import time
from termcolor import colored

def findSnippet(lines, bad):
#  print("\n")
#  print(len(lines))
#  print(len(bad))
  
  startpos = 0
  for lindex in range(0,len(lines)):
      if lines[lindex].lstrip() == bad[0].lstrip():
        startpos = lindex
        for bindex in range(0,len(bad)):
          if (lindex+bindex > len(lines)-1):
            startpos = 0
            break
          if (len(bad[bindex].lstrip()) > 0):             
            if lines[lindex+bindex].lstrip() != bad[bindex].lstrip():
              startpos = 0
  return startpos



def getWindow(lines, lnr):
  window = ""
  start = max(0, lnr-5)
  end = min(len(lines)-1, lnr+5)
  if start < end:
    for x in range(start, end):
      window = window + lines[x] + "\n"
  return window



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

def predict(tokens):
  vectorlist = []
  for t in tokens:
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
    yhat_classes = model.predict_classes(one, verbose=0)
    return yhat_probs[0][0]














thegoodstuff = ""

mode = "full"
model = load_model('LSTM-'+mode+'.h5')
w2v_model = Word2Vec.load("word2vecinterlaken.model")
word_vectors = w2v_model.wv

with open('data2/' + "full" + '-onlyWithRepSuccess', 'r') as infile:
    data = json.load(infile)

count = 0    

skipahead = True

for r in data:

 # print(r)
 # if "Aalto-LeTech" in r:
 #   skipahead = False

 # if skipahead:
 #   continue
  
  
    
 # print(r)
  name = r.split("https://github.com/")[1]
  name = name.replace("/","-")
  
  for c in data[r]:
    #print(c)
    
    
  #  if ("sql" in data[r][c]["keyword"]):
      #print("skip sql")
  #    continue
    changenr = 0
    
    changedparts = {}
    files = {}
    
    for change in data[r][c]["changes"]:
      if not "sourcecode" in change:
        continue
      changenr = changenr + 1
      
      #print(change["filename"])
      f = change["filename"]
      
      if f not in changedparts:
        changedparts[f] = []
      
      bad = change["previous"].split("\n")
      lines = change["sourcecode"].split("\n")
            
      snippet = findSnippet(lines,bad)
      
      
      #print("Snippet: " +str(snippet))
      #print("Len bad: " + str(len(bad)))
      startandend = []
      startandend.append(snippet)
      startandend.append(len(bad))
      changedparts[f].append(startandend)
      
      files[f] = lines
      
    if (len(files) > 2):
      print("too many files")
      continue
    for f in files:
      
     # print("\n")
     # print(f)
      #print(changedparts)
      #ypos = 10
      #img = Image.new('RGB', (1000, 10000))
      
      
      lines = files[f]
      
      #print("len lines: " + str(len(lines)))
      if (len(lines) > 350):
        print(" a little to long")
        continue
      
      redcount = 0
      bluecount = 0
      greencount = 0
      for lnr in range(0, len(lines)):
        window = getWindow(lines, lnr)
        tokens = getTokens(window)
        
        prediction = predict(tokens)
        
        
        #print(window)
        #print(name + " " + c + " " + str(changenr) + " " + str(lnr) + " / " + str(len(lines)) + " " + str(prediction))
        #print("-----------------\n\n\n")

        if "#" in lines[lnr]:
          color = "grey"
        else:
          color = "white"

        
        if prediction is not None:
          if prediction < 0.05:
            color = "darkred"
            redcount = redcount + 1
          elif prediction < 0.1:
            color = "red"
            redcount = redcount + 1
          elif prediction < 0.3:
            color = "darkorange"
            redcount = redcount + 1
          elif prediction < 0.4:
            color = "orange"
          elif prediction < 0.5:
            color = "gold"
          elif prediction < 0.6:
            color = "yellow"
          elif prediction < 0.7:
            color = "GreenYellow"
            greencount = greencount +1
          elif prediction < 0.8:
            color = "LimeGreen"
            greencount = greencount +1
          elif prediction < 0.9:
            color = "Green"
            greencount = greencount +1 
          else:
            color = "DarkGreen"
            greencount = greencount +1
        
        
        dangerous = False
        for bad in changedparts[f]:
          if lnr >= bad[0] and lnr < (bad[0]+bad[1]):
            dangerous = True
            break
        if dangerous:
          if prediction is not None and prediction < 0.3:
            color = "royalblue"
            if len(lines[lnr]) > 1 and not "import" in lines[lnr] and not "from" in lines[lnr]:
              bluecount = bluecount + 1
          else:
            color = "violet"
            if prediction is not None and prediction >= 0.6:
              greencount = greencount -1
        
#        try:
#          d = ImageDraw.Draw(img)
#          d.text((10, ypos), lines[lnr], fill=color)
#        except Exception as e:
#          print(e)
#        ypos = ypos + 15
      if (bluecount > 2  and redcount < 30 and greencount > 10):
        print(r + "/commit/" + c + " " + f)
        print("Red: " + str(redcount))
        print("Blue: " + str(bluecount))
  #      img.save("images/" + name + c + "_" + f.replace("/","_") + ".png")                
      
        for lnr in range(0, len(lines)):
          window = getWindow(lines, lnr)
          tokens = getTokens(window)
          
          prediction = predict(tokens)
          
          
          #print(window)
          #print(name + " " + c + " " + str(changenr) + " " + str(lnr) + " / " + str(len(lines)) + " " + str(prediction))
          #print("-----------------\n\n\n")

          if "#" in lines[lnr]:
            color = "grey"
          else:
            color = "white"

          
          if prediction is not None:
            
            
          
            dangerous = False
            for bad in changedparts[f]:
              if lnr >= bad[0] and lnr < (bad[0]+bad[1]):
                dangerous = True
              
                
            if dangerous:
              if prediction is not None and prediction < 0.4:
                print (colored(lines[lnr],'cyan'))
              else:
                print (colored(lines[lnr],'grey'))
            else:
              if prediction < 0.05:
                print (colored(lines[lnr],'red'))
              elif prediction < 0.1:
                print (colored(lines[lnr],'red'))
              elif prediction < 0.25:
                print (colored(lines[lnr],'yellow'))
              elif prediction < 0.35:
                print (colored(lines[lnr],'yellow'))
              elif prediction < 0.5:
                print (colored(lines[lnr],'yellow'))
              elif prediction < 0.6:
                print (colored(lines[lnr],'green'))
              elif prediction < 0.7:
                print (colored(lines[lnr],'green'))
              elif prediction < 0.8:
                print (colored(lines[lnr],'green'))
              elif prediction < 0.9:
                print (colored(lines[lnr],'blue'))
              else:
                print (colored(lines[lnr],'blue'))
          
            
#        print(r + "/commit/" + c + " " + f)
        thegoodstuff = thegoodstuff + "\n" + r + "/commit/" + c
        print("-------")
        print(thegoodstuff)
        print("-------")
      else:
        print("not good enough " + str(redcount) + " red, " + str(bluecount) + " blue, " + str(greencount) + " green.")
    

