# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
#
# If, at a pixel, r > Upper Threshold and g < Lower Threshold
# and b < Lower Threshold, mark this pixel as red. If, at a pixel, r < Lower Threshold and
# g > Upper Threshold and b > Upper Threshold, mark this pixel as cyan
import numpy as np
import matplotlib.image as mpimg
from typing import Union


def read_image(img_name: str) -> Union[np.ndarray, None]:
    """
    Reads an image into an ndarray
    :param img_name: name for the image being read
    :return: returns an ndarray containing RGBA values for each pixel if the file was found and read or None if it wasn't
    """
    try:
        # Read the image
        img = mpimg.imread("data/{}.png".format(img_name))
    # The file was not found, caused by the user inputting the wrong file name
    except FileNotFoundError:
        return None
    return img


def find_red_pixels(*args, **kwargs):
    """Your documentation goes here"""
    # If, at a pixel, r > Upper Threshold and g < Lower Threshold
    # and b < Lower Threshold, mark this pixel as red.


def find_cyan_pixels(*args, **kwargs):
    """Your documentation goes here"""
    # If, at a pixel, r < Lower Threshold and
    # g > Upper Threshold and b > Upper Threshold, mark this pixel as cyan


def detect_connected_components(*args, **kwargs):
    """Your documentation goes here"""

    # Set all elements in MARK as unvisited, i.e., 0.
    # Create an empty queue-like ndarray Q
    # for each pixel p(x, y) in IMG do
    #   if p(x, y) is the pavement pixel and MARK(x, y) is unvisited then
    #       set MARK(x, y) as visited;
    #       add p(x, y) into Q;
    #       while Q is not empty do
    #           Remove the first item q(m, n) from Q;
    #           for each 8-neighbour n(s, t) of q(m, n) do
    #               if n(s, t) is the pavement pixel and MARK(x, t) is unvisited then
    #                   set MARK(s, t) as visited;
    #                   add n(s, t) into Q;
    #           end for
    #       end while
    # end for


def detect_connected_components_sorted(*args, **kwargs):
    """Your documentation goes here"""
    # Your code goes here

