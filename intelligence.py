# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification
from typing import Callable, Union
import utils
import numpy as np
from matplotlib import pyplot as mat_plot
import os


# -------------------------
# My custom functions
# -------------------------


def read_image(file_name: str) -> Union[np.ndarray, None]:
    """
    ---------------
    Description
    ---------------
    Reads the input file name as an image
    If file name is not found, return None

    ---------------
    General Overview
    ---------------
    Try to read the file
    If error return None

    :param file_name: Name of the image file to load
    :return: 2d numpy array containing image data
    """
    try:
        cwd = os.getcwd()
        img = mat_plot.imread(f"{cwd}/data/{file_name}")
        return img
    except FileNotFoundError:
        return None


def red_pixel_condition(map_file: np.array, upper_threshold: int, lower_threshold: int, x: int, y: int) -> bool:
    """
    ---------------
    Description
    ---------------
    Will evaluate a given pixel for being red

    :param map_file: Array containing map data
    :param upper_threshold: Value of the upper threshold
    :param lower_threshold: Value of the lower threshold
    :param x: x coordinate for the pixel currently being evaluated
    :param y: y coordinate for the pixel currently being evaluated
    :return: Boolean value for whether the condition is valid or not
    """

    red = map_file[x, y, 0] > upper_threshold
    green = map_file[x, y, 1] < lower_threshold
    blue = map_file[x, y, 2] < lower_threshold
    return red and green and blue


def cyan_pixel_condition(map_file: np.array, upper_threshold: int, lower_threshold: int, x: int, y: int) -> bool:
    """
    ---------------
    Description
    ---------------
    Will evaluate a given pixel for being cyan

    :param map_file: Array containing map data
    :param upper_threshold: Value of the upper threshold
    :param lower_threshold: Value of the lower threshold
    :param x: x coordinate for the pixel currently being evaluated
    :param y: y coordinate for the pixel currently being evaluated
    :return: Boolean value for whether the condition is valid or not
    """
    red = map_file[x, y, 0] < upper_threshold
    green = map_file[x, y, 1] > lower_threshold
    blue = map_file[x, y, 2] > lower_threshold
    return red and green and blue


def top_two_condition(map_file: np.array, upper_threshold: int, lower_threshold: int, x: int, y: int) -> bool:
    """
    ---------------
    Description
    ---------------
    Will evaluate a given pixel for it to be either the upper or lower threshold
    This is a rather hacky use of existing code :)

    :param map_file: Array containing map data
    :param upper_threshold: Value of first valid pixel
    :param lower_threshold: Value of second valid pixel
    :param x: x coordinate for the pixel currently being evaluated
    :param y: y coordinate for the pixel currently being evaluated
    :return: Boolean value for whether the condition is valid or not
    """
    if map_file[x, y] == upper_threshold or map_file[x, y] == lower_threshold:
        return True
    return False


def filter_pixels(map_file: np.array, upper_threshold: int, lower_threshold: int, condition_valid_pixel: Callable) -> np.array:
    """
    ---------------
    Description
    ---------------
    Will filter pixels into a binary image based on a condition

    ---------------
    General Overview
    ---------------
    Create empty np array to store binary pixels
    For each pixel
    If it satisfies the condition, add it to the binary image

    :param map_file: Numpy array containing the map
    :param upper_threshold: Upper threshold to consider that a pixel has a big enough value for either R, G or B
    :param lower_threshold: Lower threshold to consider that a pixel has a small enough value for either R, G or B
    :param condition_valid_pixel: Function that will use the thresholds to identify a colour
    :return: ndarry containing a binary representation of the image with only the valid colours present
    """

    # Get the dimensions of the image
    width = map_file.shape[0]
    height = map_file.shape[1]
    empty_map_file = np.zeros((width, height, 3))
    # For each pixel in the image
    for x in range(width):
        for y in range(height):
            # Check if the RGB values of the pixel satisfy the condition to be filtered
            if condition_valid_pixel(map_file, upper_threshold, lower_threshold, x, y):
                empty_map_file[x, y] = np.array([255, 255, 255])  # White pixel
            else:
                empty_map_file[x, y] = np.array([0, 0, 0])  # Black pixel

    return empty_map_file


def push_queue(queue: np.array, value, tail: int) -> np.array:
    """
    ---------------
    Description
    ---------------
    Appends an element to the numpy ndarry queue

    :param tail: Tail of the queue like object
    :param queue: The queue to append to
    :param value: The value to append
    :return: The new queue with the appended value
    """

    queue[tail] = value
    tail += 1

    return tail


