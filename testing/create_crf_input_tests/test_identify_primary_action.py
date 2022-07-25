import pytest
from nlp.nlp_tools.crf.create_crf_input import identify_primary_action

@pytest.fixture
def annotated_story():
    annotated_story = ["","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","a","a","a","a","a","a","","","","e","e","e","e","e","e","","","","","","","","","","","","","","","","a","a","a","a","","","","","","","","","e","e","e","e","e","e","e","e","e"]
    return annotated_story

@pytest.fixture
def label_id_list():
    label_id_list = [1,2,3,4,5,6,7]
    return label_id_list

@pytest.fixture
def offset_list():
    offset_list = [[0,3],[10,19],[31,37],[40,46],[55,82],[61,65],[73,82]]
    return offset_list

"11: As an applicant, I want to create a button so that I can move to the next page"

@pytest.fixture
def relations():
    relations = [{"id": 100,"from_id": 2,"to_id": 3,"type":"triggers"},\
                 {"id": 101,"from_id": 3,"to_id": 4,"type":"targets"},\
                 {"id": 102,"from_id": 6,"to_id": 7,"type":"targets"}]
    
    return relations

@pytest.mark.identify_primary_action
def test_normal_case(annotated_story, label_id_list, offset_list, relations):
    updated_annotated_story = ["","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","A","A","A","A","A","A","","","","e","e","e","e","e","e","","","","","","","","","","","","","","","","a","a","a","a","","","","","","","","","e","e","e","e","e","e","e","e","e"]
    primary_action_id_list = [3]

    expected = (updated_annotated_story, primary_action_id_list)

    assert identify_primary_action(annotated_story, label_id_list, offset_list, relations) == expected

@pytest.mark.identify_primary_action
def test_many_primary_actions(annotated_story, label_id_list, offset_list, relations):
    relations.append({"id": 103,"from_id": 2,"to_id": 6,"type":"triggers"})
    relations.append({"id": 104,"from_id": 2,"to_id": 7,"type":"triggers"})

    updated_annotated_story = ["","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","A","A","A","A","A","A","","","","e","e","e","e","e","e","","","","","","","","","","","","","","","","A","A","A","A","","","","","","","","","A","A","A","A","A","A","A","A","A"]
    primary_action_id_list = [3,6,7]

    expected = (updated_annotated_story, primary_action_id_list)

    assert identify_primary_action(annotated_story, label_id_list, offset_list, relations) == expected

@pytest.mark.identify_primary_action
def test_no_primary_action(annotated_story, label_id_list, offset_list, relations):
    relations.pop(0)
    primary_action_id_list = []

    expected = (annotated_story, primary_action_id_list)


    assert identify_primary_action(annotated_story, label_id_list, offset_list, relations) == expected

@pytest.mark.identify_primary_action
def test_empty_relations(annotated_story, label_id_list, offset_list):
    relations = []
    primary_action_id_list = []

    expected = (annotated_story, primary_action_id_list)

    assert identify_primary_action(annotated_story, label_id_list, offset_list, relations) == expected

@pytest.mark.identify_primary_action
def test_action_primary_secondary(annotated_story, label_id_list, offset_list,relations):  
    #id 3 has a triggers and a target relation 
    relations.append({"id": 103,"from_id": 4,"to_id": 3,"type":"targets"})
    updated_annotated_story = ["","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","A","A","A","A","A","A","","","","e","e","e","e","e","e","","","","","","","","","","","","","","","","a","a","a","a","","","","","","","","","e","e","e","e","e","e","e","e","e"]
    primary_action_id_list = [3]

    expected = (updated_annotated_story, primary_action_id_list)

    assert identify_primary_action(annotated_story, label_id_list, offset_list, relations) == expected

@pytest.mark.identify_primary_action
def test_missing_entity_key(annotated_story, label_id_list, offset_list):
    relations = [{"id": 103,"from_id": 4,"type":"triggers"}]
    with pytest.raises(KeyError):
        results = identify_primary_action (annotated_story, label_id_list, offset_list, relations)

@pytest.mark.identify_primary_action
def test_wrong_entity_key(annotated_story, label_id_list, offset_list):
    relations = [{"id": 103,"from_id": 4,"to": 3,"type":"triggers"}]
     
    with pytest.raises(KeyError):
        results = identify_primary_action (annotated_story, label_id_list, offset_list, relations)

@pytest.mark.identify_primary_action
def test_invalid_relations_id(annotated_story, label_id_list, offset_list):
    relations = [{"id": 103,"from_id": 4,"to_id": 1000,"type":"triggers"}]
     
    with pytest.raises(ValueError):
        results = identify_primary_action (annotated_story, label_id_list, offset_list, relations)

    






