#This script will get all the final comparision data and output final results 
import argparse
import csv
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import statistics
import sys


def main():
    primary_path, all_path, dataset_name_path, saving_path, comparison_type, number_dataset = command()
    primary_data = extract_data(primary_path, number_dataset)
    all_data = extract_data(all_path, number_dataset)

    primary_save_path = saving_path + "\\primary"
    all_save_path = saving_path + "\\all"
    os.mkdir(primary_save_path)
    os.mkdir(all_save_path)

    with open(dataset_name_path) as file:
        dataset_names = file.readlines()

    create_final_scatterplot(primary_path, "Persona Precision", "Persona Recall", "Recall Vs. Precision Persona " + comparison_type, "m", primary_save_path + "\\primary_persona_scatter.png")
    create_final_scatterplot(primary_path, "Entity Precision", "Entity Recall", "Recall Vs. Precision Entity " + comparison_type, "r", primary_save_path + "\\primary_entity_scatter.png")
    create_final_scatterplot(primary_path, "Action Precision", "Action Recall", "Recall Vs. Precision Action " + comparison_type, "b", primary_save_path + "\\primary_action_scatter.png")
    create_final_scatterplot(all_path, "Persona Precision", "Persona Recall", "Recall Vs. Precision Persona " + comparison_type, "m", all_save_path + "\\all_persona_scatter.png")
    create_final_scatterplot(all_path, "Entity Precision", "Entity Recall", "Recall Vs. Precision Entity " + comparison_type, "r", all_save_path + "\\all_entity_scatter.png")
    create_final_scatterplot(all_path, "Action Precision", "Action Recall", "Recall Vs. Precision Action " + comparison_type, "b", all_save_path + "\\all_action_scatter.png")

    create_final_bargraph(primary_path,"Persona Precision", "Persona Recall", "Persona F-Measure", "Persona " + comparison_type, primary_save_path + "\\primary_persona_bargraph.png", dataset_names)
    create_final_bargraph(primary_path,"Entity Precision", "Entity Recall", "Entity F-Measure", "Entity " + comparison_type, primary_save_path + "\\primary_entity_bargraph.png", dataset_names)
    create_final_bargraph(primary_path,"Action Precision", "Action Recall", "Action F-Measure", "Action " + comparison_type, primary_save_path + "\\primary_action_bargraph.png", dataset_names)
    create_final_bargraph(all_path,"Persona Precision", "Persona Recall", "Persona F-Measure", "Persona " + comparison_type, all_save_path + "\\all_persona_bargraph.png", dataset_names)
    create_final_bargraph(all_path,"Entity Precision", "Entity Recall", "Entity F-Measure", "Entity " + comparison_type, all_save_path + "\\all_entity_bargraph.png", dataset_names)
    create_final_bargraph(all_path,"Action Precision", "Action Recall", "Action F-Measure", "Action " + comparison_type, all_save_path + "\\all_action_bargraph.png", dataset_names)

    primary_average = calculate_average(primary_data)
    primary_standard_deviation = calculate_standard_deviation(primary_data)
    all_average = calculate_average(all_data)
    all_standard_deviation = calculate_standard_deviation(all_data)

    output_terminal(primary_average, primary_standard_deviation, all_average, all_standard_deviation)

    save_results(primary_average, primary_standard_deviation, primary_save_path + "\\primary_results.csv")
    save_results(all_average, all_standard_deviation, all_save_path + "\\all_results.csv")

    primary_csv_copy_saving_path = saving_path + "\\primary_results_copy.csv"
    all_csv_copy_saving_path = saving_path + "\\all_results_copy.csv"

    copy_and_clear(primary_path, primary_csv_copy_saving_path)
    copy_and_clear(all_path, all_csv_copy_saving_path)
