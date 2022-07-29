import pytest
import stanza
from compare.compare_nlp import relaxed_compare

stanza.download('en') 
global stanza_pos_nlp
stanza_pos_nlp = stanza.Pipeline('en')

@pytest.fixture
def baseline():
    baseline = ["quickly enter", "load", "update"]
    return baseline

@pytest.fixture
def nlp():
    nlp = ["enter", "load efficiently", "update page", "download"]
    return nlp

@pytest.fixture
def pos_data():
    pos_data = [[["ADJ", "VERB"],["VERB"],["VERB"]],[["quickly", "enter"],["load"],["update"]]]
    return pos_data

@pytest.fixture
def expected():
    true_positive = ["quickly enter", "load"]
    false_positive = ["update page", "download"]
    false_negative = ["update"]

    expected = [true_positive, false_positive, false_negative]
    return expected

@pytest.mark.relaxed_compare
def test_normal_case(baseline, nlp, pos_data, expected):
    assert relaxed_compare(baseline, nlp, pos_data, stanza_pos_nlp) == expected

@pytest.mark.relaxed_compare
def test_plural_case(baseline, nlp, pos_data, expected):
    baseline.append("runs")
    nlp.append("run")
    pos_data[0].append(["VERB"])
    pos_data[1].append(["runs"])
    expected[1].append("run")
    expected[2].append("runs")

    assert relaxed_compare(baseline, nlp, pos_data, stanza_pos_nlp) == expected

@pytest.mark.relaxed_compare
def test_numeral(baseline, nlp, pos_data, expected):
    baseline.append("{0, 1/2, 2,3, 4, etc.}")
    nlp.append("valuable {0, 1/2, 2,3, 4, etc.}")
    pos_data[0].append(['NOUN', 'PUNCT', 'NUM', 'PUNCT', 'NUM', 'PUNCT', 'NUM', 'PUNCT', 'NOUN'])
    pos_data[1].append(['{0', ',', '1/2', ',', '2,3', ',', '4', ',', 'etc.}'])
    expected[0].append("{0, 1/2, 2,3, 4, etc.}")

    assert relaxed_compare(baseline, nlp, pos_data, stanza_pos_nlp) == expected

@pytest.mark.relaxed_compare
def test_who_what (baseline, nlp, pos_data, expected):
    baseline.append("who")
    baseline.append("what is effective")
    nlp.append("exactly who")
    nlp.append("what")
    pos_data[0].append(["PRON"])
    pos_data[0].append(['PRON', 'AUX', 'ADJ'])
    pos_data[1].append(["who"])
    pos_data[1].append(["what", "is", "effective"])
    expected[0].append("who")
    expected[0].append("what is effective")

    assert relaxed_compare(baseline, nlp, pos_data, stanza_pos_nlp) == expected

@pytest.mark.relaxed_compare
def test_different_alphabetic_case(baseline, nlp, pos_data, expected):
    nlp[1] = "LoaD EFfiCiEnTly"

    assert relaxed_compare(baseline, nlp, pos_data, stanza_pos_nlp) == expected

@pytest.mark.relaxed_compare
def test_negative (baseline, nlp, pos_data, expected):
    baseline.append("did not save")
    nlp.append("save")
    pos_data[0].append(["AUX", "PART", "VERB"])
    pos_data[1].append(["did", "not", "save"])
    expected[1].append("save")
    expected[2].append("did not save")

    assert relaxed_compare(baseline, nlp, pos_data, stanza_pos_nlp) == expected

@pytest.mark.relaxed_compare
def test_various_qualifiers(baseline, nlp, pos_data, expected):
    nlp[1] = "if quickly load beutifully and is secure."

    assert relaxed_compare(baseline, nlp, pos_data, stanza_pos_nlp) == expected

@pytest.mark.relaxed_compare
def test_split_two_case(baseline, nlp, pos_data, expected):
    baseline.append("user's stats")
    baseline.append("owners' data")
    nlp.append("user's")
    nlp.append("stats")
    nlp.append("owners'")
    nlp.append("data")
    pos_data[0].append(["NOUN", "PART", "NOUN"])
    pos_data[0].append(["NOUN", "PART", "NOUN"])
    pos_data[1].append(["user", "'s", "stats"])
    pos_data[1].append(["owners", "'", "data"])
    expected[1].append("user's")
    expected[1].append("stats")
    expected[1].append("owners'")
    expected[1].append("data")
    expected[2].append("user's stats")
    expected[2].append("owners' data")

    assert relaxed_compare(baseline, nlp, pos_data, stanza_pos_nlp) == expected

@pytest.mark.relaxed_compare
def test_particle(baseline, nlp, pos_data, expected):
    baseline.append("computer's usage")
    baseline.append("haven't submitted")
    nlp.append("computer usage")
    nlp.append("have submitted")
    pos_data[0].append(["NOUN", "PART", "NOUN"])
    pos_data[0].append(["AUX", "PART", "VERB"])
    pos_data[1].append(["computer", "'s", "usage"])
    pos_data[1].append(["have", "n't", "submitted"])
    expected[1].append("computer usage")
    expected[1].append("have submitted")
    expected[2].append("computer's usage")
    expected[2].append("haven't submitted")

    assert relaxed_compare(baseline, nlp, pos_data, stanza_pos_nlp) == expected

@pytest.mark.relaxed_compare
def test_data_typo(baseline, nlp, pos_data, expected):
    baseline.append("submitt")
    nlp.append("submit")
    pos_data[0].append(["PROPN"])
    pos_data[1].append(["submitt"])
    expected[1].append("submit")
    expected[2].append("submitt")

    assert relaxed_compare(baseline, nlp, pos_data, stanza_pos_nlp) == expected

@pytest.mark.relaxed_compare
def test_similar_case(baseline, nlp, pos_data, expected):
    baseline.append("come more often")
    baseline.append("come")
    nlp.append("come")
    pos_data[0].append(["VERB", "ADV", "ADV"])
    pos_data[0].append(["VERB"])
    pos_data[1].append(["come", "more", "often"])
    pos_data[1].append(["come"])
    expected[0] = ["come"] + expected [0]
    expected[2].append("come more often")

    assert relaxed_compare(baseline, nlp, pos_data, stanza_pos_nlp) == expected

@pytest.mark.relaxed_compare
def test_noun_and_verb(baseline, nlp, pos_data, expected):
    baseline.append("privately view")
    nlp.append("view") #stanza will see this "view" as a noun instead of a verb
    pos_data[0].append(["ADV", "VERB"])
    pos_data[1].append(["privately", "view"])
    expected[0].append("privately view")

    assert relaxed_compare(baseline, nlp, pos_data, stanza_pos_nlp) == expected

@pytest.mark.relaxed_compare
def test_adj_and_verb(baseline, nlp, pos_data, expected):
    baseline.append("correct") #stanza will see this "correct" as a adjective instead of a verb
    nlp.append("quickly correct") 
    pos_data[0].append(["ADJ"])
    pos_data[1].append(["correct"])
    expected[0].append("correct")

    assert relaxed_compare(baseline, nlp, pos_data, stanza_pos_nlp) == expected

@pytest.mark.relaxed_compare
def test_empty_baseline(nlp):
    baseline = []
    pos_data = [[],[]]
    expected = [[],nlp,[]]

    assert relaxed_compare(baseline, nlp, pos_data, stanza_pos_nlp) == expected

@pytest.mark.relaxed_compare
def test_empty_nlp(baseline, pos_data):
    nlp = []
    expected = [[],[],baseline]

    assert relaxed_compare(baseline, nlp, pos_data, stanza_pos_nlp) == expected