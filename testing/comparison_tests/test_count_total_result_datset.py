import pytest
from comparison import count_total_result_dataset

@pytest.mark.count_total_result_dataset
def test_normal_case():
    total_comparison_results = [[1,2,3],[7,8,9],[4,5,6],[0,1,4]]
    expected = [12,16,22]

    assert count_total_result_dataset(total_comparison_results) == expected

@pytest.mark.count_total_result_dataset
def test_no_stories():
    total_comparison_results = []
    expected = [0,0,0]

    assert count_total_result_dataset(total_comparison_results) == expected

@pytest.mark.count_total_result_dataset
def test_zero_value():
    total_comparison_results = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    expected = [0,0,0]

    assert count_total_result_dataset(total_comparison_results) == expected

@pytest.mark.count_total_result_dataset
def test_different_input():
    total_comparison_results = [[1,2,3],[7,[],9],["p",5,6],[0,1,4]]
    with pytest.raises(TypeError):
        results =  count_total_result_dataset(total_comparison_results)