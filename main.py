# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
import datetime
import os
import re
import numpy as np
import reporting
import monitoring
import intelligence
import sys
import utils
import pandas as pd

# -------------------------
# My custom functions
# -------------------------


def get_pollutant() -> str:
    """
    Lists the options for the different pollutants and gets the users input
    :return: selected pollutant
    """
    valid_options_regex = '[nN][oO]|[pP][mM](10|25)'
    menu_options = "----------AQUA System Reporting Module-----------\n" \
                   "Select a pollutant:\n" \
                   "• NO - Nitric Oxide\n" \
                   "• PM10 - Particulate Matter 10\n" \
                   "• PM25 - Particulate Matter 2.5"
    pollutant = utils.get_valid_user_input(menu_options, valid_options_regex)
    utils.clear()
    return pollutant.lower()


def get_file(files: list, module_str: str) -> str:
    valid_options_regex = '[0-9]*'
    chosen_file = ''
    while True:
        menu_options = f"---------AQUA System {module_str} Module----------\n" \
                       "Select a file to use:"
        for i, file in enumerate(files):
            menu_options += f'\n[{i}] - {file}'
        file_index_chosen = utils.get_valid_user_input(menu_options, valid_options_regex)
        try:
            chosen_file = files[int(file_index_chosen)]
            break
        except IndexError:
            utils.clear()

    utils.clear()
    return chosen_file


def get_date() -> datetime.datetime:
    while True:
        valid_date_regex = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
        menu_options = "----------AQUA System Reporting Module-----------\n" \
                       "Enter a date in the form YYYY-MM-DD:"

        user_choice = utils.get_valid_user_input(menu_options, valid_date_regex)
        try:
            date = datetime.datetime.fromisoformat(user_choice)
            break
        except ValueError:
            utils.clear()

    return date


# -------------------------
# Template Functions
# -------------------------


def main_menu():
    """
    Will list the all the available modules that can be accessed and then get the user's choice and redirect them to the correct module
    ----------------------
    Options
    ----------------------
    • R - Access the Pollution Reporting module
    • I - Access the Mobility Intelligence module
    • M - Access the Real-time Monitoring module
    • A - Print the About text
    • Q - Quit the application
    :return: None
    """

    # Define the regex that will be used to check if the users input to the menu is a valid choice
    valid_options_regex = '[rimaqRIMAQ]'
    # Define the menu string to print
    menu_options = "--------------AQUA System Main Menu--------------\n" \
                   "• R - Access the Pollution Reporting module\n" \
                   "• I - Access the Mobility Intelligence module\n" \
                   "• M - Access the Real-time Monitoring module\n" \
                   "• A - Print the About text\n" \
                   "• Q - Quit the application"
    # while loop is used so the user can come back to the main menu and the program not close until they pick quit
    while True:
        # Clear the console of text
        utils.clear()
        # Get the user input
        user_choice = utils.get_valid_user_input(menu_options, valid_options_regex)
        # Open the menu requested by the user
        if user_choice.lower() == 'r':
            reporting_menu()
        elif user_choice.lower() == 'i':
            intelligence_menu()
        elif user_choice.lower() == 'm':
            monitoring_menu()
        elif user_choice.lower() == 'a':
            about()
        elif user_choice.lower() == 'q':
            quit()


def reporting_menu():
    """
    Lists the available options for the reporting module and gets the user input to perform the requested operation
    ----------------------
    Options
    ----------------------
    • DA - Calculate the daily average
    • DM - Calculate the daily median
    • HA - Calculate the hourly average
    • MA - Calculate the monthly average
    • C - Count the number of rows with missing data
    • F - Fill missing data rows
    • B - Return to main menu
    :return: None
    """

    while True:
        utils.clear()
        # Loading all data files
        # Finds all the files in the data directory
        file_names = os.listdir("data")
        # Regex to find files that end with .csv
        csv_regex = re.compile('.*\\.csv')
        # Gets names of all the csv files in the directory
        csv_files = list(filter(csv_regex.match, file_names))
        # Reads each csv into a dictionary of pandas dataframes
        data = {}
        for file in csv_files:
            data[file] = utils.read_file(file)

        # List options and get user input
        valid_options_regex = '[dD][mM]|[dhDHmM][aA]|[cfbCFB]|[pP][hH]'
        menu_options = "----------AQUA System Reporting Module-----------\n" \
                       "Select an operation:\n" \
                       "• DA - Calculate the daily average\n" \
                       "• DM - Calculate the daily median\n" \
                       "• HA - Calculate the hourly average\n" \
                       "• MA - Calculate the monthly average\n" \
                       "• PH - Peak value at a specified date\n" \
                       "• C - Count the number of rows with missing data\n" \
                       "• F - Fill missing data rows\n" \
                       "• B - Return to main menu"
        user_choice = utils.get_valid_user_input(menu_options, valid_options_regex)
        utils.clear()

        if user_choice.lower() != 'b':
            chosen_file = get_file(csv_files, "Reporting")
            pollutant = get_pollutant()
        else:
            break

        if user_choice.lower() == 'da':
            output = reporting.daily_average(data, chosen_file, pollutant)
            print(output)
            input()
        elif user_choice.lower() == 'dm':
            reporting.daily_median(data, chosen_file, pollutant)
        elif user_choice.lower() == 'ha':
            reporting.hourly_average(data, chosen_file, pollutant)
        elif user_choice.lower() == 'ma':
            reporting.monthly_average(data, chosen_file, pollutant)
        elif user_choice.lower() == 'ph':
            date = get_date()
            reporting.peak_hour_date(data, date, chosen_file, pollutant)
        elif user_choice.lower() == 'c':
            reporting.count_missing_data(data, chosen_file, pollutant)
        elif user_choice.lower() == 'f':
            about()


