# Vulnerability Detection with Github and Long Short Term Memory Networks

This code is part of a project and master thesis with the goal to scrape a lot of security related commits from github, process them and train a deep neural network on classifying code into vulnerable and not vulnerable.




### Training the Word2Vec model

The word2vec model is trained on a large set of python code which is simply concatenated. 


First, the code has to be downloaded. The Repository Mining from pydriller is used to accomplish this task.

```
python3 10python-for-training.py
```

The results are saved in the file pythontraining.txt.

Since there are syntax and indentation errors in those files, the following script fixes those:

```
python3 11RemoveProblems.py
```

The results are saved in pythontraining_edit.txt.

Then, the python tokenizer is applied to retrieve the python source code tokens.
The mode can be set in the file to be either "withString" or "withoutString". Without string would indicate that all strings are replaced by a generic string token, while the other option (with string) leaves them as they are.

```
python3 11TokenizerPythoncode.py
```

The results of that step are saved as a bunch of files of the form 'pythontraining_withString_39.py' etc. This is because to save a lot of large files often is relatively slow. The outputs are merged into a single file with:


```
python3 11tokenizerMerge.py
```

... which creates the file pythontraining_withString_X.py or pythontraining_withoutString_X.py, respectively.

Finally, the word2vec model can be trained.


```
python3 23w2v1.py
```

This trains a word2vec model on the code and saves it.

It can be tried out like this just to play around with it a little:

```

>>> from gensim.models import Word2Vec, KeyedVectors
>>> model = Word2Vec.load("w2v/word2vec_withoutString1000-200.model")
>>> model.wv.most_similar("if")
[('elif', 0.7818458676338196), ('and', 0.7453325986862183), ('or', 0.687163233757019), ('assert', 0.6153841614723206), ('raise', 0.42978066205978394), ('continue', 0.3989405632019043), ('other', 0.3266211152076721), ('logger', 0.32225584983825684), ('logging', 0.3215404748916626), ('else', 0.3158685564994812)]

```


### Collecting Data from Github


First, it is neccessary (or at least highly recommended) to get a github API access token. Create it here: https://github.com/settings/tokens
Save the token in a file called 'access' in the same folder as the python scripts.

To download a lot of commits, the following script is used:

```
python3 scraping.py
```

By modifying it, the keywords that are used to fetch the commits can be altered. The results are saved in 'all_commits.json'.

