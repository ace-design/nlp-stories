#This script will compare the average of the final results of each nlp tool 

import argparse
import matplotlib.pyplot as plt
import pandas as pd
import sys

def main():
    simple_path, fabian_path, visual_narrator_path, saving_path, comparison_type = command()
    simple_data = extract_data(simple_path)
    fabian_data= extract_data(fabian_path)
    visual_narrator_data= extract_data(visual_narrator_path)

    persona_formatted_data, entity_formatted_data, action_formatted_data  = format_data(simple_data, fabian_data, visual_narrator_data)

    create_final_bargraph(persona_formatted_data, "Final Persona Average " + comparison_type, saving_path + "_persona_compare_average.png")
    create_final_bargraph(entity_formatted_data, "Final Entity Average " + comparison_type, saving_path + "_entity_compare_average.png")
    create_final_bargraph(action_formatted_data, "Final Action Average " + comparison_type, saving_path + "_action_compare_average.png")


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
    parser = argparse.ArgumentParser(description = "This program will output a visulation of the average final results")
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

    data = [average, standard_deviation]

    return data

def format_data(simple_data, fabian_data, visual_narrator_data):
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
    simple_average, simple_sd = simple_data
    fabian_average, fabian_sd = fabian_data
    visual_narrator_average, visual_narrator_sd = visual_narrator_data

    row_data = []

    for i in range(9):
        row_data.append([simple_average[i], fabian_average[i], visual_narrator_average[i], simple_sd[i], fabian_sd[i], visual_narrator_sd[i]])

    persona_data = pd.DataFrame([row_data[0],row_data[1],row_data[2]] , columns= ["Simple Average", "Fabian Average","VN Average", "Simple SD","Fabian SD","VN SD"], index= ["Persona Precision", "Persona Recall", "Persona F-Measure"])
    entity_data = pd.DataFrame([row_data[3],row_data[4],row_data[5]] , columns= ["Simple Average", "Fabian Average","VN Average", "Simple SD","Fabian SD","VN SD"], index= ["Entity Precision", "Entity Recall", "Entity F-Measure"])
    action_data = pd.DataFrame([row_data[6],row_data[7],row_data[8]] , columns= ["Simple Average", "Fabian Average","VN Average", "Simple SD","Fabian SD","VN SD"], index= ["Action Precision", "Action Recall", "Action F-Measure"])

    return persona_data, entity_data, action_data

def create_final_bargraph(data, title, saving_path):
    yerr = data[["Simple SD","Fabian SD","VN SD"]].to_numpy().T

    data[["Simple Average", "Fabian Average","VN Average"]].plot(kind='bar', yerr=yerr, alpha=0.5, error_kw=dict(ecolor='k'), figsize=(17,7))
    plt.title(title,fontsize= 20)
    plt.ylabel("Average Score",fontsize=14)
    plt.xlabel("Measurement Type", fontsize=14)
    plt.ylim([0, 1.1])
    plt.legend(loc=(1.005,0.5))
    plt.xticks(rotation = 0)
    plt.tight_layout()
    plt.savefig(saving_path)

if __name__ == "__main__":
    main()