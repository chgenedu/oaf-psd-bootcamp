"""
The DataService object directs the WeatherDatabase object to interact with the database.
"""
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import datetime
import requests

from location import Location
from database import WeatherDatabase
import exception as e
import read_config as rc

import logging
logger = logging.getLogger(__name__)

# interface for DataService
class IDataService(ABC):
    @abstractmethod
    def __init__(self, data_source: str, database: WeatherDatabase):
        pass

    @abstractmethod
    def download_data(self, location: Location):
        pass
    
    @abstractmethod
    def get_data_from_db(self, location: Location):
        pass
    
    @abstractmethod
    def print_status(self):
        pass

class DataServiceFromAPI(IDataService):
    def __init__(self, data_source: str, database: WeatherDatabase):
        """
        Create the data service for accessing weather data API.
        """
        self._url, self._payload = rc.get_config(data_source)
        self._database = database

    def download_data(self, location: Location):
        """
        Download data from online weather API.
        """
        self._location = location
        self._payload["longitude"] = location.get_longitude()
        self._payload["latitude"] = location.get_latitude()
        try:
            r = requests.get(self._url, params=self._payload)
        except Exception as err:
            logger.critical("Error: Cannot get data with API.")
            logger.critical("Exception: " + str(err))
        else:
            if r.status_code != 200:
                logging.critical("Critical error: api code: " + str(r.status_code))
                raise e.DataServiceError("Critical exception error.")
            data = r.json().get("hourly", {})
            df = pd.DataFrame(data)
            for index, row in df.iterrows():
                self._database.insert_single_record(self._location, row["time"],
                                             row["precipitation_probability"],
                                             row["precipitation"],
                                             row["wind_speed_10m"])
        # in either case, save the status_code from "try" section
        self.status_code = r.status_code

    def get_data_from_db(self, location: Location):
        """
        Get weather data for a given location from the database.
        """
        return self._database.get_location_record(location)

    def print_status(self):
        """
        Print the status code from API access.
        """
        logger.info("API status code: " + str(self.status_code))

# Mocked data service
class DataServiceMocked(IDataService):
    def __init__(self, data_source: str, database: WeatherDatabase):
        """
        Create data service for a mocked data set.
        """
        super().__init__(data_source, database)
        self.status_code = "init"
        self._database = database

    def download_data(self, location: Location):
        """
        Generate n data points for a mocked data service 
        where data is randomly generated as normal distribution 
        with mean mu and standard deviation sd.
        """
        n: int = 168 # 24 hours * 7 days = 168 hours
        mu: float = 65
        sd: float = 5
        now = datetime.datetime.now()
        time_delta = datetime.timedelta(hours=n)
        t = now - time_delta
        self.time_list = [(t+datetime.timedelta(hours=i)).isoformat(timespec="minutes") for i in range(n) ]
        self.precipitation_probability_list = \
            [round(np.random.randn()*sd, 1) + mu for _ in range(n)]
        self.precipitation_list = [round(np.random.randn()*sd, 1) + mu for _ in range(n)]    
        self.wind_speed_10m_list = [round(np.random.randn()*sd, 1) + mu for _ in range(n)]    
        for time, precip_prob, precip, wind in zip(
                                    self.time_list, 
                                    self.precipitation_probability_list,
                                    self.precipitation_list,
                                    self.wind_speed_10m_list):
            self._database.insert_single_record(location, time, precip_prob, precip, wind)
        self.status_code = "OK"

    def get_data_from_db(self, location: Location):
        return self._database.get_location_record(location)
    
    def print_status(self):
        logger.info("Mocked service status code: " + str(self.status_code))


class DataServiceFactory:
    def __init__(self, data_source: str, database: WeatherDatabase, mode: str = "API", ):
        """
        Instantiates the DataService.
        By default, getting the data service via API.
        """    
        self.data_source = data_source
        self.mode = mode.upper()
        self._database = database
    
    def create(self) -> IDataService:
        """
        Create the data service for the mode stored in the object.
        """
        if self.mode == "API":
            return DataServiceFromAPI(self.data_source, self._database)
        elif self.mode == "MOCK":
            return DataServiceMocked(self.data_source, self._database)
        else:
            raise e.ModeError("Mode error.", self.mode)
