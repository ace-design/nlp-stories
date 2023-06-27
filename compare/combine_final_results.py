#This script will combine the final results grpahs of benchmark into one graph

import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

def main():
    with_crf, primary, save_name, title= command()

    file_list = identify_files(with_crf, primary)

    data = extract_data(file_list)

    formatted_data  = format_data(data, with_crf)

    save_csv_file(formatted_data, save_name)
    create_final_bargraph(formatted_data, title, save_name, with_crf)
    
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

    vn_bklg = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "individual_backlog\\visual_narrator\\dataset_csv_input_visual_narrator\\" +data_type + "_csv_results\\visual_narrator_individual_backlog_average.csv"
    chatgpt_bklg = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "individual_backlog\\chatgpt\\dataset_csv_input_chatgpt\\" +data_type + "_csv_results\\chatgpt_individual_backlog_average.csv"
    vn_cat = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "categories\\visual_narrator\\dataset_csv_input_visual_narrator\\" +data_type + "_csv_results\\visual_narrator_categories_average.csv"
    chatgpt_cat = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "categories\\chatgpt\\dataset_csv_input_chatgpt\\" +data_type + "_csv_results\\chatgpt_categories_average.csv"
    vn_glo = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "global\\visual_narrator\\dataset_csv_input_visual_narrator\\" +data_type + "_csv_results\\visual_narrator_global_average.csv"
    chatgpt_glo = "final_results\\individual_nlp_results\\total_results\\" + crf_path + "global\\chatgpt\\dataset_csv_input_chatgpt\\" +data_type + "_csv_results\\chatgpt_global_average.csv"

    file_list = [vn_bklg, chatgpt_bklg, vn_cat, chatgpt_cat, vn_glo, chatgpt_glo]

    if with_crf:
        crf_bklg = "final_results\\individual_nlp_results\\total_results\\with_crf\\individual_backlog\\crf\\dataset_csv_input_crf\\" + data_type + "_csv_results\\crf_individual_backlog_average.csv"
        crf_cat = "final_results\\individual_nlp_results\\total_results\\with_crf\\categories\\crf\\dataset_csv_input_crf\\" + data_type + "_csv_results\\crf_categories_average.csv"
        crf_glo = "final_results\\individual_nlp_results\\total_results\\with_crf\\global\\crf\\dataset_csv_input_crf\\" + data_type + "_csv_results\\crf_global_average.csv"
        file_list.append(crf_bklg)
        file_list.append(crf_cat)
        file_list.append(crf_glo)

    return file_list

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

def format_data(data, with_crf):
    '''
    formats the data so that it can be easily plotted onto the graphs

    Parameters:
    data(3D list): the final data results to be graphed
    with_crf (bool): use crf results in graphs

    Returns:
    formatted_data (list): contains the formatted data to graph
    '''
    if with_crf:
        vn_bklg, chatgpt_bklg, vn_cat, chatgpt_cat, vn_glo, chatgpt_glo, crf_bklg, crf_cat, crf_glo = data
        
        strict_bklg_data, inclusion_bklg_data, relaxed_bklg_data = organize_data_with_crf( vn_bklg, chatgpt_bklg, crf_bklg)
        strict_cat_data, inclusion_cat_data, relaxed_cat_data = organize_data_with_crf( vn_cat, chatgpt_cat, crf_cat)
        strict_glo_data, inclusion_glo_data, relaxed_glo_data = organize_data_with_crf( vn_glo, chatgpt_glo, crf_glo)
    else:
        vn_bklg, chatgpt_bklg,  vn_cat, chatgpt_cat,  vn_glo, chatgpt_glo = data
        
        strict_bklg_data, inclusion_bklg_data, relaxed_bklg_data = organize_data_without_crf(vn_bklg, chatgpt_bklg)
        strict_cat_data, inclusion_cat_data, relaxed_cat_data = organize_data_without_crf(vn_cat, chatgpt_cat)
        strict_glo_data, inclusion_glo_data, relaxed_glo_data = organize_data_without_crf(vn_glo, chatgpt_glo)
    
    formatted_data = [strict_bklg_data, inclusion_bklg_data, relaxed_bklg_data, strict_cat_data, inclusion_cat_data, relaxed_cat_data,strict_glo_data, inclusion_glo_data, relaxed_glo_data]

    return formatted_data