def pop_queue(queue: np.array, head: int) -> tuple:
    """
    ---------------
    Description
    ---------------
    Pops an element from the front of the numpy ndarry queue

    :param head: Value for head pointer of queue
    :param queue: The queue to pop the value from
    :return: A tuple containing the new queue and the popped value
    """

    pop = queue[head]
    head += 1

    return pop, head


def find_neighbours(s: int, t: int, img_width: int, img_height: int) -> list:
    """
    ---------------
    Description
    ---------------
    Finds all the 8 adjacent pixels to s and t
    Also makes sure that the pixel is within the bounds of the image

    ---------------
    General Overview
    ---------------
    Get all adjacent pixels
    Evaluate whether they are within the bound of the picture

    :param s: Row number for the pixel
    :param t: Column number for the pixel
    :param img_width: Width of the image
    :param img_height: Height of the image
    :return: List containing the row and column for all the valid adjacent pixels
    """
    neighbours = []
    # Find the 8 neighbouring pixels
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x != 0 or y != 0:
                neighbours.append([x + s, y + t])

    # Check if the pixel calculated will be inside the bounds of the image
    for neighbour in neighbours.copy():
        if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= img_width or neighbour[1] >= img_height:
            neighbours.remove(neighbour)

    return neighbours


def countvalue_2d(array: np.array, xw):
    """
    ---------------
    Description
    ---------------
    Finds the number of instances of xw in the input 2d array

    :param array: 2d numpy array to find instances in
    :param xw: What to find instances of
    :return: Number of xw instances
    """

    # Holds the number of occurrences of xw found in values
    xw_count = 0
    # For each element in values, if it is equal to xw, add 1 to xw_count
    for row in array:
        xw_count += utils.countvalue(row, xw)

    return xw_count


# -------------------------
# Template Functions
# -------------------------

def find_red_pixels(*args, **kwargs):
    """
    ---------------
    Description
    ---------------
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

    # Load the image
    map_file = read_image(map_filename) * 255
    # Get all red pixels from the image
    new_map = filter_pixels(map_file, upper_threshold, lower_threshold, red_pixel_condition)

    # Save the binary image array as a jpg file
    mat_plot.imsave("outputs/map-red-pixels.jpg", np.uint8(new_map))

    return new_map


def find_cyan_pixels(*args, **kwargs):
    """
    ---------------
    Description
    ---------------
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

    # Load the image
    map_file = read_image(map_filename) * 255
    # Get all cyan pixels from the image
    new_map = filter_pixels(map_file, upper_threshold, lower_threshold, cyan_pixel_condition)

    # Save the binary image array as a jpg file
    mat_plot.imsave("outputs/map-cyan-pixels.jpg", np.uint8(new_map))

    return new_map


