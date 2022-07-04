#This script will compare the average of the final results of each nlp tool 

import argparse
from calendar import c
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys

def main():
    simple_path, fabian_path, visual_narrator_path, saving_path, comparison_type = command()
    simple_data = extract_data(simple_path)
    fabian_data = extract_data(fabian_path)
    visual_narrator_data = extract_data(visual_narrator_path)

    measurement = ["Persona Precision", "Persona Recall", "Persona F-Measure", "Entity Precision", "Entity Recall", "Entity F-Measure","Action Precision", "Action Recall", "Action F-Measure"]

    formatted_data = format_data(simple_data, fabian_data, visual_narrator_data, measurement)

    create_final_bargraph(formatted_data, "Final Average " + comparison_type, saving_path + "_compare_average.png", simple_data, fabian_data, visual_narrator_data)

def command():
    '''
    Runs the command line inputs

    Returns:
    args.load_simple_path (str): Path to the simple data csv file to be loaded
    args.load_fabian_path (str): Path to the fabian data csv file to be loaded
    args.load_visual_narrator_path (str): Path to the visual narrator data csv file to be loaded
    args.save_file_name (str): name of the file to be saved

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

    if not("simple" in args.load_simple_path) or not("fabian" in args.load_fabian_path) or not("visual_narrator" in args.load_visual_narrator_path):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect order of input file. First file is simple, then Fabian, and then visual narrator")

    try:
        load_file = open(args.load_simple_path)
        load_file.close()
        load_file = open(args.load_fabian_path)
        load_file.close()
        load_file = open(args.load_visual_narrator_path)
        load_file.close()
        save_file_path = "final_results\\comparing_all_nlp_average\\" + saving_name

    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    except FileExistsError:
        sys.tracebacklimit = 0
        print("Saving path already exists")
        raise
    else:
        return args.load_simple_path, args.load_fabian_path, args.load_visual_narrator_path, save_file_path, comparison_type

def extract_data (path):
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

    data = [average, standard_deviation]

    return data

def format_data(simple_data, fabian_data, visual_narrator_data, measurement):
    '''
    formats the data so that it can be easily plotted onto the graphs

    Parameters:
    simple_data(2D list): the final data results from simple nlp
    fabian_data(2D list): the final data results from fabian nlp
    visual_narrator_data(2D list): the final data results from visual narrator nlp
    measurement (list): x label of graph (corresponds to the data above)

    Returns:
    formatted_data (list): contains the formatted data to plot for persona, entity, action's precision, recall, f_measure
    '''
    number_measurement = 9

    rounded_simple_average = round_data(simple_data[0].values.tolist())
    rounded_fabian_average = round_data(fabian_data[0].values.tolist())
    rounded_visual_narrator_average = round_data(visual_narrator_data[0].values.tolist())

    formatted_data = pd.DataFrame({ "Measurement": measurement*3, "Average": rounded_simple_average + rounded_fabian_average + rounded_visual_narrator_average,
                            "Standard Deviation": simple_data[1].values.tolist() + fabian_data[1].values.tolist() + visual_narrator_data [1].values.tolist(),
                            "nlp": ["simple"]*number_measurement + ["fabian"]*number_measurement + ["visual narrator"]*number_measurement})

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

def create_final_bargraph(formatted_data, title, save_path, a, b, c):

    palette ={"simple": "y", "fabian": "c", "visual narrator": "b"}

    sns.set(rc = {'figure.figsize':(17,8)})
    
    
    bargraph = sns.barplot(x= "Measurement", y= "Average", hue = "nlp",data = formatted_data, palette = palette)
    bargraph.set(xlabel= "Measurement Calculation")
    bargraph.set(ylabel= "Average Score")

    for i in bargraph.containers:
        bargraph.bar_label(i)

    bargraph.set(ylim=(0, 1.1))

    bargraph.set_title(title, fontsize = 16)
    bargraph.legend(bbox_to_anchor=(1.12, 0.5), borderaxespad=0)

    bargraph.figure.savefig(save_path)

if __name__ == "__main__":
    main()