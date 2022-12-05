# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
from typing import Union
import numpy as np

# -------------------------
# My custom functions
# -------------------------


def check_numeric(values: Union[list, np.array], exception_message: str):
    """
    ---------------
    Description
    ---------------
    Will check the input list/array for non-numeric values
    Raises ValueError exception with the given message if a non-numeric value was found

    ---------------
    General Overview
    ---------------
    For each element in the input data
    If the data type is not int or float
    Raise an exception

    :param values: List/array of the values to check
    :param exception_message: Message to display with the exception if a non-numeric is found
    :return: None
    """

    # For each element in values, convert it to a string can check if it is numeric
    for element in values:
        if type(element) != int and type(element) != float:
            raise ValueError(exception_message)


def remove_no_value(data: list):
    """
    ---------------
    Description
    ---------------
    Removes all 'No data' values from the input data

    ---------------
    General Overview
    ---------------
    For each element in the data
    If it is 'No data'
    Remove it from the list

    :param data: Data to remove 'No data' entries from
    :return: None
    """

    for element in data.copy():
        if element == "No data":
            data.remove(element)


# -------------------------
# Template functions
# -------------------------


def sumvalues(values):
    """
    ---------------
    Description
    ---------------
    Will take an input list/array and sum all the values in it
    Raises ValueError exception if a non-numeric value is present in the input

    ---------------
    General Overview
    ---------------
    Check for non-numeric values
    For each value in the data
    Add it to a sum variable

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
    ---------------
    Description
    ---------------
    Will find the largest value in the input list/array
    Raises ValueError exception if a non-numeric value is present in the input

    ---------------
    General Overview
    ---------------
    Check for non-numeric values
    Starting with the item at the 0th index as the current max
    For each value check to see if it is larger than the current max
    If so make that value the current max
    Return the index of the current max

    :param values: List/array that will contain the values to find the max of
    :return: The index of the maximum value found in values parameter
    """

    # Check for non-numeric values
    check_numeric(values, "Cannot find maximum with non-numeric values present")
    # Check for no values
    if len(values) == 0:
        raise ValueError("No values present to find maximum for")

    # Holds the current maximum value found in the input
    current_max = values[0]
    # For each element in values
    for element in values:
        # Check if it is greater than the current found maximum
        if element > current_max:
            # Set the element to the new current maximum
            current_max = element

    return values.index(current_max)


def minvalue(values):
    """
    ---------------
    Description
    ---------------
    Will find the smallest value in the input list/array
    Raises ValueError exception if a non-numeric value is present in the input

    ---------------
    General Overview
    ---------------
    Check for non-numeric values
    Starting with the item at the 0th index as the current min
    For each value check to see if it is smaller than the current min
    If so make that value the current min
    Return the index of the current min

    :param values: List/array that will contain the values to find the min of
    :return: The index of the minimum value found in values parameter
    """

    # Check for non-numeric values
    check_numeric(values, "Cannot find minimum with non-numeric values present")
    # Check for no values
    if len(values) == 0:
        raise ValueError("No values present to find minimum for")

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
    ---------------
    Description
    ---------------
    Finds the arithmetic mean of the input list/array

    ---------------
    General Overview
    ---------------
    Check for non-numeric values in the data
    Get the number of items in the data
    If there are no items in the input data return 0
    Sum up values
    Divide by number of values

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
    ---------------
    Description
    ---------------
    Finds the number of instances of xw in the input list/array

    ---------------
    General Overview
    ---------------
    For each value
    Check if it is the value being counted
    If so add one to a counter

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

