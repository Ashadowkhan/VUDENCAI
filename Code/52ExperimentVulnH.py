import myutils
import sys
import os.path
import json
from datetime import datetime
import random
import pickle
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.preprocessing import sequence
from keras import backend as K
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.utils import class_weight
import tensorflow as tf
from gensim.models import Word2Vec, KeyedVectors




def f1(y_true, y_pred):
    y_pred = K.round(y_pred)
    tp = K.sum(K.cast(y_true*y_pred, 'float'), axis=0)
    tn = K.sum(K.cast((1-y_true)*(1-y_pred), 'float'), axis=0)
    fp = K.sum(K.cast((1-y_true)*y_pred, 'float'), axis=0)
    fn = K.sum(K.cast(y_true*(1-y_pred), 'float'), axis=0)

    p = tp / (tp + fp + K.epsilon())
    r = tp / (tp + fn + K.epsilon())

    f1 = 2*p*r / (p+r+K.epsilon())
    f1 = tf.where(tf.is_nan(f1), tf.zeros_like(f1), f1)
    return K.mean(f1)

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
  

def f1(y_true, y_pred):
    def recall(y_true, y_pred):
        """Recall metric.

        Only computes a batch-wise average of recall.

        Computes the recall, a metric for multi-label classification of
        how many relevant items are selected.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

    def precision(y_true, y_pred):
        """Precision metric.

        Only computes a batch-wise average of precision.

        Computes the precision, a metric for multi-label classification of
        how many selected items are relevant.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision
    precision = precision(y_true, y_pred)
    recall = recall(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))






mode = "sql"


if (len(sys.argv) > 1):
  mode = sys.argv[1]



progress = 0
count = 0
output = ""



#for mode in ["unauthorized","command_injection", "cross_frame_scripting","csv_injection", "execution_after_redirect","formatstring","path_disclosure","function_injection", "man-in-the-middle","replay_attack","sql","flooding", "tampering","sanitize","open_redirect","xss","xsrf","directory_traversal","remote_code_execution","spoof","hijack","function_injection","remote_code_execution","cross_frame_scripting","csv_injection"]:
#for mode in ["sql","flooding", "tampering","sanitize","open_redirect","xss","xsrf","directory_traversal","remote_code_execution","spoof","hijack", "function_injection","remote_code_execution","cross_frame_scripting","csv_injection","unauthorized","command_injection", "cross_frame_scripting", "csv_injection", "execution_after_redirect","formatstring","path_disclosure","function_injection", "man-in-the-middle","replay_attack",]:

for mode in ["sql"]:
  for restriction in [[10000,2,2,3]]:
      print(restriction)
#for mode in ["remote_code_execution","hijack"]:
#for mode in ["tampering","sanitize","open_redirect","directory_traversal"]:
#for mode in ["formatstring","path_disclosure","function_injection","man-in-the-middle"]:
      if mode in ["brute_force","session_fixation","cross_origin","csv_injection","cross_frame_scripting","buffer_overflow","cache_overflow","brute_force","eval_injection","session_hijacking","smurf","denial_of_service","clickjack"]:
        print(mode + " -- don't do this")
        continue
      
    #  if os.path.isfile('model/LSTM'+mode+'2.h5'):
    #    print(mode + " already done.")
    #    continue

      for param in [[5,200]]:
      #  for mincount in [10,30,50,100,300,500,5000]:
      #  for mincount in [5000,500,300,100,30,10]:
      #  for mincount in [10]:
        for mincount in [10]:
          for iterationen in [300]:
      #    for iterationen in [1,10,100,30]:
        #  for iterationen in [100]:
        #    for s in [5,10,15,30,50,75,100,200,300]:
            for s in [200]:
      #        for w in ["withoutString","withString"]:
              for w in ["withString"]:

                      
                      output = output + "\n\n--------------------------\n"+mode+"\n"
                      
                      
                      print("\n")
                      print("=================Train in place (VULNERABILITIES " + mode +")======================================")
                      now = datetime.now() # current date and time
                      nowformat = now.strftime("%H:%M")
                      print("mode: " + mode + " ", nowformat)
                      
                      w2v = "word2vec_"+w+str(mincount) + "-" + str(iterationen) +"-" + str(s)
                      w2vmodel = "w2v/" + w2v + ".model"
                      step = param[0]
                      fulllength = param[1]
                      mode2 = str(step)+"_"+str(fulllength) 
                      filename = 'data/plain_' + mode + '_dataset-train-X_'+w2v + "__" + mode2
                      
                    
                    
                      if not (os.path.isfile(w2vmodel)):
                        print("word2vec model is still being created...")
                        continue
                      
                      
                                            
                                            
                      now = datetime.now() # current date and time
                      nowformat = now.strftime("%H:%M")
                      print("loading data. ", nowformat)


                      with open('data/plain_' + mode, 'r') as infile:
                        data = json.load(infile)


                      now = datetime.now() # current date and time
                      nowformat = now.strftime("%H:%M")
                      print("finished loading. ", nowformat)
                      
                      w2v_model = Word2Vec.load(w2vmodel)
                      word_vectors = w2v_model.wv
                      allblocks = []


                      
                      for r in data:

                        progress = progress + 1
                        for c in data[r]:
                          
                          if "files" in data[r][c]:
