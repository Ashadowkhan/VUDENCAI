import myutils
from termcolor import colored
from datetime import datetime
import os
import sys
import numpy
from keras.models import load_model
from keras import backend as K
from keras.preprocessing import sequence
from gensim.models import Word2Vec, KeyedVectors
import tensorflow as tf
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#Define F1 loss and measurement

def f1_loss(y_true, y_pred):
    
    tp = K.sum(K.cast(y_true*y_pred, 'float'), axis=0)
    tn = K.sum(K.cast((1-y_true)*(1-y_pred), 'float'), axis=0)
    fp = K.sum(K.cast((1-y_true)*y_pred, 'float'), axis=0)
    fn = K.sum(K.cast(y_true*(1-y_pred), 'float'), axis=0)

    p = tp / (tp + fp + K.epsilon())
    r = tp / (tp + fn + K.epsilon())

    f1 = 2*p*r / (p+r+K.epsilon())
    f1 = tf.where(tf.is_nan(f1), tf.zeros_like(f1), f1)
    return 1 - K.mean(f1)

def predict(vectorlist): 
  
  if (len(vectorlist) > 0):
    one = []
    one.append(vectorlist)
    one = numpy.array(one)
    max_length = 200
    one = sequence.pad_sequences(one, maxlen=max_length)
    yhat_probs = model.predict(one, verbose=0)
    prediction = int(yhat_probs[0][0] * 100000)
    prediction = 0.00001 * prediction 
    return prediction
    
  else:
    return -1




def getblocksVisual(mode,r,c,sourcecode, badpositions,commentareas, fulllength,step, nr,w2v_model,threshold):
  
  
      ypos = 0
      xpos = 0
      lines = (sourcecode.count("\n"))
      #print("lines: " + str(lines))
      img = Image.new('RGB', (2000, 11*(lines+1)))
      color = "white"
      
      
          
      
      
      
      blocks = []
       
      focus = 0
      lastfocus = 0
      
      string = ""
      
      trueP = False
      falseP = False
      
      while (True):
        if focus > len(sourcecode):
          break
        
        
        
        comment = False
        for com in commentareas:
          
          if (focus >= com[0] and focus <= com[1] and lastfocus >= com[0] and lastfocus < com[1]):
                focus = com[1]
                #print("within")
                comment = True
          if (focus > com[0] and focus <= com[1] and  lastfocus < com[0]):
              focus = com[0]
              #print("before")
              comment = False                   
          elif (lastfocus >= com[0] and lastfocus < com[1] and focus > com[1]):
              focus = com[1]
              #print("up to the end")
              comment = True
      
        #print([lastfocus,focus,comment, "["+sourcecode[lastfocus:focus]+"]"])
        focusarea = sourcecode[lastfocus:focus]
     
        if(focusarea == "\n"):
          string = string + "\n"
          
        else:
          if comment:
              color = "grey"
              string = string + colored(focusarea,'grey')
          else:
              
              
              middle = lastfocus+round(0.5*(focus-lastfocus))              
              context = myutils.getcontextPos(sourcecode,middle,fulllength)
              
              
              if context is not None:
              
                vulnerablePos = False
                for bad in badpositions:
                    if (context[0] > bad[0] and context[0] <= bad[1]) or (context[1] > bad[0] and context[1] <= bad[1]) or (context[0] <= bad[0] and context[1] >= bad[1]):
                      vulnerablePos = True
                      
                predictionWasMade = False
                text = sourcecode[context[0]:context[1]].replace("\n", " ")
                token = myutils.getTokens(text)
                if (len(token) > 1):                  
                  vectorlist = []                  
                  for t in token:
                    if t in word_vectors.vocab and t != " ":
                      vector = w2v_model[t]
                      vectorlist.append(vector.tolist())   
                      
                  if len(vectorlist) > 0:
                      p = predict(vectorlist)
                      if p >= 0:
                        predictionWasMade = True
                        
                      #  print(p)
                        if vulnerablePos:
                          if p > 0.5:
                            color = "royalblue"
                            string = string + colored(focusarea,'cyan')
                          else:
                            string = string + colored(focusarea,'magenta')
                            color = "violet"
                            
                        else:
                          
                        
                          if p > threshold[0]:
                            color = "darkred"
                          elif p >  threshold[1]:
                            color = "red"
                          elif p >  threshold[2]:
                            color = "darkorange"
                          elif p >  threshold[3]:
                            color = "orange"
                          elif p >  threshold[4]:
                            color = "gold"
                          elif p >  threshold[5]:
                            color = "yellow"
                          elif p >  threshold[6]:
                            color = "GreenYellow"
                          elif p >  threshold[7]:
                            color = "LimeGreen"
                          elif p >  threshold[8]:
                            color = "Green"
                          else:
                            color = "DarkGreen"
                
                          if p > 0.8:
                            string = string + colored(focusarea,'red')
                          elif p > 0.5:
                            string = string + colored(focusarea,'yellow')
                          else:
                            string = string + colored(focusarea,'green')
                            
                if not predictionWasMade:
                  string = string + focusarea
              else:
                string = string + focusarea
                
        
        
            
        try:
          if len(focusarea) > 0:
            d = ImageDraw.Draw(img)
#            print(list(focusarea))
            if focusarea[0] == "\n":
              ypos = ypos + 11
              xpos = 0
              d.text((xpos, ypos), focusarea[1:], fill=color)
              xpos = xpos + d.textsize(focusarea)[0]
            else:
              d.text((xpos, ypos), focusarea, fill=color)
              xpos = xpos + d.textsize(focusarea)[0]

        except Exception as e:
          print(e)

        if ("\n" in sourcecode[focus+1:focus+7]):
          lastfocus = focus
          focus = focus + sourcecode[focus+1:focus+7].find("\n")+1
        else:
          if myutils.nextsplit(sourcecode,focus+step) > -1:
            lastfocus = focus
            focus = myutils.nextsplit(sourcecode,focus+step)
          else:
            if focus < len(sourcecode):
              lastfocus = focus
              focus = len(sourcecode)
            else:
              break

      
      
      print(string)
      
      for i in range(0,100):
        if not os.path.isfile('demo_' + mode + "_" + str(i) + '.png'):
                img.save('demo_' + mode + "_" + str(i) + '.png')    
                break
      return blocks


  




#==========================================================================================================

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
  
mode2 = mode + nr

now = datetime.now() # current date and time
nowformat = now.strftime("%H:%M")
print("time:", nowformat)


mincount = 10
iterationen = 300
s = 200
w2v = "word2vec_"+"withString"+str(mincount) + "-" + str(iterationen) +"-" + str(s)
w2vmodel = "w2v/" + w2v + ".model"
w2v_model = Word2Vec.load(w2vmodel)
word_vectors = w2v_model.wv
                
model = load_model('model/LSTM'+mode+'.h5',custom_objects={'f1_loss': f1_loss, 'f1':f1})



with open('examples/'+mode+"-"+nr+".py", 'r') as infile:
  sourcecodefull = infile.read()


commentareas = myutils.findComments(sourcecodefull)
getblocksVisual(mode2,"","",sourcecodefull, [], commentareas, 200,5, 0, w2v_model,threshold2)

