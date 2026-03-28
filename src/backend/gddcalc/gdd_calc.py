from typing import List, Tuple
from ..weather.dailyweather import (
    DailyWeatherRange
)

class GDDCalculator:
    def __init__(self, base_temp: int):
        self.base_temp: int = base_temp

    # Sine Method
    def calculate_sine(self, weather: DailyWeatherRange) -> Tuple[List[float],List[float]]:
        pass

    # Simple Method
    def calculate_simple_day(self, temp_high: float, temp_low: float) -> Tuple[List[float],List[float]]:
        gdd = (temp_high + temp_low)/2 - self.base_temp
        gdd = gdd if gdd > 0 else 0
        return gdd

    def calculate_other(self, weather: DailyWeatherRange) -> Tuple[List[float],List[float]]:
        pass

    # Baskerville-Emin method
    def calculate_be_day(self, daily_temperatures: List[int]):
        pass

    def calculate(self, calc_type: str, weather: DailyWeatherRange) -> Tuple[List[float],List[float]]:
        options = {
            "simple": self.calculate_simple,
            "sine": self.calculate_sine,
            "other": self.calculate_other,
        }

        return options[calc_type](weather)
