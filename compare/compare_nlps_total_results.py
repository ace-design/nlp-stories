#This script will compare all the final results of the nlp with each other
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys

def main():
    nlp_paths, nlps, saving_path, comparison_type, number_dataset, title_name = command()
    datasets_label = get_datasets_labels(comparison_type)

    nlp_data = []
    for nlp_path in nlp_paths:
        data = extract_data(nlp_path, number_dataset)
        nlp_data.append(data)

    formatted_data = format_data(datasets_label, number_dataset, nlp_data, nlps)

    persona_precision, persona_recall, persona_f_measure,entity_precision, entity_recall, entity_f_measure, action_precision, action_recall, action_f_measure = formatted_data

    create_final_bargraph(nlps, persona_precision,persona_recall, persona_f_measure, "Persona" + title_name + " " + comparison_type, saving_path + "_persona_nlp_compare.png")
    create_final_bargraph(nlps, entity_precision,entity_recall, entity_f_measure, "Entity" + title_name + " " + comparison_type, saving_path + "_entity_nlp_compare.png")
    create_final_bargraph(nlps, action_precision,action_recall, action_f_measure, "Action" + title_name + " " +  comparison_type, saving_path + "_action_nlp_compare.png")

    print("Graphs are saved")

def command():
    '''
    Runs the command line inputs

    Returns:
    args.evalationType (str): type of data scope used

    Raises:
    FileNotFoundError: raises excpetion
    wrong file type: raises exception
    not same comparison mode of both loading files: raises excpetion
    wrong file order: raises exception
    '''
    parser = argparse.ArgumentParser(description = "This program will compare all the nlp results and output visulations of the results")
    parser.add_argument("--load_gpt_3_5_v0125_path", type = str, help = "path of GPT-3.5 V0125 csv file")
    parser.add_argument("--load_gpt_3_5_v0613_2023_path", type = str, help = "path of GPT-3.5 V0613 2023 csv file")
    parser.add_argument("--load_gpt_3_5_v0613_2024_path", type = str, help = "path of GPT-3.5 V0613 2024 csv file")
    parser.add_argument("--load_gpt_4_turbo_v0125_path", type = str, help = "path of GPT-4 Turbo V0125 csv file") 
    parser.add_argument("--load_gpt_4_v0613_path", type = str, help = "path of GPT-4 Turbo V0613 csv file") 
    parser.add_argument("--load_visual_narrator_path", type = str, help = "path of visual narrator csv file")
    parser.add_argument("--load_crf_path", nargs="?", type = str, help = "path of crf csv file")
    parser.add_argument("evalationType", type = str, choices=["all", "primary"], help = "Type of data scope used [all, primary]")
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
            if not(args.path.endswith(".csv")):
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
            comparison_type = title(comparisons) + " Comparison"
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

        
        save_file_path = "final_results\\comparing_nlps_results\\total_results\\" + crf_path + data_type_folder + "\\" + comparison_type.lower().replace(" ", "_") + "\\" + saving_name

        if args.evalationType != "primary":
            title = ""
        else:
            title = " Primary Results"

    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        data = pd.read_csv(nlp_paths[0])
        number_dataset = len(data)

        return  nlp_paths, nlps, save_file_path, comparison_type, number_dataset, title

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

def format_data(datasets_label, number_dataset, nlp_data, nlps):
    '''
    formats the data so that it can be easily plotted onto the graphs

    Parameters:
    datasets_label (list): all the datsets that are in the csv files
    number_dataset (int): the number of datsets in the csv files
    nlp_data(3D list): the final data results from each nlp
    nlps (1D list): string list of nlp names corresponding to nlp_data

    Returns:
    formatted_data (list): contains the formatted data to plot for persona, entity, action's precision, recall, f_measure
    '''
    formatted_data = []

    for i in range(9):
        rounded_data_list = []
        nlp_list = []

        for j in range(len(nlp_data)):
            data = nlp_data[j]
            nlp = nlps[j]

            rounded_data = round_data(data[i].values.tolist())

            rounded_data_list.append(rounded_data)
            nlp_list = nlp_list + [nlp]*number_dataset

        formatted_data.append(pd.DataFrame({ "Dataset": datasets_label * 2,
                            "Data":  rounded_data_list,
                            "nlp":  nlp_list}))

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

def create_final_bargraph(nlps, precision_results,recall_results, f_measure_results, title, save_path):
    
    graph, (precision_plot, recall_plot, f_measure_plot) = plt.subplots(3, 1, figsize=(20, 6), sharex=True)

    palette = {}
    for i in range(len(nlps)):
        nlp = nlps[i]
        palette[nlp] = plt.cm.Pastel1(i)

    precision = sns.barplot(x= "Dataset", y= "Data", hue = "nlp",data = precision_results, ax = precision_plot, palette = palette, ci = None)
    precision.set(xlabel=None)
    precision.set_ylabel("Precision", fontsize = 14)

    # for i in precision.containers:
    #     precision.bar_label(i, fontsize = 6)

    recall = sns.barplot(x= "Dataset", y= "Data", hue = "nlp", data = recall_results, ax = recall_plot, palette = palette, ci = None)
    recall.set(xlabel=None)
    recall.set_ylabel("Recall", fontsize = 14)

    # for i in recall.containers:
    #     recall.bar_label(i, fontsize = 6)

    f_measure = sns.barplot(x= "Dataset", y= "Data", hue = "nlp", data = f_measure_results, ax = f_measure_plot, palette = palette, ci = None)
    f_measure_plot.set_xlabel("Dataset Grouping", fontsize = 14)
    f_measure.set_ylabel("F-Measure", fontsize = 14)

    # for i in f_measure.containers:
    #     f_measure.bar_label(i, fontsize = 6)


    precision_plot.set(ylim=(0, 1.05))
    recall_plot.set(ylim=(0, 1.05))
    f_measure_plot.set(ylim=(0, 1.05)) 
    
    graph.suptitle(title, fontsize = 20)

    precision.legend([],[], frameon=False)
    recall.legend([],[], frameon=False)
    f_measure.legend([],[], frameon=False)

    handles, labels = precision_plot.get_legend_handles_labels()
    graph.legend(handles=handles[:], labels=labels[:], title = "LEGEND", loc = "center right", bbox_to_anchor=(0.99, 0.5))

    graph.savefig(save_path)
    graph.savefig(save_path.replace(".png", ".pdf"))

if __name__ == "__main__":
    main()