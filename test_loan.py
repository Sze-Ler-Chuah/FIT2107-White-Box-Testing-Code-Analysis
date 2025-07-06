import unittest
from src.borrowable_item import *
from src.data_mgmt import *
from src.business_logic import *
from datetime import datetime

class TestLoan(unittest.TestCase):
    def test_str(self):
        """
        Test the string representation of a BorrowableItem object.
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
        loan = patron._loans[0]
        borrowable_item_expected_output = f"Item 8: Alice in the Wonderland (Book); due {datetime.now().strftime('%d/%m/%Y')}"
        
        self.assertEqual(str(loan), borrowable_item_expected_output)
