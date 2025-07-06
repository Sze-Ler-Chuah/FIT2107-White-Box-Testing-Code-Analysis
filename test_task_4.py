import unittest
from unittest import mock
from src.bat_ui import BatUI
from src.data_mgmt import DataManager


class TestMainMenu(unittest.TestCase):
    def setUp(self):
        self.ui = BatUI(DataManager())

    @mock.patch('src.user_input.read_string')
    def test_main_menu_to_loan_item(self, selection):
        """
        Test to check if the main menu can navigate to the loan item screen.
        Mock value to 1 as loan item is the first option in the main menu.
        """
        selection.return_value = "1"
        self.ui.run_current_screen()
        self.assertEqual(self.ui.get_current_screen(), "LOAN ITEM")

    @mock.patch('src.user_input.read_string')
    def test_main_menu_to_return_item(self, selection):
        """
        Test to check if the main menu can navigate to the return item screen.
        Mock value to 2 as return item is the second option in the main menu.
        """
        selection.return_value = "2"
        self.ui.run_current_screen()
        self.assertEqual(self.ui.get_current_screen(), "RETURN ITEM")

    @mock.patch('src.user_input.read_string')
    def test_main_menu_to_search_for_patron(self, selection):
        """
        Test to check if the main menu can navigate to the search for patron
        screen.
        Mock value to 3 as search for patron is the third option in the main
        menu.
        """
        selection.return_value = "3"
        self.ui.run_current_screen()
        self.assertEqual(self.ui.get_current_screen(), "SEARCH FOR PATRON")

    @mock.patch('src.user_input.read_string')
    def test_main_menu_to_register_patron(self, selection):
        """
        Test to check if the main menu can navigate to the register patron
        screen.
        Mock value to 4 as register patron is the fourth option in the main
        menu.
        """
        selection.return_value = "4"
        self.ui.run_current_screen()
        self.assertEqual(self.ui.get_current_screen(), "REGISTER PATRON")

    @mock.patch('src.user_input.read_string')
    def test_main_menu_to_access_makerspace(self, selection):
        """
        Test to check if the main menu can navigate to the access makerspace
        screen.
        Mock value to 5 as access makerspace is the fifth option in the
        main menu.
        """
        selection.return_value = "5"
        self.ui.run_current_screen()
        self.assertEqual(self.ui.get_current_screen(), "ACCESS MAKERSPACE")

    @mock.patch('src.user_input.read_string')
    def test_main_menu_to_quit(self, selection):
        """
        Test to check if the main menu can navigate to the quit screen.
        Mock value to 6 as quit is the sixth option in the main menu.
        """
        selection.return_value = "6"
        self.ui.run_current_screen()
        self.assertEqual(self.ui.get_current_screen(), "QUIT")

    @mock.patch('src.user_input.read_string')
    def test_main_menu_invalid_input_first(self, selection):
        """
        Test for asking user repeatedly for input until a valid input is given.
        Mock value to 0,7,1 as the input range is 1 to 6 and 0,7 are
        invalid inputs.
        """
        selection.side_effect = ["abc", "1"]
        self.ui.run_current_screen()
        self.assertEqual(self.ui.get_current_screen(), "LOAN ITEM")

    @mock.patch('src.user_input.read_string')
    def test_main_menu_out_of_range_first(self, selection):
        """
        Test for asking user repeatedly for input until a valid input is given.
        Mock value is 7 as the valid values are 1 to 6 and 7 is an invalid
        invalid inputs.
        """
        selection.side_effect = ["7", "1"]
        self.ui.run_current_screen()
        self.assertEqual(self.ui.get_current_screen(), "LOAN ITEM")

    @mock.patch('src.user_input.read_string')
    def test_main_menu_str_first(self, selection):
        """
        Test for asking user repeatedly for input until a valid input is given.
        Mock value is 7 as the valid values are 1 to 6 and 7 is an invalid
        invalid inputs.
        """
        selection.side_effect = ["abc", "1"]
        self.ui.run_current_screen()
        self.assertEqual(self.ui.get_current_screen(), "LOAN ITEM")

    @mock.patch('src.user_input.read_string')
    def test_main_menu_float_first(self, selection):
        """
        Test for asking user repeatedly for input until a valid input is given.
        Mock value is 7 as the valid values are 1 to 6 and 7 is an invalid
        invalid inputs.
        """
        selection.side_effect = ["2.0", "1"]
        self.ui.run_current_screen()
        self.assertEqual(self.ui.get_current_screen(), "LOAN ITEM")
