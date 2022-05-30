import pytest 
from comparison import calculate_recall

@pytest.mark.calculate_recall
def test_normal_case():
    number_compared_results = [3,5,6]
    expected = 0.3333333333333333

    assert calculate_recall(number_compared_results) == expected

@pytest.mark.calculate_recall
def test_zero_true_positive():
    number_compared_results = [0,5,6]
    expected = 0

    assert calculate_recall(number_compared_results) == expected

@pytest.mark.calculate_recall
def test_zero_inputs():
    number_compared_results = [0,6,0]
    expected = 0

    assert calculate_recall(number_compared_results) == expected

@pytest.mark.calculate_recall
def test_different_type():
    number_compared_results = [0,5,"6"]
    
    with pytest.raises(TypeError):
        result = calculate_recall(number_compared_results)

@pytest.mark.calculate_recall
def test_negative_value():
    number_compared_results = [-3,5,6]
    expected = -1
    
    assert calculate_recall(number_compared_results) == expected

@pytest.mark.calculate_recall
def test_empty():
    number_compared_results = []
    
    with pytest.raises(ValueError):
        result = calculate_recall(number_compared_results)