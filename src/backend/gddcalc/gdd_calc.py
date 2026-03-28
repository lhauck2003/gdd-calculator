from typing import List, Tuple, Optional, Union
import time
from time import struct_time, mktime, strptime
import datetime
from datetime import timedelta  
from ..weather.weather import (
    Weather, WeatherLocation, WeatherStation
)

class GDDCalculator:
    def __init__(self, base_temp: int):
        self.base_temp: int = base_temp

    # Sine Method
    def calculate_sine(self, temp_high: float, temp_low: float) -> Tuple[List[float],List[float]]:
        pass

    # Simple Method
    def calculate_simple_day(self, temp_high: float, temp_low: float) -> Tuple[List[float],List[float]]:
        gdd = (temp_high + temp_low)/2 - self.base_temp
        gdd = gdd if gdd > 0 else 0
        return gdd

    def calculate_other(self, temp_high: float, temp_low: float) -> Tuple[List[float],List[float]]:
        pass

    # Baskerville-Emin method
    def calculate_be_day(self, daily_temperatures: List[int]):
        pass

    def calculate_day(self, calc_type: str, weather: Weather, date: Union[Optional[str], struct_time]) -> Tuple[List[float],List[float]]:
        options = {
            "simple": self.calculate_simple,
            "sine": self.calculate_sine,
            "other": self.calculate_other,
            "baskerville-emin": self.calculate_be_day,
        }
        temp_high = weather.get_temp_high(date)
        temp_low = weather.get_temp_low(date)

        return options[calc_type](temp_high, temp_low)

    def calculate_range(self, calc_type: str, weather: Weather, start: Union[Optional[str], struct_time], end: Union[Optional[str], struct_time]):
        options = {
            "simple": self.calculate_simple,
            "sine": self.calculate_sine,
            "other": self.calculate_other,
            "baskerville-emin": self.calculate_be_day,
        }
        start_date = datetime.fromtimestamp(time.mktime(start)).date()
        end_date = datetime.fromtimestamp(time.mktime(end)).date()

        delta = timedelta(days=1)

        curr_date = start_date
        gdd_tot = 0
        gdd_total = []
        gdd_day = []
        while curr_date <= end_date:
            gdd = self.calculate_day(calc_type, weather, curr_date.timetuple())
            gdd_tot += gdd
            gdd_day.append(gdd)
            gdd_total.append(gdd_tot)
            curr_date += delta

        return {"GDD": {"GDD_daily":gdd_day, "GDD_totals":gdd_total}}