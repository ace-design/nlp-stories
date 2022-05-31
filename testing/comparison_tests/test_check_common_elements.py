import pytest
from comparison import check_common_elements

@pytest.mark.check_common_elements
def test_normal_case():
    baseline = "quickly load"
    nlp = "load"
    
    assert check_common_elements(baseline, nlp) == True
    
@pytest.mark.check_common_elements
def test_not_the_same():
    baseline = "load"
    nlp = "quickly save"
    
    assert check_common_elements(baseline, nlp) == False

@pytest.mark.check_common_elements
def test_nlp_adjective():
    baseline = "load"
    nlp = "quickly load"
    
    assert check_common_elements(baseline, nlp) == True

@pytest.mark.check_common_elements
def test_similar():
    baseline = "load"
    nlp = "quickly loaded"
    
    assert check_common_elements(baseline, nlp) == False

@pytest.mark.check_common_elements
def test_empty():
    baseline = "load"
    nlp = ""
    
    assert check_common_elements(baseline, nlp) == False

@pytest.mark.check_common_elements
def test_no_split():
    baseline = "load"
    nlp = "quicklyload"
    
    assert check_common_elements(baseline, nlp) == False

@pytest.mark.check_common_elements
def test_double_same_word():
    baseline = "load"
    nlp = "load quickly load"
    
    assert check_common_elements(baseline, nlp) == True

@pytest.mark.check_common_elements
def test_different_type():
    baseline = 342
    nlp = "quickly load"
    
    with pytest.raises(AttributeError):
        result = check_common_elements(baseline, nlp)
