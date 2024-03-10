#This script will compare the average of the final results of each nlp tool 

import argparse
import matplotlib.pyplot as plt
import pandas as pd
import sys

def main():
    nlp_paths, nlps, saving_path, comparison_type, title_name = command()

    nlp_data = []
    for nlp_path in nlp_paths:
        data = extract_data(nlp_path)
        nlp_data.append(data)

    precision_formatted_data, recall_formatted_data, f_measure_formatted_data  = format_data(nlp_data, nlps)

    create_final_bargraph(nlps, precision_formatted_data, "Precision Average" + title_name + " " + comparison_type, saving_path + "_precison_compare_average.png")
    create_final_bargraph(nlps, recall_formatted_data, "Recall Average" + title_name + " " + comparison_type, saving_path + "_recall_compare_average.png")
    create_final_bargraph(nlps, f_measure_formatted_data, "F-Measure Average" + title_name + " " + comparison_type, saving_path + "_f_measure_compare_average.png")

    print("Graphs are saved")

def command():
    '''
    Runs the command line inputs

    Returns:
    args.load_visual_narrator_path (str): Path to the visual narrator data csv file to be loaded
    args.load_chatgpt_path (str): Path to the ChatGPT data csv file to be loaded
    args.load_crf_path (str): Path to the crf data csv file to be loaded, it is NONE if it is not given
    args.evalationType (str): Type of data scope used 

    Raises:
    FileNotFoundError: raises excpetion
    wrong file type: raises exception
    not same comparison mode of both loading files: raises excpetion
    wrong file order: raises exception
    '''
    parser = argparse.ArgumentParser(description = "This program will output a visulation of the average final results")
    parser.add_argument("--load_gpt_3_5_v0125_path", type = str, help = "path of GPT-3.5 V0125 csv file")
    parser.add_argument("--load_gpt_3_5_v0613_2023_path", type = str, help = "path of GPT-3.5 V0613 2023 csv file")
    parser.add_argument("--load_gpt_3_5_v0613_2024_path", type = str, help = "path of GPT-3.5 V0613 2024 csv file")
    parser.add_argument("--load_gpt_4_turbo_v0125_path", type = str, help = "path of GPT-4 Turbo V0125 csv file") 
    parser.add_argument("--load_gpt_4_v0613_path", type = str, help = "path of GPT-4 Turbo V0613 csv file") 
    parser.add_argument("--load_visual_narrator_path", type = str, help = "path of visual narrator csv file")
    parser.add_argument("--load_crf_path", nargs="?", type = str, help = "path of crf csv file")
    parser.add_argument("evalationType", type = str, choices=["all", "primary"], help = "type of data scope used [all, primary]")
    parser.add_argument("data_type", type = str, choices=["BKLG", "CAT", "GLO"], help = "evaluation by individual backlogs - BKLG, categorized backlogs - CAT, or global - GLO")

    args = parser.parse_args()

    paths = [args.load_gpt_3_5_v0125_path, args.load_gpt_3_5_v0613_2023_path, args.load_gpt_3_5_v0613_2024_path, args.load_gpt_4_turbo_v0125_path, 
            args.load_gpt_4_v0613_path, args.load_visual_narrator_path, args.load_crf_path]
    nlpList = ["GPT-3.5 Turbo v0125", "GPT-3.5 v0613 2023", "GPT-3.5 v0613 2024", "GPT-4 Turbo v0125", "GPT-4 Turbo v0613", "Visual Narrator", "CRF"]
    
    # Remove nlp paths that are not specfied
    nlp_paths = []
    nlps = []
    for i in range(len(paths)):
        path = paths[i]
        nlp = nlpList[i]

        if path != None:
            if not(path.endswith(".csv")):
                sys.tracebacklimit = 0
                raise Exception ("Incorrect input file type. File type is .csv")
            nlp_paths.append(path)
            nlps.append(nlp)

    # Find the comparison type
    comparisons = ["strict", "inclusion", "relaxed"]
    comparison_type = ""

    for comparison in comparisons:
        validComparison = True
        for path in nlp_paths:
            if not(comparison in path):
                validComparison = False
                break
        
        if validComparison:
            comparison_type = comparison.title() + " Comparison"
            saving_name = comparison + "_" + args.evalationType
            break

    if comparison_type == "":
        sys.tracebacklimit = 0 
        raise Exception("Incompatible combination. All files must be evaluated by same comparison mode")

    try:
        for path in nlp_paths:
            load_file = open(path)
            load_file.close()

        if args.load_crf_path != None:
            crf_path = "benchmark_with_crf\\"
        else:
            crf_path = "benchmark_without_crf\\"

        if args.data_type == "BKLG":
            data_type_folder = "individual_backlog"
        elif args.data_type == "CAT":
            data_type_folder = "categories"
        else:
            data_type_folder = "global"

        save_file_path = "final_results\\comparing_nlps_results\\average_results\\" + crf_path + data_type_folder + "\\" + comparison_type.lower().replace(" ", "_") + "\\" + saving_name

        if args.evalationType != "primary":
            title = ""
        else:
            title = " Primary Results"

    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        return  nlp_paths, nlps, save_file_path, comparison_type, title

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

