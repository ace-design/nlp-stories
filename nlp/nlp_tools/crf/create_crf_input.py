#This script will create the input files for crf

#Output labels: "PER": Persona, "P-ACT": primary action, "S-ACT": secondary action, "P-ENT": primary entity, "S-ENT": secondary entity, "O": no labels

import argparse
import json
import random
import stanza
import sys
sys.path.append("setup_data")
import jsonl_to_human_readable


def main():
    load_path, intersecting_path, save_name, previous_testing_path, amount = command()
    stories, annotated_stories = extract_stories(load_path)
    intersecting_stories = extract_intersecting_stories(intersecting_path)
    previous_testing_set = extract_previous_testing_set(previous_testing_path)


    stanza.download('en') 
    stanza_nlp = stanza.Pipeline('en')

    training_stories, training_annotated, testing_stories, testing_annotated = randomize_stories(stories, annotated_stories, intersecting_stories, previous_testing_set, amount)
    ensure_no_intersection(training_stories, testing_stories)

    final_results_training = []
    final_results_testing = []

    for i in range(len(training_stories)):
        training_stories_info = pos_tags(training_stories[i], training_annotated[i], stanza_nlp)
        story_format_training = format_output(training_stories[i], training_stories_info)
        final_results_training.append(story_format_training)

    for i in range(len(testing_stories)):
        testing_stories_info = pos_tags(testing_stories[i], testing_annotated[i], stanza_nlp)
        story_format_testing = format_output(testing_stories[i], testing_stories_info)
        final_results_testing.append(story_format_testing)

    save_results(final_results_training, final_results_testing, save_name)

def command():
    '''
    takes in the info from the commandline

    Returns:
    args.load_baseline_path (str): Path to the dataset file to be loaded
    args_intersecting_path (str): path of intersecting file
    args.save_name (str): name to the saving file
    args.append_testing_set (str): testing set to append to
    amount (float): percent in decimal (/100) of amount of stories in testing set

    Raises:
        FileNotFoundError: raises excpetion
        wrong file type: raises exception
    '''
    parser = argparse.ArgumentParser(description = "This program will create the input files for crf")
    parser.add_argument("load_baseline_path", type = str, help = "path of baseline file from doccano (jsonl)")
    parser.add_argument("load_intersecting_path", type = str, help = "path of intersecting file")
    parser.add_argument("save_name", type = str, help = "name of the file save the results")
    parser.add_argument("--append_testing_set", nargs="?", type = str, help = "testing set to append to")
    parser.add_argument("--amount", nargs="?", type = float, help = "percent in decimal (/100) of amount of stories to be in the testing set")

    
    args = parser.parse_args()

    if not(args.load_baseline_path.endswith(".jsonl")):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect input file type. Input file type is .jsonl")

    if not(args.load_intersecting_path.endswith(".txt")):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect input file type. Input file type is .txt")

    if args.amount != None and args.amount >= 1.0:
        sys.tracebacklimit = 0
        raise Exception ("Amount can only be less than 1.0. Amount is the percent in decimal (/100) of amount of stories to be in the testing set")

    try:
        load_file = open(args.load_baseline_path)
        load_file.close()
        load_file = open (args.load_intersecting_path)
        load_file.close()
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        if args.amount == None:
            amount = 0.2
        else:
            amount = args.amount

        return args.load_baseline_path, args.load_intersecting_path, args.save_name, args.append_testing_set, amount

def extract_stories(path):
    '''
    extract the stories and annotations from the input file

    Parameters:
    path (str): path to the file that contains the stories

    Returns
    text (list): all the stories in the dataset
    annotated_stories (list): annotated story that indicates the label type of each character in each story
    '''

    text, entities, relations = jsonl_to_human_readable.extract(path)

    annotated_stories = []

    for i in range(len(text)):
        annotated_story, label_id_list, offset_list = identify_labels_crf(text[i], entities[i])
        annotated_story, primary_action_id_list = identify_primary_action(annotated_story, label_id_list, offset_list, relations[i])
        annotated_story = identify_primary_entity(annotated_story, primary_action_id_list, label_id_list, offset_list, relations[i])
        annotated_stories.append(annotated_story)

    return text, annotated_stories
       
def extract_intersecting_stories(path):
    '''
    extract the data from intersecting stories 

    Parameters
    path (str): path to the intersecting stories file

    Returns
    intersecting_stories (list): all the stories in the intersecting set
    '''

    with open(path, encoding = "utf8") as file:
        data = file.readlines()

    intersecting_stories = []

    for story in data:
        intersecting_stories.append(story.strip(" \n\t"))

    return intersecting_stories

