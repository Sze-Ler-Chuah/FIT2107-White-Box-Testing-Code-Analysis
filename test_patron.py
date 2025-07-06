import unittest
from src.data_mgmt import *
from src.patron import *
from src.business_logic import *


class TestLoadData(unittest.TestCase):
        
    def test_load_data(self):
        """
        Test the loading of patron data from JSON.
        We will use multiple assert to check all the attributes of the patron object.
        """
        patron = Patron()
        patron_json_record = {"patron_id": 101,
                              "name": "John Manor",
                              "age": 25,
                              "outstanding_fees": 7.45,
                              "gardening_tool_training": False,
                              "carpentry_tool_training": False,
                              "makerspace_training": False,
                              "loans": []
                              }

        patron.load_data(patron_json_record, [])
        self.assertEqual(patron._id, 101)
        self.assertEqual(patron._name, "John Manor")
        self.assertEqual(patron._age, 25)
        self.assertEqual(patron._outstanding_fees, 7.45)
        self.assertFalse(patron._gardening_tool_training)
        self.assertFalse(patron._carpentry_tool_training)
        self.assertFalse(patron._makerspace_training)

class TestLoadLoans(unittest.TestCase):
    def test_load_loans(self):
        """
        Test the loading of patron loans from JSON.
        At here, we will test the number of loans and the item ID of the loans.
        Therfore, the number of assert statements will be based on the loan of the patron.
        """
        patron = Patron()
        patron_json_record = {"patron_id": 101,
                              "name": "John Manor",
                              "age": 25,
                              "outstanding_fees": 7.45,
                              "gardening_tool_training": False,
                              "carpentry_tool_training": False,
                              "makerspace_training": False,
                              "loans": []
                              }
        patron.load_data(patron_json_record, [])
        
        loans = patron.load_loans(patron_json_record["loans"], [])
        self.assertEqual(len(loans), 0)

class TestFindLoan(unittest.TestCase):
    def test_find_loan_has_loan(self):
        """
        Test to find a loan that exists.
        """
        patron = Patron()
        patron_json_record = {"patron_id": 101,
                              "name": "John Manor",
                              "age": 25,
                              "outstanding_fees": 7.45,
                              "gardening_tool_training": False,
                              "carpentry_tool_training": False,
                              "makerspace_training": False,
                              "loans": []
                              }
        patron.load_data(patron_json_record, [])
        
        item = BorrowableItem()
        item_json_record = {"item_id": 8,
                            "item_name": "Alice in the Wonderland",
                            "item_type": "Book",
                            "year": 2024,
                            "number_owned": 10,
                            "on_loan": 0
                            }
        item.load_data(item_json_record)
        
        patron._loans.append(Loan(item, datetime.now()))
        
        result = patron.find_loan(8)
        self.assertEqual(result, patron._loans[0])
    
    def test_find_loan_no_loan(self):
        """
        Test to find a loan that does not exist.
        """
        patron = Patron()
        patron_json_record = {"patron_id": 101,
                              "name": "John Manor",
                              "age": 25,
                              "outstanding_fees": 7.45,
                              "gardening_tool_training": False,
                              "carpentry_tool_training": False,
                              "makerspace_training": False,
                              "loans": []
                              }
        patron.load_data(patron_json_record, [])
        
        result = patron.find_loan(1)
        self.assertEqual(result, None)

class TestSetNewPatronData(unittest.TestCase):
    def test_set_new_patron_data(self):
        """
        Test to set new patron data.
        The patron's ID, name, and age are set to new values.
        """
        patron = Patron()
        patron.set_new_patron_data(1, "Albert Jackson", 25)
        self.assertEqual(patron._id, 1)
        self.assertEqual(patron._name, "Albert Jackson")
        self.assertEqual(patron._age, 25)
        self.assertEqual(patron._outstanding_fees, 0.0)
        self.assertFalse(patron._gardening_tool_training)
        self.assertFalse(patron._carpentry_tool_training)
        self.assertFalse(patron._makerspace_training)


