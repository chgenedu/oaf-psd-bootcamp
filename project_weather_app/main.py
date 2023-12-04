from database import WeatherDatabase
from data_handler import DataHandler
from data_service import DataServiceFactory
from location import Location

MODE = "API" # data retrieval mode: ["API"|"MOCK"]
LONGITUDE = -122.431297 # "longitude": -122.431297,
LATITUDE = 37.773972    # "latitude": 37.773972,

DATA_SOURCE = "config.json" # config file for data service
API_DB_FILE = "weather_api.db" # database file location
MOCKED_DB_FILE = "weather_mocked.db" 

def main():
    print("Begin program.")

    # select database file based on the mode
    if MODE.upper() == "API":
        print("Database: ", API_DB_FILE)
        db_file = API_DB_FILE
    elif MODE.upper() == "MOCK":
        print("Database: ", MOCKED_DB_FILE)
        db_file = MOCKED_DB_FILE
    else:
        raise("invalid mode")

    # create database to store weather data
    db = WeatherDatabase(db_file)

    # setup the data_service and data_handler
    data_service = DataServiceFactory(DATA_SOURCE, database=db, mode=MODE).create()    
    data_handler = DataHandler(data_service)

    # handle the data for the given location
    location = Location(longitude=LONGITUDE, latitude=LATITUDE)
    data_handler.execute(location)

    print("Program finished.")

if __name__ == "__main__":
    main()
