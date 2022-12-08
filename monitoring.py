# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification.
# 
# This module will access data from the LondonAir Application Programming Interface (API)
# The API provides access to data to monitoring stations. 
# 
# You can access the API documentation here http://api.erg.ic.ac.uk/AirQuality/help
#
import csv
import requests
import datetime
import math
import utils

# -------------------------
# Data presentation functions
# -------------------------


def add_row(element: dict, column_info: list, wrap: int, col_max: dict) -> str:
    """
    ---------------
    Description
    ---------------
    Adds a row for a given bit of data
    Data that is longer than wrap will wrap onto the next line

    ---------------
    General Overview
    ---------------
    While there is still data to display for this row
    Find the amount of data that will fit on this row
    Append it to the row
    Remove the appended data from the data left to display on this row

    ---------------
    WARNING
    ---------------
    If the data contains an element that, when split by spaces, is longer than wrap, an infinite loop will be encountered
    Thus an exception will be raised

    :param element: Dictionary containing all data to display on this row
    :param column_info: List of column headings and dict keys associated with them
    :param wrap: Max length a line in row can be before the data will be wrapped onto the next line
    :param col_max: Length of longest element in each column
    :return: Row to append to table
    """
    row = ''
    # While that element had data left to be displayed
    while any(value != '' for value in element.values()):
        # For each column
        for heading_name, dict_key in column_info:
            data_for_row = []
            data_split = element[dict_key].split(' ')  # Split the data for this column up by spaces
            # Add segments to data_for_row until it becomes longer than the max length allowed for a row or all data has been used
            for segments in data_split.copy():
                if len(segments) > wrap:
                    raise Exception()
                data_for_row.append(segments)
                length_joined = len(' '.join(data_for_row))
                if length_joined > wrap:  # Got enough data for one row
                    # Remove the last segment because it made the string too long
                    data_for_row.pop(-1)
                    # Replace the data with the remaining data
                    element[dict_key] = ' '.join(data_split)
                    break
                else:
                    # Add data to the list for the row and remove it from the list
                    data_split.remove(segments)

            if len(data_split) == 0:  # When there is no remaining data for this column set the data in the dict to ''
                element[dict_key] = ''

            # Add data that will fit for that row
            if col_max[dict_key] > wrap:
                row += f"{' '.join(data_for_row):<{wrap}} | "
            else:
                row += f"{' '.join(data_for_row):<{col_max[dict_key]}} | "
        row += '\n'

    return row


def make_table(data: list[dict], column_info: list[tuple], wrap: int = 200) -> str:
    """
    ---------------
    Description
    ---------------
    Will make a string to print that will be a table of the input data
    Wraps data onto a new line when the line is longer than the max row length

    ---------------
    General Overview
    ---------------
    Remove keys from the data that are not going to be displayed
    Find the length of the longest entry in each column
    Make headings
    Add rows to the table

    ---------------
    WARNING
    ---------------
    If an exception is raised by the add_row function, then the following string with be
    returned from this function:
    "A piece of data contained a segment that was longer than the wrap limit"

    :param wrap: Max length of a column before text wraps
    :param data: Data to make table from
    :param column_info: List of tuples containing (Heading name, Dictionary key)
    :return: A string containing the table
    """

    # Remove keys from data that will not be displayed
    valid_keys = []
    for element in column_info:
        valid_keys.append(element[1])
    for d in data:
        for key in list(d.keys()):
            if key not in valid_keys:
                del d[key]

    # Finds the length of longest elements in each column
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
        if col_max[dict_key] > wrap:
            table_string += f"{heading_name:<{wrap}} | "
        else:
            table_string += f"{heading_name:<{col_max[dict_key]}} | "

    # Puts a row of '-' after the heading row
    table_string += f"\n{'-' * (len(table_string) - 1)}"

    # For each element in the data, append the correct column data to the row in the table string
    table_string += "\n"
    try:
        for d in data:
            table_string += add_row(d, column_info, wrap, col_max)
    except Exception:
        return "A piece of data contained a segment that was longer than the wrap limit"

    return table_string


