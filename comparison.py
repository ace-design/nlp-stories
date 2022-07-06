#This file will compare the results of the baseline and the nlp tools annotations for accuracy
#POS tags: https://universaldependencies.org/u/pos/ 

import argparse
import copy
import csv
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import stanza
import subprocess
import sys

def main():
    base_path, nlp_tool_path, save_folder_path, comparison_mode, save_name = command()

    base_path = check_pos_file(base_path, save_name)

    primary_baseline_data, primary_pos_data = extract_primary_baseline_info(base_path)
    all_baseline_data, all_pos_data = extract_all_baseline_info(base_path)
    nlp_tool_data = extract_nlp_tool_info(nlp_tool_path)

    
    primary_save_path = save_folder_path + "\\primary"
    all_save_path = save_folder_path + "\\all"
    os.mkdir(primary_save_path)
    os.mkdir(all_save_path)

    primary_csv_folder_path = "dataset_csv_final_results\\primary_csv_results\\"
    all_csv_folder_path = "dataset_csv_final_results\\all_csv_results\\"

    stanza.download('en') 
    stanza_pos_nlp = stanza.Pipeline('en')
 
    primary_story_results, primary_count_list, primary_comparison_collection, primary_missing_stories, primary_baseline_text = compare_and_get_results(primary_baseline_data, nlp_tool_data, comparison_mode, primary_pos_data, stanza_pos_nlp)
    output_results(primary_story_results, primary_count_list, primary_comparison_collection, primary_missing_stories, primary_baseline_text, primary_save_path, primary_csv_folder_path, comparison_mode)

    all_story_results, all_count_list, all_comparison_collection, all_missing_stories, all_baseline_text = compare_and_get_results(all_baseline_data, nlp_tool_data, comparison_mode, all_pos_data, stanza_pos_nlp)
    output_results(all_story_results, all_count_list, all_comparison_collection, all_missing_stories, all_baseline_text, all_save_path, all_csv_folder_path, comparison_mode)


    if comparison_mode == 1:
        path = "dataset_names_list\\dataset_list_strict.txt"
    elif comparison_mode == 2:
        path = "dataset_names_list\\dataset_list_inclusion.txt"
    else:
        path = "dataset_names_list\\dataset_list_relaxed.txt"

    save_dataset(path, save_name)

def compare_and_get_results(baseline_data, nlp_tool_data, comparison_mode, pos_data, stanza_pos_nlp):
    '''
    Runs all the functions that will compare and get the results of the comparison

    Parameters:
    baseline_data (2D list): contains text, persona, primary entities, and primary actions identified by the baseline data
    nlp_tool_data (2D list): contains text, persona, primary entities, and primary actions identified by the nlp tool 
    comparison_mode (int): determines the mode of comparing (1-strict, 2-inclusive, 3-relaxed)
    pos_data (3D list): contains the pos data of persona, entity, and action
    stanza_pos_nlp (class): runs the stanza application to get the tags

    Returns:
    story_results (3D list): has the precision, recall and f-measure of each story for the persona, action, entity
    count_list (3D list): has the count for persona, entity, action results for each story for the number of true/false postive and false negative
    comparison_collection (3D list): has the elements for persona, entity, action results for each story for the elements that are true/false postive and false negative
    missing_stories (2D list): missing stories from baseline_data and nlp tool 
    baseline_text (list): story text in order based on evaluation order
    '''
    sorted_baseline_data, sorted_nlp_tool_data, sorted_pos, missing_stories = sort(baseline_data, nlp_tool_data, pos_data)

    baseline_text, baseline_persona, baseline_entity, baseline_action = sorted_baseline_data
    _, nlp_persona, nlp_entity, nlp_action = sorted_nlp_tool_data

    persona_comparison_collection = []
    entity_comparison_collection = []
    action_comparison_collection = []
    count_persona_comparison_list = []
    count_entity_comparison_list = []
    count_action_comparison_list = []
   
    for i in range(len(baseline_text)):
        #Strict comparison 
        if comparison_mode == 1:
            persona_comparison = strict_compare(baseline_persona[i], nlp_persona[i])
            entity_comparison = strict_compare(baseline_entity[i], nlp_entity[i])
            action_comparison = strict_compare(baseline_action[i], nlp_action[i])
        #Inclusion comparison
        elif comparison_mode == 2:
            persona_comparison = inclusion_compare(baseline_persona[i], nlp_persona[i])
            entity_comparison = inclusion_compare(baseline_entity[i], nlp_entity[i])
            action_comparison = inclusion_compare(baseline_action[i], nlp_action[i])
        #relaxed comparison
        else:
            persona_pos, entity_pos, action_pos = sorted_pos
            persona_comparison = relaxed_compare(baseline_persona[i], nlp_persona[i], persona_pos[i], stanza_pos_nlp)
            entity_comparison = relaxed_compare(baseline_entity[i], nlp_entity[i], entity_pos[i], stanza_pos_nlp)
            action_comparison = relaxed_compare(baseline_action[i], nlp_action[i], action_pos[i], stanza_pos_nlp)

        persona_comparison_collection.append(persona_comparison)
        entity_comparison_collection.append(entity_comparison)
        action_comparison_collection.append(action_comparison)

        count_persona_comparison = count_true_false_positives_negatives(persona_comparison)
        count_entity_comparison = count_true_false_positives_negatives(entity_comparison)
        count_action_comparison = count_true_false_positives_negatives(action_comparison)

        count_persona_comparison_list.append(count_persona_comparison)
        count_entity_comparison_list.append(count_entity_comparison)
        count_action_comparison_list.append(count_action_comparison)

    count_list = [count_persona_comparison_list, count_entity_comparison_list, count_action_comparison_list]
    comparison_collection = [persona_comparison_collection, entity_comparison_collection, action_comparison_collection]
    
    story_results = individual_story(count_list)

    return story_results, count_list, comparison_collection, missing_stories, baseline_text

