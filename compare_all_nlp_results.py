#This script will compare all the final results of the nlp with each other
import argparse
import matplotlib.pyplot as plt
from numpy import compare_chararrays
import pandas as pd
import seaborn as sns
import sys

def main():
    simple_path, fabian_path, visual_narrator_path, saving_path, comparison_type, number_dataset = command()
    simple_data = extract_data(simple_path, number_dataset)
    fabian_data = extract_data(fabian_path, number_dataset)
    visual_narrator_data = extract_data(visual_narrator_path, number_dataset)

    if comparison_type == "Strict Comparison":
        path = "dataset_names_list\\dataset_list_strict.txt"
    elif comparison_type == "Inclusion Comparison":
        path = "dataset_names_list\\dataset_list_inclusion.txt"
    else:
        path = "dataset_names_list\\dataset_list_relaxed.txt"

    with open (path, "r") as file:
        datasets_label = file.readlines()

    formatted_data = format_data(datasets_label, number_dataset, simple_data, fabian_data, visual_narrator_data)

    persona_precision, persona_recall, persona_f_measure,entity_precision, entity_recall, entity_f_measure, action_precision, action_recall, action_f_measure = formatted_data

    create_final_bargraph(persona_precision,persona_recall, persona_f_measure, "Persona " + comparison_type, saving_path + "_persona_nlp_compare.png")
    create_final_bargraph(entity_precision,entity_recall, entity_f_measure, "Entity " + comparison_type, saving_path + "_entity_nlp_compare.png")
    create_final_bargraph(action_precision,action_recall, action_f_measure, "Action " + comparison_type, saving_path + "_action_nlp_compare.png")

def command():
    '''
    Runs the command line inputs

    Returns:
    args.load_primary_path (str): Path to the primary data csv file to be loaded
    args.load_all_path (str): Path to the all data csv file to be loaded
    args.save_folder_name (str): name of the folder to be saved

    Raises:
        FileNotFoundError: raises excpetion
        FileExistsError: raises exception
        wrong file type: raises exception
        not same comparison mode of both loading files: raises excpetion
        wrong file order: raises exception
    '''
    parser = argparse.ArgumentParser(description = "This program is to convert jsonl files to human readiable files")
    parser.add_argument("load_simple_path", type = str, help = "path of simple csv file")
    parser.add_argument("load_fabian_path", type = str, help = "path of fabian csv file")
    parser.add_argument("load_visual_narrator_path", type = str, help = "path of visual narrator csv file")
    parser.add_argument("save_file_name", type = str, help = "name of file to save")
    parser.add_argument("number_of_datasets", type = int, help = "number of dataset un the csv file, Note: must be same amount for all three files")
    
    args = parser.parse_args()

    if not(args.load_simple_path.endswith(".csv")) or not(args.load_fabian_path.endswith(".csv")) or not(args.load_visual_narrator_path.endswith(".csv")):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect input file type. Save file type is .csv")

    if "strict" in args.load_simple_path and "strict" in args.load_fabian_path and "strict" in args.load_visual_narrator_path:
        comparison_type = "Strict Comparison"
        saving_name = "strict_" + args.save_file_name
    elif "inclusion" in args.load_simple_path and "inclusion" in args.load_fabian_path and "inclusion" in args.load_visual_narrator_path:
        comparison_type = 'Inclusion Comparison'
        saving_name = "inclusion_" + args.save_file_name
    elif "relaxed" in args.load_simple_path and "relaxed" in args.load_fabian_path and "relaxed" in args.load_visual_narrator_path:
        comparison_type = "Relaxed Comparison"
        saving_name = "relaxed_" + args.save_file_name
    else:
        sys.tracebacklimit = 0 
        raise Exception("Incompatible combination. All files must be evaluated by same comparison mode")

    try:
        load_file = open(args.load_simple_path)
        load_file.close()
        load_file = open(args.load_fabian_path)
        load_file.close()
        load_file = open(args.load_visual_narrator_path)
        load_file.close()
        save_file_path = "final_results\\comparing_all_nlp\\" + saving_name

    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    except FileExistsError:
        sys.tracebacklimit = 0
        print("Saving path already exists")
        raise
    else:
        return args.load_simple_path, args.load_fabian_path, args.load_visual_narrator_path, save_file_path, comparison_type, args.number_of_datasets

