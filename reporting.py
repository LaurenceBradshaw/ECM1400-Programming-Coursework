# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification
from datetime import datetime, timedelta
from typing import Union
import numpy as np
import utils


# -------------------------
# My custom functions
# -------------------------


def sort(values: Union[list, np.array]) -> list:
    """
    ---------------
    Description
    ---------------
    Returns a sorted (smallest to largest) list
    Implementation of the quicksort algorithm

    ---------------
    General Overview
    ---------------
    If there are less than 2 elements, the array is sorted
    Find a pivot
    Sort into values greater than and less than the pivot

    :param values: list/array to sort
    :return: sorted list
    """

    # if the input array has 1 or fewer elements, it is already sorted
    if len(values) <= 1:
        return values

    # select the first element in the array to be the pivot
    pivot = values[0]

    # create two empty lists, one for elements less than the pivot and one for elements greater than the pivot
    less = []
    greater = []

    # iterate over the rest of the array
    for i in range(1, len(values)):
        # if the element is less than the pivot, add it to the less_than list otherwise, add it to the greater_than list
        if values[i] < pivot:
            less.append(values[i])
        else:
            greater.append(values[i])

    # call sort on the less_than list, then the greater_than list, then combine the sorted lists and return them
    return sort(less) + [pivot] + sort(greater)


def get_time_range(data: list[dict], start_date: datetime, end_date: datetime, pollutant: str):
    """
    ---------------
    Description
    ---------------
    Will get data within the specified date ranges for a given pollutant

    ---------------
    General Overview
    ---------------
    For each entry in the data
    If the date field is within the date range
    Add the pollutant value to the list

    :param data: data to get subset from
    :param start_date: starting date for data to return (inclusive)
    :param end_date: ending date for data to return (exclusive)
    :param pollutant: Pollutant to get values for
    :return: List of values within the time range
    """
    data_in_range = []
    for d in data:
        if start_date <= d['datetime'] < end_date:
            data_in_range.append(d[pollutant])

    return data_in_range


def add_month(date: datetime):
    """
    ---------------
    Description
    ---------------
    Will add a month to the given date

    ---------------
    General Overview
    ---------------
    Get the month number for the given date
    Add one
    If its larger than 12
    Add a year to the date
    Else
    Replace the old month with the new month

    :param date:
    :return:
    """
    new_month = date.month + 1
    if new_month < 13:
        new_date = date.replace(month=new_month)
    else:
        new_date = date.replace(year=date.year + 1, month=1)

    return new_date


# -------------------------
# Template Functions
# -------------------------


def daily_average(data, monitoring_station, pollutant):
    """
    ---------------
    Description
    ---------------
    Finds the average level of the given pollutant per day
    Will omit data values that are 'No data' and notify the user
    Sum of pollutant values / number of valid data points in the day

    Example:
    Sum of all values for the pollutant on 2021-01-01 / number of hours in that day that are not 'No data'

    ---------------
    General Overview
    ---------------
    Iterate through each day in the year
    Remove 'No data' entries
    Add up the values for the given pollutant
    Find average

    :param data: Dictionary containing lists of dictionaries representing each monitoring station
    :param monitoring_station: The monitoring station to use
    :param pollutant: The pollutant to use
    :return: A list containing the daily averages
    """

    station_data = data[monitoring_station]

    missing_data_count = count_missing_data(data, monitoring_station, pollutant)
    if missing_data_count > 0:
        print(f'{missing_data_count} values contained \'No data\' and have been omitted from the calculations')

    output = []
    start_date = station_data[0]['datetime']
    time_delta = timedelta(days=1)

    for day in range(365):
        daily_sum = 0

        daily_data = get_time_range(station_data, start_date, start_date + time_delta, pollutant)
        utils.remove_no_value(daily_data)
        daily_data = [float(d) for d in daily_data]

        # If there is no data of the day the output for that day is 'No data'
        if len(daily_data) == 0:
            output.append('No data')

        else:
            output.append(utils.meannvalue(daily_data))

        start_date += time_delta

    return output


