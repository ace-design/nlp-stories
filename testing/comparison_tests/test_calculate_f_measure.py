import pytest 
from comparison import calculate_f_measure

@pytest.mark.calculate_f_measure
def test_normal_case():
    precision = 3
    recall = 5
    expected = 3.75

    assert calculate_f_measure(precision, recall) == expected

@pytest.mark.calculate_f_measure
def test_zero_precision():
    precision = 0
    recall = 5
    expected = 0

    assert calculate_f_measure(precision, recall) == expected

@pytest.mark.calculate_f_measure
def test_both_zero():
    precision = 0
    recall = 0
    expected = 0

    assert calculate_f_measure(precision, recall) == expected

@pytest.mark.calculate_f_measure
def test_different_type():
    precision = []
    recall = 5

    with pytest.raises(TypeError):
        results = calculate_f_measure(precision, recall)

@pytest.mark.calculate_f_measure
def test_negative_input():
    precision = -5
    recall = 3
    expected = 15.0

    assert calculate_f_measure(precision, recall) == expected
