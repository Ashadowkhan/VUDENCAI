import myutils
from termcolor import colored
from datetime import datetime
import sys
from keras.models import load_model
from keras.preprocessing import sequence
from gensim.models import Word2Vec, KeyedVectors
import json
threshold = []
threshold1 = [0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1]
threshold2 = [0.9999,0.999,0.99,0.9,0.5,0.1,0.01,0.001,0.0001]


mode = "sql"
nr = "1"
fine = ""

if (len(sys.argv) > 1):
  mode = sys.argv[1]
  if len(sys.argv) > 2:
    nr = sys.argv[2]
    if len(sys.argv) > 3:
      fine = sys.argv[3]
      
if fine == "fine":
  threshold = threshold2
else:
  threshold = threshold1

mincount = 10
iterationen = 300
s = 200
w2v = "word2vec_"+"withString"+str(mincount) + "-" + str(iterationen) +"-" + str(s)
w2vmodel = "w2v/" + w2v + ".model"

w2v_model = Word2Vec.load(w2vmodel)
word_vectors = w2v_model.wv


step = 5
fulllength = 200
                

rep = ""
com = ""
myfile = ""
    
progress = 0
count = 0

step = 5
fulllength = 200


if (len(sys.argv) > 1):
  mode = sys.argv[1]
  if len(sys.argv) > 2:
    nr = sys.argv[2]
    if len(sys.argv) > 3:
      fine = sys.argv[3]

model = load_model('model/LSTM-'+mode+'.h5',custom_objects={'f1_loss': myutils.f1_loss, 'f1': myutils.f1})

with open('data/plain_' + mode, 'r') as infile:
  data = json.load(infile)
  

print("finished loading")  
  
if mode == "sql":
  if nr == "1":
    rep = "instacart/lore"
    com = "a0a5fd945a8bf128d4b9fb6a3ebc6306f82fa4d0"
    myfile = "/lore/io/connection.py"
  elif nr == "2":
    rep = "uktrade/export-wins-data"
    com = "307587cc00d2290a433bf74bd305aecffcbb05a2"
    myfile = "/wins/views/flat_csv.py"
  elif nr == "3":
    rep = "kyojuceles/mud"
    com = "47f5aa6aa2e82de7ce2a440aea870958edf0ae77"
    myfile = "/db/db_processor_mysql.py"
if mode == "xss":
  if nr == "1":
    rep = "dongweiming/lyanna"
    com = "fcefac79e4b7601e81a3b3fe0ad26ab18ee95d7d"
    myfile = "/models/comment.py"
  elif nr == "2":
    rep = "inveniosoftware/invenio-records"
    com = "361def20617cde5a1897c2e81b70bfadaabae608"
    myfile = "/invenio_records/admin.py"
  elif nr == "3":
    rep = "onefork/pontoon-sr"
    com = "fc07ed9c68e08d41f74c078b4e7727f1a0888be8"
    myfile = "/pontoon/batch/views.py"
if mode == "command_injection":
  if nr == "1":
    rep = "saltstack/salt"
    com = "ebdef37b7e5d2b95a01d34b211c61c61da67e46a"
    myfile = "/salt/modules/disk.py"
  elif nr == "2":
    rep = "Atticuss/ajar"
    com = "5ed8aba271ad20e6168f2e3bd6c25ba89b84484f"
    myfile = "/ajar.py"
  elif nr == "3":
    rep = "yasong/netzob"
    com = "557abf64867d715497979b029efedbd2777b912e"
    myfile = "/src/netzob/Simulator/Channels/RawEthernetClient.py"
if mode == "xsrf":
  if nr == "1":
    rep = "deepnote/notebook"
    com = "d7becafd593c2958d8a241928412ddf4ba801a42"
    myfile = "/notebook/files/handlers.py"
  elif nr == "2":
    rep = "wbrxcorp/forgetthespiltmilk"
    com = "51bed3f7f01079d91864ddc386a73eb3e1ca634b"
    myfile = "/frontend/app.py"
  elif nr == "3":
    rep = "tricycle/lesswrong"
    com = "ef303fe078c60d964e3f9e87d3da1a67fecd2c2b"
    myfile = "/r2/r2/models/account.py"
if mode == "remote_code_execution":
  if nr == "1":
    rep = "Scout24/monitoring-config-generator"
    com = "2191fe6c5a850ddcf7a78f7913881cef1677500d"
    myfile = "/src/main/python/monitoring_config_generator/yaml_tools/readers.py "
  elif nr == "2":
    rep = "ntc-chip-revived/ChippyRuxpin"
    com = "0cd7d78e4d806852fd75fee03c24cce322f76014"
    myfile = "/chippyRuxpin.py"
  elif nr == "3":
    rep = "johanbluecreek/reddytt"
    com = "bd037e882d675ea27b96d41faf0deeac6563695c"
    myfile = "/reddytt.py"
if mode == "path_disclosure":
  if nr == "1":
    rep = "fkmclane/python-fooster-web"
    com = "80202a6d3788ad1212a162d19785c600025e6aa4"
    myfile = "/fooster/web/file.py"
  elif nr == "2":
    rep = "zms-publishing/zms4"
    com = "3f28620d475220dfdb06f79787158ac50727c61a"
    myfile = "/ZMSItem.py"
  elif nr == "3":
    rep = "cuckoosandbox/cuckoo"
    com = "168cabf86730d56b7fa319278bf0f0034052666a"
    myfile = "/cuckoo/web/controllers/submission/api.py"
if mode == "open_redirect":
  if nr == "1":
    rep = "karambir/mozilla-django-oidc"
    com = "22b6ecb953bbf40f0394a8bfd41d71a3f16e3465"
    myfile = "/mozilla_django_oidc/views.py"
  elif nr == "2":
    rep = "nyaadevs/nyaa"
    com = "b2ddba994ca5e78fa5dcbc0e00d6171a44b0b338"
    myfile = "/nyaa/views/account.py"
  elif nr == "3":
    rep = "readthedocs/readthedocs.org"
    com = "e3bccfc582beb57800c33e4f0afe01351733f2a5"
    myfile = "/readthedocs/redirects/models.py"



for r in data:
  if  "https://github.com/"+rep ==r:
      for c in data[r]:
        if c == com:
          if "files" in data[r][c]:
              for f in data[r][c]["files"]:
                if myfile == f:                       
                    if "source" in data[r][c]["files"][f]:                          
                        allbadparts = []
                        sourcecode = data[r][c]["files"][f]["source"]
                        sourcefull = data[r][c]["files"][f]["sourceWithComments"]
                        
                        
                        for change in data[r][c]["files"][f]["changes"]:
                          badparts = change["badparts"]
                          
                          if (len(badparts) < 20):
                            for bad in badparts:
                              pos = myutils.findposition(bad,sourcecode)
                              if not -1 in pos:
                                allbadparts.append(bad)
                          
                        positions = myutils.findpositions(allbadparts,sourcefull)
                        commentareas = myutils.findComments(sourcefull)
                        myutils.getblocksVisual(mode, r, c, sourcefull, positions, commentareas, fulllength, step, nr, w2v_model, model, threshold, "labeled")

