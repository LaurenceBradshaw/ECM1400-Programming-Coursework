# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
from typing import Union
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime
import csv


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


def read_file(file_name: str) -> Union[list[dict], None]:
    try:
        # Read the file
        with open("data/{}".format(file_name)) as f:
            data = [{key: value for key, value in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
    # File was not found
    except FileNotFoundError:
        return None

    # Merge date and time fields into datetime objects
    for d in data:
        date = datetime.date.fromisoformat(d['date'])

        time_as_list = d['time'].split(':')
        time = datetime.time(int(time_as_list[0]) - 1)

        d['datetime'] = datetime.datetime.combine(date, time)

    return data


def read_image(file_name: str) -> Union[np.ndarray, None]:
    try:
        img = plt.imread(f"data/{file_name}")
        return img
    except FileNotFoundError:
        return None


def sort(values: Union[list, np.array]) -> list:
    """
    Returns a sorted (smallest to largest) list
    :param values: list/array to sort
    :return: sorted list
    """

    output = []
    for i in range(len(values)):
        # Find the smallest value
        index = minvalue(values)
        # Append and remove it from the list
        output.append(values[index])
        values.pop(index)

    return output


def remove_no_value(data: list):
    for element in data.copy():
        if element == "No data":
            data.remove(element)


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
    Finds the number of instances of xw in the input list/array
    :param values: List/array of values to check for xw in
    :param xw: The value to count the number of instances of
    :return: The number of instances of xw
    """

    # Holds the number of occurrences of xw found in values
    xw_count = 0
    # For each element in values, if it is equal to xw, add 1 to xw_count
    for element in values:
        if element == xw:
            xw_count += 1

    return xw_count

