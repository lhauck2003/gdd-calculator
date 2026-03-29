import pytest
import os
from pytest import fixture
from time import localtime, strptime, strftime
from .weather import WeatherStation, WeatherLocation
from .NOAA.noaa_weather import NOAAInterface, NOAAClient
from .OpenWeather.ow_interface import OpenWeatherInterface, OpenWeatherClient

@fixture
def client():
    return NOAAClient(token=os.getenv("NOAA_UNIQUE_TOKEN"))

@fixture
def ow_client():
    return OpenWeatherClient(api_key=os.getenv("OPENWEATHER_API_KEY"))

@fixture
def NOAAinterface(client):
    return NOAAInterface(client=client)

@fixture
def OWInterface(ow_client):
    return OpenWeatherInterface(ow_client)

@fixture
def timestamps():
    return ["2026-03-01", "2026-02-23", "2026-02-14", "2026-01-25"]

@fixture
def stations():
    return ["GHCND:USW00024033", "GHCND:USW00024229"]

@fixture
def locations():
    return [(45.7828, -108.5046), (45.5152, -122.6784)]

@fixture
def weatherstations(stations, NOAAinterface):
    return [WeatherStation(stationid=stationid, interface=NOAAinterface) for stationid in stations]

@fixture
def weatherlocations(locations, OWInterface):
    return [WeatherLocation(interface=OWInterface, lat=location[0], lon=location[1]) for location in locations]

def test_get_temp_low_station(weatherstations, timestamps):
    for w_station in weatherstations:
        for date in timestamps:
            result = w_station.get_temp_low(date)
            print(f"Result for station: {w_station.stationid} on date: {date} is :{result}")
            assert isinstance(result, float)

def test_get_temp_high_station(weatherstations, timestamps):
    for w_station in weatherstations:
        for date in timestamps:
            result = w_station.get_temp_high(date)
            print(f"Result for station: {w_station.stationid} on date: {date} is :{result}")
            assert isinstance(result, float)

def test_get_temp_low_location(weatherlocations, timestamps):
    for w_location in weatherlocations:
        for date in timestamps:
            result = w_location.get_temp_low(date)
            print(f"Result for location: {w_location.lat},{w_location.lon} on date: {date} is :{result}")
            assert isinstance(result, float)

def test_get_temp_high_location(weatherlocations, timestamps):
    for w_location in weatherlocations:
        for date in timestamps:
            result = w_location.get_temp_high(date)
            print(f"Result for location: {w_location.lat},{w_location.lon} on date: {date} is :{result}")
            assert isinstance(result, float)