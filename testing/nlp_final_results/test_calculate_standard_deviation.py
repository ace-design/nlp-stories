from statistics import StatisticsError
import pytest
from nlp_final_results import calculate_standard_deviation

@pytest.fixture
def input_data ():
    persona_precision = [1,2,3,4,5,6]
    persona_recall = [1,5,9,3,5,7]
    persona_f_measure = [10,11,15,19,54,47]
    entity_precision = [4,5,6,7,8,9]
    entity_recall = [8,5,2,6,5,4]
    entity_f_measure = [12,101,65,47,18,49]
    action_precision = [9,8,7,5,2,6]
    action_recall = [4,2,6,8,1,0]
    action_f_measure = [47,60,23,25,95,412]

    input_data = [persona_precision, persona_recall, persona_f_measure, entity_precision, entity_recall, entity_f_measure, action_precision, action_recall, action_f_measure]

    return input_data

@pytest.fixture
def expected ():
    expected = [1.871, 2.828, 19.37, 1.871, 2.0, 32.537, 2.483, 3.082, 150.128]

    return expected

@pytest.mark.calculate_standard_deviation
def test_normal_case(input_data, expected):
    assert calculate_standard_deviation(input_data) == expected

@pytest.mark.calculate_standard_deviation
def test_empty_input():
    input_data = [[],[],[],[],[],[],[],[],[]]

    with pytest.raises(StatisticsError):
        result = calculate_standard_deviation(input_data)

@pytest.mark.calculate_standard_deviation
def test_zeros_input():
    zeroes = [0,0,0,0,0,0]
    input_data = [zeroes] * 9
    expected = [0,0,0,0,0,0,0,0,0]
    
    assert calculate_standard_deviation(input_data) == expected

@pytest.mark.calculate_standard_deviation
def test_combo_empty_input(input_data):
    input_data[3] = []

    with pytest.raises(StatisticsError):
        result = calculate_standard_deviation(input_data)

@pytest.mark.calculate_standard_deviation
def test_combo_zeroes_input(input_data, expected):
    input_data[4]  = [0,0,0]
    input_data[6]  = [0,0,0,0,0,0]
    expected[4] = 0
    expected[6] = 0

    assert calculate_standard_deviation(input_data) == expected

@pytest.mark.calculate_standard_deviation
def test_different_type():
    input_data = ["hello", "testing"]

    with pytest.raises(TypeError):
        result = calculate_standard_deviation(input_data)

@pytest.mark.calculate_standard_deviation
def test_one_dimension_list():
    input_data = [1,2,3,4,5,6,7,8,9]

    with pytest.raises(TypeError):
        result = calculate_standard_deviation(input_data)

