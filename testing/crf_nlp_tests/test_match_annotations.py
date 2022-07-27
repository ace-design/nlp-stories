import pytest
from nlp.nlp_tools.crf.crf_nlp import match_annotations
import stanza

stanza.download('en')
global stanza_pos_nlp
stanza_nlp = stanza.Pipeline('en')

@pytest.mark.match_annotations
def test_normal_case():
    y_pred = ["O", "O", "O", "O", "PER", "O", "O", "O", "O", "P-ACT", "O", "P-ENT", "O", "O", "O", "O", "S-ACT", "O", "O", "O", "S-ENT"]

    testing_set = [ ("11", "NUM", "O"), (":", "PUNCT", "O"), ("As", "ADP", "O"), ("an", "DET", "O"), ("applicant", "NOUN", "PER"), (",", "PUNCT", "O"), ("I", "PRON", "O"),\
                    ("want", "VERB", "O"), ("to", "PART", "O"), ("create", "VERB", "P-ACT"),("a", "DET", "O"), ("button", "NOUN", "P-ENT"), ("so", "SCONJ", "O"), ("that", "SCONJ", "O"),\
                    ("I", "PRON", "O"), ("can", "AUX", "O"), ("move", "VERB", "S-ACT"), ("to", "ADP", "O"), ("the", "DET", "O"), ("next", "ADJ", "O"), ("page", "NOUN", "S-ENT")]

    story_text = "11: As an applicant, I want to create a button so that I can move to the next page"

    expected = (["applicant"], ["create"], ["move"], ["button"], ["page"])

    assert match_annotations(y_pred, testing_set, story_text, stanza_nlp) == expected

@pytest.mark.match_annotations
def test_multiple_annotations():
    y_pred = ["O", "O", "O", "O", "PER", "PER", "PER", "O", "O", "O", "O", "P-ACT", "O", "P-ENT", "P-ENT", "O", "O", "O", "O", "S-ACT", "O", "O", "S-ENT", "S-ENT", "O", "S-ENT", "S-ENT"]

    testing_set = [ ("11", "NUM", "O"), (":", "PUNCT", "O"), ("As", "ADP", "O"), ("an", "DET", "O"),("smart", "NOUN", "PER"), ("GOV", "NOUN", "PER"), ("applicant", "NOUN", "PER"), (",", "PUNCT", "O"), ("I", "PRON", "O"),\
                    ("want", "VERB", "O"), ("to", "PART", "O"), ("create", "VERB", "P-ACT"),("a", "DET", "O"), ("button", "NOUN", "P-ENT"), ("unit", "NOUN", "P-ENT"), ("so", "SCONJ", "O"), ("that", "SCONJ", "O"),\
                    ("I", "PRON", "O"), ("can", "AUX", "O"), ("move", "VERB", "S-ACT"), ("to", "ADP", "O"), ("the", "DET", "O"), ("next", "ADJ", "S-ENT"), ("page", "NOUN", "S-ENT"), ("and", "CONJ", "O"), ("old", "NOUN", "S-ENT"), ("tab", "NOUN", "S-ENT")]

    story_text = "11: As an smart GOV applicant, I want to create a button unit so that I can move to the next page and old tab"

    expected = (["smart GOV applicant"], ["create"], ["move"], ["button unit"], ["next page", "old tab"])

    assert match_annotations(y_pred, testing_set, story_text, stanza_nlp) == expected