def organize_data_with_crf(vn_bklg, chatgpt, crf):
    vn_average, vn_sd, vn_label = vn_bklg
    chatgpt_average, chatgpt_sd, chatgpt_label = chatgpt
    crf_average, crf_sd, crf_label = crf
    
    row_data = []

    for i in range(27):
        row_data.append([ vn_average[i], chatgpt_average[i], crf_average[i],  vn_sd[i], chatgpt_sd[i], crf_sd[i]])

    for i in range (0,27,9):
        if  vn_label[i] == "Strict Comparison" and chatgpt_label[i] == "Strict Comparison" and crf_label[i] == "Strict Comparison":
            strict_data = pd.DataFrame([row_data[i+2],row_data[i+5],row_data[i+8]] , columns= ["Visual Narrator", "ChatGPT" "CRF", "Visual Narrator SD", "ChatGPT SD", "CRF SD"], index= ["Persona", "Entity", "Action"])
        elif vn_label[i] == "Inclusion Comparison"and chatgpt_label[i] == "Inclusion Comparison" and crf_label[i] == "Inclusion Comparison":
            inclusion_data = pd.DataFrame([row_data[i+2],row_data[i+5],row_data[i+8]] , columns= [ "Visual Narrator", "ChatGPT", "CRF", "Visual Narrator SD", "ChatGPT SD", "CRF SD"], index= ["Persona", "Entity", "Action"])
        elif vn_label[i] == "Relaxed Comparison" and chatgpt_label[i] == "Relaxed Comparison" and crf_label[i] == "Relaxed Comparison":
            relaxed_data = pd.DataFrame([row_data[i+2],row_data[i+5],row_data[i+8]] , columns= ["Visual Narrator", "ChatpGPT", "CRF", "Visual Narrator SD","ChatGPT SD", "CRF SD"], index= ["Persona", "Entity", "Action"])
        else:
            sys.tracebacklimit = 0
            raise Exception ("Invalid data matching across files. Ensure that the comparison mode matches across each file")

    return strict_data, inclusion_data, relaxed_data
def organize_data_without_crf(vn_bklg, chatgpt):
    vn_average, vn_sd, vn_label = vn_bklg
    chatgpt_average, chatgpt_sd, chatgpt_label = chatgpt
    
    row_data = []

    for i in range(27):
        row_data.append([vn_average[i], chatgpt_average[i], vn_sd[i], chatgpt_sd[i]])

    for i in range (0,27,9):
        if vn_label[i] == "Strict Comparison" and chatgpt_label[i] == "Strict Comparison":
            strict_data = pd.DataFrame([row_data[i+2],row_data[i+5],row_data[i+8]] , columns= [ "Visual Narrator", "ChatGPT", "Visual Narrator SD", "ChatGPT SD"], index= ["Persona", "Entity", "Action"])
        elif vn_label[i] == "Inclusion Comparison" and chatgpt_label[i] == "Strict Comparison":
            inclusion_data = pd.DataFrame([row_data[i+2],row_data[i+5],row_data[i+8]] , columns= ["Visual Narrator", "ChatGPT","Visual Narrator SD", "ChatGPT SD"], index= ["Persona", "Entity", "Action"])
        elif vn_label[i] == "Relaxed Comparison" and chatgpt_label[i] == "Relaxed Comparison":
            relaxed_data = pd.DataFrame([row_data[i+2],row_data[i+5],row_data[i+8]] , columns= ["Visual Narrator", "ChatGPT", "Visual Narrator SD", "ChatGPT SD"], index= ["Persona", "Entity", "Action"])
        else:
            sys.tracebacklimit = 0
            raise Exception ("Invalid data matching across files. Ensure that the comparison mode matches across each file")

    return strict_data, inclusion_data, relaxed_data

def save_csv_file(formatted_data, save_name):
    '''
    will save all the final results into one csv file

    Parameters:
    formatted_data (list): contains all the final information
    save_name (str): name of the saving file
    ''' 
    final_data = pd.concat(formatted_data)
    comparison_mode = (["Strict"] * 3 + ["Inclusion"] * 3 + ["Relaxed"] * 3) * 3
    data_groupings = ["Individual Backlog"] * 9 + ["Categories"] * 9 + ["Global"] * 9

    final_data["Comparison Mode"] = comparison_mode
    final_data["Data Groupings"] = data_groupings

    saving_path = "final_results\\comparing_nlps_results\\average_results\\combined_results\\final_data\\" + save_name + ".csv"

    final_data.to_csv(saving_path)

