# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
import csv
import datetime
import os
import re
import time
from typing import Union
import reporting
import monitoring
import intelligence
import sys


class Menu:
    """
    This class is used to store the menu text and regex for menu's that are not dynamically created
    The aim is to make the rest of the code in main.py look less cluttered
    """

    class Pollutant:
        options = "Select a pollutant:\n" \
                    "• NO - Nitric Oxide\n" \
                    "• PM10 - Particulate Matter 10\n" \
                    "• PM25 - Particulate Matter 2.5"
        regex = '[nN][oO]|[pP][mM](10|25)'

    class Date:
        options = "Enter a date in the form YYYY-MM-DD:"
        regex = '[0-9]{4}-[0-9]{2}-[0-9]{2}'

    class Display:
        options = "Select a way to display data:\n" \
                       "• T - Table\n" \
                       "• G - Graph\n" \
                       "• B - Return to reporting menu"
        regex = "[tgbTGB]"

    class DisplaySave:
        options = "Select a way to display data:\n" \
                       "• T - Table\n" \
                       "• G - Graph\n" \
                       "• S - Save\n" \
                       "• B - Return to monitoring menu"
        regex = "[tgbsTGBS]"

    class Main:
        options = "--------------AQUA System Main Menu--------------\n" \
                       "• R - Access the Pollution Reporting module\n" \
                       "• I - Access the Mobility Intelligence module\n" \
                       "• M - Access the Real-time Monitoring module\n" \
                       "• A - Print the About text\n" \
                       "• Q - Quit the application"
        regex = '[rimaqRIMAQ]'

    class File:
        options = "Enter file name to save new data as:"
        regex = "^[\\w\\-. ]+$"

    class NewValue:
        options = "Input new value:"
        regex = "[0-9]+\\.[0-9]+"

    class Reporting:
        options = "----------AQUA System Reporting Module-----------\n" \
                       "Select an operation:\n" \
                       "• DA - Calculate the daily average\n" \
                       "• DM - Calculate the daily median\n" \
                       "• HA - Calculate the hourly average\n" \
                       "• MA - Calculate the monthly average\n" \
                       "• PH - Peak value at a specified date\n" \
                       "• C - Count the number of rows with missing data\n" \
                       "• F - Fill missing data rows\n" \
                       "• B - Return to main menu"
        regex = '[dD][mM]|[dhDHmM][aA]|[cfbCFB]|[pP][hH]'

    class Monitoring:
        options = "----------AQUA System Monitoring Module----------\n" \
                       "Select an operation:\n" \
                       "• G - List groups\n" \
                       "• S - List stations in a group\n" \
                       "• P - Get information about the different pollutants\n" \
                       "• N - Get news information\n" \
                       "• D - Get data from a station\n" \
                       "• B - Return to main menu"
        regex = '[gsdpbnGSDBPN]'

    class Intelligence:
        options = "---------AQUA System Intelligence Module---------\n" \
                       "Select an operation:\n" \
                       "• FR - Filter red pixels\n" \
                       "• FC - Filter cyan pixels\n" \
                       "• CC - Find connected components\n" \
                       "• SCC - Find connected components sorted\n" \
                       "• B - Return to main menu"
        regex = '[fF][rRcC]|[sS]?[cC]{2}|[bB]'

    class Filter:
        options = "Select types of pixel to find connected components for:\n" \
                       "• FR - Filter red pixels\n" \
                       "• FC - Filter cyan pixels"
        regex = '[fF][rRcC]'

    class About:
        options = "-------------------About AQUA--------------------\n" \
                       "Module Code: ECM1400\n" \
                       "Candidate Number: 239766\n" \
                       "• Anykey - Return to main menu"
        regex = ".*"

    class Group:
        options = "Enter group to get stations for:"
        regex = ".*"

    class Station:
        options = "Enter station code to get data for:"
        regex = ".*"

# -------------------------
# My custom functions
# -------------------------


def read_file(file_name: str) -> Union[list[dict], None]:
    """
    ---------------
    Description
    ---------------
    Reads the input file name into a list of dict
    If file name is not found, return None

    ---------------
    General Overview
    ---------------
    Open the file
    Use csv builtin library to read data into list of dict
    If no file found return None
    Merge date and time values into a datetime object

    :param file_name: Name of the file to read
    :return: List of dictionaries containing the data
    """
    try:
        # Read the file
        cwd = os.getcwd()
        with open("{}/data/{}".format(cwd, file_name), 'r') as f:
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


