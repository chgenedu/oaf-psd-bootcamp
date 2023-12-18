"""
The DataHandler directs the DataService 
to get the data for a given location and 
processes the data.
"""
from data_service import IDataService
from location import Location
from visualization_handler import IVisualizationHandler

import logging
logger = logging.getLogger(__name__)

class DataHandler():
    """
    Given the data_service, get the data, and process it.
    """
    def __init__(self, data_service: IDataService, 
                 visualization_handler: IVisualizationHandler):
        self.data_service = data_service
        self.visualization_handler = visualization_handler

    def execute(self, location: Location):
        """
        Execute the data handler process for a given location
        Get data from data service if data for the specified location 
        is not available in the database.
        """
        self.data = self.data_service.get_data_from_db(location) 

        if self.data.empty:
            logger.info("Data is not in database. Downloading data...")
            self.data_service.download_data(location)
            self.data_service.print_status()
            self.data = self.data_service.get_data_from_db(location)
        else: 
            logger.info("Using data in database.")
        
        # Print data to console
        self.print_data()

        # Use the visualizer.
        self.visualization_handler.visualize_data(self.data)
    
    def print_data(self):
        """
        Print the data in the data handler.
        """
        print(self.data) 
