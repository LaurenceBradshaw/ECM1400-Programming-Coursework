import intelligence
import monitoring
import reporting
import utils
import pytest
import numpy as np


# -------------------------
# reporting.py tests
# -------------------------

# Test get_time_range with date inside and outside of data range
# Test remove_no_value with list with 0 'No data's and 1 'No data'
# Test add_month with normal date, then one which will need year changing

# -------------------------
# monitoring.py tests
# -------------------------

# Test correct_spaces, column is largest, current is largest, current is not largest

# -------------------------
# intelligence.py tests
# -------------------------

# Test inside, outside and in all four corners for find_neighbours
# Test countvalue_2d for 0 instances, and > 1 instances
# Test push queue
def test_queue_pop_more_than_one_element():
    """
    Tests that pop_queue returns the correct popped value and correct new queue when more than one element is present
    :return: None
    """
    arr = np.array([[2, 3], [5, 5]])
    queue, pop = intelligence.pop_queue(arr)
    assert (queue == np.array([[5, 5]])).all()
    assert (pop == np.array([2, 3])).all()


def test_queue_pop_empty():
    """
    Tests that pop_queue returns None for the popped value and an empty queue when given a queue with 0 elements
    :return: None
    """
    arr = np.zeros((0, 2), dtype=int)
    queue, pop = intelligence.pop_queue(arr)
    assert queue.shape == (0, 2)
    assert pop is None


def test_queue_pop_one_element():
    """
    Tests that pop_queue returns the popped value and an empty queue when only one element is present in the queue
    :return: None
    """
    arr = np.array([[2, 3]])
    queue, pop = intelligence.pop_queue(arr)
    assert queue.shape == (0, 2)
    assert (pop == np.array([2, 3])).all()


def test_filter_pixels_with_no_valid_pixels():
    """
    Tests filter_pixels returns the correct array when there are no pixels that fit the condition
    :return: None
    """
    arr = [[[255, 255, 255], [255, 255, 255], [255, 255, 255]],
           [[255, 255, 255], [255, 255, 49], [255, 255, 255]],
           [[255, 255, 255], [10, 255, 255], [255, 255, 32]]]
    arr = np.array(arr)
    expected = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
    expected = np.array(expected)
    assert (intelligence.filter_pixels(arr, 100, 50, intelligence.red_pixel_condition) == expected).all()


def test_filter_pixels_with_valid_pixels():
    """
    Tests that the filter_pixels function returns the correct array given a condition
    :return: None
    """
    arr = [[[255, 40, 30], [255, 255, 255], [255, 255, 255]],
           [[255, 255, 255], [255, 10, 49], [255, 255, 255]],
           [[255, 255, 255], [10, 255, 255], [255, 42, 32]]]
    arr = np.array(arr)
    expected = [[[255, 255, 255], [0, 0, 0], [0, 0, 0]],
                [[0, 0, 0], [255, 255, 255], [0, 0, 0]],
                [[0, 0, 0], [0, 0, 0], [255, 255, 255]]]
    expected = np.array(expected)

    assert (intelligence.filter_pixels(arr, 100, 50, intelligence.red_pixel_condition) == expected).all()


def test_red_pixel_condition():
    """
    Tests that the red_pixel_condition only returns true when given a coordinate with valid values
    :return: None
    """
    arr = [[[255, 40, 30], [255, 255, 255], [255, 255, 255]],
           [[255, 255, 255], [255, 10, 49], [255, 255, 255]],
           [[255, 255, 255], [10, 255, 255], [255, 42, 32]]]
    arr = np.array(arr)
    assert intelligence.red_pixel_condition(arr, 100, 50, 0, 0) == True
    assert intelligence.red_pixel_condition(arr, 100, 50, 0, 1) == False