def extract_previous_testing_set(path):
    '''
    extract info from previous testing set if given

    Parameters:
    path (str): path to testing set if exists
    
    '''
    previous_testing_set = []

    if path != None:
        file = open(path, encoding= "utf-8")
        data = json.load(file)
        
        for story in data:
            previous_testing_set.append(story["Text"].strip(" \t"))

    return previous_testing_set

def randomize_stories(stories, annotated_stories, intersecting_stories, previous_testing_set, amount):
    '''
    randomize the stories to have 20% of set for testing and 80% of set for training

    Parameters:
    stories (list): contains the text of every story in the dataset
    annotated_stories (list): contains the annotated information corresponding to the stories list
    intersecting_stories (list): all the stories in the intersecting set of the dataset
    previous_testing_set (list): text that must be in the testing set 

    Returns:
    training_stories (list): stories for the training set
    training_annotated (list): contains the annotated information corresponding to the training_stories list
    testing_stories (list): stories for the testing set
    testing_annotated (list): contains the annotated infromation correspongind the the testing_stories list  
    '''

    training_stories = stories
    training_annotated = annotated_stories
    testing_stories = []
    testing_annotated = []

    if len(intersecting_stories) < (len(training_stories) * amount):
        max_random = len(intersecting_stories)
    else:
        max_random = len(training_stories) * amount

    num_test = round(max_random)

    for i in range(num_test):
        length = len(training_stories)

        while True:
            index = random.randint(0, length -1)

            story = training_stories[index].strip(" \t")
            
            if (story in intersecting_stories) and (story in previous_testing_set or previous_testing_set == []):
            
                testing_stories.append(training_stories[index])
                testing_annotated.append(training_annotated[index])
                training_stories.pop(index)
                training_annotated.pop(index)

                if story in previous_testing_set:
                    previous_testing_set.remove(story)

                break

    return training_stories, training_annotated, testing_stories, testing_annotated

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

def identify_labels_crf(text, entities):
    '''
    Identify and sort labels within story

    Paramaters:
        text (str): story text
        entities (list): entities and their locations within the story

    Returns:
        annotate_story (list): list of characters from story that has a letter that indicates what annotation they are, "" = no annotation, "P" = persona, "a" = action, "e" = entity
        label_id_list (list): elements Id
        offset_list (list): offset position in stories correspoinding to the elements ID list
    '''
    annotate_story = []

    for i in range(len(text)):
        annotate_story.append("")

    label_id_list = []
    offset_list = []

    for label in entities:
        label_id = label["id"]
        label_type = label["label"]
        start_offset = label["start_offset"]
        end_offset = label["end_offset"]

        label_id_list.append(label_id)
        offset_list.append([start_offset, end_offset])
    

        if label_type == "Persona":
            annotate_story[start_offset : end_offset] = ["P"] * (end_offset - start_offset)
        elif label_type == "Entity":
            annotate_story[start_offset : end_offset] = ["e"] * (end_offset - start_offset)
        elif label_type == "Action":
            annotate_story[start_offset : end_offset] = ["a"] * (end_offset - start_offset)
        else:
            pass

    return annotate_story, label_id_list, offset_list

def identify_primary_action(annotated_story, label_id_list, offset_list, relations):
    '''
    identifies the primary action in the story
    
    Parameters:
    story (list): list of characters from story that has a letter that indicates what annotation they are, "" = no annotation, "P" = persona, "a" = action, "e" = entity
    label_id_list (list): elements Id
    offset_list (list): offset position in stories correspoinding to the elements ID list
    relations (list): the relations of annotations within the story

    Returns:
    annotated_story (list): list of characters from story that has a letter that indicates what annotation they are, "" = no annotation, "P" = persona, "A" = primary action, "e" = entity, "a" = secondary action
    primary_action_id_list (list): contains the ids of the primary actions
    '''

    primary_action_id_list = []

    for relation in relations:
        relation_type = relation["type"]

        if relation_type == "triggers":
            end_id = relation["to_id"]
            trigger_index = label_id_list.index(end_id)
            start_offset, end_offset = offset_list[trigger_index]

            annotated_story[start_offset : end_offset] = ["A"] * (end_offset - start_offset)

            primary_action_id_list.append(end_id)


    return annotated_story, primary_action_id_list

