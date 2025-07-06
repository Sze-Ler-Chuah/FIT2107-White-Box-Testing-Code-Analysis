import unittest

from src.business_logic import can_borrow_carpentry_tool
from src.data_mgmt import *

'''
____________________________________________________________________________
|Test Case | fees_owed > 0 | patron_age <= 18 | patron_age >= 90 | Outcome |
|    1     | False         | False            | False            | True    |
|    2     | False         | False            | True             | False   |
|    3     | False         | True             | False            | False   |
|    4     | False         | True             | True             | False   |
|    5     | True          | False            | False            | False   |
|    6     | True          | False            | True             | False   |
|    7     | True          | True             | False            | False   |
|    8     | True          | True             | True             | False   |
____________________________________________________________________________

Possible tests:

fees_owed > 0 : {1,5}
patron_age <= 18 : {1,3}
patron_age >= 90 : {1,2}

Possible optimal sets of tests using MC/DC: {1,2,3,5}

Set chosen: {1,2,3,5}
'''


class TestCanBorrowCarpentryTool(unittest.TestCase):
    #Test for test case 1: fees_owed > 0 = False, patron_age <= 18 = False, patron_age >= 90 = False
    def test_borrow_carpentry_tool_success(self):
        """
        Test to borrow a carpentry tool successfully.
        Patron within the age (19-89) and within the length of loan
        (14 for carpentry tool) and has no outstanding fee.
        """
        self.assertTrue(can_borrow_carpentry_tool(50, 10, 0.0, True))

    #Test for test case 2: fees_owed > 0 = False, patron_age <= 18 = False, patron_age >= 90 = True
    def test_borrow_carpentry_tool_fail_elderly_patron_type(self):
        """
        Test to unsuccessfully borrow a carpentry tool due to Elderly
        patron type.
        Patron age 90 and above and cannot borrow a carpentry tool.
        """
        self.assertFalse(can_borrow_carpentry_tool(95, 10, 0.0, True))

    #Test for test case 3: fees_owed > 0 = False, patron_age <= 18 = True, patron_age >= 90 = False
    def test_borrow_carpentry_tool_fail_minor_patron_type(self):
        """
        Test to unsuccessfully borrow a carpentry tool due to Minor
        patron type.
        Patron aged 18 and below and cannot borrow a carpentry tool
        """
        self.assertFalse(can_borrow_carpentry_tool(15, 10, 0.0, True))

    #Test for test case 5: fees_owed > 0 = True, patron_age <= 18 = False, patron_age >= 90 = False
    def test_borrow_carpentry_tool_fail_has_outstanding_fee(self):
        """
        Test to unsuccessfully borrow a carpentry tool due to outstanding fee.
        Patron within the age (19-89) and within the length of loan
        (14 for carpentry tool) but has outstanding fee.
        """
        self.assertFalse(can_borrow_carpentry_tool(50, 10, 10.0, True))
