
#import tokenizer

import sys

import StringIO
import subprocess
import time

f=open("w2v/pythontraining.txt", "r")
contents =f.read()
contents = contents.replace('\t', '    ')

if 'PositiveSmallIntegerField(\n                choices' in contents:
    pos = contents.find('PositiveSmallIntegerField(\n                choices')
    #print("\n\n" + contents[pos-198:pos+178])
    #print(list(contents[pos-198:pos+178]))
    contents = contents[:pos-198] + contents[pos+178:]


if "            raise ImportError,self.__dict__.get('_ppimport_exc_info')[1]" in contents:
  pos = contents.find("            raise ImportError,self.__dict__.get('_ppimport_exc_info')[1]")
  length = len("            raise ImportError,self.__dict__.get('_ppimport_exc_info')[1]")
  contents = contents[:pos] + contents[pos+length+1:]


if "[k]*step+start)" in contents:
  pos = contents.find("[k]*step+start)")
#    print("\n\n" + contents[pos-400:pos+300])
#    print(list(contents[pos+17:pos+21]))
  contents = contents[:pos+17] + contents[pos+21:]

  
badstring = ["silly_field", "('id', models.AutoField(primary_key=True))"]

while "check_framework.Model2." in contents:
  pos = contents.find("check_framework.Model2.")
  area = contents[pos-300:pos+300]
  start = area.find("class")
  end = area.find("def")
  
#    print(len(contents))
  contents = contents[:pos-300+start] + contents[pos-300+end:]
#    print(len(contents))
#    print("\n\n")

fromhere = 0
while "DEFAULT_KMS_KEY_NAME" in contents[fromhere:] and "ENCRYPTION_CONFIG" in contents[fromhere:fromhere+2000]:
  pos = fromhere + contents[fromhere:].find("DEFAULT_KMS_KEY_NAME")
  area = contents[pos-1000:pos+1000]
  start = area[:1000].find("class")
  if (start == -1):
    start = area[:1000].find("from")
  if (start == -1):
    start = area[:1000].find("import")
  if (start == -1):
    start = area[:1000].find("def")
    
  end = area[1000:].find("def")
  if (end == -1):
    end = area[1000:].find("from")
  if (end == -1):
    end = area[1000:].find("import")
  
  print("Found it at  " + str(pos))
#    print(len(contents))
  if (start > 0 and end > 0):
    contents = contents[:pos-1000+start] + contents[pos-1000+end:]
    fromhere = pos-1000+start+end+1
    print("countinue at " + str(fromhere))
    print(start)
    print(end)
  else:
#      print("=================")
#      print(start)
#      print(end)
#      print(area[:1000] + "\n\n" + area[1000:])
#      print(area.find("from"))
#      print(area.find("import"))
#      print(area.find("def"))
#      print(area.find("class"))
    fromhere = pos + 1000
#    print(len(contents))
#    print("\n\n")
  
  
fromhere = 0
while "somepassword" in contents[fromhere:]:
  pos = fromhere + contents[fromhere:].find("somepassword")
  #print(pos)
  #print("apparently still one in there at position "  + str(pos))
  area = contents[pos-1000:pos+1000]
  start = area.find("def")
  end = area[1000:].find("def")
  if (end == -1):
    end = area[1000:].find("from")
  if (end == -1):
    end = area[1000:].find("import")
  
  #print(str(start) + " to " + str(end) + " shall be deleted.")
  #print("Length: " + str(len(contents)))
  if start > 0 and end > 0:
    contents = contents[:pos-1000+start] + contents[pos+end:]
    fromhere = pos-1000+start
    #print("After deletion: " + str(len(contents)))

  else:
    fromhere = pos + 1
  # print("new position: " + str(fromhere))
  # print("\n\n")
  
  
if "somepassword" in contents and "someuser" in contents and "somehost" in contents:
  pos = contents.find("somepassword")
  #print(pos)
  #print("\n\n" + contents[pos-1000:pos+1000])
#    print(list(contents[pos+17:pos+21]))
#    contents = contents[:pos+17] + contents[pos+21:]

for x in badstring:
  while(x in contents):    
    
    
    pos = contents.find(x)    
    area = contents[pos-500:pos+1000]        
    
    if("db.create_table" in area):
      contents = contents.replace("('id', models.AutoField(primary_key=True))","('id', models.AutoField(primary_key=False))",1)
      continue
    
    start = area.find("class")    
    restarea = area[start:]    
    end = restarea.find("from") + start
    end2 = restarea.find("import") + start    
    if end2 < end:
      end = end2 
    if (end > start):
      contents = contents[:pos-500+start] + contents[pos-500+end:]
 
 
f = open("w2v/pythontraining_edit.txt", "w")
f.write(contents)
f.close()    