def output_results(story_results, count_list, comparison_collection, missing_stories, baseline_text, save_folder_path, csv_folder_path, comparison_mode):
    ''''
    Ouput the results to various formats

    Parameters:
    story_results (3D list): has the precision, recall and f-measure of each story for the persona, action, entity
    count_list (3D list): has the count for persona, entity, action results for each story for the number of true/false postive and false negative
    comparison_collection (3D list): has the elements for persona, entity, action results for each story for the elements that are true/false postive and false negative
    missing_stories (2D list): missing stories from baseline_data and nlp tool 
    baseline_text (list): story text in order based on evaluation order
    save_folder_path (str): the path of the folder to save results
    csv_folder_path (str): path to save final results to 
    comparison_mode (int): the mode of the comparision that was completed on the data (1-strict, 2-inclusive, 3-relaxed)
    '''
    x_axis_data = np.linspace(10,100,10)
    bargraph(story_results, x_axis_data, save_folder_path)

    dataset_results = total_dataset(count_list)

    output_terminal(baseline_text, comparison_collection, dataset_results, story_results, missing_stories)
    save_missing_stories(missing_stories, save_folder_path)
    save_csv(csv_folder_path, dataset_results, comparison_mode)

def individual_story(count_list):
    '''
    get all the info for plotting for each individual story

    Parameters:
    count_list (2D list): for each story, has the total count for true/false positives and false negative

    Returns:
    story_results (3D list): has the precision, recall and f-measure of each story for the persona, action, entity    
    '''
    count_persona_comparison_list, count_entity_comparison_list, count_action_comparison_list = count_list

    story_persona_precision = []
    story_entity_precision = []
    story_action_precision = []
    
    story_persona_recall = []
    story_entity_recall = []
    story_action_recall = []

    story_persona_f_measure = []
    story_entity_f_measure = []
    story_action_f_measure = []

    for i in range(len(count_persona_comparison_list)):
        persona_precision = calculate_precision(count_persona_comparison_list[i])
        entity_precision = calculate_precision(count_entity_comparison_list[i])
        action_precision = calculate_precision(count_action_comparison_list[i])

        story_persona_precision.append(persona_precision)
        story_entity_precision.append(entity_precision)
        story_action_precision.append(action_precision)

        persona_recall = calculate_recall(count_persona_comparison_list[i])
        entity_recall = calculate_recall(count_entity_comparison_list[i])
        action_recall = calculate_recall(count_action_comparison_list[i])

        story_persona_recall.append(persona_recall)
        story_entity_recall.append(entity_recall)
        story_action_recall.append(action_recall)

        persona_f_measure = calculate_f_measure(persona_precision, persona_recall)
        entity_f_measure = calculate_f_measure(entity_precision, entity_recall)
        action_f_measure = calculate_f_measure(action_precision, action_recall)

        story_persona_f_measure.append(persona_f_measure)
        story_entity_f_measure.append(entity_f_measure)
        story_action_f_measure.append(action_f_measure)

    precision_results = [story_persona_precision, story_entity_precision, story_action_precision]
    recall_results = [story_persona_recall, story_entity_recall, story_action_recall]
    f_measure_results = [story_persona_f_measure, story_entity_f_measure, story_action_f_measure]

    story_results = [precision_results, recall_results, f_measure_results]

    return story_results

def total_dataset(count_list):
    '''
    Gets all the required info for the entire dataset

    Parameters:
    count_list (2D list): for each story, has the total count for true/false positives and false negative
    
    Returns:
    dataset_results (2D list): calculated precison, recall, and f-measure of persona, entity, action of the whole dataset
    '''

    count_persona_comparison_list, count_entity_comparison_list, count_action_comparison_list = count_list 

    total_persona_comparison = count_total_result_dataset(count_persona_comparison_list)
    total_entity_comparison = count_total_result_dataset(count_entity_comparison_list)
    total_action_comparison = count_total_result_dataset(count_action_comparison_list)

    dataset_persona_precision = calculate_precision(total_persona_comparison)
    dataset_entity_precision = calculate_precision(total_entity_comparison)
    dataset_action_precision = calculate_precision(total_action_comparison)

    dataset_persona_recall = calculate_recall(total_persona_comparison)
    dataset_entity_recall = calculate_recall(total_entity_comparison)
    dataset_action_recall = calculate_recall(total_action_comparison)

    total_persona_f_measure = calculate_f_measure(dataset_persona_precision, dataset_persona_recall)
    total_entity_f_measure = calculate_f_measure(dataset_entity_precision, dataset_entity_recall)
    total_action_f_measure = calculate_f_measure(dataset_action_precision, dataset_action_recall)

    
    dataset_precision = [dataset_persona_precision, dataset_entity_precision, dataset_action_precision]
    dataset_recall = [dataset_persona_recall, dataset_entity_recall, dataset_action_recall]
    dataset_f_measure = [total_persona_f_measure, total_entity_f_measure, total_action_f_measure]
    
    dataset_results = [dataset_precision, dataset_recall, dataset_f_measure]

    return dataset_results

