#This script will compare the average of the final results of each nlp tool 

import argparse
import matplotlib.pyplot as plt
import pandas as pd
import sys

def main():
    simple_path, ecmfa_vn_path, visual_narrator_path, chatgpt_path, crf_path, saving_path, comparison_type, title_name = command()
    simple_data = extract_data(simple_path)
    ecmfa_vn_data= extract_data(ecmfa_vn_path)
    visual_narrator_data= extract_data(visual_narrator_path)
    chatgpt_data= extract_data(chatgpt_path)

    precision_formatted_data, recall_formatted_data, f_measure_formatted_data  = format_data(simple_data, ecmfa_vn_data, visual_narrator_data, chatgpt_data, crf_path)

    create_final_bargraph(precision_formatted_data, "Precision Average" + title_name + " " + comparison_type, saving_path + "_precison_compare_average.png", crf_path)
    create_final_bargraph(recall_formatted_data, "Recall Average" + title_name + " " + comparison_type, saving_path + "_recall_compare_average.png", crf_path)
    create_final_bargraph(f_measure_formatted_data, "F-Measure Average" + title_name + " " + comparison_type, saving_path + "_f_measure_compare_average.png", crf_path)

    print("Graphs are saved")

def command():
    '''
    Runs the command line inputs

    Returns:
    args.load_simple_path (str): Path to the simple data csv file to be loaded
    args.load_ecmfa_vn_path (str): Path to the ecmfa_vn data csv file to be loaded
    args.load_visual_narrator_path (str): Path to the visual narrator data csv file to be loaded
    args.load_chatgpt_path (str): Path to the ChatGPT data csv file to be loaded
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
    parser.add_argument("load_ecmfa_vn_path", type = str, help = "path of ecmfa_vn csv file")
    parser.add_argument("load_visual_narrator_path", type = str, help = "path of visual narrator csv file")
    parser.add_argument("load_chatgpt_path", type = str, help = "path of ChatGPT csv file")
    parser.add_argument("--load_crf_path", nargs="?", type = str, help = "path of crf csv file")
    parser.add_argument("save_file_name", type = str, help = "name of file to save")
    parser.add_argument("data_type", type = str, choices=["BKLG", "CAT", "GLO"], help = "evaluation by individual backlogs - BKLG, categorized backlogs - CAT, or global - GLO")

    args = parser.parse_args()

    if not(args.load_simple_path.endswith(".csv")) or not(args.load_ecmfa_vn_path.endswith(".csv")) or not(args.load_visual_narrator_path.endswith(".csv")) or not(args.load_chatgpt_path.endswith(".csv")) or (args.load_crf_path != None and not(args.load_crf_path.endswith(".csv"))):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect input file type. Save file type is .csv")

    if "strict" in args.load_simple_path and "strict" in args.load_ecmfa_vn_path and "strict" in args.load_visual_narrator_path and "strict" in args.load_chatgpt_path:
        comparison_type = "Strict Comparison"
        saving_name = "strict_" + args.save_file_name
    elif "inclusion" in args.load_simple_path and "inclusion" in args.load_ecmfa_vn_path and "inclusion" in args.load_visual_narrator_path and "inclusion" in args.load_chatgpt_path:
        comparison_type = 'Inclusion Comparison'
        saving_name = "inclusion_" + args.save_file_name
    elif "relaxed" in args.load_simple_path and "relaxed" in args.load_ecmfa_vn_path and "relaxed" in args.load_visual_narrator_path and "relaxed" in args.load_chatgpt_path:
        comparison_type = "Relaxed Comparison"
        saving_name = "relaxed_" + args.save_file_name
    else:
        sys.tracebacklimit = 0 
        raise Exception("Incompatible combination. All files must be evaluated by same comparison mode")

    if not("simple" in args.load_simple_path) or not("ecmfa_vn" in args.load_ecmfa_vn_path) or not("visual_narrator" in args.load_visual_narrator_path) or not("chatgpt" in args.load_visual_narrator_path):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect order of input file. First file is simple, then ecmfa_vn, and then visual narrator")

    try:
        load_file = open(args.load_simple_path)
        load_file.close()
        load_file = open(args.load_ecmfa_vn_path)
        load_file.close()
        load_file = open(args.load_visual_narrator_path)
        load_file.close()
        load_file = open(args.load_chatgpt_path)
        load_file.close()
        if args.load_crf_path != None:
            load_file = open(args.load_crf_path)
            load_file.close()
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

        if args.save_file_name != "primary":
            title = ""
        else:
            title = " Primary Results"

    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        return args.load_simple_path, args.load_ecmfa_vn_path, args.load_visual_narrator_path, args.load_chatgpt_path, args.load_crf_path, save_file_path, comparison_type, title

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

def format_data(simple_data, ecmfa_vn_data, visual_narrator_data, chatgpt_data, crf_path):
    '''
    formats the data so that it can be easily plotted onto the graphs

    Parameters:
    simple_data(2D list): the final data results from simple nlp
    ecmfa_vn_data(2D list): the final data results from ecmfa_vn nlp
    visual_narrator_data(2D list): the final data results from visual narrator nlp
    crf_path (str): path to csv file, it is NONE if it was not given at the command line

    Returns:
    formatted_data (list): contains the formatted data to plot for persona, entity, action's precision, recall, f_measure
    '''
    simple_average, simple_sd = simple_data
    ecmfa_vn_average, ecmfa_vn_sd = ecmfa_vn_data
    visual_narrator_average, visual_narrator_sd = visual_narrator_data
    chatgpt_average, chatgpt_sd = chatgpt_data

    row_data = []

    if crf_path == None:
        for i in range(9):
            row_data.append([simple_average[i], ecmfa_vn_average[i], visual_narrator_average[i], chatgpt_average[i], simple_sd[i], ecmfa_vn_sd[i], visual_narrator_sd[i], chatgpt_sd[i]])

        precision_data = pd.DataFrame([row_data[0],row_data[3],row_data[6]] , columns= ["Simple nlp", "ECMFA-VN","Visual Narrator", "ChatGPT", "Simple SD","ecmfa-vn SD","VN SD", "ChatGPT SD"], index= ["Persona Precision", "Entity Precision", "Action Precision"])
        recall_data = pd.DataFrame([row_data[1],row_data[4],row_data[7]] , columns= ["Simple nlp", "ECMFA-VN","Visual Narrator", "ChatGPT", "Simple SD","ecmfa-vn SD","VN SD", "ChatGPT SD"], index= ["Persona Recall", "Entity Recall", "Action Recall"])
        f_measure_data = pd.DataFrame([row_data[2],row_data[5],row_data[8]] , columns= ["Simple nlp", "ECMFA-VN","Visual Narrator", "ChatGPT", "Simple SD","ecmfa-vn SD","VN SD", "ChatGPT SD"], index= ["Persona F-Measure", "Entity F-Measure", "Action F-Measure"])
    else:
        crf_data = extract_data(crf_path)
        crf_average, crf_sd = crf_data

        for i in range(9):
            row_data.append([simple_average[i], ecmfa_vn_average[i], visual_narrator_average[i], chatgpt_average[i], crf_average[i], simple_sd[i], ecmfa_vn_sd[i], visual_narrator_sd[i], chatgpt_sd[i], crf_sd[i]])

        precision_data = pd.DataFrame([row_data[0],row_data[3],row_data[6]] , columns= ["Simple nlp", "ECMFA-VN", "Visual Narrator", "ChatGPT", "CRF", "Simple SD","ecmfa-vn SD","VN SD", "ChatGPT SD", "CRF SD"], index= ["Persona Precision", "Entity Precision", "Action Precision"])
        recall_data = pd.DataFrame([row_data[1],row_data[4],row_data[7]] , columns= ["Simple nlp", "ECMFA-VN", "Visual Narrator", "ChatGPT", "CRF", "Simple SD","ecmfa-vn SD","VN SD", "ChatGPT SD", "CRF SD"], index= ["Persona Recall", "Entity Recall", "Action Recall"])
        f_measure_data = pd.DataFrame([row_data[2],row_data[5],row_data[8]] , columns= ["Simple nlp", "ECMFA-VN", "Visual Narrator", "ChatGPT", "CRF", "Simple SD","ecmfa-vn SD","VN SD", "ChatGPT SD", "CRF SD"], index= ["Persona F-Measure", "Entity F-Measure", "Action F-Measure"])

    return precision_data, recall_data, f_measure_data

def create_final_bargraph(data, title, saving_path, crf_path):

    if crf_path == None:
        yerr = fix_max_y_error(data[["Simple SD","ecmfa-vn SD","VN SD", "ChatGPT SD"]], data[["Simple nlp", "ECMFA-VN","Visual Narrator", "ChatGPT"]])
        data[["Simple nlp", "ECMFA-VN","Visual Narrator", "ChatGPT"]].plot(kind='bar', yerr=yerr, error_kw=dict(lw = 3, capthick = 2, capsize = 7, ecolor='k'), figsize=(20,7), color = [plt.cm.Pastel1(0), plt.cm.Pastel1(1), plt.cm.Pastel1(2), plt.cm.Pastel1(3)])
    else:
        yerr = fix_max_y_error(data[["Simple SD","ecmfa-vn SD","VN SD", "ChatGPT SD", "CRF SD"]], data[["Simple nlp", "ECMFA-VN","Visual Narrator", "ChatGPT", "CRF"]])
        data[["Simple nlp", "ECMFA-VN","Visual Narrator", "ChatGPT", "CRF"]].plot(kind='bar', yerr=yerr, error_kw=dict(lw = 3, capthick = 2, capsize = 7, ecolor='k'), figsize=(20,7), color = [plt.cm.Pastel1(0), plt.cm.Pastel1(1), plt.cm.Pastel1(2), plt.cm.Pastel1(3), plt.cm.Pastel1(4)])
    
    plt.title(title,fontsize= 20)
    plt.ylabel("Average Score",fontsize=14)
    plt.xlabel("Measurement Type", fontsize=14)
    plt.ylim([0, 1])
    plt.legend(loc=(1.005,0.5))
    plt.xticks(rotation = 0)
    plt.tight_layout()
    plt.savefig(saving_path)

def fix_max_y_error(standard_deviation, y_data):
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