#                            print(r + "/commit/" + c + "(" + str(len(data[r][c]["files"])) + " files)")
                           
                            if len(data[r][c]["files"])> restriction[3]:
                              print("too many files")
                              continue
                            
                            for f in data[r][c]["files"]:
                              
                              if len(data[r][c]["files"][f]["changes"]) >= restriction[2]:
                                continue
                              
                              #print(" file " + f + " with " + str(len(data[r][c]["files"][f]["changes"])) + " changes")
                              
                              if not "source" in data[r][c]["files"][f]:
                                continue
                              if "source" in data[r][c]["files"][f]:
                                
                                sourcecode = data[r][c]["files"][f]["source"]
                                #print("\n\n" + r + "/commit/" + c)
                                #print("    " + f)
                                
                                if len(sourcecode) > restriction[0]:
                                  #print("sourcecode is too long.")
                                  continue
                                
                                allbadparts = []
                                
                                foundMeaningful = False
                                
                                for change in data[r][c]["files"][f]["changes"]:
                                  badparts = change["badparts"]
                                #  print("  " + str(len(badparts)) + " badparts (total " + str(len(allbadparts))+ ")")

                                  count = count + len(badparts)
                                  if len(badparts) > restriction[2]:
                                    break
                                  
                                  for bad in badparts:
                                    pos = myutils.findposition(bad,sourcecode)
                                    if not -1 in pos:
                                        allbadparts.append(bad)
                                        #print(str(pos) + "   "  + bad.replace("\n"," ").lstrip())
                                        
                                  if (len(allbadparts) > restriction[2]):
                                 #   print("    stop it here")
                                    break
                                
                              
                                if(len(allbadparts) > 0):
                                  #print("    " + str(len(allbadparts)) + " bad parts in source code of length " + str(len(sourcecode)) + " for file " + f)
                                 # if len(allbadparts) >= restriction[2]:
                                   # print("    too many.")
                                  if len(allbadparts) < restriction[2]:
                                    positions = myutils.findpositions(allbadparts,sourcecode)
                                    #print("  " + str(positions) + "  positions")
                                    blocks = myutils.getblocks(sourcecode, positions, step, fulllength)
                                    
                                    for b in blocks:
                                        #print(b)
                                        allblocks.append(b)
                      #          time.sleep(0.5)

                      vulcount = 0
                      for b in allblocks:
                        if b[1] == 0:
                          vulcount = vulcount + 1
                                  
      #                print("badparts: " + str(count))
      #                print("step length: "  + str(step))
      #                print("full length: " + str(fulllength))
      #                print("Blocks: "+str(len(allblocks)))
      #                print("vulnerable blocks: " + str(vulcount))
      #                 print("\n\n\n")


                      keys = []

                      for i in range(len(allblocks)):
                        keys.append(i)
                        


                      random.shuffle(keys)


                      cutoff = round(0.8 * len(keys))
                      cutoff2 = round(0.999 * len(keys))


                      keystrain = keys[:cutoff]
                      keystest = keys[cutoff:cutoff2]
                      keysfinaltest = keys[cutoff2:]

      #                newcutoff = round(0.8 * len(keys))
      #                keystrain = keys[:cutoff]
      #                keystest = keys[cutoff:]




                      TrainX = []
                      TrainY = []
                      ValidateX = []
                      ValidateY = []
                      FinaltestX = []
                      FinaltestY = []


                            



                      print("Creating training dataset...")
                      for k in keystrain:
                        block = allblocks[k]
                        
                        code = block[0]
                        token = myutils.getTokens(code)
                        vectorlist = []
                        for t in token:
                          if t in word_vectors.vocab and t != " ":
                            vector = w2v_model[t]
                            vectorlist.append(vector.tolist()) 
                        TrainX.append(vectorlist)
                        TrainY.append(block[1])


                      print("Creating validation dataset...")
                      for k in keystest:
                        block = allblocks[k]
                        code = block[0]
                        token = myutils.getTokens(code)
                        vectorlist = []
                        for t in token:
                          if t in word_vectors.vocab and t != " ":
                            vector = w2v_model[t]
                            vectorlist.append(vector.tolist()) 
                        ValidateX.append(vectorlist)
                        ValidateY.append(block[1])




                     # print("Creating finaltest dataset...")
                     # for k in keysfinaltest:
                     #   block = allblocks[k]  
                     #   code = block[0]
                     #   token = myutils.getTokens(code)
                     #   vectorlist = []
                     #   for t in token:
                     #     if t in word_vectors.vocab and t != " ":
                     #       vector = w2v_model[t]
                     #       vectorlist.append(vector.tolist()) 
                     #   FinaltestX.append(vectorlist)
                     #   FinaltestY.append(block[1])





                    
                      print("Train length: " + str(len(TrainX)))
                      print("Test length: " + str(len(ValidateX)))
                      print("Finaltesting length: " + str(len(FinaltestX)))
                      now = datetime.now() # current date and time
                      nowformat = now.strftime("%H:%M")
                      print("time: ", nowformat)


                  #    with open('data/plain_' + mode + '_dataset-train-X_'+w2v + "__" + mode2, 'wb') as fp:
                  #      pickle.dump(TrainX, fp)
                  #    with open('data/plain_' + mode + '_dataset-train-Y_'+w2v + "__" + mode2, 'wb') as fp:
                  #      pickle.dump(TrainY, fp)
                  #    with open('data/plain_' + mode + '_dataset-validate-X_'+w2v + "__" + mode2, 'wb') as fp:
                  #      pickle.dump(ValidateX, fp)
                  #    with open('data/plain_' + mode + '_dataset-validate-Y_'+w2v + "__" + mode2, 'wb') as fp:
                  #      pickle.dump(ValidateY, fp)
                  #    with open('data/plain_' + mode + '_dataset-finaltest-X_'+w2v + "__" + mode2, 'wb') as fp:
                  #      pickle.dump(FinaltestX, fp)
                  #    with open('data/plain_' + mode + '_dataset-finaltest-Y_'+w2v  + "__" + mode2, 'wb') as fp:
                  #      pickle.dump(FinaltestY, fp)
                  #    print("saved finaltest.")
      
                       


                          
                      output = output + "\nTrain length: " + str(len(TrainX))
                      output = output + "\nTest length: " + str(len(ValidateX))

                        
                        
            

                      X_train =  numpy.array(TrainX)
                      y_train =  numpy.array(TrainY)
                      X_test =  numpy.array(ValidateX)
                      y_test =  numpy.array(ValidateY)
            
                      for i in range(len(y_train)):
                        if y_train[i] == 0:
                          y_train[i] = 1
                        else:
                          y_train[i] = 0
                          
                      for i in range(len(y_test)):
                        if y_test[i] == 0:
                          y_test[i] = 1
                        else:
                          y_test[i] = 0

                      now = datetime.now() # current date and time
                      nowformat = now.strftime("%H:%M")
                      print("numpy array done. ", nowformat)
                      
                      print(str(len(X_train)) + " samples in the training set.")
                          
                      print(str(len(X_test)) + " samples in the test set.")
                        
              
                      csum = 0
                      for a in y_train:
                        csum = csum+a
                        
                      print("percentage of vulnerable samples: "  + str(int((csum / len(X_train)) * 10000)/100) + "%")
                      output = output + "\npercentage of vulnerable samples: " + str(int((csum / len(X_train)) * 10000)/100) + "%"
                        
                      testvul = 0
                      for y in y_test:
                        if y == 1:
                          testvul = testvul+1
                      print("absolute amount of vul in test set: " + str(testvul))

                      max_length = fulllength 
                        
                      for dropout in [0.2]:
