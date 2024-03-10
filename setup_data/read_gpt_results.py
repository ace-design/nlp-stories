# This file is to read in GPT results folder that contains json results for each backlog and store the story as a text file for each backlog
import argparse
import json
import os

def main():
    resultFolderPath, saving_path = command()
    stories = retrieveStories(resultFolderPath, saving_path)

    


def command():
    parser = argparse.ArgumentParser(description = "This program is to read in GPT results and store the story as a text file")
    parser.add_argument("load_gpt_results_folder", type = str, help = "path to GPT results folder")
    parser.add_argument("saving_path", type = str, help = "saving path")

    args = parser.parse_args()
    
    return args.load_gpt_results_folder, args.saving_path

def retrieveStories(resultFolderPath, saving_path):
    # Given the GPT folder path, extract all the stories

    folder = os.listdir(resultFolderPath)

    for fileName in folder:
        file = open(resultFolderPath + "/" + fileName)
        allData = json.load(file) 

        stories = []

        # Extract the stories in the file
        for data in allData:
            text = data["Text"].strip(" \t\n")
            text = text.replace('\\\'', "\'")
            text = text.replace('\\\"', "\"")

            stories.append(text)

        # Save the results
        savingFileName = fileName.strip(".json")
        savingFileName += ".txt"
        with open(saving_path + "/" + savingFileName ,"w", encoding="utf-8") as file:
            for story in stories:
                file.write(story + "\n")

    return stories

if __name__ == "__main__":
    main()