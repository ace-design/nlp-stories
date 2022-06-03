import pytest
from comparison import compare

@pytest.mark.compare
def test_normal_case():
    baseline = ["send", "click", "load"]
    nlp = ["send", "click", "load"]
    expected = [["send", "click", "load"],[],[],[]]

    assert compare(baseline, nlp) == expected

@pytest.mark.compare
def test_exact_and_similar_match():
    baseline = ["come more often", "come"]
    nlp = ["come"]
    expected = [["come"],[],[],["come more often"]]
    assert compare(baseline, nlp) == expected

@pytest.mark.compare
def test_plural():
    baseline = ["trucks", "computer", "emails"]
    nlp = ["computer", "emails", "truck"]
    expected = [["computer", "emails"], [], ["truck"], ["trucks"]]

    assert compare(baseline, nlp) == expected

@pytest.mark.compare
def test_nlp_adjective():
    baseline = ["savely delete", "quickly send", "load"]
    nlp = ["load efficiently", "quickly send", "delete"]
    expected = [["quickly send"], ["load", "savely delete"], [], []]

    assert compare(baseline, nlp) == expected

@pytest.mark.compare
def test_nlp_different_seperate_elements():
    baseline = ["user's stats"]
    nlp = ["user", "stats"]
    expected = [[], ["user's stats"], ["user"], []]

    assert compare(baseline, nlp) == expected

@pytest.mark.compare
def test_nlp_same_seperate_elements():
    baseline = ["load and save"]
    nlp = ["load", "save"]
    expected = [[], ["load and save"], ["save"], []]

    assert compare(baseline, nlp) == expected

@pytest.mark.compare
def test_false_positives():
    baseline = ["computer"]
    nlp = ["mouse"]
    expected = [[],[],["mouse"],["computer"]]

    assert compare(baseline, nlp) == expected

@pytest.mark.compare
def test_double_elements():
    baseline = ["click", "send"]
    nlp = ["click", "click"]
    expected = [["click"], [],["click"],["send"]]

    assert compare(baseline, nlp) == expected

@pytest.mark.compare
def test_empty_nlp():
    baseline = ["email", "files", "data"]
    nlp = []
    expected = [[],[],[], baseline]

    assert compare(baseline, nlp) == expected

@pytest.mark.compare
def test_empty_baseline():
    baseline = []
    nlp = ["email", "files", "data"]
    expected = [[], [], nlp, []]

    assert compare(baseline, nlp) == expected

@pytest.mark.compare
def test_different_type ():
    baseline = [1 ,2, 3,4]
    nlp = ["email", "files", "data"]
    
    with pytest.raises(AttributeError):
        result = compare(baseline, nlp)