#This script will run the files to convert a raw file from Doccano to pos baseline json file
import argparse
import subprocess


def main():
    path, save_name, group_code = command()
    run_sub_script(path, save_name, group_code)

def command():
    '''
    runs the command line prompt

    Returns:
    args.doccano_file_path (str): path to the Doccano output file
    args.save_name (str): name of the saving file
    args.data_type (str):  evaluation by individual backlogs - BKLG, categorized backlogs - CAT, or global - GLO
    '''

    parser = argparse.ArgumentParser(description = "This script will run the files to convert a raw file from Doccano to pos baseline json file")
    parser.add_argument("doccano_file_path", type = str, help = "path to the Doccano output file")
    parser.add_argument("save_name", type = str, help = "name of the saving file")
    parser.add_argument("data_type", type = str, choices=["BKLG", "CAT", "GLO"], help = "evaluation by individual backlogs - BKLG, categorized backlogs - CAT, or global - GLO")
    

    args = parser.parse_args()

    return args.doccano_file_path, args.save_name, args.data_type

def run_sub_script(path, save_name, group_code):
    '''
    run the existing scripts to convert Doccano output to pos baseline json 

    Parameters:
    path (str): path to the Doccano output file
    save_name (str): name of the saving file
    group_code (str): grouping code: evaluation by individual backlogs - BKLG, categorized backlogs - CAT, or global - GLO    
    '''

    line = "python setup_data\jsonl_to_human_readable.py " + path  + " " + save_name + " " + group_code
    print ("Starting jsonl_to_human_readable.py")
    subprocess.run(line)
    print ("Finished jsonl_to_human_readable.py")

    if group_code == "BKLG":
        grouping = "individual_backlog"
    elif group_code == "CAT":
        grouping = "categories"
    else:
        grouping = "global"


    baseline_path = "nlp\\nlp_outputs\\"+ grouping + "\\nlp_outputs_original\\baseline\\" + save_name + "_baseline.json"

    line = "python setup_data\create_pos_baseline.py " +baseline_path + " " + save_name + " " + group_code
    print ("\nStarting creating POS tags")
    subprocess.run(line)
    print ("Finished creating POS tags")

if __name__ == "__main__":
    main()