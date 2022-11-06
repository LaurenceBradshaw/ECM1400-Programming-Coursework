import intelligence
import monitoring
import reporting
import utils
import pytest


def test_valid_image_file_name():
    """
    Test that the function has found a file and does not return None
    :return: None
    """
    output = intelligence.read_image("map")
    assert output is not None


def test_invalid_image_file_name():
    """
    Test that the function returns None when given the name of a file that does not exist
    :return: None
    """
    assert intelligence.read_image("ma") is None
