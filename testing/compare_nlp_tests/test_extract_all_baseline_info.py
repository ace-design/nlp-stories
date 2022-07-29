import pytest
from compare.compare_nlp import extract_all_baseline_info
from testing.compare_nlp_tests.test_sort import pos_data

@pytest.fixture
def expected():

    text = ["#G00# As a user, I want to quickly click on the button to go to next page in tab."]
    persona = [["user"]]
    entity = [["button", "next page", "tab"]]
    action = [["quickly click", "go"]]

    persona_pos = [[[["NOUN"]],[["user"]]]]
    entity_pos = [[[["NOUN"],["ADJ","NOUN"],["NOUN"]],[["button"],["next", "page"],["tab"]]]]
    action_pos = [[[["ADJ", "VERB"],["VERB"]], [["quickly", "click"], ["go"]]]]
    
    baseline_data = [text, persona, entity, action]
    pos_data = [persona_pos, entity_pos, action_pos]

    expected = (baseline_data, pos_data)
    return expected

@pytest.mark.extract_all_baseline_info
def test_normal_case(expected):
    path = "testing\\compare_nlp_tests\\comparison_testing_files\\normal_case.json"
    assert extract_all_baseline_info(path) == expected

@pytest.mark.extract_all_baseline_info
def test_no_primary_action(expected):
    path = "testing\\compare_nlp_tests\\comparison_testing_files\\no_primary_action.json"
    
    baseline_data, pos_data = expected
    del baseline_data[3][0][0]
    del pos_data[2][0][0][0] #[label type][story number][pos tag][pos tag value]
    del pos_data[2][0][1][0] #[label type][story number][pos text][pos text value]

    expected = (baseline_data, pos_data)
    
    assert extract_all_baseline_info(path) == expected

@pytest.mark.extract_all_baseline_info
def test_no_primary_entity(expected):
    path = "testing\\compare_nlp_tests\\comparison_testing_files\\no_primary_entity.json"

    baseline_data, pos_data = expected
    del baseline_data[2][0][0]
    del pos_data[1][0][0][0]
    del pos_data[1][0][1][0]

    expected = (baseline_data, pos_data)
    
    assert extract_all_baseline_info(path) == expected

@pytest.mark.extract_all_baseline_info
def test_no_secondary_action(expected):
    path = "testing\\compare_nlp_tests\\comparison_testing_files\\no_secondary_action.json"

    baseline_data, pos_data = expected
    del baseline_data[3][0][1]
    del pos_data[2][0][0][1]
    del pos_data[2][0][1][1]

    expected = (baseline_data, pos_data)
    
    assert extract_all_baseline_info(path) == expected

@pytest.mark.extract_all_baseline_info
def test_no_secondary_entity(expected):
    path = "testing\\compare_nlp_tests\\comparison_testing_files\\no_secondary_entity.json"

    baseline_data, pos_data = expected
    del baseline_data[2][0][2]
    del baseline_data[2][0][1]
    del pos_data[1][0][0][2]
    del pos_data[1][0][0][1]
    del pos_data[1][0][1][2]
    del pos_data[1][0][1][1]
    
    expected = (baseline_data, pos_data)
    
    assert extract_all_baseline_info(path) == expected

