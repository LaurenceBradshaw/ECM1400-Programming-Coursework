# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
#
# If, at a pixel, r > Upper Threshold and g < Lower Threshold
# and b < Lower Threshold, mark this pixel as red. If, at a pixel, r < Lower Threshold and
# g > Upper Threshold and b > Upper Threshold, mark this pixel as cyan
import numpy as np
import matplotlib.image as mpimg
from skimage import io
from typing import Callable
import utils


def red_pixel_condition(map_file: np.array, upper_threshold: float, lower_threshold: float, x: int, y: int) -> bool:
    red = map_file[x, y, 0] > upper_threshold
    green = map_file[x, y, 1] < lower_threshold
    blue = map_file[x, y, 2] < lower_threshold
    return red and green and blue


def cyan_pixel_condition(map_file: np.array, upper_threshold: float, lower_threshold: float, x: int, y: int) -> bool:
    red = map_file[x, y, 0] < upper_threshold
    green = map_file[x, y, 1] > lower_threshold
    blue = map_file[x, y, 2] > lower_threshold
    return red and green and blue


def filter_pixels(map_filename: str, upper_threshold: int, lower_threshold: int, condition_valid_pixel: Callable):
    map_file = utils.read_image(map_filename)
    width = map_file.shape[0]
    height = map_file.shape[1]
    empty_map_file = np.zeros((width, height, 3))
    for x in range(width):
        for y in range(height):
            if condition_valid_pixel(map_file, upper_threshold, lower_threshold, x, y):
                empty_map_file[x, y] = np.array([1, 1, 1])
            else:
                empty_map_file[x, y] = np.array([0, 0, 0])

    return empty_map_file


def find_red_pixels(*args, **kwargs):
    """
    Finds all the red pixels in the input image and saves them to a binary png file
    If, at a pixel, r > Upper Threshold and g < Lower Threshold
    and b < Lower Threshold, this pixel is red.

    :param args: First element contains the name of the image file
    :param kwargs: upper_threshold and lower_threshold to hold the values used to consider a pixel red
    :return: An array containing all the binary pixels
    """

    map_filename = args[0]
    upper_threshold = kwargs['upper_threshold']
    lower_threshold = kwargs['lower_threshold']

    new_map = filter_pixels(map_filename, upper_threshold, lower_threshold, red_pixel_condition)

    io.imsave("map-red-pixels.jpg", new_map)

    return new_map


def find_cyan_pixels(*args, **kwargs):
    """
    Finds all the cyan pixels in the input image and saves them to a binary png file
    If, at a pixel, r < Lower Threshold and
    g > Upper Threshold and b > Upper Threshold, this pixel is cyan

    :param args: First element contains the name of the image file
    :param kwargs: upper_threshold and lower_threshold to hold the values used to consider a pixel cyan
    :return: An array containing all the binary pixels
    """

    map_filename = args[0]
    upper_threshold = kwargs['upper_threshold']/255
    lower_threshold = kwargs['lower_threshold']/255

    new_map = filter_pixels(map_filename, upper_threshold, lower_threshold, cyan_pixel_condition)

    mpimg.imsave("map-cyan-pixels.jpg", new_map)

    return new_map


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

