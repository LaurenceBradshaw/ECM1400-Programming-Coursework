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
import utils


def find_red_pixels(*args, **kwargs):
    """
    Finds all the red pixels in the input image and saves them to a binary png file
    If, at a pixel, r > Upper Threshold and g < Lower Threshold
    and b < Lower Threshold, this pixel is marked as red.
    :param args:
    :param kwargs:
    :return:
    """
    map_filename = args[0]
    upper_threshold = kwargs['upper_threshold']/255
    lower_threshold = kwargs['lower_threshold']/255
    map_file = utils.read_image("map")
    empty_map_file = np.zeros(map_file.shape)
    width = map_file.shape[0]
    height = map_file.shape[1]
    for x in range(width):
        for y in range(height):
            if map_file[x, y, 0] > upper_threshold and map_file[x, y, 1] < lower_threshold and map_file[x, y, 2] < lower_threshold:
                empty_map_file[x, y] = np.array([1, 1, 1, 1])
            else:
                empty_map_file[x, y] = np.array([0, 0, 0, 1])

    mpimg.imsave("test2.png", empty_map_file)


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

