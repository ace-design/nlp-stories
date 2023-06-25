#will merge data from files into the first file that was given

import argparse
import csv
import json
import pandas as pd
import sys

def main():
    all_path, merge_path = command()

    if ".json" in all_path and ".json" in merge_path:
        all_data = extract_data_json(all_path)
        merge_data = extract_data_json(merge_path)
        all_data = all_data + merge_data

        save_file_json(all_path, all_data)
    elif ".txt" in all_path and ".txt" in merge_path:
        all_data = extract_data_txt(all_path)
        merge_data = extract_data_txt(merge_path)
        all_data.append(merge_data)

        save_file_txt(all_path, all_data)
    elif ".csv" in all_path and ".csv" in merge_path:
        all_data = extract_data_csv(all_path)
        merge_data = extract_data_csv(merge_path)

        save_file_csv(all_path, all_data, merge_data)
    else:
        sys.tracebacklimit = 0
        raise Exception ("incompatible files. Both file must either be json files or txt files.")

def command():
    '''
    gets info from the commandline input

    Returns:
    args.all_path (str): file path to the file with all the data
    args.merge_path (str): file path to the data to merge

    Raises:
        FileNotFoundError: raises excpetion
        wrong file type: raises exception
    '''
    parser = argparse.ArgumentParser(description = "This program will merge files into one file")
    parser.add_argument("load_all_path", type = str, help = "file path to the file with all the data(THIS IS THE FILE SAVING TO)")
    parser.add_argument("load_merge_path", type = str, help = "file path to the data to merge")
    
    args = parser.parse_args()

    try:
        load_file = open(args.load_all_path)
        load_file.close()
        load_file = open(args.load_merge_path)
        load_file.close()
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        return args.load_all_path, args.load_merge_path

def extract_data_json(path):
    '''
    extracts the data from the json file
    
    Parameters:
    path (str): path of file

    Returns:
    data (list): the data of each story in the file
    '''

    file = open(path, encoding= "utf-8")
    data = json.load(file)

    return data

def save_file_json(path, data):
    '''
    save the results into json file

    Parameters:
        path (str): path of file to be saved
        data (list): info to be saved onto file
    '''
    with open(path,"w", encoding="utf-8") as file:
        json.dump(data, file, indent = 4)
    print("File is saved")

def extract_data_txt(path):
    '''
    extracts the data from the txt file
    
    Parameters:
    path (str): path of file

    Returns:
    data (list): the data of each story in the file
    '''

    file = open(path, encoding= "utf-8")
    data = file.readlines()
    return data

def extract_data_csv(path):
    '''
    extracts the data from the csv file

    Parameters:
    path (str): path of file

    Returns:
    data (list): the data in the file
    '''
    extract = pd.read_csv(path) 

    label = extract["Measurement"].tolist()
    average = extract["Average"].tolist()
    standard_deviation = extract["Standard Deviation"].tolist()
    comparison = extract["Comparison Mode"].tolist()
    nlp_type = extract["nlp"].tolist()

    data = [label, average, standard_deviation, comparison, nlp_type]

    return data

def save_file_txt(path, data):
    '''
    save the results into txt file

    Parameters:
        path (str): path of file to be saved
        data (list): info to be saved onto file
    '''
    with open(path,"w", encoding="utf-8") as file:
        for story in data:
            file.writelines(story)
    print("File is saved")

def save_file_csv(path, all_data, merge_data):
    '''
    save the results into csv file

    Parameters:
        path (str): path of file to be saved
        all_data (list): info to be saved onto file
        merge_data (list): info to be saved onto file ontop of all_data
    '''
    all_label, all_average, all_standard_devation, all_comparison_mode, all_nlp_type = all_data
    merge_label, merge_average, merge_standard_devation, merge_comparison_mode, merge_nlp_type = merge_data

    all_label.extend(merge_label)
    all_average.extend(merge_average)
    all_standard_devation.extend(merge_standard_devation)
    all_comparison_mode.extend(merge_comparison_mode)
    all_nlp_type.extend(merge_nlp_type)

    all_label.insert(0, "Measurement")
    all_average.insert(0, "Average")
    all_standard_devation.insert(0, "Standard Deviation")
    all_comparison_mode.insert(0, "Comparison Mode")
    all_nlp_type.insert(0, "nlp")

    with open (path, "w", newline = "") as file:
        writer = csv.writer(file)
        for i in range (len(all_label)):
            row = all_label[i], all_average[i], all_standard_devation[i], all_comparison_mode[i], all_nlp_type[i]
            writer.writerow(row)

if __name__ == "__main__":
    main()