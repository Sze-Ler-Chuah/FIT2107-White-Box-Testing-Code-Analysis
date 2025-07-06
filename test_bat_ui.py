import unittest
from unittest import mock
from src.bat_ui import BatUI
from src.data_mgmt import *
from src.loan import *
from datetime import datetime

class TestMainMenu(unittest.TestCase):
    def setUp(self):
        self.ui = BatUI(DataManager())
    
    @mock.patch('src.user_input.read_integer_range')
    def test_main_menu_invalid_choice(self, selection):
        """
        Test for invalid choice in the main menu.
        7 is an invalid choice as there are only 6 options in the main menu.
        """
        selection.return_value = 7
        
        #Run the main menu screen with the invalid choice
        self.ui.run_current_screen()
        
        #Verify that the current screen is still the main menu
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

class TestLoanItem(unittest.TestCase):
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

    @mock.patch('src.search.find_item_by_id')
    @mock.patch('src.user_input.read_string')
    def test_loan_item_fail_invalid_item(self, mock_read_string,
                                         mock_find_item_by_id):
        """
        Test to fail loaning an item due to invalid item id is inputted.
        The return value of the item id is 10 which is invalid.
        The return value of find_item_by_id is None.
        """
        #Mocking the input for the loan item process
        mock_read_string.return_value = "10"
        mock_find_item_by_id.return_value = None

        #Execute the loan item process
        self.ui._current_screen = self.ui._loan_item
        self.ui.run_current_screen()
        
        #Verify that the current screen is the main menu
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

    @mock.patch('src.search.find_item_by_id')
    @mock.patch('src.user_input.read_string')
    def test_loan_item_fail_valid_item_not_choice_of_item(self,
                                                          mock_read_string,
                                                          mock_find_item_by_id):
        """
        Test to fail loaning an item due to the inputted item id is not the
        choice of item.
        At here, the item id is 8 which is a book.
        The choice of item is 'n' which is not a valid choice.
        """
        #Mocking the input for the loan item process
        mock_read_string.side_effect = ["8","n"]
        mock_find_item_by_id.return_value = self.item

        #Execute the loan item process
        self.ui._current_screen = self.ui._loan_item
        self.ui.run_current_screen()

        #Verify that the current screen is the main menu
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

    @mock.patch('src.search.find_item_by_id')
    @mock.patch('src.user_input.read_string')    
    def test_loan_item_fail_invalid_patron(self,
                                           mock_read_string,
                                           mock_find_item_by_id):
        """
        Test to fail loaning an item due to invalid patron name
        At here the iten to be loaned is item id 8 which is a book.
        The patron name is 'Jane Major'(aged 25) which is not in the patron data.
        The patron name should be 'Jane Manor'.
        """
        #Mocking the input for the loan item process
        mock_read_string.side_effect = ["8", "y", "John Major", "25"]
        mock_find_item_by_id.return_value = self.item

        #Execute the loan item process
        self.ui._current_screen = self.ui._loan_item
        self.ui.run_current_screen()
    
        #Verify that the patron name is not the name of the patron created
        self.assertTrue(mock_read_string.return_value != self.patron._name)

        #Verify that the current screen is the main menu
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")
    
    @mock.patch('src.search.find_patron_by_name_and_age')
    @mock.patch('src.search.find_item_by_id')
    @mock.patch('src.user_input.read_string')    
    def test_loan_item_fail_invalid_length_of_loan(self,
                                                   mock_read_string,                                                   
                                                   mock_find_item_by_id,
                                                   find_name_and_age):
        """
        Test to fail loaning an item due to invalid length of loan.
        At here the iten to be loaned is item id 8 which is a book and it is the choice of item.
        The patron name is 'John Manor'(aged 25) and the length of loan is 100 days.
        This is invalid as books can only be loaned for 56 days at most.
        """
        #Mocking the input for the loan item process
        mock_read_string.side_effect = ["8", "y", "John Manor", "25", "100"]
        mock_find_item_by_id.return_value = self.item
        find_name_and_age.return_value = self.patron

        #Store the original loan count
        original_loan = len(self.patron._loans)

        #Execute the loan item process
        self.ui._current_screen = self.ui._loan_item
        self.ui.run_current_screen()

        #Verify that the loan count has not increased
        self.assertEqual(len(self.patron._loans), original_loan)

        #Verify that the current screen is the main menu
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

    @mock.patch('src.search.find_patron_by_name_and_age')
    @mock.patch('src.search.find_item_by_id')
    @mock.patch('src.user_input.read_string')
    def test_loan_item_success(self, mock_read_string,
                               mock_find_item_by_id,
                               mock_find_patron_by_name_and_age):
        """
        Test to successfully loan an item.
        At here the iten to be loaned is item id 8 which is a book and it is the choice of item.
        The patron name is 'John Manor'(aged 25) and the length of loan is 10 days
        which is valid (books can be loaned for 56 days at most).
        """
        #Mocking the input for the loan item process
        mock_read_string.side_effect = ["8", "y", "John Manor", "25", "10"]
        mock_find_item_by_id.return_value = self.item
        mock_find_patron_by_name_and_age.return_value = self.patron
        
        #Storing the original loan count
        original_loan = len(self.patron._loans)

        #Execute the loan item process
        self.ui._current_screen = self.ui._loan_item
        self.ui.run_current_screen()
        
        #Verify that the loan count has increased by 1
        self.assertEqual(len(self.patron._loans), original_loan + 1)
        
        #Verify that the current screen is the main menu
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

