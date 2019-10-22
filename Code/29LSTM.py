
import time
import sys
import json
#import StringIO
from io import StringIO
import subprocess
import time
import bs4 as bs  
import urllib.request  
import re  
import nltk
from gensim.models import Word2Vec, KeyedVectors
import numpy
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import LSTM
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.layers import Bidirectional
from keras.preprocessing import sequence
from tokenizer import tokenize
import builtins
import keyword
import pickle

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score


from matplotlib import pyplot 


mode = "command_injection"
modelw2v = "word2vec_withoutString.model"
modelw2v = "word2vecinterlaken.model"

if (len(sys.argv) > 1):
  mode = sys.argv[1]
  if (len(sys.argv) > 2):
    modelw2v = sys.argv[2]
    
    

w2v_model = Word2Vec.load(modelw2v)
word_vectors = w2v_model.wv

print("finished loading w2v model " + modelw2v)


    
    
with open('data2/' + mode + '_dataset-train-X-withDuplicates', 'rb') as fp:
    X_train =  numpy.array(pickle.load(fp))
    
with open('data2/' + mode + '_dataset-train-Y-withDuplicates', 'rb') as fp:
    y_train =  numpy.array(pickle.load(fp))

with open('data2/' + mode + '_dataset-validate-X-withDuplicates', 'rb') as fp:
    X_test =  numpy.array(pickle.load(fp))

with open('data2/' + mode + '_dataset-validate-Y-withDuplicates', 'rb') as fp:
    y_test = numpy.array(pickle.load(fp))
    
print(str(len(X_train)) + " datapoints in the training set.")
    
print(str(len(X_test)) + " datapoinst in the test set.")


csum = 0
for a in y_train:
  csum = csum+a
  
print("Share of good ones: "  + str(int((csum / len(X_train)) * 10000)/100) + "%")
  


max_length = 200


X_train = sequence.pad_sequences(X_train, maxlen=max_length)



X_test = sequence.pad_sequences(X_test, maxlen=max_length)



# create the model

#for x in X_train:
#  print("\n\n")
#  print(x)
#  for y in x:
#    print(len(y))

print(len(X_train))
print(len(X_test))


#EMBEDDING_DIM = 100
#embedding_matrix = numpy.zeros((len(w2v_model.wv.vocab) + 1, EMBEDDING_DIM))
#word_index = {token: token_index for token_index, token in enumerate(w2v_model.wv.index2word)} 



#for word, i in word_index.items():
#    embedding_vector = w2v_model[word]
#    if embedding_vector is not None:
#        # words not found in embedding index will be all-zeros.
#        embedding_matrix[i] = embedding_vector





#embedding_vecor_length = 32

model = Sequential()

#embedding_layer = Embedding(len(word_index) + 1,
#                            EMBEDDING_DIM,
#                            weights=[embedding_matrix],
#                            input_length=1000,
#                            trainable=False)
#model.add(Embedding(top_words, embedding_vecor_length, input_length=max_length))



#model.add(Conv1D(filters=128, kernel_size=20, padding='same', activation='relu')) #original: filters 32, kernel size 3
#model.add(MaxPooling1D(pool_size=3)) #little to no effect
model.add(LSTM(50)) #around 50 seems good
model.add(Dense(1, activation='sigmoid'))
#model.add(Dropout(0.1))
#model.add(Dropout(0.05))


#optimizers = ['rmsprop', 'adamax', 'adagrad', 'adam']
#for opt in optimizers:
#  print("===================")
#  print(opt)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=50, batch_size=128, validation_data=(X_test, y_test)) #epochs more are good, batch_size more is good


# evaluate the model
_, train_acc = model.evaluate(X_train, y_train, verbose=0)
_, test_acc = model.evaluate(X_test, y_test, verbose=0)
print('Train: %.3f, Test: %.3f' % (train_acc, test_acc))
# plot history
model.save('LSTM-' + mode + '-Dup.h5')  # creates a HDF5 file 'my_model.h5'
   

#pyplot.plot(history.history['loss'])
#pyplot.plot(history.history['val_loss'])
#pyplot.title('Model loss (no dropout)')
#pyplot.ylabel('Loss')
#pyplot.xlabel('Epoch')
#pyplot.legend(['train', 'validation'], loc='upper right')
#pyplot.savefig('lossNoDropout.png')



# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
# predict probabilities for test set
yhat_probs = model.predict(X_test, verbose=0)
# predict crisp classes for test set
yhat_classes = model.predict_classes(X_test, verbose=0)
# reduce to 1d array
yhat_probs = yhat_probs.flatten()
yhat_classes = yhat_classes.flatten()

# accuracy: (tp + tn) / (p + n)
accuracy = accuracy_score(y_test, yhat_classes)
print('Accuracy: %f' % accuracy)
# precision tp / (tp + fp)
precision = precision_score(y_test, yhat_classes)
print('Precision: %f' % precision)
# recall: tp / (tp + fn)
recall = recall_score(y_test, yhat_classes)
print('Recall: %f' % recall)
# f1: 2 tp / (2 tp + fp + fn)
f1 = f1_score(y_test, yhat_classes)
print('F1 score: %f' % f1)

print("Accuracy: %.2f%%" % (scores[1]*100))
print('Loss: {:0.3f}'.format(scores[0]))





























sys.exit()



print("-----------------")

wrong = {}
right = {}

sumlenwrong = 0
sumlenright = 0
nrwrong = 0
nrright = 0

