# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
from datetime import datetime, timedelta
import pandas as pd
import utils

# -------------------------
# My custom functions
# -------------------------


def get_time_range(data: pd.DataFrame, start_date: datetime, end_date: datetime):
    data_in_range = []
    for row in data.values:
        if start_date <= row[0] < end_date:
            data_in_range.append(row[1])

    return data_in_range


def remove_no_value(data: list):
    for element in data.copy():
        if element == "No data":
            data.remove(element)


def add_month(date: datetime):
    new_month = date.month + 1
    if new_month < 13:
        new_date = date.replace(month=new_month)
    else:
        new_date = date.replace(year=date.year + 1, month=1)

    return new_date


# -------------------------
# Template Functions
# -------------------------


def daily_average(data, monitoring_station: str, pollutant: str):
    """
    Finds the average level of the given pollutant per day
    Will omit data values that are 'No data' and notify the user
    Sum of pollutant values / number of valid data points in the day

    Example:
    Sum of all values for the pollutant on 2021-01-01 / number of hours in that day that are not 'No data'

    :param data: Dictionary containing pandas dataframes for each monitoring station
    :param monitoring_station: The monitoring station to use
    :param pollutant: The pollutant to use
    :return: A list containing the daily averages
    """

    missing_data_count = count_missing_data(data, monitoring_station, pollutant)
    if missing_data_count > 0:
        print(f'{missing_data_count} values contain \'No data\' and have been omitted from the calculations')

    # Stores the averages
    output = []

    # Gets the correct data for the monitoring station from the data dictionary
    station_data = data[monitoring_station]
    # Takes just the datetime and pollutant that was specified columns from the dataframe
    date_and_pollutant = station_data[['datetime', pollutant]]

    # Sets the start date and difference in time
    start_date = date_and_pollutant['datetime'][0]
    time_delta = timedelta(days=1)

    # For each day in the year, get the values for that day, remove 'No data' and find the average
    for i in range(365):
        day_values = get_time_range(date_and_pollutant, start_date, start_date + time_delta)
        remove_no_value(day_values)
        output.append(utils.meannvalue(day_values))
        start_date += time_delta

    return output


def daily_median(data, monitoring_station: str, pollutant: str):
    """
    Finds the median level of the given pollutant per day
    Will omit data values that are 'No data' and notify the user
    Largest - smallest value of the given pollutant per day

    Example:
    Largest value of pollutant on 2021-01-01 - smallest value of pollutant on 2021-01-01
    Excluding values that are 'No data'

    :param data: Dictionary containing pandas dataframes for each monitoring station
    :param monitoring_station: The monitoring station to use
    :param pollutant: The pollutant to use
    :return: An array containing the daily medians
    """

    # Stores the averages
    output = []

    # Gets the correct data for the monitoring station from the data dictionary
    station_data = data[monitoring_station]
    # Takes just the datetime and pollutant that was specified columns from the dataframe
    date_and_pollutant = station_data[['datetime', pollutant]]

    # Sets the start date and difference in time
    start_date = date_and_pollutant['datetime'][0]
    time_delta = timedelta(days=1)

    # For each day in the year, get the values for that day, remove 'No data' and find the median
    for i in range(365):
        day_values = get_time_range(date_and_pollutant, start_date, start_date + time_delta)
        remove_no_value(day_values)
        max_value_index = utils.maxvalue(day_values)
        min_value_index = utils.minvalue(day_values)
        output.append(day_values[max_value_index] - day_values[min_value_index])
        start_date += time_delta

    return output


