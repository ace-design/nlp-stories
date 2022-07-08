#This script will create the input files for crf

#Output labels: "PER": Persona, "P-ACT": primary action, "S-ACT": secondary action, "P-ENT": primary entity, "S-ENT": secondary entity

import argparse
import json
import jsonl_to_human_readable
import stanza
import sys


def main():
    load_path, save_name = command()
    stories, annotated_stories = extract_stories(load_path)
    
    stanza.download('en') 
    global stanza_nlp
    stanza_nlp = stanza.Pipeline('en')

    final_results_testing = []
    final_results_evaluation = []

    for i in range(len(stories)):
        testing_stories_info = pos_tags_testing(stories[i], annotated_stories[i], stanza_nlp)
        story_format_testing = format_output(stories[i], testing_stories_info)
        final_results_testing.append(story_format_testing)

    for i in range(len(stories)):
        evaluation_stories_info = pos_tags_evaluation(stories[i], stanza_nlp)
        story_format_evaluation = format_output(stories[i], evaluation_stories_info)
        final_results_evaluation.append(story_format_evaluation)

    save_results(final_results_testing, final_results_evaluation, save_name)

def command():
    '''
    takes in the info from the commandline

    Returns:
    args.load_baseline_path (str): Path to the dataset file to be loaded
    args.save_name (str): name to the saving file

    Raises:
        FileNotFoundError: raises excpetion
        wrong file type: raises exception
    '''
    parser = argparse.ArgumentParser(description = "This program will create the input files for crf")
    parser.add_argument("load_baseline_path", type = str, help = "path of baseline file from doccano (jsonl)")
    parser.add_argument("save_name", type = str, help = "name of the file save the results")
    
    args = parser.parse_args()

    if not(args.load_baseline_path.endswith(".jsonl")):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect input file type. input file type is .jsonl")

    try:
        load_file = open(args.load_baseline_path)
        load_file.close()
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        return args.load_baseline_path, args.save_name

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
        annotated_story, label_id_list, offset_list = identify_labels(text[i], entities[i])
        annotated_story, primary_action_id_list = identify_primary_action(annotated_story, label_id_list, offset_list, relations[i])
        annotated_story = identify_primary_entity(annotated_story, primary_action_id_list, label_id_list, offset_list, relations[i])
        annotated_stories.append(annotated_story)

    return text, annotated_stories
       
def identify_labels(text, entities):
    '''
    Identify and sort labels within story

    Paramaters:
        text (str): story text
        entities (list): entities and their locations within the story

    Returns:
        story (list): list of characters from story that has a letter that indicates what annotation they are, "" = no annotation, "P" = persona, "a" = action, "e" = entity
        label_id_list (list): elements Id
        offset_list (list): offset position in stories correspoinding to the elements ID list
    '''
    story = []

    for i in range(len(text)):
        story.append("")

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
            story[start_offset : end_offset] = ["P"] * (end_offset - start_offset)
        elif label_type == "Entity":
            story[start_offset : end_offset] = ["e"] * (end_offset - start_offset)
        elif label_type == "Action":
            story[start_offset : end_offset] = ["a"] * (end_offset - start_offset)
        else:
            pass

    return story, label_id_list, offset_list

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

def pos_tags_testing(story, annotated_story, stanza_nlp):
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


    # "" = no annotation, "P" = persona, "A" = primary action, "E" = primary entity, "e" = secondary entity, "a" = secondary action  

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
            word_info = (stanza_text[i], pos[i], "-")

        story_counter = end

        #ignore whitespaces so that we are not behind in the annotated story list
        while story_counter < len(annotated_story) and story[story_counter] == " " :
            story_counter += 1

        story_info.append(word_info)

    if story_counter != len(story):
        sys.tracebacklimit = 0
        raise Exception ("matching annotated data with stanza data failed.")

    return story_info

def pos_tags_evaluation(story, stanza_nlp):
    '''
    get the pos tags of each word in the story for the evaluation story set

    Parameters:
    story (str): the story that is getting the pos tags
    stanza_nlp (obj): the nlp that will get the pos tags of each word

    Returns:
    story_info (list): contains tuples of each word in the sentence in the format of (word, pos tag)
    '''

    pos = []
    text = []
    story_info = []

    evaluated_story = stanza_nlp(story)
    for sent in evaluated_story.sentences:
        for word in sent.words:
            pos.append(word.upos)
            text.append(word.text)

    for i in range(len(text)):
        word_info = (text[i], pos[i])
        story_info.append(word_info)

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

def save_results(final_results_testing, final_results_evaluation, save_name):
    '''
    save the results to a json file

    Parameters:
    final_results_testing (list): final results for testing story set to output to the json file
    final_results_evaluation (list): final results for evaluating story set to output to the json file
    save_name (str): name of the file to save
    '''

    testing_saving_path = "crf_input\\testing_input\\" + save_name + ".json"
    evaluation_saving_path = "crf_input\\evaluation_input\\" + save_name + ".json"

    with open(testing_saving_path,"w", encoding="utf-8") as file:
        json.dump(final_results_testing, file, indent = 4)

    with open(evaluation_saving_path,"w", encoding="utf-8") as file:
        json.dump(final_results_evaluation, file,  indent = 4)

    print("File is saved")


if __name__ == "__main__":
    main()