#This script is the most basic nlp that will annotate the stories 
#Noun and verb list from https://drive.google.com/file/d/0B5eYVI2s0XztOVdaUnNWQWFZOEU/edit?resourcekey=0-jNd6JksVlwXjv6YnXDu-wg via http://www.ashley-bovan.co.uk/words/partsofspeech.html
import argparse
import json
import sys

def main():
    load_path, save_name, data_type_folder = command()
    stories = extract(load_path)

    persona_list = []
    action_list = []
    entity_list = []
    noun_text_file = "nlp\\nlp_tools\\simple\\word_lists\\nouns.txt"
    verb_text_file = "nlp\\nlp_tools\\simple\\word_lists\\verbs.txt"

    noun_data = retrieve_word_list(noun_text_file)
    verb_data = retrieve_word_list(verb_text_file)
    final_results = []

    for story in stories:
        persona, ending_text = identify_persona(story)
        persona_list.append(persona)
        actions, entities = identify_action_entity(ending_text, noun_data, verb_data)
        action_list.append(actions)
        entity_list.append(entities)
        output(story, persona, actions, entities)
        story_dictionary =create_dictionary(story, persona, actions, entities)
        final_results.append(story_dictionary)

    save_results(save_name, final_results, data_type_folder)

def command():
    '''
    Runs the command line inputs

    Returns:
        args.load_path (str): Path to the input file to be annotated
        save_folder_path (str): path to the folder to save the annotated results
        data_type_folder (str): type of dataset grouping

    Raises:
        FileNotFoundError: raises excpetion
        FileExistsError: raise exception
        wrong file type: raises exception
    '''

    parser = argparse.ArgumentParser(description = "This program is the most basic nlp tool that identifies entities and action based on a dictionary")
    parser.add_argument("load_path", type = str, help = "path of input dataset file to be annotated")
    parser.add_argument("save_name", type = str, help = "name of the saving file")
    parser.add_argument("data_type", type = str, choices=["BKLG", "CAT", "GLO"], help = "evaluation by individual backlogs - BKLG, categorized backlogs - CAT, or global - GLO")

    args = parser.parse_args()

    try:
        load_file = open(args.load_path)
        load_file.close()
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise

    else:
        if args.data_type == "BKLG":
            data_type_folder = "individual_backlog"
        elif args.data_type == "CAT":
            data_type_folder = "categories"
        else:
            data_type_folder = "global"

        return args.load_path, args.save_name, data_type_folder

def extract(load_path):
    '''
    Extracts each story from the the file 

    Parameters:
    load_path (str): path to the file with the stories to be annotated

    Returns:
    stories (list): each story in the datset
    '''

    with open (load_path, encoding="utf-8") as file:
        stories = file.readlines()
        for i in range(len(stories)):
            stories[i] = stories[i].strip("\n")

    return stories

def retrieve_word_list(load_file):
    '''
    Retrieves all the words in the file

    Parameters:
    load_file (str): file to load the words 

    Returns:
    word_list (list): list of words of the specific part of speech
    '''
    with open (load_file) as file:
        word_list = file.readlines()

    for i in range(len(word_list)):
        word_list[i] = word_list[i].strip(" \n")

    return word_list

def identify_persona(story):
    '''
    identifies the persona of the story

    Parameters:
    story (str): the story to be annotated

    Returns:
    persona (str): the identified persona of the story
    ending_text (str): the ending part of the story that does not include "#G00# As a persona,"
    '''
    story_split = story.partition(',')
    beginning_text = story_split[0]
    ending_text = story_split[2]

    if story[9:11] == "an":
        persona = beginning_text.partition("an")[2]
    else:
        persona = beginning_text.partition("a")[2]

    return persona, ending_text

def identify_action_entity(ending_text, noun_data, verb_data):
    '''
    identifies the actions and entities in the story 

    Parameters:
    ending_text(str): part of the story to be annotated
    noun_data (str): contains over 91K nouns
    verb_data (str): contains over 31K verbs

    Returns:
    story_action (list): identified actions in the story 
    story_entity (list): identified entities in the story
    '''

    story_action = []
    story_entity = []

    words = ending_text.split(" ")

    for word in words:
        word = word.strip(",.0123456789-/ ")
        word = word.lower()

        if word in verb_data:
            story_action.append(word)
        if word in noun_data:
            story_entity.append(word)
    
    return story_action, story_entity

def output (story, persona, actions, entities):
    '''
    Outputs the results to the terminal 

    Parameters:
    story (str): the story text
    persona (str): the persona identified in the story 
    actions (list): the actions identified in the story
    entities (list): the entities identified in the story 
    '''

    action_string = ""
    entity_string = ""

    for action_word in actions:
        action_string += action_word + ", "

    action_string.strip(", ")

    for entity_word in entities:
        entity_string += entity_word + ", "

    entity_string.strip(", ")

    print("\n-----------------------------------------------")
    print("Text:", story)
    print("Persona:", persona)
    print("Action:", action_string)
    print("Entity:", entity_string)

def create_dictionary(story, persona, actions, entities):
    '''
    create a dictionary for the results so it can be easily saved later 

    Parameters:
    story (str): the story text
    persona (str): the persona identified in the story 
    actions (list): the actions identified in the story
    entities (list): the entities identified in the story 
    
    Returns:
    story_dictionary (dictionary): contains the stoy text, identified persona, identified actions, and identifies entities
    '''

    story_dictionary = {
                        "Text": story,
                        "Persona": [persona], 
                        "Action" : actions,
                        "Entity": entities
                        }

    return story_dictionary

def save_results(save_name, final_results, data_type_folder):
    '''
    Save the results to a json file

    Parameters:
    save_name (str): the name of the file to be saved
    final_results (dictionary): contains the annotations of each story from this simple nlp
    data_type_folder (str): type of folder to save into
    '''

    save_file_name =  "nlp\\nlp_outputs\\" + data_type_folder+ "\\nlp_outputs_original\\simple_nlp\\" + save_name + "_simple_nlp.json"

    json.dumps(final_results)
    with open(save_file_name,"w", encoding="utf-8") as file:
        json.dump(final_results, file, ensure_ascii=False, indent = 4)

    print("\n\nFile is saved: " + save_file_name)

if __name__ == "__main__":
    main()