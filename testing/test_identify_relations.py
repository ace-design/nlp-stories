import pytest
from jsonl_to_human_readable import *

@pytest.fixture
def relations():
    relations = [{"id": 100,"from_id": 2,"to_id": 3,"type":"triggers"},\
                 {"id": 101,"from_id": 3,"to_id": 5,"type":"targets"},\
                 {"id": 102,"from_id": 3,"to_id": 6,"type":"targets"},\
                 {"id": 103,"from_id": 4,"to_id": 6,"type":"targets"},\
                 {"id": 104,"from_id": 8,"to_id": 9,"type":"contains"},\
                 {"id": 105,"from_id": 7,"to_id": 8,"type":"targets"},\
                 {"id": 106,"from_id": 9,"to_id": 10,"type":"contains"},\
                 {"id": 107,"from_id": 9,"to_id": 11,"type":"contains"}]
    
    return relations

@pytest.fixture
def label_id_list():
    label_id_list = [2,3,4,5,6,7,8,9,10,11]
    return label_id_list

@pytest.fixture
def element_list():
    element_list = ["applicant", "click", "rename", "new tab", "button", "access", "info", "user info","name", "address"]
    return element_list


@pytest.mark.identify_relations
def test_normal_case(relations, label_id_list, element_list):
    triggers = "applicant --> click, "
    targets = "click --> new tab, click --> button, rename --> button, access --> info, "
    contains = "info --> user info, user info --> name, user info --> address, "
    triggers_list = [["applicant", "click"]]
    targets_list = [["click", "new tab"], ["click", "button"], ["rename", "button"], ["access", "info"]]
    contains_list = [["info", "user info"], ["user info", "name"], ["user info", "address"]]
    primary_actions = "click, "
    primary_action_list = ["click"]
    primary_action_id_list = [3]
    target_action = [[3, "click"], [3, "click"], [4,"rename"],[7,"access"]]
    target_entity = [[5, "new tab"], [6, "button"], [6, "button"], [8, "info"]]

    relation_string_list = [triggers, targets, contains]
    relation_list = [triggers_list, targets_list, contains_list]
    primary_element_data = [primary_actions, primary_action_list, primary_action_id_list, target_action, target_entity]
    expected = (relation_string_list, relation_list, primary_element_data)
    
    assert identify_relations(relations, label_id_list, element_list) == expected

@pytest.mark.identify_relations
def test_empty_relations(label_id_list, element_list):
    relations = []
    relation_string_list = ["","",""]
    relation_list = [[],[],[]]
    primary_element_data = ["",[],[],[],[]]

    expected = (relation_string_list, relation_list, primary_element_data)

    assert identify_relations(relations, label_id_list, element_list) == expected









    
