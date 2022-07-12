#This script will convert nlp_outputs to only include the stories that were identified to be intersecting
import argparse
import json
import sys


def main():
    nlp_results_path, intersecting_path, save_file_path = command()

    intersecting_data = get_intersecting_data(nlp_results_path, intersecting_path)

    save_results(intersecting_data, save_file_path)


def command():
    '''
    This will take the inputs from the command line

    args.load_path (str): Path to the file to be loaded
        args.save_name (str): name of the file to save results

    Raises:
        FileNotFoundError: raises excpetion
        wrong file type: raises exception
    '''

    parser = argparse.ArgumentParser(description = "This program is to cconvert nlp outputs to only contain results from the intersecting stories")
    parser.add_argument("load_nlp_output_path", type = str, help = "path of file that contains the nlp outputs")
    parser.add_argument("load_intersecting_path", type = str, help = "path of file that contains the intersecting stories")
    parser.add_argument("save_name", type = str, help = "name of file to save")
    parser.add_argument('nlp_type', type = str, choices=["VN", "BASE", "FABIAN", "SIMPLE"], help = "choose from VN - visual narrator, BASE - baseline, FABIAN - fabian, SIMPLE - simple nlp to identify which nlp was used for the current results being converted")
    
    args = parser.parse_args()

    try:
        load_file = open(args.load_nlp_output_path)
        load_file.close()
        load_file = open(args.load_intersecting_path)
        load_file.close()
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        if args.nlp_type == "VN":
            save_file_path = "nlp_outputs_intersecting\\visual_narrator\\" + args.save_name + "_visual_narrator_intersecting.json"
        elif args.nlp_type == "BASE":
            save_file_path = "nlp_outputs_intersecting\\pos_baseline\\" + args.save_name + "_baseline_intersecting.json"
        elif args.nlp_type == "SIMPLE":
            save_file_path = "nlp_outputs_intersecting\\simple\\" + args.save_name + "_simple_intersecting.json"
        else:
            save_file_path = "nlp_outputs_intersecting\\fabian\\" + args.save_name + "_fabian_intersecting.json"
        
        return args.load_nlp_output_path, args.load_intersecting_path, save_file_path

def get_intersecting_data(nlp_results_path, intersecting_path):
    '''
    will get the results of the stories that were indentifies as intersecting. 

    Parameters:
    nlp_results_path (str): path to the file that contains the nlp annotated results
    intersecting_path (str): path to the file that contains the stories that are intersecting

    Returns:
    intersecting_data (list): the annotations results of only the intersecting stories
    '''

    intersecting_text = []
    intersecting_data = []
    passed_text = []

    
    nlp_file = open(nlp_results_path, encoding= "UTF-8")
    nlp_data = json.load(nlp_file) 
    nlp_file.close()

    with open(intersecting_path, encoding= "utf-8") as intersecting_file:
        read_data = intersecting_file.readlines()

    for story in read_data:
        intersecting_text.append(story.strip(" \n\t"))

    for i in range(len(nlp_data)):
        nlp_text = nlp_data[i]["Text"].strip(" \n\t") 
        if nlp_text in intersecting_text and not(nlp_text in passed_text):
                intersecting_data.append(nlp_data[i])
                passed_text.append(nlp_text)

    if len(intersecting_text) != len(intersecting_data):
        print("ERROR: THERE ARE MISSING DATA IN THE FILE.\n")
        difference = list(set(intersecting_text) - set(passed_text))
        print(difference)

    return intersecting_data
    
def save_results(intersecting_data, save_file_path):
    '''
    save the intersecting stories results

    Parameters:
    intersecting_data (list): the annotations results of only the intersecting stories
    save_file_path (str): path to save the file
    '''
    with open(save_file_path,"w", encoding="utf-8") as file:
        json.dump(intersecting_data, file, ensure_ascii=False, indent = 4)
    print("File is saved")


if __name__ == "__main__":
    main()