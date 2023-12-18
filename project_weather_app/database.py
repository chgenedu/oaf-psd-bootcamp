"""
The WeatherDatabase object manages the low level interaction with the database.
"""
import sqlite3
from location import Location
from util import get_file_path
import os.path

class WeatherDatabase():
    """
    Create database for storing weather time temperature
    """
    def __init__(self, db_file: str) -> None:
        # get complete path to the file
        filepath = get_file_path(db_file, calling_file=__file__)        
        
        # check if db_file exist
        if not os.path.exists(filepath):
            print("Database not found: ", filepath)
            self.conn = None # for destructor in case file does not exist.
            exit(1)
        else:
            print("Connecting to database: ", filepath)
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

    def get_single_record(self, location: Location, time):
        self.cursor.execute(''' 
            SELECT precipitation_probability, precipitation, wind_speed_10m 
                FROM weather
                WHERE longitude = ? 
                AND latitude = ?
                AND time = ?;
        ''', (location.get_longitude(), location.get_latitude(), time))
        data = self.cursor.fetchall()
        return data

    def get_location_record(self, location: Location):
        self.cursor.execute(''' 
            SELECT time, precipitation_probability, precipitation, wind_speed_10m 
                FROM weather
                WHERE longitude = ? 
                AND latitude = ?;
        ''', (location.get_longitude(), location.get_latitude()))
        data = self.cursor.fetchall()
        return data

    def get_all_data(self):
        self.cursor.execute('''  
            SELECT * FROM weather;
        ''')
        data = self.cursor.fetchall()
        return data

    def insert_single_record(self, location: Location, time, 
                        precipitation_probability, precipitation, wind_speed_10m):
        record = self.get_single_record(location, time)
        if record == []: # insert only if there is no database record 
                         # for this location and time
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

    def reset(self):
        self.cursor.execute(''' 
            DELETE FROM weather; 
        ''')
        self.conn.commit()
        print("Database table 'weather' is deleted.")

    def drop(self):
        self.cursor.execute(''' 
            DROP TABLE IF EXISTS weather; 
        ''')
        self.conn.commit()
        print("Database table 'weather' is dropped.")

    def __del__(self):
        """
        Close connection when object is deleted.
        """
        if self.conn is not None:
            self.conn.close()
