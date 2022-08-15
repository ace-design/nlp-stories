#runs the comparison files to get compare nlp final results with each other for a specific dataset grouping type 
import argparse
import csv
import pandas as pd
import subprocess

def main():
    grouping_code, with_crf = command()
    data_group_names, datasets, grouping, crf_path, is_crf, crf_string, nlp, nlp_code = get_info(grouping_code, with_crf)
    types = ["all", "primary"]
    comparison_mode = ["strict", "inclusion", "relaxed"]

    # for i in range(len(nlp)):
    #     run_compare_nlp(nlp[i], nlp_code[i], datasets, grouping, grouping_code, crf_path, is_crf)
    #     reset_nlp_dataset_names_list(data_group_names)
    #     run_compare_individual_nlp_total_results(comparison_mode, nlp_code[i], grouping_code, is_crf)

    # run_compare_nlps_total_results(types, comparison_mode, grouping, grouping_code, crf_string)
    # run_compare_nlps_average_results(types, comparison_mode, grouping, grouping_code, crf_string)
    for nlp_tool in nlp:
        combine_average_results_data(nlp_tool, types, grouping, crf_string)
    
def command():
    '''
    runs the command line prompt

    Returns:
    args.data_type (str): evaluation by individual backlogs - BKLG, categorized backlogs - CAT, or global - GLO
    args.with_crf (bool): True if dataset contains the crf intersecting set 
    '''
    parser = argparse.ArgumentParser(description = "This program is to run the comparison files to get compare nlp final results with each other for a specific dataset grouping type ")
    parser.add_argument("data_type", type = str, choices=["BKLG", "CAT", "GLO"], help = "evaluation by individual backlogs - BKLG, categorized backlogs - CAT, or global - GLO")
    parser.add_argument('--with_crf', default = False, action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    return args.data_type, args.with_crf

def get_info(grouping_code, with_crf):
    '''
    gets relevant info based on the input from the command line

    Parameters:
    grouping_code (str): evaluation by individual backlogs - BKLG, categorized backlogs - CAT, or global - GLO
    with_crf (bool): True if dataset contains the crf intersecting set 
    
    Returns:
    data_group_names (list): names of groupings of dataset 
    datasets (list): groupings of the dataset
    grouping (str): grouping type  
    crf_path (str): folder name if it includes crf intersecting set or not
    is_crf (str): command to indicate if crf intersecting set is included
    nlp (list): the nlp tools in the comparison
    nlp_code (list): nlp code names corresponding to the nlp list
    '''
    if grouping_code == "BKLG":
        data_group_names = ["g02\n", "g03\n", "g04\n", "g05\n", "g08\n", "g10\n", "g11\n", "g12\n", "g13\n", "g14\n", "g17\n", "g18\n", "g19\n", "g21\n", "g22\n", "g23\n", "g24\n", "g25\n", "g26\n", "g27\n", "g28\n"]
        datasets = ["g02", "g03", "g04", "g05", "g08", "g10", "g11", "g12", "g13", "g14", "g17", "g18", "g19", "g21", "g22", "g23", "g24", "g25", "g26", "g27", "g28"]
        grouping = "individual_backlog"
    elif grouping_code == "CAT":
        data_group_names = ["Content Management\n", "DEV\n", "IOT\n", "Management App\n", "Reporting\n", "Web\n"]
        datasets = ["content_management", "dev", "iot", "management_app", "reporting", "web"]
        grouping = "categories"
    else:
        data_group_names = ["Global\n"]
        datasets = ["global"]
        grouping = "global"

    if with_crf:
        crf_path = "nlp_outputs_intersecting_crf"
        is_crf = "--with_crf"
        crf_string = "with_crf"
        nlp = ["crf", "ecmfa_vn", "simple", "visual_narrator"]
        nlp_code = ["CRF", "ECMFA", "SIMPLE", "VN"]
    else:
        crf_path = "nlp_outputs_intersecting"
        is_crf = ""
        crf_string = "without_crf"
        nlp = ["ecmfa_vn", "simple", "visual_narrator"]
        nlp_code = ["ECMFA", "SIMPLE", "VN"]

    return data_group_names, datasets, grouping, crf_path, is_crf, crf_string, nlp, nlp_code

def run_compare_nlp(nlp, nlp_code, datasets, grouping, grouping_code, crf_path, is_crf):
    '''Runs compare_nlp.py '''
    print("Starting " + nlp + " baseline comparison")

    for dataset in datasets:
        line = "python .\compare\compare_nlp.py nlp\\nlp_outputs\\" + grouping + "\\" + crf_path + "\\pos_baseline\\" + dataset + "_baseline_intersecting_pos.json"  + \
        " nlp\\nlp_outputs\\" + grouping + "\\" + crf_path + "\\" + nlp + "\\"+ dataset + "_" + nlp + "_intersecting.json "+ dataset + "_" + nlp + " STRICT " + nlp_code + " " + grouping_code + " " + is_crf
        subprocess.run(line)

        line = "python .\compare\compare_nlp.py nlp\\nlp_outputs\\" + grouping + "\\" + crf_path + "\\pos_baseline\\" + dataset + "_baseline_intersecting_pos.json"  + \
        " nlp\\nlp_outputs\\" + grouping + "\\" + crf_path + "\\" + nlp + "\\"+ dataset + "_" + nlp + "_intersecting.json "+ dataset + "_" + nlp + " INCLU " + nlp_code + " " + grouping_code + " " + is_crf
        subprocess.run(line)

        line = "python .\compare\compare_nlp.py nlp\\nlp_outputs\\" + grouping + "\\" + crf_path + "\\pos_baseline\\" + dataset + "_baseline_intersecting_pos.json"  + \
        " nlp\\nlp_outputs\\" + grouping + "\\" + crf_path + "\\" + nlp + "\\"+ dataset + "_" + nlp + "_intersecting.json "+ dataset + "_" + nlp + " RELAX " + nlp_code + " " + grouping_code + " " + is_crf
        subprocess.run(line)

def reset_nlp_dataset_names_list(data_group_names):
    '''Reset nlp_dataset_names_list'''
    paths = ["compare\\nlp_dataset_names_list\\dataset_list_strict.txt", "compare\\nlp_dataset_names_list\\dataset_list_inclusion.txt", "compare\\nlp_dataset_names_list\\dataset_list_relaxed.txt"]
    for path in paths:
        with open(path, "w", encoding = "utf-8") as file:
            file.writelines(data_group_names)

def run_compare_individual_nlp_total_results(comparison_mode, nlp_code, grouping_code, is_crf):
    '''Runs the compare_individual_nlp_total_results.py script'''
    for comparison in comparison_mode:
        line = "python .\compare\compare_individual_nlp_total_results.py compare\\nlp_dataset_csv_results\\primary_csv_results\\" + comparison + "_dataset_results.csv " +\
            "compare\\nlp_dataset_csv_results\\all_csv_results\\" + comparison + "_dataset_results.csv  " + nlp_code + " " + grouping_code + " " + is_crf 
        subprocess.run(line)

def run_compare_nlps_total_results(types, comparison_mode, grouping, grouping_code, crf_path):
    '''Runs the compare_nlps_total_results.py script '''

    print("Starting nlps' total results comparison")

    for type in types:
        for comparison in comparison_mode:
            line = "python .\compare\compare_nlps_total_results.py final_results\\individual_nlp_results\\total_results\\" + crf_path + "\\" + grouping + "\\simple\\dataset_csv_input_simple\\" + type + "_csv_results\\" + comparison + "_comparison_dataset_results.csv " +\
            "final_results\\individual_nlp_results\\total_results\\" + crf_path + "\\" + grouping + "\\ecmfa_vn\\dataset_csv_input_ecmfa_vn\\" + type + "_csv_results\\" + comparison + "_comparison_dataset_results.csv "+\
            "final_results\\individual_nlp_results\\total_results\\" + crf_path + "\\" + grouping + "\\visual_narrator\\dataset_csv_input_visual_narrator\\" + type + "_csv_results\\" + comparison + "_comparison_dataset_results.csv " +\
            "--load_crf_path final_results\\individual_nlp_results\\total_results\\" + crf_path + "\\" + grouping + "\\crf\\dataset_csv_input_crf\\" + type + "_csv_results\\" + comparison + "_comparison_dataset_results.csv " +\
            type + " " + grouping_code
            subprocess.run(line)

def run_compare_nlps_average_results(types, comparison_mode, grouping, grouping_code, crf_path):
    '''Runs the compare_nlps_average_results.py script'''

    print("Starting nlps' average results comparison")

    for type in types:
        for comparison in comparison_mode:
            line = "python .\compare\compare_nlps_average_results.py final_results\\individual_nlp_results\\total_results\\" + crf_path + "\\" + grouping + "\\simple\\" + comparison + "_simple\\" + type + "\\" + type + "_results.csv " +\
            "final_results\\individual_nlp_results\\total_results\\" + crf_path + "\\" + grouping + "\\ecmfa_vn\\" + comparison + "_ecmfa_vn\\" + type + "\\" + type + "_results.csv " +\
            "final_results\\individual_nlp_results\\total_results\\" + crf_path + "\\" + grouping + "\\visual_narrator\\" + comparison + "_visual_narrator\\" + type + "\\" + type + "_results.csv " +\
            "--load_crf_path final_results\\individual_nlp_results\\total_results\\" + crf_path + "\\" + grouping + "\\crf\\" + comparison + "_crf\\" + type + "\\" + type + "_results.csv " +\
            type + " " + grouping_code
            subprocess.run(line)

def combine_average_results_data(nlp, types, grouping, crf_path):
    '''combine the average final results into csv files so that the final graphs can be made later'''

    print("starting " + nlp + " combining final average results")
    
    for type in types:
        strict_path = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "\\" + grouping + "\\" + nlp + "\\strict_" + nlp + "\\" + type + "\\" + type + "_results.csv"
        extract = pd.read_csv(strict_path) 

        final_path = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "\\" + grouping + "\\" + nlp + "\\dataset_csv_input_" + nlp + "\\" + type + "_csv_results\\" + nlp + "_" + grouping + "_average.csv"
        file = open(final_path, "w")
        file.close()
        extract.to_csv(final_path, index = False)

        line = "python .\setup_data\merge_data.py " + final_path + " final_results\\individual_nlp_results\\total_results\\" + crf_path + "\\" + grouping + "\\" + nlp + "\\inclusion_" + nlp + "\\" + type + "\\" + type + "_results.csv"
        subprocess.run(line)

        line = "python .\setup_data\merge_data.py " + final_path + " final_results\\individual_nlp_results\\total_results\\" + crf_path + "\\" + grouping + "\\" + nlp + "\\relaxed_" + nlp + "\\" + type + "\\" + type + "_results.csv"
        subprocess.run(line)

    print("Finished " + nlp + " combining final average results")

if __name__ == "__main__":
    main()