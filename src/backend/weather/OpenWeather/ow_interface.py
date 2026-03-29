from typing import Optional, Union, List, Dict
import time
from time import struct_time, strftime
from datetime import datetime, date, timedelta

from .ow_client import OpenWeatherClient, is_valid_format

class OpenWeatherInterface:
    def __init__(self, client: OpenWeatherClient):
        self.client = client

    def search_data_by_location(self, lat: float, lon: float):
        self.client.fetch_current_weather(lat, lon)

    # avoid using, each day is one request, limit at 1000 requests per month
    def search_data_in_time_range(self, lat: float, lon: float, start: Union[Optional[str], struct_time], end: Union[Optional[str], struct_time]):
        pass

    def get_temp_high_by_day(self, lat: float, lon: float, date: Union[Optional[str], struct_time]):
        if isinstance(date, str) and not is_valid_format(date):
            raise Exception("Date string must be in YYYY-MM-DD format")
        elif isinstance(date, struct_time):
            date = strftime("%Y-%m-%d", date)
        elif date is None:
            raise Exception("Must specify date")
        
        results = self.client.fetch_daily_aggregation_weather(lat, lon, date)
        return results["temperature"]["max"]

    def get_temp_low_by_day(self, lat: float, lon: float, date: Union[Optional[str], struct_time]):
        if isinstance(date, str) and not is_valid_format(date):
            raise Exception("Date string must be in YYYY-MM-DD format")
        elif isinstance(date, struct_time):
            date = strftime("%Y-%m-%d", date)
        elif date is None:
            raise Exception("Must specify date")
        
        results = self.client.fetch_daily_aggregation_weather(lat, lon, date)
        return results["temperature"]["min"]