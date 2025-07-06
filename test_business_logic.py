import unittest
from datetime import datetime
from src.business_logic import *
from src.borrowable_item import *
from src.data_mgmt import *
from src.bat_ui import BatUI


class TestTypeOfPatron(unittest.TestCase):
    def test_error_age(self):
        """
        Test to check on Error patron type.
        Patron has a negative age(smaller than 0) thus the patron type is
        invalid(Error).
        """
        self.assertEqual(type_of_patron(-5), 'ERROR')

    def test_minor_age(self):
        """
        Test to check on Minor patron type.
        Patron has an age of 15(smaller than 18) thus the patron type is Minor.
        """
        self.assertEqual(type_of_patron(15), 'Minor')

    def test_adult_age(self):
        """
        Test to check on Adult patron type.
        Patron has an age of 50(>= 18 and < 90) thus the patron type is Adult.
        """
        self.assertEqual(type_of_patron(50), 'Adult')

    def test_elderly_age(self):
        """
        Test to check on Elderly patron type.
        Patron has an age of 95(>= 90) thus the patron type is Elderly.
        """
        self.assertEqual(type_of_patron(95), 'Elderly')


class TestCanBorrow(unittest.TestCase):
    def test_borrow_book_failure_length_of_loan(self):
        """
        Test to fail borrowing a book due to length of loan.
        Patron has an age of 15(No age restriction for borrowing books),
        exceeding the length of loan(> 56) and no fees owed.
        """
        self.assertFalse(can_borrow('Book', 15, 60, 0.0, True, True))

    def test_borrow_book_failure_fees_owed(self):
        """
        Test to fail borrowing a book due to having outstanding fees.
        Patron has an age of 15(No age restriction for borrowing books),
        within the length of loan(<= 56) but has fees owed(> 0.0).
        """
        self.assertFalse(can_borrow('Book', 15, 10, 10.0, True, True))

    def test_borrow_book_success(self):
        """
        Test to successfully borrow a book.
        Patron has an age of 15(No age restriction for borrowing books),
        within the length of loan(<= 56) and no fees owed.
        """
        self.assertTrue(can_borrow('Book', 15, 10, 0.0, True, True))

    def test_borrow_gardening_tool_success(self):
        """
        Test to successfully borrow a gardening tool.
        Patron has an age of 15
        (No age restriction for borrowing gardening tools),
        within the length of loan(<= 28) and no fees owed.
        """
        self.assertTrue(can_borrow('Gardening tool', 15, 10, 0.0, True, True))

    def test_borrow_gardening_tool_failure_length_of_loan(self):
        """
        Test to fail borrowing a gardening tool due to length of loan.
        Patron has an age of 15
        (No age restriction for borrowing gardening tools),
        exceeding the length of loan(> 28) and no fees owed.
        """
        self.assertFalse(can_borrow('Gardening tool', 15, 60, 0.0, True, True))

    def test_borrow_gardening_tool_failure_fees_owed(self):
        """
        Test to fail borrowing a gardening tool due to having outstanding fees.
        Patron has an age of 15
        (No age restriction for borrowing gardening tools),
        within the length of loan(<= 28) but has fees owed(> 0.0).
        """
        self.assertFalse(can_borrow('Gardening tool', 15, 10, 10.0, True, 
                                    True))

    def test_borrow_carpentry_tool_failure_length_of_loan(self):
        """
        Test to fail borrowing a carpentry tool due to length of loan.
        Patron has an age of 50(Within the age for Adult patron type),
        exceeding the length of loan(> 14) and no fees owed.
        """
        self.assertFalse(can_borrow('Carpentry tool', 50, 60, 0.0, True, True))

    def test_invalid_item(self):
        """
        Test to fail borrowing due to borrowing an invalid item.
        The item to be borrowed is 'BOOK' but not within the item type of
        'Book', 'Gardening tool' or 'Carpentry tool'.
        """
        self.assertFalse(can_borrow('BOOK', 50, 10, 0.0, True, True))


