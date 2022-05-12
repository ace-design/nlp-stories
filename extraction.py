import argparse
import subprocess
import sys
import json

def main():
    data, save_path = extract_visual_Narrator()
    line_story_data = split_data(data)
    dictionary_list =[]
    
    for story in line_story_data:
        functional_role = extract_label_info(story, 7)
        main_verb = extract_label_info(story, 9)
        main_object = extract_label_info(story, 10)
        identified_labels = [functional_role, main_verb, main_object]
        output(identified_labels)
        dictionary = json_format(identified_labels)
        dictionary_list.append(dictionary)

    save_json(save_path, dictionary_list)
    

def extract_visual_Narrator():
    '''
    Run the visual narrator with given input file

    Returns:
    data (str): output from the command window

    '''
    
    parser = argparse.ArgumentParser()
    parser.add_argument("load_path", type = str, help = "path to file of evaluation")
    parser.add_argument("save_path", type = str, help = "path to file of evaluation")
    args = parser.parse_args()

    try:
        load_file = open(args.load_path)
        load_file.close()
        save_file = open(args.save_path)
        save_file.close()
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else: 
        command = subprocess.run("python visual_narrator_extraction\\run.py " + args.load_path + " -u", capture_output = True)
        data = command.stdout.decode()
        return data, args.save_path

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

def output (identified_labels):
    '''
    ouputs the results to command window

    Parameters:
    identified_labels (list): persona, action, entity of each story
    '''

    persona, action, entity = identified_labels
    print("Persona:", persona)
    print("Action:", action)
    print("Entity:", entity)
    print("Trigger:", persona, "-->", action)
    print("Targets:", action, "-->", entity)
    print("\n\n")
        
def json_format(identified_labels):
    '''
    format the results for a json file

    Parameters:
    identified_labels (list): persona, action, entity of each story
    '''

    persona, action, entity = identified_labels
    
    data = {
            "Persona": persona,
            "Action": action,
            "Entity": entity,
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
    with open(save_path,"w") as file:
        json.dump(dictionary_list, file, ensure_ascii=False, indent = 4)
    print("File is saved")
    
if __name__ == "__main__":
    main()







    
