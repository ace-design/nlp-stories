import pytest
from nlp.nlp_tools.crf.create_crf_input import pos_tags
import stanza


stanza.download('en')
global stanza_pos_nlp
stanza_nlp = stanza.Pipeline('en')


@pytest.mark.pos_tags
def test_normal_case():
    text = "11: As an applicant, I want to create a button so that I can move to the next page"
    annotated_story = ["","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","A","A","A","A","A","A","","","","E","E","E","E","E","E","","","","","","","","","","","","","","","","a","a","a","a","","","","","","","","","","","","","","e","e","e","e"]

    expected = [("11", "NUM", "O"), (":", "PUNCT", "O"), ("As", "ADP", "O"), ("an", "DET", "O"), ("applicant", "NOUN", "PER"), (",", "PUNCT", "O"), ("I", "PRON", "O"),\
                ("want", "VERB", "O"), ("to", "PART", "O"), ("create", "VERB", "P-ACT"),("a", "DET", "O"), ("button", "NOUN", "P-ENT"), ("so", "SCONJ", "O"), ("that", "SCONJ", "O"),\
                ("I", "PRON", "O"), ("can", "AUX", "O"), ("move", "VERB", "S-ACT"), ("to", "ADP", "O"), ("the", "DET", "O"), ("next", "ADJ", "O"), ("page", "NOUN", "S-ENT")]

    assert pos_tags(text, annotated_story, stanza_nlp) == expected

@pytest.mark.pos_tags
def test_same_annotation_across_mulitple_words():
    text = "11: As an applicant, I want to create a button so that I can move to the next page"
    annotated_story = ["","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","A","A","A","A","A","A","","","","E","E","E","E","E","E","","","","","","","","","","","","a","a","a","a","a","a","a","a","","","","","","","","","e","e","e","e","e","e","e","e","e"]

    expected = [("11", "NUM", "O"), (":", "PUNCT", "O"), ("As", "ADP", "O"), ("an", "DET", "O"), ("applicant", "NOUN", "PER"), (",", "PUNCT", "O"), ("I", "PRON", "O"),\
                ("want", "VERB", "O"), ("to", "PART", "O"), ("create", "VERB", "P-ACT"),("a", "DET", "O"), ("button", "NOUN", "P-ENT"), ("so", "SCONJ", "O"), ("that", "SCONJ", "O"),\
                ("I", "PRON", "O"), ("can", "AUX", "S-ACT"), ("move", "VERB", "S-ACT"), ("to", "ADP", "O"), ("the", "DET", "O"), ("next", "ADJ", "S-ENT"), ("page", "NOUN", "S-ENT")]

    assert pos_tags(text, annotated_story, stanza_nlp) == expected

@pytest.mark.pos_tags
def test_same_annotation_seperated_by_hyphen():
    text = "11: As an applicant, I want to create a button so that I can move to the next-page"
    annotated_story = ["","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","A","A","A","A","A","A","","","","E","E","E","E","E","E","","","","","","","","","","","","a","a","a","a","a","a","a","a","","","","","","","","","e","e","e","e","e","e","e","e","e"]

    expected = [("11", "NUM", "O"), (":", "PUNCT", "O"), ("As", "ADP", "O"), ("an", "DET", "O"), ("applicant", "NOUN", "PER"), (",", "PUNCT", "O"), ("I", "PRON", "O"),\
                ("want", "VERB", "O"), ("to", "PART", "O"), ("create", "VERB", "P-ACT"),("a", "DET", "O"), ("button", "NOUN", "P-ENT"), ("so", "SCONJ", "O"), ("that", "SCONJ", "O"),\
                ("I", "PRON", "O"), ("can", "AUX", "S-ACT"), ("move", "VERB", "S-ACT"), ("to", "ADP", "O"), ("the", "DET", "O"), ("next", "ADJ", "S-ENT"), ("-", "PUNCT", "S-ENT"), ("page", "NOUN", "S-ENT")]

    assert pos_tags(text, annotated_story, stanza_nlp) == expected

@pytest.mark.pos_tags
def test_multiple_whitespaces():
    text = "11:   As   an   applicant,  I want to create a button so that I can move to the next-page"
    annotated_story = ["","","","","","","","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","","A","A","A","A","A","A","","","","E","E","E","E","E","E","","","","","","","","","","","","a","a","a","a","a","a","a","a","","","","","","","","","e","e","e","e","e","e","e","e","e"]

    expected = [("11", "NUM", "O"), (":", "PUNCT", "O"), ("As", "ADP", "O"), ("an", "DET", "O"), ("applicant", "NOUN", "PER"), (",", "PUNCT", "O"), ("I", "PRON", "O"),\
                ("want", "VERB", "O"), ("to", "PART", "O"), ("create", "VERB", "P-ACT"),("a", "DET", "O"), ("button", "NOUN", "P-ENT"), ("so", "SCONJ", "O"), ("that", "SCONJ", "O"),\
                ("I", "PRON", "O"), ("can", "AUX", "S-ACT"), ("move", "VERB", "S-ACT"), ("to", "ADP", "O"), ("the", "DET", "O"), ("next", "ADJ", "S-ENT"), ("-", "PUNCT", "S-ENT"), ("page", "NOUN", "S-ENT")]

    assert pos_tags(text, annotated_story, stanza_nlp) == expected

@pytest.mark.pos_tags
def test_different_size_text():
    text = "11: As an applicant, I want to create a button so that I can move to"
    annotated_story = ["","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","A","A","A","A","A","A","","","","E","E","E","E","E","E","","","","","","","","","","","","a","a","a","a","a","a","a","a","","","","","","","","","e","e","e","e","e","e","e","e","e"]

    with pytest.raises(IndexError):
        result = pos_tags(text, annotated_story, stanza_nlp)

@pytest.mark.pos_tags
def test_different_size_annotated_story():
    text = "11: As an applicant, I want to create a button so that I can move to the next page"
    annotated_story = ["","","","","","","","","","","P","P","P","P","P","P","P","P","P","","","","","","","","","","","","","A","A","A","A","A","A","","","","E","E","E","E","E","E"]

    with pytest.raises(Exception):
        result = pos_tags(text, annotated_story, stanza_nlp)