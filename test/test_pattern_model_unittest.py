
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)  


import pytest
from mpin_security_checker.utils.model_utils import load_model, predict_strength
from mpin_security_checker.utils.pattern_checker import get_pattern_type


classifier, regressor, encoder = load_model()


test_cases = [

    ("1111", "weak"),
    ("000000", "weak"),
    ("777777", "weak"),


    ("1234", "weak"),
    ("654321", "weak"),


    ("2580", "weak"),
    ("159357", "weak"),
    ("147852", "weak"),


    ("1221", "weak"),
    ("123321", "weak"),


    ("2020", "weak"),
    ("1947", "weak"),
    ("200000", "weak"),
    ("151515", "weak"),


    ("9081", "strong"),
    ("3492", "strong"),
    ("7286", "strong"),
    ("841729", "strong"),
    ("9527", "strong"),
    ("739102", "strong"),
    ("901273", "strong"),
    ("432189", "strong"),
]

@pytest.mark.parametrize("mpin, expected", test_cases)
def test_mpin_strength_model(mpin, expected):
    pattern_type = get_pattern_type(mpin)
    guess_percent, label = predict_strength(classifier, regressor, encoder, mpin, pattern_type)

    actual = "weak" if label == 1 else "strong"
    assert actual == expected, f" Failed for {mpin} | Pattern: {pattern_type} | Expected: {expected}, Got: {actual}"
