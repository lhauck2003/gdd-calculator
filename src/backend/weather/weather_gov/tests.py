import os

import pytest
import requests

from . import weather_gov_client as client_module
from .weather_gov_client import GOVClient, HEADERS, StationRequest, WeatherRequest, SEARCH_BY_STATION_ID_URL


class FakeResponse:
    def __init__(self, *, json_payload=None, raise_error=None):
        self._json_payload = json_payload
        self._raise_error = raise_error

    def json(self):
        return self._json_payload

    def raise_for_status(self):
        if self._raise_error is not None:
            raise self._raise_error


def test_weather_request_builds_full_query_string():
    request = WeatherRequest(
        start="2024-06-01T00:00:00Z",
        end="2024-06-02T00:00:00Z",
        cursor="next-page",
        limit=50,
        stationId="KSEA",
    )

    assert (
        request.request
        == "https://api.weather.gov/stations/KSEA/observations"
        "?start=2024-06-01T00:00:00Z"
        "&end=2024-06-02T00:00:00Z"
        "&cursor=next-page"
        "&limit=50"
    )


def test_weather_request_requires_station_id():
    with pytest.raises(Exception, match="StationId must be provided"):
        WeatherRequest(
            start="2024-06-01T00:00:00Z",
            end="2024-06-02T00:00:00Z",
            cursor=None,
            limit=None,
            stationId=None,
        )


def test_station_request_builds_points_url():
    request = StationRequest(latitude=36.67, longitude=-121.65)

    assert request.request == "https://api.weather.gov/points/36.6700,-121.6500"


def test_add_to_requests_rejects_unsupported_request_type():
    client = GOVClient()

    with pytest.raises(
        Exception,
        match="supported request type \\[WeatherRequest, StationRequest\\]",
    ):
        client.add_to_requests(object())


def test_gov_client_init_initializes_request_lists():
    client = GOVClient()
    index = client.add_to_requests(StationRequest(36.67, -121.65))

    assert index == 0
    assert len(client.station_requests) == 1
    assert client.st_rq_end == 1


def test_weather_request_uses_requests_get_with_params(monkeypatch):
    client = GOVClient()
    req = WeatherRequest(
        start="2024-06-01T00:00:00Z",
        end="2024-06-02T00:00:00Z",
        cursor="next-page",
        limit=25,
        stationId="KSEA",
    )
    calls = []

    def fake_get(url, headers=None, params=None):
        calls.append((url, headers, params))
        return FakeResponse(json_payload={"features": []})

    monkeypatch.setattr(client_module.requests, "get", fake_get)

    response = client.weather_request(req)

    assert response == []
    assert calls == [
        (
            "https://api.weather.gov/stations/KSEA/observations",
            HEADERS,
            {
                "start": "2024-06-01T00:00:00Z",
                "end": "2024-06-02T00:00:00Z",
                "cursor": "next-page",
                "limit": 25,
            },
        )
    ]


def test_weather_request_raises_when_api_fails(monkeypatch):
    client = GOVClient()
    req = WeatherRequest(
        start="2024-06-01T00:00:00Z",
        end="2024-06-02T00:00:00Z",
        cursor=None,
        limit=None,
        stationId="KSEA",
    )

    monkeypatch.setattr(
        client_module.requests,
        "get",
        lambda url, headers=None, params=None: FakeResponse(
            raise_error=Exception("boom")
        ),
    )

    with pytest.raises(Exception, match="boom"):
        client.weather_request(req)


def test_station_request_uses_requests_get_with_request_object(monkeypatch):
    client = GOVClient()
    req = StationRequest(36.67, -121.65)
    calls = []

    def fake_get(url, headers=None):
        calls.append((url, headers))
        return FakeResponse(json_payload={"properties": {"city": "Salinas"}})

    monkeypatch.setattr(client_module.requests, "get", fake_get)

    response = client.station_request(req)
    assert response == {"properties": {"city": "Salinas"}}
    assert calls == [(req.base % (req.latitude, req.longitude), HEADERS)]


def test_get_station_list_fetches_observation_stations_url(monkeypatch):
    client = GOVClient()
    req = StationRequest(36.67, -121.65)
    client.station_request = lambda station_req: {
        "properties": {
            "observationStations": "https://api.weather.gov/gridpoints/MTR/85,105/stations"
        }
    }
    calls = []

    def fake_get(url, headers=None):
        calls.append((url, headers))
        return FakeResponse(json_payload={"features": [{"id": "KSFO"}]})

    monkeypatch.setattr(client_module.requests, "get", fake_get)

    stations = client.get_station_list(req, limit=2)

    assert stations == {"features": [{"id": "KSFO"}]}
    assert calls == [
        (f"https://api.weather.gov/gridpoints/MTR/85,105/stations?limit={2}", HEADERS)
    ]


LIVE_API_REASON = (
    "set RUN_WEATHER_GOV_INTEGRATION=1 and WEATHER_GOV_USER_AGENT to run live api tests"
)


requires_live_api = pytest.mark.skipif(
    os.getenv("RUN_WEATHER_GOV_INTEGRATION") != "1" or not HEADERS["User-Agent"],
    reason=LIVE_API_REASON,
)

@requires_live_api
def test_station_request_integration_hits_points_api():
    req = StationRequest(36.67, -121.65)

    response = requests.get(req.request, headers=HEADERS)
    response.raise_for_status()
    payload = response.json()
    #print(f"Features: {payload["type"]}")

    assert payload["type"] == "Feature"
    assert "observationStations" in payload["properties"]


@requires_live_api
def test_weather_request_integration_hits_observations_api():
    req = WeatherRequest(
        start="2026-01-01T00:00:00Z",
        end="2026-03-24T00:00:00Z",
        cursor=None,
        limit=50,
        stationId="KBIL",
    )

    response = requests.get(
        f"https://api.weather.gov/stations/{req.stationId}/observations",
        headers=HEADERS,
        params={
            "start": req.start,
            "end": req.end,
            "limit": req.limit,
        },
    )
    response.raise_for_status()
    payload = response.json()
    #print(f"Features: {payload["features"]}")

    assert payload["type"] == "FeatureCollection"
    assert isinstance(payload["features"], list)


@requires_live_api
def test_gov_client_weather_request_integration_uses_live_api():
    client = GOVClient()
    req = WeatherRequest(
        start="2026-03-22T00:00:00Z",
        end="2026-03-23T00:00:00Z",
        cursor=None,
        limit=None,
        stationId="KBIL",
    )
    #print(SEARCH_BY_STATION_ID_URL % req.stationId)

    payload = client.weather_request(req)
    #print(f"Features: {payload["features"]}")

    assert payload is not None
    print(payload)
    assert isinstance(payload, list)

@requires_live_api
def test_gov_client_stations_request_uses_live_api():
    client = GOVClient()
    stations_request = StationRequest(45.9600, -108.1610)

    payload = client.get_station_list(stations_request, limit=10)
    #print(f"List: {payload}")
    assert payload is not None