def get_pollutant() -> str:
    """
    ---------------
    Description
    ---------------
    Lists the options for the different pollutants and gets the users input

    ---------------
    Options
    ---------------
    • NO - Nitric Oxide
    • PM10 - Particulate Matter 10
    • PM25 - Particulate Matter 2.5

    :return: selected pollutant
    """

    pollutant = get_valid_user_input(Menu.Pollutant.options, Menu.Pollutant.regex)
    return pollutant.lower()


def get_file(files: list) -> str:
    """
    ---------------
    Description
    ---------------
    Lists files and gets the users input to select one

    :param files: List of files to display
    :return: File name of file selected
    """

    valid_options_regex = '[0-9]*'
    chosen_file = ''
    while True:
        menu_options = "Select a file to use:"
        for i, file in enumerate(files):
            menu_options += f'\n[{i}] - {file}'
        file_index_chosen = get_valid_user_input(menu_options, valid_options_regex)
        try:
            chosen_file = files[int(file_index_chosen)]
            break
        except IndexError:
            clear()

    return chosen_file


def get_date() -> datetime.datetime:
    """
    ---------------
    Description
    ---------------
    Gets the user to enter a date

    :return: the inputted date as a datetime object
    """

    while True:
        user_choice = get_valid_user_input(Menu.Date.options, Menu.Date.regex)
        try:
            date = datetime.datetime.fromisoformat(user_choice)
            break
        except ValueError:
            clear()

    return date


def get_daily_dates(start_date: datetime.datetime):
    """
    ---------------
    Description
    ---------------
    Will return daily dates from the start_date for the whole year

    :param start_date: First date listed in the file
    :return: List of daily dates for the year
    """
    dates = []
    day_time_delta = datetime.timedelta(days=1)
    for i in range(365):
        dates.append(str(start_date.date()))
        start_date += day_time_delta

    return dates


def get_hourly_times():
    """
    ---------------
    Description
    ---------------
    Returns the times 1:00:00 to 24:00:00

    :return: List of hours in a day
    """
    hours = []
    for i in range(24):
        hours.append(f"{i + 1}:00:00")

    return hours


def get_monthly_dates(start_date: datetime.datetime):
    """
    ---------------
    Description
    ---------------
    Will return the monthly dates beginning from the start_date

    :param start_date: First date listed in the file
    :return: List of monthly dates
    """
    dates = []
    for i in range(12):
        d = datetime.date(start_date.year, start_date.month, start_date.day)
        dates.append(str(d))

        start_date = reporting.add_month(start_date)

    return dates


def display_data(output, pollutant, time_steps):
    """
    ---------------
    Description
    ---------------
    Lists the different ways the used can display the data coming from the reporting module
    Borrows the data displaying functions from the monitoring module

    :param output: List of data values
    :param pollutant: Name of pollutant
    :param time_steps: List of dates/hours
    :return: None
    """

    # List the options and get user input
    display_type = get_valid_user_input(Menu.Display.options, Menu.Display.regex)

    display = ""

    # Convert data into list of dicts
    output_list_of_dicts = []
    for time, value in zip(time_steps, output):
        output_list_of_dicts.append({'time': time, 'data': str(value)})

    if display_type.lower() == 'b':  # Return to the reporting menu
        return

    elif display_type.lower() == 't':  # Display table
        # Make headings and table
        headings = [('Time for value', 'time'), ('Value', 'data')]
        display += monitoring.make_table(output_list_of_dicts, headings)

    elif display_type.lower() == 'g':  # Display graph
        # Convert data to dataframe
        display += monitoring.make_graph(output_list_of_dicts, 'data')

    # Display the data
    display += "\n• Anykey - Return to reporting menu"
    valid_options_regex = ".*"
    get_valid_user_input(display, valid_options_regex)


def get_valid_user_input(menu_text: str, regex: str) -> str:
    """
    ---------------
    Description
    ---------------
    Used to get a valid response from a user for a menu

    ---------------
    General Overview
    ---------------
    Print the menu
    Get user input
    Check it against the regex
    If there is a match return the input
    Repeat until input provides a match against the regex

    :param menu_text: The different options to be displayed for the user to pick from
    :param regex: Regex used to find the valid input
    :return: The valid user input
    """

    while True:
        # Clears the console of previous test
        clear()
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


def clear():
    """
    ---------------
    Description
    ---------------
    Clears the text in the console

    :return: None
    """
    os.system('cls')


# -------------------------
# Template Functions
# -------------------------


