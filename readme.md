# VUDENC - Vulnerability Detection with Deep Learning on a Natural Codebase

This code is part of a project and master thesis with the goal to scrape a lot of security related commits from Github, process them and train a deep neural network on classifying code into vulnerable and not vulnerable. Word2Vec is used as embedding, and Long Short Term Memory networks for feature extraction.




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
python3 55w2vParams.py
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


First, it is neccessary (or at least highly recommended) to get a github API access token. Create it here: https://github.com/settings/tokens. Save the token in a file called 'access' in the same folder as the python scripts.

To download a lot of commits, the following script is used:

```
python3 1scraping.py
```

By modifying it, the keywords that are used to fetch the commits can be altered. The results are saved in 'all_commits.json'.

### Preparing the data

Next, the commits are checked to see if they contain python code, and to download the diff files. This is done with:

```
python3 4DownloadEverythingClean.py
```

While this is done, the file 'DataFilter.json' is created to store information about which repositories and commits are useful and which aren't. The resulting data is stored in the file PyCommitsWithDiffs.json.

```
python3 50GetData.py sql
```

This python script takes one argument which specifies which subset of data should be used to prepare the dataset (in the example, everything relevant to sql injections.) 

This script does a lot of the main work. It reads the file 'PyCommitsWithDiffs.json', checks a lot of contraints and downloads the full source code of the changed files. It also identifies changed parts and comments and collects all relevant information in a file. The result is saved in the file 'data/plain_sql', 'data/plain_brute_force' etc.


### Training the LSTM

Next, the data has to be split at random in three segments: training, validating and final testing.

```
python3 51MakeBlocks.py sql
```

This script takes one argument, the vulnerability / data subset it should work on which was created in the previous step. The data is shuffled randomly and then split in parts of 70%, 15% and 15% (training, validation and final test set), and the tokens are encoded using the oaded word2vec model. The results are then ready for feeding into the LSTM network, and saved as six files (samples X and labels Y for each of the three sets).  

```
python3 52ExperimentAll.py sql
```

The LSTM script takes the same arguments as the one before: vulnerability subset. It contains a lot of parameters for the LSTM model and trains the model according to those before displaying statistics and optionally saving the model.
