import unittest
import sys
import os
from datetime import datetime


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from mpin_security_checker.utils.demographic_utils import predict_demographic_strength


def to_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()

class TestDemographicModel(unittest.TestCase):

    def test_exact_match_dob(self):
        mpin = "0805"
        result = predict_demographic_strength(mpin,
            to_date("2004-08-05"), to_date("2005-01-01"),
            to_date("2020-12-12"), to_date("2021-06-20"))
        self.assertEqual(result, "WEAK")

    def test_jumbled_dob(self):
        mpin = "0508"  
        result = predict_demographic_strength(mpin,
            to_date("2004-08-05"), to_date("2005-01-01"),
            to_date("2020-12-12"), to_date("2021-06-20"))
        self.assertEqual(result, "WEAK")

    def test_match_spouse(self):
        mpin = "0101"
        result = predict_demographic_strength(mpin,
            to_date("2004-08-05"), to_date("2005-01-01"),
            to_date("2020-12-12"), to_date("2021-06-20"))
        self.assertEqual(result, "WEAK")

    def test_jumbled_anniversary(self):
        mpin = "2006"
        result = predict_demographic_strength(mpin,
            to_date("2004-08-05"), to_date("2005-01-01"),
            to_date("2020-12-12"), to_date("2021-06-20"))
        self.assertEqual(result, "WEAK")

    def test_strong_random_pin(self):
        mpin = "9581"
        result = predict_demographic_strength(mpin,
            to_date("2004-08-05"), to_date("2005-01-01"),
            to_date("2020-12-12"), to_date("2021-06-20"))
        self.assertEqual(result, "STRONG")

    def test_strong_6digit_random(self):
        mpin = "739102"
        result = predict_demographic_strength(mpin,
            to_date("2004-08-05"), to_date("2005-01-01"),
            to_date("2020-12-12"), to_date("2021-06-20"))
        self.assertEqual(result, "STRONG")

    def test_exact_anniversary(self):
        mpin = "0620"
        result = predict_demographic_strength(mpin,
            to_date("2004-08-05"), to_date("2005-01-01"),
            to_date("2020-12-12"), to_date("2021-06-20"))
        self.assertEqual(result, "WEAK")

    def test_jumbled_pet_dob(self):
        mpin = "1212"
        result = predict_demographic_strength(mpin,
            to_date("2004-08-05"), to_date("2005-01-01"),
            to_date("2020-12-12"), to_date("2021-06-20"))
        self.assertEqual(result, "WEAK")

if __name__ == '__main__':
    unittest.main(verbosity=2)