def main_menu():
    """
    ---------------
    Description
    ---------------
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
    # while loop is used so the user can come back to the main menu and the program not close until they pick quit
    while True:
        # Get the user input for the main menu
        user_choice = get_valid_user_input(Menu.Main.options, Menu.Main.regex)
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
    ---------------
    Description
    ---------------
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
        # Loading all data files
        # Finds all the files in the data directory
        file_names = os.listdir("data")
        # Regex to find files that end with .csv
        csv_regex = re.compile('.*\\.csv')
        # Gets names of all the csv files in the directory
        csv_files = list(filter(csv_regex.match, file_names))
        # Reads each csv into a list of dicts
        data = {}
        for file in csv_files:
            data[file] = read_file(file)

        # List options and get user input
        user_choice = get_valid_user_input(Menu.Reporting.options, Menu.Reporting.regex)

        # If the user has not chosen to return to the main menu get the file and pollutant that the user wishes to use
        if user_choice.lower() != 'b':
            chosen_file = get_file(csv_files)
            pollutant = get_pollutant()
        else:
            break

        start_date = data[chosen_file][0]['datetime']  # First date listen in the chosen file
        # Find which option the user picked
        if user_choice.lower() == 'da':  # Daily Average
            output = reporting.daily_average(data, chosen_file, pollutant)
            display_data(output, pollutant, get_daily_dates(start_date))

        elif user_choice.lower() == 'dm':  # Daily Median
            output = reporting.daily_median(data, chosen_file, pollutant)
            display_data(output, pollutant, get_daily_dates(start_date))

        elif user_choice.lower() == 'ha':  # Hourly Average
            output = reporting.hourly_average(data, chosen_file, pollutant)
            display_data(output, pollutant, get_hourly_times())

        elif user_choice.lower() == 'ma':  # Monthly Average
            output = reporting.monthly_average(data, chosen_file, pollutant)
            display_data(output, pollutant, get_monthly_dates(start_date))

        elif user_choice.lower() == 'ph':  # Peak Hour
            date = get_date()  # Get the date the user wants to find peak hour for
            output = reporting.peak_hour_date(data, date, chosen_file, pollutant)
            # Display data
            menu_options = f"Peak hour: {output[0]}, Peak Value: {output[1]}\n" \
                           f"• Anykey - Return to reporting menu"
            valid_options_regex = ".*"
            get_valid_user_input(menu_options, valid_options_regex)

        elif user_choice.lower() == 'c':  # Count Missing Data
            output = reporting.count_missing_data(data, chosen_file, pollutant)
            # Display data
            menu_options = f"Number of 'No data' entries: {output}\n" \
                           f"• Anykey - Return to reporting menu"
            valid_options_regex = ".*"
            get_valid_user_input(menu_options, valid_options_regex)

        elif user_choice.lower() == 'f':  # Fill Missing Data
            # Get the new value that should replace 'No data' entries
            new_value = get_valid_user_input(Menu.NewValue.options, Menu.NewValue.regex)
            output = reporting.fill_missing_data(data, new_value, chosen_file, pollutant)
            # Get the name of the file the user wishes to save the updated data to
            file_name = get_valid_user_input(Menu.File.options, Menu.File.regex)
            # Borrow the save function from the monitoring module to save the new data
            monitoring.save(output[chosen_file], file_name)


def monitoring_menu():
    """
    ---------------
    Description
    ---------------
    Lists the available options for the monitoring module and gets the user input to perform the requested operation

    ----------------------
    Options
    ----------------------
    • G - List groups
    • S - List stations in a group
    • P - Get information about the different pollutants
    • N - Get news information
    • D - Get data from a station
    • B - Return to main menu"

    :return: None
    """

    while True:
        # List options and get user input
        user_choice = get_valid_user_input(Menu.Monitoring.options, Menu.Monitoring.regex)

        if user_choice.lower() == 'g':  # List all the groups available
            valid_options_regex = ".*"
            table = monitoring.get_groups()
            table += "• Anykey - Return to main menu"
            get_valid_user_input(table, valid_options_regex)

        elif user_choice.lower() == 's':  # List all the stations within a group
            group = get_valid_user_input(Menu.Group.options, Menu.Group.regex)
            table = monitoring.get_monitoring_sites(group)
            table += "• Anykey - Return to main menu"
            get_valid_user_input(table, valid_options_regex)

        elif user_choice.lower() == 'n':  # List news and options for displaying more
            skip = 1
            while True:
                table = monitoring.get_news(skip, 20)
                table += "• N - Next news items\n" \
                         "• P - Previous news items\n" \
                         "• B - Back to monitoring menu"
                valid_options_regex = "[npbNPB]"
                choice = get_valid_user_input(table, valid_options_regex)
                if choice.lower() == 'n':  # Next set of news
                    skip += 21

                elif choice.lower() == 'p':  # Previous set of news
                    skip -= 21
                    skip = skip if skip > 0 else 1

                elif choice.lower() == 'b':  # Back
                    break

        elif user_choice.lower() == 'd':  # Get data from a station
            station_code = get_valid_user_input(Menu.Station.options, Menu.Station.regex)
            # Get start and end dates for getting the data
            start = get_date()
            end = get_date()
            # Make sure the start date is not after the end date
            while start > end:
                print('Start date was before end date...\n Reenter dates')
                time.sleep(2)
                start = get_date()
                end = get_date()

            # Get data
            output_data = monitoring.get_current_data(start.date(), end.date(), station_code.upper())

            # Give options for how the user wishes to see the data
            display_type = get_valid_user_input(Menu.DisplaySave.options, Menu.DisplaySave.regex)

            if display_type.lower() == 't':  # Display table
                # Convert datetime objects into strings
                for row in output_data:
                    row['datetime'] = str(row['datetime'])
                # Make headings
                headings = [('Date and Time', 'datetime'), ('NO', 'no'), ('PM10', 'pm10'), ('PM25', 'pm25')]
                # Make and display table
                table = monitoring.make_table(output_data, headings)
                table += "• Anykey - Return to main menu"
                valid_options_regex = ".*"
                get_valid_user_input(table, valid_options_regex)

            elif display_type.lower() == 'g':  # Display graph
                pollutant = get_pollutant()  # Get the pollutant to show graph for
                # Make and display graph
                graph = monitoring.make_graph(output_data, pollutant)
                graph += "\n• Anykey - Return to main menu"
                valid_options_regex = ".*"
                get_valid_user_input(graph, valid_options_regex)

            elif display_type == 's':  # Save data
                # Get name of file to save data under
                file_name = get_valid_user_input(Menu.File.options, Menu.File.regex)
                monitoring.save(output_data, file_name)  # Save data

        elif user_choice.lower() == 'p':  # Get info on different pollutants
            valid_options_regex = ".*"
            # Display in table form
            table = monitoring.get_species_info()
            table += "• Anykey - Return to main menu"
            get_valid_user_input(table, valid_options_regex)

        elif user_choice.lower() == 'b':  # Back
            break


def intelligence_menu():
    """
    ---------------
    Description
    ---------------
    Lists the available options for the intelligence module and gets the user input to perform the requested operation

    ----------------------
    Options
    ----------------------
    • FR - Filter red pixels
    • FC - Filter cyan pixels
    • CC - Find connected components
    • SCC - Find connected components sorted
    • B - Return to main menu
    :return: None
    """
    while True:
        # Finds all the files in the data directory
        file_names = os.listdir("data")
        # Regex to find files that end with .png
        csv_regex = re.compile('.*\\.png')
        # Gets names of all the png files in the directory
        png_file_names = list(filter(csv_regex.match, file_names))

        # List options and get user input
        user_choice = get_valid_user_input(Menu.Intelligence.options, Menu.Intelligence.regex)

        # If the user has not chosen to return to the main menu get the map the user wishes to use
        if user_choice.lower() != 'b':
            file_name = get_file(png_file_names)
        else:
            break

        if user_choice.lower() == 'fr':  # Filter red pixels
            intelligence.find_red_pixels(file_name, upper_threshold=100, lower_threshold=50)

        elif user_choice.lower() == 'fc':  # Filter cyan pixels
            intelligence.find_cyan_pixels(file_name, upper_threshold=100, lower_threshold=50)

        elif user_choice.lower() == 'cc':  # Find connected components
            # Find the type of pixel the user wishes to find connected components for
            filter_choice = get_valid_user_input(Menu.Filter.options, Menu.Filter.regex)
            if filter_choice.lower() == 'fr':
                filtered = intelligence.find_red_pixels(file_name, upper_threshold=100, lower_threshold=50)

            else:
                filtered = intelligence.find_cyan_pixels(file_name, upper_threshold=100, lower_threshold=50)

            intelligence.detect_connected_components(filtered)

        elif user_choice.lower() == 'scc':  # Find connected components sorted
            # Find the type of pixel the user wishes to find connected components for
            filter_choice = get_valid_user_input(Menu.Filter.options, Menu.Filter.regex)

            if filter_choice.lower() == 'fr':
                filtered = intelligence.find_red_pixels(file_name, upper_threshold=100, lower_threshold=50)

            else:
                filtered = intelligence.find_cyan_pixels(file_name, upper_threshold=100, lower_threshold=50)

            mark = intelligence.detect_connected_components(filtered)
            intelligence.detect_connected_components_sorted(mark)


def about():
    """
    ---------------
    Description
    ---------------
    Prints the course module code and my candidate number

    :return: None
    """
    # List the about information and get user input to return to main menu
    get_valid_user_input(Menu.About.options, Menu.About.regex)


def quit():
    """
    ---------------
    Description
    ---------------
    Stops the execution of the program

    :return: None
    """

    sys.exit("Program has quit")


if __name__ == '__main__':
    main_menu()
