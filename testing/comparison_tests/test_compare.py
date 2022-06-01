import pytest
from comparison import compare

@pytest.fixture
def baseline():
    baseline = ["send", "click", "load", "save easily", "delete"]
    return baseline

@pytest.fixture
def nlp():
    nlp = ["send", "click", "save", "deleted"]
    return nlp

@pytest.fixture
def expected():
    expected = [["send", "click", "save easily","delete"],[],["load"]]
    return expected

@pytest.mark.compare
def test_exact_and_similar_match():
    baseline = ["come more often", "come"]
    nlp = ["come"]
    expected = [["come"],[],[],["come more often"]]
    assert compare(baseline, nlp) == expected


# @pytest.mark.compare
# def test_normal_case(baseline, nlp, expected):
#     assert compare(baseline, nlp) == expected

# @pytest.mark.compare
# def test_nlp_adjective(baseline, nlp, expected):
#     nlp[3] = "savely deleted"

#     assert compare(baseline, nlp) == expected

# @pytest.mark.compare
# def test_similar_elements(baseline, expected):
#     nlp = ["sent quickly", "clicks", "Saves immediately", "deleted"]

#     assert compare(baseline, nlp) == expected

# @pytest.mark.compare
# def test_false_positives(baseline, nlp, expected):
#     nlp.append("print")
#     nlp.append("recover latest")

#     expected[1] = ["print", "recover latest"]   

#     assert compare(baseline, nlp) == expected

# @pytest.mark.compare
# def test_double_true_positives(baseline, nlp, expected):
#     baseline.append("click")
#     expected[2].append("click")

#     assert compare(baseline, nlp) == expected

# @pytest.mark.compare
# def test_two_in_one_element(baseline, nlp, expected):
#     nlp[2] = "load and save"
#     expected[2] = ["save easily"]
#     expected[0][2] = "load"

#     assert compare(baseline, nlp) == expected

# @pytest.mark.compare
# def test_empty_nlp(baseline):
#     nlp = []
#     expected = [[],[],baseline]

#     assert compare(baseline, nlp) == expected

# @pytest.mark.compare
# def test_empty_baseline(nlp):
#     baseline = []
#     expected = [[],nlp, []]

#     assert compare(baseline, nlp) == expected

# @pytest.mark.compare
# def test_different_type (nlp):
#     baseline = [1 ,2, 3,4]
    
#     with pytest.raises(AttributeError):
#         result = compare(baseline, nlp)