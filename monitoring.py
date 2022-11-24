# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification.
# 
# This module will access data from the LondonAir Application Programming Interface (API)
# The API provides access to data to monitoring stations. 
# 
# You can access the API documentation here http://api.erg.ic.ac.uk/AirQuality/help
#
import requests
import datetime


def make_api_call(url: str):
    """
    Takes the last part of the url to make the API call

    :param url: Remaining part of the url
    :return: Response from API
    """
    url = f"http://api.erg.ic.ac.uk/AirQuality/{url}"
    res = requests.get(url)
    return res.json()


def spaces_needed(max, col_max, current):
    """
    Calculates the correct number of spaces for the data in the row

    :param max: Length of the largest element in the column
    :param col_max: Max valid length of the row
    :param current: Current element in the row
    :return: The number of spaces to make the row line up
    """

    # If the largest element in the column is less that the max length a column can be
    if max < col_max:
        spaces = max - len(current)
        return spaces if spaces >= 0 else 0
    else:
        spaces = col_max - len(current)
        return spaces if spaces >= 0 else 0


def make_table(data: dict, column_info: list, wrap: int = 200) -> str:
    """
    Will make a string to print that will be a table of the input data
    Wraps data onto a new line when the line is longer than the max row length

    :param wrap: Max length of a column before text wraps
    :param data: Data to make table from
    :param column_info: List of tuples containing (Heading name, Dictionary key)
    :return: A string containing the table
    """

    # Remove keys from data that will not be displayed
    valid_keys = []
    for element in column_info:
        valid_keys.append(element[1])
    for site in data:
        for key in list(site.keys()):
            if key not in valid_keys:
                del site[key]

    # Finds the max length of elements in that column
    col_max = {}
    for heading_name, dict_key in column_info:
        curr_longest = len(heading_name)  # Current longest starts with the heading
        # For each site, if the data in the specified field is longer than the current longest, make it the current longest
        for element in data:
            if len(element[dict_key]) > curr_longest:
                curr_longest = len(element[dict_key])

        col_max[dict_key] = curr_longest

    table_string = ""
    # Creates the headings for the table
    for heading_name, dict_key in column_info:
        table_string += f"{heading_name}{' ' * spaces_needed(wrap, col_max[dict_key], heading_name)} | "

    # Puts a row of '-' after the heading row
    table_string += f"\n {'-' * len(table_string)}"

    # For each site in the data, append the correct row data to the table string
    table_string += "\n"
    for element in data:

        # While that element had data left to be displayed
        while any(value != '' for value in element.values()):
            for heading_name, dict_key in column_info:
                if len(element[dict_key]) > wrap:  # There is too much data to display on one line
                    data_for_row = []
                    data_split = element[dict_key].split(' ')
                    # Add segments to data_for_row until it becomes longer than the max length allowed for a row
                    for segments in data_split.copy():
                        if len(' '.join(data_for_row)) > wrap:  # Got enough data for one row
                            # Remove the last segment because it made the string too long
                            data_for_row.pop(-1)
                            # Replace the data with the remaining data
                            element[dict_key] = ' '.join(data_split)
                            break
                        else:
                            # Add data to the list for the row and remove it from the list
                            data_for_row.append(segments)
                            data_split.remove(segments)
                    # Add data that will fit for that row
                    table_string += f"{' '.join(data_for_row)}{' ' * spaces_needed(wrap, col_max[dict_key], ' '.join(data_for_row))} | "
                else:
                    table_string += f"{element[dict_key]}{' ' * spaces_needed(wrap, col_max[dict_key], element[dict_key])} | "
                    element[dict_key] = ''
            table_string += "\n"

    return table_string


