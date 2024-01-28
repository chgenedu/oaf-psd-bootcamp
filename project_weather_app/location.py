"""
A Location object is used to store the location data,
such as the longitude and the latitude of a location.
"""
class Location():
    def __init__(self, longitude, latitude) -> None:
        self._longitude = longitude
        self._latitude = latitude
    def get_longitude(self):
        return self._longitude
    def get_latitude(self):
        return self._latitude