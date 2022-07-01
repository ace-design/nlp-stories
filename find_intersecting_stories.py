#this script will find stories that are valid for raw dataset, fabian results and visual narrator (stories that do not crash either one of these)
import argparse
import copy
import json
import sys
from turtle import left


def main():
    raw_data_path, fabian_path, visual_narrator_path, save_name = command()

    raw_data_stories = extract_text_file(raw_data_path)
    fabian_stories = extract_fabian(fabian_path)
    visual_narrator_stories = extract_text_file(visual_narrator_path)
    
    raw_data_stories, duplicates = remove_duplicates(raw_data_stories)
    intersect_stories = find_intersection(raw_data_stories, fabian_stories, visual_narrator_stories)

    left_out_raw_data = left_out_stories(intersect_stories, raw_data_stories)
    left_out_fabian = left_out_stories(intersect_stories, fabian_stories)
    left_out_visual_narrator = left_out_stories(intersect_stories, visual_narrator_stories)

    save_results(intersect_stories, duplicates, left_out_raw_data, left_out_fabian, left_out_visual_narrator, save_name)

    print("Completed")

def command():
    '''
    Runs the command line inputs

    Returns:
        args.load_raw_data_path (str): path of raw data text file
        args.load_fabian_path (str): path of fabian results file
        args.load_visual_narrator_path (str): path of visual narrator valid text file
        args.save_name (str): name to the saving file

    Raises:
        FileNotFoundError: raises excpetion
        wrong file type: raises exception
    '''
    parser = argparse.ArgumentParser(description = "This program is to get POS tags of the elements of the annotations")
    parser.add_argument("load_raw_data_path", type = str, help = "path of raw data text file")
    parser.add_argument("load_fabian_path", type = str, help = "path of fabian results file")
    parser.add_argument("load_visual_narrator_path", type = str, help = "path of visual narrator valid text file")
    parser.add_argument("save_name", type = str, help = "name of the file save the results")
    
    args = parser.parse_args()

    if not(args.load_raw_data_path.endswith(".txt")) or not(args.load_fabian_path.endswith(".json")) or not(args.load_visual_narrator_path.endswith(".txt")):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect input file type. input file type is .txt for raw data and visual narrator and .json for fabian")

    try:
        load_file = open(args.load_raw_data_path)
        load_file.close()
        load_file = open(args.load_fabian_path)
        load_file.close()
        load_file = open(args.load_visual_narrator_path)
        load_file.close()

    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise

    else:
        return args.load_raw_data_path, args.load_fabian_path, args.load_visual_narrator_path, args.save_name

def extract_text_file(path):
    '''
    extract the stories from the given path

    Parameters:
    path (str): the path to the file to extract

    Return:
    stories (list): all the stories in the file
    '''

    with open(path, "r", encoding="utf-8") as file:
        data = file.readlines()

    stories = []

    for story in data:
        stories.append(story.strip(" \n"))

    return stories

def extract_fabian (path):
    '''
    extrat the stories from the fabian results 

    Parameters:
    path (str): path to the file 

    Returns:
    stories (list): all the stories in the file
    '''
    text = []

    file = open(path)
    data = json.load(file)

    stories = data["stories"]
    pid = data["case"].capitalize()
    identifier = "#" + pid + "# "

    for story in stories:
        text.append(identifier + story["text"].strip())

    file.close()

    return text

def remove_duplicates(data):
    '''
    remove any duplicated stories in the dataset

    Parameters:
    data (list): the stories in the dataset

    Returns:
    non_duplicates (list): stories that are unique in dataset
    duplicates (list): stories that already exist in the unique datset
    '''
    stories = copy.deepcopy(data)

    duplicates = []
    
    for i in range(len(stories)):
        check = stories[0].strip()
        del stories[0]
        for j in range(len(stories)):
            if check == stories[j].strip():
                duplicates.append(stories[j])
                break

    non_duplicates = list(set(data))

    return non_duplicates, duplicates

def find_intersection(raw_data, fabian, visual_narrator):
    '''
    find the same valid stories of raw dataset, fabian, and visual_narrator
    
    Parameters:
    raw_data (list): unique stories in dataset
    fabian (list): stories from fabian results
    visual_narrator (list): valid stories for visual narrator

    Returns:
    intersect_stories (list): stories that exist in all sets
    '''

    first_intersection = set(raw_data).intersection(set(fabian))
    intersect_stories = list(first_intersection.intersection(visual_narrator))

    return intersect_stories

def left_out_stories(intersect_stories, dataset):
    '''
    determines the left_out stories from the dataset

    Parameters:
    intersect_stories (list): valid stories that exist in raw dataset, fabian results and visual_narrator
    dataset (list): stories of the dataset to check the missing stories

    Returns:
    left_out_stories (list): stories that are missing from the dataset 
    '''

    left_out_stories = list(set(dataset).difference(intersect_stories))

    return left_out_stories

def save_results(intersect_stories, duplicates, left_out_raw_data, left_out_fabian, left_out_visual_narrator, save_name):
    '''
    save results to file

    Parameters:
    intersect_stories (list): stories that exist and are valid for raw dataset, fabian results and for visual narrator 
    duplicates (list): stories that are already exist in the intersect_stories
    left_out_raw_data (list): left out stories from the raw data that are not in intersect_stories
    left_out_fabian (list): left out stories from fabian resutlts that are not in intersect_stories
    left_out_visual_narrator (list): left out stories from valid visual narrator stories that are not in intersect_stories
    save_name (str): name of the saving file
    '''

    intersect_stories_path = "inputs\\intersecting_stories\\" + save_name + ".txt"

    with open(intersect_stories_path, "w", encoding="utf-8") as file:
        for i in range(len(intersect_stories)):
            file.write(intersect_stories[i] + "\n")

    duplicates_path = "logs\\repeated_stories\\" + save_name + "_duplicated_stories.txt"

    with open(duplicates_path, "w", encoding="utf-8") as file:
        for i in range(len(duplicates)):
            file.write(duplicates[i] + "\n")

    left_out_stories_path = "logs\\left_out_stories\\" + save_name + "_left_out_stories.txt"

    with open (left_out_stories_path, "w", encoding="utf-8") as file:
        file.write("Left Over Stories Raw Data:\n")
        for i in range(len(left_out_raw_data)):
            file.write(left_out_raw_data[i] + "\n")

        for i in range(len(duplicates)):
            file.write(duplicates[i] + "\n")

        file.write("\nLeft Over Stories Fabian Results:\n")
        for i in range(len(left_out_fabian)):
            file.write(left_out_fabian[i] + "\n")

        file.write("\nLeft Over Stories Valid Visual Narrator:\n")
        for i in range(len(left_out_visual_narrator)):
            file.write(left_out_visual_narrator[i] + "\n")
    


if __name__ == "__main__":
    main()