class TestReturnItem(unittest.TestCase):
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
    
    @mock.patch('src.search.find_patron_by_name_and_age')    
    @mock.patch('src.user_input.read_string')
    def test_return_item_fail_invalid_patron_name(self,
                                                  mock_read_string,
                                                  mock_find_patron_by_name_and_age):
        """
        Test to fail returning an item due to invalid patron name.
        At here, the patron name is 'John Major' which is not the name of the
        Patron object created.
        """
        #Mocking the input for the return item process
        mock_read_string.side_effect = ["John Major", "25"]
        # Mocking the return value of find_patron_by_name_and_age to be None
        mock_find_patron_by_name_and_age.return_value = None
        
        #Execute the return item process
        self.ui._current_screen = self.ui._return_item
        self.ui.run_current_screen()
        
        #Verify that the patron name is not the name of the patron created
        self.assertTrue(mock_read_string.return_value != self.patron._name)

        #=Verify that the current screen is the main menu
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

    @mock.patch('src.search.find_patron_by_name_and_age')    
    @mock.patch('src.user_input.read_string')
    def test_return_item_fail_invalid_patron_age(self, 
                                                 mock_read_string,
                                                 mock_find_patron_by_name_and_age):
        """
        Test to fail returning an item due to invalid patron age.
        At here, the patron with the name 'John Manor' has an age of 25 but the
        inputted age is 23.
        Thus, the patron is not found.
        """
        #Mocking the input for the return item process
        mock_read_string.side_effect = ["John Manor", "23"]
        # Mocking the return value of find_patron_by_name_and_age to be None
        mock_find_patron_by_name_and_age.return_value = None

        #Execute the return item process
        self.ui._current_screen = self.ui._return_item
        self.ui.run_current_screen()

        #Verify that the age of the patron is not the age of the patron created
        self.assertTrue(mock_read_string.return_value != self.patron._age)

        #Verify that the current screen is the main menu
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")
    
    @mock.patch('src.search.find_patron_by_name_and_age')
    @mock.patch('src.user_input.read_string')
    def test_return_item_success(self,
                                 mock_read_string,
                                 mock_find_patron_by_name_and_age):
        """
        Test to successfully return an item with multiple tries of inputting
        the item id.
        The patron tested to return item from loan is 'John Manor' (aged 25).
        At here, the item id is 8 which is a book and is valid.
        """
        #Mocking the input for the return item process
        mock_read_string.side_effect = ["John Manor", "25", "8"]

        # Mocking the return value of find_patron_by_name_and_age to be John Doe
        mock_find_patron_by_name_and_age.return_value = self.patron

        #Adding a loan to the patron 
        self.patron._loans.append(Loan(self.item, datetime.now()))

        #Storing the original loan count
        original_loan = len(self.patron._loans)
        
        #Execute the return item process
        self.ui._current_screen = self.ui._return_item
        self.ui.run_current_screen()

        #Verify that the loan count has decreased by 1
        self.assertEqual(len(self.patron._loans), original_loan - 1)
        #Verify that the current screen is the main menu
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

    @mock.patch('src.search.find_patron_by_name_and_age')
    @mock.patch('src.user_input.read_string')
    def test_return_item_success_with_invalid_choice_first(self,
                                                           mock_read_string,
                                                           mock_find_patron_by_name_and_age):
        """
        Test to successfully return an item with multiple tries of inputting
        the item id.
        The patron tested to return item from loan is 'John Manor' (aged 25).
        At here, the item id is 1 which is a book but is an invalid input.
        Thus when during the next try, the item id is 8 which is a book
        is valid and the item is returned successfully.
        """
        #Mocking the input for the return item process
        mock_read_string.side_effect = ["John Doe", "95", "1", "8"]

        # Mocking the return value of find_patron_by_name_and_age to be John Doe
        mock_find_patron_by_name_and_age.return_value = self.patron

        #Adding a loan to the patron 
        self.patron._loans.append(Loan(self.item, datetime.now()))

        #Storing the original loan count
        original_loan = len(self.patron._loans)
        
        #Execute the return item process
        self.ui._current_screen = self.ui._return_item
        self.ui.run_current_screen()

        #Verify that the loan count has decreased by 1
        self.assertEqual(len(self.patron._loans), original_loan - 1)

        #Verify that the current screen is the main menu
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

    @mock.patch('src.search.find_patron_by_name_and_age')
    @mock.patch('src.user_input.read_string')
    def test_return_item_success_with_str_first(self,
                                                mock_read_string,
                                                mock_find_patron_by_name_and_age):
        """
        Test to successfully return an item with multiple tries of inputting
        the item id.
        The patron tested to return item from loan is 'John Manor' (aged 25).
        At here, the item id is hello which is a string and is an invalid input.
        Thus when during the next try, the item id is 8 which is a book
        is valid and the item is returned successfully.
        """
        #Mocking the input for the return item process
        mock_read_string.side_effect = ["John Doe", "95", "hello", "8"]

        # Mocking the return value of find_patron_by_name_and_age to be John Doe
        mock_find_patron_by_name_and_age.return_value = self.patron

        #Adding a loan to the patron 
        self.patron._loans.append(Loan(self.item, datetime.now()))

        #Storing the original loan count
        original_loan = len(self.patron._loans)
        
        #Execute the return item process
        self.ui._current_screen = self.ui._return_item
        self.ui.run_current_screen()

        #Verify that the loan count has decreased by 1
        self.assertEqual(len(self.patron._loans), original_loan - 1)

        #Verify that the current screen is the main menu
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

    @mock.patch('src.search.find_patron_by_name_and_age')
    @mock.patch('src.user_input.read_string')
    def test_return_item_success_with_float_first(self,
                                                         mock_read_string,
                                                         mock_find_patron_by_name_and_age):
        """
        Test to successfully return an item with multiple tries of inputting
        the item id.
        The patron tested to return item from loan is 'John Manor' (aged 25).
        At here, the item id is 9.0 which is a float and is an invalid input. 
        Thus when during the next try, the item id is 8 which is a book
        is valid and the item is returned successfully.
        """
        #Mocking the input for the return item process
        mock_read_string.side_effect = ["John Doe", "95", "9.0", "8"]

        # Mocking the return value of find_patron_by_name_and_age to be John Doe
        mock_find_patron_by_name_and_age.return_value = self.patron

        #Adding a loan to the patron 
        self.patron._loans.append(Loan(self.item, datetime.now()))

        #Storing the original loan count
        original_loan = len(self.patron._loans)
        
        #Execute the return item process
        self.ui._current_screen = self.ui._return_item
        self.ui.run_current_screen()

        #Verify that the loan count has decreased by 1
        self.assertEqual(len(self.patron._loans), original_loan - 1)

        #Verify that the current screen is the main menu
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