def command():
    '''
    Runs the command line inputs

    Returns:
        args.load_baseline_path (str): Path to the baseline evaluation file to be loaded
        args.load_nlp_tool_path (str): Path to the nlp tool evaluation file to be loaded
        save_folder_path (str): Path to the file to be saved
        args.comparison_mode (int): the comparison mode, where (1-strict, 2-inclusive, 3-relaxed)
        args.save_folder_name (str): name of file to save

    Raises:
        FileNotFoundError: raises excpetion
        FileExistsError: raise exception
        wrong file type: raises exception
        wrpng comparioson mode value: raises exception (must be either 1, 2, or 3)
    '''
    parser = argparse.ArgumentParser(description = "This program is to compare accuracy of NLP")
    parser.add_argument("load_baseline_path", type = str, help = "path of file")
    parser.add_argument("load_nlp_tool_path", type = str, help = "path of file to save")
    parser.add_argument("save_folder_name", type = str, help = "name of the folder to save the graphs")
    parser.add_argument("comparison_mode", type = int, help = "Comparision mode for comparing. Following are options: (1-strict, 2-inclusive, 3-relaxed)")
    
    args = parser.parse_args()

    if not(args.comparison_mode == 1 or args.comparison_mode == 2 or args.comparison_mode == 3):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect mode value. Following are options: (1-strict, 2-inclusive, 3-relaxed)")


    if not(args.load_nlp_tool_path.endswith(".json") and args.load_baseline_path.endswith(".json")):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect input file type. input file type is .json")

    try:
        load_baseline_file = open(args.load_baseline_path)
        load_baseline_file.close()
        load_nlp_tool_path = open(args.load_nlp_tool_path)
        load_nlp_tool_path.close()

        if args.comparison_mode == 1:
            save_folder_path = "graphs\\" + args.save_folder_name + "_strict_comparison"
        elif args.comparison_mode == 2:
            save_folder_path = "graphs\\" + args.save_folder_name + "_inclusive_comparison"
        else:
            save_folder_path = "graphs\\" + args.save_folder_name + "_relaxed_comparison"
        
        
        os.mkdir(save_folder_path)
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    except FileExistsError:
        sys.tracebacklimit = 0
        print("Saving path already exists")
        raise
    else:
        return args.load_baseline_path, args.load_nlp_tool_path, save_folder_path, args.comparison_mode, args.save_folder_name

def check_pos_file(load_path, save_name):
    '''
    Checks if the input path is a pos.json file and if not, it will create a pos file that contains the pos info of the annotations

    Parameters:
    load_path (str): path of the input file
    save_name (Str): name of the file when saving
    '''

    if not(load_path.endswith("pos.json")):
        command_input = "python create_pos_baseline.py " + load_path + " " + save_name
        
        subprocess.run(command_input)

        saving_path = "outputs\\pos_baseline\\" + save_name +  "_pos.json"

        return saving_path
    else:
        return load_path

def extract_primary_baseline_info(path):
    '''
    Extracts the primary info from the baseline 

    Parameters:
    path (str): path to the file

    Returns:
    baseline_data (2D list): contains text, persona, primary entities, and primary actions identified by the baseline data
    pos_data (3D list): contains the text and the POS of the each annotation in each story 
    '''
    text = []
    persona = []
    primary_entity = []
    primary_action = []
    persona_pos = []
    primary_entity_pos = []
    primary_action_pos = []

    file = open(path, encoding= "utf-8")
    data = json.load(file)

    for story in data:
        text.append(story["Text"])
        persona.append(story["Persona"])
        primary_entity.append(story["Entity"]["Primary Entity"])
        primary_action.append(story["Action"]["Primary Action"])
        persona_pos.append([story["Persona POS"]["Persona POS tag"], story["Persona POS"]["Persona POS text"]])
        primary_entity_pos.append([story["Entity POS"]["Primary Entity POS"]["Primary Entity POS tag"], story["Entity POS"]["Primary Entity POS"]["Primary Entity POS text"]])
        primary_action_pos.append([story["Action POS"]["Primary Action POS"]["Primary Action POS tag"], story["Action POS"]["Primary Action POS"]["Primary Action POS text"]])
    file.close()

    baseline_data = [text, persona, primary_entity, primary_action]
    pos_data = [persona_pos, primary_entity_pos, primary_action_pos]

    return baseline_data, pos_data

