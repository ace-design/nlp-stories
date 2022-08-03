#This script will combine the final results grpahs of benchmark into one graph

import argparse
import matplotlib.pyplot as plt
import pandas as pd
import sys

def main():
    with_crf, primary, save_name, title= command()

    file_list = identify_files(with_crf, primary)


    data = extract_data(file_list)

    formatted_data  = format_data(data, with_crf)

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
    parser.add_argument('--with_crf', default = False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--primary', default = False, action=argparse.BooleanOptionalAction)
    parser.add_argument("save_file_name", type = str, help = "name of file to save")
    parser.add_argument("title", type = str, help = "title of graph")

    args = parser.parse_args()


    return args.with_crf, args.primary, args.save_file_name, args.title

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

    ecmfa_vn_bklg = "final_results\\individual_nlp_results\\total_results\\individual_backlog\\ecmfa_vn\\dataset_csv_input_ecmfa_vn\\" + data_type + "_csv_results\\ecmfa_vn_individual_backlog_average.csv"
    simple_bklg = "final_results\\individual_nlp_results\\total_results\\individual_backlog\\simple\\dataset_csv_input_simple\\" + data_type + "_csv_results\\simple_individual_backlog_average.csv"
    vn_bklg = "final_results\\individual_nlp_results\\total_results\\individual_backlog\\visual_narrator\\dataset_csv_input_visual_narrator\\" +data_type + "_csv_results\\visual_narrator_individual_backlog_average.csv"
    ecmfa_vn_cat = "final_results\\individual_nlp_results\\total_results\\categories\\ecmfa_vn\\dataset_csv_input_ecmfa_vn\\" + data_type + "_csv_results\\ecmfa_vn_categories_average.csv"
    simple_cat = "final_results\\individual_nlp_results\\total_results\\categories\\simple\\dataset_csv_input_simple\\" + data_type + "_csv_results\\simple_categories_average.csv"
    vn_cat = "final_results\\individual_nlp_results\\total_results\\categories\\visual_narrator\\dataset_csv_input_visual_narrator\\" +data_type + "_csv_results\\visual_narrator_categories_average.csv"
    ecmfa_vn_glo = "final_results\\individual_nlp_results\\total_results\\global\\ecmfa_vn\\dataset_csv_input_ecmfa_vn\\" + data_type + "_csv_results\\ecmfa_vn_global_average.csv"
    simple_glo = "final_results\\individual_nlp_results\\total_results\\global\\simple\\dataset_csv_input_simple\\" + data_type + "_csv_results\\simple_global_average.csv"
    vn_glo = "final_results\\individual_nlp_results\\total_results\\global\\visual_narrator\\dataset_csv_input_visual_narrator\\" +data_type + "_csv_results\\visual_narrator_global_average.csv"

    file_list = [ecmfa_vn_bklg, simple_bklg, vn_bklg, ecmfa_vn_cat, simple_cat, vn_cat, ecmfa_vn_glo, simple_glo, vn_glo]

    if with_crf:
        crf_bklg = "final_results\\individual_nlp_results\\total_results\\individual_backlog\\crf\\dataset_csv_input_crf\\" + data_type + "_csv_results\\crf_individual_backlog_average.csv"
        crf_cat = "final_results\\individual_nlp_results\\total_results\\categories\\crf\\dataset_csv_input_crf\\" + data_type + "_csv_results\\crf_categories_average.csv"
        crf_glo = "final_results\\individual_nlp_results\\total_results\\global\\crf\\dataset_csv_input_crf\\" + data_type + "_csv_results\\crf_global_average.csv"
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
    formatted_data (3D-list): contains the formatted data to graph
    '''
    if with_crf:
        ecmfa_vn_bklg, simple_bklg, vn_bklg, ecmfa_vn_cat, simple_cat, vn_cat, ecmfa_vn_glo, simple_glo, vn_glo, crf_bklg, crf_cat, crf_glo = data
        
        strict_bklg_data, inclusion_bklg_data, relaxed_bklg_data = organize_data_with_crf(ecmfa_vn_bklg, simple_bklg, vn_bklg, crf_bklg)
        strict_cat_data, inclusion_cat_data, relaxed_cat_data = organize_data_with_crf(ecmfa_vn_cat, simple_cat, vn_cat, crf_cat)
        strict_glo_data, inclusion_glo_data, relaxed_glo_data = organize_data_with_crf(ecmfa_vn_glo, simple_glo, vn_glo, crf_glo)
    else:
        ecmfa_vn_bklg, simple_bklg, vn_bklg, ecmfa_vn_cat, simple_cat, vn_cat, ecmfa_vn_glo, simple_glo, vn_glo= data
        
        strict_bklg_data, inclusion_bklg_data, relaxed_bklg_data = organize_data_without_crf(ecmfa_vn_bklg, simple_bklg, vn_bklg)
        strict_cat_data, inclusion_cat_data, relaxed_cat_data = organize_data_without_crf(ecmfa_vn_cat, simple_cat, vn_cat)
        strict_glo_data, inclusion_glo_data, relaxed_glo_data = organize_data_without_crf(ecmfa_vn_glo, simple_glo, vn_glo)
    
    formatted_data = [strict_bklg_data, inclusion_bklg_data, relaxed_bklg_data, strict_cat_data, inclusion_cat_data, relaxed_cat_data,strict_glo_data, inclusion_glo_data, relaxed_glo_data]

    return formatted_data

def organize_data_with_crf(ecmfa, simple, bklg, crf):
    
    ecmfa_vn_average, ecmfa_vn_sd, ecmfa_vn_label = ecmfa
    simple_average, simple_sd, simple_label = simple
    vn_average, vn_sd, vn_label = bklg
    crf_average, crf_sd, crf_label = crf
    
    row_data = []

    for i in range(27):
        row_data.append([ecmfa_vn_average[i], simple_average[i], vn_average[i], crf_average[i], ecmfa_vn_sd[i], simple_sd[i], vn_sd[i], crf_sd[i]])

    for i in range (0,27,9):
        if ecmfa_vn_label[i] == "Strict Comparison" and simple_label[i] == "Strict Comparison" and vn_label[i] == "Strict Comparison" and crf_label[i] == "Strict Comparison":
            strict_data = pd.DataFrame([row_data[i+2],row_data[i+5],row_data[i+8]] , columns= ["Simple","ECMFA-VN", "Visual Narrator", "CRF", "Simple SD","ECMFA-VN SD","Visual Narrator SD", "CRF SD"], index= ["Persona F-Measure", "Entity F-Measure", "Action F-Measure"])
        elif ecmfa_vn_label[i] == "Inclusion Comparison" and simple_label[i] == "Inclusion Comparison" and vn_label[i] == "Inclusion Comparison"and crf_label[i] == "Inclusion Comparison":
            inclusion_data = pd.DataFrame([row_data[i+2],row_data[i+5],row_data[i+8]] , columns= ["Simple","ECMFA-VN", "Visual Narrator", "CRF", "Simple SD","ECMFA-VN SD","Visual Narrator SD", "CRF SD"], index= ["Persona F-Measure", "Entity F-Measure", "Action F-Measure"])
        elif ecmfa_vn_label[i] == "Relaxed Comparison" and simple_label[i] == "Relaxed Comparison" and vn_label[i] == "Relaxed Comparison"and crf_label[i] == "Relaxed Comparison":
            relaxed_data = pd.DataFrame([row_data[i+2],row_data[i+5],row_data[i+8]] , columns= ["Simple","ECMFA-VN", "Visual Narrator", "CRF", "Simple SD","ECMFA-VN SD","Visual Narrator SD", "CRF SD"], index= ["Persona F-Measure", "Entity F-Measure", "Action F-Measure"])
        else:
            sys.tracebacklimit = 0
            raise Exception ("Invalid data matching across files. Ensure that the comparison mode matches across each file")

    return strict_data, inclusion_data, relaxed_data
def organize_data_without_crf(ecmfa, simple, bklg):
    
    ecmfa_vn_average, ecmfa_vn_sd, ecmfa_vn_label = ecmfa
    simple_average, simple_sd, simple_label = simple
    vn_average, vn_sd, vn_label = bklg
    
    row_data = []

    for i in range(27):
        row_data.append([ecmfa_vn_average[i], simple_average[i], vn_average[i],ecmfa_vn_sd[i], simple_sd[i], vn_sd[i]])

    for i in range (0,27,9):
        if ecmfa_vn_label[i] == "Strict Comparison" and simple_label[i] == "Strict Comparison" and vn_label[i] == "Strict Comparison":
            strict_data = pd.DataFrame([row_data[i+2],row_data[i+5],row_data[i+8]] , columns= ["Simple","ECMFA-VN", "Visual Narrator","Simple SD","ECMFA-VN SD","Visual Narrator SD"], index= ["Persona F-Measure", "Entity F-Measure", "Action F-Measure"])
        elif ecmfa_vn_label[i] == "Inclusion Comparison" and simple_label[i] == "Inclusion Comparison" and vn_label[i] == "Inclusion Comparison":
            inclusion_data = pd.DataFrame([row_data[i+2],row_data[i+5],row_data[i+8]] , columns= ["Simple","ECMFA-VN", "Visual Narrator","Simple SD","ECMFA-VN SD","Visual Narrator SD"], index= ["Persona F-Measure", "Entity F-Measure", "Action F-Measure"])
        elif ecmfa_vn_label[i] == "Relaxed Comparison" and simple_label[i] == "Relaxed Comparison" and vn_label[i] == "Relaxed Comparison":
            relaxed_data = pd.DataFrame([row_data[i+2],row_data[i+5],row_data[i+8]] , columns= ["Simple","ECMFA-VN", "Visual Narrator","Simple SD","ECMFA-VN SD","Visual Narrator SD"], index= ["Persona F-Measure", "Entity F-Measure", "Action F-Measure"])
        else:
            sys.tracebacklimit = 0
            raise Exception ("Invalid data matching across files. Ensure that the comparison mode matches across each file")

    return strict_data, inclusion_data, relaxed_data

def create_final_bargraph(formatted_data, title, save_name, with_crf):
    
    strict_bklg_data, inclusion_bklg_data, relaxed_bklg_data, strict_cat_data, inclusion_cat_data, relaxed_cat_data,strict_glo_data, inclusion_glo_data, relaxed_glo_data = formatted_data

    if with_crf:
        standard_deviation = ["Simple SD","ECMFA-VN SD","Visual Narrator SD", "CRF SD"]
        y_data = ["Simple","ECMFA-VN", "Visual Narrator", "CRF"]
        palette = ["#f29e8e", "indianred", "#9a0200","#4c0000"]
    else:
        standard_deviation = ["ECMFA-VN SD","Simple SD","Visual Narrator SD"]
        y_data = ["Simple","ECMFA-VN", "Visual Narrator"]
        palette = ["#f29e8e", "indianred", "#9a0200"]

    graph, position = plt.subplots(3, 3, figsize=(10, 5))

    #Top Left
    yerr = strict_bklg_data[standard_deviation].to_numpy().T
    strict_bklg_data[y_data].plot(ax = position[0,0], kind='bar', alpha = 0.85, yerr = yerr, error_kw=dict(lw = 1.5, capthick = 1, capsize = 5, ecolor='k'), figsize=(17,7), color = palette)
    position[0,0].set_title("Strict Comparison", fontsize = 14)
    position[0,0].set_ylabel("Individual Backlog", fontsize = 14)
    position[0,0].tick_params(labelrotation = 0)
    position[0,0].get_legend().remove()
    position[0,0].set_ylim([0, 1.1])
    position[0,0].set_xticks([])

    #Middle Left
    yerr = strict_cat_data[standard_deviation].to_numpy().T
    strict_cat_data[y_data].plot(ax = position[1,0], kind='bar', alpha = 0.85, yerr = yerr, error_kw=dict(lw = 1.5, capthick = 1, capsize = 5, ecolor='k'), figsize=(17,7), color = palette)
    position[1,0].set_ylabel("Categories", fontsize = 14)
    position[1,0].tick_params(labelrotation = 0)
    position[1,0].get_legend().remove()
    position[1,0].set_ylim([0, 1.1])
    position[1,0].set_xticks([])

    #bottom Left
    yerr = strict_glo_data[standard_deviation].to_numpy().T
    strict_glo_data[y_data].plot(ax = position[2,0], kind='bar', alpha = 0.85, yerr = yerr, error_kw=dict(lw = 1.5, capthick = 1, capsize = 5, ecolor='k'), figsize=(17,7), color = palette)
    position[2,0].set_ylabel("Global", fontsize = 14)
    position[2,0].tick_params(labelrotation = 0)
    position[2,0].get_legend().remove()
    position[2,0].set_ylim([0, 1.1])

    #Top center
    yerr = inclusion_bklg_data[standard_deviation].to_numpy().T
    inclusion_bklg_data[y_data].plot(ax = position[0,1], kind='bar', alpha = 0.85, yerr = yerr, error_kw=dict(lw = 1.5, capthick = 1, capsize = 5, ecolor='k'), figsize=(17,7), color = palette)
    position[0,1].set_title("Inclusion Comparison", fontsize = 14)
    position[0,1].tick_params(labelrotation = 0)
    position[0,1].get_legend().remove()
    position[0,1].set_ylim([0, 1.1])
    position[0,1].set_xticks([])

    #Center
    yerr = inclusion_cat_data[standard_deviation].to_numpy().T
    inclusion_cat_data[y_data].plot(ax = position[1,1], kind='bar', alpha = 0.85, yerr = yerr, error_kw=dict(lw = 1.5, capthick = 1, capsize = 5, ecolor='k'), figsize=(17,7), color = palette)
    position[1,1].tick_params(labelrotation = 0)
    position[1,1].get_legend().remove()
    position[1,1].set_ylim([0, 1.1])
    position[1,1].set_xticks([])

    #bottom center
    yerr = inclusion_glo_data[standard_deviation].to_numpy().T
    inclusion_glo_data[y_data].plot(ax = position[2,1], kind='bar', alpha = 0.85, yerr = yerr, error_kw=dict(lw = 1.5, capthick = 1, capsize = 5, ecolor='k'), figsize=(17,7), color = palette)
    position[2,1].tick_params(labelrotation = 0)
    position[2,1].get_legend().remove()
    position[2,1].set_ylim([0, 1.1])

    #Top right
    yerr = relaxed_bklg_data[standard_deviation].to_numpy().T
    relaxed_bklg_data[y_data].plot(ax = position[0,2], kind='bar', alpha = 0.85, yerr = yerr, error_kw=dict(lw = 1.5, capthick = 1, capsize = 5, ecolor='k'), figsize=(17,7), color = palette)
    position[0,2].set_title("Relaxed Comparison", fontsize = 14)
    position[0,2].tick_params(labelrotation = 0)
    position[0,2].get_legend().remove()
    position[0,2].set_ylim([0, 1.1])
    position[0,2].set_xticks([])

    #middle right
    yerr = relaxed_cat_data[standard_deviation].to_numpy().T
    relaxed_cat_data[y_data].plot(ax = position[1,2], kind='bar', alpha = 0.85, yerr = yerr, error_kw=dict(lw = 1.5, capthick = 1, capsize = 5, ecolor='k'), figsize=(17,7), color = palette)
    position[1,2].tick_params(labelrotation = 0)
    position[1,2].get_legend().remove()
    position[1,2].set_ylim([0, 1.1])
    position[1,2].set_xticks([])
    position[1,2].legend(loc=(1.025,0.25))

    #bottom right
    yerr = relaxed_glo_data[standard_deviation].to_numpy().T
    relaxed_glo_data[y_data].plot(ax = position[2,2], kind='bar', alpha = 0.85, yerr = yerr, error_kw=dict(lw = 1.5, capthick = 1, capsize = 5, ecolor='k'), figsize=(17,7), color = palette)
    position[2,2].tick_params(labelrotation = 0)
    position[2,2].get_legend().remove()
    position[2,2].set_ylim([0, 1.1])
    


 

    graph.suptitle(title, fontsize = 20)
    graph.supxlabel("Measurement Type", fontsize=14)
    

    plt.tight_layout()

    saving_path = "final_results\\comparing_nlps_results\\average_results\\combined_results\\" + save_name + ".png"

    plt.savefig(saving_path)

if __name__ == "__main__":
    main()