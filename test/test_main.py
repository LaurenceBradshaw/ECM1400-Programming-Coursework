import pytest
import main


class TestReadFile:

    @pytest.fixture
    def valid_file_data(self):
        """
        Fixture for valid data
        :return: list of dicts containing valid data
        """
        return main.read_file("Pollution-London Harlington.csv")

    @pytest.mark.parametrize(["f_name", "output_type"], [
        ("Pollution-London Harlington.csv", list),
        ("This file does not exist.csv", type(None))
    ])
    def test_output_types(self, f_name, output_type):
        """
        Test the function returns the correct types when given valid and invalid file names
        :return: None
        """
        data = main.read_file(f_name)
        assert type(data) is output_type

    def test_expected_dimensions(self, valid_file_data):
        """
        Test the function returns a list with the expected dimensions
        :return: None
        """
        days = 365
        hours = 24
        total_entries = days * hours
        assert len(valid_file_data) == total_entries

    def test_list_of_dicts(self, valid_file_data):
        """
        Test the valid data is a list of dicts
        :return: None
        """
        is_dict = [True if type(element) == dict else False for element in valid_file_data]
        assert all(is_dict)

    @pytest.mark.parametrize("dict_key", ['date', 'time', 'no', 'pm10', 'pm25'])
    def test_expected_dict_keys(self, valid_file_data, dict_key):
        """
        Test the first element in the list is a dictionary with the expected keys
        :return: None
        """
        keys = list(valid_file_data[0].keys())

        assert dict_key in keys