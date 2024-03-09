#This script will convert nlp_outputs to only include the stories that were identified to be intersecting
import argparse
import json
import sys


def main():
    nlp_results_path, intersecting_path, save_file_path, crf = command()

    if crf:
        intersecting_data = get_crf_intersecting_data(nlp_results_path, intersecting_path)
    else:
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

    parser = argparse.ArgumentParser(description = "This program is to convert nlp outputs to only contain results from the intersecting stories")
    parser.add_argument("load_nlp_results_path", type = str, help = "path of file that contains the nlp outputs results")
    parser.add_argument("load_intersecting_path", type = str, help = "path of file that contains the intersecting stories")
    parser.add_argument("save_name", type = str, help = "name of file to save")
    parser.add_argument('nlp_type', type = str, 
                        choices=["VN", "BASE", "ECMFA", "SIMPLE", "GPT_3_5_V0125", "GPT_3_5_V0613_2023", "GPT_3_5_V0613_2024", "GPT_4_TURBO_V0125", \
                                 "GPT_4_V0613", "CRF"], 
                        help = "choose from VN - visual narrator, BASE - baseline, ECMFA - ecmfa_vn, SIMPLE - simple, GPT_3_5_V0125 - GPT 3.5 V0125, \
                                GPT_3_5_V0613_2023- GPT3.5 V0613 2023, GPT_3_5_V0613_2024 - GPT3.5 V0613 2024, GPT_4_TURBO_V0125 - GPT 4 TURBO V0125, \
                                GPT_4_TURBO_V0125 - GPT 4 TURBO V0125, CRF - crf nlp to identify which nlp was used for the current results being \
                                converted")
    parser.add_argument("data_type", type = str, choices=["BKLG", "CAT", "GLO"], help = "evaluation by individual backlogs - BKLG, categorized backlogs - CAT, or global - GLO")
    parser.add_argument('--crf_intersecting_set', default = False, action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    try:
        load_file = open(args.load_nlp_results_path)
        load_file.close()
        load_file = open(args.load_intersecting_path)
        load_file.close()
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        if args.data_type == "BKLG":
            data_type_folder = "individual_backlog"
        elif args.data_type == "CAT":
            data_type_folder = "categories"
        else:
            data_type_folder = "global"

        if args.crf_intersecting_set:
            intersecting_type_folder = "\\nlp_outputs_intersecting_crf"
        else:
            intersecting_type_folder = "\\nlp_outputs_intersecting"

        if args.nlp_type == "VN":
            save_file_path = "nlp\\nlp_outputs\\" + data_type_folder + intersecting_type_folder + "\\visual_narrator\\" + args.save_name + "_visual_narrator_intersecting.json"
        elif args.nlp_type == "BASE":
            save_file_path = "nlp\\nlp_outputs\\" + data_type_folder + intersecting_type_folder + "\\pos_baseline\\" + args.save_name + "_baseline_intersecting_pos.json"
        elif args.nlp_type == "SIMPLE":
            save_file_path = "nlp\\nlp_outputs\\" + data_type_folder + intersecting_type_folder + "\\simple\\" + args.save_name + "_simple_intersecting.json"
        elif args.nlp_type == "ECMFA":
            save_file_path = "nlp\\nlp_outputs\\" + data_type_folder + intersecting_type_folder + "\\ecmfa_vn\\" + args.save_name + "_ecmfa_vn_intersecting.json"
        elif args.nlp_type == "GPT_3_5_V0125":
            save_file_path = "nlp\\nlp_outputs\\" + data_type_folder + intersecting_type_folder + "\\gpt_3_5_v0125\\" + args.save_name + "_gpt_3_5_v0125_intersecting.json"
        elif args.nlp_type == "GPT_3_5_V0613_2023":
            save_file_path = "nlp\\nlp_outputs\\" + data_type_folder + intersecting_type_folder + "\\gpt_3_5_v0613_2023\\" + args.save_name + "_gpt_3_5_v0613_2023_intersecting.json"
        elif args.nlp_type == "GPT_3_5_V0613_2024":
            save_file_path = "nlp\\nlp_outputs\\" + data_type_folder + intersecting_type_folder + "\\gpt_3_5_v0613_2024\\" + args.save_name + "_gpt_3_5_v0613_2024_intersecting.json"
        elif args.nlp_type == "GPT_4_TURBO_V0125":
            save_file_path = "nlp\\nlp_outputs\\" + data_type_folder + intersecting_type_folder + "\\gpt_4_turbo_v0125\\" + args.save_name + "_gpt_4_turbo_v0125_intersecting.json"
        elif args.nlp_type == "GPT_4_V0613":
            save_file_path = "nlp\\nlp_outputs\\" + data_type_folder + intersecting_type_folder + "\\gpt_4_v0613\\" + args.save_name + "_gpt_4_v0613_intersecting.json"
        elif args.nlp_type == "CRF":
            save_file_path = "nlp\\nlp_outputs\\" + data_type_folder + intersecting_type_folder + "\\crf\\" + args.save_name + "_crf_intersecting.json"
        
        return args.load_nlp_results_path, args.load_intersecting_path, save_file_path, args.crf_intersecting_set

def get_crf_intersecting_data(nlp_results_path, intersecting_path):
    '''
    will get the results of the stories that were indentifies as intersecting. 

    Parameters:
    nlp_results_path (str): path to the file that contains the nlp annotated results
    intersecting_path (str): path to the file that contains the stories that are intersecting

    Returns:
    intersecting_data (list): the annotations results of only the intersecting stories
    '''

    intersecting_text = []
    crf_info = []
    intersecting_data = []
    passed_text = []

    
    nlp_file = open(nlp_results_path, encoding= "UTF-8")
    nlp_data = json.load(nlp_file) 
    nlp_file.close()

    intersecting_file = open(intersecting_path, encoding= "UTF-8")
    crf_info = json.load(intersecting_file) 
    intersecting_file.close()

    for story_data in crf_info:
        intersecting_text.append(story_data["Text"].strip(" \n\t"))

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