from typing import List, Tuple
from ..weather.dailyweather import (
    DailyWeatherRange
)

class GDDCalculator:
    def __init__(self, base_temp: int):
        self.base_temp: int = base_temp

    def calculate_sine(self, weather: DailyWeatherRange) -> Tuple[List[float],List[float]]:
        pass

    def calculate_simple(self, weather: DailyWeatherRange) -> Tuple[List[float],List[float]]:
        daily_gdd = []
        rolling_total_gdd = []
        temp_highs: List[int] = weather.get_daily_temp_highs()
        temp_lows: List[int] = weather.get_daily_temp_lows()
        if not len(temp_highs)==len(temp_lows):
            raise Exception("Length of temperature lists differ")
        
        for i in range(len(temp_highs)):
            gdd = (temp_highs[i] + temp_lows[i])/2 - self.base_temp
            gdd = gdd if gdd > 0 else 0
            daily_gdd.append(gdd)
            if i == 0:
                rolling_total_gdd.append(gdd)
            else:
                rolling_total_gdd.append(rolling_total_gdd[i-1] + gdd)
        return (daily_gdd, rolling_total_gdd)

    def calculate_other(self, weather: DailyWeatherRange) -> Tuple[List[float],List[float]]:
        pass

    def _calculate(self, calculator) -> Tuple[List[float],List[float]]:
       return calculator

    def calculate(self, calc_type: str, weather: DailyWeatherRange) -> Tuple[List[float],List[float]]:
        options = {
            "simple": self.calculate_simple,
            "sine": self.calculate_sine,
            "other": self.calculate_other,
        }

        return options[calc_type](weather)
