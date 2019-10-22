

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



counting = 0
forkcount = 0

mode = "replay_attack"
allowedKeywords = ["replay attack"]




if (len(sys.argv) > 1):
  mode = sys.argv[1]






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






#words that should not appear in the filename
suspicious = ["injection", "vulnerability", "exploit"]


#words that should not appear in the commit message
bad = ["sqlmap"]


messages = ""




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
  print("Changes that were the same: " + str(samecount))
  print("big arrays: " + str(bigarraycount))
  print("HTML in the change: " + str(htmlcount))
  print("sage in the change: " + str(sagecount))
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





#===========================================================================

myheaders = {'Authorization': 'token ' + 'c20605ddc8cfd10d1e12a1c5e89315f0bf78b6db'}


#mode = "Self-X"
#mode = "Self-XVAR"
#mode = "Self-XwithoutStrings"
#mode = "interlaken"




datanew = {}





with open('PyCommitsWithDiffs.json', 'r') as infile:
  data = json.load(infile)

print("finished loading")

print("\n\n\n")
print("\n\n\n")
                
                
  
i = 0
for r in data:
  for c in data[r]:
    i = i+1

print("We have " + str(len(data)) + " repositories in this file, and "+ str(i) + " commits.")

count = 0



now = datetime.now() # current date and time
nowformat = now.strftime("%H:%M")
print("time:", nowformat)

alldata = []
jdata = {}

countnomessage = 0
timer = 0
total = len(data)
progress = 0


notrep_weirdlogin = 0
notrep_fork = 0
notrep_nochanges = 0
notrep_irrelevant = 0
notrep_nopython = 0


suspicious_files = 0
samecount = 0
bigarraycount = 0
htmlcount = 0
sagecount = 0

thisrep = 0
mining_noChanges = 0
mining_suspicious = 0
mining_merge = 0
mining_noCodeFound = 0
mining_BadPartsNotFound = 0
mining_notFound = 0

for r in data:
  z = 0
  v = 0

  
  progress = progress +1


  #if ((float(int(progress/total * 100 * 100)) / 100) % 2 == 0 and (float(int(progress/total * 100 * 100)) / 100) > 0):
  
  
  progressing = float(int((progress/total * 10000) / 100))
  print("progress: " + str(progressing))
  stats()
  
  
  if("anhday22" in r or "Chaser-wind" in r or "notakang" in r or "mihaildragos" in r or "aselimov" in r or "tamhidat-api" in r or "aiden-law" in r or "sreeragvv" in r or "bvanseg" in r or  "sudoku-solver" in r or "tgbot" in r or "lluviaBOT" in r or "jumatberkah" in r or "luisebg" in r or "emredir" in r or "anhday22" in r or "pablogsal" in r or "zhuyunfeng111" in r or "chasinglogic" in r):
    notrep_weirdlogin = notrep_weirdlogin +1
    continue


  
