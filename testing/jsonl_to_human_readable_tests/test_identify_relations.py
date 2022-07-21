import pytest
from setup_data.jsonl_to_human_readable import *

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

@pytest.fixture
def expected():
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

    return relation_string_list, relation_list, primary_element_data


@pytest.mark.identify_relations
def test_normal_case_identify_relations(relations, label_id_list, element_list, expected):    
    assert identify_relations(relations, label_id_list, element_list) == expected

@pytest.mark.identify_relations
def test_empty_relations(label_id_list, element_list):
    relations = []
    relation_string_list = ["","",""]
    relation_list = [[],[],[]]
    primary_element_data = ["",[],[],[],[]]

    expected = (relation_string_list, relation_list, primary_element_data)

    assert identify_relations(relations, label_id_list, element_list) == expected

@pytest.mark.identify_relations
def test_two_triggers(relations, label_id_list, element_list, expected):
    relations.extend([{"id": 108,"from_id": 2,"to_id": 12,"type":"triggers"},\
                     {"id": 109,"from_id": 12,"to_id": 13,"type":"targets"}])
    label_id_list.extend([12,13])
    element_list.extend(["add", "phone number"])

    relation_string_list, relation_list, primary_element_data = expected

    triggers, targets, contains= relation_string_list
    triggers += "applicant --> add, "
    targets += "add --> phone number, "
    relation_string_list = [triggers, targets, contains]

    triggers_list, targets_list, contains_list = relation_list
    triggers_list.append(["applicant", "add"])
    targets_list.append(["add", "phone number"])
    relation_list = [triggers_list, targets_list, contains_list]

    primary_actions, primary_action_list, primary_action_id_list, target_action, target_entity = primary_element_data
    primary_actions += "add, "
    primary_action_list.append("add")
    primary_action_id_list.append(12)
    target_action.append([12, "add"])
    target_entity.append([13, "phone number"])
    primary_element_data = [primary_actions, primary_action_list, primary_action_id_list, target_action, target_entity]
    
    expected = (relation_string_list, relation_list, primary_element_data)
    

        
    assert identify_relations(relations, label_id_list, element_list) == expected

@pytest.mark.identify_relations
def test_action_primary_secondary(relations, label_id_list, element_list, expected):
    relations.append({"id": 108,"from_id": 12,"to_id": 13,"type":"targets"})
    label_id_list.extend([12,13])
    element_list.extend(["click", "new tab"])

    relation_string_list, relation_list, primary_element_data = expected

    triggers, targets, contains= relation_string_list
    targets += "click --> new tab, "
    relation_string_list = [triggers, targets, contains]

    triggers_list, targets_list, contains_list = relation_list
    targets_list.append(["click", "new tab"])
    relation_list = [triggers_list, targets_list, contains_list]

    primary_actions, primary_action_list, primary_action_id_list, target_action, target_entity = primary_element_data
    target_action.append([12, "click"])
    target_entity.append([13, "new tab"])
    primary_element_data = [primary_actions, primary_action_list, primary_action_id_list, target_action, target_entity]
    
    expected = (relation_string_list, relation_list, primary_element_data)

    assert identify_relations(relations, label_id_list, element_list) == expected

@pytest.mark.identify_relations
def test_missing_relation_key(label_id_list, element_list):
    relations = [{"id": 100,"from_id": 2,"type":"triggers"}]
     
    with pytest.raises(KeyError):
        results = identify_relations(relations, label_id_list, element_list)

@pytest.mark.identify_relations
def test_wrong_relation_key(label_id_list, element_list):
    relations = [{"id": 100,"fromid": 2,"toid": 3,"type":"triggers"}]
     
    with pytest.raises(KeyError):
        results = identify_relations(relations, label_id_list, element_list)

@pytest.mark.identify_relations
def test_invalid_relation_type(relations,label_id_list, element_list, expected):
    relations[0] = {"id": 100,"from_id": 2,"to_id": 3,"type":"tigers"}
    
    relation_string_list, relation_list, primary_element_data = expected

    triggers, targets, contains= relation_string_list
    triggers = ""
    relation_string_list = [triggers, targets, contains]

    triggers_list, targets_list, contains_list = relation_list
    triggers_list.clear()
    relation_list = [triggers_list, targets_list, contains_list]

    primary_actions, primary_action_list, primary_action_id_list, target_action, target_entity = primary_element_data
    primary_actions = ""
    primary_action_list.clear()
    primary_action_id_list.clear()
    primary_element_data = [primary_actions, primary_action_list, primary_action_id_list, target_action, target_entity]
    
    expected = (relation_string_list, relation_list, primary_element_data)

    assert identify_relations(relations, label_id_list, element_list) == expected

@pytest.mark.identify_relations
def test_invalid_relation_id(relations,label_id_list, element_list):
    relations[0] = {"id": 100,"from_id": 100,"to_id": 3,"type":"triggers"}

    with pytest.raises(TypeError):
        results = identify_relations(relations, label_id_list, element_list)
