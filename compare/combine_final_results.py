#This script will combine the final results grpahs of benchmark into one graph

import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

def main():
    with_crf, primary, save_name, title= command()

    # bklg_file_list, cat_file_list, glo_file_list, nlps = identify_files(with_crf, primary)
    bklg_file_list, glo_file_list, nlps = identify_files(with_crf, primary)

    bklg_data = extract_data(bklg_file_list)
    # cat_data = extract_data(cat_file_list)
    glo_data = extract_data(glo_file_list)

    # formatted_data = format_data(bklg_data, cat_data, glo_data, nlps)
    formatted_data = format_data(bklg_data, glo_data, nlps)

    save_csv_file(formatted_data, save_name)
    create_final_bargraph(formatted_data, nlps, title, save_name)
    
    print("Graph is saved")

def command():
    '''
    Runs the command line inputs

    Returns:
    args.with_crf (bool): use crf results in graphs
    args.primary (str): use primary results
    args.save_file_name (str): name of the file to be saved
    args.title (str): title of the graph

    Raises:
    FileNotFoundError: raises excpetion
    wrong file type: raises exception
    not same comparison mode of both loading files: raises excpetion
    wrong file order: raises exception
    '''
    parser = argparse.ArgumentParser(description = "This program will output a visulation of the results of differnt grouping of crf. NOTE: order within csv file must be strict, inclusion and then relaxed")
    parser.add_argument('--with_crf_intersection', default = False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--primary', default = False, action=argparse.BooleanOptionalAction)
    parser.add_argument("save_file_name", type = str, help = "name of file to save")
    parser.add_argument("title", type = str, help = "title of graph")

    args = parser.parse_args()


    return args.with_crf_intersection, args.primary, args.save_file_name, args.title

def identify_files(with_crf, primary):
    '''
    identify the files that contains the data to graph

    Parameters:
    with_crf (bool): use crf results in graphs
    primary (str): use primary results
    
    Returns:
    file_list (list): all the paths to the files with the data to graph

    '''

    if primary:
        data_type = "primary"
    else:
        data_type = "all"

    if with_crf:
        crf_path = "with_crf\\"
    else:
        crf_path = "without_crf\\"



    if with_crf:
        vn_bklg = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "individual_backlog\\visual_narrator\\dataset_csv_input_visual_narrator\\" +data_type + "_csv_results\\visual_narrator_individual_backlog_average.csv"
        gpt_4_v0613_bklg = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "individual_backlog\\gpt_4_v0613\\dataset_csv_input_gpt_4_v0613\\" + data_type + "_csv_results\\gpt_4_v0613_individual_backlog_average.csv"
        crf_bklg = "final_results\\individual_nlp_results\\total_results\\with_crf\\individual_backlog\\crf\\dataset_csv_input_crf\\" + data_type + "_csv_results\\crf_individual_backlog_average.csv"
        
        # vn_cat = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "categories\\visual_narrator\\dataset_csv_input_visual_narrator\\" +data_type + "_csv_results\\visual_narrator_categories_average.csv"
        # gpt_4_v0613_cat = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "categories\\gpt_4_v0613\\dataset_csv_input_gpt_4_v0613\\" + data_type + "_csv_results\\gpt_4_v0613_categories_average.csv"
        # crf_cat = "final_results\\individual_nlp_results\\total_results\\with_crf\\categories\\crf\\dataset_csv_input_crf\\" + data_type + "_csv_results\\crf_categories_average.csv"
        
        vn_glo = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "global\\visual_narrator\\dataset_csv_input_visual_narrator\\" +data_type + "_csv_results\\visual_narrator_global_average.csv"
        gpt_4_v0613_glo = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "global\\gpt_4_v0613\\dataset_csv_input_gpt_4_v0613\\" + data_type + "_csv_results\\gpt_4_v0613_global_average.csv"        
        crf_glo = "final_results\\individual_nlp_results\\total_results\\with_crf\\global\\crf\\dataset_csv_input_crf\\" + data_type + "_csv_results\\crf_global_average.csv"

        bklg_file_list = [vn_bklg, gpt_4_v0613_bklg, crf_bklg]
        # cat_file_list = [vn_cat, gpt_4_v0613_cat, crf_cat]
        glo_file_list = [vn_glo, gpt_4_v0613_glo, crf_glo]

        nlps = ["Visual Narrator", "GPT-4 v0613", "CRF"]
    else:
        gpt_3_5_v0125_bklg = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "individual_backlog\\gpt_3_5_v0125\\dataset_csv_input_gpt_3_5_v0125\\" + data_type + "_csv_results\\gpt_3_5_v0125_individual_backlog_average.csv"
        gpt_3_5_v0613_2023_bklg = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "individual_backlog\\gpt_3_5_v0613_2023\\dataset_csv_input_gpt_3_5_v0613_2023\\" + data_type + "_csv_results\\gpt_3_5_v0613_2023_individual_backlog_average.csv"
        gpt_3_5_v0613_2024_bklg = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "individual_backlog\\gpt_3_5_v0613_2024\\dataset_csv_input_gpt_3_5_v0613_2024\\" + data_type + "_csv_results\\gpt_3_5_v0613_2024_individual_backlog_average.csv"
        gpt_4_turbo_v0125_bklg = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "individual_backlog\\gpt_4_turbo_v0125\\dataset_csv_input_gpt_4_turbo_v0125\\" + data_type + "_csv_results\\gpt_4_turbo_v0125_individual_backlog_average.csv"
        gpt_4_v0613_bklg = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "individual_backlog\\gpt_4_v0613\\dataset_csv_input_gpt_4_v0613\\" + data_type + "_csv_results\\gpt_4_v0613_individual_backlog_average.csv"
        
        # gpt_3_5_v0125_cat = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "categories\\gpt_3_5_v0125\\dataset_csv_input_gpt_3_5_v0125\\" + data_type + "_csv_results\\gpt_3_5_v0125_categories_average.csv"
        # gpt_3_5_v0613_2023_cat = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "categories\\gpt_3_5_v0613_2023\\dataset_csv_input_gpt_3_5_v0613_2023\\" + data_type + "_csv_results\\gpt_3_5_v0613_2023_categories_average.csv"
        # gpt_3_5_v0613_2024_cat = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "categories\\gpt_3_5_v0613_2024\\dataset_csv_input_gpt_3_5_v0613_2024\\" + data_type + "_csv_results\\gpt_3_5_v0613_2024_categories_average.csv"
        # gpt_4_turbo_v0125_cat = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "categories\\gpt_4_turbo_v0125\\dataset_csv_input_gpt_4_turbo_v0125\\" + data_type + "_csv_results\\gpt_4_turbo_v0125_categories_average.csv"
        # gpt_4_v0613_cat = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "categories\\gpt_4_v0613\\dataset_csv_input_gpt_4_v0613\\" + data_type + "_csv_results\\gpt_4_v0613_categories_average.csv"
       
        gpt_3_5_v0125_glo = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "global\\gpt_3_5_v0125\\dataset_csv_input_gpt_3_5_v0125\\" + data_type + "_csv_results\\gpt_3_5_v0125_global_average.csv"
        gpt_3_5_v0613_2023_glo = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "global\\gpt_3_5_v0613_2023\\dataset_csv_input_gpt_3_5_v0613_2023\\" + data_type + "_csv_results\\gpt_3_5_v0613_2023_global_average.csv"
        gpt_3_5_v0613_2024_glo = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "global\\gpt_3_5_v0613_2024\\dataset_csv_input_gpt_3_5_v0613_2024\\" + data_type + "_csv_results\\gpt_3_5_v0613_2024_global_average.csv"
        gpt_4_turbo_v0125_glo = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "global\\gpt_4_turbo_v0125\\dataset_csv_input_gpt_4_turbo_v0125\\" + data_type + "_csv_results\\gpt_4_turbo_v0125_global_average.csv"
        gpt_4_v0613_glo = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "global\\gpt_4_v0613\\dataset_csv_input_gpt_4_v0613\\" + data_type + "_csv_results\\gpt_4_v0613_global_average.csv"

        bklg_file_list = [gpt_3_5_v0125_bklg, gpt_3_5_v0613_2023_bklg, gpt_3_5_v0613_2024_bklg, gpt_4_turbo_v0125_bklg, gpt_4_v0613_bklg]
        # cat_file_list = [gpt_3_5_v0125_cat, gpt_3_5_v0613_2023_cat, gpt_3_5_v0613_2024_cat, gpt_4_turbo_v0125_cat, gpt_4_v0613_cat]
        glo_file_list = [gpt_3_5_v0125_glo, gpt_3_5_v0613_2023_glo, gpt_3_5_v0613_2024_glo, gpt_4_turbo_v0125_glo, gpt_4_v0613_glo]

        nlps = ["GPT-3.5 Turbo v0125", "GPT-3.5 v0613 2023", "GPT-3.5 v0613 2024", "GPT-4 Turbo v0125", "GPT-4 v0613"]
        

    # return bklg_file_list, cat_file_list, glo_file_list, nlps
    return bklg_file_list, glo_file_list, nlps

def extract_data(file_list):
    '''
    extract the data from the csv file 

    Parameters:
    file_list (list): all the paths to the files with the data to graph

    Returns:
    data(3D list): the final data results to be graphed
    '''

    data = []

    for path in file_list:
        extract = pd.read_csv(path) 

        average = extract["Average"]
        standard_deviation = extract["Standard Deviation"]
        label = extract["Comparison Mode"]

        data.append([average, standard_deviation, label])

    return data

# def format_data(bklg_data, cat_data, glo_data, nlps):
def format_data(bklg_data, glo_data, nlps):
    '''
    formats the data so that it can be easily plotted onto the graphs

    Parameters:
    data(3D list): the final data results to be graphed
    with_crf (bool): use crf results in graphs

    Returns:
    formatted_data (list): contains the formatted data to graph
    '''

    strict_bklg_data, inclusion_bklg_data, relaxed_bklg_data = organize_data(bklg_data, nlps)
    # strict_cat_data, inclusion_cat_data, relaxed_cat_data = organize_data(cat_data, nlps)
    strict_glo_data, inclusion_glo_data, relaxed_glo_data = organize_data(glo_data, nlps)
    
    # formatted_data = [strict_bklg_data, inclusion_bklg_data, relaxed_bklg_data, strict_cat_data, inclusion_cat_data, relaxed_cat_data,strict_glo_data, inclusion_glo_data, relaxed_glo_data]
    formatted_data = [strict_bklg_data, inclusion_bklg_data, relaxed_bklg_data, strict_glo_data, inclusion_glo_data, relaxed_glo_data]

    return formatted_data

def organize_data(data, nlps):
    
    table = []
    nlp_labels = []

    for i in range(27):
        nlps_average = []
        nlps_sd = []
        labels = []

        for j in range(len(nlps)):
            nlp_data = data[j]

            average, sd, label = nlp_data

            nlps_average.append(float(average[i]))
            nlps_sd.append(float(sd[i]))
            labels.append(label[i])
        
        row = nlps_average + nlps_sd
        nlp_labels.append(labels)
        table.append(row)

    
    average_label = []
    sd_label = []
    for nlp in nlps:
        average_label.append(nlp)
        sd_label.append(nlp + " SD")

    
    column_label = average_label + sd_label

    for i in range (0,27,9):
        isStrict = True
        isInclusion = True
        isRelaxed = True

        formattedData = pd.DataFrame([table[i+2],table[i+5],table[i+8]] , columns= column_label, index= ["Persona", "Entity", "Action"])

        interestedLabels = [nlp_labels[i+2], nlp_labels[i+5], nlp_labels[i+8]]

        for labelRow in interestedLabels:
            for label in labelRow:
                if label != "Strict Comparison":
                    isStrict = False
                if label != "Inclusion Comparison":
                    isInclusion = False
                if label != "Relaxed Comparison":
                    isRelaxed = False

        # Only one can be true
        if (isStrict and isInclusion) or (isStrict and isRelaxed) or (isInclusion and isRelaxed):
            sys.tracebacklimit = 0
            raise Exception ("Invalid data matching across files. Ensure that the comparison mode matches across each file")

        if isStrict:
            strict_data = formattedData
        elif isInclusion:
            inclusion_data = formattedData
        elif isRelaxed:
            relaxed_data = formattedData
            

    return strict_data, inclusion_data, relaxed_data


def save_csv_file(formatted_data, save_name):
    '''
    will save all the final results into one csv file

    Parameters:
    formatted_data (list): contains all the final information
    save_name (str): name of the saving file
    ''' 
    final_data = pd.concat(formatted_data)
    # comparison_mode = (["Strict"] * 3 + ["Inclusion"] * 3 + ["Relaxed"] * 3) * 3
    # data_groupings = ["Individual Backlog"] * 9 + ["Categories"] * 9 + ["Global"] * 9
    comparison_mode = (["Strict"] * 3 + ["Inclusion"] * 3 + ["Relaxed"] * 3) * 2
    data_groupings = ["Individual Backlog"] * 9  + ["Global"] * 9


    final_data["Comparison Mode"] = comparison_mode
    final_data["Data Groupings"] = data_groupings

    saving_path = "final_results\\comparing_nlps_results\\average_results\\combined_results\\final_data\\" + save_name + ".csv"

    final_data.to_csv(saving_path)

def create_final_bargraph(formatted_data, nlps, title, save_name):
    
    # strict_bklg_data, inclusion_bklg_data, relaxed_bklg_data, strict_cat_data, inclusion_cat_data, relaxed_cat_data,strict_glo_data, inclusion_glo_data, relaxed_glo_data = formatted_data
    strict_bklg_data, inclusion_bklg_data, relaxed_bklg_data, strict_glo_data, inclusion_glo_data, relaxed_glo_data = formatted_data

    standard_deviation = []
    palette = []
    for i in range(len(nlps)):
        nlp = nlps[i]
        standard_deviation.append(nlp + " SD")
        palette.append(plt.cm.Pastel1(i))

    # graph, position = plt.subplots(3, 3, figsize=(10, 5))
    graph, position = plt.subplots(2, 3, figsize=(10, 5))

    #Top Left
    yerr = fix_max_y_error(strict_bklg_data[standard_deviation], strict_bklg_data[nlps])
    strict_bklg_data[nlps].plot(ax = position[0,0], kind='bar', yerr = yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 4, ecolor='k'), figsize=(17,7), color = palette)
    position[0,0].set_title("Strict Comparison", fontsize = 14)
    position[0,0].set_ylabel("Individual Backlog", fontsize = 14)
    position[0,0].tick_params(labelrotation = 0)
    position[0,0].get_legend().remove()
    position[0,0].set_ylim([0, 1])
    position[0,0].set_xticks([])

    #Middle Left
    # yerr = fix_max_y_error(strict_cat_data[standard_deviation], strict_cat_data[y_data])
    # strict_cat_data[y_data].plot(ax = position[1,0], kind='bar', yerr = yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 4, ecolor='k'), figsize=(17,7), color = palette)
    # position[1,0].set_ylabel("Categories", fontsize = 14)
    # position[1,0].tick_params(labelrotation = 0)
    # position[1,0].get_legend().remove()
    # position[1,0].set_ylim([0, 1])
    # position[1,0].set_xticks([])

    #bottom Left
    yerr = fix_max_y_error(strict_glo_data[standard_deviation], strict_glo_data[nlps])
    strict_glo_data[nlps].plot(ax = position[1,0], kind='bar', yerr = yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 4, ecolor='k'), figsize=(17,7), color = palette)
    position[1,0].set_ylabel("Global", fontsize = 14)
    position[1,0].tick_params(labelrotation = 0)
    position[1,0].get_legend().remove()
    position[1,0].set_ylim([0, 1])

    #Top center
    yerr = fix_max_y_error(inclusion_bklg_data[standard_deviation], inclusion_bklg_data[nlps])
    inclusion_bklg_data[nlps].plot(ax = position[0,1], kind='bar', yerr = yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 4, ecolor='k'), figsize=(17,7), color = palette)
    position[0,1].set_title("Inclusion Comparison", fontsize = 14)
    position[0,1].tick_params(labelrotation = 0)
    position[0,1].get_legend().remove()
    position[0,1].set_ylim([0, 1])
    position[0,1].set_xticks([])

    #Center
    # yerr = fix_max_y_error(inclusion_cat_data[standard_deviation], inclusion_cat_data[y_data])
    # inclusion_cat_data[y_data].plot(ax = position[1,1], kind='bar', yerr = yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 4, ecolor='k'), figsize=(17,7), color = palette)
    # position[1,1].tick_params(labelrotation = 0)
    # position[1,1].get_legend().remove()
    # position[1,1].set_ylim([0, 1])
    # position[1,1].set_xticks([])

    #bottom center
    yerr = fix_max_y_error(inclusion_glo_data[standard_deviation], inclusion_glo_data[nlps])
    inclusion_glo_data[nlps].plot(ax = position[1,1], kind='bar', yerr = yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 4, ecolor='k'), figsize=(17,7), color = palette)
    position[1,1].tick_params(labelrotation = 0)
    position[1,1].get_legend().remove()
    position[1,1].set_ylim([0, 1])

    #Top right
    yerr = fix_max_y_error(relaxed_bklg_data[standard_deviation], relaxed_bklg_data[nlps])
    relaxed_bklg_data[nlps].plot(ax = position[0,2], kind='bar', yerr = yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 4, ecolor='k'), figsize=(17,7), color = palette)
    position[0,2].set_title("Relaxed Comparison", fontsize = 14)
    position[0,2].tick_params(labelrotation = 0)
    position[0,2].get_legend().remove()
    position[0,2].set_ylim([0, 1])
    position[0,2].set_xticks([])

    #middle right
    # yerr = fix_max_y_error(relaxed_cat_data[standard_deviation], relaxed_cat_data[y_data])
    # relaxed_cat_data[y_data].plot(ax = position[1,2], kind='bar', yerr = yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 4, ecolor='k'), figsize=(17,7), color = palette)
    # position[1,2].tick_params(labelrotation = 0)
    # position[1,2].get_legend().remove()
    # position[1,2].set_ylim([0, 1])
    # position[1,2].set_xticks([])
    # position[1,2].legend(loc=(1.025,0.25))

    #bottom right
    yerr = fix_max_y_error(relaxed_glo_data[standard_deviation], relaxed_glo_data[nlps])
    relaxed_glo_data[nlps].plot(ax = position[1,2], kind='bar', yerr = yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 4, ecolor='k'), figsize=(17,7), color = palette)
    position[1,2].tick_params(labelrotation = 0)
    position[1,2].get_legend().remove()
    position[1,2].set_ylim([0, 1])

    graph.suptitle(title, fontsize = 20)
    graph.supxlabel("Label Type", fontsize=14)
    graph.supylabel("F-Measure", x = 0.01, y = 0.5, fontsize = 14)
    graph.legend(labels=nlps, title = "LEGEND", loc = "center right", bbox_to_anchor=(1.12, 0.5))
    
    plt.tight_layout()

    saving_path_png = "final_results\\comparing_nlps_results\\average_results\\combined_results\\graphs\\" + save_name + ".png"
    saving_path_pdf = "final_results\\comparing_nlps_results\\average_results\\combined_results\\graphs\\" + save_name + ".pdf"
    
    plt.savefig(saving_path_png, bbox_inches='tight')
    plt.savefig(saving_path_pdf, bbox_inches='tight')

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