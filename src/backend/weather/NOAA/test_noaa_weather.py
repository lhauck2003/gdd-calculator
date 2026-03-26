import pytest
import os
import random
from .noaa_weather import NOAAInterface, NOAAClient
from .noaa_weather import get_stateid_by_state, get_stateid_by_abbr


@pytest.fixture
def token():
    return os.getenv("NOAA_UNIQUE_TOKEN")

@pytest.fixture
def client(token):
    return NOAAClient(token)

@pytest.fixture
def interface(client):
    return NOAAInterface(client)

@pytest.fixture
def state_abbrs():
    return ["AR", "MT", "OR", "CA", "NY", "OH"]

@pytest.fixture
def states():
    return ["Arkansas", "Montana", "Oregon", "California", "New York", "Ohio"]

@pytest.fixture
def cities():
    return ["CITY:US300001", "CITY:US410014"]

@pytest.fixture
def stations():
    return ["GHCND:USW00024033", "GHCND:USW00024229"]

@pytest.fixture
def lat_long_pairs():
    return [{"Billings": (45.7828, -108.5046)}, {"Portland": (45.5853,-122.5917)}]

@pytest.fixture
def dates():
    return [("2026-01-01", "2026-02-25"), ("2026-02-13", "2026-02-23")]

def test_search_stations_by_lat_long(interface, lat_long_pairs):
    correct = [list(city.keys()) for city in lat_long_pairs]
    response = []
    for i in range(len(lat_long_pairs)):
        lat, long = lat_long_pairs[i][correct[i][0]]
        response.append(interface.search_stations_by_lat_long(lat, long, radius=0.05))
    
    for i, value in enumerate(response):
        assert correct[i][0].strip().lower() in value["results"][0]["name"].strip().lower()

def test_search_data_by_station(interface, stations, dates):
    response = []
    for i, station in enumerate(stations):
        results = interface.search_data_by_station(
            stationid=station, startdate=dates[i][0], enddate=dates[i][1], units="metric"
            )["results"]
        response.append(results)
        
    for i, value in enumerate(response):
        # assert start date is correct
        assert dates[i][0] in value[0]["date"]
        # assert end date is correct
        assert dates[i][1] in value[-1]["date"]
        # assert station is correct
        assert stations[i] in value[0]["station"]

def test_search_stations_by_state(interface, states):
    response = []
    correct = ["GHCND:US1ARAS0012", "GHCND:USC00242793", "GHCND:USC00350036","GHCND:US1CALA0120", "GHCND:USC00300055", "GHCND:USC00331779", ""]
    for i, state in enumerate(states):
        results = interface.search_stations_by_state(
            state=states[i]
        )["results"]
        response.append(results)
    for i, value in enumerate(response):
        # assert stateid is correct, checks 1st result
        assert value[0]["id"] == correct[i]


def test_search_stations_by_city(interface, cities):
    response = []
    correct = ["SODA SPRINGS MONTANA, MT US", "PORTLAND INTERNATIONAL AIRPORT, OR US"]
    for i, city in enumerate(cities):
        results = interface.search_stations_by_city(
            cityid=city
        )["results"]
        response.append(results)
    
    for i, value in enumerate(response):
        # assert city is correct
        assert value[i]["name"] == correct[i]

def test_get_all_us_cities(interface):
    response = interface.get_all_us_cities(all=False)
    #print(response)
    #print(len(response))
    # choose random number between 0:len(response)
    test = [random.randint(0,len(response)) for _ in range(50)]
    assert response is not None
    for i in test:
        assert "CITY:US" in response[i]["id"]

def test_get_cities_by_state(interface, state_abbrs):
    response = []
    for state in state_abbrs:
        results = interface.get_cities_by_state(state)
        response.append(results)

    for i, value in enumerate(response):
        print(value)
        test = [random.randint(0,len(value)) for _ in range(10)]
        assert state_abbrs[i] in value[i]["name"]