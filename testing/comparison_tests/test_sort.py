import copy
import pytest 
from compare.comparison import sort

@pytest.fixture
def baseline_data():
    text = ["abc", "def", "ghi", "jkl", "mno"]
    persona = [["cat"], ["dog"], ["horse"], ["pig"], ["cow"]]
    entity = [["shed"], ["tab"], ["book"], ["data", "cache"], ["file"]]
    action = [["jumps"], ["leaps"], ["carries"], ["click"], ["save"]]
    
    baseline_data = [text, persona, entity, action]

    return baseline_data

@pytest.fixture
def nlp_tool_data():
    text = ["mno", "abc", "ghi", "def", "jkl"]
    persona = [["cat"], ["moose"], ["horse"], ["cheetah"], ["cow"]]
    entity = [["house"], ["tab"], ["paper"], ["data", "cache"], ["file"]]
    action = [["jumps"], ["load"], ["carries"], ["click"], ["delete"]]
    
    nlp_tool_data = [text, persona, entity, action]

    return nlp_tool_data

@pytest.fixture
def pos_data():
    persona_pos = [[["Noun"], ["cat"]], [["Noun"], ["dog"]], [["Noun"], ["horse"]], [["Noun"], ["pig"]], [["Noun"], ["cow"]]]
    entity_pos = [[["Noun"], ["shed"]], [["Noun"], ["tab"]], [["Noun"], ["book"]], [["Noun", "Noun"], ["data", "cache"]], [["Noun"], ["file"]]]
    action_pos = [[["Verb"], ["jumps"]], [["Verb"], ["leaps"]], [["Verb"], ["carries"]], [["Verb"], ["click"]], [["Verb"], ["save"]]]

    pos_data = [persona_pos, entity_pos, action_pos]

    return pos_data

@pytest.fixture
def expected(baseline_data, pos_data):
    sorted_baseline_data =copy.deepcopy(baseline_data)
    sorted_pos_data = copy.deepcopy(pos_data)

    text = ["abc","def","ghi", "jkl", "mno"]
    persona = [["moose"],["cheetah"],["horse"], ["cow"], ["cat"]]
    entity = [["tab"],["data", "cache"],["paper"], ["file"], ["house"]]
    action = [["load"],["click"], ["carries"], ["delete"], ["jumps"]]

    sorted_nlp_data = [text, persona, entity, action]

    missing_text = [[],[]]

    expected = (sorted_baseline_data, sorted_nlp_data, sorted_pos_data, missing_text)

    return expected

@pytest.mark.sort
def test_normal_case(baseline_data, nlp_tool_data, pos_data, expected):
    assert sort(baseline_data, nlp_tool_data, pos_data) == expected

@pytest.mark.sort
def test_missing_nlp_tool_data (baseline_data, nlp_tool_data, pos_data, expected):

    del nlp_tool_data[0][2]
    del nlp_tool_data[1][2]
    del nlp_tool_data[2][2]
    del nlp_tool_data[3][2]  

    del expected[0][0][2]
    del expected[0][1][2]
    del expected[0][2][2]
    del expected[0][3][2]
    del expected[1][0][2]
    del expected[1][1][2]
    del expected[1][2][2]
    del expected[1][3][2]
    del expected[2][0][2]
    del expected[2][1][2]
    del expected[2][2][2]

    expected[3][1].append("ghi")

    assert sort(baseline_data, nlp_tool_data, pos_data) == expected

@pytest.mark.sort
def test_missing_baseline_data(baseline_data, nlp_tool_data, pos_data, expected):

    print(baseline_data[1][3])

    del baseline_data[0][3]
    del baseline_data[1][3]
    del baseline_data[2][3]
    del baseline_data[3][3]  

    del pos_data[0][3]
    del pos_data[1][3]
    del pos_data[2][3]

    del expected[0][0][3]
    del expected[0][1][3]
    del expected[0][2][3]
    del expected[0][3][3]
    del expected[1][0][3]
    del expected[1][1][3]
    del expected[1][2][3]
    del expected[1][3][3]
    del expected[2][0][3]
    del expected[2][1][3]
    del expected[2][2][3]

    expected[3][0].append("jkl")

    assert sort(baseline_data, nlp_tool_data, pos_data) == expected

@pytest.mark.sort
def test_missing_both_data(baseline_data, nlp_tool_data, pos_data, expected):
    nlp_tool_data[0].append("xyz")
    nlp_tool_data[1].append(["manager"])
    nlp_tool_data[2].append(["remove"])
    nlp_tool_data[3].append(["dataset"])
    
    del nlp_tool_data[0][1]
    del nlp_tool_data[1][1]
    del nlp_tool_data[2][1]
    del nlp_tool_data[3][1]  

    del expected[0][0][0]
    del expected[0][1][0]
    del expected[0][2][0]
    del expected[0][3][0]
    del expected[1][0][0]
    del expected[1][1][0]
    del expected[1][2][0]
    del expected[1][3][0]
    del expected[2][0][0]
    del expected[2][1][0]
    del expected[2][2][0]

    expected[3][0].append("xyz")
    expected[3][1].append("abc")

    assert sort(baseline_data, nlp_tool_data, pos_data) == expected

@pytest.mark.sort
def test_empty_baseline_data(nlp_tool_data, pos_data):
    baseline_data = [[],[],[],[]]

    expected = ([[],[],[],[]],[[],[],[],[]],[[],[],[]],[["mno", "abc", "ghi", "def", "jkl"],[]])

    assert sort(baseline_data, nlp_tool_data, pos_data) == expected

@pytest.mark.sort
def test_slight_difference_text(baseline_data, nlp_tool_data, pos_data, expected):

    nlp_tool_data[0][2] = "gzi"

    del expected[0][0][2]
    del expected[0][1][2]
    del expected[0][2][2]
    del expected[0][3][2]
    del expected[1][0][2]
    del expected[1][1][2]
    del expected[1][2][2]
    del expected[1][3][2]
    del expected[2][0][2]
    del expected[2][1][2]
    del expected[2][2][2]

    expected[3][0].append("gzi")
    expected[3][1].append("ghi")

    assert sort(baseline_data, nlp_tool_data, pos_data) == expected
