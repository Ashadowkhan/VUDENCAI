from pydriller import RepositoryMining
import requests
import time
import requests
import sys
import json
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1


def searchforkeyword(key, commits, x):
  new = 0
  print(str(x) + " commits analyzed")
  print("keyword " + key)
  params = (
      ('q', key),('per_page',100)
  )

  headers = {'Accept': 'application/vnd.github.cloak-preview'}

  myheaders = {'Accept': 'application/vnd.github.cloak-preview', 'Authorization': 'token ' + '62b91a7aab880263d42d98159b3dcac407891972'}
  maximum = 9999
  nextlink = "https://api.github.com/search/commits"

  for i in range(0,maximum):
      #print(k)
      
      #print(nextlink)

      
      limit = 0
      while(limit == 0):
          response = requests.get(nextlink, headers=myheaders,params=params)
          h = response.headers
          if 'X-RateLimit-Remaining' in h:
            limit = int(h['X-RateLimit-Remaining'])
            if limit == 0:
                print("we have to sleep a while because of the rate limit.")
                time.sleep(35)
            else:
              print(h)
            
#      print(response.headers)
      #print("\n\n")
      if 'Link' not in h:
        #print(h)
        break;
      link = h['Link']
      reflinks = analyzelinks(link)
      content = response.json()
      
      for k in range(0, len(content["items"])):
          repo = content["items"][k]["repository"]["html_url"]
          
          
          
          
          x = x+1
          
          if repo not in commits:
              #print("added repository, now at " + str(len(repos)))
              
              c = {}
              c["url"] = content["items"][k]["url"]
              c["html_url"] = content["items"][k]["html_url"]
              c["message"] = content["items"][k]["commit"]["message"]
              c["sha"] = content["items"][k]["sha"]
              c["keyword"] = key
              commits[repo] = {}
              commits[repo][content["items"][k]["sha"]] = c;
              
              
          
          else:
              if content["items"][k]["sha"] in commits[repo]:
                a = 0 #noop
                #print("already known.")
              else:
                print("This is new.")
                new = new + 1
                c = {}
                c["url"] = content["items"][k]["url"]
                c["html_url"] = content["items"][k]["html_url"]
                c["sha"] = content["items"][k]["sha"]
                c["keyword"] = key
                commits[repo][content["items"][k]["sha"]] = c;
              
                    
      if "last" in reflinks:
          lastnumber = reflinks["last"].split("&page=")[1]
          maximum = int(lastnumber)-1
      
      

      #print("We collected " + str(len(repos)) + " repositories.")


   #   with open('reposfound.json', 'w') as outfile:
   #       json.dump(reposfound, outfile)

    #  print("number of repositories: " + str(len(repos)))



      if not "next" in reflinks:
          #print("Apparently we are done")
          break
      else:
          
          nextlink = reflinks["next"]
          
  print((str(new))+ " new commits found.")    
  with open('all_commits2.json', 'w') as outfile:
      json.dump(commits, outfile)
  return(x)






        
def analyzelinks(link):
    
    link = link + ","
    reflinks = {}
    
    while "," in link:
      
        
        pos = link.find(",")
        text = link[:pos]
        rest = link[pos+1:]
        
        
        try:
          if "\"next\"" in text:
              text = text.split("<")[1]
              text = text.split(">;")[0]
              reflinks["next"]=text
          if "\"prev\"" in text:
              text = text.split("<")[1]
              text = text.split(">;")[0]
              reflinks["prev"]=text
          if "\"first\"" in text:
              text = text.split("<")[1]
              text = text.split(">;")[0]
              reflinks["first"]=text
          if "\"last\"" in text:
              text = text.split("<")[1]
              text = text.split(">;")[0]
              reflinks["last"]=text
              
        except IndexError as e:
            print(e)
            print("\n")
            print(text)
            print("\n\n")
            sys.exit()
        link = rest
            
    return(reflinks)





#print("test")


#client_key = 'asoiaf'
#client_secret = 'asoidjawoi'
#request_token_url = 'https://api.github.com/user'



#sys.exit()

commits = {}
with open('all_commits2.json', 'r') as infile:
    commits = json.load(infile)
    

done = ["session fixation","dom injection","cross origin","unauthorized","unauthorised","infinite loo","xpath injection","brute force"]
keywords =  ["buffer overflow","cache overflow","command injection","cross frame scripting","csv injection","eval injection","execution after redirect","format string","path disclosure","function injection","man-in-the-middle","replay attack","session hijacking","smurf","sql injection","flooding","tampering","sanitize","sanitise","yaml.safe_load","denial of service", "dos", "XXE","open redirect","vuln","CVE","XSS","ReDos","NVD","malicious","x-frame-options","cross site","exploit","directory traversal","rce","remote code execution","XSRF","cross site request forgery","click jack","clickjack"]

prefixes =["prevent", "fix", "attack", "protect", "issue", "correct", "update", "improve", "change", "check"]

masterkeywords = ["malicious", "insecure", "vulnerable", "vulnerability"]

used = []
vaguekeywords = [  "pickle","dos","path traversal","spoof", "hijack"]


x = 0

for k in keywords:
  for pre in prefixes:
      x = searchforkeyword(k + " " + pre, commits, x);
  for master in masterkeywords:
      x = searchforkeyword(k + " " + master, commits, x);
      
for v in vaguekeywords:
  for pre in prefixes:
      x = searchforkeyword(v + " " + pre, commits, x);

with open('all_commits2.json', 'w') as outfile:
    json.dump(commits, outfile)
