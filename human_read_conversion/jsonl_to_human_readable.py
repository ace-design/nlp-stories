#This file will write doccano outputted jsonl file to human understandable annotaion
#Links: https://jsonlines.readthedocs.io/en/latest/
#https://docs.python.org/3/howto/argparse.html#id1
import jsonlines
import argparse
import os

## Codereview - Seb - 220504
# - Use argparse instead of input                                      -Completed Sath
# - Remove whitespaces in the directorie/paths                         -Completed Sath
# - refactor/reorganize with functions:                                -Completed Sath
#   - main function that 
#       1/ call the argument parser (aregparse)
#       2/ organize the business logic
# - Differentiate main entities/secondary ones, and same for actions.   


def main():
    path, state = command()

    if state == 1:
        print("Receiving results")
        text, entities, relations = extract(path)
    
        for i in range(len(text)):
            labelList, labelIdList, elementList = identifyLabels(text[i], entities[i])
            relationList = identifyRelations(relations[i], labelIdList, elementList)

            output(text[i], labelList, relationList)
        
    elif state == 2:
        print("Saving")
        
    else:
        print("Please try again")

def command():
    parser = argparse.ArgumentParser(description = "This program is to convert jsonl files to human readiable files")
    parser.add_argument("path", type = str, help = "path of file")
    parser.add_argument("-f", "--file", help = "input file directory path", action = "store_true")
    parser.add_argument("-s", "--save", help = "save results to file", action = "store_true")
    args = parser.parse_args()

    if args.file:
        if os.path.exists(args.path):
            print("File Found")
            return args.path, 1
        else:
            print("File not found")
            return None, 3
    elif args.save:
        #SAVE JSON FILE HERE
        name = ""
        return name, 2
    else:
        print("Please enter the appropriate argument. type -h for help")
        return None, 3

def extract(path):
    text = []
    entities = []
    relations = [] 
    with jsonlines.open(path) as file:
        for story in file:
            text.append(story["text"])
            entities.append(story["entities"])
            relations.append(story["relations"])
    return text, entities, relations

def identifyLabels(text, entities):
    persona = ""
    entity = ""
    action = ""
    benefit =""
    pID = ""

    labelName = ["Persona", "Entity", "Action", "Benefit", "PID"]
    labelList = [persona, entity, action, benefit, pID]
    labelIdList = []
    elementList = []

    for label in entities:
        labelID = label["id"]
        labelType = label["label"]
        startOffset = label["start_offset"]
        endOffset = label["end_offset"]
        element = text[startOffset : endOffset]

        labelIdList.append(labelID)
        elementList.append(element)

        for i in range(5):
            if labelType == labelName[i]:
                labelList[i] += element + ", "
                break
    return labelList, labelIdList, elementList

def identifyRelations(relations,labelIdList,elementList):
    triggers = ""
    targets = ""
    contains = ""
    relationName = ["triggers", "targets", "contains"]
    relationList = [triggers, targets, contains]
    
    for relation in relations:
        relationType = relation["type"]
        startId = relation["from_id"]
        endId = relation["to_id"]

        startElement = findElement(labelIdList, elementList, startId)
        endElement = findElement(labelIdList, elementList, endId)
        
        for i in range(3):
            if relationType == relationName[i]:
                relationList[i] += startElement + " --> " + endElement + ", "
                break

    return relationList

def findElement(labelId, element, findId):
    for i in range(len(labelId)):
        if labelId[i] == findId:
            return element[i]

def output(text,labelList, relationList):
    persona, entity, action, benefit, pId = labelList
    triggers, targets, contains = relationList

    print("--------------------STORY START--------------------")
    print("PID:", pId.strip(","))
    print("Story text:", text)
    print("\n")
    print("Persona:", persona.strip(","))
    print("Action:", action.strip(","))
    print("Entity:", entity.strip(","))
    print("Benefit:", benefit.strip(","))
    print("\n")
    print("Triggers:", triggers.strip(", "))
    print("Targets:", targets.strip(", "))
    print("Contains:", contains.strip(", "))
    print("---------------------STORY END---------------------\n\n")

main()
