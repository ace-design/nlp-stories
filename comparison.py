#This file will compare the results of the baseline and the nlp tools annotations for accuracy
import argparse
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import sys

def main():
    base_path, nlp_tool_path, save_folder_path = command()
    baseline_data = extract_baseline_info(base_path)
    nlp_tool_data = extract_nlp_tool_info(nlp_tool_path)

    sorted_nlp_tool_data = sort(baseline_data, nlp_tool_data)

    baseline_text, baseline_persona, baseline_entity, baseline_action = baseline_data
    nlp_text, nlp_persona, nlp_entity, nlp_action = sorted_nlp_tool_data


    persona_comparison_collection = []
    entity_comparison_collection = []
    action_comparison_collection = []
    count_persona_comparison_list = []
    count_entity_comparison_list = []
    count_action_comparison_list = []


    for i in range(len(baseline_text)):
        persona_comparison = compare(baseline_persona[i], nlp_persona[i])
        entity_comparison = compare(baseline_entity[i], nlp_entity[i])
        action_comparison = compare(baseline_action[i], nlp_action[i])

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
    story_precision_results, story_recall_results, story_f_measure_results = story_results


    scatterplot_data = [story_precision_results, story_recall_results]
    scatterplot(scatterplot_data, save_folder_path)

    x_axis_data = np.linspace(10,100,10)
    bargraph(story_results, x_axis_data, save_folder_path)



    dataset_results = total_dataset(count_list)

    output(baseline_text, comparison_collection, dataset_results, story_results)

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
    parser.add_argument("save_folder_name", type = str, help = "name of the folder to save the graphs")
    
    args = parser.parse_args()

    if not(args.load_nlp_tool_path.endswith(".json") and args.load_baseline_path.endswith(".json")):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect saving file type. Save file type is .json")
    try:
        load_baseline_file = open(args.load_baseline_path)
        load_baseline_file.close()
        load_nlp_tool_path = open(args.load_nlp_tool_path)
        load_nlp_tool_path.close()
        save_folder_path = "graphs\\" + args.save_folder_name
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
        return args.load_baseline_path, args.load_nlp_tool_path, save_folder_path  

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
    nlp_text, nlp_persona, nlp_entity, nlp_action  = nlp_tool_data

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

def compare (baseline, nlp):
    '''
    calculate the number of true/false positives and false negatives 

    Parameters:
    baseline (list): the elements being compared to 
    nlp (list): the elements comparing for accuracy 

    Returns:
    comparison_results (2D list): includes the elements identified as true/false positives and false negatives 
    '''

    true_positive = []
    false_positive = []

    for element in nlp:
        if element in baseline:
            true_positive.append(element)
            baseline.remove(element)
        else:
            false_positive.append(element)
    
    false_nagative = baseline

    comparison_results = [true_positive, false_positive, false_nagative]

    return comparison_results

def count_true_false_positives_negatives(comparison_results):
    '''
    count the number of true/false positives and false negatives 

    Parameters:
    comparison_results (2D list): includes the elements identified as true/false positives and false negatives

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

def individual_story(count_list):
    '''
    get all the info for plotting for each individual story

    Parameters:
    count_list (2D list): for each story, has the total count for true/false positives and false negative

    Returns:
    story_results (3D list): for each story, has the precision, recall and f-measure of the persona, action, entity    
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

def scatterplot(input_data, save_folder_path):
    '''
    runs the commands to plot the precision and recall of each story as a scatterplot

    Parameters:
    input_data (2D list): contains the data of precision and corresponding recall for each story
    save_folder_path (str): the path for saving the graphs

    '''

    story_precision_results, story_recall_results = input_data
    story_persona_precision, story_entity_precision, story_action_precision = story_precision_results
    story_persona_recall, story_entity_recall, story_action_recall = story_recall_results

    create_scattergraph(story_persona_precision, story_persona_recall, "m", "Linear Regression of Recall Vs. Precision for Persona", save_folder_path, "\\persona_recall_precision")
    create_scattergraph(story_entity_precision, story_entity_recall, "r", "Linear Regression of Recall Vs. Precision for Entity", save_folder_path, "\\entity_recall_precision")
    create_scattergraph(story_action_precision, story_action_recall, "b", "Linear Regression of Recall Vs. Precision for Action", save_folder_path, "\\action_recall_precision")

def create_scattergraph(precision_data, recall_data, graph_color, title, save_folder_path, save_name):
    '''
    creates and saves the bargraph

    Parameters:
    precision_data (list): data of the precision of each story in order 
    recall_Data (list): data of the recall of each story in order
    graph_color (str): the color of the plotting data
    title (str): the title of the graph 
    save_folder_path (str): the path to save the graphs
    save_name (str): name of the file for saving
    '''

    graph = sns.jointplot(x=tuple(precision_data), y=tuple(recall_data), kind="reg", xlim=(0,1), ylim=(0,1), color= graph_color, scatter_kws={"s": 40})
    graph.set_axis_labels('Precision', 'Recall', fontsize=14)
    graph.fig.suptitle(title, fontsize = 16)
    graph.figure.tight_layout() 
    
    graph.savefig(save_folder_path + save_name +".png")

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

def output(baseline_text, comparison_collection, dataset_results, story_results):
    '''
    output the results so that it is easy to read the results 

    Parameters:
    baseline_text (list): story text 
    comparison_collection (3D list): true/false positive and false negative of each story 
    precision (list): precision of persona, entity, action 
    recall (list): recall of persona, entity, action 
    f_measure (list): f_measure of persona, entity, action 
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

if __name__ == "__main__":
    main()