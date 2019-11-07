

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
import pickle
from pydriller import RepositoryMining
from gensim.models import Word2Vec, KeyedVectors



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
    print(sourcecode)
    print(":::::::::::")
    print(badpart)
    print("-----------------")
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
  



def stats():

  print("===================")

  print("\n")
  print("The bad login thing: " + str(notrep_weirdlogin))
  print("Amount of forks: " + str(notrep_fork))
  print("No changes found: " + str(notrep_nochanges))
  print("Irrelevant keywords: " + str(notrep_irrelevant))
  print("No python files: " + str(notrep_nopython))
  print("\n")
  print("Suspicious filenames: " + str(suspicious_files))
  print("\n")
  print("repositories worth a closer look because they have usable changes: " + str(thisrep))
  print("Didn't find the commit " + str(mining_notFound))
  print("Suspicious commit message " + str(mining_suspicious))
  print("Merges: " + str(mining_merge))
  print("Mining found no code " + str(mining_noCodeFound))
  print("Couldn't find the bad parts in the code: " + str(mining_BadPartsNotFound))

  v = 0
  z = 0
  for x in data:
    for y in data[x]:
      if "changes" in data[x][y]:
        z = z + len(data[x][y]["changes"]) 
  for x in datanew:
    for y in datanew[x]:
      if "changes" in data[x][y]:
        v = v + len(datanew[x][y]["changes"]) 


  print("We already have " + str(z) + " / " + str(v) + " changes for " + mode + ". Progress: " + str(float(int(progress/total * 100 * 100)) / 100) + "%")
  print("\n\n")
  

def checkFork(r):
  notfound = False
  fork = False
  okay = False
  repopath = r.split("https://github.com/")[1]
  path = "https://api.github.com/repos/" + repopath
  
  while(not fork and not okay and not notfound):
    response = requests.get(path, headers = myheaders)
    try:
      re = response.json()
      if "fork" in re:
        if re["fork"]:
          fork = True
        else:
          okay = True
      elif "message" in re and "Not Found" in re["message"]:
        notfound = True
      elif "message" in re and "API rate limit" in re["message"]:
        print("API rate limit. Sleep.")
        time.sleep(200)
    except:
      return False
  if fork:
    return True
  else:
    return False


def onlyOneSeperator(code):
#  print(list(code))
  newcode = ""
  inASeperation = False
  for x in range(0,len(code)):
    ch = code[x]
    
    if (ch != " " and ch != "\n"):
      if (inASeperation):
        inASeperation = False
        newcode = newcode + " " + ch.lower()
      else:
        newcode = newcode + ch.lower()
    else:
      inASeperation = True
      
#  print(list(newcode))
  return(newcode)




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
  

def getjustPreviousOld(change):
  lines = change
  before = ""
  while "\n" in lines:
    pos = lines.find("\n")+1
    line = lines[:pos-1]
    lines = lines[pos:]
    listline = list(line)
    if listline:
      if (listline[0] == '-'):
        listline[0] = ""
        line = "".join(listline)
        before = before + line + "\n"
  return before

def getjustAfterOld(change):
  lines = change
  after = ""
  while "\n" in lines:
    pos = lines.find("\n")+1
    line = lines[:pos-1]
    lines = lines[pos:]
    listline = list(line)
    if listline:
      if (listline[0] == '+'):
        listline[0] = ""
        line = "".join(listline)
        after = after + line + "\n"
  return after
  


def getjustAfter(change):
  after = ""
  
  lines = change.split("\n")
  first = -1
  last = -1

  for l in range(len(lines)):
    if len(lines[l]) > 0:
      if lines[l][0] == "+":
        if first < 0:
          first = l
        last = l
  
  for l in range(first,last+1):
    if len(lines[l]) > 0:
      if lines[l][0] == "-":
        continue
      after = after + lines[l][1:] + "\n"
    
  return after


def getjustPrevious(change):
  
  before = ""
  
  lines = change.split("\n")
  first = -1
  last = -1

  for l in range(len(lines)):
    if len(lines[l]) > 0:
      if lines[l][0] == "-":
        if first < 0:
          first = l
        last = l
  
  for l in range(first,last+1):
    
    if len(lines[l]) > 0:
      if lines[l][0] == "+":
        continue
      before = before + lines[l][1:] + "\n"

  return before