#  if checkFork(r):
#    #print("FORK!")
#    notrep_fork = notrep_fork + 1
#    continue



  timer = timer +1

  changesfromdiff = False
  all_irrelevant = True
  for c in data[r]:
    
    all_nopython = False
    irrelevant = True
    for k in allowedKeywords:
      if k.lower() in data[r][c]["keyword"].lower():
        irrelevant = False
        all_irrelevant = False
    
    
    if irrelevant:
    #  print(data[r][c]["keyword"] + " is irrelevant.")
      continue
    


    all_nopython = True
    diff = data[r][c]["diff"]
    rest = diff
    
    if not (".py" in data[r][c]["diff"]):
      #print(">no python file")
      continue    
    else:
      all_nopython = False
      
    if not "message" in data[r][c]:
      data[r][c]["message"] = ""
    
    
    badparts = {}    
    
    while ("diff --git" in rest):
        #print(rest)
        filename = ""
        start = rest.find("diff --git")+1
        secondpart = rest.find("index")+1
        #print("----------" + rest[start:secondpart] + "------")
    
        titleline = rest[start:secondpart]
        #print("TITLELINE: |"+titleline+"|")
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
            
           
            thischange = {}
            previous = stripComments(getPrevious(change))
            after = stripComments(getAfter(change))
            
            justprevious = stripComments(getjustPrevious(change))
            justafter = stripComments(getjustAfter(change))

           
            if not (isEmpty(previous) or isEmpty(after) or isEmpty(justprevious) or isEmpty(justafter)):
              
              linesadded = change.count("\n+")
              linesremoved = change.count("\n-")
              
              thischange["previous"] = previous
              thischange["justprevious"] = justprevious
              thischange["previous-token"] = removeDoubleSeperators(getTokens(stripComments(previous)))
              thischange["justprevious-token"] = removeDoubleSeperators(getTokens(stripComments(justprevious)))
              thischange["after"] = after
              thischange["justafter"] = justafter
              thischange["after-token"] = removeDoubleSeperators(getTokens(stripComments(after)))
              thischange["justafter-token"] = removeDoubleSeperators(getTokens(stripComments(justafter)))
              thischange["diff"] = ""
              thischange["add"] = linesadded
              thischange["remove"] = linesremoved
              thischange["keyword"] = data[r][c]["keyword"]
              thischange["titleline"] = titleline
                
              for keyw in allowedKeywords:
                if keyw.lower() in titleline.lower():
                  for s in suspicious:
                    if s.lower() in data[r][c]["keyword".lower()]:
                      print("suspicious file " + titleline[:120].replace("\n"," "))
                      suspicious_files = suspicious_files + 1
                      
              same = True            
              if (len(thischange["after-token"]) == len(thischange["previous-token"])):
                for x in range (0, len(thischange["after-token"])):
                  if (thischange["previous-token"][x] != thischange["after-token"]):
                    same = False
              else:
                same = False
              if same:
                print("They are the same!")
                samecount = samecount+1
              
              bigarray = False
              if  ("array" in thischange["previous"] and thischange["previous"].count(",") > 99) or ("array" in thischange["after"] and thischange["after"].count(",") > 99):
                bigarray = True
                print("gigantic array.")
                bigarraycount = bigarraycount+1
                
              if "<html" in change:
                print("HTML!")
                htmlcount = htmlcount+1
                
              if "sage:" in change or "sage :" in change:
                print("sage!")
                sagecount = sagecount+1
                
              
              if (not "<html" in change) and (not "sage:" in change) and (not "sage :" in change) and (not same) and (not bigarray):
                if not "changes" in data[r][c]:
                  data[r][c]["changes"] = []
                data[r][c]["changes"].append(thischange)
              #  print("Added one change (" + data[r][c]["keyword"] +") " + r + "/commits/" + c)
                counting = counting+1
                changesfromdiff = True
                #WE CAN USE THIS CHANGE 
        
        






    
  if changesfromdiff:
    thisrep = thisrep + 1
    print("Repository Mining for " + r)
  #  try:
  
    try:
      for commit in RepositoryMining(r).traverse_commits():
        
          
        found = False
        for c in data[r]:
          
          if not "changes" in data[r][c]:
            # print("  no changes, continue")
            continue
          
          
          if commit.hash == c:
            found = True
            files = {}
            print("  found the commit " + c)
            
            IsSuspicious = False
            for s in bad:
              if s in commit.msg:
                print("    suspicious because of " + s + " in " + commit.msg[:100].replace("\n"," "))
                IsSuspicious = True
              
            if IsSuspicious:
              mining_suspicious = mining_suspicious + 1
              continue
            
            messages = messages + commit.msg[:300].replace("\n", "") + "...\n" + r + "/commit/" + c + "\n\n"
            
            data[r][c]["merge"] = commit.merge
            if (data[r][c]["merge"]):
              print("MERGE")
            
            if data[r][c]["merge"]:
              mining_merge = mining_merge +1 
              continue
            
            for m in commit.modifications:
              if m.old_path == None:
                print("     created: "  + m.new_path)
              elif m.new_path == None:
                print("    deleted: "  + m.old_path)
              elif (".py" in m.old_path and m.source_code_before != None):
                print("    Noting down the filename " + m.old_path + " and getting the files with stripped comments")
                files[m.old_path] = stripComments(m.source_code_before)
                
              else:
                print("  not a python file " + m.old_path)
                
            if len(files) == 0:
              mining_noCodeFound = mining_noCodeFound+1
              print("  No code. Continue.")
              continue
            else:  
              badparts = {}
              badparts_just = {}
              for index in range(0,len(data[r][c]["changes"])):
                
                for f in files:
                  if f in data[r][c]["changes"][index]["titleline"]:
  #                    print("    change nr. " + str(index) + " for filename " + f)
                    data[r][c]["changes"][index]["filename"] = f
                    data[r][c]["changes"][index]["sourcecode"] = files[f]
                    if f not in badparts:
                      badparts[f] = []
                    if f not in badparts_just:
                      badparts_just[f] = []
                    badparts[f].append(removeDoubleSeperatorsString(stripComments(data[r][c]["changes"][index]["previous"])))
                    badparts_just[f].append(removeDoubleSeperatorsString(stripComments(data[r][c]["changes"][index]["justprevious"])))
              
              data[r][c]["badparts"] = badparts
              data[r][c]["badparts_just"] = badparts_just
              
              for changeindex in range(len(data[r][c]["changes"])):
                if data[r][c]["changes"][changeindex]["filename"] == f:
                  data[r][c]["changes"][changeindex]["badparts"] = badparts
                  data[r][c]["changes"][changeindex]["badparts_just"] = badparts_just
                
              data[r][c]["clean"] = []
              
              for filename in badparts:
                print("    Take the good code from " + filename + " where there were " + str(len(badparts[filename])) + " bad parts.")
                
                
                
                sourcecode = removeDoubleSeperatorsString(files[filename])
                
                
                
                for tix in range(len(badparts[filename])):
                  thing = badparts[filename][tix]
                  start = sourcecode.find(thing)
                  if start > 0:
                    end = start + len(thing)
                    x = sourcecode[:start]
                    y = sourcecode[end:]
                    sourcecode = x + y
                #     print("found")
                    #print("  Sourcecode shortened to: " +str(len(sourcecode)))
                  else:
                    start = sourcecode.find(thing[20:80])
                    if (start > 0):
                    #  print("found")
                      end = start + len(thing)
                      x = sourcecode[:start]
                      y = sourcecode[end:]
                      sourcecode = x + y
                    else:
                      thing2 = badparts_just[filename][tix]
                      start = sourcecode.find(thing2[1:])
                      if start > 0:
                        # print("found")
                        end = start + len(thing2)
                        x = sourcecode[:start]
                        y = sourcecode[end:]
                        sourcecode = x + y
                          
                      else:
                        print("couldn't find bad parts in the file. See: ")
                        print(thing)
                        print(":::::")
                        print(thing2)
                        print(":::::")
                        print(sourcecode)
                        print("\n\n"+r+"/commit/"+c)
                        mining_BadPartsNotFound = mining_BadPartsNotFound +1
                      
                      
                      
                  
                rest = sourcecode
                while (len(rest) > 0):
                  if len(rest) < 40:
                    block = rest
                    rest = ""
                  else:
                    for i in range(40,len(rest)):
                      if(rest[i] == " " or rest[i] == "\n"):
                        end = i
                        break
                  block = rest[:end]
                  rest = rest[end:]
                  if (len(block) > 0):
                    cleanblock = {}
                    cleanblock["source"] = block
                    cleanblock["file"] = filename
                    cleanblock["keyword"] = data[r][c]["keyword"]
                    cleanblock["token"] = removeDoubleSeperators(getTokens(stripComments(block)))
                    data[r][c]["clean"].append(cleanblock)
              
              if not r in datanew:
                datanew[r] = {}
              if not c in datanew[r]:
                datanew[r][c] = {}
              datanew[r][c] = data[r][c]
        
      if not found:
        print(c)
        print("didn't find...")
        print(data[r].keys())
        mining_notFound = mining_notFound + 1
    except Exception as e:
      print("Exception")
      print(e)
  
  
  if all_nopython:
    notrep_nopython = notrep_nopython + 1
  if all_irrelevant:
     notrep_irrelevant = notrep_irrelevant + 1
  #notrep-nochanges = notrep-nochanges +1


print("done.")


stats()

with open('data3/' + mode + '_messages.txt', 'wb') as fp:
  pickle.dump(messages, fp)
    
with open('data3/' + mode, 'w') as outfile:
  json.dump(datanew, outfile)


print(len(datanew))  
  
  
