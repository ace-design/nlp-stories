#will merge data from files into the first file that was given

import argparse
import json
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

        all_data = all_data + merge_data

        save_file_txt(all_path, all_data)
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
    parser.add_argument("load_all_path", type = str, help = "file path to the file with all the data")
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

def save_file_txt(path, data):
    '''
    save the results into txt file

    Parameters:
        path (str): path of file to be saved
        data (list): info to be saved onto file
    '''
    with open(path,"w", encoding="utf-8") as file:
        file.writelines(data)
    print("File is saved")

if __name__ == "__main__":
    main()