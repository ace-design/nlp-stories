import pytest
from jsonl_to_human_readable import secondary

@pytest.fixture
def whole_list():
    return ["add", "push", "click", "extract", "save"]

@pytest.fixture
def primary_item():
    return ["push", "extract"]

@pytest.mark.secondary
def test_nromal_case_secondary(whole_list, primary_item):
    expected = "add, click, save, "

    assert secondary(whole_list, primary_item) == expected

@pytest.mark.secondary
def test_duplicate_primary(whole_list, primary_item):
    primary_item.append("push")
    whole_list.append("push")
    expected = "add, click, save, "

    assert secondary(whole_list, primary_item) == expected

@pytest.mark.secondary
def test_empty_primary(whole_list):
    primary_item = []
    expected = "add, push, click, extract, save, "
    
    assert secondary(whole_list, primary_item) == expected

@pytest.mark.secondary
def test_whole_list(primary_item):
    whole_list = []

    with pytest.raises(ValueError):
        result = secondary (whole_list, primary_item)

@pytest.mark.secondary
def test_different_type(whole_list):
    primary_item = [["push"], ["extract"]]

    with pytest.raises(TypeError):
        result = test_different_type(whole_list, primary_item)
