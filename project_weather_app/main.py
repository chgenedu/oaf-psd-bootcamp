"""
This is a project that receives weather data from a weather data service API
and processes the data.
"""
from database import WeatherDatabase
from data_handler import DataHandler
from data_service import DataServiceFactory
from location import Location
from sys import exit
import exception as e
from util import log_setup


MODE = "API" # data retrieval mode: ["API"|"MOCK"]

# Location: from API documtation page
# https://open-meteo.com/en/docs
LONGITUDE = 13.41
LATITUDE = 52.52
# # Location: San Francisco
# LONGITUDE = -122.431297 # "longitude": -122.431297,
# LATITUDE = 37.773972    # "latitude": 37.773972,

DATA_SOURCE = "config/config.json" # config file for data service
API_DB_FILE = "data/weather_api.db" # database file location
MOCKED_DB_FILE = "data/weather_mocked.db"
LOG_FILE = "log/weather_app.log"
LOGGER_NAME = "weather_app"

def main():
    logger = log_setup(LOG_FILE, LOGGER_NAME)
    logger.warning("Begin logging.")
    print("Begin program.")

    location = Location(longitude=LONGITUDE, latitude=LATITUDE)

    # select database file based on the mode
    if MODE.upper() == "API":
        print("Database: ", API_DB_FILE)
        db_file = API_DB_FILE
    elif MODE.upper() == "MOCK":
        print("Database: ", MOCKED_DB_FILE)
        db_file = MOCKED_DB_FILE
    else:
        raise e.ModeError("Mode error.", MODE,2)
    print("Mode: ", MODE)

    # create database to store weather data
    db = WeatherDatabase(db_file)

    ### Drop database table (for testing purpose)
    # db.drop()
    # exit(0)

    # setup the data_service and data_handler
    data_service = DataServiceFactory(DATA_SOURCE, database=db, mode=MODE).create()    
    data_handler = DataHandler(data_service)

    # handle the data for the given location
    data_handler.execute(location)

    print("Program finished.")
    exit(0)

if __name__ == "__main__":
    main()
