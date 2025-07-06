import unittest
from src.borrowable_item import *
from src.data_mgmt import *
from src.business_logic import *

class TestBorrowableItem(unittest.TestCase):
    def test_load_data(self):
        """
        Test the loading of patron data from JSON.
        """
        item = BorrowableItem()
        
        json_record = {
            "item_id": 8,
            "item_name": "Book 1",
            "item_type": "Book",
            "year": 2024,
            "number_owned": 10,
            "on_loan": 0
        }
        
        item.load_data(json_record)
        
        self.assertEqual(item._id, 8)
        self.assertEqual(item._name, "Book 1")
        self.assertEqual(item._type, "Book")
        self.assertEqual(item._year, 2024)
        self.assertEqual(item._number_owned, 10)
        self.assertEqual(item._on_loan, 0)

    def test_str(self):
        item = BorrowableItem()
        
        json_record = {
            "item_id": 8,
            "item_name": "Alice in the Wonderland",
            "item_type": "Book",
            "year": 2024,
            "number_owned": 10,
            "on_loan": 0
        }
        
        item.load_data(json_record)

        """
        Test the string representation of a BorrowableItem object.
        """
        borrowable_item_expected_output = (
            "Item 8: Alice in the Wonderland (Book)\n"
            "Year: 2024\n"
            "0/10 on loan"
        )
        
        self.assertEqual(str(item), borrowable_item_expected_output)
        



   