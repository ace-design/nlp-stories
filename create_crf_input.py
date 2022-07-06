#This script will create the input files for crf
from __future__ import annotations
import argparse
import json
import stanza
import sys


def main():
    load_path, save_name = command()
    stories, annotations = extract_stories(load_path)
    
    stanza.download('en') 
    global stanza_nlp
    stanza_nlp = stanza.Pipeline('en')

    final_results = []

    for i in range(len(stories)):
        story_info = pos_tags_with_importance(stories[i], annotations[i], stanza_nlp)
        story_format = format_output(story_info, stories[i])
        final_results.append(story_format)

    save_results(final_results, save_name)

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
    parser.add_argument("load_baseline_path", type = str, help = "path of baseline file")
    parser.add_argument("save_name", type = str, help = "name of the file save the results")
    
    args = parser.parse_args()

    if not(args.load_baseline_path.endswith(".json")):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect input file type. input file type is .json")

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
    stories (list): all the stories in the dataset
    '''

    text = []
    annotations = []

    file = open(path)
    data = json.load(file)

    for story in data:
        text.append(story["Text"])
        story_annotation = story["Persona"] + story["Entity"]["Primary Entity"] + story["Entity"]["Secondary Entity"] + story["Action"]["Primary Action"] +story["Action"]["Secondary Action"]

        while "" in story_annotation:
            story_annotation.remove("")


        # story_annotation.append(story["Persona"])
        # story_annotation.append(story["Entity"]["Primary Entity"])
        # story_annotation.append(story["Entity"]["Secondary Entity"])
        # story_annotation.append(story["Action"]["Primary Action"])
        # story_annotation.append(story["Action"]["Secondary Action"])

        annotations.append(story_annotation)

    return text, annotations
       
    file.close()

    baseline_data = [text, persona, primary_entity, primary_action]
    pos_data = [persona_pos, primary_entity_pos, primary_action_pos]

    return baseline_data, pos_data

def pos_tags_with_importance(story, annotations, stanza_nlp):
    '''
    get the pos tags and importance (if the word has been annotated) of each word in the story

    Parameters:
    story (str): the story that is getting the pos tags
    annotations (list): contains all the words that have been annotated from the baseline
    stanza_nlp (obj): the nlp that will get the pos tags of each word

    Returns:
    story_info (list): contains tuples of each word in the sentence in the format of (word, pos tag, immportant)
    '''

    pos = []
    text = []
    story_info = []

    evaluated_story = stanza_nlp(story)
    for sent in evaluated_story.sentences:
        for word in sent.words:
            pos.append(word.upos)
            text.append(word.text)

    print(annotations)

    for i in range(len(text)):
        if text[i] in annotations:
            word_info = (text[i], pos[i], True)
        else:
            word_info = (text[i], pos[i], False)
        story_info.append(word_info)

    return story_info

def format_output(story_info, story_text):
    '''
    will format the results for json file

    Parameters:
    story_info (list): contains tuples of each word in the sentence in the format of (word, pos tag, immportant)
    story_text (str): the story text 

    Returns:
    story_format (dict): output format for the story results
    '''

    story_format = {"Text": story_text, "Word Data": story_info}

    return story_format

def save_results(final_results, save_name):
    '''
    save the results to a json file

    Parameters:
    final_results (list): final results to output to the json file
    save_name (str): name of the file to save
    '''

    testing_saving_path = "crf_input\\testing_input\\" + save_name + ".json"
    evaluation_saving_path = "crf_input\\evaluation_input\\" + save_name + ".json"

    json.dumps(final_results)
    with open(testing_saving_path,"w", encoding="utf-8") as file:
        json.dump(final_results, file, ensure_ascii=False, indent = 4)

    print("File is saved")


if __name__ == "__main__":
    main()