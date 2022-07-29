#This file will write doccano outputted jsonl file to human understandable annotaion
#Links: https://jsonlines.readthedocs.io/en/latest/
#https://docs.python.org/3/howto/argparse.html#id1
import jsonlines
import json
import argparse
import sys

def main():
    load_path, save_path = command()

    dictionary_list = []
        
    print("Receiving results")
   
    text, entities, relations = extract(load_path)

    for i in range(len(text)):
        label_list, label_id_list, element_list = identify_labels(text[i], entities[i])
        relation_string_list, relation_list, primary_element_data = identify_relations(relations[i], label_id_list, element_list)
        
        primary_action, primary_action_list, primary_action_id_list, target_action, target_entity = primary_element_data
        primary_entity, primary_entity_list = identify_primary_entity(primary_action_id_list, target_action, target_entity)

        persona , entity_list, action_list, benefit, pid = label_list

        secondary_entity = secondary(entity_list, primary_entity_list)
        secondary_action = secondary(action_list, primary_action_list)

        labels = [persona, primary_entity, secondary_entity, primary_action, secondary_action, benefit, pid]
        output(text[i], labels, relation_string_list)

        
        dictionary = convert_json_format(text[i], labels, relation_list)
        dictionary_list.append(dictionary)
        
    print("Saving\n")
    save_file(save_path, dictionary_list)

def command():
    '''
    Runs the command line inputs

    Returns:
        args.load_path (str): Path to the file to be loaded
        args.save_name (str): name of the file to save results

    Raises:
        FileNotFoundError: raises excpetion
        wrong file type: raises exception
    '''

    parser = argparse.ArgumentParser(description = "This program is to convert jsonl files to human readiable files")
    parser.add_argument("load_path", type = str, help = "path of file")
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
        if args.data_type == "BKLG":
            data_type_folder = "individual_backlog"
        elif args.data_type == "CAT":
            data_type_folder = "categories"
        else:
            data_type_folder = "global"

        save_folder_path = "nlp\\nlp_outputs\\"+ data_type_folder + "\\nlp_outputs_original\\baseline\\" + args.save_name + "_baseline.json"
        return args.load_path, save_folder_path

def extract(path):
    '''
    Extracts the information of given file

    Parameters:
        path (str): Path of the file to extract info

    Returns:
        text (2D list): story text
        entities (2D list): entities and their location within the story
        relations (2D list): relations and their location within the story
    '''
    print(path)
    
    text = []
    entities = []
    relations = [] 
    with jsonlines.open(path) as file:
        for story in file:
            text.append(story["text"])
            entities.append(story["entities"])
            relations.append(story["relations"])

    return text, entities, relations

def identify_labels(text, entities):
    '''
    Identify and sort labels within story

    Paramaters:
        text (str): story text
        entities (list): entities and their locations within the story

    Returns:
        label_list (2D list): sorted str labels
        label_id_list (list): element Id
        element_list (list): element corresponding in order to label_id_list
    '''
    
    persona = ""
    entity = []
    action = []
    benefit = ""
    pid = ""

    label_id_list = []
    element_list = []

    for label in entities:
        label_id = label["id"]
        label_type = label["label"]
        start_offset = label["start_offset"]
        end_offset = label["end_offset"]
        element = text[start_offset : end_offset]

        label_id_list.append(label_id)
        element_list.append(element)

        if label_type == "Persona":
            persona += element + ", "
        elif label_type == "Entity":
            entity.append(element)
        elif label_type == "Action":
            action.append(element)
        elif label_type == "Benefit":
            benefit+= element + ", "
        elif label_type == "PID":
            pid = element

    label_list = [persona, entity, action, benefit, pid]

    return label_list, label_id_list, element_list

def identify_relations(relations, label_id_list, element_list):
    '''
    Identify and sort relations within story

    Parameters:
        relations (list): relations and their locations within story
        label_id_list (list): element Id
        element_list (list): element corresponding in order to label_id_list

    Returns:
        relation_string_list (2D list): sorted str relations
        relation_list (2D list): list of sorted pairs relations
        primary_element_data (2D list): data of primary elements
    '''
    
    triggers = ""
    targets = ""
    contains = ""
    primary_actions = ""
    primary_action_list = []
    primary_action_id_list = []
    target_action = []
    target_entity = []
    triggers_list = []
    targets_list = []
    contains_list = []
 
    
    for relation in relations:
        relation_type = relation["type"]
        start_id = relation["from_id"]
        end_id = relation["to_id"]

        start_element = find_element(label_id_list, element_list, start_id)
        end_element = find_element(label_id_list, element_list, end_id)
        
        if relation_type == "triggers":
            triggers += start_element + " --> " + end_element + ", "
            triggers_list.append([start_element, end_element])
            
            if not(end_id in primary_action_id_list):
                primary_actions += end_element + ", "
                primary_action_list.append(end_element)
                primary_action_id_list.append(end_id)
            
        elif relation_type == "targets":
            targets += start_element + " --> " + end_element + ", "
            targets_list.append([start_element, end_element])
            target_action.append([start_id, start_element])
            target_entity.append([end_id, end_element])
            
        elif relation_type == "contains":
            contains += start_element + " --> " + end_element + ", "
            contains_list.append([start_element, end_element])
    
    relation_string_list = [triggers, targets, contains]
    relation_list = [triggers_list, targets_list, contains_list]
    primary_element_data = [primary_actions, primary_action_list, primary_action_id_list, target_action, target_entity]

    return relation_string_list, relation_list, primary_element_data

