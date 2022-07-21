import pytest
from compare.comparison import inclusion_compare

@pytest.fixture
def baseline():
    baseline = ["data", "mouse", "large server", "tab", "button"]
    return baseline

@pytest.fixture
def nlp():
    nlp = ["data", "keyboard", "server", "new tab", "buttons"]
    return nlp 

@pytest.fixture
def expected():
    true_positive = ["data", "button"]
    false_positive = ["keyboard", "server", "new tab"]
    false_negative = ["mouse", "large server", "tab"]
    expected = [true_positive, false_positive, false_negative]

    return expected

@pytest.mark.inclusion_compare
def test_normal_case(baseline, nlp, expected):
    assert inclusion_compare(baseline, nlp) == expected

@pytest.mark.inclusion_compare
def test_more_inclusion_cases(baseline, nlp, expected):
    baseline.append("computer")
    baseline.append("wires")
    baseline.append("typed")
    baseline.append("hand in")

    nlp.append("computers")
    nlp.append("wire")
    nlp.append("type")
    nlp.append("handed in")

    expected[0].append("computer")
    expected[0].append("wires")
    expected[0].append("typed")
    expected[0].append("hand in")

    assert inclusion_compare(baseline, nlp) == expected

@pytest.mark.inclusion_compare
def test_qualifiers(baseline, nlp, expected):
    #should fail because qualifiers are strict comparison in this comparison mode
    baseline.append("beautiful design")
    baseline.append("website")
    nlp.append("design")
    nlp.append("fast website")

    expected[1].append("design")
    expected[1].append("fast website")
    expected[2].append("beautiful design")
    expected[2].append("website")

    assert inclusion_compare(baseline, nlp) == expected

@pytest.mark.inclusion_compare
def test_negative(baseline, nlp, expected):
    baseline.append("without knowing")
    nlp.append("knowing")
    expected[1].append("knowing")
    expected[2].append("without knowing")

    assert inclusion_compare(baseline, nlp) == expected
    
@pytest.mark.inclusion_compare
def test_similar(baseline, nlp, expected):
    baseline.append("dataset")
    nlp.append("data")
    expected[0].append("dataset")
    
    assert inclusion_compare(baseline, nlp) == expected

@pytest.mark.inclusion_compare
def test_similar_two_words(baseline, nlp, expected):
    baseline.append("dataset")
    baseline.append("data")
    nlp.append("data")
    expected[0].append("data")
    expected[2].append("dataset")

    assert inclusion_compare(baseline, nlp) == expected

@pytest.mark.inclusion_compare
def test_split_two(baseline, nlp, expected):
    baseline.append("user's stats")
    nlp.append("user's")
    nlp.append("stats")
    expected[1].append("user's")
    expected[1].append("stats")
    expected[2].append("user's stats")

    assert inclusion_compare(baseline, nlp) == expected

@pytest.mark.inclusion_compare
def test_difference_alphabetic_case(baseline, nlp, expected):
    baseline[0] = "DaTa"
    nlp[2] = "SeRvEr"
    nlp[4] = "ButToNs"
    expected[0][0] = "DaTa"

    assert inclusion_compare(baseline, nlp) == expected

@pytest.mark.inclusion_compare
def test_different_qualifiers(baseline, nlp, expected):
    #qualifiers have strict comparison
    baseline.append("quickly add")
    baseline.append("effectively load")
    baseline.append("eat all")
    baseline.append("merge perfectly")
    baseline.append("beautiful design")
    nlp.append("slowly adds")
    nlp.append("effectively loads")
    nlp.append("eats all")
    nlp.append("merges terribly")
    nlp.append("wonderful design")

    expected[0].append("effectively load")
    expected[0].append("eat all")
    expected[1].append("slowly adds")
    expected[2].append("quickly add")
    expected[1].append("merges terribly")
    expected[2].append("merge perfectly")
    expected[1].append("wonderful design")
    expected[2].append("beautiful design")

    assert inclusion_compare(baseline, nlp) == expected

@pytest.mark.inclusion_compare
def test_empty_baseline(nlp):
    baseline = []
    expected = [[],nlp,[]]
    
    assert inclusion_compare(baseline, nlp) == expected

@pytest.mark.inclusion_compare
def test_empty_nlp(baseline):
    nlp = []
    expected = [[],[], baseline]

    assert inclusion_compare(baseline, nlp) == expected