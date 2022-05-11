import argparse
import subprocess
import sys

def main():
    data = extract_visual_Narrator()
    print(data)

def extract_visual_Narrator():
    '''
    Run the visual narrator with given input file

    Returns:
    data (str): output from the command window

    '''
    
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type = str, help = "path to file of evaluation")
    args = parser.parse_args()

    try:
        load_file = open(args.path)
        load_file.close()
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else: 
        command = subprocess.run("python visual_narrator_extraction\\run.py " + args.path + " -u", capture_output = True)
        data = command.stdout.decode()
        return data

if __name__ == "__main__":
    main()