@pytest.mark.match_annotations
def test_qualitative_actions():
    y_pred = ["O", "O", "O", "O", "PER", "O", "O", "O", "O", "P-ACT", "P-ACT", "O", "P-ENT", "O", "O", "O", "O", "S-ACT", "S-ACT", "O", "O", "O", "S-ENT"]

    testing_set = [ ("11", "NUM", "O"), (":", "PUNCT", "O"), ("As", "ADP", "O"), ("an", "DET", "O"), ("applicant", "NOUN", "PER"), (",", "PUNCT", "O"), ("I", "PRON", "O"),\
                    ("want", "VERB", "O"), ("to", "PART", "O"), ("quickly", "ADJ", "P-ACT"), ("create", "VERB", "P-ACT"),("a", "DET", "O"), ("button", "NOUN", "P-ENT"), ("so", "SCONJ", "O"), ("that", "SCONJ", "O"),\
                    ("I", "PRON", "O"), ("can", "AUX", "O"), ("move", "VERB", "S-ACT"), ("effectively", "ADJ", "S-ACT"), ("to", "ADP", "O"), ("the", "DET", "O"), ("next", "ADJ", "O"), ("page", "NOUN", "S-ENT")]

    story_text = "11: As an applicant, I want to quickly create a button so that I can move effectively to the next page"

    expected = (["applicant"], ["quickly create"], ["move effectively"], ["button"], ["page"])

    assert match_annotations(y_pred, testing_set, story_text, stanza_nlp) == expected

@pytest.mark.match_annotations
def test_double_actions():
    y_pred = ["O", "O", "O", "O", "PER", "O", "O", "O", "O", "P-ACT", "P-ACT", "O", "P-ENT", "O", "O", "O", "O", "S-ACT", "O", "O", "O", "S-ENT"]

    testing_set = [ ("11", "NUM", "O"), (":", "PUNCT", "O"), ("As", "ADP", "O"), ("an", "DET", "O"), ("applicant", "NOUN", "PER"), (",", "PUNCT", "O"), ("I", "PRON", "O"),\
                    ("want", "VERB", "O"), ("to", "PART", "O"), ("start", "VERB", "P-ACT"), ("creating", "VERB", "P-ACT"),("a", "DET", "O"), ("button", "NOUN", "P-ENT"), ("so", "SCONJ", "O"), ("that", "SCONJ", "O"),\
                    ("I", "PRON", "O"), ("can", "AUX", "O"), ("move", "VERB", "S-ACT"), ("to", "ADP", "O"), ("the", "DET", "O"), ("next", "ADJ", "O"), ("page", "NOUN", "S-ENT")]

    story_text = "11: As an applicant, I want to start creating a button so that I can move to the next page"

    expected = (["applicant"], ["start", "creating"], ["move"], ["button"], ["page"])

    assert match_annotations(y_pred, testing_set, story_text, stanza_nlp) == expected

@pytest.mark.match_annotations
def test_multiple_whitespaces():
    y_pred = ["O", "O", "O", "O", "PER", "O", "O", "O", "O", "P-ACT", "O", "P-ENT", "O", "O", "O", "O", "S-ACT", "O", "O", "O", "S-ENT"]

    testing_set = [ ("11", "NUM", "O"), (":", "PUNCT", "O"), ("As", "ADP", "O"), ("an", "DET", "O"), ("applicant", "NOUN", "PER"), (",", "PUNCT", "O"), ("I", "PRON", "O"),\
                    ("want", "VERB", "O"), ("to", "PART", "O"), ("create", "VERB", "P-ACT"),("a", "DET", "O"), ("button", "NOUN", "P-ENT"), ("so", "SCONJ", "O"), ("that", "SCONJ", "O"),\
                    ("I", "PRON", "O"), ("can", "AUX", "O"), ("move", "VERB", "S-ACT"), ("to", "ADP", "O"), ("the", "DET", "O"), ("next", "ADJ", "O"), ("page", "NOUN", "S-ENT")]

    story_text = "11:   As an     applicant    , I want to create     a    button    so that   I can   move to the  next    page"

    expected = (["applicant"], ["create"], ["move"], ["button"], ["page"])

    assert match_annotations(y_pred, testing_set, story_text, stanza_nlp) == expected

@pytest.mark.match_annotations
def test_different_size_y_pred():
    y_pred = ["O", "O", "O", "O", "PER", "O", "O", "O", "O", "P-ACT", "O", "P-ENT", "O", "O", "O", "O"]

    testing_set = [ ("11", "NUM", "O"), (":", "PUNCT", "O"), ("As", "ADP", "O"), ("an", "DET", "O"), ("applicant", "NOUN", "PER"), (",", "PUNCT", "O"), ("I", "PRON", "O"),\
                    ("want", "VERB", "O"), ("to", "PART", "O"), ("create", "VERB", "P-ACT"),("a", "DET", "O"), ("button", "NOUN", "P-ENT"), ("so", "SCONJ", "O"), ("that", "SCONJ", "O"),\
                    ("I", "PRON", "O"), ("can", "AUX", "O"), ("move", "VERB", "S-ACT"), ("to", "ADP", "O"), ("the", "DET", "O"), ("next", "ADJ", "O"), ("page", "NOUN", "S-ENT")]

    story_text = "11: As an applicant, I want to create a button so that I can move to the next page"

    expected = (["applicant"], ["create"], [], ["button"], [])

    assert match_annotations(y_pred, testing_set, story_text, stanza_nlp) == expected

