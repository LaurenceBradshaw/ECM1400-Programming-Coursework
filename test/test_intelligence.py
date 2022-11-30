import pytest
import intelligence
import numpy as np


class TestCustom:

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
        pass

    class TestQueuePop:
        pass

    class TestQueuePush:
        pass

    class TestFindNeighbours:
        pass

    class TestCountValue2D:
        pass


class TestTemplate:
    pass