index = 0
again = 0

stringofExamples = ""





index = 0
print(len(origVectorlist))
for index in range(0,len(origVectorlist)):
#for datapoint in X_test:
  index = index+1



  try:
    
    
    one = []

    vector = origVectorlist[index]
    one.append(vector)


    one = numpy.array(one)
    
    
    max_length = 200
    one = sequence.pad_sequences(one, maxlen=max_length)
    
    yhat_probs = model.predict(one, verbose=1)
    yhat_classes = model.predict_classes(one, verbose=1)
    
    if (int(yhat_classes[0][0]) != int(origValue[index])):
    
    
      print("wrong")
      ##wrong prediction
      nrwrong = nrwrong +1
      sumlenwrong = sumlenwrong + len(origPre[index]+origAfter[index])
      
      if origValue[index] == 1:
        stringofExamples = stringofExamples + "\n\nThought it was wrong, but it is correct."
      else:
        stringofExamples = stringofExamples + "\n\nThought it was correct, but it is flawed."
      
      print("adding more content")
      stringofExamples = stringofExamples + "\n" + origKey[index] + "\n"  + origPre[index] + "\n-------------------\n" + origAfter[index] + "\n" + "====================================================\n\n"
      print(yhat_probs)
      print(yhat_classes[0][0])
      
      print("actually:")  
     
      print(origValue[index])
      print(origKey[index])
      print(len(origPre[index]))
      print(len(origAfter[index]))
      again = again+1
      
      
      keyword = origKey[index]
      
      if keyword not in wrong:
        wrong[keyword] = 0
      else:
        wrong[keyword] = wrong[keyword]+1
    else:
      print("right")
      ##true prediction
      nrright = nrright +1
      sumlenright = sumlenright + len(origPre[index]+origAfter[index])
      keyword = origKey[index]
      if keyword not in right:
        right[keyword] = 0
      else:
        right[keyword] = right[keyword]+1
        
  except:
    continue
  
print(wrong)
print(right)


print("Wrong: " + str(nrwrong) + " " + str(sumlenwrong/(2*nrwrong)))
print("Right: " + str(nrright) + " " + str(sumlenright/(2*nrright)))

prefixes =["session fixation","dom injection","cross origin","unauthorized","unauthorised","infinite loo","xpath injection","brute force", "buffer overflow","cache overflow","command injection","cross frame scripting","csv injection","eval injection","execution after redirect","format string","path disclosure","function injection","man-in-the-middle","replay attack","session hijacking","smurf","sql injection","flooding","tampering","sanitize","sanitise","yaml.safe_load","denial of service","dos", "XXE","open redirect","vuln","CVE","XSS","ReDos","NVD","malicious","x-frame-options","cross site","exploit","directory traversal","rce","remote code execution","XSRF","cross site request forgery","click jack","clickjack"]

analysis = {}
for pre in prefixes:
  l = []
  l.append(0)
  l.append(0)
  analysis[pre] = l
  
  for key in wrong:
    if pre in key:
      analysis[pre][0] = analysis[pre][0]+wrong[key]
      
  for key in right:
    if pre in key:
      analysis[pre][1] = analysis[pre][1]+right[key]


for key in analysis:
  if (analysis[key][0] == 0):
    print(key + ": never wrong!")
  elif (analysis[key][1] == 0):
    print(key + ": never right!")
  else:
    print(key + ": " + str(analysis[key][1]) + " correct and " + str(analysis[key][0]) + " incorrect, that's a rate of " + str(float(100 * analysis[key][1]/(analysis[key][1] + analysis[key][0]))) + " percent correct predicted") 



text_file = open("WrongExamples.txt", "w")
text_file.write(stringofExamples)
text_file.close()





print("We were working with " + str(len(y_train)) + " train, " + (str(len(y_test))) + " test.")

print('Train: %.3f, Test: %.3f' % (train_acc, test_acc))

# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
# predict probabilities for test set
yhat_probs = model.predict(X_test, verbose=0)
# predict crisp classes for test set
yhat_classes = model.predict_classes(X_test, verbose=0)
# reduce to 1d array
yhat_probs = yhat_probs.flatten()
yhat_classes = yhat_classes.flatten()

# accuracy: (tp + tn) / (p + n)
accuracy = accuracy_score(y_test, yhat_classes)
print('Accuracy: %f' % accuracy)
# precision tp / (tp + fp)
precision = precision_score(y_test, yhat_classes)
print('Precision: %f' % precision)
# recall: tp / (tp + fn)
recall = recall_score(y_test, yhat_classes)
print('Recall: %f' % recall)
# f1: 2 tp / (2 tp + fp + fn)
f1 = f1_score(y_test, yhat_classes)
print('F1 score: %f' % f1)

print("Accuracy: %.2f%%" % (scores[1]*100))
print('Loss: {:0.3f}'.format(scores[0]))

model.save('data/' + mode + '_LSTM.h5')  # creates a HDF5 file 'my_model.h5'
   

print("-------------------")



#index = 0
#for datapoint in X_test:
#  index = index+1
#  print(datapoint)



  
#model.fit(X_train, y_train, epochs=50, batch_size=50, validation_data=(X_test, y_test))
#for prediction in model.predict(X_test):
#  print(prediction)

#validate['predicted_gender'] = ['m' if prediction[0] > prediction[1] else 'f' for prediction in model.predict(validate_x)]
#validate[validate['gender'] != validate['predicted_gender']].head()