def monitoring_menu():
    """
    Lists the available options for the monitoring module and gets the user input to perform the requested operation
    :return: None
    """


def intelligence_menu():
    """
    Lists the available options for the intelligence module and gets the user input to perform the requested operation
    :return:
    """
    while True:
        utils.clear()
        # Finds all the files in the data directory
        file_names = os.listdir("data")
        # Regex to find files that end with .png
        csv_regex = re.compile('.*\\.png')
        # Gets names of all the png files in the directory
        png_file_names = list(filter(csv_regex.match, file_names))

        # List options and get user input
        valid_options_regex = '[fF][rRcC]|[sS]?[cC]{2}|[bB]'
        menu_options = "---------AQUA System Intelligence Module---------\n" \
                       "Select an operation:\n" \
                       "• FR - Filter red pixels\n" \
                       "• FC - Filter cyan pixels\n" \
                       "• CC - Find connected components\n" \
                       "• SCC - Find connected components sorted\n" \
                       "• B - Return to main menu"
        user_choice = utils.get_valid_user_input(menu_options, valid_options_regex)
        utils.clear()

        if user_choice.lower() != 'b':
            file_name = get_file(png_file_names, "Intelligence")
        else:
            break

        if user_choice.lower() == 'fr':
            intelligence.find_red_pixels(file_name, upper_threshold=100, lower_threshold=50)
        elif user_choice.lower() == 'fc':
            intelligence.find_cyan_pixels(file_name, upper_threshold=100, lower_threshold=50)
        elif user_choice.lower() == 'cc':
            valid_options_regex = '[fF][rRcC]'
            menu_options = "---------AQUA System Intelligence Module---------\n" \
                           "Select types of pixel to find connected components for:\n" \
                           "• FR - Filter red pixels\n" \
                           "• FC - Filter cyan pixels\n"
            filter_choice = utils.get_valid_user_input(menu_options, valid_options_regex)
            if filter_choice.lower() == 'fr':
                filtered = intelligence.find_red_pixels(file_name, upper_threshold=100, lower_threshold=50)
            else:
                filtered = intelligence.find_cyan_pixels(file_name, upper_threshold=100, lower_threshold=50)

            intelligence.detect_connected_components(filtered)
        elif user_choice.lower() == 'scc':
            valid_options_regex = '[fF][rRcC]'
            menu_options = "---------AQUA System Intelligence Module---------\n" \
                           "Select types of pixel to find connected components for:\n" \
                           "• FR - Filter red pixels\n" \
                           "• FC - Filter cyan pixels\n"
            filter_choice = utils.get_valid_user_input(menu_options, valid_options_regex)
            if filter_choice.lower() == 'fr':
                filtered = intelligence.find_red_pixels(file_name, upper_threshold=100, lower_threshold=50)
            else:
                filtered = intelligence.find_cyan_pixels(file_name, upper_threshold=100, lower_threshold=50)

            mark = intelligence.detect_connected_components(filtered)
            intelligence.detect_connected_components_sorted(mark)


def about():
    """
    Prints the course module code and my candidate number
    :return: None
    """
    # Clear the console of text
    utils.clear()

    # List the about information and get user input to return to main menu
    valid_options_regex = ".*"
    menu_options = "-------------------About AQUA--------------------\n" \
                   "Module Code: ECM1400\n" \
                   "Candidate Number: 239766\n" \
                   "• Anykey - Return to main menu"

    utils.get_valid_user_input(menu_options, valid_options_regex)


def quit():
    """
    Stops the execution of the program
    :return: None
    """

    sys.exit("Program has quit")


if __name__ == '__main__':
    main_menu()

