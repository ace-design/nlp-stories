#run crf model for each dataset to help find best features

import argparse
import statistics
import subprocess


def main():
    save_name = command()

    datasets = ["g02", "g03", "g04", "g05", "g08", "g10", "g11", "g12", "g13", "g14", "g16", "g17", "g18", "g19", "g21", "g22", "g23"]
    train = []
    test = []

    #Find the results for persona, primary/secondary action and entity
    for dataset in datasets:
        train.append("crf_input\\training_input\\" + dataset + ".json")
        test.append("crf_input\\evaluation_input\\" + dataset + ".json")

    p_act = []
    s_act = []
    p_ent = []
    s_ent = []
    per  = []
    weighted_average = []

    for i in range(len(datasets)):
        line = "python crf_nlp.py " + train[i] + " " + test[i] + " " + save_name + str(i)
        results = subprocess.run(line, capture_output = True)
        data = results.stdout.decode()
        print(data)
        get_results = data.split("P-ACT")[2]
        get_results = get_results.split()
        p_act.append(float(get_results[2]))
        s_act.append(float(get_results[7]))
        p_ent.append(float(get_results[12]))
        s_ent.append(float(get_results[17]))
        per.append(float(get_results[22]))
        weighted_average.append(float(get_results[len(get_results) -2]))

    p_act_average = average(p_act)
    s_act_average = average(s_act)
    p_ent_average = average(p_ent)
    s_ent_average = average(s_ent)
    per_average = average(per)
    weighted_average_average = average(weighted_average)

    

    #Find the results for just Action, Entity, and persona as labels
    train = []
    test = []

    for dataset in datasets:
        train.append("crf_input\\training_input_no_secondary\\" + dataset + ".json")
        test.append("crf_input\\evaluation_input_no_secondary\\" + dataset + ".json")

    act = []
    ent = []
    per  = []
    weighted_average = []

    for i in range(len(datasets)):
        line = "python crf_nlp.py " + train[i] + " " + test[i] + " " + save_name + str(i)+ str(i)+ str(i)
        results = subprocess.run(line, capture_output = True)
        data = results.stdout.decode()
        print(data)
        get_results = data.split("ACT")[2]
        get_results = get_results.split()
        act.append(float(get_results[2]))
        per.append(float(get_results[7]))
        ent.append(float(get_results[12]))
        weighted_average.append(float(get_results[len(get_results) -2]))

    act_average2 = average(act)
    ent_average2 = average(ent)
    per_average2 = average(per)
    weighted_average_average2 = average(weighted_average)


    #Output
    print("P-Act", p_act_average)
    print("S-Act", s_act_average)
    print("P-Ent", p_ent_average)
    print("S-Ent", s_ent_average)
    print("Per", per_average)
    print("Weighted Average", weighted_average_average)
    print()

    print("Act", act_average2)
    print("Ent", ent_average2)
    print("Per", per_average2)
    print("Weighted Average", weighted_average_average2)



def command():
    parser = argparse.ArgumentParser(description = "This program will run crf model for each dataset to help find best features")
    parser.add_argument("save_name", type = str, help = "name of the file save the results")

    args = parser.parse_args()

    return args.save_name


def average(numbers):

    average= round(statistics.mean(numbers), 3)

    return average



if __name__ == "__main__":
    main()