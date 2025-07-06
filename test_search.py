import unittest
from src.data_mgmt import *
from src.search import *


class TestFindPatronByName(unittest.TestCase):
    def setUp(self):
        """
        Set up the data manager and the data for the tests.
        This helps to ensure that the data is easily accessible for the tests.
        """
        self.dataManager = DataManager()
        self.patron_data = self.dataManager._patron_data
        self.library_catalogue = self.dataManager._catalogue_data

    def test_find_patron_by_name_no_matching_patron(self):
        """
        Test to find a patron by name.
        This test is designed to find a non-matching patron by name.
        At here, patron with the name John Doee is not available in the patron data. 
        Thus, we will fail to search for patron with that name.
        """
        result = find_patron_by_name("John Doee", self.patron_data)
        self.assertEqual(len(result), 0)

    def test_find_patron_by_name_matching_patron(self):
        """
        Test to find a patron by name.
        This test is designed to find a matching patron by name.
        At here, patron with the name John Doe is available in the patron data. 
        Thus, we can successfully find the patron.
        """
        result = find_patron_by_name("John Doe", self.patron_data)
        self.assertEqual(len(result), 1)


class TestFindPatronByAge(unittest.TestCase):
    def setUp(self):
        """
        Set up the data manager and the data for the tests.
        This helps to ensure that the data is easily accessible for the tests.
        """
        self.dataManager = DataManager()
        self.patron_data = self.dataManager._patron_data
        self.library_catalogue = self.dataManager._catalogue_data

    def test_find_patron_by_age_no_matching_patron(self):
        """
        Test to find a patron by age.
        This test is designed to find a non-matching patron by age.
        At here, patron with the age 99 is not available in the patron data. 
        Thus, we will fail to search for patron with that age.
        """
        result = find_patron_by_age(99, self.patron_data)
        self.assertEqual(len(result), 0)

    def test_find_patron_by_age_matching_patron(self):
        """
        Test to find a patron by age.
        This test is designed to find a matching patron by age.
        At here, patron with the age 95 is available in the patron data and the 
        patron is the patron with patron id 1 (John Doe). 
        Thus, we can successfully search for the patron with that age.
        """
        result = find_patron_by_age(95, self.patron_data)
        self.assertEqual(len(result), 1)


class TestFindPatronByNameAndAge(unittest.TestCase):
    def setUp(self):
        """
        Set up the data manager and the data for the tests.
        This helps to ensure that the data is easily accessible for the tests.
        """
        self.dataManager = DataManager()
        self.patron_data = self.dataManager._patron_data
        self.library_catalogue = self.dataManager._catalogue_data

    def test_find_patron_by_name_and_age_failure_invalid_age(self):
        """
        Test to find a patron by name and age unsuccessfully.
        This means that the patron is not found by a valid name and invalid
        age pair.
        At here, we test for a patron with name John Doe and aged 99. 
        This will fail the test as we have a patron named John Doe but his age is 95. 
        """
        result = find_patron_by_name_and_age("John Doe", 99, self.patron_data)
        self.assertEqual(result, None)

    def test_find_patron_by_name_and_age_failure_invalid_name(self):
        """
        Test to find a patron by name and age unsuccessfully.
        This means that the patron is not found by an invalid name and valid
        age pair.
        At here, we test for a patron with name John Doee and aged 95. 
        This will fail the test as we have a patron aged 95 but his name is John Doe.
        """
        result = find_patron_by_name_and_age("John Doee", 95, self.patron_data)
        self.assertEqual(result, None)
    
    def test_find_patron_by_name_and_age_success(self):
        """
        Test to find a patron by name and age successfully.
        This means that the patron is found by a valid name and age pair.
        At here, we test for a patron with name John Dow and aged 95. 
        This will pass the test as we have a patron name “John Doe” with the age of 95.
        """
        result = find_patron_by_name_and_age("John Doe", 95, self.patron_data)
        self.assertEqual(self.patron_data[0], result)