class TestCalculateDiscount(unittest.TestCase):
    def test_invalid_discount(self):
        """
        Test to check on Error discount.
        Patron has a negative age(smaller than 0) thus the discount
        is invalid(Error).
        """
        self.assertEqual(calculate_discount(-5), 'ERROR')

    def test_0_percent_discount(self):
        """
        Test to check on 0% discount.
        Patron has an age of 25 thus no discount applied as
        no discount is given to patrons under age of 50.
        """
        self.assertEqual(calculate_discount(25), 0)

    def test_10_percent_discount(self):
        """
        Test to check on 10% discount.
        Patron has an age of 50 thus 10% discount applied as
        patrons aged 50 and over, but under 65 receive a 10% discount.
        """
        self.assertEqual(calculate_discount(60), 10)

    def test_15_percent_discount(self):
        """
        Test to check on 15% discount.
        Patron has an age of 65 thus 15% discount applied as
        patrons aged 65 and over, but under 90 receive a 15% discount.
        """
        self.assertEqual(calculate_discount(75), 15)

    def test_100_percent_discount(self):
        """
        Test to check on 100% discount.
        Patron has an age of 95 thus 100% discount applied as
        patrons aged 90 and over receive a 100% discount.
        """
        self.assertEqual(calculate_discount(95), 100)

class TestProcessReturn(unittest.TestCase):
    def setUp(self):
        self.ui = BatUI(DataManager())
                #Create a BorrowableItem object
        self.item = BorrowableItem()
        item_json_record = {"item_id": 8,
                            "item_name": "Alice in the Wonderland",
                            "item_type": "Book",
                            "year": 2024,
                            "number_owned": 10,
                            "on_loan": 0
                            }
        self.item.load_data(item_json_record)
        
        #Create a Patron object
        self.patron = Patron()
        patron_json_record = {"patron_id": 101,
                              "name": "John Manor",
                              "age": 25,
                              "outstanding_fees": 0.00,
                              "gardening_tool_training": False,
                              "carpentry_tool_training": False,
                              "makerspace_training": False,
                              "loans": []
                              }
        self.patron.load_data(patron_json_record, [])
        self.patron._loans.append(Loan(self.item, datetime.now()))
    
    def test_process_return(self):
        """
        Test to successfully process a return.
        Patron returns an item and the loan is removed from the patron.
        """
        process_return(self.patron, 8)
        
        self.assertEqual(len(self.patron._loans), 0)
    
    
class TestProcessLoan(unittest.TestCase):
    def setUp(self):
        self.ui = BatUI(DataManager())
                #Create a BorrowableItem object
        self.item = BorrowableItem()
        item_json_record = {"item_id": 8,
                            "item_name": "Alice in the Wonderland",
                            "item_type": "Book",
                            "year": 2024,
                            "number_owned": 10,
                            "on_loan": 0
                            }
        self.item.load_data(item_json_record)
        
        #Create a Patron object
        self.patron = Patron()
        patron_json_record = {"patron_id": 101,
                              "name": "John Manor",
                              "age": 25,
                              "outstanding_fees": 0.00,
                              "gardening_tool_training": False,
                              "carpentry_tool_training": False,
                              "makerspace_training": False,
                              "loans": []
                              }
        self.patron.load_data(patron_json_record, [])
    
    def test_process_loan_success(self):
        """
        Test to successfully process a loan.
        At here, the new patron added has no outstanding fees and the length of
        loan is within 8 weeks as the item is a book.
        """
        original_loan_count = len(self.patron._loans)
        
        process_loan(self.patron, self.item, 10)
        
        self.assertEqual(len(self.patron._loans), original_loan_count + 1)
    
    def test_process_loan_failure(self):
        """
        Test to fail processing a loan.
        At here, the length of loan is exceeding 8 weeks as the item is a book.
        Thus, the loan is not processed.
        """
        original_loan_count = len(self.patron._loans)
        
        process_loan(self.patron, self.item, 100)

        self.assertEqual(len(self.patron._loans), original_loan_count)