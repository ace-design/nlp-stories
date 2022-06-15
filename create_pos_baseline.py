#This script will create the POS tags for the words in the baseline annotations. 
import argparse
import json
import stanza
import sys

def main():
    load_path, save_path = command()
    primary_baseline_data = load_primary_data(load_path)
    all_baseline_data = load_all_data(load_path)

    stanza.download('en') 
    global stanza_nlp
    stanza_nlp = stanza.Pipeline('en')

    primary_saving_path = save_path + "_primary_pos.json"
    all_saving_path = save_path + "_all_pos.json"

    get_results_and_save(primary_baseline_data, primary_saving_path)
    print("Primary file is saved")

    get_results_and_save(all_baseline_data, all_saving_path)
    print("All file is saved")

def command():
    '''
    Runs the command line inputs

    Returns:
        args.load_baseline_path (str): Path to the baseline file to be loaded
        args.save_name (str): name to the saving file

    Raises:
        FileNotFoundError: raises excpetion
        wrong file type: raises exception
    '''
    parser = argparse.ArgumentParser(description = "This program is to get POS tags of the elements of the annotations")
    parser.add_argument("load_baseline_path", type = str, help = "path of file")
    parser.add_argument("save_name", type = str, help = "name of the file save the results")
    
    args = parser.parse_args()

    if not(args.load_baseline_path.endswith(".json")):
        sys.tracebacklimit = 0
        raise Exception ("Incorrect input file type. input file type is .json")

    try:
        load_baseline_file = open(args.load_baseline_path)
        load_baseline_file.close()
    except FileNotFoundError:
        sys.tracebacklimit = 0
        print("File or directory does not exist")
        raise
    else:
        save_folder_path = "outputs\\pos_baseline\\" + args.save_name
        return args.load_baseline_path, save_folder_path

def load_primary_data(load_path):
    '''
    Gets the primary data that saved on the baseline annoitation json file

    Parameters:
    path (str): path to the file

    Returns:
    baseline_data (2D list): contains the whole story data, persona, primary entities, and primary actions identified by the baseline data
    '''
    story_data = []
    persona = []
    primary_entity = []
    primary_action = []

    file = open(load_path)
    data = json.load(file)

    for story in data:
        story_data.append(story)
        persona.append(story["Persona"])
        primary_entity.append(story["Entity"]["Primary Entity"])
        primary_action.append(story["Action"]["Primary Action"])
    file.close()

    baseline_data = [story_data, persona, primary_entity, primary_action]

    return baseline_data

def load_all_data(load_path):
    '''
    Gets the all data that saved on the baseline annoitation json file

    Parameters:
    load_path (str): the path of the baseline annotations

    Returns:
    baseline_data (2d list): contains the whole story data, persona, entity and action of each story
    '''

    persona = []
    entity = []
    action = []
    story_data = []
 

    file = open(load_path)
    data = json.load(file)

    for story in data:
        story_data.append(story)
        persona.append(story["Persona"])

        primary_entity = story["Entity"]["Primary Entity"]
        secondary_entity = story["Entity"]["Secondary Entity"]
        primary_action = story["Action"]["Primary Action"]
        secondary_action = story["Action"]["Secondary Action"]


        if secondary_action != [""]:
            action.append(primary_action + secondary_action)
        else:
            action.append(primary_action)

        if secondary_entity != [""]:
            entity.append(primary_entity + secondary_entity)
        else:
            entity.append(primary_entity)

    file.close()

    baseline_data = [story_data, persona, entity, action]

    return baseline_data

def get_results_and_save(baseline_data, save_path):
    '''
    Runs all the functions to get the POS tags and save it to a file

    Parameters:
    basleine_data (2d list): contains the data to get the POS tag for
    save_path (str): the savign path to save save the final results
    '''
    total_output = []

    story_data, persona, entity, action = baseline_data

    for i in range(len(story_data)):
        persona_tag_info = get_pos_tag(persona[i])
        entity_tag_info = get_pos_tag(entity[i])
        action_tag_info = get_pos_tag(action[i])

        update_story_data = create_output_format(story_data[i], persona_tag_info, entity_tag_info, action_tag_info)
        total_output.append(update_story_data)

    save_results(total_output, save_path)


def get_pos_tag(label):
    '''
    gets the pos tag of each word of the annotation

    Paramters:
    label (list): either persona, entity, or action. This is what we are getting the POS tag for

    Returns:
    label_text (2d list): contains the text of each annotation element in the story for the specific label
    label_pos_tag (2d list): contains the POS tag of each word of each annotation element in the story for the specific label
    '''

    label_text = []
    label_pos_tag = []

    for i in range(len(label)):
        baseline_stanza = stanza_nlp(label[i])

        text = []
        pos_tag = []
        for sent in baseline_stanza.sentences:
            for word in sent.words:
                pos_tag.append(word.upos)
                text.append(word.text)
        label_text.append(text)
        label_pos_tag.append(pos_tag)

    return label_text, label_pos_tag

def create_output_format(story_data, persona_tag_info, entity_tag_info, action_tag_info):
    '''
    creates a output format to save the results to the a json file

    Parameters:
    story_data (dict): contains the all the information of the story from the file
    persona_tag_info (2d list): the pos tag info of the all the persona annotations of the story
    entity_tag_info (2d list): the pos tag info of the all the entity annotations of the story
    action_tag_info (2d list): the pos tag info of the all the action annotations of the story
    
    Returns:
    story_data (dict): updated story data that now has the POS tags of annotations as well
    '''
    persona_text, persona_pos = persona_tag_info
    entity_text, entity_pos = entity_tag_info
    action_text, action_pos = action_tag_info

    story_data["Persona POS"] = persona_pos
    story_data["Persona POS text"] = persona_text
    story_data["Action POS"] = action_pos
    story_data["Action POS text"] = action_text
    story_data["Entity POS"] = entity_pos
    story_data["Entity POS text"] = entity_text

    return story_data

def save_results(data, save_path):
    '''
    Saves the final results to a json file

    Parameters:
    data (list): the data that contains that annoitated results and the POS tags
    save_path (str): the saving path to save the final results
    '''

    json.dumps(data)
    with open(save_path,"w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent = 4)

if __name__ == "__main__":
    main()