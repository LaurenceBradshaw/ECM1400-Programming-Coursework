import pytest
import intelligence
import numpy as np


class TestCustom:

    class TestReadImage:

        @pytest.mark.parametrize(["f_name", "output_type"], [
            ("map.png", np.ndarray),
            ("This image does not exist.png", type(None))
        ])
        def test_output_types(self, f_name, output_type):
            """
            Test the function returns the correct types when given valid and invalid file names
            :return:
            """
            img = intelligence.read_image(f_name)
            assert type(img) is output_type

        def test_expected_shape(self):
            """
            Test that the function returns a numpy array of the expected dimensions
            :return: None
            """
            img = intelligence.read_image("map.png")
            img_shape = img.shape
            assert img_shape == (1140, 1053, 4)

    class TestConditions:

        @pytest.fixture
        def map_array(self):
            """
            Fixture for valid map file data
            :return: Valid 2d list containing mock pixel data
            """
            arr = [[[255, 40, 30], [255, 255, 255], [255, 255, 255]],
                   [[255, 255, 255], [255, 10, 49], [255, 255, 255]],
                   [[255, 255, 255], [10, 255, 255], [255, 42, 32]]]
            return np.array(arr)

        @pytest.fixture
        def upper_threshold(self):
            """
            Fixture for the upper threshold value
            :return: None
            """
            return 100

        @pytest.fixture
        def lower_threshold(self):
            """
            Fixture for the lower threshold value
            :return: None
            """
            return 50

        @pytest.mark.parametrize(["x", "y", "output"], [
            (0, 0, True), (0, 1, False), (0, 2, False),
            (1, 0, False), (1, 1, True), (1, 2, False),
            (2, 0, False), (2, 1, False), (2, 2, True)
        ])
        def test_red_condition(self, map_array, upper_threshold, lower_threshold, x, y, output):
            """
            Tests the red pixel condition against the map_array fixture
            :param map_array: Mock map data
            :param upper_threshold: upper threshold fixture
            :param lower_threshold: lower threshold fixture
            :param x: x value for accessing the map_array
            :param y: y value for accessing the map_array
            :param output: Expected boolean output
            :return: None
            """
            assert intelligence.red_pixel_condition(map_array, upper_threshold, lower_threshold, x, y) == output

        @pytest.mark.parametrize(["x", "y", "output"], [
            (0, 0, False), (0, 1, False), (0, 2, False),
            (1, 0, False), (1, 1, False), (1, 2, False),
            (2, 0, False), (2, 1, True), (2, 2, False)
        ])
        def test_cyan_condition(self, map_array, upper_threshold, lower_threshold, x, y, output):
            """
            Tests the cyan pixel condition against the map_array fixture
            :param map_array: Mock map data
            :param upper_threshold: upper threshold fixture
            :param lower_threshold: lower threshold fixture
            :param x: x value for accessing the map_array
            :param y: y value for accessing the map_array
            :param output: Expected boolean output
            :return: None
            """
            assert intelligence.cyan_pixel_condition(map_array, upper_threshold, lower_threshold, x, y) == output

        @pytest.mark.parametrize(["x", "y", "output"], [
            (0, 0, True), (0, 1, True), (0, 2, True),
            (1, 0, True), (1, 1, False), (1, 2, False),
            (2, 0, False), (2, 1, False), (2, 2, False)
        ])
        def test_top_two_condition(self, upper_threshold, lower_threshold, x, y, output):
            """
            Tests the top two condition
            :return: None
            """
            arr = [[100, 100, 50],
                   [50, 5, 3],
                   [5, 70, 3]]
            arr = np.array(arr)
            assert intelligence.top_two_condition(arr, upper_threshold, lower_threshold, x, y,) == output

    class TestFilterPixels:

        def test_no_valid_pixels(self):
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

        def test_valid_pixels(self):
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

    class TestQueuePop:

        @pytest.mark.parametrize(["queue", "head", "output"], [
            (np.array([[2, 3], [5, 5]]), 0, [2, 3]),
            (np.array([[2, 3], [5, 5]]), 1, [5, 5]),
            (np.array([[2, 3], [0, 2], [4, 6]]), 1, [0, 2]),
            (np.array([[5, 5]]), 0, [5, 5])
        ])
        def test_expected(self, queue, head, output):
            """
            Tests the expected output from the pop_queue function with a range of data
            :param queue: Queue like object to pop from
            :param head: Value for head pointer
            :param output: expected value to be popped
            :return: None
            """
            pop, new_head = intelligence.pop_queue(queue, head)
            assert (pop == output).all()
            assert new_head == head + 1

    class TestQueuePush:

        @pytest.mark.parametrize(["queue", "tail", "data", "output"], [
            (np.array([[2, 3], [5, 5], [0, 0]]), 2, [2, 3], np.array([[2, 3], [5, 5], [2, 3]])),
            (np.array([[5, 5], [0, 0], [0, 0]]), 1, [5, 5], np.array([[5, 5], [5, 5], [0, 0]])),
            (np.array([[0, 0], [0, 0], [0, 0]]), 0, [1, 2], np.array([[1, 2], [0, 0], [0, 0]]))
        ])
        def test_expected(self, queue, tail, data, output):
            """
            Test data is pushed into the expected position
            :param queue: Queue to push to
            :param tail: Value for tail pointer
            :param data: Data to push to queue
            :param output: Expected new queue
            :return: None
            """
            new_tail = intelligence.push_queue(queue, data, tail)
            assert (queue == output).all()
            assert new_tail == tail + 1

    class TestFindNeighbours:

        @pytest.mark.parametrize(["s", "t", "img_w", "img_h", "expected"], [
            (0, 0, 3, 3, [[0, 1], [1, 0], [1, 1]]),  # Top left
            (0, 1, 3, 3, [[0, 0], [0, 2], [1, 0], [1, 1], [1, 2]]),  # Top middle
            (0, 2, 3, 3, [[0, 1], [1, 1], [1, 2]]),  # Top right
            (1, 0, 3, 3, [[0, 0], [0, 1], [1, 1], [2, 0], [2, 1]]),  # Middle left
            (1, 1, 3, 3, [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]]),  # Center
            (1, 2, 3, 3, [[0, 1], [0, 2], [1, 1], [2, 1], [2, 2]]),  # Middle right
            (2, 0, 3, 3, [[1, 0], [1, 1], [2, 1]]),  # Bottom left
            (2, 1, 3, 3, [[1, 0], [1, 1], [1, 2], [2, 0], [2, 2]]),  # Bottom middle
            (2, 2, 3, 3, [[1, 1], [1, 2], [2, 1]]),  # Bottom right
            (4, 4, 3, 3, []),  # Outside positive
            (4, -4, 3, 3, [])  # Outside negative
        ])
        def test_expected(self, s, t, img_w, img_h, expected):
            neighbours = intelligence.find_neighbours(s, t, img_w, img_h)
            assert neighbours == expected

    class TestCountValue2D:  # Test countvalue_2d for 0 instances, and > 1 instances
        pass


class TestTemplate:
    pass
