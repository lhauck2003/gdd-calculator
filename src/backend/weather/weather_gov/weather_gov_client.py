# client to interact with weather.gov API
from typing import List, Optional, Union, Dict
import requests
import os
from time import strptime, strftime, struct_time
from .urls import (
    NOAA_API_URL,
    SEARCH_BY_LAT_LONG_URL,
    SEARCH_BY_STATION_ID_URL,
    SEARCH_BY_GRID_ID
)

HEADERS = {
    "Accept": "application/geo+json",
    "User-Agent": os.getenv("WEATHER_GOV_USER_AGENT"),
}

class Request:
    pass

class WeatherRequest(Request):
    def __init__(
            self, 
            start: Optional[Union[str, struct_time]], 
            end: Optional[Union[str, struct_time]], 
            cursor: Optional[str],
            limit: Optional[int], 
            stationId: Optional[str]
        ):
        self.base = SEARCH_BY_STATION_ID_URL
        self.start = start if isinstance(start, str) else strftime("%Y-%m-%dT%H:%M:%SZ", start)
        self.end = end if isinstance(end, str) else strftime("%Y-%m-%dT%H:%M:%SZ", end)
        self.cursor = cursor
        self.limit = limit
        if stationId is None:
            raise Exception("StationId must be provided")
        self.stationId = stationId

    @property
    def request(self) -> str:
        base = self.base % self.stationId
        params = []

        if self.start is not None:
            params.append(f"start={self.start}")
        if self.end is not None:
            params.append(f"end={self.end}")
        if self.cursor is not None:
            params.append(f"cursor={self.cursor}")
        if self.limit is not None:
            params.append(f"limit={self.limit}")

        if not params:
            return base

        return f"{base}?{'&'.join(params)}"


class StationRequest(Request):
    def __init__(self, latitude: float, longitude: float):
        self.base = SEARCH_BY_LAT_LONG_URL
        self.latitude = latitude
        self.longitude = longitude

    @property
    def request(self):
        base = self.base % (self.latitude, self.longitude)
        return base

# client to handle requests
# when appending a new request to the client, return an index, which is the index
# of the result once returned
class GOVClient:
    def __init__(self):
        self.station_requests: List[StationRequest] = []
        self.weather_requests: List[WeatherRequest] = []
        self.st_rq_end = 0
        self.w_rq_end = 0

    # adds a request to the batch
    # :param request - a request, can be of type StationRequest or WeatherRequest
    # :returns index of the request in corresponding batch (by type)
    def add_to_requests(self, request: Request) -> int:
        if isinstance(request, StationRequest):
            self.station_requests.append(request)
            self.st_rq_end+=1
            return (self.st_rq_end - 1)
        if isinstance(request,WeatherRequest):
            self.weather_requests.append(request)
            self.w_rq_end+=1
            return (self.w_rq_end - 1)
        else:
            raise Exception("Must be a supported request type [WeatherRequest, StationRequest]")

    # TODO: batch requests of same type if possible
    # for WeatherRequests, find all requests with the same station ID, choose the earliest
    # start and latest end, and remove limits (if needed) and submit request. keep track of 
    # specific requests, and store individual requests separately after applying correct 
    # start, end, and limits to the results.
    # 
    # RETURNS: list containing the data from the specific query. The index of the result
    # should match the index of the query in the list
    def batch_weather_request(self) -> List:
        pass

    def weather_request(self, req: WeatherRequest) -> List:
        params = {}
        if req.start:
            params["start"] = req.start
        if req.end:
            params["end"] = req.end
        if req.cursor:
            params["cursor"] = req.cursor
        if req.limit:
            params["limit"] = req.limit
        obs = requests.get(
            SEARCH_BY_STATION_ID_URL % req.stationId,
            headers=HEADERS,
            params=params,
        )
        obs.raise_for_status()
        obs_data = obs.json()

        features = obs_data["features"]
        # get all next pages
        while "pagination" in obs_data.keys():
            obs = requests.get(obs_data["pagination"]["next"], headers=HEADERS)
            obs.raise_for_status()
            obs_data = obs.json()
            new_features = obs_data["features"]
            features.extend(new_features)
        return features
    # TODO
    # for each request in the list, request the data
    #
    # RETURNS: list containing the data from the specific query. The index of the result
    # should match the index of the query in the list
    def station_request(self, req: StationRequest) -> List:
        point = requests.get(
            req.base % (req.latitude, req.longitude)
            , headers=HEADERS
        )
        point.raise_for_status()
        point_data = point.json() 
        return point_data
    
    def get_station_list(self, req: StationRequest, limit: Optional[int]) -> List:
        res = self.station_request(req)

        stations_url = res["properties"]["observationStations"]
        stations = requests.get(stations_url + f"?limit={limit}" if limit is not None else ""
                                , headers=HEADERS)
        stations.raise_for_status()
        stations_data = stations.json()
        return stations_data