def format_data(nlp_data, nlps):
    '''
    formats the data so that it can be easily plotted onto the graphs

    Parameters:
    data(3D list): the final data results for each nlp

    Returns:
    formatted_data (list): contains the formatted data to plot for persona, entity, action's precision, recall, f_measure
    '''

    table = []
    for i in range(9):
        nlps_average = []
        nlps_sd = []

        for data in nlp_data:
            average, sd = data

            nlps_average.append(float(average[i]))
            nlps_sd.append(float(sd[i]))

        row = nlps_average + nlps_sd
        table.append(row)

    
    precision_label = ["Persona Precision", "Entity Precision", "Action Precision"]
    recall_label = ["Persona Recall", "Entity Recall", "Action Recall"]
    f_measure_label = ["Persona F-Measure", "Entity F-Measure", "Action F-Measure"]

    averageLabel = []
    sdLabel = []
    for nlp in nlps:
        averageLabel.append(nlp)
        sdLabel.append(nlp + " SD")

    columnLabel = averageLabel + sdLabel

    precision_data = pd.DataFrame([table[0],table[3],table[6]] , columns= columnLabel, index= precision_label)
    recall_data = pd.DataFrame([table[1],table[4],table[7]] , columns= columnLabel, index= recall_label)
    f_measure_data = pd.DataFrame([table[2],table[5],table[8]] , columns= columnLabel, index= f_measure_label)

    return precision_data, recall_data, f_measure_data

def create_final_bargraph(nlps, data, title, saving_path):

    sd_label = []
    colors = []
    for i in range(len(nlps)):
        sd_label.append(nlps[i] + " SD")
        colors.append(plt.cm.Pastel1(i))

    yerr = fix_max_y_error(data[sd_label], data[nlps])
    data[nlps].plot(kind='bar', yerr=yerr, error_kw=dict(lw = 3, capthick = 2, capsize = 7, ecolor='k'), figsize=(15,7), color = colors)
    
    plt.title(title,fontsize= 20)
    plt.ylabel("Average Score",fontsize=14)
    plt.xlabel("Measurement Type", fontsize=14)
    plt.ylim([0, 1])
    plt.legend(loc=(1.005,0.5))
    plt.xticks(rotation = 0)
    plt.tight_layout()
    plt.savefig(saving_path)
    plt.savefig(saving_path.replace(".png", ".pdf"))

def fix_max_y_error(standard_deviation, y_data):
    '''
    will check if the yerror will go above 1 and if yes, it will make the limit as 1 

    Parameters:
    standard_deviation: standard deviation of the data for the graph
    y_data: the y_data for the graph to plot
    '''

    standard_deviation_list = standard_deviation.to_numpy().T
    y_data_list = y_data.to_numpy().T

    for i in range(len(y_data_list)):
        for j in range(len(y_data_list[i])):
            if standard_deviation_list[i][j] + y_data_list[i][j] > 1:
                standard_deviation_list[i][j] = 1 - y_data_list[i][j]

    return standard_deviation_list

if __name__ == "__main__":
    main()