def identify_primary_entity(annotated_story, primary_action_id_list, label_id_list, offset_list, relations):
    '''
    identify the primary entity in the story
    
    Parameters:
    annotated_story (list): list of characters from story that has a letter that indicates what annotation they are, "" = no annotation, "P" = persona, "A" = primary action, "e" = entity, "a" = secondary action
    primary_action_id_list (list): contains the ids of the primary actions
    label_id_list (list): elements Id
    offset_list (list): offset position in stories correspoinding to the elements ID list
    relations (list): the relations of annotations within the story

    Returns:
    annotated_story (list): list of characters from story that has a letter that indicates what annotation they are, "" = no annotation, "P" = persona, "A" = primary action, "E" = primary entity, "e" = secondary entity, "a" = secondary action    
    '''

    for relation in relations:
        relation_type = relation["type"]
        start_id = relation["from_id"]

        if relation_type == "targets" and start_id in primary_action_id_list:
            end_id = relation["to_id"]
            trigger_index = label_id_list.index(end_id)
            start_offset, end_offset = offset_list[trigger_index]

            annotated_story[start_offset : end_offset] = ["E"] * (end_offset - start_offset)


    return annotated_story

def pos_tags(story, annotated_story, stanza_nlp):
    '''
    get the pos tags and the cooresponding label type of each token determined by stanza tool

    Parameters:
    story (str): story text
    annotated_story (list): contains the label type of each character in the story "" = no annotation, "P" = persona, "A" = primary action, "E" = primary entity, "e" = secondary entity, "a" = secondary action  
    stanza_nlp (obj): the nlp that will get the pos of each word

    Returns:
    story_info (list): contains tuples of each word in the sentence in the format of (word, pos tag, label type)
    '''
    pos = []
    stanza_text = []
    story_info = []

    evaluated_story = stanza_nlp(story)
    for sent in evaluated_story.sentences:
        for word in sent.words:
            pos.append(word.upos)
            stanza_text.append(word.text)


    # "O" = no annotation, "P" = persona, "A" = primary action, "E" = primary entity, "e" = secondary entity, "a" = secondary action  

    story_counter = 0

    for i in range(len(stanza_text)):
        word_length = len(stanza_text[i])

        start = story_counter
        end = story_counter + word_length

        #check the label type correspoding to the annotated story
        if annotated_story[start : end] ==  ["P"] * word_length:
            word_info = (stanza_text[i], pos[i], "PER")
        elif annotated_story[start : end] ==  ["A"] * word_length:
            word_info = (stanza_text[i], pos[i], "P-ACT")
        elif annotated_story[start : end] ==  ["E"] * word_length:
            word_info = (stanza_text[i], pos[i], "P-ENT")
        elif annotated_story[start : end] ==  ["a"] * word_length:
            word_info = (stanza_text[i], pos[i], "S-ACT")
        elif annotated_story[start : end] ==  ["e"] * word_length:
            word_info = (stanza_text[i], pos[i], "S-ENT")
        else:
            word_info = (stanza_text[i], pos[i], "O")

        story_counter = end

        #ignore whitespaces so that we are not behind in the annotated story list
        while story_counter < len(annotated_story) and story[story_counter] == " " :
            story_counter += 1

        story_info.append(word_info)

    if story_counter != len(story):
        sys.tracebacklimit = 0
        raise Exception ("matching annotated data with stanza data failed.")

    return story_info

def format_output(story_text, story_info):
    '''
    will format the results for json file

    Parameters:
    story_text (str): the story text 
    story_info (list): contains tuples of each word in the sentence in the format of (word, pos tag, immportant)
    
    Returns:
    story_format (dict): output format for the story results
    '''

    story_format = {"Text": story_text, "Word Data": story_info}

    return story_format

def save_results(final_results_training, final_results_testing, save_name):
    '''
    save the results to a json file

    Parameters:
    final_results_training (list): final results for training story set to output to the json file
    final_results_testing (list): final results for evaluating story set to output to the json file
    save_name (str): name of the file to save
    '''

    training_saving_path = "inputs\\individual_backlog\\crf_input\\training_input\\" + save_name + ".json"
    testing_saving_path = "inputs\\individual_backlog\\crf_input\\testing_input\\" + save_name + ".json"

    with open(training_saving_path,"w", encoding="utf-8") as file:
        json.dump(final_results_training, file, indent = 4)

    with open(testing_saving_path,"w", encoding="utf-8") as file:
        json.dump(final_results_testing, file,  indent = 4)

    print("Files are saved")


if __name__ == "__main__":
    main()