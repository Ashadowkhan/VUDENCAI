

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
  
  
  return withoutComments


  
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

def removeTripleN(tokenlist):
    secondlast = ""
    last = ""
    newtokens = []
    for token in tokenlist:
      if len(token) > 0:
        
        if ((secondlast == "\n") and (last == "\n") and (token == "\n")):
          print("too many \\n.")
        else:
          newtokens.append(token)
          
        
        thirdlast = secondlast
        secondlast = last
        last = token
        
    return(newtokens)

def is_builtin(name):
    return name in builtins.__dict__
def is_keyword(name):
      return name in keyword.kwlist

myheaders = {'Authorization': 'token ' + '62b91a7aab880263d42d98159b3dcac407891972'}



#mode = "Self-X"
#mode = "Self-XVAR"
#mode = "Self-XwithoutStrings"
#mode = "interlaken"



#mode = "sql"
mode = "full"
counting = 0
forkcount = 0

mode = "sql"

messages = ""

with open('+DataFilter2.json', 'r') as infile:
    datafilter = json.load(infile)

print("loaded DataFilter")



datanew = {}

#allowedKeywords = ["sql"]
suspicious = ["injection", "vulnerability", "exploit"]
allowedKeywords = ["session fixation", "command injection", "sql injection", "XSS", "cross site", "remote code execution", "XSRF", "cross site request forgery", "hijack"]
bad = ["sqlmap"]
allowedKeywords = ["sql"]





with open('+PyCommitsWithDiffs2.json', 'r') as infile:
  data = json.load(infile)

print("finished loading")


  
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





