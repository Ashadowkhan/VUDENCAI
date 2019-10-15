from pydriller import RepositoryMining
import requests
import time
import requests
import sys
import json
import datetime

data1 = {}
data = {}

repositories = {}

with open('all_commits2.json', 'r') as infile:
    repositories = json.load(infile)
    
print("loaded commits")

with open('+DataFilter2.json', 'r') as infile:
    datafilter = json.load(infile)

print("loaded filter")

if not 'checked' in datafilter:
  datafilter['checked'] = {}

  

print(str(len(datafilter['showcase'])) + " repositories are showcases and therefore ignored.")
print(str(len(datafilter['no-python'])) + " repositories don't even contain ANY python.")
print(str(len(datafilter['python'])) + " might contain python.")


#try:
#    with open('+PyCommitsWithDiffs.json', 'r') as infile:
#        data = json.load(infile)
#except:
#  data = {}
  
data = {}
with open('commits_pyB.json', 'r') as infile:
    dataB = json.load(infile)
with open('commits_pyC.json', 'r') as infile:
    dataC = json.load(infile)
with open('commits_pyA.json', 'r') as infile:
    dataA = json.load(infile)
    
    
for r in dataA:
  name = r.split('https://github.com/')[1]
  if (name in datafilter['showcase']):
      continue
  data[r] = dataA[r]
for r in dataB:
  name = r.split('https://github.com/')[1]
  if (name in datafilter['showcase']):
      continue
  data[r] = dataB[r]
for r in dataC:
  name = r.split('https://github.com/')[1]
  if (name in datafilter['showcase']):
      continue
  data[r] = dataC[r]

i = 0
for r in data:
  for c in data[r]:
    i = i+1

print("We have " + str(len(data)) + " repositories in those files, and "+ str(i) + " commits.")

olddata = data

data = {}






myheaders = {'Authorization': 'token ' + '62b91a7aab880263d42d98159b3dcac407891972'}
pycommit = 0

totalnumber = 0

count = 0





nextTimeTrying = 0
yep = 0
nope = 0
progress = 0
total = 0
newrepos = 0
nopythonlist = {} #used to mark which COMMITS have and don't have python files modified

print("starting")
for repo in repositories:
  progress = progress + 1
      
  
  if (((progress % 3000) == 0) and total > 0) and not saved:
    print("Time to save.")
    saved = True

    before = time.time()
   
    with open('+DataFilter2.json', 'w') as outfile:
        json.dump(datafilter, outfile)
    
    with open('+PyCommitsWithDiffs2.json', 'w') as outfile:
        json.dump(data, outfile)
  
 #  after = time.time()
  #  print("time used for saving:")
  #  print(after - before)

  
  

  count = count+1
  name = repo.split('https://github.com/')[1]
  
  if (name in datafilter['showcase']):
      print("skip: showcase")
      continue
  if (name in datafilter['no-python']):
    
      print("skip: no python")
      continue


  print("\n" + repo + "     " + str(progress))
  
  
  
  if not repo in nopythonlist:
    nopythonlist[repo] = {}
  
  noPythonAtAll = True
  
  
  if (repo in olddata):
    print("repo is known.")
    for c in repositories[repo]:
      if c in nopythonlist[repo]:
        continue
      if c in olddata[repo]:
        print("take this commit.")
        diffcontent = olddata[repo][c]["diff"]
        if (".py" in diffcontent):        
          noPythonAtAll = False
          print(c + " changes a python file.")
          
          if not repo in data:
            data[repo] = {} 
            
          
          total = total + 1 
          saved = False
          
          data[repo][c] = repositories[repo][c]
          
          data[repo][c]["diff"] = diffcontent
      
        
  else:
   
   for c in repositories[repo]:
      if c in nopythonlist[repo]:
        continue
      
      target = repo+'/commit/' + c + '.diff'
      response = requests.get(target,headers = myheaders)
      content = response.content
      try:
          diffcontent = content.decode('utf-8',errors='ignore');
      except:
          print("an exception occured. Skip.");
          continue;
      
      if (".py" in diffcontent):        
          noPythonAtAll = False
          print("   " + c + " changes a python file ("+repositories[repo][c]["keyword"] + ")")
          
          if not repo in data:
            data[repo] = {} 
            
          
          total = total + 1 
          saved = False
          
          data[repo][c] = repositories[repo][c]
          
          data[repo][c]["diff"] = content.decode('utf-8',errors='ignore');
        

                      
          
      else:
         # print("   " + c + " ..nope ("+repositories[repo][c]["keyword"] + ")")
          if not repo in nopythonlist:
            nopythonlist[repo] = {}
          nopythonlist[repo][c] = {}
        
  if noPythonAtAll:
    nope = nope+1
    print("repository has no python at all or was unknown.")
    datafilter['no-python'][name] = {}    
  else:
    print("repository has some python")
    yep = yep+1
    
    datafilter['checked'][name] = {}
    
    if not (repo in olddata):
      newrepos = newrepos+1
      print("EVEN THOUGHT IS IS UNKNOWN!?")
      #with open('+DataFilter2.json', 'w') as outfile:
      #  json.dump(datafilter, outfile)

      #with open('+PyCommitsWithDiffs2.json', 'w') as outfile:
      #    json.dump(data, outfile)
      #sys.exit()


print("Of " + str(progress) + " repositories, there were " + str(yep) + " / " + str(nope))

print(str(total) + " commits modifying python were found.")

print(str(newrepos) + " new repos.")

with open('+DataFilter2.json', 'w') as outfile:
    json.dump(datafilter, outfile)

with open('+PyCommitsWithDiffs2.json', 'w') as outfile:
    json.dump(data, outfile)
    
