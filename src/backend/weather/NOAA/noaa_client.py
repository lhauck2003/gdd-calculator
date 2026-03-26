# module to intereact with NOAA api
# https://www.ncdc.noaa.gov/cdo-web/api/v2
from typing import List, Optional, Union, Dict, Tuple
import requests
import os
from time import strptime, strftime, struct_time

from .urls import (
    NOAA_API_STATIONS_PATH,
    NOAA_LOCATIONS_PATH,
    NOAA_API_DATA_PATH
)

HEADERS = {"token": os.getenv("NOAA_UNIQUE_TOKEN")}

class NOAAClient:
    def __init__(self, token: Optional[str]):
        if token is None:
            raise Exception("Must include NOAA unique Token")
        self.__token = token
        self.header = {"token": token}

    def stations(
            self,
            stationid: Optional[str] = None,
            datasetid: Optional[str] = None,
            locationid: Optional[str] = None,
            datacategoryid: Optional[str] = None,
            datatypeid: Optional[str] = None,
            extent: Optional[Tuple[float,float,float,float]] = None,
            startdate: Optional[str] = None,
            enddate: Optional[str] = None,
            sortfield: Optional[str] = None,
            sortorder: Optional[str] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
    ):
        params = {}
        if datasetid is not None:
            params["datasetid"] = datasetid
        if datatypeid is not None:
            params["datatypeid"] = datatypeid
        if locationid is not None:
            params["locationid"] = locationid
        if datacategoryid is not None:
            params["datacategoryid"] = datacategoryid
        if extent is not None:
            params["extent"] = f"{extent[0]},{extent[1]},{extent[2]},{extent[3]}"
        if startdate is not None:
            params["startdate"] = startdate
        if enddate is not None:
            params["enddate"] = enddate
        if sortfield is not None:
            params["sortfield"] = sortfield
        if sortorder is not None:
            params["sortorder"] = sortorder
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = requests.get(url=NOAA_API_STATIONS_PATH + (f"/{stationid}" if stationid else "")
                                , params=params
                                , headers=self.header)
        response.raise_for_status()
        response_data = response.json()
        return response_data

    def data(
            self,
            datasetid: Optional[str], # REQUIRED
            startdate: Optional[str], # REQUIRED
            enddate: Optional[str], # REQUIRED
            datatypeid: Optional[str]=None,
            locationid: Optional[str]=None,
            stationid: Optional[str]=None,
            units: Optional[str]=None,
            sortfield: Optional[str]=None,
            sortorder: Optional[str]=None,
            limit: Optional[int]=None,
            offset: Optional[int]=None,
            includemetadata: Optional[bool]=None
        ):
        if datasetid is None or startdate is None or enddate is None:
            raise Exception("Must specify datasetid, startdate, and enddate")
        params = {}
        if datasetid is not None:
            params["datasetid"] = datasetid
        if datatypeid is not None:
            params["datatypeid"] = datatypeid
        if locationid is not None:
            params["locationid"] = locationid
        if stationid is not None:
            params["stationid"] = stationid
        if startdate is not None:
            params["startdate"] = startdate
        if enddate is not None:
            params["enddate"] = enddate
        if units is not None:
            params["units"] = units
        if sortfield is not None:
            params["sortfield"] = sortfield
        if sortorder is not None:
            params["sortorder"] = sortorder
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if includemetadata is not None:
            params["includemetadata"] = includemetadata

        response = requests.get(NOAA_API_DATA_PATH, params=params, headers=self.header)
        response.raise_for_status()
        response_data = response.json()
        return response_data



    def locations(
            self,
            stateid: Optional[str] = None,
            datasetid: Optional[str] = None,
            locationcategoryid: Optional[str] = None,
            datacategoryid: Optional[str] = None,
            startdate: Optional[str] = None,
            enddate: Optional[str] = None,
            sortfield: Optional[str] = None,
            sortorder: Optional[str] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
    ):
        params = {}
        if datasetid is not None:
            params["datasetid"] = datasetid
        if locationcategoryid is not None:
            params["locationcategoryid"] = locationcategoryid
        if datacategoryid is not None:
            params["datacategoryid"] = datacategoryid
        if startdate is not None:
            params["startdate"] = startdate
        if enddate is not None:
            params["enddate"] = enddate
        if sortfield is not None:
            params["sortfield"] = sortfield
        if sortorder is not None:
            params["sortorder"] = sortorder
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = requests.get(NOAA_LOCATIONS_PATH + f"/{stateid}" if stateid else ""
                                , params=params
                                , headers=self.header)
        response.raise_for_status()
        response_data = response.json()
        return response_data
    
    # ---------------------------
    # OTHER
    # ---------------------------
    def get_all_us_cities(self, all:bool=True):
        all_cities = []
        offset = 1

        while True:
            params = {
                "datasetid": "GHCND",
                "locationcategoryid": "CITY",
                "limit": 1000,
                "offset": offset
            }

            response = requests.get(NOAA_LOCATIONS_PATH, headers=self.header, params=params)
            data = response.json()

            results = data.get("results", [])
            if not results:
                break

            us_cities = [
                loc for loc in results
                if "CITY:US" in loc["id"]
            ]
            
            all_cities.extend(us_cities)
            offset += 1000
            if not all:
                break

        return all_cities
    
    # input expects State Abbreviation
    def get_cities_by_state(self, state: Optional[str]):
        us_cities = self.get_all_us_cities()
        filtered = [loc for loc in us_cities
                    if f", {state} " in loc["name"]]

        return filtered