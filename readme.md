# VUDENC - Vulnerability Detection with Deep Learning on a Natural Codebase

This is VUDENC, a project and master thesis for learning security vulnerability features from a large natural code basis using deep learning. The goal is to scrape a lot of security related commits of Python code from Github, process them and train a deep neural network on classifying code tokens and their context into 'vulnerable' and 'not vulnerable'. Word2Vec is used as embedding, and Long Short Term Memory networks for feature extraction.

## Background


![Architecture of the model](https://github.com/LauraWartschinski/VulnerabilityDetection/blob/master/Architecture.png)


For an exhaustive description of the theoretical background of this work, refer to the thesis itself, available as a pdf and tex file in the Master Thesis folder. A brief summary:
Vulnerability detection is crucial in preventing dangerous software exploits. There are several approaches including static and dynamic analysis, but recently, machine learning has been applied in various ways to create better models and tools. Because many tools rely on human experts to define features that make up vulnerabilities, they are subjective and require a lot of time-consuming manual work. Therefore, it is desireable to automatically learn vulnerability features with machine learning algorithms that can later recognize those typical patterns of vulnerable code and warn the user.

There are many possible ways of representing source code and embedding it in a suitable format, in varying granularity (from the file level down to the code itself). This approach works directly on the code itself and attempts classification on the level of individual code tokens, so it can highlight where exactly a vulnerability might be located in the code.

The data for this work is mined from Github. If a code snippet was changed in a commit that has a message like "fix sql injection issue", it is assumed that the part of the code that was changed was vulnerable before, and everything else is not vulnerable or at least of unclear status. The labels are thus generated purely from the commit context. The code tokens (in text form, such as "if" or "+" or "return" or "x") are embedded in a numerical vector format using a word2vec model that was trained on a large Python corpus before. 

To learn the features, an LSTM (long short term memory) network is used. LSTMs are similar to standard RNNs - they have a internal state, a 'memory', that allows them to model sequential data and take the context of the current input into account - but they are better suited for long term dependencies as they don't suffer from the problem of vanishing and exploding gradients. A single code token can not be vulnerable or safe (what about "if"? what about "return"?), but it's effect only becomes apparent when put into context with the tokens that came before it. This is why an LSTM that uses its memory to model the data is useful to learn the correct features.


![Focus area and context](https://github.com/LauraWartschinski/VulnerabilityDetection/blob/master/FocusBlocks.png)

In a given source file, small focus areas (blue) of length n are classified by taking the source code around them (their context of length m) and using this moving window of attention to create samples. Each sample is labeled depending on whether it contains code that is vulnerable (i.e. that was changed in a security-related commit).In the image, A and D are contexts that are not labeled vulnerable, while B and C are labeled as vulnerable because they (partly) contain vulnerable code, depicted in red. The tokens making up that sample are embedded using word2vec and the LSTM is trained on those samples. 


In the same way, a new piece of sourcecode can be analyzed, taking the context of each token to classify it as vulnerable or not.

## Code


### Training the Word2Vec model

The word2vec model is trained on a large set of python code which is simply concatenated. 


First, the code has to be downloaded. The Repository Mining from pydriller is used to accomplish this task.

```
python3 w2v_pythoncorpus.py
```

The results are saved in the file pythontraining.txt.

Since there are syntax and indentation errors in those files, the following script fixes those:

```
python3 w2v_cleancorpus.py
```

The results are saved in pythontraining_edit.txt.

Then, the python tokenizer is applied to retrieve the python source code tokens.
The mode can be set in the file to be either "withString" or "withoutString". Without string would indicate that all strings are replaced by a generic string token, while the other option (with string) leaves them as they are.

```
python3 w2v_tokenize.py
```

The results of that step are saved as a bunch of files of the form 'pythontraining_withString_39.py' etc. This is because to save a lot of large files often is relatively slow. The outputs are merged into a single file with:


```
python3 w2v_mergecorpus.py
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
python3 getData.py sql
```

This python script takes one argument which specifies which subset of data should be used to prepare the dataset (in the example, everything relevant to sql injections.) 

This script does a lot of the main work. It reads the file 'PyCommitsWithDiffs.json', checks a lot of contraints and downloads the full source code of the changed files. It also identifies changed parts and comments and collects all relevant information in a file. The result is saved in the file 'data/plain_sql', 'data/plain_brute_force' etc.


### Training the LSTM

Next, the data has to be split at random in three segments: training, validating and final testing.

```
python3 makemodel.py sql
```

This script takes one argument, the vulnerability / data subset it should work on which was created in the previous step. The data is shuffled randomly and then split in parts of 70%, 15% and 15% (training, validation and final test set), and the tokens are encoded using the oaded word2vec model. The results are then ready for feeding into the LSTM network, and saved as six files (samples X and labels Y for each of the three sets).  

```
python3 52ExperimentAll.py sql
```

The LSTM script takes the same arguments as the one before: vulnerability subset. It contains a lot of parameters for the LSTM model and trains the model according to those before displaying statistics and optionally saving the model.
