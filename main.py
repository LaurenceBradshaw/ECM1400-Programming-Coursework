# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
import time
import reporting
import monitoring
import intelligence
import re
import os
import sys


def clear():
    """
    Clears the text in the console

    :return: None
    """
    os.system('cls')


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
        user_choice = input("Select Option: ")
        # Check the user input against the provided regex
        re_match = re.fullmatch(regex, user_choice)
        # If a match is not found - invalid input
        if re_match is None:
            print("Invalid Menu Input.")
            time.sleep(2)
            clear()
        # else a match is found - valid input
        else:
            return user_choice


def read_file(file_name: str) -> list:
    data = []
    with open("data/{}.csv".format(file_name)) as f:
        for line in f:
            data.append(line[:-1])

    return data


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

    clear()
    # Define the regex that will be used to check if the users input to the menu is a valid choice
    valid_options_regex = '[rimaqRIMAQ]'
    # Define the menu string to print
    menu_options = "• R - Access the Pollution Reporting module\n• I - Access the Mobility Intelligence module\n• M - Access the Real-time Monitoring module\n• A - Print the About text\n• Q - Quit the application"
    # while loop is used so the user can come back to the main menu and the program not close until they pick quit
    while True:
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
        else:
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
    • B - Return to main menu\n
    :return: None
    """

    clear()
    # Load all data
    harlington_data = read_file("Pollution-London Harlington")
    marylebone_data = read_file("Pollution-London Marylebone Road")
    kensington_data = read_file("Pollution-London N Kensington")
    # List options and get user input
    valid_options_regex = '[dD][mM]|[dhDHmM][aA]|[cfbCFB]'
    menu_options = "• DA - Calculate the daily average\n• DM - Calculate the daily median\n• HA - Calculate the hourly average\n• MA - Calculate the monthly average\n• C - Count the number of rows with missing data\n• F - Fill missing data rows\n• B - Return to main menu\n"
    user_choice = get_valid_user_input(menu_options, valid_options_regex)
    # Implement options
    if user_choice.lower() == 'da':
        reporting_menu()
    elif user_choice.lower() == 'dm':
        intelligence_menu()
    elif user_choice.lower() == 'ha':
        monitoring_menu()
    elif user_choice.lower() == 'ma':
        about()
    elif user_choice.lower() == 'c':
        about()
    elif user_choice.lower() == 'f':
        about()


def monitoring_menu():
    """
    Lists the available options for the monitoring module and gets the user input to perform the requested operation
    :return: None
    """

    # Your code goes here


def intelligence_menu():
    """
    Lists the available options for the intelligence module and gets the user input to perform the requested operation
    :return:
    """

    # Your code goes here


def about():
    """
    Prints the course module code and my candidate number
    :return: None
    """

    print("Module Code: ECM1400\nCandidate Number: 720004138")


def quit():
    """
    Stops the execution of the program
    :return: None
    """

    sys.exit("Program has quit")


if __name__ == '__main__':
    main_menu()

# Questions:
# Does altering the parameters for a function mess up the automated test?
# How do I know what format the automated test will input data to the function? For example, the data parameter on the daily_average function, is data expected to be a list or a dictionary or something else?
# How do I know what format to output data from functions so it is marked correctly?

