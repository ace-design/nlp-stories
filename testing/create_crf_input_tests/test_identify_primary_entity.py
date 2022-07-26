from multiprocessing.sharedctypes import Value
import pytest
from nlp.nlp_tools.crf.create_crf_input import identify_primary_entity

@pytest.fixture
def annotated_story():
    annotated_story = ["","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","A","A","A","A","A","A","","","","e","e","e","e","e","e","","","","","","","","","","","","","","","","a","a","a","a","","","","","","","","","e","e","e","e","e","e","e","e","e"]
    return annotated_story

@pytest.fixture
def label_id_list():
    label_id_list = [1,2,3,4,5,6,7]
    return label_id_list

@pytest.fixture
def offset_list():
    offset_list = [[0,3],[10,19],[31,37],[40,46],[55,82],[61,65],[73,82]]
    return offset_list

@pytest.fixture
def relations():
    relations = [{"id": 100,"from_id": 2,"to_id": 3,"type":"triggers"},\
                 {"id": 101,"from_id": 3,"to_id": 4,"type":"targets"},\
                 {"id": 102,"from_id": 6,"to_id": 7,"type":"targets"}]
    
    return relations

@pytest.fixture
def primary_action_id_list():
    primary_action_id_list = [3]
    return primary_action_id_list

@pytest.mark.identify_primary_entity_crf
def test_normal_case(annotated_story, primary_action_id_list, label_id_list, offset_list, relations):

    expected = ["","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","A","A","A","A","A","A","","","","E","E","E","E","E","E","","","","","","","","","","","","","","","","a","a","a","a","","","","","","","","","e","e","e","e","e","e","e","e","e"]

    assert identify_primary_entity(annotated_story, primary_action_id_list, label_id_list, offset_list, relations) == expected

@pytest.mark.identify_primary_entity_crf
def test_many_primary_entities(label_id_list, offset_list, relations):
    primary_action_id_list = [3,6,7]
    relations.append({"id": 104,"from_id": 7,"to_id": 1,"type":"targets"})

    annotated_story = ["","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","A","A","A","A","A","A","","","","e","e","e","e","e","e","","","","","","","","","","","","","","","","A","A","A","A","","","","","","","","","A","A","A","A","A","A","A","A","A"]
    expected = ["E","E","E","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","A","A","A","A","A","A","","","","E","E","E","E","E","E","","","","","","","","","","","","","","","","A","A","A","A","","","","","","","","","E","E","E","E","E","E","E","E","E"]

    assert identify_primary_entity(annotated_story, primary_action_id_list, label_id_list, offset_list, relations) == expected

@pytest.mark.identify_primary_entity_crf
def test_secondary_action(annotated_story, primary_action_id_list, label_id_list, offset_list, relations):
    #should not change since id 7 is  not in primary_action_id_list
    relations.append({"id": 104,"from_id": 7,"to_id": 4,"type":"targets"})

    expected = ["","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","A","A","A","A","A","A","","","","E","E","E","E","E","E","","","","","","","","","","","","","","","","a","a","a","a","","","","","","","","","e","e","e","e","e","e","e","e","e"]

    assert identify_primary_entity(annotated_story, primary_action_id_list, label_id_list, offset_list, relations) == expected

@pytest.mark.identify_primary_entity_crf
def test_no_primary_entity(annotated_story, label_id_list, offset_list, relations):
    primary_action_id_list = []
    
    expected = ["","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","A","A","A","A","A","A","","","","e","e","e","e","e","e","","","","","","","","","","","","","","","","a","a","a","a","","","","","","","","","e","e","e","e","e","e","e","e","e"]

    assert identify_primary_entity(annotated_story, primary_action_id_list, label_id_list, offset_list, relations) == expected

@pytest.mark.identify_primary_entity_crf
def test_no_relations(annotated_story, primary_action_id_list, label_id_list, offset_list, relations):
    relations = []
    
    expected = ["","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","A","A","A","A","A","A","","","","e","e","e","e","e","e","","","","","","","","","","","","","","","","a","a","a","a","","","","","","","","","e","e","e","e","e","e","e","e","e"]

    assert identify_primary_entity(annotated_story, primary_action_id_list, label_id_list, offset_list, relations) == expected

@pytest.mark.identify_primary_entity_crf
def test_entity_primary_secondary(annotated_story, primary_action_id_list, label_id_list, offset_list, relations):
    relations.insert(0, {"id": 103,"from_id": 6,"to_id": 4 ,"type":"targets"})

    expected = ["","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","A","A","A","A","A","A","","","","E","E","E","E","E","E","","","","","","","","","","","","","","","","a","a","a","a","","","","","","","","","e","e","e","e","e","e","e","e","e"]

    assert identify_primary_entity(annotated_story, primary_action_id_list, label_id_list, offset_list, relations) == expected

@pytest.mark.identify_primary_entity_crf
def test_missing_relation_key(annotated_story, primary_action_id_list, label_id_list, offset_list):
    relations = [{"id": 103,"from_id": 3, "type":"targets"}]
    with pytest.raises(KeyError):
        results = identify_primary_entity(annotated_story, primary_action_id_list, label_id_list, offset_list, relations)

@pytest.mark.identify_primary_entity_crf
def test_wrong_relation_key(annotated_story, primary_action_id_list, label_id_list, offset_list):
    relations = [{"id": 103,"from_id": 3,"to": 3,"type":"targets"}]
     
    with pytest.raises(KeyError):
        results = identify_primary_entity(annotated_story, primary_action_id_list, label_id_list, offset_list, relations)

@pytest.mark.identify_primary_entity_crf
def test_invalid_relations_id(annotated_story, primary_action_id_list, label_id_list, offset_list):
    relations = [{"id": 103,"from_id": 3,"to_id": 1000,"type":"targets"}]
    
    with pytest.raises(ValueError):
        results =  identify_primary_entity(annotated_story, primary_action_id_list, label_id_list, offset_list, relations)