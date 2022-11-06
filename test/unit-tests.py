import intelligence
import monitoring
import reporting
import utils
import pytest


# -------------------------
# reporting.py tests
# -------------------------


# -------------------------
# monitoring.py tests
# -------------------------


# -------------------------
# intelligence.py tests
# -------------------------


# -------------------------
# utils.py tests
# -------------------------


def test_read_image_with_valid_file_name():
    """
    Test that the function has found an image file and does not return None
    :return: None
    """
    assert utils.read_image("map") is not None


def test_read_image_with_invalid_file_name():
    """
    Test that the function returns None when given the name of an image file that does not exist
    :return: None
    """
    assert utils.read_image("This image does not exist") is None


def test_read_file_with_valid_file_name():
    """
    Test that the function has found a file and does not return None
    :return: None
    """
    assert utils.read_file("Pollution-London Harlington") is not None


def test_read_file_with_invalid_file_name():
    """
    Test that the function returns None when given the name of a file that does not exist
    :return: None
    """
    assert utils.read_file("This file does not exist") is None


def test_check_numeric_with_non_numeric_value_present():
    values = [1, 2, 3, '5', 'w']
    with pytest.raises(ValueError):
        utils.check_numeric(values, "")


def test_check_numeric_without_non_numeric_value_present():
    values = [1, 2, 3, '5']
    try:
        utils.check_numeric(values, "")
    except ValueError:
        pytest.fail("Unexpected error raised")


def test_sumvalues_correctly_sums_values():
    values = [5, 3, 4, 7, 8]
    sum = 27

    assert utils.sumvalues(values) == sum


def test_maxvalue_returns_correct_index_of_max_value():
    values = [5, 3, 9, 7, 8]
    index = 2

    assert utils.maxvalue(values) == index


def test_minvalue_returns_correct_index_of_min_value():
    values = [5, 3, 9, 7, 8]
    index = 1

    assert utils.minvalue(values) == index


def test_meanvalue_returns_correct_mean():
    values = [5, 3, 9, 7, 8]
    mean = 6.4

    assert utils.meannvalue(values) == mean


def test_meanvalue_handles_input_of_length_zero():
    values = []
    mean = 0

    assert utils.meannvalue(values) == mean


def test_countvalue_returns_zero_when_x_is_not_present():
    values = [1, 1, 2, 2, 3, 6, 4, 3, 3, 3, 2]
    x = 5
    count = 0

    assert utils.countvalue(values, x) == count


def test_countvalue_returns_correctly_when_x_is_present():
    values = [1, 1, 2, 2, 3, 6, 4, 3, 3, 3, 2]
    x = 2
    count = 3

    assert utils.countvalue(values, x) == count