def hourly_average(data, monitoring_station: str, pollutant: str):
    """
    Finds the average level of the given pollutant at every hour across the year
    Will omit data values that are 'No data' and notify the user
    Sum of pollutant values at an hour per day / number of valid data points for that hour

    Example:
    Sum of values at 01:00:00 across all days in the year / number of values at 01:00:00 that are not 'No data' across all days in the year

    :param data: Dictionary containing pandas dataframes for each monitoring station
    :param monitoring_station: The monitoring station to use
    :param pollutant: The pollutant to use
    :return: An array containing the hourly averages
    """

    # Stores the averages
    output = []

    # Gets the correct data for the monitoring station from the data dictionary
    station_data = data[monitoring_station]
    # Takes just the datetime and pollutant that was specified columns from the dataframe
    date_and_pollutant = station_data[['datetime', pollutant]]

    # Sets the start date and difference in time
    start_date = date_and_pollutant['datetime'][0]
    time_delta_day = timedelta(days=1)
    time_delta_hour = timedelta(hours=1)

    # For every hour
    for j in range(24):
        hour_values = []
        # For every day in the year
        for i in range(365):
            # Get the value of pollutant for that hour and increment the day by 1
            hour_values += get_time_range(date_and_pollutant, start_date, start_date + time_delta_hour)
            start_date += time_delta_day

        # Remove 'No data' and calculate average
        remove_no_value(hour_values)
        output.append(utils.meannvalue(hour_values))

        # Reset the start date and add an hour to it
        start_date = date_and_pollutant['datetime'][0] + time_delta_hour

    return output


def monthly_average(data, monitoring_station: str, pollutant: str):
    """
    Finds the average level of the given pollutant per month
    Will omit data values that are 'No data' and notify the user
    Sum of pollutant values for that month / number of valid data points

    Example:
    Sum of values for January / number of data points in January that are not 'No data'

    :param data: Dictionary containing pandas dataframes for each monitoring station
    :param monitoring_station: The monitoring station to use
    :param pollutant: The pollutant to use
    :return: An array containing the monthly averages
    """

    # Stores the averages
    output = []

    # Gets the correct data for the monitoring station from the data dictionary
    station_data = data[monitoring_station]
    # Takes just the datetime and pollutant that was specified columns from the dataframe
    date_and_pollutant = station_data[['datetime', pollutant]]

    # Sets the start date and difference in time
    start_date = date_and_pollutant['datetime'][0]

    # For each day in the year, get the values for that day, remove 'No data' and find the average
    for i in range(12):
        end_date = add_month(start_date)
        month_values = get_time_range(date_and_pollutant, start_date, end_date)
        remove_no_value(month_values)
        output.append(utils.meannvalue(month_values))
        start_date = end_date

    return output


def peak_hour_date(data, date, monitoring_station: str, pollutant: str):
    """
    For a given date it will find the hour with the highest amount of pollution

    :param data: Dictionary containing pandas dataframes for each monitoring station
    :param date: Date to find the peak value for
    :param monitoring_station: The monitoring station to use
    :param pollutant: The pollutant to use
    :return: Tuple containing the hour and value
    """

    # Gets the correct data for the monitoring station from the data dictionary
    station_data = data[monitoring_station]
    # Takes just the datetime and pollutant that was specified columns from the dataframe
    date_and_pollutant = station_data[['datetime', pollutant]]

    time_delta = timedelta(days=1)

    # Gets all the values for the specified date
    day_values = get_time_range(date_and_pollutant, date, date + time_delta)
    # Find the largest
    max_value_index = utils.maxvalue(day_values)
    max_value = day_values[max_value_index]
    # Format the hour into a string. Add one to realign with the original data that was altered when reading the file
    hour = f'{max_value_index + 1}:00'

    return hour, max_value


def count_missing_data(data, monitoring_station: str, pollutant: str):
    """
    Counts the number of 'No data' entries in the data

    :param data: Dictionary containing pandas dataframes for each monitoring station
    :param monitoring_station: The monitoring station to use
    :param pollutant: The pollutant to use
    :return: The number of 'No data' entries
    """

    # Gets the correct data for the monitoring station from the data dictionary
    station_data = data[monitoring_station]
    # Takes just the specified pollutant column from the dataframe
    date_and_pollutant = station_data[pollutant]

    count = 0
    for element in date_and_pollutant:
        if element == 'No data':
            count += 1

    return count


def fill_missing_data(data, new_value, monitoring_station: str, pollutant: str):
    """
    Will replace all 'No data' entries with the new value

    :param data: Dictionary containing pandas dataframes for each monitoring station
    :param new_value: The value to replace 'No data' with
    :param monitoring_station: The monitoring station to use
    :param pollutant: The pollutant to use
    :return:
    """
    # Gets the correct data for the monitoring station from the data dictionary
    station_data = data[monitoring_station]
    # Takes just the specified pollutant column from the dataframe
    date_and_pollutant = station_data[pollutant]

