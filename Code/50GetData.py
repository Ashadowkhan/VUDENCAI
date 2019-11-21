import myutils
import time
import sys
import json
import subprocess
from datetime import datetime
import requests 
import pickle
from pydriller import RepositoryMining



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
 #   print("html")
    #print(change)
    #time.sleep(3)
    return None
  
  if "sage:" in change or "sage :" in change:
#    print("sage")
    #print(change)
    #time.sleep(3)
    return None
  
  thischange = {}
#  previous = stripComments(getPrevious(change))
#  after = stripComments(getAfter(change))      
#  justprevious = stripComments(getjustPrevious(change))
#  justafter = stripComments(getjustAfter(change))

  
  if myutils.getBadpart(change) is not None:
      
    badparts = myutils.getBadpart(change)[0]
    goodparts = myutils.getBadpart(change)[1]
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
      #print("   Got changes for file " + thischange["filename"] + " (" + str(len(badparts)) + ")")
      return thischange

#  print("get Badpart is none.")
  return None

#===========================================================================



myheaders = {'Authorization': 'token ' + 'c20605ddc8cfd10d1e12a1c5e89315f0bf78b6db'}


#mode = "Self-X"
#mode = "Self-XVAR"
#mode = "Self-XwithoutStrings"
#mode = "interlaken"








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



if (len(sys.argv) > 1):
    mode = sys.argv[1]
  

for mode in ["remote_code_execution","redirect"]:
  
    print(mode + " is the mode.")
    
    if mode == "full":
      allowedKeywords = ["sql","sql injection", "command injection", "function injection", "xss", "cross site", "xsrf", "unauthorized", "unauthorised", "brute force", "flooding", "tampering", "remote code", "click jack", "clickjack", "eval injection", "session fixation", "denial of service"]

    if mode == "function_injection":
      keywords = ["function_injection"]
      allowedKeywords = ["function injection"]

    if mode == "remote_code_execution":
      keywords = ["remote_code_execution"]
      allowedKeywords = ["remote code"]
      
      
    if mode == "cross_frame_scripting":
      keywords = ["cross_frame_scripting"]
      allowedKeywords = ["cross frame"]
      

    if mode == "csv_injection":
      keywords = ["csv_injection"]
      allowedKeywords = ["csv"]
      
    if mode == "redirect":
      keywords = ["redirect"]
      allowedKeywords = ["redirect"]
      

    if mode == "hijack":
      keywords = ["hijack"]
      allowedKeywords = ["session hijack","session fixation"]

    if mode == "command_injection":
      keywords = ["command_injection"]
      allowedKeywords = ["command injection"] 


    if mode == "sql":
      keywords = ["sql"]
      allowedKeywords = ["sql"] 


    if mode == "xsrf":
      keywords = ["xsrf"]
      allowedKeywords = ["xsrf","request forgery"] 


    if mode == "xss":
      keywords = ["xss"]
      allowedKeywords = ["xss", "cross site scripting","cross-site scripting"] 


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
    suspiciouswords = ["injection", "vulnerability", "exploit", " ctf","capture the flag","ctf","burp","capture","flag","attack","hack","filesystem.py", "models.py", "notebook/auth/login.py", "main.py", "jogging_result.py"]


    #words that should not appear in the commit message
    badwords = ["sqlmap", "sql-map", "sql_map","ctf "," ctf"]


    messages = ""


    
    if mode == "session_fixation":
      allowedKeywords = ["fixation"]
    if mode == "cross_origin":
      allowedKeywords = ["cross origin"]
    if mode == "buffer overflow":
      allowedKeywords = ["buffer"]
    if mode == "cache":
      allowedKeywords = ["cache"]
    if mode == "eval":
      allowedKeywords = ["eval"]
    if mode == "csv":
      allowedKeywords = ["csv"]
    if mode == "path_disclosure":
      allowedKeywords = ["path"]
    if mode == "man-in-the-middle":
      allowedKeywords = ["man in the middle", "man-in-the-middle"]
    if mode == "hijack":
      allowedKeywords = ["hijack"]
    if mode == "smurf":
      allowedKeywords = ["smurf"]
    if mode == "tampering":
      allowedKeywords = ["tamper"]
    if mode == "sanitize":
      allowedKeywords = ["saniti"]
    if mode == "denial":
      allowedKeywords = ["denial"]
    if mode == "open_redirect":
      allowedKeywords = ["redirect"]
    if mode =="directory_traversal":
      allowedKeywords = ["directory","traversal"]
    if mode == "clickjack":
      allowedKeywords = ["clickjack", "click jack"]
    if allowedKeywords == "spoof":
      allowedKeywords = ["spoof"]
    
    
    print(str(allowedKeywords))
    progress = 0

    datanew = {}
    for r in data:

      progress = progress +1

      suspicious = False
      for b in badwords:
        if b.lower() in r.lower():
          suspicious = True
      
      if suspicious:
        continue


      
      
      
      if("anhday22" in r or "Chaser-wind" in r or "/masamitsu-murase" in r or "joshc/young-goons" in r or "notakang" in r or "sudheer628" in r or "mihaildragos" in r or "aselimov" in r or "tamhidat-api" in r or "aiden-law" in r or "sreeragvv" in r or "LaurenH1090" in r or "/matthewdenaburg1" in r or "haymanjoyce" in r or "/bloctavius" in r or "jordanott/No-Weight-Sharing" in r or "bvanseg" in r or  "sudoku-solver" in r or "tgbot" in r or "lluviaBOT" in r or "jumatberkah" in r or "luisebg" in r or "emredir" in r or "anhday22" in r or "faprioryan" in r or "pablogsal" in r or "zhuyunfeng111" in r or "bikegeek/METplus" in r or "chasinglogic" in r or "Sudhir0547" in r or "fyp_bot" in r):
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
#            print("\""+k.lower()+"\" is in " + data[r][c]["keyword"].lower())
            irrelevant = False

        if irrelevant:
          continue
        
        if not (".py" in data[r][c]["diff"]):
        # print(">no python file")
          continue    
        

      #  print("\n\n" + r + "/commit/" + c)
      #  print("Keyword: " + data[r][c]["keyword"])
        
        if not "message" in data[r][c]:
          data[r][c]["message"] = ""
        #else:
         # print(data[r][c]["message"].replace("\n"," ")[:100]+"...")

        
        if not c in changedict:
          changedict[c] = 0
        if c in changedict:
          changedict[c] = changedict[c] + 1
          if changedict[c] > 5:
