"""
This is a project that receives weather data from a weather data service API
and processes the data.
"""
import argparse
import logging

# From this project:
from database import WeatherDatabase
from data_handler import DataHandler
from data_service import DataServiceFactory
from location import Location
import visualization_handler as vh
from util import logger_setup
import exception as e

MODE = "API" # data retrieval mode: ["API"|"MOCK"]

# This is the default location for weather data retrieval and visualization.
# Location: from API documtation page: https://open-meteo.com/en/docs
LONGITUDE = 13.41
LATITUDE = 52.52

# # Location: San Francisco
# LONGITUDE = -122.431297 # "longitude": -122.431297,
# LATITUDE = 37.773972    # "latitude": 37.773972,

# Logging level
LOG_LEVEL = logging.INFO

# File locations:
DATA_SOURCE = "config/config.json" # config file for data service
API_DB_FILE = "data/weather_api.db" # database file location
MOCKED_DB_FILE = "data/weather_mocked.db"
LOG_FILE = "log/weather_app.log"

def main():
    logger = logging.getLogger() # create the root logger
    logger = logger_setup(logger, LOG_FILE, level=LOG_LEVEL)
    logger.info("Begin program. ---------------------------------")

    # setup the parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", help="program mode: API or MOCK")
    parser.add_argument("--reset", action="store_true", 
                        help="Reset the database by deleting all records before downloading data.")
    args = parser.parse_args()
    if args.mode:
        mode = args.mode
        logger.info("Using command line mode: " + str(mode))
    else:
        mode = MODE
        logger.info("No mode given on command line. Using default mode: " + str(mode))

    # select database file based on the mode
    if mode.upper() == "API":
        logger.info("Database: " + str(API_DB_FILE))
        db_file = API_DB_FILE
    elif mode.upper() == "MOCK":
        logger.info("Database: " + str(MOCKED_DB_FILE))
        db_file = MOCKED_DB_FILE
    else:
        raise e.ModeError("Mode error.", mode)

    # create database object for accessing the stored weather data
    db = WeatherDatabase(db_file)
    if args.reset:
        logger.info("reset the database....")
        db.reset()

    # setup the data_service and data_handler
    data_service = DataServiceFactory(DATA_SOURCE, database=db, mode=mode).create()    
    data_handler = DataHandler(data_service, vh.VisualizationHandler())

    # handle the data for the given location
    location = Location(longitude=LONGITUDE, latitude=LATITUDE)
    data_handler.execute(location)

    # print("Program finished.")
    logger.info("Program finished.")

if __name__ == "__main__":
    main()
