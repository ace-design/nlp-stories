from itertools import count
import pytest
from compare.comparison import count_true_false_positives_negatives

@pytest.fixture
def comparison_results():
    true_positives = ["bank", "website", "laptop"]
    false_positives = ["agent", "counter"]
    false_negatives = ["chair", "orange", "code", "coffee"]
    comparison_results = [true_positives, false_positives, false_negatives]

    return comparison_results

@pytest.fixture
def expected():
    expected = [3,2,4]
    return expected

@pytest.mark.count_true_false_positives_negatives
def test_normal_case(comparison_results, expected):
    assert count_true_false_positives_negatives(comparison_results) == expected

@pytest.mark.count_true_false_positives_negatives
def test_zero_case(comparison_results, expected):
    comparison_results[1] = []
    expected[1] = 0

    assert count_true_false_positives_negatives(comparison_results) == expected

@pytest.mark.count_true_false_positives_negatives
def test_empty():
    comparison_results = [[],[],[]]
    expected = [0,0,0]

    assert count_true_false_positives_negatives(comparison_results) == expected

@pytest.mark.count_true_false_positives_negatives
def test_different_input(comparison_results, expected):
    comparison_results[2] = ["chair", [], "code", 5]

    assert count_true_false_positives_negatives(comparison_results) == expected