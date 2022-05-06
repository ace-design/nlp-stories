#This file will write doccano outputted jsonl file to human understandable annotaion
#Links: https://jsonlines.readthedocs.io/en/latest/
#https://docs.python.org/3/howto/argparse.html#id1
import jsonlines
import json
import argparse
import os
import sys

def main():
    loadPath, savePath = command()

    dictionaryList = []
        
    print("Receiving results")
   
    text, entities, relations = extract(loadPath)

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

        
        dictionary = convertJsonFormat(text[i], labels, relationList)
        dictionaryList.append(dictionary)
    print("Saving\n")
    saveFile(savePath, dictionaryList)

def command():
    '''
    Runs the command line inputs

    Returns:
        loadPath (str): Path to the file to be loaded
        savePath (str): Path to the file to be saved

    Raises:
        FileNotFoundError: raises excpetion
        wrong file type: raises exception
    '''

    parser = argparse.ArgumentParser(description = "This program is to convert jsonl files to human readiable files")
    parser.add_argument("loadPath", type = str, help = "path of file")
    parser.add_argument("savePath", type = str, help = "path of file to save")
    
    args = parser.parse_args()

    if not(args.savePath.endswith(".json")):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect saving file type. Save file type is .json")
    try:
        loadFile = open(args.loadPath)
        loadFile.close()
        saveFile = open(args.savePath)
        saveFile.close()
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        return args.loadPath, args.savePath
    
def extract(path):
    '''
    Extracts the information of given file

    Parameters:
        path (str): Path of the file to extract info

    Returns:
        text (list): story text
        entities (list): entities and their location within the story
        relations (list): relations and their location within the story
    '''
    
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
    '''
    Identify and sort labels within story

    Paramaters:
        text (str): story text
        entities (list): entities and their locations within the story

    Returns:
        labelList (list): sorted str labels
        labelIDList (list): element Id
        elementList (list): element corresponding in order to labelIdlist
    '''
    
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
    '''
    Identify and sort relations within story

    Parameters:
        relations (list): relations and their locations within story
        labelIDList (list): element Id
        elementList (list): element corresponding in order to labelIdlist

    Returns:
        relationList (list): sorted str relations
        primaryString (list): primary str elements
        primaryList (list): primary elements
    '''
    
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
            triggers += startElement + " --> " + endElement + ", "
            primaryActions += endElement + ", "
            primaryActionList.append(endElement)
            
        elif relationType == "targets":
            targets += startElement + " --> " + endElement + ", "
            targetAction.append(startElement)
            targetEntity.append(endElement)
            
        else:
            contains += startElement + " --> " + endElement + ", "

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
    '''
    find specific element within story

    Parameters:
        labelId (list): all element Id within story
        element (list): all element within story
        findId (int): Id to search for

    Returns:
        element (string): element that is found
    '''
    
    for i in range(len(labelId)):
        if labelId[i] == findId:
            return element[i]
    

def secondary (wholeList, primaryItem):
    '''
    identify the secondary elements within story

    Parameters:
        wholeList (list) : all elements in story
        primaryItem (list): all primary elements in story

    Returns:
        secondaryItem (str): secondary elements in story
    '''
    
    secondaryItem = ""
    for item in wholeList:
        if not(item in primaryItem):
            secondaryItem += item + ", "

    return secondaryItem

def output(text,labelList, relationList):
    '''
    outputs results to terminal

    Parameters:
        text (str): story text
        labelList (list): str of all sorted labels in story
        relationList (list): str of all sorted relations in story
    '''
    
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

def convertJsonFormat(text, labelList, relationList):
    '''
    converts results to json file format

    Parameters:
        text (str): story text
        labelList (list): str of all sorted labels in story
        relationList (list): str of all sorted relations in story

    Returns:
        data (dictionary): includes all sorted information about the story      
    '''
    persona, primaryEntity, secondaryEntity, primaryAction, secondaryAction, benefit, pId = labelList
    triggers, targets, contains = relationList

    data = {
            "PID": pId.strip(", "),
            "Text": text,
            "Persona": persona.strip(", "),
            "Action":[{"Primary Action": primaryAction.strip(", ").split(", ")},
                      {"Secondary Action": secondaryAction.strip(", ").split(", ")}],
            "Entity":[{"Primary Entity": primaryEntity.strip(", ").split(", ")},
                      {"Secondary Entity": secondaryEntity.strip(", ").split(", ")}],
            "Benefit": benefit.strip(", "),
            "Triggers": triggers.strip(", ").split(", "),
            "Targets": targets.strip(", ").split(", "),
            "Contains": contains.strip(", ").split(", ")}

    return data 

def saveFile(path, dictionaryList):
    '''
    save the results into json file

    Parameters:
        path (str): path of file to be saved
        dictionaryList (list): info to be saved onto file
    '''
    json.dumps(dictionaryList)
    with open(path,"w") as file:
        json.dump(dictionaryList, file, ensure_ascii=False, indent = 4)
    print("File is saved")

main()
