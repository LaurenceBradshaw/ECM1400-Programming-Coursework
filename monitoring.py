# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification.
# 
# This module will access data from the LondonAir Application Programming Interface (API)
# The API provides access to data to monitoring stations. 
# 
# You can access the API documentation here http://api.erg.ic.ac.uk/AirQuality/help
#

def get_live_data_from_api(site_code='MY1', species_code='NO', start_date=None, end_date=None):
    """
    Return data from the LondonAir API using its AirQuality API. 
    
    *** This function is provided as an example of how to retrieve data from the API. ***
    It requires the `requests` library which needs to be installed. 
    In order to use this function you first have to install the `requests` library.
    This code is provided as-is. 
    """
    import requests
    import datetime
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


def rm_function_1(*args, **kwargs):
    """Your documentation goes here"""
    # Your code goes here


def rm_function_2(*args, **kwargs):
    """Your documentation goes here"""
    # Your code goes here


def rm_function_3(*args, **kwargs):
    """Your documentation goes here"""
    # Your code goes here


def rm_function_4(*args, **kwargs):
    """Your documentation goes here"""
    # Your code goes here
