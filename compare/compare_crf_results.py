#This script will compare the results of the different crf groupings

import argparse
import matplotlib.pyplot as plt
import pandas as pd
import sys

def main():
    individual_backlog_path, category_path, global_path, save_name, title= command()
    individual_backlog_data = extract_data(individual_backlog_path)
    category_data = extract_data(category_path)
    global_data = extract_data(global_path)

    strict_data, inclusion_formatted_data, relaxed_formatted_data  = format_data(individual_backlog_data, category_data, global_data)

    create_final_bargraph(strict_data, inclusion_formatted_data, relaxed_formatted_data, title, save_name)
    
    print("Graph is saved")

def command():
    '''
    Runs the command line inputs

    Returns:
    args.load_individual_backlog_path (str): Path to the individual backlog crf data csv file to be loaded
    args.load_category_path (str): Path to the category crf data csv file to be loaded
    args.load_global_path (str): Path to the global crf data csv file to be loaded
    args.save_file_name (str): name of the file to be saved
    args.title(str): the title of the graph

    Raises:
    FileNotFoundError: raises excpetion
    wrong file type: raises exception
    not same comparison mode of both loading files: raises excpetion
    wrong file order: raises exception
    '''
    parser = argparse.ArgumentParser(description = "This program will output a visulation of the results of differnt grouping of crf. NOTE: order within csv file must be strict, inclusion and then relaxed")
    parser.add_argument("load_individual_backlog_path", type = str, help = "path of individual backlog crf csv file")
    parser.add_argument("load_category_path", type = str, help = "path of category crf csv file")
    parser.add_argument("load_global_path", type = str, help = "path of global crf csv file")
    parser.add_argument("save_file_name", type = str, help = "name of file to save")
    parser.add_argument("title", type = str, help = "title of graph")

    args = parser.parse_args()

    if not(args.load_individual_backlog_path.endswith(".csv")) or not(args.load_category_path.endswith(".csv")) or not(args.load_global_path.endswith(".csv")):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect input file type. Save file type is .csv")

    try:
        load_file = open(args.load_individual_backlog_path)
        load_file.close()
        load_file = open(args.load_category_path)
        load_file.close()
        load_file = open(args.load_global_path)
        load_file.close()

    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        return args.load_individual_backlog_path, args.load_category_path, args.load_global_path, args.save_file_name, args.title

def extract_data(path):
    '''
    extract the data from the csv file 

    Parameters:
    path (str): path to the file to extract data

    Returns:
    data (2D list): the average and standard deviation of the precision, recall, f-measure of persona, entity and action of all the final results
    '''

    extract = pd.read_csv(path) 

    average = extract["Average"]
    standard_deviation = extract["Standard Deviation"]
    label = extract["Comparison Mode"]

    data = [average, standard_deviation, label]

    return data

def format_data(backlog_data, category_data, global_data):
    '''
    formats the data so that it can be easily plotted onto the graphs

    Parameters:
    backlog_data(2D list): the final data results from simple nlp
    category_data(2D list): the final data results from ecmfa_vn nlp
    global_data(2D list): the final data results from visual narrator nlp
    crf_path (str): path to csv file, it is NONE if it was not given at the command line

    Returns:
    strict_data (list): contains the formatted data to plot for strict data
    inclusion_data (list): contains the formatted data to plot for inclusion data
    relaxed_data (list): contains the formatted data to plot for relaxed data
    '''
    backlog_average, backlog_sd, backlog_label = backlog_data
    category_average, category_sd, category_label = category_data
    global_average, global_sd, global_label = global_data

    row_data = []

    for i in range(27):
        row_data.append([backlog_average[i], category_average[i], global_average[i], backlog_sd[i], category_sd[i], global_sd[i]])

    for i in range (0,27,9):
        if backlog_label[i] == "Strict Comparison" and category_label[i] == "Strict Comparison" and global_label[i] == "Strict Comparison":
            strict_data = pd.DataFrame([row_data[i+2],row_data[i+5],row_data[i+8]] , columns= ["Individual Backlog", "Categories","Global", "individual backlog SD","categories SD","global SD"], index= ["Persona F-Measure", "Entity F-Measure", "Action F-Measure"])
        elif backlog_label[i] == "Inclusion Comparison" and category_label[i] == "Inclusion Comparison" and global_label[i] == "Inclusion Comparison":
            inclusion_data = pd.DataFrame([row_data[i+2],row_data[i+5],row_data[i+8]] , columns= ["Individual Backlog", "Categories","Global", "individual backlog SD","categories SD","global SD"], index= ["Persona F-Measure", "Entity F-Measure", "Action F-Measure"])
        elif backlog_label[i] == "Relaxed Comparison" and category_label[i] == "Relaxed Comparison" and global_label[i] == "Relaxed Comparison":
            relaxed_data = pd.DataFrame([row_data[i+2],row_data[i+5],row_data[i+8]] , columns= ["Individual Backlog", "Categories","Global", "individual backlog SD","categories SD","global SD"], index= ["Persona F-Measure", "Entity F-Measure", "Action F-Measure"])
        else:
            sys.tracebacklimit = 0
            raise Exception ("Invalid data matching across files. Ensure that the comparison mode matches across each file")

    return strict_data, inclusion_data, relaxed_data