def identify_primary_entity(primary_action_id_list, target_action, target_entity):
    '''
     identify primary entities

    Parameters:
        primary_action_id_list (list): contains all the primary actions in the story
        target_action (2D list): contains all ids and corresponding actions in the target relations
        target_entity (2D list): contains all ids and corresponding entities in the target relations

    Returns:
        primary_entities (str): indentified primary entities
        primary_entity_list (list): indentified primary entities
    '''
    
    primary_entities = ""
    primary_entity_list = []
    
    
    for primary_action_id in primary_action_id_list:
        for i in range(len(target_action)):
            if primary_action_id == target_action[i][0]:
                if not(target_entity[i][1] in primary_entity_list):
                    primary_entities += target_entity[i][1] + ", "
                    primary_entity_list.append(target_entity[i][1])
                
    return primary_entities, primary_entity_list

def find_element(label_id, element, find_id):
    '''
    find specific element within story

    Parameters:
        label_id (list): all element Id within story
        element (list): all element within story
        find_id (int): Id to search for

    Returns:
        element (string): element that is found
    '''
    
    for i in range(len(label_id)):
        if label_id[i] == find_id:
            return element[i]
    

def secondary (whole_list, primary_item):
    '''
    identify the secondary elements within story

    Parameters:
        whole_list (list) : all elements in story
        primary_item (list): all primary elements in story

    Returns:
        secondary_item (str): secondary elements in story
    '''
    
    secondary_item = ""
    
    for item in primary_item:
        whole_list.remove(item)

    for item in whole_list:
        secondary_item += item + ", "

    return secondary_item

def output(text,label_list, relation_string_list):
    '''
    outputs results to terminal

    Parameters:
        text (str): story text
        label_list (2D list): str of all sorted labels in story
        relation_string_list (2D list): str of all sorted relations in story
    '''
    
    persona, primary_entity, secondary_entity, primary_action, secondary_action, benefit, pid = label_list
    triggers, targets, contains = relation_string_list

    print("--------------------STORY START--------------------")
    print("PID:", pid.strip(", "))
    print("Story text:", text)
    print("\n")
    print("Persona:", persona.strip(", "))
    print("Primary Action:", primary_action.strip(", "))
    print("Secondary Action:", secondary_action.strip(", "))
    print("Primary Entity:", primary_entity.strip(", "))
    print("Secondary Entity:", secondary_entity.strip(", "))
    print("Benefit:", benefit.strip("., "))
    print("\n")
    print("Triggers:", triggers.strip(", "))
    print("Targets:", targets.strip(", "))
    print("Contains:", contains.strip(", "))
    print("---------------------STORY END---------------------\n")

def convert_json_format(text, label_list, relation_list):
    '''
    converts results to json file format

    Parameters:
        text (str): story text
        label_list (2D list): str of all sorted labels in story
        relation_list (2D list): str of all sorted relations in story

    Returns:
        data (dictionary): includes all sorted information about the story      
    '''
    persona, primary_entity, secondary_entity, primary_action, secondary_action, benefit, pid = label_list
    triggers, targets, contains = relation_list

    data = {
            "PID": pid.strip(", "),
            "Text": text,
            "Persona": persona.strip(", ").split(", "),
            "Action":{"Primary Action": primary_action.strip(", ").split(", "),\
                        "Secondary Action": secondary_action.strip(", ").split(", ")},
            "Entity":{"Primary Entity": primary_entity.strip(", ").split(", "),\
                      "Secondary Entity": secondary_entity.strip(", ").split(", ")},
            "Benefit": benefit.strip("., "),
            "Triggers": triggers,
            "Targets": targets,
            "Contains": contains}

    return data 

def save_file(path, dictionary_list):
    '''
    save the results into json file

    Parameters:
        path (str): path of file to be saved
        dictionary_list (list): info to be saved onto file
    '''
    json.dumps(dictionary_list)
    with open(path,"w", encoding="utf-8") as file:
        json.dump(dictionary_list, file, ensure_ascii=False, indent = 4)
    print("File is saved")

if __name__ == "__main__":
    main()
