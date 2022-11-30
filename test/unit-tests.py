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
    arr = [[[255, 50, 255], [255, 255, 255], [255, 255, 255]],
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

