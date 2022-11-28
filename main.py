# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
import datetime
import os
import re
import time
import reporting
import monitoring
import intelligence
import sys
import utils

# -------------------------
# My custom functions
# -------------------------
from utils import clear


def get_pollutant(module: str) -> str:
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

    valid_options_regex = '[nN][oO]|[pP][mM](10|25)'
    menu_options = f"----------AQUA System {module} Module-----------\n" \
                   "Select a pollutant:\n" \
                   "• NO - Nitric Oxide\n" \
                   "• PM10 - Particulate Matter 10\n" \
                   "• PM25 - Particulate Matter 2.5"
    pollutant = get_valid_user_input(menu_options, valid_options_regex)
    utils.clear()
    return pollutant.lower()


def get_file(files: list, module_str: str) -> str:
    """
    ---------------
    Description
    ---------------
    Lists files and gets the users input to select one

    :param files: List of files to display
    :param module_str: Text to display in the menu heading
    :return: File name of file selected
    """

    valid_options_regex = '[0-9]*'
    chosen_file = ''
    while True:
        menu_options = f"---------AQUA System {module_str} Module----------\n" \
                       "Select a file to use:"
        for i, file in enumerate(files):
            menu_options += f'\n[{i}] - {file}'
        file_index_chosen = get_valid_user_input(menu_options, valid_options_regex)
        try:
            chosen_file = files[int(file_index_chosen)]
            break
        except IndexError:
            utils.clear()

    utils.clear()
    return chosen_file