def extract_all_baseline_info(path):
    '''
    Extracts the info from the baseline 

    Parameters:
    path (str): path to the file

    Returns:
    baseline_data (2D list): contains text, persona, entities, and actions identified by the baseline data
    pos_data (3D list): contains the text and the POS of the each annotation in each story 
    '''
    text = []
    persona = []
    entity = []
    action = []
    persona_pos = []
    entity_pos = []
    action_pos = []
 

    file = open(path, encoding= "utf-8")
    data = json.load(file)

    for story in data:
        text.append(story["Text"])
        persona.append(story["Persona"])

        primary_entity = story["Entity"]["Primary Entity"]
        secondary_entity = story["Entity"]["Secondary Entity"]
        primary_action = story["Action"]["Primary Action"]
        secondary_action = story["Action"]["Secondary Action"]

        persona_pos.append([story["Persona POS"]["Persona POS tag"], story["Persona POS"]["Persona POS text"]])

        primary_entity_pos = story["Entity POS"]["Primary Entity POS"]["Primary Entity POS tag"]
        secondary_entity_pos = story["Entity POS"]["Secondary Entity POS"]["Secondary Entity POS tag"]
        primary_action_pos = story["Action POS"]["Primary Action POS"]["Primary Action POS tag"]
        secondary_action_pos = story["Action POS"]["Secondary Action POS"]["Secondary Action POS tag"]

        story_action = primary_action + secondary_action
        story_entity = primary_entity + secondary_entity

        while "" in story_action:
            story_action.remove("")

        action.append(story_action)

        while "" in story_entity:
            story_entity.remove("")
        
        entity.append(story_entity)

        if primary_action_pos !=[[]] and secondary_action_pos != [[]]:
            action_pos.append([primary_action_pos + secondary_action_pos, story["Action POS"]["Primary Action POS"]["Primary Action POS text"] + story["Action POS"]["Secondary Action POS"]["Secondary Action POS text"]])
        elif primary_action_pos != [[]]:
            action_pos.append([primary_action_pos, story["Action POS"]["Primary Action POS"]["Primary Action POS text"]])
        else:
            action_pos.append([secondary_action_pos, story["Action POS"]["Secondary Action POS"]["Secondary Action POS text"]])

        if primary_entity_pos != [[]] and secondary_entity_pos != [[]]:
            entity_pos.append([primary_entity_pos + secondary_entity_pos, story["Entity POS"]["Primary Entity POS"]["Primary Entity POS text"] + story["Entity POS"]["Secondary Entity POS"]["Secondary Entity POS text"]])
        elif primary_entity_pos != [[]]:
            entity_pos.append([primary_entity_pos, story["Entity POS"]["Primary Entity POS"]["Primary Entity POS text"]])
        else:
            entity_pos.append([secondary_entity_pos, story["Entity POS"]["Secondary Entity POS"]["Secondary Entity POS text"]])

    file.close()

    baseline_data = [text, persona, entity, action]
    pos_data = [persona_pos, entity_pos, action_pos]

    return baseline_data, pos_data

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

    file = open(path, encoding= "utf-8")
    data = json.load(file)

    for story in data:
        text.append(story["Text"])
        persona.append(story["Persona"])
        entity.append(story["Entity"])
        action.append(story["Action"])
    file.close()

    nlp_tool_data = [text, persona, entity, action]

    return nlp_tool_data

def sort(baseline_data, nlp_tool_data, pos_data):
    '''
    sorts the list in order to match the text, and detect missing stories

    Parameters:
    baseline_data (2D list): contains text, persona, primary entity, and primnary action identifies by the baseline data
    nlp_tool_data (2D list): contains text, persona, entity, and action identifies by the nlp tool data
    pos_data (3D list): contains the pos data of persona, entity, and action

    Returns:
    sorted_baseline_data(2D list): sorted text, persona, entity, and action identified of baseline_data (considering missing stories of nlp)
    sorted_nlp_tool_data (2D list): sorted text, persona, entity, and action identified coresponding to baseline_data
    sorted_pos (3d): sorted pos data based on sorted_baseline_data
    missing_stories (2D list): missing stories from baseline_data and nlp tool 
    '''
 
    baseline_text,baseline_persona, baseline_entity, baseline_action = baseline_data
    persona_pos_data, entity_pos_data, action_pos_data = pos_data
    nlp_tool_data_copy = copy.deepcopy(nlp_tool_data)
    nlp_text, nlp_persona, nlp_entity, nlp_action  = nlp_tool_data_copy
    
    sorted_baseline_text = []
    sorted_baseline_persona = []
    sorted_baseline_entity = []
    sorted_baseline_action= []

    sorted_nlp_text = []
    sorted_nlp_persona = []
    sorted_nlp_entity = []
    sorted_nlp_action= []

    sorted_persona_pos = []
    sorted_entity_pos = []
    sorted_action_pos = []

    for i in range(len(baseline_text)):
        for j in range(len(nlp_text)):
            if baseline_text[i].strip() == nlp_text[j].strip():

                sorted_baseline_text.append(baseline_text[i])
                sorted_baseline_persona.append(baseline_persona[i])
                sorted_baseline_entity.append(baseline_entity[i])
                sorted_baseline_action.append(baseline_action[i])

                sorted_nlp_text.append(nlp_text[j])
                sorted_nlp_persona.append(nlp_persona[j])
                sorted_nlp_entity.append(nlp_entity[j])
                sorted_nlp_action.append(nlp_action[j])

                sorted_persona_pos.append(persona_pos_data[i])
                sorted_entity_pos.append(entity_pos_data[i])
                sorted_action_pos.append(action_pos_data[i])
                
                del nlp_text[j]
                del nlp_persona[j]
                del nlp_entity[j]
                del nlp_action[j]
                break

    nlp_missing_story = set(baseline_text).difference(set(sorted_baseline_text))
    nlp_missing_story_list = list(nlp_missing_story)

    baseline_missing_story_list = nlp_text

    sorted_baseline_data = [sorted_baseline_text, sorted_baseline_persona, sorted_baseline_entity, sorted_baseline_action]
    sorted_nlp_tool_data = [sorted_nlp_text, sorted_nlp_persona, sorted_nlp_entity, sorted_nlp_action]
    sorted_pos = [sorted_persona_pos, sorted_entity_pos, sorted_action_pos]
    missing_stories = [baseline_missing_story_list, nlp_missing_story_list]

    return sorted_baseline_data, sorted_nlp_tool_data, sorted_pos, missing_stories