def extract_data (path, number_dataset):
    '''
    extract the data from the csv file 

    Parameters:
    path (str): path to the file to extract data
    number_dataset (int): number of datasets in the csv files

    Returns:
    data (2D list): persona, entity, action data of the precision, recall and f-measure of each dataset

    Raises:
    not enough data: raise exception
    '''

    extract = pd.read_csv(path) 

    persona_precision = extract["Persona Precision"]
    entity_precision = extract["Entity Precision"]
    action_precision = extract["Action Precision"]
    persona_recall = extract["Persona Recall"]
    entity_recall = extract["Entity Recall"]
    action_recall = extract["Action Recall"]
    persona_f_measure = extract["Persona F-Measure"]
    entity_f_measure = extract["Entity F-Measure"]
    action_f_measure = extract["Action F-Measure"]

    if len(persona_precision) != number_dataset:
        sys.tracebacklimit = 0
        raise Exception ("Invalid number of data. Expected number of rows is", number_dataset)

    data = [persona_precision, persona_recall, persona_f_measure,entity_precision, entity_recall, entity_f_measure, action_precision, action_recall, action_f_measure]

    return data

def format_data(datasets_label, number_dataset, simple_data, fabian_data, visual_narrator_data):
    '''
    formats the data so that it can be easily plotted onto the graphs

    Parameters:
    datasets_label (list): all the datsets that are in the csv files
    number_dataset (int): the number of datsets in the csv files
    simple_data(2D list): the final data results from simple nlp
    fabian_data(2D list): the final data results from fabian nlp
    visual_narrator_data(2D list): the final data results from visual narrator nlp

    Returns:
    formatted_data (list): contains the formatted data to plot for persona, entity, action's precision, recall, f_measure
    '''
    formatted_data = []

    for i in range(9):
        rounded_simple = round_data(simple_data[i].values.tolist())
        rounded_fabian = round_data(fabian_data[i].values.tolist())
        rounded_visual_narrator = round_data(visual_narrator_data[i].values.tolist())

        formatted_data.append(pd.DataFrame({ "Dataset": datasets_label + datasets_label + datasets_label,
                            "Data": rounded_simple + rounded_fabian + rounded_visual_narrator,
                            "nlp": ["simple"]*number_dataset + ["fabian"]*number_dataset + ["visual narrator"]*number_dataset}))

    return formatted_data

def round_data(data):
    '''
    will round each element in list to nearest 2 decimaal

    Parameters:
    data (list): elements to rounded

    Returns:
    rounded(list): rounded elements of data
    '''
    rounded = []

    for num in data:
        rounded.append(round(num, 2))

    return rounded

def create_final_bargraph(precision_results,recall_results, f_measure_results, title, save_path):
    
    graph, (precision_plot, recall_plot, f_measure_plot) = plt.subplots(3, 1, figsize=(20, 5), sharex=True)

    palette ={"simple": "y", "fabian": "c", "visual narrator": "b"}


    precision = sns.barplot(x= "Dataset", y= "Data", hue = "nlp",data = precision_results, ax = precision_plot, palette = palette, ci = None)
    precision.set(xlabel=None)
    precision.set(ylabel= "Precision")

    for i in precision.containers:
        precision.bar_label(i)

    recall = sns.barplot(x= "Dataset", y= "Data", hue = "nlp", data = recall_results, ax = recall_plot, palette = palette, ci = None)
    recall.set(xlabel=None)
    recall.set(ylabel= "Recall")

    for i in recall.containers:
        recall.bar_label(i)

    f_measure = sns.barplot(x= "Dataset", y= "Data", hue = "nlp", data = f_measure_results, ax = f_measure_plot, palette = palette, ci = None)
    f_measure_plot.set_xlabel("Dataset")
    f_measure.set(ylabel= "F-Measure")

    for i in f_measure.containers:
        f_measure.bar_label(i)


    precision_plot.set(ylim=(0, 1.2))
    recall_plot.set(ylim=(0, 1.2))
    f_measure_plot.set(ylim=(0, 1.2)) 
    
    graph.suptitle(title, fontsize = 16)

    precision.legend([],[], frameon=False)
    recall.legend([],[], frameon=False)
    f_measure.legend([],[], frameon=False)

    handles, labels = precision_plot.get_legend_handles_labels()
    graph.legend(handles=handles[:], labels=labels[:], title = "LEGEND", loc = "center right", bbox_to_anchor=(1, 0.5))

    graph.savefig(save_path)

if __name__ == "__main__":
    main()