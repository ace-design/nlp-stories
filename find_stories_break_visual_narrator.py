import argparse
import subprocess
import sys

def main():
    load_path, save_name = command()
    valid_stories, invalid_stories = find_invalid(load_path)

    valid_save_path = "inputs\\valid_visual_narrator_stories\\" + save_name + ".txt"
    invalid_save_path = "logs\\invalid_visual_narrator_stories\\" + save_name + ".txt"

    save_results(valid_save_path, valid_stories)
    save_results(invalid_save_path, invalid_stories)

    print("Completed")

def command():
    '''
    Runs the command line inputs

    Returns:
        args.load_path (str): Path to the text file to be loaded
        args.save_name (str): name to the saving file

    Raises:
        FileNotFoundError: raises excpetion
        wrong file type: raises exception
    '''
    parser = argparse.ArgumentParser(description = "This program is to get POS tags of the elements of the annotations")
    parser.add_argument("load_path", type = str, help = "path of input text file")
    parser.add_argument("save_name", type = str, help = "name of the file save the results")
    
    args = parser.parse_args()

    if not(args.load_path.endswith(".txt")):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect input file type. input file type is .txt")

    try:
        load_file = open(args.load_path)
        load_file.close()
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        return args.load_path, args.save_name

def find_invalid(load_path):
    '''
    Find stories within the database that when run through visual narrator, causes an Index Error

    Parameters:
    load_path (str): path of the text file of the stories to check if visual narrator can evaluate them 

    Returns:
    valid_stories (list): contains all the story that visual narrator can evaluate
    invalid_stories (list): contains all the story that visual narrator can not evaluate
    '''

    valid_stories = []
    invalid_stories = []
    temp_path = "visual_narrator_extraction\\story_test.txt"

    with open(load_path, "r") as file:
        stories = file.readlines()

    for i in range(len(stories)):
        try:
            story = stories[i]
            with open(temp_path, "w") as file:
                file.write(story)
            command = subprocess.check_output("python visual_narrator\\run.py visual_narrator_extraction\\story_test.txt -u")
        except:
            sys.tracebacklimit = 0 
            invalid_stories.append(stories[i])
        else:
            valid_stories.append(stories[i])

    return valid_stories, invalid_stories

def save_results(save_path, data):
    '''
    save the results to files so that it can be used for later

    Parameters:
    save_path (str): the path of the file to save the results
    data (list): the data that contains the stories to save to the file
    '''

    file = open(save_path, "a")

    for story in data:
        file.write(story)
    
    file.close()

if __name__ == "__main__":
    main()