def add_row(element, dict_key, wrap, col_max):
    """
    WIP
    :param element:
    :param dict_key:
    :param wrap:
    :param col_max:
    :return:
    """
    data_for_row = []
    data_split = element[dict_key].split(' ')
    # Add segments to data_for_row until it becomes longer than the max length allowed for a row
    for segments in data_split.copy():
        if len(' '.join(data_for_row)) > wrap:  # Got enough data for one row
            # Remove the last segment because it made the string too long
            data_for_row.pop(-1)
            # Replace the data with the remaining data
            element[dict_key] = ' '.join(data_split)
            break
        else:
            # Add data to the list for the row and remove it from the list
            data_for_row.append(segments)
            data_split.remove(segments)
    # Add data that will fit for that row
    return f"{' '.join(data_for_row)}{' ' * spaces_needed(wrap, col_max[dict_key], ' '.join(data_for_row))} | "


def get_monitoring_sites(group: str) -> str:
    """
    Gets the names, site code, lat, long, open date and close date for all of the sites in a group
    :param group: Name of the group to get the site info for
    :return: String to print containing the data in a table
    """

    res = make_api_call(f"Information/MonitoringSites/GroupName={group}/Json")
    data = res['Sites']['Site']
    column_info = [("Site Name", "@SiteName"), ("Site Code", "@SiteCode"), ("Longitude", "@Longitude"), ("Latitude", "@Latitude"), ("Opened", "@DateOpened"), ("Closed", "@DateClosed")]
    table = make_table(data, column_info)
    return table


def get_groups() -> str:
    """
    Gets the names and description for all of the groups that contain sites
    :return: String to print containing the data in a table
    """

    res = make_api_call("/Information/Groups/Json")
    data = res['Groups']['Group']
    column_info = [("Group Name", "@GroupName"), ("Description", "@Description"), ("URL", "@WebsiteURL")]
    table = make_table(data, column_info, 80)
    return table


def get_current_data(start_date: datetime.date, end_date: datetime.date, site_code: str) -> list[dict]:
    """
    Gets data from the specified site between the given dates

    :param start_date: Date to start getting data for
    :param end_date: Date to stop getting data for
    :param site_code: Site to get data from
    :return: List of dictionaries containing the data
    """

    # Get data for the three pollutant types between the given dates for the given site
    res_no = make_api_call(f"/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode=NO/StartDate={start_date}/EndDate={end_date}/Json")['RawAQData']['Data']
    # Rename @value key to @no and delete the @value key
    for entry in res_no:
        entry['@no'] = entry['@Value']
        del entry['@Value']
        if entry['@no'] == '':
            entry['@no'] = 'No data'
    res_pm10 = make_api_call(f"/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode=PM10/StartDate={start_date}/EndDate={end_date}/Json")['RawAQData']['Data']
    for entry in res_pm10:
        entry['@pm10'] = entry['@Value']
        del entry['@Value']
        if entry['@pm10'] == '':
            entry['@pm10'] = 'No data'
    res_pm25 = make_api_call(f"/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode=PM25/StartDate={start_date}/EndDate={end_date}/Json")['RawAQData']['Data']
    for entry in res_pm25:
        entry['@pm25'] = entry['@Value']
        del entry['@Value']
        if entry['@pm25'] == '':
            entry['@pm25'] = 'No data'

    # Merge all the dictionaries into one
    data = []
    for i in range(len(res_no)):
        data.append(res_no[i] | res_pm10[i] | res_pm25[i])

    return data


def save(data: list[dict], file_name: str):
    """
    Takes input data in the format that the get_current_data will give and saves it to a .csv file
    so that it can be used in other parts of the AQUA System

    :param data: Data to save to csv
    :param file_name: Name to give csv
    :return: None
    """

    with open('data/' + file_name, "w") as f:
        # Write headings
        f.write("date,time,no,pm10,pm25\n")

        for element in data:
            line = ''
            date_and_time = element['@MeasurementDateGMT'].split(' ')
            line += date_and_time[0]  # Split the date into the date and time then write
            time = date_and_time[1].split(':')
            time[0] = str(int(time[0]) + 1)
            line += ',' + ':'.join(time)
            line += ',' + element['@no']
            line += ',' + element['@pm10']
            line += ',' + element['@pm25']
            f.write(line + '\n')


# save(get_current_data(datetime.date(year=2021, month=1, day=1), datetime.date(year=2022, month=1, day=1), "KC1"), 'test_save.csv')
# print(get_monitoring_sites("London"))