#            print(" we already have more than five. Skip.")
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
         #         print("suspicious word in filename: " + f)
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
            
     # print(changesfromdiff)
      if changesfromdiff:
          #now get the sourcecode!
          print("\n\n" + mode + "    mining "  + r + " " + str(progress) + "/" + str(len(data)))

          commitlist = []
          try:
            for commit in RepositoryMining(r).traverse_commits():
              commitlist.append(commit.hash)
              
              if not commit.hash in changeCommits:
                continue
              
              for m in commit.modifications:
                  
                  if m.old_path != None and m.source_code_before != None:
                    if not ".py" in m.old_path:
                      continue
                  
                    if len(m.source_code_before) > 30000:
                    # print(str(len(m.source_code_before)) + " is too long. " +r + "/commit/" + commit.hash + " " + m.old_path)
                      continue
                      
                    print("\n  modification with old path: " + str(m.old_path))
                    
                    for c in data[r]: 
                        if c == commit.hash:   
                          print("  found commit " + c)
                          
                          if not "files" in data[r][c]:
                            print("  no files :(")
                            
                          data[r][c]["msg"] = commit.msg
                          for badword in badwords:
                            if badword.lower() in commit.msg.lower():
                              suspicious = True
                          
                          if suspicious:
                            print("  suspicious commit msg: \"" + commit.msg.replace("\n"," ")[:300] + "...\"")
                            continue
                          
                          print("  The commit has " + str(len(data[r][c]["files"])) + " files.")
                          for f in data[r][c]["files"]:
                              #print("    File " + f +  " with " + str(len(data[r][c]["files"][f]["changes"])) + " changes")
                              
                              
                              
                              if m.old_path in f:
                                
                                
                                
                                if not ("source" in data[r][c]["files"][f] and (len(data[r][c]["files"][f]["source"])> 0)):
                                  sourcecode = "\n" + myutils.removeDoubleSeperatorsString(myutils.stripComments(m.source_code_before))
                                  data[r][c]["files"][f]["source"] = sourcecode
                                
                                if not ("sourceWithComments" in data[r][c]["files"][f] and (len(data[r][c]["files"][f]["sourceWithComments"])> 0)):
                                  data[r][c]["files"][f]["sourceWithComments"] = m.source_code_before
                                
                                if not ("sourceWithComments" in data[r][c]["files"][f] and (len(data[r][c]["files"][f]["sourceWithComments"])> 0)):
                                  data[r][c]["files"][f]["sourcecodeafter"] = ""
                                  if m.source_code is not None:
                                    data[r][c]["files"][f]["sourcecodeafter"] = m.source_code   
                                
                                if not r in datanew:
                                  datanew[r] = {}
                                if not c in datanew[r]:
                                  datanew[r][c] = {}
                                  
                                datanew[r][c] = data[r][c]
                                print("     ->> added to the dataset.")
                                #print("         now there are " + str(len(datanew[r][c]["files"])))
                                  
          except Exception as e:
              print("Exception occured.")
              print(e)
              time.sleep(2)
              continue
          # print(commitlist)
            
        #                          print("added to datanew, has " + str(len(blocks)) + " blocks.")




    print("done.")



    print(len(data))  
        
    with open('data/plain_' + mode, 'w') as outfile:
      json.dump(datanew, outfile)


      
      
