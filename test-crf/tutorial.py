## Source: https://sklearn-crfsuite.readthedocs.io/en/latest/tutorial.html (initial)
from cmath import pi
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from itertools import chain

import nltk
import sklearn
import scipy.stats
from sklearn.metrics import make_scorer, classification_report

# Edit from tutorial (package renaming, doc is out of sync)
#  - from sklearn.cross_validation import cross_val_score
#  - from sklearn.grid_search import RandomizedSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RandomizedSearchCV

import sklearn_crfsuite
from sklearn_crfsuite import scorers

# Edit from tutorial : 
from sklearn_crfsuite import metrics

import pickle
import bz2
import os
import time


####
# Importing the corpus
####

# Description of ther corpus: 
#   - CONLL 2002 Named Entity Recognition Corpus
#   - file contents:  https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/conll2002.zip

# To import the corpus with nltk automatically: (first time only)
nltk.download('conll2002')

# Files contained in the conll2002 corpus
# - contains train, testA and testB data for spanish (esp) and dutch (ned) 
print(nltk.corpus.conll2002.fileids())

####
# Manipulating the corpus
####

# A sentence is defined as a sequence of words
s = nltk.corpus.conll2002.iob_sents('esp.train')[2]

# Each word is a tuple (TOKEN, POS, LABEL), where:
#   - TOKEN is the word, 
#   - POS is the part-of-speech (grammatical role), 
#   - and LAB the classified label
print(s)

def sent2token(sentence): # the token available in the text
    return [tok for tok, _, _ in sentence]

def sent2pos(sentence): # Part-of-speech (grammatical) tags
    return [pos for _, pos, _ in sentence]

def sent2labels(sentence): # Label is what we are looking for
    return [label for _, _, label in sentence]

print("tokens:  " + str(sent2token(s)))
print("postags: " + str(sent2pos(s)))
print("labels:  " + str(sent2labels(s)))

####
# Transforming sentences into features (a feature is a vector representing the sentence in the NLP space)
####

def word2features(sent, i):
    """ transform the i-st word in a sentence into a usable feature vector (here a dict)"""
    word = sent[i][0]
    postag = sent[i][1]

    features = { # Features for each and every word in the dataset
        'bias': 1.0,
        'word.lower()':   word.lower(),   # lower case word to harmonize -> str
        'word[-3:]':      word[-3:],      # last 3 letters -> str
        'word[-2:]':      word[-2:],      # last 2 letters -> str
        'word.isupper()': word.isupper(), # all letter upopercase -> bool
        'word.istitle()': word.istitle(), # first letter uppercase -> bool
        'word.isdigit()': word.isdigit(), # is a digit? -> bool
        'postag':         postag,         # Part-of-speech tag
        'postag[:2]':     postag[:2],     # first 2 letters of the POS tag
    }
    ## Update for words that are not the first one
    if i > 0: 
        word1 = sent[i-1][0]      # previous word
        postag1 = sent[i-1][1]    # previous POS tag
        features.update({
            '-1:word.lower()':   word1.lower(),    # Previous word spelled uniformously
            '-1:word.istitle()': word1.istitle(),  # is it a title?
            '-1:word.isupper()': word1.isupper(),  # is it upper case?
            '-1:postag':         postag1,          # POS tag for the previous word
            '-1:postag[:2]':     postag1[:2],      # first 2 letters of the previous POS tag
        })
    else:
        features['BOS'] = True # If the first one, Beginning Of Sentence is True

    # Update for words that are not the last ones
    if i < len(sent)-1:
        word1 = sent[i+1][0]   # Next word
        postag1 = sent[i+1][1] # next POS tag
        features.update({
            '+1:word.lower()':   word1.lower(),   # next word spelled uniformously
            '+1:word.istitle()': word1.istitle(), # is it a title?
            '+1:word.isupper()': word1.isupper(), # is it uppercase?
            '+1:postag':         postag1,         # next POS tag
            '+1:postag[:2]':     postag1[:2],     # first 2 letters of the POS tag
        })
    else:
        features['EOS'] = True # If the last one, then End Of Sentence is True.

    return features # return the feature vector for this very sentence


def sent2features(sent):
    """Transform a sentences into features"""
    return [word2features(sent, i) for i in range(len(sent))]

print(sent2features(s)[0])

#####
# Extracting the feature from the datasets
####

train_sents = list(nltk.corpus.conll2002.iob_sents('esp.train')) # training sentences
test_sents = list(nltk.corpus.conll2002.iob_sents('esp.testb'))  # test sentences

X_train = [sent2features(s) for s in train_sents] # Features fort he training set
y_train = [sent2labels(s) for s in train_sents]   # expected labels

X_test = [sent2features(s) for s in test_sents]   # Features for the test set
y_test = [sent2labels(s) for s in test_sents]     # expected labels


####
# Training
####

def train_model(model, x_features, y_labels, file):
    """Train model so that X fits Y, used file to store the model and avoid unnecessary training"""
    start = time.time()
    if os.path.exists(file):
        print("Loading from memory")
        with bz2.BZ2File(file, 'r') as infile:
            model = pickle.load(infile)
    else:
        print("Training")
        # training the model to fit the X space (features) with the Y one (labels)
        model.fit(x_features, y_labels)
        with bz2.BZ2File(file, 'w') as outfile:
            pickle.dump(model, outfile)

    end = time.time()
    print('Execution time:', end-start, 'seconds')
    return model


# Configuring the CRF model (kinda default)
config = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)
crf = train_model(config, X_train, y_train, "crf_model.pkl")

####
# Evaluation
####

# We do not care of the 'O' labels => we're going to remove them form the evaluation
available_labels = list(crf.classes_)
available_labels.remove('O')

print("Relevant labels: " + str(available_labels))

# We now ask the trained model to predict the labels based on out test feature set
y_pred = crf.predict(X_test)

# And we ask sklearn to compute the weighted f1-score
f1 = metrics.flat_f1_score(y_test, y_pred, average='weighted', labels=available_labels)
print("Weighted f-measure:" + str(f1))

sorted_labels = sorted(
    available_labels,
    key=lambda name: (name[1:], name[0])
)

# flat_classification_metrics in crfsuite is broken, PR made 26 days ago, wating for merge. In the meanwhile:
def classification_report(y_true, y_pred, labels=None, **kwargs):
    from sklearn import metrics
    from sklearn_crfsuite.utils import flatten
    return metrics.classification_report(flatten(y_true), flatten(y_pred), labels=labels, **kwargs)

report = classification_report(y_test, y_pred, labels=sorted_labels)
print(report)

 ####
 # Hyperparameter Optimization
 ####

crf_hp = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    max_iterations=100,
    all_possible_transitions=True,
    keep_tempfiles=False,
    model_filename="tmp_crf_model_hp.pkl"
)

params_space = { # Isntead of fixing c1 and c2 to 0.1, we let the system explore the space to find the "best" value
    'c1': scipy.stats.expon(scale=0.5),
    'c2': scipy.stats.expon(scale=0.05),
}

# use the weighted F1-score for evaluation, to identify which are the "best" parameters
f1_scorer = make_scorer(metrics.flat_f1_score,
                        average='weighted', labels=available_labels)

# search
config_rs = RandomizedSearchCV(crf_hp, params_space,
                               cv=3, verbose=1, n_jobs=-1, n_iter=50,
                               scoring=f1_scorer)

train_model(config_rs, X_train, y_train, 'crf_model_hp.pkl')


