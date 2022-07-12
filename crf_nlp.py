#nlp tool that will train and test the set given

from ace_sklearn_crfsuite import CRF, metrics
import argparse
import bz2
import json
import os
import pickle
import time
from sklearn.metrics import make_scorer, classification_report
import sys

def main():
    train_path, test_path, save_name = command()
    training_set = extract_info(train_path)
    testing_set = extract_info(test_path)

    X_train = [sent2features(s) for s in training_set] # Features for the training set
    y_train = [sent2labels(s) for s in training_set]   # expected labels

    X_test = [sent2features(s) for s in testing_set]   # Features for the test set
    y_test = [sent2labels(s) for s in testing_set]     # expected labels

    config = CRF( algorithm = 'lbfgs', c1 = 0.1, c2 = 0.1, max_iterations = 100, all_possible_transitions = True)
    crf = train_model(config, X_train, y_train, save_name + "_crf_model.pkl")

    y_pred = crf.predict(X_test)

    available_labels = list(crf.classes_)
    available_labels.remove('O')

    print("Relevant labels: " + str(available_labels))

    f1 = metrics.flat_f1_score(y_test, y_pred, average='weighted', labels=available_labels)
    print("Weighted f-measure:" + str(f1))

    sorted_labels = sorted(available_labels, key = lambda name: (name[1:], name[0]))

    report = metrics.flat_classification_report(y_test, y_pred, labels = sorted_labels, digits = 3)
    print(report)

def command():
    '''
    gets info from the commandline input

    Returns:
    args.load_crf_input_path (str): Path to the dataset file to be loaded
    args.save_name (str): name to the saving file

    Raises:
        FileNotFoundError: raises excpetion
        wrong file type: raises exception
    '''
    parser = argparse.ArgumentParser(description = "This program will create the input files for crf")
    parser.add_argument("load_training_path", type = str, help = "path of crf file with the training set input")
    parser.add_argument("load_testing_path", type = str, help = "path of crf file with the testing set input")
    parser.add_argument("save_name", type = str, help = "name of the file save the results")
    
    args = parser.parse_args()

    if not(args.load_training_path.endswith(".json")) and not(args.load_testing_path.endswith(".json")):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect input file type. input file type is .jsonl")

    try:
        load_file = open(args.load_training_path)
        load_file.close()
        load_file = open(args.load_testing_path)
        load_file.close()
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        return args.load_training_path, args.load_testing_path, args.save_name

def extract_info(path):
    '''
    extracts info from the path into tuples

    Parameters:
    path (str): path of the input file

    Returns:
    word_data (list): contains tuples of each word in each story in format of (word, POS, label)
    '''
    word_data = []

    file = open(path, encoding= "utf-8")
    data = json.load(file)

    for story in data:
        word_data.append([tuple(element) for element in story["Word Data"]])

    return word_data

def sent2tokens(sentence): 
    return [tok for tok, _, _ in sentence]

def sent2pos(sentence): 
    return [pos for _, pos, _ in sentence]

def sent2labels(sentence): 
    return [label for _, _, label in sentence]

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

def train_model(model, x_features, y_labels, file):
    """Train model so that X fits Y, used file to store the model and avoid unnecessary training"""
    start = time.time()
    if os.path.exists(file):
        print("Loading from memory")
        with bz2.BZ2File(file, 'r') as infile:
            model = pickle.load(infile)
    else:
        print("Starting training")
        # training the model to fit the X space (features) with the Y one (labels)
        model.fit(x_features, y_labels)  ## <<== this is the training call
        print("training completed")
        with bz2.BZ2File(file, 'w') as outfile:
            print("dumping model into memory")
            pickle.dump(model, outfile)

    end = time.time()
    print('Execution time:', end-start, 'seconds')
    return model


if __name__ == "__main__":
    main()