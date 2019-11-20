import json

def countloc(code):
  loc = 0
  lines = code.split("\n")
  for l in lines:
    if len(l) > 0:
      l = l.lstrip()
    if len(l) > 0:
      if not l[0] == "#":
        loc = loc+1 
#      else: 
#        print("line is comment")
  return loc



if False:
    with open('all_commits.json', 'r') as  infile:
        data = json.load(infile)
        
    repos = 0
    commits = 0
    old = ""

    for r in data:
      repos = repos+1
      for c in data[r]:
        commits = commits+1
        new = data[r][c]["keyword"]
        if new != old:
        # print(new)
          old = new
        
    print(str(repos) + " " + str(commits))
      
        
    print("\n\n")


if False:
      with open('PyCommitsWithDiffs.json', 'r') as infile:
        data = json.load(infile)
      print("Interesting: " + str(len(data)))

      repos = 0
      commits = 0


      keywords = {}

      for r in data:
        repos = repos+1
        for c in data[r]:
          commits = commits+1
          
          k =  data[r][c]["keyword"]
          if k not in keywords:
            keywords[k] = 0
          else:
            keywords[k] = keywords[k] +1
            
          
            
      print(str(repos) + " " + str(commits))
      print(keywords)

          
      print("\n\n")




#for vul in ["unauthorized","command_injection", "cross_frame_scripting","csv_injection", "execution_after_redirect","formatstring","path_disclosure","function_injection", "man-in-the-middle","replay_attack","sql","flooding", "tampering","sanitize","open_redirect","xss","xsrf","directory_traversal","remote_code_execution","spoof","hijack"]:
#for vul in ["sql","spoof"]:
for vul in ["unauthorized","command_injection", "cross_frame_scripting","csv_injection", "execution_after_redirect","formatstring","path_disclosure","function_injection", "man-in-the-middle","replay_attack","sql","flooding", "tampering","sanitize","open_redirect","xss","xsrf","directory_traversal","remote_code_execution","spoof","hijack","function_injection","remote_code_execution","cross_frame_scripting","csv_injection","execution_after_redirect"]:

  scfl = 0

  repos = 0
  commits = 0
  files = 0
  loc = 0
  functions = 0
#  print("\n"+vul)
  try:
    with open('data/plain_' + vul, 'r') as infile:
      data = json.load(infile)
          
          
      for r in data:
        repos = repos+1
        for c in data[r]:
          commits = commits+1
          for f in data[r][c]["files"]:
            files = files + 1
            source = data[r][c]["files"][f]["sourceWithComments"]
            scfl = scfl + len(source)
            loc = loc + countloc(source)
            functions = functions + source.count("def ")
      
      if commits < 50:
        print("Very little for " + vul + " " + str(commits))
      
#      print(str(repos) + " repos, " + str(commits) + " commits, " + str(files) + " files.")
#      print("length in chars: " + str(scfl))
#      print("loc: " + str(loc))
#      print("functions: " + str(functions))
      
#      print(str(repos) + " & " + str(files)+ " & " + str(loc)+ " & " + str(functions) + " & " + str(scfl) + "")
#      print("\n\n")
  except:
    continue
