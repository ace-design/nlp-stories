import pytest
from nlp.nlp_tools.crf.create_crf_input import identify_labels_crf

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
                {"id": 7, "label": "Entity", "start_offset": 73 ,"end_offset": 82}]
    return entities

@pytest.mark.identify_labels_crf
def test_normal_case(text, entities):
    annotated_story = ["","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","a","a","a","a","a","a","","","","e","e","e","e","e","e","","","","","","","","","","","","","","","","a","a","a","a","","","","","","","","","e","e","e","e","e","e","e","e","e"]
    label_id_list = [1,2,3,4,5,6,7]
    offset_list = [[0,3],[10,19],[31,37],[40,46],[55,82],[61,65],[73,82]]
    expected = (annotated_story, label_id_list, offset_list)

    assert identify_labels_crf(text, entities) == expected

@pytest.mark.identify_labels_crf
def test_empty_text(entities):
    text = ""
    annotated_story = ["P","P","P","P","P","P","P","P","P","a","a","a","a","a","a","e","e","e","e","e","e","a","a","a","a","e","e","e","e","e","e","e","e","e"]
    label_id_list = [1,2,3,4,5,6,7]
    offset_list = [[0,3],[10,19],[31,37],[40,46],[55,82],[61,65],[73,82]]
    expected = (annotated_story, label_id_list, offset_list)

    assert identify_labels_crf(text, entities) == expected

@pytest.mark.identify_labels_crf
def test_empty_entities(text):
    entities = []
    annotated_story = ["","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]
    label_id_list = []
    offset_list = []
    expected = (annotated_story, label_id_list, offset_list)

    assert identify_labels_crf(text, entities) == expected

@pytest.mark.identify_labels_crf
def test_empty_text_and_entities():
    text  = []
    entities = []
    annotated_story = []
    label_id_list = []
    offset_list = []
    expected = (annotated_story, label_id_list, offset_list)

    assert identify_labels_crf(text, entities) == expected

@pytest.mark.identify_labels_crf
def test_missing_entity_key(text):
    entities = [{"id": 2, "label": "Persona", "start_offset": 10}]
     
    with pytest.raises(KeyError):
        results = identify_labels_crf (text, entities)

@pytest.mark.identify_labels_crf
def test_wrong_entity_key(text):
    entities = [{"id": 2, "label": "Persona", "start_offset": 10,"end": 19}]
     
    with pytest.raises(KeyError):
        results = identify_labels_crf (text, entities)

@pytest.mark.identify_labels_crf
def test_overlapping_labels(text, entities):
    entities.append({"id": 8, "label": "Action", "start_offset": 73 ,"end_offset": 82})
    annotated_story = ["","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","a","a","a","a","a","a","","","","e","e","e","e","e","e","","","","","","","","","","","","","","","","a","a","a","a","","","","","","","","","a","a","a","a","a","a","a","a","a"]
    label_id_list = [1,2,3,4,5,6,7,8]
    offset_list = [[0,3],[10,19],[31,37],[40,46],[55,82],[61,65],[73,82],[73,82]]
    expected = (annotated_story, label_id_list, offset_list)

    assert identify_labels_crf(text, entities) == expected