for r in data:
  z = 0
  v = 0


  for x in data:
    for y in data[x]:
      if "changes" in data[x][y]:
        z = z + len(data[x][y]["changes"]) 
  for x in datanew:
    for y in datanew[x]:
      if "changes" in data[x][y]:
        v = v + len(datanew[x][y]["changes"]) 
  #print("===================//////////" + r  + "//////////====================")
  #print("We already have " + str(z) + " / " + str(v) + " changes for " + mode + ". Progress: " + str(float(int(progress/total * 100 * 100)) / 100) + "%")
  if ((float(int(progress/total * 100 * 100)) / 100) % 2 == 0 and (float(int(progress/total * 100 * 100)) / 100) > 0):
    print("progress: " + str(float(int(progress/total * 100 * 100)) / 100))
  
  if("anhday22" in r or "Chaser-wind" in r or "luisebg" in r or "emredir" in r or "anhday22" in r or "pablogsal" in r or "zhuyunfeng111" in r or "chasinglogic" in r):
    continue


  
  if checkFork(r):
    #print("FORK!")
    forkcount = forkcount +1 
    continue







  timer = timer +1

  changesfromdiff = False
  
  for c in data[r]:
    irrelevant = True
    for k in allowedKeywords:
      if k in data[r][c]["keyword"]:
        irrelevant = False
    
    if irrelevant:
    #  print(data[r][c]["keyword"] + " is irrelevant.")
      continue
    
    diff = data[r][c]["diff"]
    rest = diff
    if not (".py" in data[r][c]["diff"]):
      #print(">no python file")
      continue    
      
    if not "message" in data[r][c]:
      data[r][c]["message"] = ""
    
    
    nopython = True
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
        
        
        nopython = False
        
        
    
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
            previous = getPrevious(change)[2:]
            after = getAfter(change)[2:]
            linesadded = change.count("\n+")
            linesremoved = change.count("\n-")
            
            thischange["previous"] = previous
            thischange["previous-token"] = removeTripleN(getTokens(previous))
            thischange["after"] = after
            thischange["after-token"] = removeTripleN(getTokens(after))
            thischange["diff"] = ""
            thischange["add"] = linesadded
            thischange["remove"] = linesremoved
            thischange["keyword"] = data[r][c]["keyword"]
            thischange["titleline"] = titleline
              
            for keyw in allowedKeywords:
              if keyw in titleline:
                for s in suspicious:
                  if s in data[r][c]["keyword"]:
                    print("suspicious file " + titleline.replace("\n"," "))
                    
            same = True
            if (len(thischange["after-token"]) == len(thischange["previous-token"])):
              for x in range (0, len(thischange["after-token"])):
                if (thischange["previous-token"][x] != thischange["after-token"]):
                  same = False
            else:
              same = False
            if same:
              print("They are the same!")
            
            
            bigarray = False
            if  ("array" in thischange["previous"] and thischange["previous"].count(",") > 99) or ("array" in thischange["after"] and thischange["after"].count(",") > 99):
              bigarray = True
              print("gigantic array.")
              
            if "<html" in change:
              print("HTML!")
            if "sage:" in change or "sage :" in change:
              print("sage!")
              
            
            if (not "<html" in change) and (not "sage:" in change) and (not "sage :" in change) and (not same) and (not bigarray):
              if not "changes" in data[r][c]:
                data[r][c]["changes"] = []
              data[r][c]["changes"].append(thischange)
            #  print("Added one change (" + data[r][c]["keyword"] +") " + r + "/commits/" + c)
              counting = counting+1
              changesfromdiff = True
              #WE CAN USE THIS CHANGE 
        
        
    
  if changesfromdiff:
    print("Repository Mining for " + r)
    try:
      for commit in RepositoryMining(r).traverse_commits():
        for c in data[r]:
          if not "changes" in data[r][c]:
           # print("  no changes, continue")
            continue
          
          
          if commit.hash == c:
            files = {}
            print("  found the commit " + c)
            
            IsSuspicious = False
            for s in bad:
              if s in commit.msg:
                print("    suspicious because of " + s + " in " + commit.msg[:100].replace("\n"," "))
                IsSuspicious = True
              
            if IsSuspicious:
              continue
            
            progress = progress +1
            messages = messages + commit.msg[:150].replace("\n", "") + "... " + r + "/commits/" + c + "\n"
            
            data[r][c]["merge"] = commit.merge
            if (data[r][c]["merge"]):
              print("MERGE")
            
            if data[r][c]["merge"]:
              continue
            
            for m in commit.modifications:
              if m.old_path == None:
                print("     created: "  + m.new_path)
              elif m.new_path == None:
                print("    deleted: "  + m.old_path)
              elif (".py" in m.old_path and m.source_code_before != None):
                #print("    Noting down the filename " + m.old_path)
                files[m.old_path] = stripComments(m.source_code_before)
              else:
                print("  not a python file " + m.old_path)
                
            if len(files) == 0:
              print("  No code. Continue.")
            else:  
              badparts = {}
              for index in range(0,len(data[r][c]["changes"])):
                for f in files:
                  if f in data[r][c]["changes"][index]["titleline"]:
                   # print("    change nr. " + str(index) + " has filename " + f)
                    data[r][c]["changes"][index]["filename"] = f
                    data[r][c]["changes"][index]["sourcecode"] = files[f]
                    if f not in badparts:
                      badparts[f] = []
                    badparts[f].append(stripComments(data[r][c]["changes"][index]["previous"]))
              

              data[r][c]["clean"] = []
              
              for filename in badparts:
                print("    Take the good code from " + filename + " where there were " + str(len(badparts[filename])) + " bad parts.")
                sourcecode = onlyOneSeperator(files[filename])
                for thing in badparts[filename]:
                  thing = onlyOneSeperator(thing)
                  start = sourcecode.find(thing)
                  if start > 0:
                    end = start + len(thing)
                    x = sourcecode[:start]
                    y = sourcecode[end:]
                    sourcecode = x + y
                    #print("  Sourcecode shortened to: " +str(len(sourcecode)))
                  else:
                    start = sourcecode.find(thing[20:80])
                    if (start > 0):
                      end = start + len(thing)
                      x = sourcecode[:start]
                      y = sourcecode[end:]
                      sourcecode = x + y
                    else:
                      print("couldn't find bad parts in the file. See: ")
                      print(thing)
                      print(":::::")
                      print(sourcecode)
                  
                rest = sourcecode
                while (len(rest) > 0):
                  if len(rest) < 450:
                    block = rest
                    rest = ""
                  else:
                    for i in range(400,len(rest)):
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
                    cleanblock["token"] = removeTripleN(getTokens(block))
                    data[r][c]["clean"].append(cleanblock)
              
              if not r in datanew:
                datanew[r] = {}
              if not c in datanew[r]:
                datanew[r][c] = {}
              datanew[r][c] = data[r][c]
        
        
        #if(nopython):
        #  print("no python for this change")
        #else:
        #  print("python in this change! :)")
    except Exception as e:
      print("Exception")
      print(e)
  
print("done.")
print("fork count: " + str(forkcount))



with open('data2/' + mode + '_messages', 'wb') as fp:
  pickle.dump(messages, fp)
    
with open('data2/' + mode, 'w') as outfile:
  json.dump(data, outfile)
  #
with open('data2/' + mode+'-onlyWithRepSuccess', 'w') as outfile:
  json.dump(datanew, outfile)

print(len(datanew))  
  
  