def detect_connected_components(*args, **kwargs):
    """
    ---------------
    Description
    ---------------
    Detects all of the connected components in the input image
    Gives each connected component a number and counts the number of pixels in the component
    Writes the output to a txt file called cc-output-2a.txt

    :param args: Input ndarray image
    :param kwargs: None
    :return: 2D array MARK
    """

    img = args[0]
    # Gets the width and height of the input image
    img_width = img.shape[0]
    img_height = img.shape[1]

    # List to store lines to write to cc-output-2a.txt (modification to original algorithm)
    output_strings = []
    # Two variables to hold the number of the component that is currently being processed and the number of pixels in the component (modification to original algorithm)
    component_number = 0
    current_component_pixel_count = 0

    # Set all elements in MARK as unvisited, i.e., 0.
    # When a pixel is visited it will be marked in MARK with its component number (modification to original algorithm)
    mark = np.zeros((img_width, img_height), dtype=int)
    # Create an empty queue-like ndarray Q
    max_queue_length = img_height * img_width
    queue = np.zeros((max_queue_length, 2), dtype=int)
    queue_head = 0
    queue_tail = 0
    # for each pixel p(x, y) in IMG do
    for x in range(img_width):
        for y in range(img_height):
            # if p(x, y) is the pavement pixel and MARK(x, y) is unvisited then
            if img[x, y, 0] >= 255 and mark[x, y] == 0:
                # Increment the component number as a new component has been found (modification to original algorithm)
                component_number += 1
                # Set the current number of pixels in this component to 1 because the first pixel has been found (modification to original algorithm)
                current_component_pixel_count = 1
                # set MARK(x, y) as visited;
                mark[x, y] = component_number
                # add p(x, y) into Q;
                queue_tail = push_queue(queue, [x, y], queue_tail)
                # while Q is not empty do
                while queue_tail != queue_head:
                    # Remove the first item q(m, n) from Q;
                    current_pixel, queue_head = pop_queue(queue, queue_head)
                    # for each 8-neighbour n(s, t) of q(m, n) do
                    neighbours = find_neighbours(current_pixel[0], current_pixel[1], img_width, img_height)
                    for neighbour in neighbours:
                        s = neighbour[0]
                        t = neighbour[1]
                        # if n(s, t) is the pavement pixel and MARK(s, t) is unvisited then
                        if img[s, t, 0] >= 255 and mark[s, t] == 0:
                            # Increment the pixel count for the current component (modification to original algorithm)
                            current_component_pixel_count += 1
                            # set MARK(s, t) as visited;
                            mark[s, t] = component_number
                            # add n(s, t) into Q;
                            queue_tail = push_queue(queue, [s, t], queue_tail)

                # All pixels in the current component have been found
                # Add a string containing this information to the output_strings list
                output_strings.append(f"Connected Component {component_number}, number of pixels = {current_component_pixel_count}")

    # Count the total number of connected components
    component_count = len(output_strings)

    # Opens and overwrites the cc-output-2a.txt file if it exists, else it makes a new one
    with open("outputs/cc-output-2a.txt", 'w') as f:
        # Writes all lines to the file
        for line in output_strings:
            f.write(line)
            f.write("\n")
        # Writes the total number of connected components to the end of the file
        f.write(f"Total number of connected components = {component_count}")

    return mark


def detect_connected_components_sorted(*args, **kwargs):
    """
    ---------------
    Description
    ---------------
    Uses MARK from detect_connected_components function and orders the connected components largest to smallest
    Writes the output to "cc-output-2b.txt"
    Write the top two components to "cc-top-2.jpg"

    :param args: MARK from detect_connected_components function
    :param kwargs: None
    :return: None
    """

    mark = args[0]
    # Will contain tuples of (component number, pixel count)
    components = []
    components_as_dict = {}
    component_number = 1
    # Count the number of pixels in each component
    for x in range(mark.shape[0]):
        for y in range(mark.shape[1]):
            if mark[x, y] > 0:
                if mark[x, y] not in components_as_dict:
                    components_as_dict[mark[x, y]] = 1
                else:
                    components_as_dict[mark[x, y]] += 1

    # Convert to tuples as defined above
    for key in components_as_dict:
        components.append((key, components_as_dict[key]))

    def sort_components(comp):
        """
        Modified version of the sort function in reporting.py so that it functions with tuples
        Defined locally within another function because this is its only use

        :param comp: List of components to sort
        :return: Sorted list of component tuples
        """
        if len(comp) <= 1:
            return comp

        # select the first element in the array to be the pivot
        pivot = comp[0][1]

        # create two empty lists to act as buckets, one for elements less than the pivot and one for elements greater than the pivot
        less = []
        greater = []

        # iterate over the rest of the array
        for i in range(1, len(comp)):
            # if the element is less than the pivot, add it to the less_than list otherwise, add it to the greater_than list
            if comp[i][1] < pivot:
                less.append(comp[i])
            else:
                greater.append(comp[i])

        # call sort on the less_than list, then the greater_than list, then combine the sorted lists and return them
        return sort_components(less) + [comp[0]] + sort_components(greater)

    sorted_components = sort_components(components)
    # Create line to write to file
    output_strings = []
    for i in range(len(sorted_components)):
        output_strings.append(f"Connected Component {sorted_components[i][0]}, number of pixels = {sorted_components[i][1]}")

    # Opens and overwrites the cc-output-2b.txt file if it exists, else it makes a new one
    with open("outputs/cc-output-2b.txt", 'w') as f:
        # Writes all lines to the file
        for line in output_strings:
            f.write(line)
            f.write("\n")
        # Writes the total number of connected components to the end of the file
        f.write(f"Total number of connected components = {len(sorted_components)}")

    # Very hacked together use of the filter_pixels function :)
    top_two_map = filter_pixels(mark, sorted_components[0][0], sorted_components[1][0], top_two_condition)
    # Save the binary image of the top two components as a jpg file
    mat_plot.imsave("outputs/cc-top-2.jpg", np.uint8(top_two_map))

