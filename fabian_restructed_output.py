import argparse
import json
import os
import sys


def main():
    load_path, save_name = command()
    required_data = extract(load_path)
    output_data = create_output(required_data)
    save_results(output_data, save_name)

def command():
    '''
    Runs the command line inputs

    Returns:
        args.load_path (str): Path to the file to be loaded
        args.save_name (str): Path to the file to be saved

    Raises:
        FileNotFoundError: raises excpetion
        wrong file type: raises exception
    '''
    
    parser = argparse.ArgumentParser(description = "This program will convert fabian's output to output that is useable by comparison.py")
    parser.add_argument("load_path", type = str, help = "path to the file of to convert output")
    parser.add_argument("save_name", type = str, help = "name of the file of to save results")

    args = parser.parse_args()

    if not(args.load_path.endswith(".json")):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect input file type. Input file type is .json")

    try:
        file = open(args.load_path)
        file.close()
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        return args.load_path, args.save_name

def extract (path):
    '''
    extrat the neccessary info from the file 

    Parameters:
    path (str): path to the file 

    Returns:
    required_data (3D list): the text, persona, entity, actions of each story in the dataset
    '''

    text = []
    persona = []
    entity = []
    action = []

    file = open(path)
    data = json.load(file)

    stories = data["stories"]
    pid = data["case"].capitalize()
    identifier = "#" + pid + "# "

    for story in stories:
        text.append(identifier + story["text"])
        persona.append(story["personas"])
        entity.append(story["entities"])
        action.append(story["actions"])
    file.close()

    required_data = [text, persona, entity, action]

    return required_data

def create_output(data):
    '''
    create the output layout for json file

    Parameters:
    required_data (3D list): the text, persona, entity, actions of each story in the dataset

    Returns:
    dictionary_list (list): dictionaries of all the data for json output
    '''

    text, persona, entity, action = data
    dictionary_list = []

    for i in range(len(text)):
        dictionary = {
                    "Text": text[i],
                    "Persona": persona[i],
                    "Entity": entity[i], 
                    "Action": action[i]
                    }
        dictionary_list.append(dictionary)

    return dictionary_list

def save_results(output_data, save_name):
    '''
    saves the results to json file

    Parameters:
    output_data (list): contains the output for the json file
    save_name (str): name of the file to be saved 
    '''

    save_path = "nlp_outputs\\fabian\\" + save_name + ".json"

    json.dumps(output_data)
    with open(save_path,"w", encoding="utf-8") as file:
        json.dump(output_data, file, ensure_ascii=False, indent = 4)

if __name__ == "__main__":
    main()