@pytest.mark.match_annotations
def test_different_size_testing_set():
    y_pred = ["O", "O", "O", "O", "PER", "O", "O", "O", "O", "P-ACT", "O", "P-ENT", "O", "O", "O", "O"]

    testing_set = [ ("11", "NUM", "O"), (":", "PUNCT", "O"), ("As", "ADP", "O"), ("an", "DET", "O"), ("applicant", "NOUN", "PER"), (",", "PUNCT", "O"), ("I", "PRON", "O"),\
                    ("want", "VERB", "O"), ("to", "PART", "O"), ("create", "VERB", "P-ACT"),("a", "DET", "O"), ("button", "NOUN", "P-ENT"), ("so", "SCONJ", "O")]

    story_text = "11: As an applicant, I want to create a button so that I can move to the next page"

    with pytest.raises(IndexError):
        result =  match_annotations(y_pred, testing_set, story_text, stanza_nlp)


@pytest.mark.match_annotations
def test_different_size_story_text():
    y_pred = ["O", "O", "O", "O", "PER", "O", "O", "O", "O", "P-ACT", "O", "P-ENT", "O", "O", "O", "O"]

    testing_set = [ ("11", "NUM", "O"), (":", "PUNCT", "O"), ("As", "ADP", "O"), ("an", "DET", "O"), ("applicant", "NOUN", "PER"), (",", "PUNCT", "O"), ("I", "PRON", "O"),\
                    ("want", "VERB", "O"), ("to", "PART", "O"), ("create", "VERB", "P-ACT"),("a", "DET", "O"), ("button", "NOUN", "P-ENT"), ("so", "SCONJ", "O"), ("that", "SCONJ", "O"),\
                    ("I", "PRON", "O"), ("can", "AUX", "O"), ("move", "VERB", "S-ACT"), ("to", "ADP", "O"), ("the", "DET", "O"), ("next", "ADJ", "O"), ("page", "NOUN", "S-ENT")]


    story_text  = "11: As an applicant, I want to create a button so that"

    expected = (["applicant"], ["create"], [], ["button"], [])

    assert match_annotations(y_pred, testing_set, story_text, stanza_nlp) == expected

@pytest.mark.match_annotations
def test_no_white_space():
    y_pred = ["O", "O", "O", "O", "PER", "O", "O", "O", "O", "P-ACT", "O", "P-ENT", "O", "O", "O", "O", "S-ACT", "O", "O", "O", "S-ENT"]

    testing_set = [ ("11", "NUM", "O"), (":", "PUNCT", "O"), ("As", "ADP", "O"), ("an", "DET", "O"), ("applicant", "NOUN", "PER"), (",", "PUNCT", "O"), ("I", "PRON", "O"),\
                    ("want", "VERB", "O"), ("to", "PART", "O"), ("create", "VERB", "P-ACT"),("a", "DET", "O"), ("button", "NOUN", "P-ENT"), ("so", "SCONJ", "O"), ("that", "SCONJ", "O"),\
                    ("I", "PRON", "O"), ("can", "AUX", "O"), ("move", "VERB", "S-ACT"), ("to", "ADP", "O"), ("the", "DET", "O"), ("next", "ADJ", "O"), ("page", "NOUN", "S-ENT")]

    story_text = "11:As anapplicant, I want tocreate a buttonsothatI can move tothe nextpage"

    expected = (["applicant"], ["create"], ["move"], ["button"], ["page"])

    assert match_annotations(y_pred, testing_set, story_text, stanza_nlp) == expected