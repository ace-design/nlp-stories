import argparse
from email.mime import base
import json
import sys


def main():
    base_path, nlp_tool_path, save_path = command()
    baseline_data = extract_baseline_info(base_path)
    nlp_tool_data = extract_nlp_tool_info(nlp_tool_path)
    
    sorted_nlp_tool_data = sort(baseline_data, nlp_tool_data)


def command():
    '''
    Runs the command line inputs

    Returns:
        args.load_baseline_path (str): Path to the baseline evaluation file to be loaded
        args.load_nlp_tool_path (str): Path to the nlp tool evaluation file to be loaded
        args.save_path (str): Path to the file to be saved

    Raises:
        FileNotFoundError: raises excpetion
        wrong file type: raises exception
    '''
    parser = argparse.ArgumentParser(description = "This program is to compare accuracy of NLP")
    parser.add_argument("load_baseline_path", type = str, help = "path of file")
    parser.add_argument("load_nlp_tool_path", type = str, help = "path of file to save")
    parser.add_argument("save_path")
    
    args = parser.parse_args()

    if not(args.load_nlp_tool_path.endswith(".json") and args.load_baseline_path.endswith(".json")):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect saving file type. Save file type is .json")
    try:
        load_baseline_file = open(args.load_baseline_path)
        load_baseline_file.close()
        load_nlp_tool_path = open(args.load_nlp_tool_path)
        load_nlp_tool_path.close()
        save_file = open(args.save_path)
        save_file.close()
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        return args.load_baseline_path, args.load_nlp_tool_path, args.save_path    

def extract_baseline_info(path):
    '''
    Extracts the info from the baseline 

    Parameters:
    path (str): path to the file

    Returns:
    baseline_data (2D list): contains text, persona, primary entities, and primary actions identified by the baseline data
    '''
    text = []
    persona = []
    primary_entity = []
    primary_action = []

    file = open(path)
    data = json.load(file)

    for story in data:
        text.append(story["Text"])
        persona.append(story["Persona"])
        primary_entity.append(story["Entity"]["Primary Entity"])
        primary_action.append(story["Action"]["Primary Action"])
    file.close()

    baseline_data = [text, persona, primary_entity, primary_action]

    return baseline_data

def extract_nlp_tool_info(path):
    '''
    Extracts the info from the evaluation of the nlp tool 

    Parameters:
    path (str): path to the file

    Returns:
    nlp_tool_data (2D list): contains text, persona, entity, and action identified by the nlp tool data
    '''
    text = []
    persona = []
    entity = []
    action = []

    file = open(path)
    data = json.load(file)

    for story in data:
        text.append(story["Text"])
        persona.append(story["Persona"])
        entity.append(story["Entity"])
        action.append(story["Action"])
    file.close()

    nlp_tool_data = [text, persona, entity, action]

    return nlp_tool_data
def sort(baseline_data, nlp_tool_data):
    '''
    sorts the list in order to match the text

    Parameters:
    baseline_data (2D list): contains text, persona, primary entity, and primnary action identifies by the baseline data
    nlp_tool_data (2D list): contains text, persona, entity, and action identifies by the nlp tool data

    Returns:
    sorted_nlp_tool_data (2D list): sorted text, persona, entity, and action identified coresponding to baseline_data
    '''
    baseline_text,_, _, _ = baseline_data
    nlp_text, nlp_persona, nlp_action, nlp_entity = nlp_tool_data

    sorted_text = []
    sorted_persona = []
    sorted_entity = []
    sorted_action= []

    for i in range(len(baseline_text)):
        for j in range(len(nlp_text)):
            if baseline_text[i] == nlp_text[j]:
                sorted_text.append(nlp_text[j])
                sorted_persona.append(nlp_persona[j])
                sorted_entity.append(nlp_entity[j])
                sorted_action.append(nlp_action[j])
                del nlp_text[j]
                del nlp_persona[j]
                del nlp_entity[j]
                del nlp_action[j]
                break

    sorted_nlp_tool_data = [sorted_text, sorted_persona, sorted_entity, sorted_action]

    return sorted_nlp_tool_data

if __name__ == "__main__":
    main()