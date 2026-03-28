# Module for interacting with Weather Interface
from typing import Optional, List, Union, Dict
from time import struct_time, strptime, strftime

from .NOAA.noaa_weather import NOAAInterface
from .OpenWeather.ow_interface import OpenWeatherInterface

class Weather:
    def __init__(self, interface: Union[NOAAInterface, OpenWeatherInterface]):
        self.interface = interface

    def get_temp_high(self, date: Union[Optional[str], Optional[struct_time]] = None):
        pass

    def get_temp_low(self, date: Union[Optional[str], Optional[struct_time]] = None):
        pass

# --------------------------------
# NOAA Weather
# --------------------------------
class WeatherStation(Weather):
    def __init__(self, interface: Optional[NOAAInterface], stationid: Optional[str] = None):
        super().__init__(interface)
        if stationid is None:
            raise Exception("Must specify stationid for interface given (NOAAInterface)")
        if (self.interface.check_station(stationid)):
            self.stationid = stationid
        else:
            raise Exception("Station ID is not valid")


    def get_temp_high(self, date: Union[Optional[str], Optional[struct_time]] = None):
        if isinstance(date,str):
            date=strptime(date, "%Y-%m-%dT%H:%M:%sZ") # may change format if needed to be universal
        else:
            date=date
        return self.interface.get_temp_high_by_day(stationid=self.stationid, date=date)
        

    def get_temp_low(self, date: Union[Optional[str], Optional[struct_time]] = None):
        if isinstance(date,str):
            date=strptime(date, "%Y-%m-%dT%H:%M:%sZ") # may change format if needed to be universal
        else:
            date=date
        return self.interface.get_temp_low_by_day(stationid=self.stationid, date=date)

# --------------------------------
# OpenWeather
# --------------------------------
class WeatherLocation(Weather):
    def __init__(self, interface: OpenWeatherInterface, lat: Optional[float] = None, lon: Optional[float] = None):
        super().__init__(interface)
        if (lat is None or lon is None):
            raise Exception("Must specify lat and lon for interface given (OpenWeatherInterface)")
        self.lat = lat
        self.lon = lon

    def get_temp_high(self, date: Union[Optional[str], Optional[struct_time]] = None):
        if isinstance(date,str):
            date=strptime(date, "%Y-%m-%d") # may change format if needed to be universal
        else:
            date=date
        self.interface.get_temp_high_by_day(self.lat, self.lon, date)

    def get_temp_low(self, date: Union[Optional[str], Optional[struct_time]] = None):
        if isinstance(date,str):
            date=strptime(date, "%Y-%m-%d") # may change format if needed to be universal
        else:
            date=date
        self.interface.get_temp_low_by_day(self.lat, self.lon, date)