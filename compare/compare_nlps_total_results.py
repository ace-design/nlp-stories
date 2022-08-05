#This script will compare all the final results of the nlp with each other
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys

def main():
    simple_path, ecmfa_vn_path, visual_narrator_path, crf_path, saving_path, comparison_type, number_dataset, title_name = command()
    datasets_label = get_datasets_labels(comparison_type)

    simple_data = extract_data(simple_path, number_dataset)
    ecmfa_vn_data = extract_data(ecmfa_vn_path, number_dataset)
    visual_narrator_data = extract_data(visual_narrator_path, number_dataset)

    formatted_data = format_data(datasets_label, number_dataset, simple_data, ecmfa_vn_data, visual_narrator_data, crf_path)

    persona_precision, persona_recall, persona_f_measure,entity_precision, entity_recall, entity_f_measure, action_precision, action_recall, action_f_measure = formatted_data

    create_final_bargraph(persona_precision,persona_recall, persona_f_measure, "Persona" + title_name + " " + comparison_type, saving_path + "_persona_nlp_compare.png", crf_path)
    create_final_bargraph(entity_precision,entity_recall, entity_f_measure, "Entity" + title_name + " " + comparison_type, saving_path + "_entity_nlp_compare.png", crf_path)
    create_final_bargraph(action_precision,action_recall, action_f_measure, "Action" + title_name + " " +  comparison_type, saving_path + "_action_nlp_compare.png", crf_path)

    print("Graphs are saved")

def command():
    '''
    Runs the command line inputs

    Returns:
    args.load_simple_path (str): Path to the simple data csv file to be loaded
    args.load_ecmfa_vn_path (str): Path to the ecmfa_vn data csv file to be loaded
    args.load_visual_narrator_path (str): Path to the visual narrator data csv file to be loaded
    args.load_crf_path (str): Path to the crf data csv file to be loaded, it is NONE if it is not given
    args.save_file_name (str): name of the file to be saved

    Raises:
    FileNotFoundError: raises excpetion
    wrong file type: raises exception
    not same comparison mode of both loading files: raises excpetion
    wrong file order: raises exception
    '''
    parser = argparse.ArgumentParser(description = "This program will compare all the nlp results and output visulations of the results")
    parser.add_argument("load_simple_path", type = str, help = "path of simple csv file")
    parser.add_argument("load_ecmfa_vn_path", type = str, help = "path of ecmfa_vn csv file")
    parser.add_argument("load_visual_narrator_path", type = str, help = "path of visual narrator csv file")
    parser.add_argument("--load_crf_path", nargs="?", type = str, help = "path of crf csv file")
    parser.add_argument("save_file_name", type = str, help = "name of file to save")
    parser.add_argument("data_type", type = str, choices=["BKLG", "CAT", "GLO"], help = "evaluation by individual backlogs - BKLG, categorized backlogs - CAT, or global - GLO")

    
    args = parser.parse_args()

    if not(args.load_simple_path.endswith(".csv")) or not(args.load_ecmfa_vn_path.endswith(".csv")) or not(args.load_visual_narrator_path.endswith(".csv")) or (args.load_crf_path != None and not(args.load_crf_path.endswith(".csv"))):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect input file type. Save file type is .csv")

    if "strict" in args.load_simple_path and "strict" in args.load_ecmfa_vn_path and "strict" in args.load_visual_narrator_path:
        comparison_type = "Strict Comparison"
        saving_name = "strict_" + args.save_file_name
    elif "inclusion" in args.load_simple_path and "inclusion" in args.load_ecmfa_vn_path and "inclusion" in args.load_visual_narrator_path:
        comparison_type = 'Inclusion Comparison'
        saving_name = "inclusion_" + args.save_file_name
    elif "relaxed" in args.load_simple_path and "relaxed" in args.load_ecmfa_vn_path and "relaxed" in args.load_visual_narrator_path:
        comparison_type = "Relaxed Comparison"
        saving_name = "relaxed_" + args.save_file_name
    else:
        sys.tracebacklimit = 0 
        raise Exception("Incompatible combination. All files must be evaluated by same comparison mode")

    if not("simple" in args.load_simple_path) or not("ecmfa_vn" in args.load_ecmfa_vn_path) or not("visual_narrator" in args.load_visual_narrator_path):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect order of input file. First file is simple, then ecmfa_vn, and then visual narrator")

    try:
        load_file = open(args.load_simple_path)
        load_file.close()
        load_file = open(args.load_ecmfa_vn_path)
        load_file.close()
        load_file = open(args.load_visual_narrator_path)
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

        
        save_file_path = "final_results\\comparing_nlps_results\\total_results\\" + crf_path + data_type_folder + "\\" + comparison_type.lower().replace(" ", "_") + "\\" + saving_name

        if args.save_file_name != "primary":
            title = ""
        else:
            title = " Primary Results"

    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        data = pd.read_csv(args.load_simple_path)
        number_dataset = len(data)

        return args.load_simple_path, args.load_ecmfa_vn_path, args.load_visual_narrator_path, args.load_crf_path, save_file_path, comparison_type, number_dataset, title

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