def daily_median(data, monitoring_station, pollutant):
    """
    ---------------
    Description
    ---------------
    Finds the median level of the given pollutant per day
    Will omit data values that are 'No data' and notify the user

    ---------------
    General Overview
    ---------------
    Get data for the day
    Remove values with 'No data'
    Order the values smallest to biggest and take the middle one for each day

    :param data: Dictionary containing lists of dictionaries representing each monitoring station
    :param monitoring_station: The monitoring station to use
    :param pollutant: The pollutant to use
    :return: An array containing the daily medians
    """

    station_data = data[monitoring_station]
    output = []

    missing_data_count = count_missing_data(data, monitoring_station, pollutant)
    if missing_data_count > 0:
        print(f'{missing_data_count} values contained \'No data\' and have been omitted from the calculations')

    # Sets the start date and difference in time
    start_date = station_data[0]['datetime']
    time_delta = timedelta(days=1)

    # For each day in the year, get the values for that day, remove 'No data' and find the median
    for i in range(365):
        day_values = get_time_range(station_data, start_date, start_date + time_delta, pollutant)
        utils.remove_no_value(day_values)  # This may change the length of the list so later indexes could be any length
        day_values = [float(d) for d in day_values]
        sorted_values = sort(day_values)
        # If there is no data for all values in the day, return 'No data' as median
        if len(sorted_values) == 0:
            output.append('No data')
        else:
            # If there is an odd number of values, an integer middle index can be found
            if len(sorted_values) % 2 == 1:
                mid_index = int((len(sorted_values) + 1) / 2)
                output.append(sorted_values[mid_index - 1])
            # If there is an even number of values, take the average of the two values either side of the mid index
            else:
                mid_index_upper = len(sorted_values)//2
                mid_index_lower = len(sorted_values)//2 - 1
                upper_value = sorted_values[mid_index_upper - 1]
                lower_value = sorted_values[mid_index_lower - 1]
                output.append((upper_value + lower_value) / 2)

        # Get date for next day
        start_date += time_delta

    return output


def hourly_average(data, monitoring_station, pollutant):
    """
    ---------------
    Description
    ---------------
    Finds the average level of the given pollutant at every hour across the year
    Will omit data values that are 'No data' and notify the user
    Sum of pollutant values at an hour per day / number of valid data points for that hour

    Example:
    Sum of values at 01:00:00 across all days in the year / number of values at 01:00:00 that are not 'No data' across all days in the year

    ---------------
    General Overview
    ---------------
    Get the value at each hour across all days
    Remove 'No data' entries
    Find average

    :param data: Dictionary containing lists of dictionaries representing each monitoring station
    :param monitoring_station: The monitoring station to use
    :param pollutant: The pollutant to use
    :return: An array containing the hourly averages
    """

    station_data = data[monitoring_station]
    # Stores the averages
    output = []

    missing_data_count = count_missing_data(data, monitoring_station, pollutant)
    if missing_data_count > 0:
        print(f'{missing_data_count} values contained \'No data\' and have been omitted from the calculations')

    # Sets the start date and difference in time
    start_date = station_data[0]['datetime']
    time_delta_day = timedelta(days=1)
    time_delta_hour = timedelta(hours=1)

    # For every hour
    for j in range(24):
        hour_values = []
        # For every day in the year
        for i in range(365):
            # Get the value of pollutant for that hour and increment the day by 1
            hour_values += get_time_range(station_data, start_date, start_date + time_delta_hour, pollutant)
            start_date += time_delta_day

        # Remove 'No data' and calculate average
        utils.remove_no_value(hour_values)
        hour_values = [float(value) for value in hour_values]

        if len(hour_values) == 0:
            output.append('No data')
        else:
            output.append(utils.meannvalue(hour_values))

        # Get the date with the next hour
        # Since the first 24 values in the file will be the first day of each hour can use the index to get next hour date
        start_date = station_data[j + 1]['datetime']

    return output


