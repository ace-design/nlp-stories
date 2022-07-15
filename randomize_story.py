#randomize choose stories for training and testing for crf

import argparse
import json
import random


def main():
    training_path, testing_path = command()

    file = open(training_path, encoding= "utf-8")
    data = json.load(file)
    test = []

    num_test = int(len(data) * 0.2)

    for i in range(num_test):
        length = len(data)
        index = random.randint(0, length -1)
        test.append(data[index])
        data.pop(index)


    with open(testing_path,"w", encoding="utf-8") as file:
        json.dump(test, file, ensure_ascii=False, indent = 4)

    with open(training_path,"w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent = 4)

def command():
    parser = argparse.ArgumentParser(description = "This program will randomize choose stories for training and testing for crf")
    parser.add_argument("load_training_path", type = str, help = "path of crf file with the training set input")
    parser.add_argument("load_testing_path", type = str, help = "path of crf file with the training set input")

    
    args = parser.parse_args() 

    return args.load_training_path, args.load_testing_path


if __name__ == "__main__":
    main()