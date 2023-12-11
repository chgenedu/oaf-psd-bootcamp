from data_service import IDataService
from location import Location

class DataHandler():
    """
    Given the data_service, get the data, and process it.
    """
    def __init__(self, data_service: IDataService):
        self.data_service = data_service

    def execute(self, location: Location):
        """
        handle the data for a given location
        """
        self.data = self.data_service.get_data_from_db(location) 
        # self.data is a list of time, temperature pair.
        if len(self.data) == 0:
            print("Data is not in database. Downloading data...")
            self.data_service.download_data(location)
            self.data_service.print_status()
            self.data = self.data_service.get_data_from_db(location)
        else: 
            print("Using data in database.")
        self.print_data()
    
    def print_data(self):
        for time, temp in self.data:
            print(time, temp)