def monthly_average(data, monitoring_station, pollutant):
    """
    ---------------
    Description
    ---------------
    Finds the average level of the given pollutant per month
    Will omit data values that are 'No data' and notify the user
    Sum of pollutant values for that month / number of valid data points

    Example:
    Sum of values for January / number of data points in January that are not 'No data'

    ---------------
    General Overview
    ---------------
    Iterate through each month in the year
    Remove 'No data' entries
    Add up the values for the given pollutant
    Find average for that month

    :param data: Dictionary containing lists of dictionaries representing each monitoring station
    :param monitoring_station: The monitoring station to use
    :param pollutant: The pollutant to use
    :return: An array containing the monthly averages
    """

    station_data = data[monitoring_station]
    # Stores the averages
    output = []

    missing_data_count = count_missing_data(data, monitoring_station, pollutant)
    if missing_data_count > 0:
        print(f'{missing_data_count} values contained \'No data\' and have been omitted from the calculations')

    # Sets the start date and difference in time
    start_date = station_data[0]['datetime']

    # For each day in the year, get the values for that day, remove 'No data' and find the average
    for i in range(12):
        end_date = add_month(start_date)
        month_values = get_time_range(station_data, start_date, end_date, pollutant)
        utils.remove_no_value(month_values)
        month_values = [float(value) for value in month_values]

        # If there is no data for the month append 'No data' for that month
        if len(month_values) == 0:
            output.append('No data')
        else:
            output.append(utils.meannvalue(month_values))

        start_date = end_date

    return output


def peak_hour_date(data, date, monitoring_station, pollutant):
    """
    ---------------
    Description
    ---------------
    For a given date it will find the hour with the highest amount of pollution

    ---------------
    General Overview
    ---------------
    Find the specified date
    Get data for that day
    Remove 'No data' entries
    Find max value

    :param data: Dictionary containing lists of dictionaries representing each monitoring station
    :param date: Date to find the peak value for
    :param monitoring_station: The monitoring station to use
    :param pollutant: The pollutant to use
    :return: Tuple containing the hour and value
    """

    # Gets the correct data for the monitoring station from the data dictionary
    station_data = data[monitoring_station]
    time_delta = timedelta(days=1)

    # Gets all the values for the specified date and remove 'No data'
    day_values = get_time_range(station_data, date, date + time_delta, pollutant)
    utils.remove_no_value(day_values)
    day_values = [float(value) for value in day_values]

    # If all the values for the day are 'No data'
    if len(day_values) == 0:
        return 'No data for given date', 0

    # Find the largest
    max_value_index = utils.maxvalue(day_values)
    max_value = day_values[max_value_index]
    # Format the hour into a string. Add one to realign with the original data that was altered when reading the file
    hour = f'{max_value_index + 1}:00:00'

    return hour, max_value


def count_missing_data(data, monitoring_station, pollutant):
    """
    ---------------
    Description
    ---------------
    Counts the number of 'No data' entries in the data

    ---------------
    General Overview
    ---------------
    Get correct station data
    Iterate through each data entry
    If the data entry for the pollutant is 'No data' add 1 to count

    :param data: Dictionary containing lists of dictionaries representing each monitoring station
    :param monitoring_station: The monitoring station to use
    :param pollutant: The pollutant to use
    :return: The number of 'No data' entries
    """

    # Gets the correct data for the monitoring station from the data dictionary
    station_data = data[monitoring_station]

    count = 0
    for d in station_data:
        if d[pollutant] == 'No data':
            count += 1

    return count


def fill_missing_data(data, new_value, monitoring_station, pollutant):
    """
    ---------------
    Description
    ---------------
    Will replace all 'No data' entries with the new value

    ---------------
    General Overview
    ---------------
    Iterate over each entry
    If the entry is 'No data' replace it with the new value cast to a float
    Replace the old data from the data parameter with the new data

    :param data: Dictionary containing lists of dictionaries representing each monitoring station
    :param new_value: The value to replace 'No data' with
    :param monitoring_station: The monitoring station to use
    :param pollutant: The pollutant to use
    :return: Data in the original data parameter format
    """

    station_data = data[monitoring_station].copy()

    for d in station_data:
        if d[pollutant] == 'No data':
            d[pollutant] = float(new_value)

    data[monitoring_station] = station_data

    return data