def strict_compare (baseline, nlp):
    '''
    calculate the number of true/false positives and false negatives using STRICT comparison

    Parameters:
    baseline (list): the elements being compared to 
    nlp (list): the elements comparing for accuracy 

    Returns:
    comparison_results (2D list): includes the elements identified as true/false positives and false negatives
    '''

    true_positive = []
    false_positive = []

    for i in range(len(nlp)):
        nlp_element = nlp[i].lower().strip()
        not_true_positive = True

        for j in range (len(baseline)):
            baseline_element = baseline[j].lower().strip()

            if nlp_element == baseline_element:
                true_positive.append(baseline[j])
                baseline.pop(j)
                not_true_positive = False
                break

        if not_true_positive:
            false_positive.append(nlp_element)
    
    false_nagative = copy.deepcopy(baseline)

    comparison_results = [true_positive, false_positive, false_nagative]

    return comparison_results

def inclusion_compare (baseline, nlp):
    '''
    calculate the number of true/false positives and false negatives for inclusion comparison mode

    Parameters:
    baseline (list): the elements being compared to 
    nlp (list): the elements comparing for accuracy 

    Returns:
    comparison_results (2D list): includes the elements identified as true/false positives and false negatives, including half points
    '''
    true_positive = []
    false_positive = []

    for i in range(len(nlp)):
        nlp_element = nlp[i].lower().strip()
        not_true_positive = True

        #first checks if there are any exact cases
        for j in range (len(baseline)):
            baseline_element = baseline[j].lower().strip()

            if nlp_element == baseline_element:
                true_positive.append(baseline[j])
                baseline.pop(j)
                not_true_positive = False
                break

        #Checks if there is any inlcusions (not including qualifiers)
        if not_true_positive:
            for j in range (len(baseline)):
                baseline_element = baseline[j].lower().strip()
                if check_inclusion_elements(nlp_element, baseline_element) == True:
                    true_positive.append(baseline[j])
                    baseline.pop(j)
                    not_true_positive = False
                    break

        #If it still not identified as true_positive, then the element is a false positive
        if not_true_positive:
            false_positive.append(nlp_element)
    
    false_nagative = copy.deepcopy(baseline)

    comparison_results = [true_positive, false_positive, false_nagative]

    return comparison_results

def check_inclusion_elements(nlp_element, baseline_element):
    '''
    determine if an element is part of another element but does not contain any qualifiers

    Paramters:
    nlp_element (str): element from nlp tool to evaluate if common element exist
    baseline_element (str): element from baseline to evaluate if common element exist

    Returns:
    True if elements considers to be inclusive
    False if elements not consider to be inclusive
    '''
    nlp_element_list = nlp_element.split()
    baseline_element_list = baseline_element.split()

    if len(nlp_element_list) == len(baseline_element_list):
        for nlp in nlp_element_list:
            for baseline in baseline_element_list:
                if nlp in baseline or baseline in nlp:
                    #This part is to check if the other words in the annotation is the same or not (ex. baseline:["quickly", "adds"] and nlp["slowly", "add"],
                    # when comparing "add" and "adds, it will also make sure that "quickly" and "slowly" are same for it to be pass, in this case, it is a fail)
                    nlp_remove_comparing_word = copy.deepcopy(nlp_element_list)
                    nlp_remove_comparing_word.remove(nlp)
                    baseline_remove_comparing_word = copy.deepcopy(baseline_element_list)
                    baseline_remove_comparing_word.remove(baseline)

                    if nlp_remove_comparing_word == baseline_remove_comparing_word:
                        return True
    return False
        
