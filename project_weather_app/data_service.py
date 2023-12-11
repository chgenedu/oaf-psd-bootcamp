from abc import ABC, abstractmethod
from database import WeatherDatabase
from location import Location

import requests
import read_config as rc
import numpy as np
import datetime

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
    def print_data(self, location: Location):
        pass
    
    @abstractmethod
    def print_status(self):
        pass

class DataServiceFromAPI(IDataService):
    def __init__(self, data_source: str, database: WeatherDatabase):
        self._url, self._payload = rc.get_config(data_source)
        self._database = database

    def download_data(self, location: Location):
        self._location = location
        self._payload["longitude"] = location.get_longitude()
        self._payload["latitude"] = location.get_latitude()
        try:
            r = requests.get(self._url, params=self._payload)
        except Exception:
            print("Error: Cannot get data with API.")
            self.time_list = []
            self.temp_list = []
        else:
            data = r.json().get("hourly", {})
            self.time_list = data["time"]
            self.temp_list = data[self._payload["hourly"]]
            for time, temp in zip(self.time_list, self.temp_list):
                self._database.insert_data(location, time, temp)
        # in either case, save the status_code
        self.status_code = r.status_code

    def get_data_from_db(self, location: Location):
        return self._database.get_time_temp(location)

    def print_data(self, location: Location):
        data = self._database.get_time_temp(location)
        for time, temperature in data:
            print(time, temperature)

    def print_status(self):
        print("API status code: ", self.status_code)        

# Mocked data service
class DataServiceMocked(IDataService):
    def __init__(self, data_source: str, database: WeatherDatabase):
        super().__init__(data_source, database)
        self.status_code = "init"
        self._database = database

    def download_data(self, location: Location):
        """
        prints n data points for mocked data service 
        where temperature is randomly generated as normal distribution 
        with mean mu and standard deviation sd.
        """
        n: int = 20
        mu: float = 65
        sd: float = 5
        now = datetime.datetime.now()
        time_delta = datetime.timedelta(hours=n)
        t = now - time_delta
        self.time_list = [(t+datetime.timedelta(hours=i)).isoformat(timespec="minutes") for i in range(n) ]
        self.temp_list = [round(np.random.randn()*sd, 1) + mu for _ in range(n)]        
        for time, temp in zip(self.time_list, self.temp_list):
            self._database.insert_data(location, time, temp)
        self.status_code = "OK"

    def get_data_from_db(self, location: Location):
        return self._database.get_time_temp(location)

    def print_data(self, location: Location):
        for time, temp in zip(self.time_list, self.temp_list):
            print(time, "", temp)
    
    def print_status(self):
        print("Mocked service status code: ", self.status_code)


class DataServiceFactory:
    """
    Instantiates the DataService.
    By default, getting the data service via API.
    """    
    def __init__(self, data_source: str, database: WeatherDatabase, mode: str = "API", ):
        self.data_source = data_source
        self.mode = mode.upper()
        self._database = database
    
    def create(self) -> IDataService:
        if self.mode == "API":
            return DataServiceFromAPI(self.data_source, self._database)
        elif self.mode == "MOCK":
            return DataServiceMocked(self.data_source, self._database)
        else:
            raise RuntimeError("Invalid mode")