def getAfter(change):
  lines = change
  after = ""
  while "\n" in lines:
    pos = lines.find("\n")+1
    line = lines[:pos-1]
    lines = lines[pos:]
    listline = list(line)
    if listline:
      if (listline[0] == '-'):
        continue
      if (listline[0] == '+'):
        listline[0] = " "
      line = "".join(listline)
      after = after + line + "\n"
  return after

def getPrevious(change):
  lines = change
  before = ""
  while "\n" in lines:
    pos = lines.find("\n")+1
    line = lines[:pos-1]
    lines = lines[pos:]
    listline = list(line)
    if listline:
      if (listline[0] == '+'):
        continue
      if (listline[0] == '-'):
        listline[0] = " "
      line = "".join(listline)
      before = before + line + "\n"
  return before


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
  
  


def removeTripleN(tokenlist):
    secondlast = ""
    last = ""
    newtokens = []
    for token in tokenlist:
      if len(token) > 0:
        
        if ((secondlast == "\n") and (last == "\n") and (token == "\n")):
          #print("too many \\n.")
          o = 1 #noop
        else:
          newtokens.append(token)
          
        
        thirdlast = secondlast
        secondlast = last
        last = token
        
    return(newtokens)
  
  
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

def removeDoubleSeperatorsString(string):
  return ("".join(removeDoubleSeperators(getTokens(string))))



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
                  if (context[0] > bad[0] and context[0] <= bad[1]) or (context[1] > bad[0] and context[1] <= bad[1]):
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

def getChanges(rest):
  changes = []
  while ("diff --git" in rest):
    #print(rest)
    filename = ""
    start = rest.find("diff --git")+1
    secondpart = rest.find("index")+1
    #print("----------" + rest[start:secondpart] + "------")

    titleline = rest[start:secondpart]
    if not (".py") in rest[start:secondpart]:
      # No python file changed in this part of the commit
#          print(rest[start:secondpart])
      #print("no py")
      rest = rest[secondpart+1]
      continue

    if "diff --git" in rest[start:]:
      end = rest[start:].find("diff --git");
      filechange = rest[start:end]
      rest = rest[end:]
    else:
      end = len(rest)
      filechange = rest[start:end]
      rest = ""
    filechangerest = filechange
    
    while ("@@" in filechangerest):
      change = ""
      start = filechangerest.find("@@")+2
      start2 = filechangerest[start:start+50].find("@@")+2
      start = start+start2
      filechangerest=filechangerest[start:]
      
      if ("class" in filechangerest or "def" in filechangerest) and "\n" in filechangerest:
        filechangerest = filechangerest[filechangerest.find("\n"):]
      
      if "@@" in filechangerest:
          end = filechangerest.find("@@")
          change = filechangerest[:end]
          filechangerest = filechangerest[end+2:]
          
      else:
        end = len(filechangerest)
        change = filechangerest[:end]
        filechangerest = ""

      if len(change) > 0:
        changes.append([titleline,change])
  
#  print("We found " + str(len(changes)) + " changes.")
  return changes
  
  
def getFilename(titleline):
  
  s = titleline.find(" a/")+2
  e = titleline.find(" b/")
  name = titleline[s:e]
  
  if titleline.count(name) == 2:
    return name
  elif ".py" in name and (" a"+name+" " in titleline):
    return name
  else:
    print("couldn't find name")
    print(titleline)
    print(name)
  
  
  
  
def makechangeobj(changething):
  
  change = changething[1]
  titleline = changething[0]
  
#  if "array" in change and change.count(",") > 99:
#    #this is a big array
#    print("big array")
#    return None
  
  if "<html" in change:
    print("html")
    #print(change)
    #time.sleep(3)
    return None
  
  if "sage:" in change or "sage :" in change:
    print("sage")
    #print(change)
    #time.sleep(3)
    return None
  
  thischange = {}
#  previous = stripComments(getPrevious(change))
#  after = stripComments(getAfter(change))      
#  justprevious = stripComments(getjustPrevious(change))
#  justafter = stripComments(getjustAfter(change))

  
  if getBadpart(change) is not None:
      
    badparts = getBadpart(change)[0]
    goodparts = getBadpart(change)[1]
