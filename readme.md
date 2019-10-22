# Vulnerability Detection with Github and Long Short Term Memory Networks

This code is part of a project and master thesis with the goal to scrape a lot of security related commits from github, process them and train a deep neural network on classifying code into vulnerable and not vulnerable.




## Training the Word2Vec model

The word2vec model is trained on a large set of python code which is simply concatenated. 

### Downloading python code

First, the code has to be downloaded.

```
python3 10python-for-training.py
```

The results are saved in the file pythontraining.txt.