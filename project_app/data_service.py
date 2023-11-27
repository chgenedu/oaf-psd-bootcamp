import requests
import read_config as rc
from abc import abstractmethod


# interface for DataService
class IDataService:
    @abstractmethod
    def __init__(self, data_source):
        pass

    @abstractmethod
    def get_data(self):
        pass
    
    @abstractmethod
    def print_data(self):
        pass
    
    @abstractmethod
    def print_status(self):
        pass


class DataServiceFromAPI(IDataService):
    def __init__(self, data_source):
        self._url, self._payload = rc.get_config(data_source)

    def get_data(self):
        try:
            r = requests.get(self._url, params=self._payload)
        except Exception:
            print("Error: Cannot get data with API.")
            time = []
            temp = []
        else:
            data = r.json().get("hourly", {})
            time = data["time"]
            temp = data[self._payload["hourly"]]
        self.status_code = r.status_code
        self.time_list = time
        self.temp_list = temp
    
    def print_data(self):
        for time, temp in zip(self.time_list, self.temp_list):
            print(time, "", temp)
    
    def print_status(self):
        print("API status code: ", self.status_code)


# placeholder for dummy data service from file.
class DataServiceFromFile(IDataService):
    def __init__(self, data_source):
        super().__init__(data_source)
    def get_data(self):
        pass
    def print_data(self):
        pass
    def print_status(self):
        pass


class DataServiceFactory:
    """
    Instantiates the DataService.
    By default, getting the data service via API.
    """    
    def __init__(self, data_source, mode="API"):
        self.data_source = data_source
        self.mode = mode
    
    def create(self):
        if self.mode == "API":
            return DataServiceFromAPI(self.data_source)
        else:
            return DataServiceFromFile(self.data_source)