#    print("For this change, badparts: " + str(badparts))
    linesadded = change.count("\n+")
    linesremoved = change.count("\n-")
    thischange["diff"] = change
    thischange["add"] = linesadded
    thischange["remove"] = linesremoved
    thischange["filename"] = getFilename(titleline)
    thischange["badparts"] = badparts
    thischange["goodparts"] = []
    if goodparts is not None:
      thischange["goodparts"] = goodparts
    #print("\n")
    #print("goodparts here for file " + getFilename(titleline))
    #print(thischange["goodparts"])
    #print("Len: " + str(len(thischange["goodparts"])))
    if thischange["filename"] is not None:
      print("   Got changes for file " + thischange["filename"] + " (" + str(len(badparts)) + ")")
      return thischange

#  print("get Badpart is none.")
  return None

#===========================================================================



myheaders = {'Authorization': 'token ' + 'c20605ddc8cfd10d1e12a1c5e89315f0bf78b6db'}


#mode = "Self-X"
#mode = "Self-XVAR"
#mode = "Self-XwithoutStrings"
#mode = "interlaken"




datanew = {}




#with open('Smalldata.json', 'r') as infile:
#  data = json.load(infile)

with open('PyCommitsWithDiffs.json', 'r') as infile:
  data = json.load(infile)


print("finished loading")

print("\n\n\n")
print("\n\n\n")
                
                
  
i = 0
for r in data:
  for c in data[r]:
    i = i+1

#print("We have " + str(len(data)) + " repositories in this file, and "+ str(i) + " commits.")

count = 0


now = datetime.now() # current date and time
nowformat = now.strftime("%H:%M")
print("time:", nowformat)

alldata = []
jdata = {}

countnomessage = 0
total = len(data)
progress = 0





changedict = {}



step = 150
fulllength = 200

counting = 0
forkcount = 0

mode = "sql"
allowedKeywords = ["sql injection"]
#modelw2v = "w2v/word2vec_withString100-100.model"

if (len(sys.argv) > 1):
  mode = sys.argv[1]
  if (len(sys.argv) > 2):
    modelw2v = sys.argv[2]
    

#w2v_model = Word2Vec.load(modelw2v)
#word_vectors = w2v_model.wv


if mode == "full":
  allowedKeywords = ["sql","sql injection", "command injection", "function injection", "xss", "cross site", "xsrf", "unauthorized", "unauthorised", "brute force", "flooding", "tampering", "remote code", "click jack", "clickjack", "eval injection", "session fixation", "denial of service"]



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


if mode == "remote_code_execution":
  allowedKeywords = ["remote code execution"]
  
if mode == "formatstring":
  allowedKeywords = ["format string", "formatstring"]


#words that should not appear in the filename
suspiciouswords = ["injection", "vulnerability", "exploit", "xss", "xsrf","hack","filesystem.py", "models.py", "notebook/auth/login.py", "main.py", "jogging_result.py"]


#words that should not appear in the commit message
badwords = ["sqlmap", "sql-map", "sql_map"]


messages = ""

print(mode + " is the mode.")
print(str(allowedKeywords))

for r in data:

  progress = progress +1

  suspicious = False
  for b in badwords:
    if b.lower() in r.lower():
      suspicious = True
  
  if suspicious:
    continue


  
  
  
  if("anhday22" in r or "Chaser-wind" in r or "/masamitsu-murase" in r or "joshc/young-goons" in r or "notakang" in r or "sudheer628" in r or "mihaildragos" in r or "aselimov" in r or "tamhidat-api" in r or "aiden-law" in r or "sreeragvv" in r or "LaurenH1090" in r or "/matthewdenaburg1" in r or "haymanjoyce" in r or "/bloctavius" in r or "jordanott/No-Weight-Sharing" in r or "bvanseg" in r or  "sudoku-solver" in r or "tgbot" in r or "lluviaBOT" in r or "jumatberkah" in r or "luisebg" in r or "emredir" in r or "anhday22" in r or "pablogsal" in r or "zhuyunfeng111" in r or "bikegeek/METplus" in r or "chasinglogic" in r or "Sudhir0547" in r or "fyp_bot" in r):
    continue


  