def relaxed_compare(baseline, nlp, pos_data, stanza_pos_nlp):
    '''
    calculate the number of true/false positives and false negatives for relaxed comparison mode

    Parameters:
    baseline (list): the elements being compared to 
    nlp (list): the elements comparing for accuracy 
    pos_data (2d list): contains the POS data for each annotation of the label type 
    stanza_pos_nlp (class): runs the stanza application to get the tags

    Returns:
    comparison_results (2D list): includes the elements identified as true/false positives and false negatives, including half points
    '''
    true_positive = []
    false_positive = []
    false_negative = []
    left_over_baseline = []
    left_over_nlp = []

    baseline_pos_tag, baseline_pos_text = pos_data

    for i in range(len(nlp)):
        nlp_element = nlp[i].lower().strip()
        not_true_positive = True

        #first checks if there are any exact cases
        for j in range (len(baseline)):
            baseline_element = baseline[j].lower().strip()
            if nlp_element == baseline_element:
                true_positive.append(baseline[j])
                baseline.pop(j)
                baseline_pos_tag.pop(j)
                baseline_pos_text.pop(j)
                not_true_positive = False
                break 

        if not_true_positive:
            left_over_nlp.append(nlp_element)

    left_over_baseline = copy.deepcopy(baseline)

    #Remove qualifiers from annotations
    baseline_text = []
    nlp_text = []
    remove_qualifiers = ["ADJ", "ADP", "ADV","AUX", "CCONJ", "DET", "INTJ", "PUNCT", "SCONJ", "X"]

    for i in range(len(baseline_pos_tag)):
        pos_text = ""

        for j in range(len(baseline_pos_tag[i])):
            if not(baseline_pos_tag[i][j] in remove_qualifiers):
                pos_text += baseline_pos_text[i][j] + " "
        baseline_text.append(pos_text)

    for i in range(len(left_over_nlp)):
        nlp_stanza = stanza_pos_nlp(left_over_nlp[i])
        pos_text = ""

        for sent in nlp_stanza.sentences:
            for word in sent.words:
                if not(word.upos in remove_qualifiers):
                    pos_text += word.text + " "
        nlp_text.append(pos_text)

    #Compare with removed Qualifiers
    for i in range(len(nlp_text)):
        nlp_element = nlp_text[i].lower().strip()
        not_true_positive = True

        #first checks if there are any exact cases
        for j in range (len(baseline_text)):
            baseline_element = baseline_text[j].lower().strip()

            if nlp_element == baseline_element:
                true_positive.append(left_over_baseline[j])
                left_over_baseline.pop(j)
                baseline_text.pop(j)
                not_true_positive = False
                break 

        #If it still not identified as true_positive, then the element is a false positive
        if not_true_positive:
            false_positive.append(left_over_nlp[i])

    false_negative = copy.deepcopy(left_over_baseline)

    comparison_results = [true_positive, false_positive, false_negative]

    return comparison_results

def count_true_false_positives_negatives(comparison_results):
    '''
    count the number of true/false positives and false negatives 

    Parameters:
    comparison_results (2D list): includes the elements identified as true/false positives and false negatives.

    Returns:
    number_comparison (2D list): the number of elements identified as true/false positives and false negatives
    '''
    true_positive, false_positive, false_negative = comparison_results
    number_true_positive = len(true_positive)
    number_false_positive = len(false_positive)
    number_false_negative = len(false_negative)

    number_comparison = [number_true_positive, number_false_positive, number_false_negative]

    return number_comparison

def count_total_result_dataset (total_comparison_results):
    '''
    counts the total number of true/false positives and false negatives 

    Parameters:
    number_comparison (2D list): the number of elements identified as true/false positives and false negatives

    Returns:
    total_count (list): total number of true/false positives and false negatives in dataset
    '''

    total_true_positive = 0
    total_false_positive = 0
    total_false_negative = 0

    for count in total_comparison_results:
        total_true_positive += count[0]
        total_false_positive += count[1]
        total_false_negative += count[2]

    total_count = [total_true_positive, total_false_positive, total_false_negative]

    return total_count

def calculate_precision(number_compared_results):
    '''
    calculate the precision

    Parameters:
    number_compared_results (list): total number of true/false positives and false negatives in dataset

    Returns:
    precision (float): the precision of the data
    '''

    number_true_positive, number_false_positive, _ = number_compared_results

    if number_true_positive + number_false_positive == 0:
        precision = 0
    else:
        precision = number_true_positive / (number_true_positive + number_false_positive)

    return precision

def calculate_recall(number_compared_results):
    '''
    calculate the recall 

    Parameters:
    number_compared_results (list): total number of true/false positives and false negatives in dataset

    Returns:
    recall (float): the recall of the data
    '''

    number_true_positive, _ , number_false_negative = number_compared_results

    if number_true_positive + number_false_negative == 0:
        recall = 0
    else:
        recall = number_true_positive / (number_true_positive + number_false_negative)

    return recall 

def calculate_f_measure (precision, recall):
    '''
    calculate the f measure 

    Parameters: 
    precision (float): the precision of the data
    recall (float): the recall of the data

    Returns:
    f_measure (float): the F-measure of the data
    '''

    if (precision + recall) == 0:
        f_measure = 0
    else:
        f_measure = 2 * (precision * recall)/ (precision + recall)

    return f_measure

