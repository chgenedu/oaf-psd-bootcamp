"""
The WeatherDatabase object manages the low level interaction with the database.
"""
import sqlite3
from location import Location
from util import get_file_path
import os.path
import pandas as pd
import numpy as np

from exception import DatabaseError

import logging
logger = logging.getLogger(__name__)

class WeatherDatabase():
    def __init__(self, db_file: str) -> None:
        """
        Create database for storing weather time temperature
        """
        # get complete path to the file
        filepath = get_file_path(db_file, calling_file=__file__)        
        
        # check if db_file exist
        if not os.path.exists(filepath):
            logger.info("Database not found: " + str(filepath))
            logger.info("The database will be created.")
        else:
            logger.info("Database found: " + str(filepath))

        # sqlite3.connect() will create the database if it does not exist.
        logger.info("Connecting to database: " + str(filepath))
        try:
            self.conn = sqlite3.connect(filepath)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS weather (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    longitude REAL,
                    latitude REAL,
                    time TEXT,
                    precipitation_probability REAL,
                    precipitation REAL, 
                    wind_speed_10m REAL
                );
            ''')
        except Exception as err:
            raise DatabaseError("Error in database initialiation.", err)

    def _get_df(self, data):
        """ 
        Get the pandas dataframe fro the given data. 
        """
        columns = ["time", "precipitation_probability", "precipitation", "wind_speed_10m"]
        if data == []:
            # create an empty dataframe with column names
            df = pd.DataFrame(columns = columns) 
        else:
            # create data frame if there is data
            df = pd.DataFrame(data)
            df.columns = columns
        # convert time format from isoformat to np.datetime64
        df["time"] = df["time"].map(np.datetime64)
        df.set_index("time", inplace=True) # set time as the dataframe's index column
        return df

    def insert_single_record(self, location: Location, time, 
                        precipitation_probability, precipitation, wind_speed_10m):
        record = self.get_single_record(location, time)
        """
        Insert a single record into the database.
        Record is inserted only if there is no database record for this location and time
        """
        if record.empty:
            try:
                self.cursor.execute(''' 
                    INSERT INTO weather
                        (longitude, latitude, time,                         
                                precipitation_probability, 
                                precipitation,
                                wind_speed_10m)
                        VALUES (?, ?, ?, ?, ?, ?);
                ''', (location.get_longitude(), location.get_latitude(), time, 
                                precipitation_probability, precipitation, wind_speed_10m))
                self.conn.commit()
            except Exception as err:
                raise DatabaseError("Error in insert_single_record() from database.", err)

    def get_single_record(self, location: Location, time):
        """
        Get a single record for the specified location and time.
        """
        try:
            self.cursor.execute(''' 
                SELECT precipitation_probability, precipitation, wind_speed_10m 
                    FROM weather
                    WHERE longitude = ? 
                    AND latitude = ?
                    AND time = ?;
            ''', (location.get_longitude(), location.get_latitude(), time))
            data = self.cursor.fetchall()
        except Exception as err:
            raise DatabaseError("Error in get_single_record() from database.", err)
        else:
            return self._get_df(data)

    def get_location_record(self, location: Location):
        """
        Get the three weather records for all times for a given location from the database.
        """
        try:
            self.cursor.execute(''' 
                SELECT time, precipitation_probability, precipitation, wind_speed_10m 
                    FROM weather
                    WHERE longitude = ? 
                    AND latitude = ?;
            ''', (location.get_longitude(), location.get_latitude()))
            data = self.cursor.fetchall()
        except Exception as err:
            raise DatabaseError("Error in get_location_record() from database.", err)
        else:
            return self._get_df(data)

    def get_all_data(self):
        """
        Get all records from the database.
        """
        try:
            self.cursor.execute('''  
                SELECT * FROM weather;
            ''')
            data = self.cursor.fetchall()
        except Exception as err:
            raise DatabaseError("Error in get_all_data() from database.", err)
        else:
            return self._get_df(data)


    def reset(self):
        """
        Reset the database by deleting all records from the 'weather' table of the database.
        """
        try: 
            self.cursor.execute(''' 
                DELETE FROM weather; 
            ''')
            self.conn.commit()
        except Exception as err:
            raise DatabaseError("Error in deleting all rows for database.", err)
        else:
            logger.info("Reset database table 'weather': delete all rows.")

    def drop(self):
        """
        Drop the database table from the database.
        """
        try: 
            self.cursor.execute(''' 
                DROP TABLE IF EXISTS weather; 
            ''')
            self.conn.commit()
        except Exception as err:
            raise DatabaseError("Error in dropping table from database.", err)
        else:
            logger.info("Database table 'weather' is dropped.")

    def __del__(self):
        """
        Close connection when object is deleted.
        """
        try:
            self.conn.close()
        except Exception as err:
            raise DatabaseError("Error in closing database connection.", err)