class TestSearchForPatron(unittest.TestCase):
    def setUp(self):
        self.dataManager = DataManager()
        self.ui = BatUI(self.dataManager)
        self.patron_data = self.dataManager._patron_data
        self.library_catalogue = self.dataManager._catalogue_data
    
    @mock.patch('src.search.find_patron_by_name')
    @mock.patch('src.user_input.read_string')
    def test_search_for_patron_by_name_fail(self,
                                            mock_read_string,
                                            mock_find_patron_by_name):
        """
        Test to fail searching for a patron by name due to invalid patron name.
        At here, the choice chosen is 1 which is for searching for
        patron by name.
        The patron name is 'John Doee' which is not in the patron data.
        """
        mock_read_string.side_effect = ["1","John Doee"]
        
        # Mocking the return value of find_patron_by_name to be an empty list
        mock_find_patron_by_name.return_value = []
        
        self.ui._current_screen = self.ui._search_for_patron
        self.ui.run_current_screen()

        self.assertEqual(self.ui.get_current_screen(), "SEARCH FOR PATRON")

    @mock.patch('src.search.find_patron_by_name')
    @mock.patch('src.user_input.read_string')
    def test_search_for_patron_by_name_success(self,
                                               mock_read_string,
                                               mock_find_patron_by_name):
        """
        Test to successfully search for a patron by name.
        At here, the choice chosen is 1 which is for searching for
        patron by name.
        The patron name is 'John Doe' which is in the patron data.
        """
        mock_read_string.side_effect = ["1","John Doe"]
        
        # Mocking the return value of find_patron_by_name to be John Doe
        mock_find_patron_by_name.return_value = [self.patron_data[0]]
        
        self.ui._current_screen = self.ui._search_for_patron
        self.ui.run_current_screen()

        self.assertEqual(self.ui.get_current_screen(), "SEARCH FOR PATRON")

    @mock.patch('src.search.find_patron_by_age')
    @mock.patch('src.user_input.read_string')
    def test_search_for_patron_by_age_fail(self,
                                           mock_read_string,
                                           mock_find_patron_by_age):
        """
        Test to fail searching for a patron by age due to invalid patron age.
        At here, the choice chosen is 2 which is for searching for
        patron by age.
        The patron age is -10 which is invalid.
        """
        mock_read_string.side_effect = ["2","-10"]
        
        # Mocking the return value of find_patron_by_age to be an empty list
        mock_find_patron_by_age.return_value = []
        
        self.ui._current_screen = self.ui._search_for_patron
        self.ui.run_current_screen()

        self.assertEqual(self.ui.get_current_screen(), "SEARCH FOR PATRON")

    @mock.patch('src.search.find_patron_by_age')
    @mock.patch('src.user_input.read_string')
    def test_search_for_patron_by_age_success(self, 
                                              mock_read_string,
                                              find_patron_by_age):
        """
        Test to successfully search for a patron by age.
        At here, the choice chosen is 2 which is for
        searching for patron by age.
        The patron age is 23 which is in the patron data.
        """
        mock_read_string.side_effect = ["2","23"]
        
        # Mocking the return value of find_patron_by_age to be Jane Smith
        find_patron_by_age.return_value = [self.patron_data[1]]
        
        self.ui._current_screen = self.ui._search_for_patron
        self.ui.run_current_screen()


        self.assertEqual(self.ui.get_current_screen(), "SEARCH FOR PATRON")

    @mock.patch('src.user_input.read_string')
    def test_search_for_patron_to_main_menu(self, mock_read_string):
        """
        Test to return to the main menu from the search for patron screen.
        At here, the choice chosen is 3 which is to return to the main menu.
        """
        mock_read_string.return_value = "3"
        
        self.ui._current_screen = self.ui._search_for_patron
        self.ui.run_current_screen()

        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

    @mock.patch('src.user_input.read_string')
    def test_search_for_patron_with_out_of_range_first(self, mock_read_string):
        """
        Test to return to search for patron screen from search for patron
        screen due to invalid choice.
        At here, the choice chosen is 4 and is out of range and is an invalid input.
        Thus when during the next try, the choice chosen is 3 which is a valid
        input and the screen is navigated to the main menu.
        """
        mock_read_string.side_effect = ["4", "3"]
        
        self.ui._current_screen = self.ui._search_for_patron
        self.ui.run_current_screen()

        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

    @mock.patch('src.user_input.read_string')
    def test_search_for_patron_with_str_first(self, mock_read_string):
        """
        Test to return to search for patron screen from search for patron
        screen due to invalid choice.
        At here, the choice chosen is hello which is a string and is an invalid input.
        Thus when during the next try, the choice chosen is 3 which is a valid
        input and the screen is navigated to the main menu.
        """
        mock_read_string.side_effect = ["hello", "3"]
        
        self.ui._current_screen = self.ui._search_for_patron
        self.ui.run_current_screen()

        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

    @mock.patch('src.user_input.read_string')
    def test_search_for_patron_with_str_first(self, mock_read_string):
        """
        Test to return to search for patron screen from search for patron
        screen due to invalid choice.
        At here, the choice chosen is 9.0 which is a flaot and is an invalid input.
        Thus when during the next try, the choice chosen is 3 which is a valid
        input and the screen is navigated to the main menu.
        """
        mock_read_string.side_effect = ["9.0", "3"]
        
        self.ui._current_screen = self.ui._search_for_patron
        self.ui.run_current_screen()

        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

