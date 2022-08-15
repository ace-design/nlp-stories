import argparse
import subprocess

def main():
    grouping_code, with_crf = command()
    datasets, grouping, crf_path, is_crf, nlp, nlp_code, nlp_file_name, file_type = get_info(grouping_code, with_crf)

    for i in range(len(nlp)):
        crf_intersecting_set(grouping, grouping_code, datasets, nlp[i], nlp_code[i], nlp_file_name[i], crf_path, is_crf, file_type)

def command():
    '''
    runs the command line prompt

    Returns:
    args.data_type (str): evaluation by individual backlogs - BKLG, categorized backlogs - CAT, or global - GLO
    args.with_crf_intersection (bool): True if dataset contains the crf intersecting set 
    '''

    parser = argparse.ArgumentParser(description = "This program is to get all the intersecting outputs")
    parser.add_argument("data_type", type = str, choices=["BKLG", "CAT", "GLO"], help = "evaluation by individual backlogs - BKLG, categorized backlogs - CAT, or global - GLO")
    parser.add_argument('--with_crf_intersection', default = False, action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    return args.data_type, args.with_crf_intersection

def get_info(grouping_code, with_crf):
    '''
    get relevant information to run the scripts

    Parameters:
    grouping_code (str): evaluation by individual backlogs - BKLG, categorized backlogs - CAT, or global - GLO
    with_crf (bool): True if dataset contains the crf intersecting set 
    
    Returns:
    datasets (list): groupings of the dataset
    grouping (str): grouping type  
    crf_path (str): path of of file depending if it contains crf intersecting set
    is_crf (str): command to indicate if crf intersecting set is included
    nlp (list): the nlp tools in the comparison
    nlp_code (list): nlp code names corresponding to the nlp list
    nlp_file_name (lst): contains the file names endings for the different nlp output files
    file_type (str): file type
    '''

    if grouping_code == "BKLG":
        datasets = ["g02", "g03", "g04", "g05", "g08", "g10", "g11", "g12", "g13", "g14", "g17", "g18", "g19", "g21", "g22", "g23", "g24", "g25", "g26", "g27", "g28"]
        grouping = "individual_backlog"
    elif grouping_code == "CAT":
        datasets = ["content_management", "dev", "iot", "management_app", "reporting", "web"]
        grouping = "categories"
    else:
        datasets = ["global"]
        grouping = "global"

    if with_crf:
        crf_path = "\\crf_input\\testing_input\\"
        is_crf = " --crf_intersecting_set "
        nlp = ["crf", "ecmfa_vn", "simple_nlp", "visual_narrator", "pos_baseline"]
        nlp_code = ["CRF", "ECMFA", "SIMPLE", "VN", "BASE"]
        nlp_file_name = ["", "_ecmfa_vn", "_simple_nlp", "_visual_narrator", "_baseline_pos"]
        file_type = ".json "
    else:
        crf_path = "\\intersecting_stories\\"
        is_crf = " "
        nlp = ["ecmfa_vn", "simple_nlp", "visual_narrator", "pos_baseline"]
        nlp_code = ["ECMFA", "SIMPLE", "VN", "BASE"]
        nlp_file_name = ["_ecmfa_vn", "_simple_nlp", "_visual_narrator", "_baseline_pos"]
        file_type = ".txt "

    return datasets, grouping, crf_path, is_crf, nlp, nlp_code, nlp_file_name, file_type

def crf_intersecting_set(grouping, group_code, datasets, nlp, nlp_code, nlp_file_name, crf_path, is_crf, file_type):

    print("Starting " + nlp + " intersecting conversions")

    for dataset in datasets:
        line = "python .\setup_data\convert_to_intersecting_stories.py nlp\\nlp_outputs\\"+ grouping + "\\nlp_outputs_original\\" + nlp + "\\" + dataset + nlp_file_name + ".json "+\
            "inputs\\"+ grouping + crf_path + dataset + file_type + dataset + " " + nlp_code + is_crf  + group_code 
        
        subprocess.run(line)

    print("Finished " + nlp + " intersecting conversions\n")

if __name__ == "__main__":
    main()