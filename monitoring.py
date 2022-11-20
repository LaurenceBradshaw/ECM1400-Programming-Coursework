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


def correct_spaces(data, field, length_of_current, heading):
    """
    Finds the longest piece of data in a column and will return the number of spaces needed to put after
    an entry so that the table all lines up

    :param data: Dictionary containing the data
    :param field: Field to find the spaces for
    :param length_of_current: Length of the current item
    :param heading: Heading at the top of the column
    :return: The number of spaces needed after an entry in the column
    """

    # Sets the first longest to the length of the column heading
    curr_longest = len(heading)
    # For each site, if the data in the specified field is longer than the current longest, make it the current longest
    for site in data:
        if len(site[field]) > curr_longest:
            curr_longest = len(site[field])

    # Number of spaces to add after the data will be the length of the longest minus the length of the current bit of data
    spaces = (curr_longest - length_of_current)
    return spaces if spaces >= 0 else 0


def make_table(data: dict, column_info: list) -> str:
    """
    Will make a string to print that will be a table of the input data

    :param data: Data to make table from
    :param column_info: List of tuples containing (Heading name, Dictionary key)
    :return: A string containing the table
    """

    table_string = ""
    # Creates the headings for the table
    for heading_name, dict_key in column_info:
        table_string += f"{heading_name}{' ' * correct_spaces(data, dict_key, len(heading_name), heading_name)} | "

    # Puts a row of '-' after the heading row
    table_string += f"\n {'-'*len(table_string)}"

    # For each site in the data, append the correct row data to the table string
    for site in data:
        table_string += "\n"
        for heading_name, dict_key in column_info:
            table_string += f"{site[dict_key]}{' ' * correct_spaces(data, dict_key, len(site[dict_key]), heading_name)} | "

    return table_string


def get_monitoring_sites():
    res = make_api_call("Information/MonitoringSites/GroupName=London/Json")
    data = res['Sites']['Site']
    column_info = [("Site Name", "@SiteName"), ("Site Code", "@SiteCode"), ("Longitude", "@Longitude"), ("Latitude", "@Latitude"), ("Opened", "@DateOpened"), ("Closed", "@DateClosed")]
    table = make_table(data, column_info)
    print(table)


def get_groups():
    res = make_api_call("/Information/Groups/Json")
    data = res['Groups']['Group']
    column_info = [("Group Name", "@GroupName"), ("Description", "@Description"), ("URL", "@WebsiteURL")]
    table = make_table(data, column_info)
    print(table)


def test():
    res = make_api_call(f"/Data/SiteSpecies/SiteCode=MY1/SpeciesCode=NO/StartDate={datetime.date.today()}/EndDate={datetime.date.today() + datetime.timedelta(days=1)}/Json")
    # res = make_api_call("/Information/Species/Json")
    # res = make_api_call(f"/Data/Site/SiteCode=MY1/StartDate={datetime.date.today()}/EndDate={datetime.date.today() + datetime.timedelta(days=1)}/Json")
    print()


def get_live_data_from_api(site_code='MY1', species_code='NO', start_date=None, end_date=None):
    """
    Return data from the LondonAir API using its AirQuality API. 
    
    *** This function is provided as an example of how to retrieve data from the API. ***
    It requires the `requests` library which needs to be installed. 
    In order to use this function you first have to install the `requests` library.
    This code is provided as-is. 
    """
    start_date = datetime.date.today() if start_date is None else start_date
    end_date = start_date + datetime.timedelta(days=1) if end_date is None else end_date

    # /Data/SiteSpecies/SiteCode={SiteCode}/SpeciesCode={SpeciesCode}/StartDate={StartDate}/EndDate={EndDate}/Period={Period}/Units={Units}/Step={Step}/Json
    # This returns raw data based on 'SiteCode', 'SpeciesCode', 'StartDate', 'EndDate'. Default time period is 'hourly'. Data returned in JSON format
    # endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
    #
    # url = endpoint.format(
    #     site_code=site_code,
    #     species_code=species_code,
    #     start_date=start_date,
    #     end_date=end_date
    # )

    # endpoint = "http://api.erg.ic.ac.uk/AirQuality/Information/News/Skip={SKIP}/limit={LIMIT}/Json"
    # url = endpoint.format(
    #     SKIP=1,
    #     LIMIT=5
    # )
    url = "http://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName={GroupName}/Json"
    url = url.format(GroupName="London")

    res = requests.get(url)
    return res.json()


get_groups()