def bargraph(story_results, x_axis_data, save_folder_path):
    '''
    runs the commands to graph the precision, recall and f-measure of each story as a bargraph

    Parameters:
    story_results (3D list): contains the data of precision, recall and f-measure of each story
    x_axis_data (list): the interval for the data to be set up in 
    save_folder_path (str): path of the folder to save the graphs

    '''
    story_precision_results, story_recall_results, story_f_measure_results = story_results
    story_persona_precision, story_entity_precision, story_action_precision = story_precision_results
    story_persona_recall, story_entity_recall, story_action_recall = story_recall_results
    story_person_f_measure, story_entity_f_measure, story_action_f_measure = story_f_measure_results

    persona_precision_data = setup_bargraph_data(story_persona_precision, x_axis_data)
    persona_recall_data = setup_bargraph_data(story_persona_recall, x_axis_data)
    persona_f_measure_data = setup_bargraph_data(story_person_f_measure, x_axis_data)
    persona_title = "Persona"

    entity_precision_data = setup_bargraph_data(story_entity_precision, x_axis_data)
    entity_recall_data = setup_bargraph_data(story_entity_recall, x_axis_data)
    entity_f_measure_data = setup_bargraph_data(story_entity_f_measure, x_axis_data)
    entity_title = "Entity"

    action_precision_data = setup_bargraph_data(story_action_precision, x_axis_data)
    action_recall_data = setup_bargraph_data(story_action_recall, x_axis_data)
    action_f_measure_data = setup_bargraph_data(story_action_f_measure, x_axis_data)
    action_title = "Action"

    x_label = []
    for i in range(len(x_axis_data)):
        if i == 0:
            x_label.append("0 - " + str(x_axis_data[i]))
        else:
            x_interval = str(x_axis_data[i-1] +0.1 )+ " - " + str(x_axis_data[i]) 
            x_label.append(x_interval)


    create_bargraph(persona_precision_data, persona_recall_data, persona_f_measure_data, x_label, persona_title, save_folder_path, "\\persona_bargraph")
    create_bargraph(entity_precision_data, entity_recall_data, entity_f_measure_data, x_label, entity_title, save_folder_path, "\\entity_bargraph")
    create_bargraph(action_precision_data, action_recall_data, action_f_measure_data, x_label, action_title, save_folder_path, "\\action_bargraph")

def setup_bargraph_data(story_data, x_axis_data):
    '''
    sets up the data for the bar graph

    Parameters:
    story_data (list): contains the data to be set up 
    x_axis_data (lsit): the interval for the data to be set up in 

    Returns:
    bargraph_data (list): the setup up data to be inputed for the bargraph data
    '''
    bargraph_data = [0]*len(x_axis_data)
    for item in story_data:
        for i in range(len(x_axis_data)):
            if item*100 <= x_axis_data[i]:
                bargraph_data[i] += 1
                break

    return bargraph_data

def create_bargraph(precision_data, recall_data, f_measure_data, x_label, title, save_folder_path, save_name):
    '''
    creates and saves the bargraph

    Parameters
    precision_data (list): contains number of times the dataset has a certain precision within pre determined intervals
    recall_data (list): contains number of times the dataset has a certain recall within pre determined intervals
    f_measure_data (list): contains number of times the dataset has a certain f_measure within pre determined intervals
    x_label (list): the interval for the data to be set up in 
    title(str): the title of the graph 
    save_folder_path (str): the path to save the graphs
    save_name (str): name of the file for saving
    '''
    graph, (precision_plot, recall_plot, f_measure_plot) = plt.subplots(3, 1, figsize=(10, 5), sharex=True)

    sns.barplot(x=x_label, y=precision_data, ax= precision_plot, color= "m")
    precision_plot.set_ylabel("Precision")
    precision_plot.bar_label(precision_plot.containers[0])

    sns.barplot(x=x_label, y=recall_data, ax=recall_plot, color= "r")
    recall_plot.set_ylabel("Recall")
    recall_plot.bar_label(recall_plot.containers[0])

    sns.barplot(x=x_label, y=f_measure_data, ax=f_measure_plot , color= "b")
    f_measure_plot.set_ylabel("F-Measure")
    f_measure_plot.set_xlabel("Number of Occurance")
    f_measure_plot.bar_label(f_measure_plot.containers[0])
    graph.suptitle(title, fontsize = 16)

    plt.tight_layout()

    graph.savefig(save_folder_path + save_name + ".png")

