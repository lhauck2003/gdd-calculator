import pytest
import os
from pytest import fixture
from time import localtime, strptime, strftime
from .weather import WeatherStation
from .NOAA.noaa_weather import NOAAInterface, NOAAClient

@fixture
def client():
    return NOAAClient(token=os.getenv("NOAA_UNIQUE_TOKEN"))

@fixture
def interface(client):
    return NOAAInterface(client=client)

@fixture
def dates():
    return ["2026-03-01", "2026-02-23", "2026-02-14", "2026-01-25"]

@fixture
def stations():
    return ["GHCND:USW00024033", "GHCND:USW00024229"]

@fixture
def weatherstations(stations, interface):
    return [WeatherStation(stationid=stationid, interface=interface) for stationid in stations]

def test_get_temp_low(weatherstations, dates):
    for w_station in weatherstations:
        for date in dates:
            result = w_station.get_temp_low(date)
            print(f"Result for station: {w_station.stationid} on date: {date} is :{result}")
            assert isinstance(result, float)

def test_get_temp_high(weatherstations, dates):
    for w_station in weatherstations:
        for date in dates:
            result = w_station.get_temp_high(date)
            print(f"Result for station: {w_station.stationid} on date: {date} is :{result}")
            assert isinstance(result, float)