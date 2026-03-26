import pytest

from typing import List
from .gdd_calc import GDDCalculator
from ..weather.dailyweather import DailyWeatherRange
from ..weather.weather_gov.weather_gov_client import GOVClient

@pytest.fixture
def calculator():
    return GDDCalculator(0)

@pytest.fixture
def client():
    return GOVClient()

@pytest.fixture
def weather(client):
    return DailyWeatherRange("2026-01-01T00:00:00Z", "KBIL", client)

def test_simple_calc(calculator, weather):
    calc_type = "simple"
    print([item.get_temp_high() for item in weather.daily_weather_list])

    daily_gdd, total_gdd = calculator.calculate(calc_type, weather)
    print(f"Last 5 days GDD by day: {daily_gdd[-5:]}")
    print(f"Total GDD: {total_gdd[-1]}")
    