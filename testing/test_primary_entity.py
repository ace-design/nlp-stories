import pytest
from jsonl_to_human_readable import identify_primary_entity


@pytest.fixture
def primary_action_id_list():
    primary_action_id_list = [2,3]

    return primary_action_id_list

@pytest.fixture
def target_action():
    target_action = [[1,"add"],[2,"click"],[3,"send"],[4,"download"],[5,"upload"]]

    return target_action

@pytest.fixture
def target_entity():
    target_entity = [[6, "button"],[7, "tabs"],[8, "emails"],[9,"data"],[10,"results"]]

    return target_entity

@pytest.fixture
def expected():
    primary_entities = "tabs, emails, "
    primary_entity_list = ["tabs", "emails"]

    expected = (primary_entities, primary_entity_list)

    return expected

@pytest.fixture
def empty_expected():
    return ("",[])

@pytest.mark.identify_primary_entity
def test_normal_case_identify_primary_entity(primary_action_id_list,target_action,target_entity, expected):

    assert identify_primary_entity(primary_action_id_list,target_action,target_entity) == expected

@pytest.mark.identify_primary_entity
def test_same_action(primary_action_id_list,target_action,target_entity, expected):
    target_action.append([11,"click"])
    target_entity.append([12, "close button"])

    assert identify_primary_entity(primary_action_id_list,target_action,target_entity) == expected

@pytest.mark.identify_primary_entity
def test_no_id_found(primary_action_id_list,target_action,target_entity,empty_expected):
    primary_action_id_list = [100,101]
    
    assert identify_primary_entity(primary_action_id_list,target_action,target_entity) == empty_expected

@pytest.mark.identify_primary_entity
def test_empty_target(primary_action_id_list,empty_expected):
    target_action = []
    target_entity= []

    assert identify_primary_entity(primary_action_id_list,target_action,target_entity) == empty_expected


@pytest.mark.identify_primary_entity
def test_empty_primary_Action_id_list(target_action,target_entity,empty_expected):
    primary_action_id_list = []
    
    assert identify_primary_entity(primary_action_id_list,target_action,target_entity) == empty_expected