def output_terminal(baseline_text, comparison_collection, dataset_results, story_results, missing_stories):
    '''
    output the results so that it is easy to read the results 

    Parameters:
    baseline_text (list): story text 
    comparison_collection (3D list): true/false positive and false negative of each story 
    dataset_results (2D list): calculated precison, recall, and f-measure of persona, entity, action of the whole dataset
    story_results (3D list): has the precision, recall and f-measure of each story for the persona, action, entity
    missing_stories (2D list): contains missing stories and data from baseline and/or nlp tool 
    '''
    persona_comparison_collection, entity_comparison_collection, action_comparison_collection = comparison_collection
    dataset_precision, dataset_recall, dataset_f_measure = dataset_results
    story_precision_results, story_recall_results, story_f_measure_results = story_results
    
    persona_precision, entity_precision, action_precision = dataset_precision 
    persona_recall, entity_recall, action_recall = dataset_recall
    persona_f_measure, entity_f_measure, action_f_measure = dataset_f_measure

    story_persona_precision, story_entity_precision, story_action_precision = story_precision_results
    story_persona_recall, story_entity_recall, story_action_recall = story_recall_results
    story_persona_f_measure, story_entity_f_measure, story_action_f_measure = story_f_measure_results

    baseline_missing_stories, nlp_tool_missing_stories = missing_stories

    for i in range(len(baseline_text)):
        print("Text:", baseline_text[i])
        print("__PERSONA__")
        print("True Positive:", ", ".join(persona_comparison_collection[i][0]))
        print("False Postive:", ", ".join(persona_comparison_collection[i][1]))
        print("False Negative:", ", ".join(persona_comparison_collection[i][2]))
        print("\nPrecision:", story_persona_precision [i])
        print("Recall:", story_persona_recall[i])
        print("F-Measure:", story_persona_f_measure[i])
        print("\n__ENTITY__")
        print("True Positive:", ", ".join(entity_comparison_collection[i][0]))
        print("False Postive:", ", ".join(entity_comparison_collection[i][1]))
        print("False Negative:", ", ".join(entity_comparison_collection[i][2]))
        print("\nPrecision:", story_entity_precision [i])
        print("Recall:", story_entity_recall[i])
        print("F-Measure:", story_entity_f_measure[i])
        print("\n__ACTION__")
        print("True Positive:", ", ".join(action_comparison_collection[i][0]))
        print("False Postive:", ", ".join(action_comparison_collection[i][1]))
        print("False Negative:", ", ".join(action_comparison_collection[i][2]))
        print("\nPrecision:", story_action_precision [i])
        print("Recall:", story_action_recall[i])
        print("F-Measure:", story_action_f_measure[i])
        print("\n________________________________________________________")

    print("DATASET RESULTS")
    print("__PERSONA__")
    print("Precision:", persona_precision)
    print("Recall:", persona_recall)
    print("F-Measure:", persona_f_measure)
    print("\n__ENTITY__")
    print("Precision:", entity_precision)
    print("Recall:", entity_recall)
    print("F-Measure:", entity_f_measure)
    print("\n__ACTION__")
    print("Precision:", action_precision)
    print("Recall:", action_recall)
    print("F-Measure:", action_f_measure)

    print("\nMissing Stories")
    print("Missing stories from baseline:", baseline_missing_stories)
    print("\nMissing stories from nlp tool:", nlp_tool_missing_stories)

def save_missing_stories(missing_stories, save_folder_path):
    '''
    save the missing stories from datasets into a text file

    Parameters:
    missing_stories (2D list): contains missing stories and data from baseline and/or nlp tool 
    save_folder_path (str): path of folder to save
    '''

    baseline_missing_stories, nlp_tool_missing_stories = missing_stories
    file_path = save_folder_path + "\\missing_stories.txt"
    file = open(file_path, "w")

    file.write("Missing Stories:\n")
    file.write("Missing stories from baseline:\n")
    for i in range(len(baseline_missing_stories)):
        file.write(baseline_missing_stories[i] + "\n")
    file.write("Missing stories from nlp tool:\n")
    for i in range(len(nlp_tool_missing_stories)):
        file.write(nlp_tool_missing_stories[i] + "\n")
        
    file.close()

def save_csv(saving_folder_path, dataset_results, comparison_mode):
    '''
    save the final results of dataset precision, recall and f-measure of persona, entity and action

    Parameters:
    saving_folder_path (str): path to the folder to save the data 
    dataset_results (2D list): calculated precison, recall, and f-measure of persona, entity, action of the whole dataset
    comparison_mode (int): the mode of the comparision that was completed on the data (1-strict, 2-inclusive, 3-relaxed)
    '''
    dataset_precision, dataset_recall, dataset_f_measure = dataset_results

    persona_precision, entity_precision, action_precision = dataset_precision 
    persona_recall, entity_recall, action_recall = dataset_recall
    persona_f_measure, entity_f_measure, action_f_measure = dataset_f_measure

    if comparison_mode == 1:
        saving_path = saving_folder_path + "strict_dataset_results.csv"
    elif comparison_mode == 2:
        saving_path = saving_folder_path + "inclusion_dataset_results.csv"
    else:
        saving_path = saving_folder_path + "relaxed_dataset_results.csv"

    data = [persona_precision, entity_precision, action_precision,persona_recall, entity_recall, action_recall,persona_f_measure, entity_f_measure, action_f_measure]

    with open (saving_path, "a", newline = "") as file:
        writer = csv.writer(file)
        writer.writerow(data)

def save_dataset(path, dataset_name):
    '''
    save the dataset name (will use the name of the save file name as the dataset name)

    Parameters:
    path (str): path to folder to save
    dataset_name(str): name of dataset
    '''
    with open(path, "a") as file:
        file.write(dataset_name + "\n")

if __name__ == "__main__":
    main()