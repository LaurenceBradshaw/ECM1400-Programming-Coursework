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


# -------------------------
# My custom functions
# -------------------------


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
                empty_map_file[x, y] = np.array([255, 255, 255])
            else:
                empty_map_file[x, y] = np.array([0, 0, 0])

    return empty_map_file


def push_queue(queue: np.array, value):
    """
    Appends an element to the numpy ndarry queue

    :param queue: The queue to append to
    :param value: The value to append
    :return: The new queue with the appended value
    """

    current_queue_size = queue.shape[0]
    new_queue = np.zeros((current_queue_size + 1, 2), dtype=int)

    for x in range(current_queue_size):
        new_queue[x] = queue[x]

    new_queue[current_queue_size] = value

    return new_queue


def pop_queue(queue: np.array):
    """
    Pops an element from the front of the numpy ndarry queue

    :param queue: The queue to pop the value from
    :return: A tuple containing the new queue and the popped value
    """

    current_queue_size = queue.shape[0]
    new_queue = np.zeros((current_queue_size - 1, 2), dtype=int)

    for x in range(current_queue_size - 1):
        new_queue[x] = queue[x + 1]

    pop = queue[0]
    return new_queue, pop


def find_neighbours(s, t, img_width, img_height):
    neighbours = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x != 0 or y != 0:
                neighbours.append([x + s, y + t])

    for neighbour in neighbours.copy():
        if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= img_width or neighbour[1] >= img_height:
            neighbours.remove(neighbour)

    return neighbours


# -------------------------
# Template Functions
# -------------------------


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

    io.imsave("map-red-pixels.jpg", np.uint8(new_map))

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
    upper_threshold = kwargs['upper_threshold']
    lower_threshold = kwargs['lower_threshold']

    new_map = filter_pixels(map_filename, upper_threshold, lower_threshold, cyan_pixel_condition)

    io.imsave("map-cyan-pixels.jpg", np.uint8(new_map))

    return new_map


def detect_connected_components(*args, **kwargs):
    """Your documentation goes here"""
    img = args[0]
    img_width = img.shape[0]
    img_height = img.shape[1]
    # Set all elements in MARK as unvisited, i.e., 0.
    mark = np.zeros((img_width, img_height), dtype=int)
    # Create an empty queue-like ndarray Q
    queue = np.zeros((0, 2))
    # for each pixel p(x, y) in IMG do
    for x in range(img_width):
        for y in range(img_height):
            # if p(x, y) is the pavement pixel and MARK(x, y) is unvisited then
            if img[x, y, 0] >= 255 and mark[x, y] == 0:
                # set MARK(x, y) as visited;
                mark[x, y] = 1
                # add p(x, y) into Q;
                queue = push_queue(queue, [x, y])
                # while Q is not empty do
                while queue.shape[0] != 0:
                    # Remove the first item q(m, n) from Q;
                    queue, current_pixel = pop_queue(queue)
                    # for each 8-neighbour n(s, t) of q(m, n) do
                    neighbours = find_neighbours(current_pixel[0], current_pixel[1], img_width, img_height)
                    for neighbour in neighbours:
                        s = neighbour[0]
                        t = neighbour[1]
                        # if n(s, t) is the pavement pixel and MARK(s, t) is unvisited then
                        if img[s, t, 0] >= 255 and mark[s, t] != 1:
                            # set MARK(s, t) as visited;
                            mark[s, t] = 1
                            # add n(s, t) into Q;
                            queue = push_queue(queue, [s, t])

                mark2 = np.zeros((img_width, img_height, 3))
                for x1 in range(img_width):
                    for y1 in range(img_height):
                        if mark[x1, y1] == 1:
                            mark2[x1, y1] = np.array([255, 255, 255])
                        else:
                            mark2[x1, y1] = np.array([0, 0, 0])

                io.imsave("test_mark.jpg", mark2)
    return mark


def detect_connected_components_sorted(*args, **kwargs):
    """Your documentation goes here"""
    # Your code goes here