class TestRegisterPatron(unittest.TestCase):
    def setUp(self):
        self.dataManager = DataManager()
        self.ui = BatUI(self.dataManager)
        self.patron_data = self.dataManager._patron_data
        self.library_catalogue = self.dataManager._catalogue_data

    @mock.patch('src.user_input.read_string')
    def test_register_patron_success(self, mock_read_string):
        """
        Test to successfully register a patron.
        At here, the patron name is 'Dwight Howard' and the age is 35 which is
        valid.
        """
        mock_read_string.side_effect = ['Dwight Howard', '35'] 
        
        #Storing the original patron count
        original_patron_count = len(self.patron_data)
        
        self.ui._current_screen = self.ui._register_patron
        self.ui.run_current_screen()

        #Checking if the patron count has increased by 1 as a new patron has been added
        self.assertEqual(len(self.patron_data), original_patron_count + 1)
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")
    
    @mock.patch('src.user_input.read_string')
    def test_register_patron_success_with_invalid_age_first(self, mock_read_string):
        """
        Test to have an invalid age inputted first and then successfully register a patron.
        At here, the patron name is 'Dwight Howard' and the age is -150 which is invalid.
        Thus when during the next try, the age is 35 which is valid and the patron is
        successfully registered.
        """
        mock_read_string.side_effect = ['Dwight Howard', '-150', '35']
        
        #Storing the original patron count
        original_patron_count = len(self.patron_data)
        
        self.ui._current_screen = self.ui._register_patron
        self.ui.run_current_screen()
        
        #Checking if the patron count has increased by 1 as a new patron has been added
        self.assertEqual(len(self.patron_data), original_patron_count + 1)
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")