#  if checkFork(r):
#    #print("FORK!")
#    notrep_fork = notrep_fork + 1
#    continue


  changesfromdiff = False
  all_irrelevant = True
  
  changeCommits = []
  for c in data[r]:
    
    #print(c)
    #get the info from the commits diff file - specifically the filesnames and badparts
    
    irrelevant = True
    for k in allowedKeywords:
      if k.lower() in data[r][c]["keyword"].lower():
        print("\""+k.lower()+"\" is in " + data[r][c]["keyword"].lower())
        irrelevant = False

    if irrelevant:
      continue
    
    if not (".py" in data[r][c]["diff"]):
     # print(">no python file")
      continue    
    

    print(r + "/commit/" + c)
    print("Keyword: " + data[r][c]["keyword"])
    
    if not "message" in data[r][c]:
      data[r][c]["message"] = ""
    else:
      print(data[r][c]["message"].replace("\n"," ")[:100]+"...")

    
    if not c in changedict:
      changedict[c] = 0
    if c in changedict:
      changedict[c] = changedict[c] + 1
      if changedict[c] > 10:
        print(" we already have more than ten. Skip.")
        continue
    else:
      changedict[c] = 1
    
#    duplicate = False
#    for c2 in data[r]:
#      if c != c2:
#        if data[r][c]["diff"] == data[r][c2]["diff"]:
#          #print("we already have that.")
#          duplicate = True
#    if duplicate:
#      #print("duplicate")
#      continue
    
    
    badparts = {}    
    changes = getChanges( data[r][c]["diff"])
    
    #if (len(changes) == 0):
      #print("no usable changes.")
    
    for change in changes:
      thischange = makechangeobj(change)

      if thischange is not None:
        if not "files" in data[r][c]:
          data[r][c]["files"] = {}
          f = thischange["filename"]
          
          if f is not None:
            suspicious = False
            for s in suspiciouswords:
              if s.lower() in f.lower():
                #words should not appear in the filename
                print("suspicious word in filename: " + f)
                suspicious = True
            
            if not suspicious:            
              if not f in data[r][c]["files"]:
                data[r][c]["files"][f] = {}
              if not "changes" in data[r][c]["files"][f]:
                data[r][c]["files"][f]["changes"] = []
              data[r][c]["files"][f]["changes"].append(thischange)
              changesfromdiff = True
              changeCommits.append(c)
      #else:
      #  print("thischange is none.")
        
#  print(changesfromdiff)
  if changesfromdiff:
      #now get the sourcecode!
      print("\n\n")
      print(mode + "    mining " + str(step) + " step  "  + r + " " + str(progress) + "/" + str(len(data)))
      print(changeCommits)

      commitlist = []
      try:
        for commit in RepositoryMining(r).traverse_commits():
          commitlist.append(commit.hash)
          
          if not commit.hash in changeCommits:
            continue
          
          for m in commit.modifications:
              
              if m.old_path != None:
                
                if len(m.source_code_before) > 30000:
                  print(str(len(m.source_code_before)) + " is too long. " +r + "/commit/" + commit.hash + " " + m.old_path)
                  continue
                  
                
                for c in data[r]: 
                    if c == commit.hash:   
                      
                      if not "files" in data[r][c]:
                        print("no files :(")
                        
                      data[r][c]["msg"] = commit.msg
                      for badword in badwords:
                        if badword.lower() in commit.msg.lower():
                          print("suspicious commit msg. skip. " + commit.msg.replace("\n"," ")[:200])
                          suspicious = True
                      
                      if suspicious:
                          continue
                      
                      
                      for f in data[r][c]["files"]:

                          if m.old_path in f:
                            print("  Match with commit " +r + "/commit/" + c)
                            print("  " + f + "  " + str(len(m.source_code_before)))
                            sourcecode = "\n" + removeDoubleSeperatorsString(stripComments(m.source_code_before))
                            sourcecodeafter = "\n" + removeDoubleSeperatorsString(stripComments(m.source_code))
                            #print(sourcecode)
                            data[r][c]["files"][f]["source"] = sourcecode
                            data[r][c]["files"][f]["sourceWithComments"] = m.source_code_before
                            data[r][c]["files"][f]["sourcecodeafter"] = m.source_code                        
                            if(len(data[r][c]["files"][f]["changes"]) > 1):
                              print("This is longer than expected! " + r+"/commit/"+c)
                              sys.exit()
                            
                            
                            
                            if not r in datanew:
                              datanew[r] = {}
                            if not c in datanew[r]:
                              datanew[r][c] = {}
                              
                            datanew[r][c] = data[r][c]
                            print("added to the dataset.")
                              
      except:
        time.sleep(2)
        continue
     # print(commitlist)
      
  #                          print("added to datanew, has " + str(len(blocks)) + " blocks.")




print("done.")



print(len(data))  
    
with open('data/plain_' + mode, 'w') as outfile:
  json.dump(datanew, outfile)


  
  
