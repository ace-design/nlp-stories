import pytest
from compare.comparison import strict_compare

@pytest.fixture
def baseline():
    baseline = ["quickly add", "import", "save", "load efficiently", "user's stats"]
    return baseline

@pytest.fixture
def nlp():
    nlp = ["add", "import all", "save", "load efficiently", "user's", "stats"]
    return nlp

@pytest.fixture
def expected():
    true_positive = ["save", "load efficiently"]
    false_positive = ["add", "import all", "user's", "stats"]
    false_negative = ["quickly add", "import", "user's stats"]
    expected = [true_positive, false_positive, false_negative]
    return expected

@pytest.mark.strict_compare
def test_normal_case(baseline, nlp, expected):
    assert strict_compare(baseline, nlp) == expected

@pytest.mark.strict_compare
def test_different_alphabetical_cases(baseline, nlp, expected):
    baseline[2] = "SaVe"
    nlp[0] = "AdD"
    nlp[3] = "Load Efficiently"
    expected[0][0] = baseline[2]

    assert strict_compare(baseline, nlp) == expected

@pytest.mark.strict_compare
def test_plural (baseline, nlp, expected):
    baseline.append("evaluate")
    nlp.append("evaluates")
    expected[1].append("evaluates")
    expected[2].append("evaluate")

    assert strict_compare(baseline, nlp) == expected

@pytest.mark.strict_compare
def test_similar_cases(baseline, nlp, expected):
    baseline.append("immediately download")
    baseline.append("download")
    nlp.append("download")
    expected[0].append("download")
    expected[2].append ("immediately download")

    assert strict_compare(baseline, nlp) == expected 

@pytest.mark.strict_compare
def test_negative(baseline, nlp, expected):
    baseline.append("not have")
    nlp.append("have")
    expected[1].append("have")
    expected[2].append("not have")

    assert strict_compare(baseline, nlp) == expected

@pytest.mark.strict_compare
def test_empty_baseline(nlp):
    baseline = []
    expected = [[],nlp,[]]

    assert strict_compare(baseline, nlp) == expected

@pytest.mark.strict_compare
def test_empty_nlp(baseline):
    nlp = []
    expected = [[],[],baseline]

    assert strict_compare(baseline, nlp) == expected