def test_cyan_pixel_condition():
    """
    Tests that the cyan_pixel_condition only returns true when given a coordinate with valid values
    :return: None
    """
    arr = [[[255, 40, 30], [255, 255, 255], [255, 255, 255]],
           [[255, 255, 255], [255, 10, 49], [255, 255, 255]],
           [[255, 255, 255], [10, 255, 120], [255, 42, 32]]]
    arr = np.array(arr)
    assert intelligence.cyan_pixel_condition(arr, 100, 50, 2, 1) == True
    assert intelligence.cyan_pixel_condition(arr, 100, 50, 0, 1) == False


def test_top_two_condition():
    """
    Tests that the top_two_condition function only returns true when given a coordinate with a valid value
    :return: None
    """
    arr = [[2, 2, 3],
           [2, 4, 3],
           [5, 5, 3]]
    arr = np.array(arr)
    assert intelligence.top_two_condition(arr, 2, 3, 0, 0) == True
    assert intelligence.top_two_condition(arr, 2, 3, 0, 2) == True
    assert intelligence.top_two_condition(arr, 4, 3, 0, 0) == False


# -------------------------
# utils.py tests
# -------------------------


def test_read_image_with_valid_file_name():
    """
    Test that the function has found an image file and does not return None
    :return: None
    """
    assert utils.read_image("map.png") is not None


def test_read_image_with_invalid_file_name():
    """
    Test that the function returns None when given the name of an image file that does not exist
    :return: None
    """
    assert utils.read_image("This image does not exist.png") is None


def test_read_file_with_valid_file_name():
    """
    Test that the function has found a file and does not return None and that the return type is a pandas dataframe
    :return: None
    """
    output = utils.read_file("Pollution-London Harlington.csv")
    assert output is not None
    assert type(output) == list


def test_read_file_with_invalid_file_name():
    """
    Test that the function returns None when given the name of a file that does not exist
    :return: None
    """
    assert utils.read_file("This file does not exist.csv") is None


def test_check_numeric_with_non_numeric_value_present():
    """
    Test that the function raises an error when a non-numeric value is present
    :return: None
    """
    values = [1, 2, 3, '5', 'w']
    with pytest.raises(ValueError):
        utils.check_numeric(values, "")


def test_check_numeric_without_non_numeric_value_present():
    """
    Test that the function does not raise an error when no non-numeric values are present
    :return: None
    """
    values = [1, 2, 3]
    try:
        utils.check_numeric(values, "")
    except ValueError:
        pytest.fail("Unexpected error raised")


def test_sumvalues_correctly_sums_values():
    """
    Test that the function is summing values correctly
    :return: None
    """
    values = [5, 3, 4, 7, 8]
    sum = 27

    assert utils.sumvalues(values) == sum


def test_maxvalue_returns_correct_index_of_max_value():
    """
    Test that the function returns the correct index for the largest value in the list
    :return: None
    """
    values = [5, 3, 9, 7, 8]
    index = 2

    assert utils.maxvalue(values) == index


def test_minvalue_returns_correct_index_of_min_value():
    """
    Test that the function returns the correct index for the smallest value in the list
    :return: None
    """
    values = [5, 3, 9, 7, 8]
    index = 1

    assert utils.minvalue(values) == index


def test_meanvalue_returns_correct_mean():
    """
    Test the function calculates the mean of the list correctly
    :return:
    """
    values = [5, 3, 9, 7, 8]
    mean = 6.4

    assert utils.meannvalue(values) == mean


def test_meanvalue_handles_input_of_length_zero():
    """
    Test the function can calculate a mean with an empty list with no error
    :return: None
    """
    values = []
    mean = 0

    assert utils.meannvalue(values) == mean


def test_countvalue_returns_zero_when_x_is_not_present():
    """
    Test the function can count the number of instances of a value when there are non present in the list
    :return: None
    """
    values = [1, 1, 2, 2, 3, 6, 4, 3, 3, 3, 2]
    x = 5
    count = 0

    assert utils.countvalue(values, x) == count


def test_countvalue_returns_correctly_when_x_is_present():
    """
    Test the function returns the correct number of instances of a value in the list
    :return: None
    """
    values = [1, 1, 2, 2, 3, 6, 4, 3, 3, 3, 2]
    x = 2
    count = 3

    assert utils.countvalue(values, x) == count
