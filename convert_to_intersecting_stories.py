#This script will convert nlp_outputs to only include the stories that were identified to be intersecting
import argparse
import sys


def main():
    nlp_results_path, intersecting_path, save_file_path = command()




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
        load_file = open(args.load_path)
        load_file.close()
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        if args.nlp_type == "VN":
            save_file_path = "nlp_outputs_intersecting\\visual_narrator\\" + args.save_name + "_intersecting.json"
        elif args.nlp_type == "BASE":
            save_file_path = "nlp_outputs_intersecting\\pos_baseline\\" + args.save_name + "_intersecting.json"
        elif args.nlp_type == "SIMPLE":
            save_file_path = "nlp_outputs_intersecting\\simple\\" + args.save_name + "_intersecting.json"
        else:
            save_file_path = "nlp_outputs_intersecting\\fabian\\" + args.save_name + "_intersecting.json"
        
        return args.load_nlp_output_path, args.load_intersecting_path, save_file_path

if __name__ == "__main__":
    main()