def get_date(module: str) -> datetime.datetime:
    """
    ---------------
    Description
    ---------------
    Gets the user to enter a date

    :return: the inputted date as a datetime object
    """

    while True:
        valid_date_regex = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
        menu_options = f"----------AQUA System {module} Module-----------\n" \
                       "Enter a date in the form YYYY-MM-DD:"

        user_choice = get_valid_user_input(menu_options, valid_date_regex)
        try:
            date = datetime.datetime.fromisoformat(user_choice)
            break
        except ValueError:
            utils.clear()

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
    Returns the times 01:00:00 to 24:00:00

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
    start_month = start_date.month
    for i in range(12):
        dates.append(str(datetime.date(start_date.year, start_month + i, start_date.day)))

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
    valid_options_regex = "[tgbTGB]"
    menu_options = "----------AQUA System Reporting Module-----------\n" \
                   "Select a way to display data:\n" \
                   "• T - Table\n" \
                   "• G - Graph\n" \
                   "• B - Return to reporting menu"
    display_type = get_valid_user_input(menu_options, valid_options_regex)
    utils.clear()

    display = "----------AQUA System Reporting Module-----------\n"

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
        user_choice = get_valid_user_input(menu_options, valid_options_regex)
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
        user_choice = get_valid_user_input(menu_options, valid_options_regex)
        utils.clear()

        # If the user has not chosen to return to the main menu get the file and pollutant that the user wishes to use
        if user_choice.lower() != 'b':
            chosen_file = get_file(csv_files, "Reporting")
            pollutant = get_pollutant('Reporting')
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
            date = get_date('Reporting')  # Get the date the user wants to find peak hour for
            output = reporting.peak_hour_date(data, date, chosen_file, pollutant)
            # Display data
            menu_options = f"----------AQUA System Reporting Module-----------\n" \
                           f"Peak hour: {output[0]}, Peak Value: {output[1]}\n" \
                           f"• Anykey - Return to reporting menu"
            valid_options_regex = ".*"
            get_valid_user_input(menu_options, valid_options_regex)

        elif user_choice.lower() == 'c':  # Count Missing Data
            output = reporting.count_missing_data(data, chosen_file, pollutant)
            # Display data
            menu_options = f"----------AQUA System Reporting Module-----------\n" \
                           f"Number of 'No data' entries: {output}\n" \
                           f"• Anykey - Return to reporting menu"
            valid_options_regex = ".*"
            get_valid_user_input(menu_options, valid_options_regex)

        elif user_choice.lower() == 'f':  # Fill Missing Data
            utils.clear()
            # Get the new value that should replace 'No data' entries
            menu_options = "----------AQUA System Reporting Module-----------\n" \
                           "Input new value:"
            valid_options_regex = "[0-9]+\\.[0-9]+"
            new_value = get_valid_user_input(menu_options, valid_options_regex)
            utils.clear()
            output = reporting.fill_missing_data(data, new_value, chosen_file, pollutant)
            # Get the name of the file the user wishes to save the updated data to
            menu_options = "----------AQUA System Reporting Module-----------\n" \
                           "Enter file name to save new data as:"
            valid_options_regex = "^[\\w\\-. ]+$"
            file_name = get_valid_user_input(menu_options, valid_options_regex)
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
    • D - Get data from a station
    • B - Return to main menu

    :return: None
    """

    while True:
        utils.clear()
        # List options and get user input
        valid_options_regex = '[gsdpbnGSDBPN]'
        menu_options = "----------AQUA System Monitoring Module----------\n" \
                       "Select an operation:\n" \
                       "• G - List groups\n" \
                       "• S - List stations in a group\n" \
                       "• P - Get information about the different pollutants\n" \
                       "• N - Get news information\n" \
                       "• D - Get data from a station\n" \
                       "• B - Return to main menu"
        user_choice = get_valid_user_input(menu_options, valid_options_regex)
        utils.clear()

        if user_choice.lower() == 'g':  # List all the groups available
            valid_options_regex = ".*"
            table = "----------AQUA System Monitoring Module----------\n"
            table += monitoring.get_groups()
            table += "• Anykey - Return to main menu"
            get_valid_user_input(table, valid_options_regex)

        elif user_choice.lower() == 's':  # List all the stations within a group
            valid_options_regex = ".*"
            menu_options = "----------AQUA System Monitoring Module----------\n" \
                           "Enter group to get stations for:"
            group = get_valid_user_input(menu_options, valid_options_regex)
            table = "----------AQUA System Monitoring Module----------\n"
            table += monitoring.get_monitoring_sites(group)
            table += "• Anykey - Return to main menu"
            get_valid_user_input(table, valid_options_regex)

        elif user_choice.lower() == 'n':  # List news and options for displaying more
            skip = 1
            while True:
                table = "----------AQUA System Monitoring Module----------\n"
                table += monitoring.get_news(skip, 20)
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
            valid_options_regex = ".*"
            menu_options = "----------AQUA System Monitoring Module----------\n" \
                           "Enter station code to get data for:"
            station_code = get_valid_user_input(menu_options, valid_options_regex)
            # Get start and end dates for getting the data
            start = get_date('Monitoring')
            end = get_date('Monitoring')
            # Make sure the start date is not after the end date
            while start > end:
                print('Start date was before end date...\n Reenter dates')
                time.sleep(2)
                start = get_date('Monitoring')
                end = get_date('Monitoring')

            # Get data
            output_data = monitoring.get_current_data(start.date(), end.date(), station_code.upper())

            # Give options for how the user wishes to see the data
            valid_options_regex = "[tgbsTGBS]"
            menu_options = "----------AQUA System Monitoring Module----------\n" \
                           "Select a way to display data:\n" \
                           "• T - Table\n" \
                           "• G - Graph\n" \
                           "• S - Save\n" \
                           "• B - Return to monitoring menu"
            display_type = get_valid_user_input(menu_options, valid_options_regex)

            if display_type.lower() == 't':  # Display table
                table = "----------AQUA System Monitoring Module----------\n"
                # Convert datetime objects into strings
                for row in output_data:
                    row['datetime'] = str(row['datetime'])
                # Make headings
                headings = [('Date and Time', 'datetime'), ('NO', 'no'), ('PM10', 'pm10'), ('PM25', 'pm25')]
                # Make and display table
                table += monitoring.make_table(output_data, headings)
                table += "• Anykey - Return to main menu"
                valid_options_regex = ".*"
                get_valid_user_input(table, valid_options_regex)

            elif display_type.lower() == 'g':  # Display graph
                pollutant = get_pollutant('Monitoring')  # Get the pollutant to show graph for
                # Make and display graph
                graph = "----------AQUA System Monitoring Module----------\n"
                graph += monitoring.make_graph(output_data, pollutant)
                graph += "\n• Anykey - Return to main menu"
                valid_options_regex = ".*"
                get_valid_user_input(graph, valid_options_regex)

            elif display_type == 's':  # Save data
                # Get name of file to save data under
                options = "----------AQUA System Monitoring Module----------\nEnter file name:"
                valid_options_regex = "^[\\w\\-. ]+$"
                file_name = get_valid_user_input(options, valid_options_regex)
                monitoring.save(output_data, file_name)  # Save data

        elif user_choice.lower() == 'p':  # Get info on different pollutants
            valid_options_regex = ".*"
            # Display in table form
            table = "----------AQUA System Monitoring Module----------\n"
            table += monitoring.get_species_info()
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
        user_choice = get_valid_user_input(menu_options, valid_options_regex)
        utils.clear()

        # If the user has not chosen to return to the main menu get the map the user wishes to use
        if user_choice.lower() != 'b':
            file_name = get_file(png_file_names, "Intelligence")
        else:
            break

        if user_choice.lower() == 'fr':  # Filter red pixels
            intelligence.find_red_pixels(file_name, upper_threshold=100, lower_threshold=50)

        elif user_choice.lower() == 'fc':  # Filter cyan pixels
            intelligence.find_cyan_pixels(file_name, upper_threshold=100, lower_threshold=50)

        elif user_choice.lower() == 'cc':  # Find connected components
            # Find the type of pixel the user wishes to find connected components for
            valid_options_regex = '[fF][rRcC]'
            menu_options = "---------AQUA System Intelligence Module---------\n" \
                           "Select types of pixel to find connected components for:\n" \
                           "• FR - Filter red pixels\n" \
                           "• FC - Filter cyan pixels"
            filter_choice = get_valid_user_input(menu_options, valid_options_regex)
            if filter_choice.lower() == 'fr':
                filtered = intelligence.find_red_pixels(file_name, upper_threshold=100, lower_threshold=50)

            else:
                filtered = intelligence.find_cyan_pixels(file_name, upper_threshold=100, lower_threshold=50)

            intelligence.detect_connected_components(filtered)

        elif user_choice.lower() == 'scc':  # Find connected components sorted
            # Find the type of pixel the user wishes to find connected components for
            valid_options_regex = '[fF][rRcC]'
            menu_options = "---------AQUA System Intelligence Module---------\n" \
                           "Select types of pixel to find connected components for:\n" \
                           "• FR - Filter red pixels\n" \
                           "• FC - Filter cyan pixels"
            filter_choice = get_valid_user_input(menu_options, valid_options_regex)

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
    # Clear the console of text
    utils.clear()

    # List the about information and get user input to return to main menu
    valid_options_regex = ".*"
    menu_options = "-------------------About AQUA--------------------\n" \
                   "Module Code: ECM1400\n" \
                   "Candidate Number: 239766\n" \
                   "• Anykey - Return to main menu"

    get_valid_user_input(menu_options, valid_options_regex)


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