def save(data: list[dict], file_name: str):
    """
    ---------------
    Description
    ---------------
    Takes input data in the format that the get_current_data will give and saves it to a .csv file
    so that it can be used in other parts of the AQUA System

    ---------------
    General Overview
    ---------------
    Copy the data
    Remove the 'datetime' key
    Create the file
    Use csv dict writer to write headings and data

    :param data: Data to save to csv
    :param file_name: Name to give csv
    :return: None
    """

    data = data.copy()
    for d in data:
        del d['datetime']

    keys = ['date', 'time', 'no', 'pm10', 'pm25']

    with open("data/" + file_name + ".csv", 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def make_graph(data: list[dict], pollutant: str):
    """
    ---------------
    Description
    ---------------
    Takes input data and returns a graph to display in the console

    ---------------
    General Overview
    ---------------
    Find min and max y
    Divide the y range into suitable segments

    For each y segment
    Iterate over the data in date order and find the values that lie within the segment range y1 <= value < y2
    Add a character there to indicate a data point

    :param pollutant: Name of the pollutant to plot a graph for
    :param data: Data from containing the data to plot
    :return: A string to print a graph
    """

    values = []
    for d in data:
        values.append(d[pollutant])

    # Get the values of the input pollutant and convert them to floats
    values_for_min_max = values.copy()
    utils.remove_no_value(values_for_min_max)
    values_as_float = [float(value) for value in values_for_min_max]

    # Find the min and max values and find the range
    max_value_index = utils.maxvalue(values_as_float)
    min_value_index = utils.minvalue(values_as_float)
    max_value = math.ceil(values_as_float[max_value_index])
    min_value = math.floor(values_as_float[min_value_index])
    # Divide into 21 steps
    step = (max_value - min_value)/21

    # Replace 'No data' values with -1 since this shouldn't display on the graph
    values_without_no_data = []
    for value in values:
        if value == 'No data':
            values_without_no_data.append(-1)
        else:
            values_without_no_data.append(value)

    # Find the value with the longest length
    longest = 0
    values_for_min_max = [str(float(f'{current_value:.1f}')) for current_value in values_as_float]
    for value in values_for_min_max:
        if len(str(value)) > longest:
            longest = len(str(value))

    graph_string = ''
    current_value = max_value  # Current value is the value that is at the top of the current range for data to be displayed
    # For each line that will be in the graph
    for i in range(21):
        # Put a value label on every other line in the graph
        if i % 2 == 0:
            graph_string += f"{current_value:>{longest}.1f} +"
        else:
            graph_string += " " * longest + " |"

        # For each value in the data, if it is within the range to be displayed on this line, put a *
        for value in values_without_no_data:
            if (current_value - step) <= float(value):
                graph_string += "*"
            else:
                graph_string += " "

        graph_string += "\n"
        current_value -= step  # Change the bounds that wil be checked for the next line

    # Put a line at the bottom of the graph
    graph_string += ' ' * (longest + 1) + '+' + '-' * len(values)

    return graph_string


# -------------------------
# Data Retrieving Functions
# -------------------------


def make_api_call(endpoint: str):
    """
    ---------------
    Description
    ---------------
    Takes the last part of the url to make the API call

    ---------------
    General Overview
    ---------------
    Append the endpoint to form a url
    Make http request with the url
    Return the data

    :param endpoint: Remaining part of the url
    :return: Response from API
    """
    url = f"http://api.erg.ic.ac.uk/AirQuality/{endpoint}"
    res = requests.get(url)
    return res.json()


def get_monitoring_sites(group: str) -> str:
    """
    ---------------
    Description
    ---------------
    Gets the names, site code, lat, long, open date and close date for all of the sites in a group
    and returns a table string to display
    This information can be used to get realtime data from the get_current_data function

    ---------------
    General Overview
    ---------------
    Make an API call to retrieve the information about all the monitoring sites in the input group
    Turn the data into a table to be displayed

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
    ---------------
    Description
    ---------------
    Gets the names and description for all of the groups that contain sites
    This information can be used to see what sites are in a group

    ---------------
    General Overview
    ---------------
    Make an API call to get the information on all the different groups
    Turn the data into a table to be displayed

    :return: String to print containing the data in a table
    """

    res = make_api_call("Information/Groups/Json")
    data = res['Groups']['Group']
    column_info = [("Group Name", "@GroupName"), ("Description", "@Description"), ("URL", "@WebsiteURL")]
    table = make_table(data, column_info, 80)
    return table


def get_current_data(start_date: datetime.date, end_date: datetime.date, site_code: str) -> list[dict]:
    """
    ---------------
    Description
    ---------------
    Gets data from the specified site between the given dates

    ---------------
    General Overview
    ---------------
    Make 3 API calls - One for each of the three pollutants the AQUA System deals with
    Rename the dictionary keys to ones used in the rest of the AQUA system
    Set empty values to 'No data'
    Merge the 3 dictionaries into one
    Turn into list of dicts in the correct format

    :param start_date: Date to start getting data for
    :param end_date: Date to stop getting data for
    :param site_code: Site to get data from
    :return: List of dicts containing the data for the three pollutants
    """

    # Get data for the three pollutant types between the given dates for the given site
    res_no = make_api_call(f"Data/SiteSpecies/SiteCode={site_code}/SpeciesCode=NO/StartDate={start_date}/EndDate={end_date}/Json")['RawAQData']['Data']
    # Rename @value key to 'no' and the @MeasurementDateGMT to 'datetime'
    for entry in res_no:
        entry['no'] = entry.pop('@Value')
        entry['datetime'] = entry.pop('@MeasurementDateGMT')
        if entry['no'] == '':
            entry['no'] = 'No data'

    res_pm10 = make_api_call(f"/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode=PM10/StartDate={start_date}/EndDate={end_date}/Json")['RawAQData']['Data']
    for entry in res_pm10:
        entry['pm10'] = entry.pop('@Value')
        entry['datetime'] = entry.pop('@MeasurementDateGMT')
        if entry['pm10'] == '':
            entry['pm10'] = 'No data'

    res_pm25 = make_api_call(f"/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode=PM25/StartDate={start_date}/EndDate={end_date}/Json")['RawAQData']['Data']
    for entry in res_pm25:
        entry['pm25'] = entry.pop('@Value')
        entry['datetime'] = entry.pop('@MeasurementDateGMT')
        if entry['pm25'] == '':
            entry['pm25'] = 'No data'

    # Merge all the dictionaries into one and reformat datetime
    data = []
    for i in range(len(res_no)):
        merged = res_no[i] | res_pm10[i] | res_pm25[i]
        merged['datetime'] = datetime.datetime.fromisoformat(merged['datetime'])
        merged['date'] = str(merged['datetime'].date())
        merged['time'] = str((merged['datetime'] + datetime.timedelta(hours=1)).time()) if str(merged['datetime'].time()) != '23:00:00' else '24:00:00'
        data.append(merged)

    return data


def get_species_info():
    """
    ---------------
    Description
    ---------------
    Gets information about all the species

    ---------------
    General Overview
    ---------------
    Make API call to get the data
    Make headings
    Make and return table containing data

    :return: Table string to print
    """

    data = make_api_call("Information/Species/Json")['AirQualitySpecies']['Species']
    headings = [('Species Name', '@SpeciesName'), ('Species Code', '@SpeciesCode'), ('Description', '@Description'), ('Health Effect', '@HealthEffect')]
    table = make_table(data, headings, 80)
    return table


def get_news(skip: int, limit: int):
    """
    ---------------
    Description
    ---------------
    Gets news from the API

    ---------------
    General Overview
    ---------------
    Make API call
    Create URL with @NewsId
    Create headings for table
    Make table

    :param skip: How many news articles to skip from start
    :param limit: Number of articles to return
    :return: Table to print
    """

    data = make_api_call(f"Information/News/Skip={skip}/limit={limit}/Json")['News']['NewsItem']

    for item in data:
        item['@url'] = f"https://www.londonair.org.uk/london/asp/news.asp?NewsId={item['@NewsId']}"

    headings = [('News Title', '@NewsTitle'), ('URL', '@url')]
    table = make_table(data, headings, 100)

    return table
