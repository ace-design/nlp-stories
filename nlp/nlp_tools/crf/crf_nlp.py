#nlp tool that will train and test the set given

from ace_sklearn_crfsuite import CRF, metrics
import argparse
import bz2
from collections import Counter
import matplotlib.pyplot as plt
import json
import numpy as np
import os
import pickle
import stanza
import time
import scipy.stats
from sklearn.metrics import make_scorer, classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
import sys

def main():
    train_path, test_path, random_optimize, grid_optimize, model_name, saving_path, data_type_folder, c1, c2, feature_type = command()

    stanza.download('en') 
    stanza_nlp = stanza.Pipeline('en')
    
    testing_set, testing_stories = extract_info(test_path)

    X_test = [sent2features(s, feature_type) for s in testing_set]   # Features for the test set
    y_test = [sent2labels(s) for s in testing_set]     # expected labels

    crf, X_train, y_train = get_model(train_path, testing_stories, testing_set, saving_path, model_name, feature_type, c1, c2)
    
    y_pred, available_labels = get_results(crf, X_test, y_test, feature_type)
    
    output = []
    for i in range(len(y_pred)):
        persona, primary_action, secondary_action, primary_entity, secondary_entity = match_annotations(y_pred[i], testing_set[i], testing_stories[i], stanza_nlp)
        formatted_data = format_results(testing_stories[i], persona, primary_action, secondary_action, primary_entity, secondary_entity)
        output.append(formatted_data)

    save_results(model_name, output, data_type_folder)
    optimize_parameters(random_optimize, grid_optimize, X_train, y_train, available_labels, model_name, train_path, testing_stories, testing_set, feature_type)
    
