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
    training_set, testing_stories = extract_info(train_path)
    testing_set, training_stories = extract_info(test_path)

    ensure_no_intersection(training_stories, testing_stories)
    ensure_no_intersection(list(map(frozenset, training_set)), list(map(frozenset, testing_set)))

    X_train = [sent2features(s) for s in training_set] # Features for the training set
    y_train = [sent2labels(s) for s in training_set]   # expected labels

    X_test = [sent2features(s) for s in testing_set]   # Features for the test set
    y_test = [sent2labels(s) for s in testing_set]     # expected labels


    saving_path = "crf_models\\"  + save_name + "_crf_model.pkl"

    config = CRF( algorithm = 'lbfgs', c1 = 0.1, c2 = 0.1, max_iterations = 100, all_possible_transitions = True)
    crf = train_model(config, X_train, y_train, saving_path)

    y_pred = crf.predict(X_test)

    available_labels = list(crf.classes_)
    available_labels.remove('O')

    print("Relevant labels: " + str(available_labels))

    f1 = metrics.flat_f1_score(y_test, y_pred, average='weighted', labels=available_labels)
    print("Weighted f-measure:" + str(f1))

    sorted_labels = sorted(available_labels, key = lambda name: (name[1:], name[0]))

    report = metrics.flat_classification_report(y_test, y_pred, labels = sorted_labels, digits = 3)
    print(report)

    for i in range(len(y_pred)):
        match_annotations(y_pred[i], testing_set[i], training_stories[i])

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
    story_data (list): contains the text of each story in the dataset
    '''
    word_data = []
    story_data = []

    file = open(path, encoding= "utf-8")
    data = json.load(file)

    for story in data:
        word_data.append([tuple(element) for element in story["Word Data"]])
        story_data.append(story["Text"])

    return word_data, story_data

def ensure_no_intersection(training_set, testing_set):
    '''
    Ensures that stories and information in the training set is not in the testing set

    Parameters:
    training_set (list): data in the training set
    testing_set (list): data in the testing set

    Raises error if same story or information in both training and testing set. 
    '''

    same_data = set(training_set).intersection(set(testing_set))

    if len(same_data) != 0:
        print(same_data)
        raise Exception ("Same stories exist in both training and testing set")


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
        'postag':         postag,         # Part-of-speech tag
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
            "isalpha()": word1.isalpha(),
            '+1:word[-3:]':      word1[-3:],      # last 3 lett
        })
    else:
        features['EOS'] = True # If the last one, then End Of Sentence is True.


    if i > 1: 
        word1 = sent[i-2][0]      # two words before
        postag1 = sent[i-2][1]    # two POS tags before
        features.update({
            '-2:word.lower()':   word1.lower(),    # Previous word spelled uniformously
            '-2:word.istitle()': word1.istitle(),  # is it a title?
            '-2:word.isupper()': word1.isupper(),  # is it upper case?
            '-2:postag':         postag1,          # POS tag for the previous word
            '-2:word[-3:]':      word1[-3:],      # last 2 letters -> str
            
        })

    if i > 2: 
        word1 = sent[i-3][0]      # three word before
        postag1 = sent[i-3][1]    # three POS tag before
        features.update({
            '-3:word.lower()':   word1.lower(),    # Previous word spelled uniformously
            '-3:word.istitle()': word1.istitle(),  # is it a title?
            '-3:word.isupper()': word1.isupper(),  # is it upper case?
            '-3:postag':         postag1,          # POS tag for the previous word
            '-3:word[-2:]':      word1[-2:],      # last 2 letters -> str
        })

    if i > 3: 
        word1 = sent[i-4][0]      # four word before
        postag1 = sent[i-4][1]    # four POS tag before
        features.update({
            '-4:word.lower()':   word1.lower(),    # Previous word spelled uniformously
            '-4:word.istitle()': word1.istitle(),  # is it a title?
            '-4:word.isupper()': word1.isupper(),  # is it upper case?
            '-4:postag':         postag1,          # POS tag for the previous word
        })

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

def match_annotations(y_pred, testing_set, story_text):
    '''
    match the annotation to the words in the story

    Parameters:
    y_pred (list): contains the annotated informations for each token in each story of the testing set
    testing_set (list): contains the tuples of all the information of the the testing set 
    story_text (str): the story

    Returns:
    
    '''

    tokens = sent2tokens(testing_set)

    print(y_pred)
    print(tokens)
    persona = []
    primary_action = []
    secondary_action = []
    primary_entity = []
    secondary_entity = []

    i = 0
    j = 0 
    while i < len(y_pred):
        #match the tokens with the story text by identifying start and end characters
        start = story_text.find(tokens[i], j)
        end = start + len(tokens[i])

        #match labels (if the same label appears in next token, then merge the annotations as one)
        if y_pred[i] == "PER":
            end, i = check_next(y_pred, story_text, tokens, end, i, "PER")
            persona.append(story_text[start:end])

        elif y_pred[i] == "P-ACT":
            end, i = check_next(y_pred, story_text, tokens, end, i, "P-ACT")
            primary_action.append(story_text[start:end])

        elif y_pred[i] == "S-ACT":
            end, i = check_next(y_pred, story_text, tokens, end, i, "S-ACT")
            secondary_action.append(story_text[start:end])

        elif y_pred[i] == "P-ENT":
            end, i = check_next(y_pred, story_text, tokens, end, i, "P-ENT")
            primary_entity.append(story_text[start:end])

        elif y_pred[i] == "S-ENT":
            end, i = check_next(y_pred, story_text, tokens, end, i, "S-ENT")
            secondary_entity.append(story_text[start:end])

        i += 1
        j = end

    print(persona)
    print(primary_action)
    print(secondary_action)
    print(primary_entity)
    print(secondary_entity)
    print()



def check_next (y_pred, story_text, tokens, end, i, label_type): 
    '''
    checks if the next token is the same annotation type

    Parameters:
    y_pred (list): contains the annotated informations for each token in each story of the testing set
    story_text (str): the story
    tokens (list): contains the tokens of the text in the story
    end (int): position of end character of the annotation
    i (int): counter that goes through positions of y_pred and tokens
    label_type (str): the label type of the annotation ex. "PER" pr "ACT"

    Returns:
    end (int): position of end character of the annotation
    i (int): counter that goes through positions of y_pred and tokens
    '''
    #runs process if next token label is the same as the token we were just looking at 
    while y_pred [i + 1] == label_type and i < len(y_pred):
        #adjust the end character position to include this token so we can identify as one annotation
        end = story_text.find(tokens[i+1], end) + len(tokens[i+1])
        i += 1

    return end, i

if __name__ == "__main__":
    main()
