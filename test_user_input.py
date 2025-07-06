import unittest
from unittest import mock
from src.user_input import *


class TestUserInput(unittest.TestCase):
    def test_is_int_with_int(self):
        self.assertTrue(is_int('5'))
    
    def test_is_int_with_str(self):
        self.assertFalse(is_int('abc'))
    
    def test_is_float_with_float(self):
        self.assertTrue(is_float('5.0'))
    
    def test_is_float_with_str(self):
        self.assertFalse(is_float('abc'))

    @mock.patch('builtins.input')
    def test_read_string(self, mock_input):
        mock_input.return_value = 'test input'
        self.assertEqual(read_string(""), 'test input')

    @mock.patch('src.user_input.read_string')
    def test_read_integer_with_int(self, readint):
        readint.return_value = "5"
        self.assertEqual(5, read_integer(""))
    
    @mock.patch('src.user_input.read_string')
    def test_read_integer_with_str_first(self, readint):
        readint.side_effect = ['hello', "5"]
        self.assertEqual(5, read_integer(""))
    
    @mock.patch('src.user_input.read_string')
    def test_read_float_with_flaot(self, readfloat):
        readfloat.return_value = "5.0"
        self.assertEqual(5.0, read_float(""))

    @mock.patch('src.user_input.read_string')
    def test_read_float_with_str_first(self, readfloat):
        readfloat.side_effect = ['hello', "5.0"]
        self.assertEqual(5.0, read_float(""))

    @mock.patch('src.user_input.read_string')
    def test_read_integer_range_in_range(self, readintrange):
        readintrange.return_value = "5"
        self.assertEqual(5, read_integer_range("", 1, 10))
    
    @mock.patch('src.user_input.read_string')
    def test_read_integer_range_out_of_range_first(self, readintrange):
        readintrange.side_effect = ["15","5"]
        self.assertEqual(5, read_integer_range("", 1, 10))

    @mock.patch('src.user_input.read_string')
    def test_read_float_range_in_range(self, readfloatrange):
        readfloatrange.return_value = "5.0"
        self.assertEqual(5, read_float_range("", 1, 10))

    @mock.patch('src.user_input.read_string')
    def test_read_float_range_out_of_range_first(self, readfloatrange):
        readfloatrange.side_effect = ["15.0", "5.0"]
        self.assertEqual(5, read_float_range("", 1, 10))

    @mock.patch('src.user_input.read_string')
    def test_read_bool_lowercase_y(self, readbool):
        readbool.return_value = "y"
        self.assertEqual("y", read_bool(""))
    
    @mock.patch('src.user_input.read_string')
    def test_read_bool_uppercase_y(self, readbool):
        readbool.return_value = "Y"
        self.assertEqual("y", read_bool(""))
    
    @mock.patch('src.user_input.read_string')
    def test_read_bool_lowercase_n(self, readbool):
        readbool.return_value = "n"
        self.assertEqual("n", read_bool(""))
    
    @mock.patch('src.user_input.read_string')
    def test_read_bool_uppercase_n(self, readbool):
        readbool.return_value = "N"
        self.assertEqual("n", read_bool(""))
    
    @mock.patch('src.user_input.read_string')
    def test_read_bool_int_first(self, readbool):
        readbool.side_effect = ["5", "y"]
        self.assertEqual("y", read_bool(""))

    @mock.patch('src.user_input.read_string')
    def test_read_bool_float_first(self, readbool):
        readbool.side_effect = ["5.0", "y"]
        self.assertEqual("y", read_bool(""))

    @mock.patch('src.user_input.read_string')
    def test_read_bool_str_first(self, readbool):
        readbool.side_effect = ["abc", "y"]
        self.assertEqual("y", read_bool(""))
