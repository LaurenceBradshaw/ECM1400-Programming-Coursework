# Requires copy of the /data directory to be put in /test/data so the testing functions have access to the data
import pytest
import utils
import numpy as np


class TestCustom:

    class TestCheckNumeric:

        @pytest.mark.parametrize("data", [[1, 2, 3, 'w'], [2, '2', 4]])
        def test_with_non_numeric_value_present(self, data):
            """
            Test that the function raises an error when a non-numeric value is present
            :return: None
            """
            with pytest.raises(ValueError):
                utils.check_numeric(data, "")

        @pytest.mark.parametrize("data", [[1, 2, 3], [0, 0, 2], [-1, -2, 3]])
        def test_without_non_numeric_value_present(self, data):
            """
            Test that the function does not raise an error when no non-numeric values are present
            :return: None
            """
            try:
                utils.check_numeric(data, "")
            except ValueError:
                pytest.fail("Unexpected error raised")

    class TestRemoveNoData:
        pass


class TestTemplate:

    class TestSumValue:
        @pytest.mark.parametrize(["data", "expected"], [
            ([5, 3, 4, 7, 8], 27),
            ([0, 0], 0),
            ([], 0),
            ([-2, -3], -5),
            ([1.25, 2, 3.75], 7)
        ])
        def test_expected(self, data, expected):
            """
            Test the sumvalue function returns the expected output with a range of data
            :param data: Data to sum
            :param expected: expected sum
            :return: None
            """
            assert utils.sumvalues(data) == expected

    class TestMeanValue:
        @pytest.mark.parametrize(["data", "expected"], [
            ([5, 3, 4, 7, 8], 5.4),
            ([0, 0], 0),
            ([], 0),
            ([-2, -3], -2.5),
            ([1, 1.5], 1.25)
        ])
        def test_expected(self, data, expected):
            """
            Test the meanvalue function returns the expected output with a range of data
            :param data: Data to sum
            :param expected: expected sum
            :return: None
            """
            assert utils.meannvalue(data) == expected

    class TestMaxValue:
        @pytest.mark.parametrize(["data", "expected"], [
            ([5, 3, 4, 7, 8], 4),
            ([0, 0], 0),
            ([-2, -3], 0),
            ([1.25, 2, 3.75], 2)
        ])
        def test_expected(self, data, expected):
            """
            Test the maxvalue function is returning the correct index for a range of data
            :param data: The data to find the max value for
            :param expected: The expected return index
            :return: None
            """
            assert utils.maxvalue(data) == expected

        def test_no_values(self):
            """
            Test the maxvalue function raises the ValueError exception when the input data is empty
            :return:
            """
            with pytest.raises(ValueError) as e_info:
                utils.maxvalue([])

    class TestMinValue:
        @pytest.mark.parametrize(["data", "expected"], [
            ([5, 3, 4, 7, 8], 1),
            ([0, 0], 0),
            ([-2, -3], 1),
            ([1.25, 2, 3.75], 0)
        ])
        def test_expected(self, data, expected):
            """
            Test the minvalue function is returning the correct index for a range of data
            :param data: The data to find the min value for
            :param expected: The expected return index
            :return: None
            """
            assert utils.minvalue(data) == expected

        def test_no_values(self):
            """
            Test the maxvalue function raises the ValueError exception when the input data is empty
            :return:
            """
            with pytest.raises(ValueError) as e_info:
                utils.minvalue([])

    class TestCountValue:
        @pytest.mark.parametrize(["data", "xw", "expected"], [
            ([5, 3, 4, 7, 7, 8], 7, 2),
            ([0, 0], 0, 2),
            ([-2, -3, -3, -3], -3, 3),
            ([1.25, 2, 3.75, 3.75], 3.75, 2),
            ([2, 1, 2, 'No data', 'No data'], 'No data', 2),
            ([2, 1, 2, 2], 3, 0)
        ])
        def test_countvalue(self, data, xw, expected):
            """
            Test the countvalue function returns the correct number for the number of occurrences of xw
            :param data: Data to check
            :param xw: Value to count occurrences of
            :param expected: Expected output
            :return: None
            """
            assert utils.countvalue(data, xw) == expected
