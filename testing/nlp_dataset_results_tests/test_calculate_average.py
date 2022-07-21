from statistics import StatisticsError
import pytest
from compare.nlp_dataset_results import calculate_average

@pytest.fixture
def input_data():

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
    expected = [3.5, 5, 26, 6.5, 5, 48.667, 6.167, 3.5, 110.333]
    return expected

@pytest.mark.calculate_average
def test_normal_case(input_data, expected):
    assert calculate_average(input_data) == expected

@pytest.mark.calculate_average
def test_empty_input():
    input_data = [[],[],[],[],[],[],[],[],[]]
    with pytest.raises(StatisticsError):
        result = calculate_average(input_data)

@pytest.mark.calculate_average
def test_zeros_input():
    zeroes = [0,0,0,0,0,0]
    input_data = [zeroes] * 9
    expected = [0,0,0,0,0,0,0,0,0]
    
    assert calculate_average(input_data) == expected

@pytest.mark.calculate_average
def test_combo_empty_input(input_data):
    input_data[3] = []
    

    with pytest.raises(StatisticsError):
        result = calculate_average(input_data)


@pytest.mark.calculate_average
def test_combo_zeroes_input(input_data, expected):
    input_data[4]  = [0,0,0]
    input_data[6]  = [0,0,0,0,0,0]
    expected[4] = 0
    expected[6] = 0

    assert calculate_average(input_data) == expected

@pytest.mark.calculate_average
def test_different_type():
    input_data = ["hello", "testing"]

    with pytest.raises(TypeError):
        result = calculate_average(input_data)

@pytest.mark.calculate_average
def test_one_dimension_list():
    input_data = [1,2,3,4,5,6,7,8,9]

    with pytest.raises(TypeError):
        result = calculate_average(input_data)