class TestStr(unittest.TestCase):
    def test_str_complete_gardening_only(self):
        """
        Test the string representation of a Patron object with only gardening tools training.
        """
        patron = Patron()
        patron_json_record = {"patron_id": 101,
                              "name": "John Manor",
                              "age": 25,
                              "outstanding_fees": 7.45,
                              "gardening_tool_training": True,
                              "carpentry_tool_training": False,
                              "makerspace_training": False,
                              "loans": []
                              }
        patron.load_data(patron_json_record, [])
        
        expected_str = (
            "Patron 101: John Manor (aged 25)\n"
            "Outstanding fees: $7.45\n"
            "Completed training:\n"
            " - gardening tools\n"
            "No current loans"
        )  
        self.assertEqual(str(patron), expected_str)
    
    def test_str_complete_carpentry_only(self):
        """
        Test the string representation of a Patron object with only carpentry tools training.
        """
        patron = Patron()
        patron_json_record = {"patron_id": 101,
                              "name": "John Manor",
                              "age": 25,
                              "outstanding_fees": 7.45,
                              "gardening_tool_training": False,
                              "carpentry_tool_training": True,
                              "makerspace_training": False,
                              "loans": []
                              }
        patron.load_data(patron_json_record, [])
        
        expected_str = (
            "Patron 101: John Manor (aged 25)\n"
            "Outstanding fees: $7.45\n"
            "Completed training:\n"
            " - carpentry tools\n"
            "No current loans"
        )  
        self.assertEqual(str(patron), expected_str)
        
    def test_str_complete_makerspace_only(self):
        """
        Test the string representation of a Patron object with only makerspace training.
        """
        patron = Patron()
        patron_json_record = {"patron_id": 101,
                              "name": "John Manor",
                              "age": 25,
                              "outstanding_fees": 7.45,
                              "gardening_tool_training": False,
                              "carpentry_tool_training": False,
                              "makerspace_training": True,
                              "loans": []
                              }
        patron.load_data(patron_json_record, [])
        
        expected_str = (
            "Patron 101: John Manor (aged 25)\n"
            "Outstanding fees: $7.45\n"
            "Completed training:\n"
            " - makerspace\n"
            "No current loans"
        )  
        self.assertEqual(str(patron), expected_str)
    
    def test_str_multiple_loans(self):
        """
        Test the string representation of a Patron object with multiple loans.
        """
        patron = Patron()
        patron_json_record = {"patron_id": 101,
                              "name": "John Manor",
                              "age": 25,
                              "outstanding_fees": 7.45,
                              "gardening_tool_training": False,
                              "carpentry_tool_training": False,
                              "makerspace_training": False,
                              "loans": []
                              }
        patron.load_data(patron_json_record, [])
        
        item_one = BorrowableItem()
        item_one_json_record = {"item_id": 8,
                                "item_name": "Alice in the Wonderland",
                                "item_type": "Book",
                                "year": 2024,
                                "number_owned": 10,
                                "on_loan": 0
                                }
        item_one.load_data(item_one_json_record)
        
        patron._loans.append(Loan(item_one, datetime.now()))

        item_two = BorrowableItem()
        item_two_json_record = {"item_id": 9,
                                "item_name": "Beauty and the Beast",
                                "item_type": "Book",
                                "year": 2024,
                                "number_owned": 10,
                                "on_loan": 0
                                }
        item_two.load_data(item_two_json_record)
        
        patron._loans.append(Loan(item_two, datetime.now()))
        
        expected_str = (
            "Patron 101: John Manor (aged 25)\n"
            "Outstanding fees: $7.45\n"
            "Completed training: NONE\n"
            "2 active loans:\n"
            f" - Item 8: Alice in the Wonderland (Book); due {datetime.now().strftime('%d/%m/%Y')}\n"
            f" - Item 9: Beauty and the Beast (Book); due {datetime.now().strftime('%d/%m/%Y')}"
        )  
        
        self.assertEqual(str(patron), expected_str)
        
    
    def test_str_no_completed_training(self):
        """
        Test the string representation of a Patron object with no completed training.
        """
        patron = Patron()
        patron_json_record = {"patron_id": 101,
                              "name": "John Manor",
                              "age": 25,
                              "outstanding_fees": 7.45,
                              "gardening_tool_training": False,
                              "carpentry_tool_training": False,
                              "makerspace_training": False,
                              "loans": []
                              }
        patron.load_data(patron_json_record, [])
        
        expected_str = (
            "Patron 101: John Manor (aged 25)\n"
            "Outstanding fees: $7.45\n"
            "Completed training: NONE\n"
            "No current loans"
        )  
        
        self.assertEqual(str(patron), expected_str)
    
    def test_str_one_active_loan(self):
        """
        Test the string representation of a Patron object with no completed training.
        """
        patron = Patron()
        patron_json_record = {"patron_id": 101,
                              "name": "John Manor",
                              "age": 25,
                              "outstanding_fees": 7.45,
                              "gardening_tool_training": False,
                              "carpentry_tool_training": False,
                              "makerspace_training": False,
                              "loans": []
                              }
        patron.load_data(patron_json_record, [])
        
        item = BorrowableItem()
        item_json_record = {"item_id": 8,
                            "item_name": "Alice in the Wonderland",
                            "item_type": "Book",
                            "year": 2024,
                            "number_owned": 10,
                            "on_loan": 0
                            }
        item.load_data(item_json_record)
        
        patron._loans.append(Loan(item, datetime.now()))
        
        expected_str = (
            "Patron 101: John Manor (aged 25)\n"
            "Outstanding fees: $7.45\n"
            "Completed training: NONE\n"
            "1 active loan:\n"
            f" - Item 8: Alice in the Wonderland (Book); due {datetime.now().strftime('%d/%m/%Y')}"
        )  
        
        self.assertEqual(str(patron), expected_str)
