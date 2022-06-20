import pytest
from comparison import extract_all_baseline_info
from testing.comparison_tests.test_sort import pos_data

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
    path = "testing\\comparison_tests\\comparison_testing_files\\normal_case.json"
    assert extract_all_baseline_info(path) == expected

# @pytest.mark.extract_all_baseline_info
# def test_no_primary_action():
#     print()

# @pytest.mark.extract_all_baseline_info
# def test_no_primary_entity():
#     print()

# @pytest.mark.extract_all_baseline_info
# def test_no_secondary_action():
#     print()

# @pytest.mark.extract_all_baseline_info
# def test_no_secondary_action():
#     print()

# @pytest.mark.extract_all_baseline_info
# def test_no_secondary_action_pos():
#     print()

# @pytest.mark.extract_all_baseline_info
# def test_no_primary_entity_pos():
#     print()

# @pytest.mark.extract_all_baseline_info
# def test_no_secondary_entity_pos():
#     print()