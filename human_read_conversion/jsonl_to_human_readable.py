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
            relationList, primaryString, primaryList = identifyRelations(relations[i], labelIdList, elementList)

            primaryAction, primaryEntity = primaryString
            primaryActionList, primaryEntityList = primaryList
            persona , entityList, actionList, benefit, pID = labelList

            secondaryEntity = secondary(entityList, primaryEntityList)
            secondaryAction = secondary(actionList, primaryActionList)

            labels = [persona, primaryEntity, secondaryEntity, primaryAction, secondaryAction, benefit, pID]
            output(text[i], labels, relationList)
        
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
    entity = []
    action = []
    benefit = ""
    pID = ""

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

        if labelType == "Persona":
            persona += element + ", "
        elif labelType == "Entity":
            entity.append(element)
        elif labelType == "Action":
            action.append(element)
        elif labelType == "Benefit":
            benefit+= element + ", "
        else:
            pID = element

    labelList = [persona, entity, action, benefit, pID]

    return labelList, labelIdList, elementList

def identifyRelations(relations,labelIdList,elementList):
    triggers = ""
    targets = ""
    contains = ""
    primaryActions = ""
    primaryEntities = ""
    primaryActionList = []
    primaryEntityList = []
    targetAction = []
    targetEntity = []
 
    
    for relation in relations:
        relationType = relation["type"]
        startId = relation["from_id"]
        endId = relation["to_id"]

        startElement = findElement(labelIdList, elementList, startId)
        endElement = findElement(labelIdList, elementList, endId)
        
        if relationType == "triggers":
            triggers += startElement + " --> " + endElement + ",  "
            primaryActions += endElement + ", "
            primaryActionList.append(endElement)
            
        elif relationType == "targets":
            targets += startElement + " --> " + endElement + ",  "
            targetAction.append(startElement)
            targetEntity.append(endElement)
            
        else:
            contains += startElement + " --> " + endElement + ",  "

    for primaryAction in primaryActionList:
        for i in range(len(targetAction)):
            if primaryAction == targetAction[i]:
                primaryEntities += targetEntity[i] + ", "
                primaryEntityList.append(targetEntity[i])
    
    relationList = [triggers, targets, contains]
    primaryString = primaryActions, primaryEntities
    primaryList = primaryActionList, primaryEntityList

    return relationList, primaryString, primaryList

def findElement(labelId, element, findId):
    for i in range(len(labelId)):
        if labelId[i] == findId:
            return element[i]
    

def secondary (wholeList, primaryItem):
    secondaryItem = ""
    for item in wholeList:
        if not(item in primaryItem):
            secondaryItem += item + ", "

    return secondaryItem

def output(text,labelList, relationList):
    persona, primaryEntity, secondaryEntity, primaryAction, secondaryAction, benefit, pId = labelList
    triggers, targets, contains = relationList

    print("--------------------STORY START--------------------")
    print("PID:", pId.strip(", "))
    print("Story text:", text)
    print("\n")
    print("Persona:", persona.strip(", "))
    print("Primary Action:", primaryAction.strip(", "))
    print("Secondary Action:", secondaryAction.strip(", "))
    print("Primary Entity:", primaryEntity.strip(", "))
    print("Secondary Entity:", secondaryEntity.strip(", "))
    print("Benefit:", benefit.strip(", "))
    print("\n")
    print("Triggers:", triggers.strip(", "))
    print("Targets:", targets.strip(", "))
    print("Contains:", contains.strip(", "))
    print("---------------------STORY END---------------------\n")

main()
