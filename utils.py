# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
from typing import Union
import numpy as np
import matplotlib.image as mpimg
import pandas as pd
from skimage import io
import os
import re
import datetime


# -------------------------
# My custom functions
# -------------------------


def clear():
    """
    Clears the text in the console

    :return: None
    """
    os.system('cls')


def check_numeric(values: Union[list, np.array], exception_message: str):
    """
    Will check the input list/array for non-numeric values
    Raises ValueError exception with the given message if a non-numeric value was found
    :param values: List/array of the values to check
    :param exception_message: Message to display with the exception if a non-numeric is found
    :return: None
    """

    # For each element in values, convert it to a string can check if it is numeric
    for element in values:
        if type(element) != int and type(element) != float:
            raise ValueError(exception_message)


def read_image(img_name: str) -> Union[np.ndarray, None]:
    """
    Reads the image located by the image name in the data folder into an ndarray
    :param img_name: name for the image being read
    :return: returns an ndarray containing RGBA values for each pixel if the file was found and read or None if it wasn't
    """

    try:
        # Read the image
        img = io.imread("data/{}.png".format(img_name))
    # The file was not found, caused by the user inputting the name of a file that does not exist in the data directory
    except FileNotFoundError:
        return None
    return img


def get_valid_user_input(menu_text: str, regex: str) -> str:
    """
    Used to get a valid response from a user for a menu

    :param menu_text: The different options to be displayed for the user to pick from
    :param regex: Regex used to find the valid input
    :return: The valid user input
    """

    while True:
        # Print the options to the screen
        print(menu_text)
        # Get the users input
        user_choice = input("=> ")
        # Check the user input against the provided regex
        re_match = re.fullmatch(regex, user_choice)
        # If a match is not found - invalid input - clear the console so the menu can be cleanly displayed
        if re_match is None:
            clear()
        # else a match is found - valid input
        else:
            return user_choice


def read_file(file_name: str) -> Union[pd.DataFrame, None]:
    """
    Reads the file with the specified name in the data directory

    :param file_name: Name of the file to read
    :return: Pandas dataframe containing the data
    """

    data = []
    try:
        # Read the file
        with open("data/{}".format(file_name)) as f:
            for line in f:
                # Append the line to the data list and remove the newline character at the end of the line
                data.append(line[:-1].split(','))
    # File was not found
    except FileNotFoundError:
        return None

    # Converting the data from the csv into a dictionary:
    # Remove headings from the data file
    headings = data.pop(0)
    # Remove the date and time column headings
    headings = headings[2:]
    # Make the headings into dictionary keys with an empty list as the value
    data_dict = {'datetime': []}
    for heading in headings:
        data_dict[heading] = []

    for i in range(len(data)):
        # Merge the date and time columns into a datetime object
        date = datetime.date.fromisoformat(data[i][0])

        # Minus an hour from the time to represent the start of the measurement interval instead of the end
        time_as_list = data[i][1].split(':')
        time = datetime.time(int(time_as_list[0]) - 1)

        # Combine the date and time objects
        data_dict['datetime'].append(datetime.datetime.combine(date, time))
        # Append remaining data to the dictionary
        for j, heading in enumerate(headings):
            try:
                data_dict[heading].append(float(data[i][j + 2]))
            except ValueError:
                data_dict[heading].append(data[i][j + 2])

    # Convert the dictionary to a pandas dataframe
    # Could have read the csv using pandas directly but i felt doing it this way meant the i could convert the date and time columns to a date time object easier
    return pd.DataFrame(data_dict)


# -------------------------
# Template functions
# -------------------------


def sumvalues(values):
    """
    Will take an input list/array and sum all the values in it
    Raises ValueError exception if a non-numeric value is present in the input
    :param values: List/array that will contain the values to sum
    :return: Sum of the values in the values parameter
    """

    # Check for non-numeric values
    check_numeric(values, "Cannot sum non-numeric values")

    # Holds the current sum value
    sum = 0
    # For each element in values, add its value to the sum value
    for element in values:
        sum += element

    return sum


def maxvalue(values):
    """
    Will find the largest value in the input list/array
    Raises ValueError exception if a non-numeric value is present in the input
    :param values: List/array that will contain the values to find the max of
    :return: The index of the maximum value found in values parameter
    """

    # Check for non-numeric values
    check_numeric(values, "Cannot find maximum with non-numeric values present")

    # Holds the current maximum value found in the input
    current_max = 0
    # For each element in values
    for element in values:
        # Check if it is greater than the current found maximum
        if element > current_max:
            # Set the element to the new current maximum
            current_max = element

    return values.index(current_max)


def minvalue(values):
    """
    Will find the smallest value in the input list/array
    Raises ValueError exception if a non-numeric value is present in the input
    :param values: List/array that will contain the values to find the min of
    :return: The index of the minimum value found in values parameter
    """

    # Check for non-numeric values
    check_numeric(values, "Cannot find minimum with non-numeric values present")

    # Holds the current minimum value found in the input
    # Set to the first element of values to start
    current_min = values[0]
    # For each element in values
    for element in values:
        # Check if it is less than the current found minimum
        if element < current_min:
            # Set the element to the new current minimum
            current_min = element

    return values.index(current_min)


def meannvalue(values):
    """
    Finds the arithmetic mean of the input list/array
    :param values: List/array that will contain the values to find the mean of
    :return: The arithmetic mean
    """

    # Check for non-numeric values
    check_numeric(values, "Cannot find mean with non-numeric values present")

    # Number of elements present in values
    num_values = len(values)
    # If there are no elements in values, return 0 to avoid divide by zero
    if num_values == 0:
        return 0

    # Sum of values
    sum_values = sumvalues(values)
    # Mean of values
    mean = sum_values/num_values
    return mean


def countvalue(values, xw):
    """
    Finds the number of instances of x in the input list/array
    :param values: List/array of values to check for x in
    :param xw: The value to count the number of instances of
    :return: The number of instances of x
    """

    # Holds the number of occurrences of x found in values
    x_count = 0
    # For each element in values, if it is equal to x, add 1 to x_count
    for element in values:
        if element == xw:
            x_count += 1

    return x_count