def create_final_bargraph(strict_data, inclusion_data, relaxed_data, title, save_name):
    
    graph, (left, middle, right) = plt.subplots(1, 3, figsize=(10, 5))

    strict_yerr = find_max_y_error(strict_data[["individual backlog SD","categories SD","global SD"]], strict_data[["Individual Backlog", "Categories","Global"]])
    strict_data[["Individual Backlog", "Categories","Global"]].plot(ax = left, kind='bar', alpha = 0.85, yerr = strict_yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 5, ecolor='k'), figsize=(17,7), color = ["#f29e8e", "indianred", "#9a0200"])
    left.set_title("Strict Comparison", fontsize = 20)
    left.set_ylabel("F-Measure", fontsize = 25)
    left.set_xticklabels(["Persona", "Entity", "Action"], fontsize = 16)
    left.tick_params(labelrotation = 0)
    left.get_legend().remove()
    left.set_ylim([0, 1])

    inclusion_yerr = find_max_y_error(inclusion_data[["individual backlog SD","categories SD","global SD"]], inclusion_data[["Individual Backlog", "Categories","Global"]])
    inclusion_data[["Individual Backlog", "Categories","Global"]].plot(ax = middle, kind='bar', alpha = 0.85, yerr = inclusion_yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 5, ecolor='k'), figsize=(17,7), color = ["#f29e8e", "indianred", "#9a0200"])
    middle.set_title("Inclusion Comparison", fontsize = 20)
    middle.tick_params(labelrotation = 0)
    middle.set_xticklabels(["Persona", "Entity", "Action"], fontsize = 16)
    middle.get_legend().remove() 
    middle.set_ylim([0, 1])

    relaxed_yerr = find_max_y_error(relaxed_data[["individual backlog SD","categories SD","global SD"]], relaxed_data[["Individual Backlog", "Categories","Global"]])
    relaxed_data[["Individual Backlog", "Categories","Global"]].plot(ax = right, kind='bar', alpha = 0.85, yerr = relaxed_yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 5, ecolor='k'), figsize=(17,7), color = ["#f29e8e", "indianred", "#9a0200"])
    right.set_title("Relaxed Comparison", fontsize = 20)
    right.tick_params(labelrotation = 0)
    right.set_xticklabels(["Persona", "Entity", "Action"], fontsize = 16)
    right.get_legend().remove()
    right.set_ylim([0, 1])
    

    graph.suptitle(title, fontsize = 35)
    graph.supxlabel("Label Type", fontsize=25)
    plt.legend(loc=(1.025,0.5))

    plt.tight_layout()

    saving_path = "final_results\\comparing_nlps_results\\average_results\\comparing_crf\\" + save_name + ".png"

    plt.savefig(saving_path)

def find_max_y_error(standard_deviation, y_data):
    '''
    will check if the yerror will go above 1 and if yes, it will make the limit as 1 

    Parameters:
    standard_deviation: standard deviation of the data for the graph
    y_data: the y_data for the graph to plot
    '''

    standard_deviation_list = standard_deviation.to_numpy().T
    y_data_list = y_data.to_numpy().T

    for i in range(3):
        for j in range(len(y_data_list[i])):
            if standard_deviation_list[i][j] + y_data_list[i][j] > 1:
                standard_deviation_list[i][j] = 1 - y_data_list[i][j]

    return standard_deviation_list

if __name__ == "__main__":
    main()