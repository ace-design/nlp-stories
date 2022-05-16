import pytest
from jsonl_to_human_readable import find_element

@pytest.fixture()
def label_id():
    label_id = [120, 546, 452, 128, 654, 987]
    return label_id

@pytest.fixture()
def element():
    element = ["user", "add" , "button", "view", "documentation", "website"]
    return element

@pytest.mark.find_element
def test_normal_case_find_element(label_id, element):
    assert find_element(label_id, element, 452) == "button"

@pytest.mark.find_element
def test_unmatched_id(label_id, element): 
    assert find_element(label_id, element, 100) == None

@pytest.mark.find_element
def test_first_id(label_id, element): 
    assert find_element(label_id, element, label_id[0]) == element[0]

@pytest.mark.find_element
def test_last_id(label_id, element): 
    assert find_element(label_id, element, label_id[-1]) == element[-1]

@pytest.mark.find_element
def test_string_find_id(label_id, element):
    assert find_element(label_id, element, "452") == None


