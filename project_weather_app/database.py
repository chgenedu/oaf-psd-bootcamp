import sqlite3
from location import Location

class WeatherDatabase():
    """
    Create database for storing weather time temperature
    """
    def __init__(self, db_file: str) -> None:
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                longitude REAL,
                latitude REAL,
                time TEXT,
                temperature REAL
            );
        ''')

    def get_time_temp(self, location: Location):
        self.cursor.execute(''' 
            SELECT time, temperature FROM weather
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

    def insert_data(self, location: Location, time, temperature):
        self.cursor.execute(''' 
            INSERT INTO weather
                (longitude, latitude, time, temperature)
                VALUES (?, ?, ?, ?);
        ''', (location.get_longitude(), location.get_latitude(), time, temperature))
        self.conn.commit()

    def reset(self):
        self.cursor.execute(''' 
            DELETE FROM weather; 
        ''')
        self.conn.commit()
        print("Database table 'weather' is deleted.")

    def __del__(self):
        """
        Close connection when object is deleted.
        """
        self.conn.close()
