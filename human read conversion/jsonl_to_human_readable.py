#This file will write doccano outputted jsonl file to human understandable annotaion
#Links: https://jsonlines.readthedocs.io/en/latest/
import jsonlines

#Ask user what file in folder
userInput = input("Enter the name of the json1 file:")
print("\n")

#open the jsonl file and work with each story
with jsonlines.open(userInput) as file:
    for story in file:
        text = story["text"]
        entities = story["entities"]
        relations = story["relations"]
        
        #label types
        persona = ""
        entity = ""
        action = ""
        benefit =""
        PID = ""
        labelName = ["Persona", "Entity", "Action", "Benefit", "PID"]
        labelList = [persona, entity, action, benefit, PID]
        labelIdList = []
        
        #labels identified in each story
        for label in entities:
            labelID = label["id"]
            labelType = label["label"]
            startOffset = label["start_offset"]
            endOffset = label["end_offset"]
            element = text[startOffset:endOffset]
            
            labelIdList.append([labelID, element])
            #sort label
            for i in range(5):
                if labelType == labelName[i]:
                    labelList[i] += element + ", "
                    break

        #relation types
        triggers = ""
        targets = ""
        contains = ""
        relationName = ["triggers", "targets", "contains"]
        relationList = [triggers, targets, contains]

        #relation identified in each story
        for relation in relations:
            relationType = relation["type"]
            startId = relation["from_id"]
            endId = relation["to_id"]
            #find start element
            for labelId in labelIdList:
                if labelId[0] == startId:
                   startElement = labelId[1]
                   break
            #find end element
            for labelId in labelIdList:
                if labelId[0] == endId:
                   endElement = labelId[1]
                   break
            #sort relations
            for i in range(3):
                if relationType == relationName[i]:
                    relationList[i] += startElement + " --> " + endElement + ", "
                    break
        #printing
        #labelList[persona, entity, action, benefit, PID]
        #relationList[triggers, targets, contains]
        print("PID:", labelList[4].strip(","))
        print("Story text:", text)
        print("\n")
        print("Persona:", labelList[0].strip(","))
        print("Action:", labelList[2].strip(","))
        print("Entity:", labelList[1].strip(","))
        print("Benefit:", labelList[3].strip(","))
        print("\n")
        print("Triggers:", relationList[0].strip(", "))
        print("Targets:", relationList[1].strip(", "))
        print("Contains:", relationList[2].strip(", "))
        print("---------------------------------------------------------------------")
input("") 
        