#                        for neurons in [100]:
                        for neurons in [30]:
                          for optimizer in ["adam"]:
                          #optimizers = ['rmsprop', 'adamax', 'adagrad', 'adam']
                            for epochs in [20]:
                              for batchsize in [128]:
                              #for batchsize in [200]:
                      
                                now = datetime.now() # current date and time
                                nowformat = now.strftime("%H:%M")
                                print("Starting LSTM: ", nowformat)

                                
                                print("Dropout: " + str(dropout))
                                print("Neurons: " + str(neurons))
                                print("Optimizer: " + optimizer)
                                print("Epochs: " + str(epochs))
                                print("Batch Size: " + str(batchsize))
                                print("max length: " + str(max_length))


                                X_train = sequence.pad_sequences(X_train, maxlen=max_length)
                                X_test = sequence.pad_sequences(X_test, maxlen=max_length)
                                
                                now = datetime.now() # current date and time
                                nowformat = now.strftime("%H:%M")
                                print("padded sequences. ", nowformat)

                                model = Sequential()
                                model.add(LSTM(neurons, dropout = dropout, recurrent_dropout = dropout)) #around 50 seems good
                                model.add(Dense(1, activation='sigmoid'))

                                model.compile(loss=f1_loss, optimizer='adam', metrics=[f1])
                                
                                
                                
                                
                                
                                now = datetime.now() # current date and time
                                nowformat = now.strftime("%H:%M")
                                print("Compiled LSTM: ", nowformat)
                                
                                class_weights = class_weight.compute_class_weight('balanced',numpy.unique(y_train),y_train)
                                
                                now = datetime.now() # current date and time
                                nowformat = now.strftime("%H:%M")
                                print("Fitting model...  ", nowformat)
                                
                                history = model.fit(X_train, y_train, epochs=epochs, batch_size=batchsize, class_weight=class_weights) #epochs more are good, batch_size more is good
                                
                                x = 0
                                  
                                for dataset in ["train","test"]:
                                    print("Now predicting on " + dataset + " set (" + str(dropout) + " dropout)")
                                    output = output + "\n" +  dataset + " set (" + str(dropout) + " dropout)\n"

                                    if dataset == "train":
                                      yhat_classes = model.predict_classes(X_train, verbose=0)
                                    
                                      accuracy = accuracy_score(y_train, yhat_classes)
                                      precision = precision_score(y_train, yhat_classes)
                                      recall = recall_score(y_train, yhat_classes)
                                      F1Score = f1_score(y_train, yhat_classes)
                                      
                                    if dataset == "test":

                                      yhat_classes = model.predict_classes(X_test, verbose=0)
                                        
                                        
                                      accuracy = accuracy_score(y_test, yhat_classes)
                                      precision = precision_score(y_test, yhat_classes)
                                      recall = recall_score(y_test, yhat_classes)
                                      F1Score = f1_score(y_test, yhat_classes)

                                    
                                    output = output+"\nAccuracy " + str(accuracy)
                                    output = output+"\nPrecision " + str(precision)
                                    output = output+"\nRecall " + str(recall)
                                    output = output+"\nF1 " + str(F1Score)
                                    output = output+"\n"
                                    print("Accuracy: " + str(accuracy))
                                    print("Precision: " + str(precision))
                                    print("Recall: " + str(recall))
                                    print('F1 score: %f' % F1Score)
                                  
                                    print("\n\n")
                                      
                                  
                                  


                                now = datetime.now() # current date and time
                                nowformat = now.strftime("%H:%M")
                                print("saving results (" + mode + "). ", nowformat)
                                
                                for i in range(0,100):
                                    if not os.path.isfile('OutputVulnX'+str(i)+'.txt'):
                                      with open('OutputVulnX' + str(i) + '.txt', 'w') as outputfile:
                                        outputfile.write(output)
                                      break
                                
                                now = datetime.now() # current date and time
                                nowformat = now.strftime("%H:%M")
                                print("saving LSTM model " + mode + ". ", nowformat)
                                model.save('model/LSTM'+mode+'.h5')  # creates a HDF5 file 'my_model.h5'

                                #print("\n\n")
                                

                                
