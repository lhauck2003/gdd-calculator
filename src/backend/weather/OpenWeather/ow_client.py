import os
from typing import Optional, Union, List
from time import strftime, strptime, struct_time, mktime
from datetime import datetime
import requests
from .urls import OPENWEATHER_API_BASE, OPENWEATHER_API_DAILY_AGG, OPENWEATHER_API_HISTORICAL
from .utils import is_valid_format

class OpenWeatherClient:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")

    # ------------------------------
    # Basic API Calls
    # ------------------------------
    # lat
    # lon
    # appid
    # exclude
    # units
    # lang
    def fetch_current_weather(
            self,
            lat: Optional[float] = None, # required
            lon: Optional[float] = None, # required
            exclude: Optional[List[str]] = None,
            units: Optional[str] = "imperial", # default is F
            lang: Optional[str] = None
            ):
        if lat is None or lon is None:
            raise Exception("Must specify location")
        
        # get params
        params = {}
        params["lat"] = lat
        params["lon"] = lon

        if units is not None:
            params["units"] = units
        if lang is not None:
            params["lang"] = lang

        if exclude is not None and not exclude==[]:
            exclude_list = f"{exclude[0]}"
            i = 1
            while exclude[i]:
                exclude_list+=f",{exclude[i]}"
                i+=1
            params["exclude"] = exclude_list

        params["appid"] = self.api_key

        response = requests.get(OPENWEATHER_API_BASE,
                                params=params)
        response.raise_for_status()
        response_data = response.json()
        return response_data    

    # lat
    # lon
    # appid
    # dt
    # units
    # lang
    def fetch_historical_weather_timestamp(
            self,
            lat: Optional[float] = None, # required
            lon: Optional[float] = None, # required
            dt: Union[Optional[str], Union[struct_time, float]] = None, # required
            dt_format: Optional[str] = None, # required if dt is string
            units: Optional[str] = "imperial", # default is F
            lang: Optional[str] = None
            ):
        if lat is None or lon is None:
            raise Exception("Must specify location")
        if dt is None:
            raise Exception("Must specify datetime in timestamp")
        
        if isinstance(dt, str):
            if dt_format is None:
                raise Exception("Must specify format with Date string")
            dt = mktime(strptime(dt, dt_format))
        elif isinstance(dt,struct_time):
            dt = mktime(dt)

        # get params
        params = {}
        params["lat"] = lat
        params["lon"] = lon
        params["dt"] = dt

        if units is not None:
            params["units"] = units
        if lang is not None:
            params["lang"] = lang

        params["appid"] = self.api_key

        response = requests.get(OPENWEATHER_API_HISTORICAL,
                                params=params)
        response.raise_for_status()
        response_data = response.json()
        return response_data

    # INPUTS: lat, lon, appid, date, units,lang
    # OUPUT FIELDS: see urls
    def fetch_daily_aggregation_weather(
            self,
            lat: Optional[float] = None, # required
            lon: Optional[float] = None, # required
            date: Union[Optional[str], struct_time] = None, # required
            units: Optional[str] = "imperial", # default is F
            lang: Optional[str] = None
            ):
        if lat is None or lon is None:
            raise Exception("Must specify location")
        if date is None:
            raise Exception("Must specify day YYYY-MM-DD")
        
        if isinstance(date, struct_time):
            date = strftime("%Y-%m-%d", date)
        elif not is_valid_format(date):
            # ensure in YYYY-MM-DD format
            raise Exception("Date string must be in YYYY-MM-DD format")
        
        # get params
        params = {}
        params["lat"] = lat
        params["lon"] = lon
        params["date"] = date

        if units is not None:
            params["units"] = units
        if lang is not None:
            params["lang"] = lang

        params["appid"] = self.api_key
        
        response = requests.get(OPENWEATHER_API_DAILY_AGG,
                                params=params)
        response.raise_for_status()
        response_data = response.json()
        return response_data
    
