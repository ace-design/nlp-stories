#This script will compare the average of the final results of each nlp tool 

import argparse
import matplotlib.pyplot as plt
import pandas as pd
import sys

def main():
    simple_path, fabian_path, visual_narrator_path, crf_path, saving_path, comparison_type, save_name = command()
    simple_data = extract_data(simple_path)
    fabian_data= extract_data(fabian_path)
    visual_narrator_data= extract_data(visual_narrator_path)

    precision_formatted_data, recall_formatted_data, f_measure_formatted_data  = format_data(simple_data, fabian_data, visual_narrator_data, crf_path)

    create_final_bargraph(precision_formatted_data, save_name.title() + " Precision Average " + comparison_type, saving_path + "_precison_compare_average.png", crf_path)
    create_final_bargraph(recall_formatted_data, save_name.title() + " Recall Average " + comparison_type, saving_path + "_recall_compare_average.png", crf_path)
    create_final_bargraph(f_measure_formatted_data, save_name.title() + " F-Measure Average " + comparison_type, saving_path + "_f_measure_compare_average.png", crf_path)


def command():
    '''
    Runs the command line inputs

    Returns:
    args.load_simple_path (str): Path to the simple data csv file to be loaded
    args.load_fabian_path (str): Path to the fabian data csv file to be loaded
    args.load_visual_narrator_path (str): Path to the visual narrator data csv file to be loaded
    args.load_crf_path (str): Path to the crf data csv file to be loaded, it is NONE if it is not given
    args.save_file_name (str): name of the file to be saved

    Raises:
    FileNotFoundError: raises excpetion
    wrong file type: raises exception
    not same comparison mode of both loading files: raises excpetion
    wrong file order: raises exception
    '''
    parser = argparse.ArgumentParser(description = "This program will output a visulation of the average final results")
    parser.add_argument("load_simple_path", type = str, help = "path of simple csv file")
    parser.add_argument("load_fabian_path", type = str, help = "path of fabian csv file")
    parser.add_argument("load_visual_narrator_path", type = str, help = "path of visual narrator csv file")
    parser.add_argument("--load_crf_path", nargs="?", type = str, help = "path of crf csv file")
    parser.add_argument("save_file_name", type = str, help = "name of file to save")

    args = parser.parse_args()

    if not(args.load_simple_path.endswith(".csv")) or not(args.load_fabian_path.endswith(".csv")) or not(args.load_visual_narrator_path.endswith(".csv")) or (args.load_crf_path != None and not(args.load_crf_path.endswith(".csv"))):
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
        if args.load_crf_path != None:
            load_file = open(args.load_crf_path)
            load_file.close()

        save_file_path = "final_results\\comparing_all_nlp_average\\" + saving_name

    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        return args.load_simple_path, args.load_fabian_path, args.load_visual_narrator_path, args.load_crf_path, save_file_path, comparison_type, args.save_file_name

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

def format_data(simple_data, fabian_data, visual_narrator_data, crf_path):
    '''
    formats the data so that it can be easily plotted onto the graphs

    Parameters:
    simple_data(2D list): the final data results from simple nlp
    fabian_data(2D list): the final data results from fabian nlp
    visual_narrator_data(2D list): the final data results from visual narrator nlp
    crf_path (str): path to csv file, it is NONE if it was not given at the command line

    Returns:
    formatted_data (list): contains the formatted data to plot for persona, entity, action's precision, recall, f_measure
    '''
    simple_average, simple_sd = simple_data
    fabian_average, fabian_sd = fabian_data
    visual_narrator_average, visual_narrator_sd = visual_narrator_data

    row_data = []

    if crf_path == None:
        for i in range(9):
            row_data.append([simple_average[i], fabian_average[i], visual_narrator_average[i], simple_sd[i], fabian_sd[i], visual_narrator_sd[i]])

        persona_data = pd.DataFrame([row_data[0],row_data[3],row_data[6]] , columns= ["Simple Average", "Fabian Average","VN Average", "Simple SD","Fabian SD","VN SD"], index= ["Persona Precision", "Entity Precision", "Action Precision"])
        entity_data = pd.DataFrame([row_data[1],row_data[4],row_data[7]] , columns= ["Simple Average", "Fabian Average","VN Average", "Simple SD","Fabian SD","VN SD"], index= ["Persona Recall", "Entity Recall", "Action Recall"])
        action_data = pd.DataFrame([row_data[2],row_data[5],row_data[8]] , columns= ["Simple Average", "Fabian Average","VN Average", "Simple SD","Fabian SD","VN SD"], index= ["Persona F-Measure", "Entity F-Measure", "Action F-Measure"])
    else:
        crf_data = extract_data(crf_path)
        crf_average, crf_sd = crf_data

        for i in range(9):
            row_data.append([simple_average[i], fabian_average[i], visual_narrator_average[i], crf_average[i], simple_sd[i], fabian_sd[i], visual_narrator_sd[i], crf_sd[i]])

        persona_data = pd.DataFrame([row_data[0],row_data[3],row_data[6]] , columns= ["Simple Average", "Fabian Average", "VN Average", "CRF Average", "Simple SD","Fabian SD","VN SD", "CRF SD"], index= ["Persona Precision", "Entity Precision", "Action Precision"])
        entity_data = pd.DataFrame([row_data[1],row_data[4],row_data[7]] , columns= ["Simple Average", "Fabian Average", "VN Average", "CRF Average", "Simple SD","Fabian SD","VN SD", "CRF SD"], index= ["Persona Recall", "Entity Recall", "Action Recall"])
        action_data = pd.DataFrame([row_data[2],row_data[5],row_data[8]] , columns= ["Simple Average", "Fabian Average", "VN Average", "CRF Average", "Simple SD","Fabian SD","VN SD", "CRF SD"], index= ["Persona F-Measure", "Entity F-Measure", "Action F-Measure"])

    return persona_data, entity_data, action_data

def create_final_bargraph(data, title, saving_path, crf_path):

    if crf_path == None:
        yerr = data[["Simple SD","Fabian SD","VN SD"]].to_numpy().T
        data[["Simple Average", "Fabian Average","VN Average"]].plot(kind='bar', yerr=yerr, alpha=0.5, error_kw=dict(ecolor='k'), figsize=(17,7))
    else:
        yerr = data[["Simple SD","Fabian SD","VN SD", "CRF SD"]].to_numpy().T
        data[["Simple Average", "Fabian Average","VN Average", "CRF Average"]].plot(kind='bar', yerr=yerr, alpha=0.5, error_kw=dict(ecolor='k'), figsize=(17,7))
    
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