def command():
    '''
    gets info from the commandline input

    Returns:
    args.load_training_path (str): path of crf file with the training set input
    args.load_testing_path (str): path of crf file with the testing set input
    args.save_name (str): name to the saving file
    data_type (str): type of grouping of the data

    Raises:
        FileNotFoundError: raises excpetion
        wrong file type: raises exception
        optimize without training set given: raises exception
        model does not exist and training set not given: raises exception
    '''
    parser = argparse.ArgumentParser(description = "This program will create the input files for crf")
    parser.add_argument("load_testing_path", type = str, help = "path of json file with the testing set input")
    parser.add_argument("feature_type", type = str, choices=["word_pos_feature", "pos_feature"], help = "word_pos_feature contains features containing words and POS tags; pos_feature contains features containing POS tags")
    parser.add_argument("--load_training_path", nargs="?", type = str, help = "path of json file with the training set input")
    parser.add_argument("--c1", nargs="?", type = float, help = "c1 model parameter")
    parser.add_argument("--c2", nargs="?", type = float, help = "c2 model parameter")
    parser.add_argument('--random_optimize', default = False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--grid_optimize', default = False, action=argparse.BooleanOptionalAction)
    parser.add_argument("model_name", type = str, help = "name of the model")
    parser.add_argument("data_type", type = str, choices=["BKLG", "CAT", "GLO"], help = "evaluation by individual backlogs - BKLG, categorized backlogs - CAT, or global - GLO")
    
    args = parser.parse_args()

    if  not(args.load_testing_path.endswith(".json")):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect input file type. input file type is .jsonl")

    if args.c1 == None:
        c1 = 0.1
    else:
        c1 = args.c1

    if args.c2 == None:
        c2 = 0.1
    else:
        c2 = args.c2

    if args.data_type == "BKLG":
        data_type_folder = "individual_backlog"
    elif args.data_type == "CAT":
        data_type_folder = "categories"
    else:
        data_type_folder = "global"

    saving_path = "nlp\\nlp_tools\\crf\\crf_models\\"  + args.model_name + "_crf_model.pkl"

    if args.load_training_path == None and not(os.path.exists(saving_path)):
        sys.tracebacklimit = 0
        raise Exception ("Missing training path file")

    if args.load_training_path == None and (args.random_optimize or args.grid_optimize):
        sys.tracebacklimit = 0
        raise Exception ("Can not optimize if no training dataset is given")

    try:
        if args.load_training_path != None:
            load_file = open(args.load_training_path)
            load_file.close()
        load_file = open(args.load_testing_path)
        load_file.close()
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        return args.load_training_path, args.load_testing_path, args.random_optimize, args.grid_optimize, args.model_name, saving_path, data_type_folder, c1, c2, args.feature_type

def get_model(train_path, testing_stories, testing_set, saving_path, save_name, feature_type, c1, c2):
    '''trains a model if it doesn't exist, if it exist, it will extract model from the file'''
    if  not(os.path.exists(saving_path)):
        training_set, training_stories = extract_info(train_path)

        ensure_no_intersection(training_stories, testing_stories)
        ensure_no_intersection(list(map(frozenset, training_set)), list(map(frozenset, testing_set)))

        X_train = [sent2features(s, feature_type) for s in training_set] # Features for the training set
        y_train = [sent2labels(s) for s in training_set]   # expected labels

        config = CRF(algorithm = 'lbfgs', c1 = c1, c2 = c2, max_iterations = 100, all_possible_transitions = True)

        crf = train_model(config, X_train, y_train, saving_path)


        common_transition = print_transitions(Counter(crf.transition_features_).most_common(10))
        least_common_transition = print_transitions(Counter(crf.transition_features_).most_common()[-10:])
        common_features = print_state_features(Counter(crf.state_features_).most_common(10))
        least_common_features = print_state_features(Counter(crf.state_features_).most_common()[-10:])

        path = "nlp\\nlp_tools\\crf\\crf_learned_info\\" + save_name + "_learned_info.txt"

        with open(path, "a", encoding = "utf-8") as file:
            file.write("Top likely transitions:\n")
            file.writelines("\n".join(common_transition))
            file.write("\n\nTop unlikely transitions:\n")
            file.writelines("\n".join(least_common_transition))
            file.write("\n\nTop feature factors:\n")
            file.writelines("\n".join(common_features))
            file.write("\n\nLeast feature factors:\n")
            file.writelines("\n".join(least_common_features))
        
        print("Learned information by the model has bee saved in: " + path)

    else:
        print("\nLoading from memory")
        with bz2.BZ2File(saving_path, 'r') as infile:
            crf = pickle.load(infile)

        X_train = None
        y_train = None

    return crf, X_train, y_train

def print_transitions(trans_features):
    '''gets the transitions learned by the model'''
    transition = []
    for (label_from, label_to), weight in trans_features:
        transition.append("%-6s -> %-7s %0.6f" % (label_from, label_to, weight))

    return transition

def print_state_features(state_features):
    '''gets the prominent features learned by the model'''
    features = []
    for (attr, label), weight in state_features:
        features.append("%0.6f %-8s %s" % (weight, label, attr))

    return features

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

def word2features_word_pos(sent, i):
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

    ## Update for words that are not the current word we are looking at

    if i > 0: 
        word1 = sent[i-1][0]      # previous word
        postag1 = sent[i-1][1]    # previous POS tag
        features.update({
            '-1:word.lower()':   word1.lower(),    # Previous word spelled uniformously
            '-1:word.istitle()': word1.istitle(),  # first letter uppercase -> bool
            '-1:word.isupper()': word1.isupper(),  # all letter upopercase -> bool
            '-1:postag':         postag1,          # POS tag           
        })
    else:
        features['BOS'] = True # If the first one, Beginning Of Sentence is True

    if i > 1: 
        word1 = sent[i-2][0]      # two words before
        postag1 = sent[i-2][1]    # two POS tags before
        features.update({
            '-2:word.lower()':   word1.lower(),    # word spelled uniformously
            '-2:word.istitle()': word1.istitle(),  # first letter uppercase -> bool
            '-2:word.isupper()': word1.isupper(),  # all letter upopercase -> bool
            '-2:postag':         postag1,          # POS tag 
            '-2:word[-3:]':      word1[-3:],       # last 3 letters -> str
        })

    if i > 2: 
        word1 = sent[i-3][0]      # three word before
        postag1 = sent[i-3][1]    # three POS tag before
        features.update({
            '-3:word.lower()':   word1.lower(),    # word spelled uniformously
            '-3:word.istitle()': word1.istitle(),  # first letter uppercase -> bool
            '-3:word.isupper()': word1.isupper(),  # all letter upopercase -> bool
            '-3:postag':         postag1,          # POS tag 
            '-3:word[-2:]':      word1[-2:],       # last 2 letters -> str
        })

    if i > 3: 
        word1 = sent[i-4][0]      # four word before
        postag1 = sent[i-4][1]    # four POS tag before
        features.update({
            '-4:word.lower()':   word1.lower(),    # word spelled uniformously
            '-4:word.istitle()': word1.istitle(),  # first letter uppercase -> bool
            '-4:word.isupper()': word1.isupper(),  # all letter upopercase -> bool
            '-4:postag':         postag1,          # POS tag
        })

    if i < len(sent)-1:
        word1 = sent[i+1][0]   # Next word
        postag1 = sent[i+1][1] # next POS tag
        features.update({
            '+1:word.lower()':   word1.lower(),   # next word spelled uniformously
            '+1:word.istitle()': word1.istitle(), # first letter uppercase -> bool
            '+1:word.isupper()': word1.isupper(), # all letter upopercase -> bool
            '+1:postag':         postag1,         # POS tag
            "+1:isalpha()":      word1.isalpha(), # all characters from alphabet -> bool
            '+1:word[-3:]':      word1[-3:],      # last 3 letters -> str
        })
    else:
        features['EOS'] = True # If the last one, then End Of Sentence is True.

    return features # return the feature vector for this very sentence

def word2features_pos(sent, i):
    """ transform the i-st word in a sentence into a usable feature vector (here a dict)"""
    word = sent[i][0]
    postag = sent[i][1]
    

    features = { # Features for each and every word in the dataset
        'bias': 1.0,
        'word.isupper()': word.isupper(), # all letter upopercase -> bool
        'word.istitle()': word.istitle(), # first letter uppercase -> bool
        'postag':         postag,         # Part-of-speech tag
        "len(word)":     len(word),
        "isalpha()":      word.isalpha(), # all characters from alphabet -> bool
        "position": i,
    }

    ## Update for words that are not the current word we are looking at

    if i > 0: 
        word1 = sent[i-1][0]      # previous word
        postag1 = sent[i-1][1]    # previous POS tag

        features.update({
            '-1:word.istitle()': word1.istitle(),  # first letter uppercase -> bool
            '-1:word.isupper()': word1.isupper(),  # all letter upopercase -> bool
            '-1:postag':         postag1,          # POS tag           
            "-1:isalpha()":      word1.isalpha(), # all characters from alphabet -> bool
            "-1:len(word1)":     len(word1),
        })
    else:
        features['BOS'] = True # If the first one, Beginning Of Sentence is True

    if i > 1: 
        word1 = sent[i-2][0]      # two words before
        postag1 = sent[i-2][1]    # two POS tags before
        features.update({
            '-2:word.istitle()': word1.istitle(),  # first letter uppercase -> bool
            '-2:word.isupper()': word1.isupper(),  # all letter upopercase -> bool
            '-2:postag':         postag1,          # POS tag 
            "-2:isalpha()":      word1.isalpha(), # all characters from alphabet -> bool
        })

    if i > 2: 
        word1 = sent[i-3][0]      # three word before
        postag1 = sent[i-3][1]    # three POS tag before
        features.update({
            '-3:word.istitle()': word1.istitle(),  # first letter uppercase -> bool
            '-3:word.isupper()': word1.isupper(),  # all letter upopercase -> bool
            '-3:postag':         postag1,          # POS tag 
            "-3:isalpha()":      word1.isalpha(), # all characters from alphabet -> bool
        })

    if i > 3: 
        word1 = sent[i-4][0]      # four word before
        postag1 = sent[i-4][1]    # four POS tag before
        features.update({
            '-4:word.istitle()': word1.istitle(),  # first letter uppercase -> bool
            '-4:word.isupper()': word1.isupper(),  # all letter upopercase -> bool
            '-4:postag':         postag1,          # POS tag
            "-4:isalpha()":      word1.isalpha(), # all characters from alphabet -> bool
        })


    if i < len(sent)-1:
        word1 = sent[i+1][0]   # Next word
        postag1 = sent[i+1][1] # next POS tag
        features.update({
            '+1:word.istitle()': word1.istitle(), # first letter uppercase -> bool
            '+1:word.isupper()': word1.isupper(), # all letter upopercase -> bool
            '+1:postag':         postag1,         # POS tag
            "+1:isalpha()":      word1.isalpha(), # all characters from alphabet -> bool
        })
    else:
        features['EOS'] = True # If the last one, then End Of Sentence is True.

    return features # return the feature vector for this very sentence

def sent2features(sent, feature_type):
    """Transform a sentences into features"""
    if feature_type == "word_pos_feature":
        return [word2features_word_pos(sent, i) for i in range(len(sent))]
    else:
        return [word2features_pos(sent, i) for i in range(len(sent))]

def train_model(model, x_features, y_labels, file):
    """Train model so that X fits Y, used file to store the model and avoid unnecessary training"""
    start = time.time()
    if os.path.exists(file):
        print("\nLoading from memory")
        with bz2.BZ2File(file, 'r') as infile:
            model = pickle.load(infile)
    else:
        print("\nStarting training")
        # training the model to fit the X space (features) with the Y one (labels)
        model.fit(x_features, y_labels)  ## <<== this is the training call
        print("training completed")
        with bz2.BZ2File(file, 'w') as outfile:
            print("dumping model into memory")
            pickle.dump(model, outfile)

    end = time.time()
    print('Execution time:', end-start, 'seconds')
    return model

def get_results(crf, X_test, y_test, feature_type):
    '''runs crf to get the annotations in the stories based on the model'''
    y_pred = crf.predict(X_test)

    available_labels = list(crf.classes_)
    available_labels.remove('O')

    print("Relevant labels: " + str(available_labels))

    f1 = metrics.flat_f1_score(y_test, y_pred, average='weighted', labels=available_labels)
    print("Weighted f-measure:" + str(f1))

    sorted_labels = sorted(available_labels, key = lambda name: (name[1:], name[0]))

    report = metrics.flat_classification_report(y_test, y_pred, labels = sorted_labels, digits = 3)
    print(report)

    if feature_type == "word_pos_feature":
        print("\nFeatures with words and POS tags were used")
    else:
        print("\nFeatures with POS tags were used")

    return y_pred, available_labels

def match_annotations(y_pred, testing_set, story_text, stanza_nlp):
    '''
    match the annotation to the words in the story

    Parameters:
    y_pred (list): contains the annotated informations for each token in each story of the testing set
    testing_set (list): contains the tuples of all the information of the the testing set 
    story_text (str): the story
    stanza_nlp (obj): stanza nlp tool for getting POS tags

    Returns:
    persona (list): identifies persona in the story
    primary_action (list): identifies primary action in the story
    secondary_action (list): identifies secondary action in the story
    primary_entity (list): identifies primary entity in the story
    secondary_entity (list): identifies secondary entity in the story
    '''

    tokens = sent2tokens(testing_set)

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
            end, i = check_next_action(y_pred, story_text, tokens, end, i, "P-ACT", stanza_nlp)
            primary_action.append(story_text[start:end])

        elif y_pred[i] == "S-ACT":
            end, i = check_next_action(y_pred, story_text, tokens, end, i, "S-ACT", stanza_nlp)
            secondary_action.append(story_text[start:end])

        elif y_pred[i] == "P-ENT":
            end, i = check_next(y_pred, story_text, tokens, end, i, "P-ENT")
            primary_entity.append(story_text[start:end])

        elif y_pred[i] == "S-ENT":
            end, i = check_next(y_pred, story_text, tokens, end, i, "S-ENT")
            secondary_entity.append(story_text[start:end])

        i += 1
        j = end

    return persona, primary_action, secondary_action, primary_entity, secondary_entity

def check_next (y_pred, story_text, tokens, end, i, label_type): 
    '''
    checks if the next token is the same annotation type

    Parameters:
    y_pred (list): contains the annotated informations for each token in each story of the testing set
    story_text (str): the story
    tokens (list): contains the tokens of the text in the story
    end (int): position of end character of the annotation
    i (int): counter that goes through positions of y_pred and tokens
    label_type (str): the label type of the annotation ex. "PER" or "ENT"

    Returns:
    end (int): position of end character of the annotation
    i (int): counter that goes through positions of y_pred and tokens
    '''
    #runs process if next token label is the same as the token we were just looking at 
    while i < len(y_pred) -1 and y_pred [i + 1] == label_type:
        #adjust the end character position to include this token so we can identify as one annotation
        end = story_text.find(tokens[i+1], end) + len(tokens[i+1])
        i += 1

    return end, i

def check_next_action(y_pred, story_text, tokens, end, i, label_type, stanza_nlp): 
    '''
    checks if the next token is the same annotation type for action type labels 

    Parameters:
    y_pred (list): contains the annotated informations for each token in each story of the testing set
    story_text (str): the story
    tokens (list): contains the tokens of the text in the story
    end (int): position of end character of the annotation
    i (int): counter that goes through positions of y_pred and tokens
    label_type (str): the label type of the annotation ex. "P-ACT" or "S-ACT"
    stanza_nlp (obj): stanza nlp tool for getting POS tags

    Returns:
    end (int): position of end character of the annotation
    i (int): counter that goes through positions of y_pred and tokens
    '''
    #runs process if next token label is the same as the token we were just looking at 
    while i < len(y_pred) -1 and y_pred [i + 1] == label_type:
        #if next token and current token has a POS tag as verb, then they are two seperate actions and should not be considered under the same annotation
        word1 = tokens[i+1]
        nlp_evalution1 = stanza_nlp(word1)

        word = tokens[i]
        nlp_evalution = stanza_nlp(word)

        if nlp_evalution.sentences[0].words[0].upos == "VERB" and nlp_evalution1.sentences[0].words[0].upos == "VERB":
            break
        else:
            #adjust the end character position to include this token so we can identify as one annotation
            end = story_text.find(tokens[i+1], end) + len(tokens[i+1])
            i += 1

    return end, i

def format_results(story, persona, primary_action, secondary_action, primary_entity, secondary_entity):
    '''
    format the results for json output

    Parameters:
    story (str): story text
    persona (list): identifies persona in the story
    primary_action (list): identifies primary action in the story
    secondary_action (list): identifies secondary action in the story
    primary_entity (list): identifies primary entity in the story
    secondary_entity (list): identifies secondary entity in the story
    
    Returns:
    formatted_data (dict): formatted dictionary for output into json
    '''

    trigger_list = []
    target_list = []

    for p_action in primary_action:
        for per in persona:
            trigger_list.append([per, p_action])

    for p_entity in primary_entity:
        for p_action in primary_action:
            target_list.append([p_action, p_entity])
        


    formatted_data = {  "Text": story, 
                        "Persona": persona,
                        "Action": {"Primary Action": primary_action, "Secondary Action": secondary_action}, 
                        "Entity": {"Primary Entity": primary_entity, "Secondary Entity": secondary_entity},
                        "Triggers" : trigger_list,
                        "Targets" : target_list
                    }

    return formatted_data

def save_results(save_name, output, data_type_folder):
    '''
    save the final results to a json file

    Parameters: 
    save_name (str): the name of the file to save
    output (list): contains the data to save into the file 
    data_type_folder (str): folder name to save in    
    '''   

    saving_path = "nlp\\nlp_outputs\\" + data_type_folder + "\\nlp_outputs_original\\crf\\" + save_name +".json"

    with open(saving_path,"w", encoding="utf-8") as file:
        json.dump(output, file, indent = 4)

    print("File is saved")

def optimize_parameters(random_optimize, grid_optimize, X_train, y_train, available_labels, model_name, train_path, testing_stories, testing_set, feature_type):
    '''optimize the c1 and c2 parameters'''
    training_set, training_stories = extract_info(train_path)

    ensure_no_intersection(training_stories, testing_stories)
    ensure_no_intersection(list(map(frozenset, training_set)), list(map(frozenset, testing_set)))

    X_train = [sent2features(s,feature_type) for s in training_set] # Features for the training set
    y_train = [sent2labels(s) for s in training_set]   # expected labels


    f1_scorer = make_scorer(metrics.flat_f1_score, average='weighted', labels=available_labels)

    if random_optimize:
        hp_best_param, hp_best_score = random_hyperparameter_optimization(X_train, y_train, f1_scorer, model_name)
        
        print("\n")
        print('best hp params:', hp_best_param)
        print('best hp CV score:', hp_best_score)
    
    if grid_optimize:
        grid_best_param, grid_best_score =grid_hyperparameter_optimization(X_train, y_train, f1_scorer, model_name)
        
        print("\n")
        print('best grid params:', grid_best_param)
        print('best grid CV score:', grid_best_score)

    if random_optimize and grid_optimize:
        print("\n\nRandom optimize results:")
        print('best hp params:', hp_best_param)
        print('best hp CV score:', hp_best_score)
        print("Grid optimize results:")
        print('best hp params:', grid_best_param)
        print('best hp CV score:', grid_best_score)

def random_hyperparameter_optimization(X_train, y_train, f1_scorer, model_name):
    '''hyperparameter optimization for finding c1 and c2 randomly'''

    crf_hp = CRF(algorithm='lbfgs', max_iterations=100, all_possible_transitions=True)

    # Isntead of fixing c1 and c2 to 0.1, we let the system explore the space to find the "best" value
    params_space = { 'c1': scipy.stats.expon(scale=0.5), 'c2': scipy.stats.expon(scale=0.5)}
    
    config_rs = RandomizedSearchCV(crf_hp, params_space, cv=5, verbose=100, n_jobs=-1, n_iter=50, scoring= f1_scorer, return_train_score=True, refit=False)

    crf_hp = train_model(config_rs, X_train, y_train, "nlp\\nlp_tools\\crf\\crf_models\\"+ model_name + "_crf_model_random_hp.pkl")

    plt.style.use('ggplot')
    
    plot_hp(crf_hp, 'mean_train_score') # How it behave on the training sets
    plt.savefig("nlp\\nlp_tools\\crf\\crf_graphs\\" + model_name +  "_training_random_parameter_space.png")
    plot_hp(crf_hp, 'mean_test_score') # How it behave on the validation sets
    plt.savefig("nlp\\nlp_tools\\crf\\crf_graphs\\" + model_name  +  "_testing_random_parameter_space.png")
    print("\ngraphs are saved")

    return crf_hp.best_params_, crf_hp.best_score_

def grid_hyperparameter_optimization(X_train, y_train, f1_scorer, model_name):

    crf_grid = CRF(algorithm='lbfgs',max_iterations=100,all_possible_transitions=True,)

    params_space_grid = {"c1": np.linspace(0.0, 1, 21),"c2": np.linspace(0.0, 1, 21)}

    config_grid = GridSearchCV(crf_grid, params_space_grid, cv=5, verbose=100, n_jobs=-1, scoring= f1_scorer, return_train_score=True, refit=False)

    crf_grid = train_model(config_grid, X_train, y_train, "nlp\\nlp_tools\\crf\\crf_models\\"+ model_name + "_crf_model_grid.pkl")

    plot_hp(crf_grid, 'mean_test_score')
    plt.savefig("nlp\\nlp_tools\\crf\\crf_graphs\\" + model_name + "_grid_parameter_space.png")
    print("\ngraph is saved")

    return crf_grid.best_params_, crf_grid.best_score_

def plot_hp(hp_model, color):
    _x = [s['c1'] for s in hp_model.cv_results_['params']]
    _y = [s['c2'] for s in hp_model.cv_results_['params']]
    _c = [s for s in hp_model.cv_results_[color]]

    fig = plt.figure()

    plt.scatter(_x, _y, c=_c, s=60, alpha=0.3,cmap='coolwarm')
    plt.xlabel("C1")
    plt.ylabel("C2")
    plt.title("Exploring {C1,C2} parameter space")
    cb = plt.colorbar()
    cb.ax.set_ylabel('F1-score')

if __name__ == "__main__":
    main()
