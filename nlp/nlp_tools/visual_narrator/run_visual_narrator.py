#This file will extract the info from the visual narrator nlp tool and output to json file
import argparse
import subprocess
import sys
import json

def main():
    data, save_path, stories = extract_visual_Narrator()
    line_story_data = split_data(data)
    dictionary_list =[]
    
    for i in range(len(line_story_data)):
        functional_role = extract_label_info(line_story_data[i], 7)
        main_verb = extract_label_info(line_story_data[i], 9)
        main_object = extract_label_info(line_story_data[i], 10)
        
        identified_labels = [functional_role, main_verb, main_object]
        output(identified_labels, stories[i])
        dictionary = json_format(identified_labels, stories[i])
        dictionary_list.append(dictionary)

    save_json(save_path, dictionary_list)
    

def extract_visual_Narrator():
    '''
    Run the visual narrator with given input file

    Returns:
    data (str) : output from the command window
    args.save_name (str) : path of file to save restults
    stories (list) : story text
    data_type (str): type of grouping of the data

    Raises:
    FileNotFoundError: raises excpetion

    '''
    
    parser = argparse.ArgumentParser(description = "This script is to run visual narrator on the given input datset")
    parser.add_argument("load_path", type = str, help = "path to file of evaluation")
    parser.add_argument("save_name", type = str, help = "name of file to save")
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
        #strip off PID because Visual narrator has trouble with them
        read_file = open(args.load_path)
        stories = read_file.readlines()
        text = []
        for story in stories:
            story = story[6:-1].strip("\n")
            text.append(story)
        read_file.close()
        
        write_file = open("nlp\\nlp_tools\\visual_narrator\\visual_narrator_extraction\\strip_text_visual_narrator.txt", "w")
        for story in text:
            write_file.write(story + "\n")
        write_file.close()
        
        #runs visual narrator of stripped off PID
        command = subprocess.run("python nlp\\nlp_tools\\visual_narrator\\run.py nlp\\nlp_tools\\visual_narrator\\visual_narrator_extraction\\strip_text_visual_narrator.txt -u", capture_output = True)
        #data = command.stdout.decode()
        data = command.stdout.decode('latin-1')

        if args.data_type == "BKLG":
            data_type_folder = "individual_backlog"
        elif args.data_type == "CAT":
            data_type_folder = "categories"
        else:
            data_type_folder = "global"

        save_path = "nlp\\nlp_outputs\\" + data_type_folder + "\\nlp_outputs_original\\visual_narrator\\" + args.save_name + "_visual_narrator.json"

        return data, save_path, stories

def split_data(data):
    '''
    splits the data into stories into lines

    Parameters:
    data (str): output from the command window

    Returns:
    line_data (2D list): each line from command window grouped into stories 

    '''

    story = data.split("<---------- BEGIN U S ---------->")
    line_data = []
    
    for i in range(len(story)-1):
        line_data.append(story[i+1].split("\n"))

    return line_data

def extract_label_info(story, index):
    '''
    extract specific labels from dataat known index

    Parameters:
    story (list): each line of a story
    index (int): position in list where label exist

    Returns:
    label: identified persona of the story

    '''
    label_string = story[index]
    start_index = label_string.find(":") + 1
    end_index = label_string.find("(")
    if end_index == -1:
        label = label_string[start_index:].replace("\r","").strip()
    else:
        label = label_string[start_index:end_index].strip()

    return label

def output (identified_labels, story):
    '''
    ouputs the results to command window

    Parameters:
    identified_labels (list): persona, action, entity of each story
    story (str) : the story of current evaluation
    '''

    persona, action, entity = identified_labels
    print("Story:", story.strip("\n"))
    print("Persona:", persona)
    print("Action:", action)
    print("Entity:", entity)
    print("Trigger:", persona, "-->", action)
    print("Targets:", action, "-->", entity)
    print("\n\n")
        
def json_format(identified_labels, story):
    '''
    format the results for a json file

    Parameters:
    identified_labels (list): persona, action, entity of each story
    story (str) : the story of current evaluation
    '''

    persona, action, entity = identified_labels
    
    data = {
            "Text": story.strip("\n"),
            "Persona": [persona],
            "Action": [action],
            "Entity": [entity],
            "Triggers": [persona, action],
            "Targets": [action, entity]
            }

    return data

def save_json(save_path, dictionary_list):
    '''
    saves the results to a json file

    Parameters:
    save_path (str): path directory to save
    dictionary_list (list): dictionaries of all the data
    '''

    json.dumps(dictionary_list)
    with open(save_path,"w", encoding="utf-8") as file:
        json.dump(dictionary_list, file, ensure_ascii=False, indent = 4)
    print("File is saved")
    
if __name__ == "__main__":
    main()
    