def command():
    '''
    Runs the command line inputs

    Returns:
    args.load_primary_path (str): path of primary csv file
    args.load_all_path (str): path of all csv file
    args.load_dataset_names (str): path of the dataset names in a txt file
    args.save_folder_name (str): name of folder to save
    comparison_type (str): the type of comparison used for the data

    Raises:
        FileNotFoundError: raises excpetion
        FileExistsError: raises exception
        wrong file type: raises exception
        not same comparison mode of both loading files: raises excpetion
        wrong file order: raises exception
    '''

    parser = argparse.ArgumentParser(description = "This program is to visualize the final results of the nlp")
    parser.add_argument("load_primary_path", type = str, help = "path of primary csv file")
    parser.add_argument("load_all_path", type = str, help = "path of all csv file")
    parser.add_argument("load_dataset_names_path", type = str, help = "path of dataset's name in txt file")
    parser.add_argument("save_folder_name", type = str, help = "name of folder to save")
    
    args = parser.parse_args()

    if not(args.load_primary_path.endswith(".csv")) or not(args.load_all_path.endswith(".csv")):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect input file type. Save file type is .csv")

    if not(args.load_dataset_names_path.endswith("txt")):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect input file type. Save file type is .txt")

    if not("primary" in args.load_primary_path) or not("all" in args.load_all_path):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect file order. First file must be primary data and the second file must be all data")

    if "strict" in args.load_primary_path and "strict" in args.load_all_path:
        comparison_type = "Strict Comparison"
        saving_name = "strict_" + args.save_folder_name
    elif "inclusion" in args.load_primary_path and "inclusion" in args.load_all_path:
        comparison_type = 'Inclusion Comparison'
        saving_name = "inclusion_" + args.save_folder_name
    elif "relaxed" in args.load_primary_path and "relaxed" in args.load_all_path:
        comparison_type = "Relaxed Comparison"
        saving_name = "relaxed_" + args.save_folder_name
    else:
        sys.tracebacklimit = 0 
        raise Exception("Incompatible combination. Both files must be evaluated by same comparison mode")

    try:
        load_file = open(args.load_primary_path)
        load_file.close()
        load_file = open(args.load_all_path)
        load_file.close()
        load_file = open(args.load_dataset_names_path)
        load_file.close()
        save_folder_path = "final_results\\individual_nlp_results\\all_datasets_results\\" + saving_name
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
        with open(args.load_dataset_names_path, encoding = "utf-8") as file:
            data = file.readlines()
            number_dataset = len(data)

        return args.load_primary_path, args.load_all_path, args.load_dataset_names_path, save_folder_path, comparison_type, number_dataset