class TestAccessMakerspace(unittest.TestCase):
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
        self.patron_allowed_to_use_makerspace = Patron()
        patron_json_record = {"patron_id": 101,
                              "name": "John Manor",
                              "age": 25,
                              "outstanding_fees": 0.00,
                              "gardening_tool_training": False,
                              "carpentry_tool_training": False,
                              "makerspace_training": True,
                              "loans": []
                              }
        self.patron_allowed_to_use_makerspace.load_data(patron_json_record, [])     

        self.patron_exceed_age = Patron()
        patron_json_record_two = {"patron_id": 102,
                                  "name": "Albert Stein",
                                  "age": 95,
                                  "outstanding_fees": 0.00,
                                  "gardening_tool_training": False,
                                  "carpentry_tool_training": False,
                                  "makerspace_training": True,
                                  "loans": []
                                  }
        self.patron_exceed_age.load_data(patron_json_record_two, [])

        self.patron_below_age = Patron()
        patron_json_record_three = {"patron_id": 103,
                                    "name": "Bernard Johnson",
                                    "age": 5,
                                    "outstanding_fees": 0.00,
                                    "gardening_tool_training": False,
                                    "carpentry_tool_training": False,
                                    "makerspace_training": True,
                                    "loans": []
                                    }
        self.patron_below_age.load_data(patron_json_record_three, [])
        
        self.patron_has_fees_owed = Patron()
        patron_json_record_four = {"patron_id": 104,
                                    "name": "Camilla Smith",
                                    "age": 25,
                                    "outstanding_fees": 10.00,
                                    "gardening_tool_training": False,
                                    "carpentry_tool_training": False,
                                    "makerspace_training": True,
                                    "loans": []
                                    }
        self.patron_has_fees_owed.load_data(patron_json_record_four, [])

        self.patron_no_training = Patron()
        patron_json_record_five = {"patron_id": 105,
                                    "name": "Douncy Gordon",
                                    "age": 25,
                                    "outstanding_fees": 0.00,
                                    "gardening_tool_training": False,
                                    "carpentry_tool_training": False,
                                    "makerspace_training": False,
                                    "loans": []
                                    }
        self.patron_no_training.load_data(patron_json_record_five, [])          
    
    @mock.patch('src.search.find_patron_by_name_and_age')
    @mock.patch('src.user_input.read_string')
    def test_access_makerspace_fail_invalid_patron_name(self, 
                                                        mock_read_string,
                                                        mock_find_patron_by_name_and_age):
        """
        Test to fail accessing the makerspace due to invalid patron name.
        At here, the patron name is 'John Major' which not the name the Patron object created.
        """
        #Mocking the input for the access makerspace process
        mock_read_string.side_effect = ["John Major", "25"]
        
        # Mocking the return value of find_patron_by_name_and_age to be None
        mock_find_patron_by_name_and_age.return_value = None
        
        #Execute the access makerspace process
        self.ui._current_screen = self.ui._access_makerspace
        self.ui.run_current_screen()

        #Verify that the current screen is the main menu
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

    @mock.patch('src.search.find_patron_by_name_and_age')
    @mock.patch('src.user_input.read_string')
    def test_access_makerspace_fail_invalid_patron_age(self,
                                                       mock_read_string,
                                                       mock_find_patron_by_name_and_age):
        """
        Test to fail accessing the makerspace due to invalid patron age.
        At here, the patron name is 'John Manor' and the age is 23 which is
        invalid.
        The age for John Manor is 25.
        """
        #Mocking the input for the access makerspace process
        mock_read_string.side_effect = ["John Manor", "23"]
        # Mocking the return value of find_patron_by_name_and_age to be None
        mock_find_patron_by_name_and_age.return_value = None
        
        #Execute the access makerspace process
        self.ui._current_screen = self.ui._access_makerspace
        self.ui.run_current_screen()

        #Verify that the current screen is the main menu
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

    @mock.patch('src.business_logic.can_use_makerspace')
    @mock.patch('src.search.find_patron_by_name_and_age')
    @mock.patch('src.user_input.read_string')
    def test_access_makerspace_fail_exceed_allowed_age(self, 
                                                       mock_read_string,
                                                       find_name_and_age,
                                                       can_use_makerspace):
        """
        Test to fail accessing the makerspace due to the patron age exceeds the
        allowed age.
        At here, the patron name is 'Albert Stein' and the age is 95 which is
        invalid.
        This is because makerspace can only be accessed by patrons
        aged 18 to 90.
        """
        mock_read_string.side_effect = ["Albert Stein", "95"]
        
        # Mocking the return value of find_patron_by_name_and_age to be Albert Stein
        find_name_and_age.return_value = self.patron_exceed_age
        
        # Mocking the return value of can_use_makerspace to be False
        can_use_makerspace.return_value = False

        #Execute the access makerspace process
        self.ui._current_screen = self.ui._access_makerspace
        self.ui.run_current_screen()

        #Verify that the current screen is the main menu
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

    @mock.patch('src.business_logic.can_use_makerspace')
    @mock.patch('src.search.find_patron_by_name_and_age')
    @mock.patch('src.user_input.read_string')
    def test_access_makerspace_fail_below_allowed_age(self,
                                                      mock_read_string,
                                                      find_name_and_age,
                                                      can_use_makerspace):
        """
        Test to fail accessing the makerspace due to the patron age
        is below the allowed age.
        At here, the patron name is 'Bernard Johnson' and the age is 5 which is
        invalid.
        This is because makerspace can only be accessed by patrons
        aged 18 to 90.
        """
        mock_read_string.side_effect = ["Bernard Johnson", "5"]
        
        # Mocking the return value of find_patron_by_name_and_age to be Bernard Johnson
        find_name_and_age.return_value = self.patron_below_age
        
        # Mocking the return value of can_use_makerspace to be False
        can_use_makerspace.return_value = False

        #Execute the access makerspace process
        self.ui._current_screen = self.ui._access_makerspace
        self.ui.run_current_screen()

        #Verify that the current screen is the main menu
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")


    @mock.patch('src.business_logic.can_use_makerspace')
    @mock.patch('src.search.find_patron_by_name_and_age')
    @mock.patch('src.user_input.read_string')
    def test_access_makerspace_fail_has_outstanding_fee(self,
                                                        mock_read_string,
                                                        find_name_and_age,
                                                        can_use_makerspace):
        """
        Test to fail accessing the makerspace due to the patron has
        an outstanding fee.
        At here, the patron name is 'Camilla Smith' and the age is 25.
        The patron has an outstanding fee and thus cannot access
        the makerspace.
        """
        #Mocking the input for the access makerspace process
        mock_read_string.side_effect = ['Camilla Smith', '25']

        # Mocking the return value of find_patron_by_name_and_age to be Camilla Smith
        find_name_and_age.return_value = self.patron_has_fees_owed

        # Mocking the return value of can_use_makerspace to be False
        can_use_makerspace.return_value = False

        #Execute the access makerspace process
        self.ui._current_screen = self.ui._access_makerspace
        self.ui.run_current_screen()

        #Verify that the current screen is the main menu
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")


    @mock.patch('src.business_logic.can_use_makerspace')
    @mock.patch('src.search.find_patron_by_name_and_age')
    @mock.patch('src.user_input.read_string')
    def test_access_makerspace_fail_no_training(self,
                                                mock_read_string,
                                                find_name_and_age,
                                                can_use_makerspace):
        """
        Test to fail accessing the makerspace due to the patron has
        not completed the makerspace training.
        At here, the patron name is 'Douncy Gordon' and the age is 25.
        The patron has no outstanding fee but has not completed the
        makerspace training.
        """
        mock_read_string.side_effect = ['Douncy Gordon', '25']
        
        # Mocking the return value of find_patron_by_name_and_age to be Douncy Gordon
        find_name_and_age.return_value = self.patron_no_training
        
        # Mocking the return value of can_use_makerspace to be False
        can_use_makerspace.return_value = False

        #Execute the access makerspace process
        self.ui._current_screen = self.ui._access_makerspace
        self.ui.run_current_screen()

        #Verify that the current screen is the main menu
        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")

    @mock.patch('src.business_logic.can_use_makerspace')
    @mock.patch('src.search.find_patron_by_name_and_age')
    @mock.patch('src.user_input.read_string')
    def test_access_makerspace_success(self,
                                       mock_read_string,
                                       find_name_and_age,
                                       can_use_makerspace):
        """
        Test to successfully access the makerspace.
        At here, the patron name is 'John Manor' and the age is 25.
        The patron has no outstanding fee and has completed the
        makerspace training. Besides, the patron is aged between 18 to 90.
        Thus, the patron can access the makerspace.
        """
        #Mocking the input for the access makerspace process
        mock_read_string.side_effect = ['John Manor', '25']
        
        # Mocking the return value of find_patron_by_name_and_age to be Jane Smith
        find_name_and_age.return_value = self.patron_allowed_to_use_makerspace

        # Mocking the return value of can_use_makerspace to be True
        can_use_makerspace.return_value = True

        #Execute the access makerspace process
        self.ui._current_screen = self.ui._access_makerspace
        self.ui.run_current_screen()

        self.assertEqual(self.ui.get_current_screen(), "MAIN MENU")


class TestQuit(unittest.TestCase):
    def setUp(self):
        self.dataManager = DataManager()
        self.ui = BatUI(self.dataManager)
        self.patron_data = self.dataManager._patron_data
        self.library_catalogue = self.dataManager._catalogue_data

    def test_quit(self):
        self.ui._current_screen = self.ui._quit
        self.ui.run_current_screen()
        
        self.assertEqual(self.ui.get_current_screen(), "QUIT")
