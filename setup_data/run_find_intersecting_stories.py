# This file is an automation script to run the finding_intersecting_stories.py file

import subprocess

def main():
    datasets = ["g02", "g03", "g04", "g05", "g08", "g10", "g11", "g12", "g13", "g14", "g17", "g18", "g19", "g21", "g22", "g23", "g24", "g25", "g26", "g27", "g28"]
    for dataset in datasets:
        arguments = ".\\inputs\\individual_backlog\\dataset\\" + dataset + ".txt " + \
            ".\\inputs\\individual_backlog\\valid_visual_narrator_stories\\" + dataset + ".txt " + \
            ".\\inputs\\individual_backlog\\gpt_3_5_v0125_stories\\" + dataset + ".txt " + \
            ".\\inputs\\individual_backlog\\gpt_3_5_v0613_2023_stories\\" + dataset + ".txt " + \
            ".\\inputs\\individual_backlog\\gpt_3_5_v0613_2024_stories\\" + dataset + ".txt " + \
            ".\\inputs\\individual_backlog\\gpt_4_turbo_v0125_stories\\" + dataset + ".txt " + \
            ".\\inputs\\individual_backlog\\gpt_4_v0613_stories\\" + dataset + ".txt "

        commandLine = "python setup_data/find_intersecting_stories.py " + arguments +  " " + dataset
        subprocess.run(commandLine)


if __name__ == "__main__":
    main()