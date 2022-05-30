import pytest
from jsonl_to_human_readable import identify_labels

@pytest.fixture
def text():
    text = "11: As an applicant, I want to create a button so that I can move to the next page"
    return text

@pytest.fixture
def entities():
    entities = [{"id": 1, "label": "PID", "start_offset": 0 ,"end_offset": 3},\
                {"id": 2, "label": "Persona", "start_offset": 10 ,"end_offset": 19},\
                {"id": 3, "label": "Action", "start_offset": 31 ,"end_offset": 37},\
                {"id": 4, "label": "Entity", "start_offset": 40 ,"end_offset": 46},\
                {"id": 5, "label": "Benefit", "start_offset": 55 ,"end_offset": 82},\
                {"id": 6, "label": "Action", "start_offset": 61 ,"end_offset": 65},\
                {"id": 7, "label": "Entity", "start_offset": 78 ,"end_offset": 82}]
    return entities



@pytest.mark.identify_labels
def test_normal_case_identify_labels(text, entities):
    label_list_expected = ["applicant, ", ["button", "page"], ["create", "move"], "I can move to the next page, ", "11:"]
    label_id_list_expected = [1,2,3,4,5,6,7]
    entity_expected = ["11:", "applicant", "create", "button", "I can move to the next page", "move", "page"]

    expected = (label_list_expected, label_id_list_expected, entity_expected)
    
    assert identify_labels (text, entities) == expected

@pytest.mark.identify_labels
def test_empty_text(entities):        
    text = ""
    label_list_expected = [", ", ["", ""], ["", ""], ", ", ""]
    label_id_list_expected = [1,2,3,4,5,6,7]
    entity_expected = ["", "", "", "", "", "", ""]
    expected = (label_list_expected, label_id_list_expected, entity_expected)

    assert identify_labels (text, entities) == expected

@pytest.mark.identify_labels
def test_empty_entities(text):
    entities = []
    label_list_expected = ["", [], [], "", ""]
    label_id_list_expected = []
    entity_expected = []

    expected = (label_list_expected, label_id_list_expected, entity_expected)
    
    assert identify_labels (text, entities) == expected

@pytest.mark.identify_labels
def test_empty_text_and_entities():
    text = ""
    entities = ""
    entities = []
    label_list_expected = ["", [], [], "", ""]
    label_id_list_expected = []
    entity_expected = []

    expected = (label_list_expected, label_id_list_expected, entity_expected)
    
    assert identify_labels (text, entities) == expected

@pytest.mark.identify_labels
def test_two_persona(entities):
    text = "11: As an applicant and a user, I want to create a button so that I can move to the next page"
    entities = [{"id": 1, "label": "Persona", "start_offset": 10 ,"end_offset": 19},\
                {"id": 2, "label": "Persona", "start_offset": 26 ,"end_offset": 30}]

    label_list_expected = ["applicant, user, ", [], [], "", ""]
    label_id_list_expected = [1,2]
    entity_expected = ["applicant", "user"]

    expected = (label_list_expected, label_id_list_expected, entity_expected)
    
    assert identify_labels (text, entities) == expected
    
@pytest.mark.identify_labels
def test_two_pid(text, entities):
    text = text + " 123"
    entities.append({"id": 8, "label": "PID", "start_offset": 83  ,"end_offset": 86})

    label_list_expected = ["applicant, ", ["button", "page"], ["create", "move"], "I can move to the next page, ", "123"]
    label_id_list_expected = [1,2,3,4,5,6,7,8]
    entity_expected = ["11:", "applicant", "create", "button", "I can move to the next page", "move", "page", "123"] 

    expected = (label_list_expected, label_id_list_expected, entity_expected)
    
    assert identify_labels (text, entities) == expected

@pytest.mark.identify_labels
def test_missing_entity_key(text):
    entities = [{"id": 2, "label": "Persona", "start_offset": 10}]
     
    with pytest.raises(KeyError):
        results = identify_labels (text, entities)

@pytest.mark.identify_labels
def test_wrong_entity_key(text):
    entities = [{"id": 2, "label": "Persona", "start_offset": 10,"end": 19}]
     
    with pytest.raises(KeyError):
        results = identify_labels (text, entities)
        
@pytest.mark.identify_labels
def test_list_entities(text, entities):
    entities_list = []
    for dictionary in entities:
        entities_list.append(list(dictionary.items()))
        
    with pytest.raises(TypeError):
        results = identify_labels (text, entities_list)
    

@pytest.mark.identify_labels
def test_list_text(entities):
    text = ["11: As an applicant,", "I want to create a button", "so that I can move to the next page"]

    with pytest.raises(TypeError):
        results = identify_labels (text, entities)
