from typing import Optional, Union, List, Dict
import time
from time import struct_time
from datetime import datetime, date, timedelta

from .ow_client import OpenWeatherClient

class OpenWeatherInterface:
    def __init__(self, client: OpenWeatherClient):
        self.client = client

    def search_data_by_location(self, lat, lon):
        pass

    # avoid using, each day is one request, limit at 1000 requests per month
    def search_data_in_time_range(self, lat, lon, start, end):
        pass

    def get_temp_high_by_day(self, lat, lon, date):
        pass

    def get_temp_low_by_day(self, lat, lon, date):
        pass