def get_datasets_labels(comparison_type):
    '''
    get the datasets names that were evaluated by the nlp tools 

    Parameters:
    comparison_type (str): type of comparison mode 

    Returns:
    datasets_label (list): datasets that were used
    '''

    if comparison_type == "Strict Comparison":
        path = "compare\\nlp_dataset_names_list\\dataset_list_strict.txt"
    elif comparison_type == "Inclusion Comparison":
        path = "compare\\nlp_dataset_names_list\\dataset_list_inclusion.txt"
    else:
        path = "compare\\nlp_dataset_names_list\\dataset_list_relaxed.txt" 

    with open (path, "r") as file:
        datasets_label = file.readlines()

    return datasets_label

def format_data(datasets_label, number_dataset, simple_data, ecmfa_vn_data, visual_narrator_data, crf_path):
    '''
    formats the data so that it can be easily plotted onto the graphs

    Parameters:
    datasets_label (list): all the datsets that are in the csv files
    number_dataset (int): the number of datsets in the csv files
    simple_data(2D list): the final data results from simple nlp
    ecmfa_vn_data(2D list): the final data results from ecmfa_vn nlp
    visual_narrator_data(2D list): the final data results from visual narrator nlp
    crf_path (str): path to crf csv files or is NONE if not given 

    Returns:
    formatted_data (list): contains the formatted data to plot for persona, entity, action's precision, recall, f_measure
    '''
    formatted_data = []

    if crf_path == None:
        for i in range(9):
            rounded_simple = round_data(simple_data[i].values.tolist())
            rounded_ecmfa_vn = round_data(ecmfa_vn_data[i].values.tolist())
            rounded_visual_narrator = round_data(visual_narrator_data[i].values.tolist())

            formatted_data.append(pd.DataFrame({ "Dataset": datasets_label * 3,
                                "Data": rounded_simple + rounded_ecmfa_vn + rounded_visual_narrator,
                                "nlp": ["Simple"]*number_dataset + ["ECMFA-VN"]*number_dataset + ["Visual Narrator"]*number_dataset}))
    else:
        crf_data = extract_data(crf_path, number_dataset)

        for i in range(9):
            rounded_simple = round_data(simple_data[i].values.tolist())
            rounded_ecmfa_vn = round_data(ecmfa_vn_data[i].values.tolist())
            rounded_visual_narrator = round_data(visual_narrator_data[i].values.tolist())
            rounded_crf = round_data(crf_data[i].values.tolist())

            formatted_data.append(pd.DataFrame({ "Dataset": datasets_label * 4,
                                "Data": rounded_simple + rounded_ecmfa_vn + rounded_visual_narrator + rounded_crf,
                                "nlp": ["Simple"]*number_dataset + ["ECMFA-VN"]*number_dataset + ["Visual Narrator"]*number_dataset + ["CRF"] * number_dataset}))

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

def create_final_bargraph(precision_results,recall_results, f_measure_results, title, save_path, crf_path):
    
    graph, (precision_plot, recall_plot, f_measure_plot) = plt.subplots(3, 1, figsize=(20, 6), sharex=True)

    if crf_path == None:
        palette ={"Simple": "#f29e8e", "ECMFA-VN": "indianred", "Visual Narrator": "#9a0200"}
    else:
        palette ={"Simple": "#f29e8e", "ECMFA-VN": "indianred", "Visual Narrator": "#9a0200", "CRF": "#4c0000"}

    precision = sns.barplot(x= "Dataset", y= "Data", hue = "nlp",data = precision_results, ax = precision_plot, palette = palette, ci = None, alpha = 0.85)
    precision.set(xlabel=None)
    precision.set_ylabel("Precision", fontsize = 14)

    # for i in precision.containers:
    #     precision.bar_label(i, fontsize = 6)

    recall = sns.barplot(x= "Dataset", y= "Data", hue = "nlp", data = recall_results, ax = recall_plot, palette = palette, ci = None, alpha = 0.85)
    recall.set(xlabel=None)
    recall.set_ylabel("Recall", fontsize = 14)

    # for i in recall.containers:
    #     recall.bar_label(i, fontsize = 6)

    f_measure = sns.barplot(x= "Dataset", y= "Data", hue = "nlp", data = f_measure_results, ax = f_measure_plot, palette = palette, ci = None, alpha = 0.85)
    f_measure_plot.set_xlabel("Dataset Grouping", fontsize = 14)
    f_measure.set_ylabel("F-Measure", fontsize = 14)

    # for i in f_measure.containers:
    #     f_measure.bar_label(i, fontsize = 6)


    precision_plot.set(ylim=(0, 1.2))
    recall_plot.set(ylim=(0, 1.2))
    f_measure_plot.set(ylim=(0, 1.2)) 
    
    graph.suptitle(title, fontsize = 20)

    precision.legend([],[], frameon=False)
    recall.legend([],[], frameon=False)
    f_measure.legend([],[], frameon=False)

    handles, labels = precision_plot.get_legend_handles_labels()
    graph.legend(handles=handles[:], labels=labels[:], title = "LEGEND", loc = "center right", bbox_to_anchor=(0.99, 0.5))

    graph.savefig(save_path)

if __name__ == "__main__":
    main()