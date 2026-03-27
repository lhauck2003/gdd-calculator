# Module for interacting with Weather Interface
from typing import Optional, List, Union, Dict
from time import struct_time, strptime, strftime

from .NOAA.noaa_weather import NOAAInterface

class WeatherStation:

    def __init__(self, stationid: Optional[str], interface: NOAAInterface):
        self.interface = interface
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

