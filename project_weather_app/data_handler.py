"""
The DataHandler directs the DataService 
to get the data for a given location and 
processes the data.
"""
from data_service import IDataService
from location import Location
import pandas as pd
import matplotlib.pyplot as plt

class DataHandler():
    """
    Given the data_service, get the data, and process it.
    """
    def __init__(self, data_service: IDataService):
        self.data_service = data_service
        self.visualization_handler = VisualizationHandler()

    def execute(self, location: Location):
        """
        handle the data for a given location
        """
        self.data = self.data_service.get_data_from_db(location) 
        if len(self.data) == 0:
            print("Data is not in database. Downloading data...")
            self.data_service.download_data(location)
            self.data_service.print_status()
            self.data = self.data_service.get_data_from_db(location)
        else: 
            print("Using data in database.")
        self.print_data()
        self.visualization_handler.visualize_data(self.data)
    
    def print_data(self):
        for time, precipitation_probability, precipitation, wind_speed_10m in self.data:
            print(time, precipitation_probability, precipitation, wind_speed_10m)
 
class VisualizationHandler():
    def visualize_data(self, data):
        print("visualize_data():")
        df = pd.DataFrame(data)
        df.columns = ["time", "precipitation_probability", "precipitation", "wind_speed_10m"]
        df.set_index("time", inplace=True)
        print(df)
        df.plot()
        plt.show()
