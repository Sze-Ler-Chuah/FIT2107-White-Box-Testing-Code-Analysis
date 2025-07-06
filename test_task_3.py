import unittest

from src.business_logic import can_use_makerspace


'''
Paths:

1) 135 -> 148 -> 150 -> 151 -> 153 -> 154 -> 161 -> 162 -> 164
2) 135 -> 148 -> 150 -> 151 -> 153 -> 154 -> 161 -> 164
3) 135 -> 148 -> 150 -> 151 -> 153 -> 155 -> 156 -> 161 -> 162 -> 164
4) 135 -> 148 -> 150 -> 151 -> 153 -> 155 -> 156 -> 161 -> 164
5) 135 -> 148 -> 150 -> 151 -> 153 -> 155 -> 157 -> 158 -> 159 -> 161 -> 162 -> 164
6) 135 -> 148 -> 150 -> 151 -> 153 -> 155 -> 157 -> 158 -> 159 -> 161 -> 164

Feasible paths:

2) 135 -> 148 -> 150 -> 151 -> 153 -> 154 -> 161 -> 164
4) 135 -> 148 -> 150 -> 151 -> 153 -> 155 -> 156 -> 161 -> 164
5) 135 -> 148 -> 150 -> 151 -> 153 -> 155 -> 157 -> 158 -> 159 -> 161 -> 162 -> 164
6) 135 -> 148 -> 150 -> 151 -> 153 -> 155 -> 157 -> 158 -> 159 -> 161 -> 164

'''


class TestCanUserMakerSpace(unittest.TestCase):
    #Test for path 2: 135 -> 148 -> 150 -> 151 -> 153 -> 154 -> 161 -> 164
    def test_error_patron_type(self):
        """
        Test to unsuccessfully use the makerspace due to Error patron type.
        Patron has a negative age thus the patron type is "Error"
        and cannot use the makerspace.
        """
        self.assertFalse(can_use_makerspace(-5, 0.00, True))

    #Test for path 4: 135 -> 148 -> 150 -> 151 -> 153 -> 155 -> 156 -> 161 -> 164
    #At here, the patron being tested can be Elderly or Minor and we have chosen to test for Minor
    def test_minor_patron_type(self):
        """
        Test to unsuccessfully use the makerspace due to Minor patron type.
        Patron is a minor and cannot use the makerspace.
        """
        self.assertFalse(can_use_makerspace(15, 0.00, True))

    #Test for path 5: 135 -> 148 -> 150 -> 151 -> 153 -> 155 -> 157 -> 158 -> 159 -> 161 -> 162 -> 164
    def test_adult_patron_type_has_outstanding_fee(self):
        """
        Test to unsuccessfully use the makerspace due to outstanding fee.
        Patron is an adult and has completed makerspace training but has
        outstanding fee.
        """
        self.assertFalse(can_use_makerspace(50, 1.00, True))

    #Test for path 6: 135 -> 148 -> 150 -> 151 -> 153 -> 155 -> 157 -> 158 -> 159 -> 161 -> 164
    def test_adult_patron_type_no_outstanding_fees_has_completed_makerspace_training(self):
        """
        Test to use the makerspace successfully.
        Patron is an adult and has completed makerspace training and has no
        outstanding fee.
        """
        self.assertTrue(can_use_makerspace(50, 0.00, True))
