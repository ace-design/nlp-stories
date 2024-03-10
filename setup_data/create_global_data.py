# This file is an automation script to merge the backlog data files into global and categories

import argparse
import json
import os
import subprocess

def main():
    backlogFolder, savingPath, nlp = command()
    createGlobalFile(backlogFolder, savingPath, nlp)


def command():
    parser = argparse.ArgumentParser(description = "This program is to read in GPT results and store the story as a text file")
    parser.add_argument("load_individal_backlog_folder", type = str, help = "path to folder that contains the backlog files")
    parser.add_argument("saving_path", type = str, help = "saving path")
    parser.add_argument("nlp", type = str, help = "NLP name")

    args = parser.parse_args()
    
    return args.load_individal_backlog_folder, args.saving_path, args.nlp

def createGlobalFile(backlogFolder, savingPath, nlp):
    # Merge all the files in the backlog folder into one

    folder = os.listdir(backlogFolder)
    savingName = savingPath + "/" + "global_" + nlp + ".json"


    # Copy over the first file contents to the global file
    file = open(backlogFolder + "/" + folder[0])
    initialData = json.load(file) 
    
    with open(savingName,"w", encoding="utf-8") as file:
        json.dump(initialData, file, indent = 4)
    


    # Iterative merge the rest of the file contents the global file
    if len(folder) >= 2:
        for fileName in folder[1:]:
            commandLine = "python ./setup_data/merge_data.py " + savingName + " " + backlogFolder + "/" + fileName
            subprocess.run(commandLine)

if __name__ == "__main__":
    main()