def extract_data (path, number_dataset):
    '''
    extract the data from the csv file 

    Parameters:
    path (str): path to the file to extract data
    number_dataset(int): number of datset results in the file

    Returns:
    data (3D list): persona, entity, action data of the precision, recall and f-measure of each dataset

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

def create_final_scatterplot(read_file, x_data, y_data, title, graph_color, save_path):
    '''
    Create and save the scatterplot of the data

    Parameters:
    read_file (str): the path of file to read data from 
    x_data (str): the coloumn header for x axis
    y_data (str): the coloumn header for y axis
    title (str): title for the graph
    graph_colour (str): colour for the plot of the data
    save_path (str): the path of file to save
    '''

    csv_data = pd.read_csv(read_file)

    graph = sns.jointplot(x = x_data, y = y_data, data = csv_data, kind = "scatter", color= graph_color, clip_on = False, xlim=(0, 1.1),ylim=(0, 1.1))
    graph.fig.suptitle(title, fontsize = 16)
    graph.figure.tight_layout() 
    
    graph.savefig(save_path)

def create_final_bargraph(read_file,precision_data, recall_data, f_measure_data, title, save_path, dataset_names):
    '''
    creates a bargraph based on the final results

    Parameters:
    read_file (str): the path of csv file with results
    precision_data (str): column name in csv file with the precision data
    recall_data (str): column name in csv file with the recall data
    f_measure_data (str): column name in csv file with the f-measure data
    title (str): the title for the graph
    save_path (str): the path to save the graph image
    dataset_names (list): the x label names for the datasets that corresponds to the data in the csv file
    '''
    
    graph, (precision_plot, recall_plot, f_measure_plot) = plt.subplots(3, 1, figsize=(10, 5), sharex=True)

    csv_data = pd.read_csv(read_file)
    x_label = dataset_names

    sns.barplot(x=x_label, y=precision_data, data = csv_data, ax= precision_plot, color= "m", ci = None)
    for p in precision_plot.patches:
        precision_plot.annotate(format(p.get_height(), '.3f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', size = 8, xytext = (0, 3), textcoords = 'offset points')

    sns.barplot(x=x_label, y=recall_data, data = csv_data, ax=recall_plot, color= "r",  ci = None)
    for p in recall_plot.patches:
        recall_plot.annotate(format(p.get_height(), '.3f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', size = 8, xytext = (0, 3), textcoords = 'offset points')

    sns.barplot(x=x_label, y=f_measure_data, data = csv_data, ax=f_measure_plot , color= "b", ci = None)
    for p in f_measure_plot.patches:
        f_measure_plot.annotate(format(p.get_height(), '.3f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', size = 8, xytext = (0, 3), textcoords = 'offset points')
    
    precision_plot.set(ylim=(0, 1.1))
    recall_plot.set(ylim=(0, 1.1))
    f_measure_plot.set(ylim=(0, 1.1)) 
    
    f_measure_plot.set_xlabel("Dataset")
    graph.suptitle(title, fontsize = 16)

    plt.tight_layout()

    graph.savefig(save_path)

def calculate_average(data):
    '''
    Calculate the average of the data

    Patameters:
    data (2D list): contains the data of the precision, recall, f-measure for persona, entity, action for each dataset

    Returns
    average (list): the mean of data of the precision, recall, f-measure for persona, entity, action 
    '''

    average = []

    for category in data:
        average.append(round(statistics.mean(category), 3))

    return average

def calculate_standard_deviation(data):
    '''
    Calculate the standard deviation of the data

    Patameters:
    data (2D list): contains the data of the precision, recall, f-measure for persona, entity, action for each dataset

    Returns
    standard_deviation (list): the mean of data of the precision, recall, f-measure for persona, entity, action 
    '''

    standard_deviation = []

    for category in data:
        standard_deviation.append(round(statistics.stdev(category),3))

    return standard_deviation

def output_terminal(primary_average, primary_standard_deviation, all_average, all_standard_deviation):
    '''
    output the results on the terminal 

    Parameters:
    primary_average (list): average of the primary data 
    primary_standard_deviation (list): standard deviation of the primary data
    all_average (list): average of the all data 
    all_standard_deviation (list): standard deviation of the all data
    '''

    header = ["Primary Average","All Average", "Primary Standard Deviation", "All Standard Deviation"]
    data = [primary_average, all_average, primary_standard_deviation, all_standard_deviation]

    for i in range(4):
        print (header[i])
        print("Persona Precision", data[i][0])
        print("Persona Recall", data[i][1])
        print("Persona F-Measure", data[i][2])
        print("Entity Precision", data[i][3])
        print("Entity Recall", data[i][4])
        print("Entity F-Measure", data[i][5])
        print("Action Precision", data[i][6])
        print("Action Recall", data[i][7])
        print("Action F-Measure", data[i][8])
        print("_______________________________________________________\n")
    
def save_results(average, standard_deviation, saving_path):
    '''
    save the results of the average and standard deviation to a csv file 

    Parameters:
    average (list): the average of each category in the data
    standard_deviation (list): the standard deviation of each category in the data 
    saving_path (str): the path of the file to save results
    '''

    label = ["Measurement", "Persona Precision", "Persona Recall", "Persona F-Measure","Entity Precision", "Entity Recall", "Entity F-Measure",\
            "Action Precision", "Action Recall", "Action F-Measure"]

    average.insert(0, "Average")
    standard_deviation.insert(0, "Standard Deviation")

    with open (saving_path, "a", newline = "") as file:
        writer = csv.writer(file)
        for i in range (10):
            row = label[i], average[i], standard_deviation[i]
            writer.writerow(row)

def copy_and_clear(clear_path, saving_path):
    '''
    Create of copy of the csv file and clear the old one for later use 

    Parameters:
    clear_path (str): path of the file to clear
    saving_path (str): path of saving file
    '''

    copy_data = []

    with open(clear_path, "r") as copy_file:
        reader = csv.reader(copy_file)
        for rows in reader:
            copy_data.append(rows)
    
    #overwrites original copy but keeps the title labels
    with open(clear_path, "w", newline = "") as clear_file:
        writer = csv.writer(clear_file)
        writer.writerow(copy_data[0])

    with open(saving_path, "w", newline = "") as save_file:
        writer = csv.writer(save_file)
        writer.writerows(copy_data)

if __name__ == "__main__":
    main()