def create_final_bargraph(formatted_data, title, save_name, with_crf):
    
    strict_bklg_data, inclusion_bklg_data, relaxed_bklg_data, strict_cat_data, inclusion_cat_data, relaxed_cat_data,strict_glo_data, inclusion_glo_data, relaxed_glo_data = formatted_data

    if with_crf:
        standard_deviation = ["Visual Narrator SD", "ChatGPT SD" "CRF SD"]
        y_data = ["Visual Narrator", "ChatGPT", "CRF"]
        palette = [plt.cm.Pastel1(0), plt.cm.Pastel1(1), plt.cm.Pastel1(2)]
    else:
        standard_deviation = ["Visual Narrator SD", "ChatGPT SD"]
        y_data = ["Visual Narrator", "ChatGPT"]
        palette = [plt.cm.Pastel1(0), plt.cm.Pastel1(1)]

    graph, position = plt.subplots(3, 3, figsize=(10, 5))

    #Top Left
    yerr = fix_max_y_error(strict_bklg_data[standard_deviation], strict_bklg_data[y_data])
    strict_bklg_data[y_data].plot(ax = position[0,0], kind='bar', yerr = yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 4, ecolor='k'), figsize=(17,7), color = palette)
    position[0,0].set_title("Strict Comparison", fontsize = 14)
    position[0,0].set_ylabel("Individual Backlog", fontsize = 14)
    position[0,0].tick_params(labelrotation = 0)
    position[0,0].get_legend().remove()
    position[0,0].set_ylim([0, 1])
    position[0,0].set_xticks([])

    #Middle Left
    yerr = fix_max_y_error(strict_cat_data[standard_deviation], strict_cat_data[y_data])
    strict_cat_data[y_data].plot(ax = position[1,0], kind='bar', yerr = yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 4, ecolor='k'), figsize=(17,7), color = palette)
    position[1,0].set_ylabel("Categories", fontsize = 14)
    position[1,0].tick_params(labelrotation = 0)
    position[1,0].get_legend().remove()
    position[1,0].set_ylim([0, 1])
    position[1,0].set_xticks([])

    #bottom Left
    yerr = fix_max_y_error(strict_glo_data[standard_deviation], strict_glo_data[y_data])
    strict_glo_data[y_data].plot(ax = position[2,0], kind='bar', yerr = yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 4, ecolor='k'), figsize=(17,7), color = palette)
    position[2,0].set_ylabel("Global", fontsize = 14)
    position[2,0].tick_params(labelrotation = 0)
    position[2,0].get_legend().remove()
    position[2,0].set_ylim([0, 1])

    #Top center
    yerr = fix_max_y_error(inclusion_bklg_data[standard_deviation], inclusion_bklg_data[y_data])
    inclusion_bklg_data[y_data].plot(ax = position[0,1], kind='bar', yerr = yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 4, ecolor='k'), figsize=(17,7), color = palette)
    position[0,1].set_title("Inclusion Comparison", fontsize = 14)
    position[0,1].tick_params(labelrotation = 0)
    position[0,1].get_legend().remove()
    position[0,1].set_ylim([0, 1])
    position[0,1].set_xticks([])

    #Center
    yerr = fix_max_y_error(inclusion_cat_data[standard_deviation], inclusion_cat_data[y_data])
    inclusion_cat_data[y_data].plot(ax = position[1,1], kind='bar', yerr = yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 4, ecolor='k'), figsize=(17,7), color = palette)
    position[1,1].tick_params(labelrotation = 0)
    position[1,1].get_legend().remove()
    position[1,1].set_ylim([0, 1])
    position[1,1].set_xticks([])

    #bottom center
    yerr = fix_max_y_error(inclusion_glo_data[standard_deviation], inclusion_glo_data[y_data])
    inclusion_glo_data[y_data].plot(ax = position[2,1], kind='bar', yerr = yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 4, ecolor='k'), figsize=(17,7), color = palette)
    position[2,1].tick_params(labelrotation = 0)
    position[2,1].get_legend().remove()
    position[2,1].set_ylim([0, 1])

    #Top right
    yerr = fix_max_y_error(relaxed_bklg_data[standard_deviation], relaxed_bklg_data[y_data])
    relaxed_bklg_data[y_data].plot(ax = position[0,2], kind='bar', yerr = yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 4, ecolor='k'), figsize=(17,7), color = palette)
    position[0,2].set_title("Relaxed Comparison", fontsize = 14)
    position[0,2].tick_params(labelrotation = 0)
    position[0,2].get_legend().remove()
    position[0,2].set_ylim([0, 1])
    position[0,2].set_xticks([])

    #middle right
    yerr = fix_max_y_error(relaxed_cat_data[standard_deviation], relaxed_cat_data[y_data])
    relaxed_cat_data[y_data].plot(ax = position[1,2], kind='bar', yerr = yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 4, ecolor='k'), figsize=(17,7), color = palette)
    position[1,2].tick_params(labelrotation = 0)
    position[1,2].get_legend().remove()
    position[1,2].set_ylim([0, 1])
    position[1,2].set_xticks([])
    position[1,2].legend(loc=(1.025,0.25))

    #bottom right
    yerr = fix_max_y_error(relaxed_glo_data[standard_deviation], relaxed_glo_data[y_data])
    relaxed_glo_data[y_data].plot(ax = position[2,2], kind='bar', yerr = yerr, error_kw=dict(lw = 1.5, capthick = 2, capsize = 4, ecolor='k'), figsize=(17,7), color = palette)
    position[2,2].tick_params(labelrotation = 0)
    position[2,2].get_legend().remove()
    position[2,2].set_ylim([0, 1])

    graph.suptitle(title, fontsize = 20)
    graph.supxlabel("Label Type", fontsize=14)
    graph.supylabel("F-Measure", x = 0.01, y = 0.5, fontsize = 14)
    
    plt.tight_layout()

    saving_path = "final_results\\comparing_nlps_results\\average_results\\combined_results\\graphs\\" + save_name + ".png"

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