import pytest
from jsonl_to_human_readable import *

lst = [[["a","b","c"],["c"],"a, b, "], [["a","b","c"],["c","a"],"b, "], [["d","e","f"],["e"],"d, f, "]]
lst_two = [[[1,2,3,4,5],["a","b","c","d","e"],3,"c"], [[1,2,3,4,5],["a","b","c","d","e"],5,"e"]]
lst_three = [["test_files\\test_case_one.jsonl", (["hi", "hello"], [[{"id":1},{"id":2}],[{"id":5},{"id":6}]], [[{"id":3},{"id":4}],[{"id":7},{"id":8}]])],\
             ["test_files\\test_case_two.jsonl", (["test", "testing"], [[{"id":"a"},{"id":"b"}],[{"id":"c"},{"id":"d"}]], [[{"id":"e"},{"id":"f"}],[{"id":"g"},{"id":"h"}]])]]
             
@pytest.mark.parametrize("whole_list,primary_item, expected", lst)
def test_secondary(whole_list,primary_item, expected):
    assert secondary(whole_list,primary_item) == expected

@pytest.mark.parametrize("label_id, element, find_id, expected", lst_two)
def test_find_element (label_id, element, find_id, expected):
    assert find_element(label_id, element, find_id) == expected   

@pytest.mark.parametrize("path, expected", lst_three)
def test_extract(path, expected):
    assert extract(path) == expected

#def test_identify_labels():
#    assert True
#
#def test_identify_relations():
#    assert True
