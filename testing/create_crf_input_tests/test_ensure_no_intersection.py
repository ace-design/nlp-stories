import pytest
from nlp.nlp_tools.crf.create_crf_input import ensure_no_intersection

@pytest.mark.ensure_no_intersection
def test_normal_case():
    training = ["red", "yellow", "blue"]
    testing = ["green", "purple", "orange"]
    assert ensure_no_intersection(training, testing) == None

@pytest.mark.ensure_no_intersection
def test_fails():
    training = ["red", "purple", "blue"]
    testing = ["green", "purple", "blue"]

    with pytest.raises(Exception):
        results =  ensure_no_intersection(training, testing)

@pytest.mark.ensure_no_intersection
def test_different_size():
    training = ["red", "yellow", "blue", "brown", "cyan"]
    testing = ["green", "purple", "orange"]
    assert ensure_no_intersection(training, testing) == None

@pytest.mark.ensure_no_intersection
def test_different_size_fails():
    training = ["red", "purple", "blue"]
    testing = ["green", "purple", "pink", "magenta", "red", "black"]

    with pytest.raises(Exception):
        results =  ensure_no_intersection(training, testing)


@pytest.mark.ensure_no_intersection
def test_set():
    training = {"red", "yellow", "blue"}
    testing = {"green", "purple", "orange"}
    
    assert ensure_no_intersection(training, testing) == None

@pytest.mark.ensure_no_intersection
def test_set_fails():
    training = {"red", "yellow", "blue"}
    testing = {"red", "purple", "orange"}

    with pytest.raises(Exception):
        results =  ensure_no_intersection(training, testing)

@pytest.mark.ensure_no_intersection
def test_int():
    training =  [1,2,3]
    testing = [4,5,6]
    
    assert ensure_no_intersection(training, testing) == None

@pytest.mark.ensure_no_intersection
def test_int_fails():
    training =  [1,2,3]
    testing = [4,5,3]
    
    with pytest.raises(Exception):
        results =  ensure_no_intersection(training, testing)

@pytest.mark.ensure_no_intersection
def test_empty_training():
    training =  []
    testing = [4,5,3]
    
    assert ensure_no_intersection(training, testing) == None

@pytest.mark.ensure_no_intersection
def test_empty_testing():
    training =  [1,2,3,4,5,6]
    testing = []
    
    assert ensure_no_intersection(training, testing) == None

@pytest.mark.ensure_no_intersection
def test_empty_testing_and_training():
    training =  []
    testing = []
    
    assert ensure_no_intersection(training, testing) == None
