import pytest

from .dailyweather import (
    DailyWeatherRange,
    DayWeatherInfo,
    StationOptions,
    WeatherInfo,
)
from .weather_gov.weather_gov_client import StationRequest, WeatherRequest


def make_weather_entry(timestamp, *, value, min_value, max_value, description="Clear"):
    return {
        "properties": {"timestamp": timestamp},
        "station": "https://api.weather.gov/stations/KXYZ",
        "stationId": "KXYZ",
        "stationName": "Example Station",
        "timestamp": timestamp,
        "rawMessage": "KXYZ observation",
        "textDescription": description,
        "presentWeather": [{"intensity": "light", "weather": "rain"}],
        "temperature": {
            "unitCode": "wmoUnit:degC",
            "value": value,
            "minValue": min_value,
            "maxValue": max_value,
        },
        "dewpoint": {"unitCode": "wmoUnit:degC", "value": value - 2},
        "windDirection": {"unitCode": "wmoUnit:degree_(angle)", "value": 180},
        "windSpeed": {"unitCode": "wmoUnit:km_h-1", "value": 10},
        "windGust": {"unitCode": "wmoUnit:km_h-1", "value": 15},
        "barometricPressure": {"unitCode": "wmoUnit:Pa", "value": 100000},
        "seaLevelPressure": {"unitCode": "wmoUnit:Pa", "value": 100500},
        "visibility": {"unitCode": "wmoUnit:m", "value": 16000},
        "maxTemperatureLast24Hours": {"unitCode": "wmoUnit:degC", "value": max_value},
        "minTemperatureLast24Hours": {"unitCode": "wmoUnit:degC", "value": min_value},
        "precipitationLastHour": {"unitCode": "wmoUnit:mm", "value": 1},
        "precipitationLast3Hours": {"unitCode": "wmoUnit:mm", "value": 2},
        "precipitationLast6Hours": {"unitCode": "wmoUnit:mm", "value": 3},
        "relativeHumidity": {"unitCode": "wmoUnit:percent", "value": 55},
        "windChill": {"unitCode": "wmoUnit:degC", "value": value - 1},
        "heatIndex": {"unitCode": "wmoUnit:degC", "value": value + 1},
        "cloudLayers": [{"base": {"unitCode": "wmoUnit:m", "value": 1200}}],
    }


class FakeGovClient:
    def __init__(self, *, station_metadata=None, weather_features=None, station_list=None):
        self.station_metadata = station_metadata or {"properties": {"city": "Davis", "state": "CA"}}
        self.weather_features = weather_features or []
        self.station_list_response = station_list or [{"id": "KXYZ", "name": "Example Station"}]
        self.requests = []
        self.get_station_list_calls = []

    def add_to_requests(self, request):
        self.requests.append(request)
        return len(self.requests) - 1

    def station_request(self):
        return [self.station_metadata]

    def batch_weather_request(self):
        return [{"features": self.weather_features}]

    def get_station_list(self, req, limit):
        self.get_station_list_calls.append((req, limit))
        return self.station_list_response


@pytest.fixture
def weather_features():
    return [
        make_weather_entry("2024-06-01T08:00:00+00:00", value=10, min_value=8, max_value=15),
        make_weather_entry("2024-06-01T14:00:00+00:00", value=18, min_value=12, max_value=22),
        make_weather_entry("2024-06-02T09:00:00+00:00", value=11, min_value=7, max_value=16),
        make_weather_entry("2024-06-02T15:00:00+00:00", value=20, min_value=13, max_value=24),
        {
            **make_weather_entry(None, value=99, min_value=99, max_value=99),
            "properties": {},
            "timestamp": None,
        },
    ]


def test_station_options_loads_metadata_on_init():
    client = FakeGovClient(station_metadata={"properties": {"city": "Salinas", "state": "CA"}})

    options = StationOptions(latitude=36.67, longitude=-121.65, client=client)

    assert options.city == "Salinas"
    assert isinstance(client.requests[0], StationRequest)
    assert client.requests[0].latatude == 36.67
    assert client.requests[0].longitude == -121.65


def test_station_options_stations_uses_client_station_lookup():
    client = FakeGovClient(station_list=[{"id": "KSFO", "name": "San Francisco"}])
    options = StationOptions(latitude=37.62, longitude=-122.38, client=client)

    stations = options.stations()

    assert stations == [{"id": "KSFO", "name": "San Francisco"}]
    req, limit = client.get_station_list_calls[0]
    assert isinstance(req, StationRequest)
    assert limit is None


def test_weather_info_exposes_temperature_helpers():
    info = WeatherInfo(make_weather_entry("2024-06-01T08:00:00+00:00", value=14, min_value=9, max_value=20))

    assert info.stationId == "KXYZ"
    assert info.textDescription == "Clear"
    assert info.temp_low == 9
    assert info.temp_avg == 14
    assert info.temp_high == 20


def test_day_weather_info_builds_weather_objects_and_temperatures():
    day = DayWeatherInfo(
        [
            make_weather_entry("2024-06-01T08:00:00+00:00", value=10, min_value=8, max_value=15),
            make_weather_entry("2024-06-01T14:00:00+00:00", value=18, min_value=12, max_value=22),
        ]
    )
    weather_list = day.get_weather_list()

    assert len(weather_list) == 2
    assert all(isinstance(entry, WeatherInfo) for entry in weather_list)
    assert day.get_temperatures() == [10, 18]


def test_daily_weather_range_requests_station_history_from_client(weather_features):
    client = FakeGovClient(weather_features=weather_features)

    weather_range = DailyWeatherRange(
        start_day="2024-06-01T00:00:00Z",
        station_id="KXYZ",
        client=client,
    )

    assert weather_range.station_id == "KXYZ"
    assert weather_range.weather_data == weather_features
    assert isinstance(client.requests[0], WeatherRequest)
    assert client.requests[0].stationId == "KXYZ"
    assert client.requests[0].start == "2024-06-01T00:00:00Z"


def test_daily_weather_range_groups_entries_by_day_and_skips_missing_timestamps(weather_features):
    weather_range = DailyWeatherRange(
        start_day="2024-06-01T00:00:00Z",
        station_id="KXYZ",
        client=FakeGovClient(weather_features=weather_features),
    )

    grouped = weather_range.get_daily_weather_list()

    assert len(grouped) == 2
    assert all(isinstance(day, DayWeatherInfo) for day in grouped)
    assert [len(day.weather_data) for day in grouped] == [2, 2]


def test_daily_weather_range_returns_temperatures_grouped_by_day(weather_features):
    weather_range = DailyWeatherRange(
        start_day="2024-06-01T00:00:00Z",
        station_id="KXYZ",
        client=FakeGovClient(weather_features=weather_features),
    )

    assert weather_range.get_temperatures() == [[10, 18], [11, 20]]
