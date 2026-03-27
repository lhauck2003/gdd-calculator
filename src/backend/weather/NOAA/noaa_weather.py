from typing import Optional, Union, List, Dict
import time
from datetime import datetime, date, timedelta
from .noaa_client import NOAAClient
from .cache.states import states
from .utils import active_date, get_stateid_by_abbr, get_stateid_by_state

STATES = states.get("results", [])


class NOAAInterface:
    def __init__(self, client: NOAAClient):
        self.client = client

    def check_station(self, stationid: Optional[str]) -> bool:
        check = self.client.stations(stationid=stationid)
        return check["id"] == stationid

    def search_stations_by_lat_long(
            self, 
            lat:Optional[float], 
            long: Optional[float], 
            radius: Optional[float],
            datasetid: Optional[str]="GHCND", 
            active: Optional[bool]=True
        ):
        if lat is None or long is None:
            raise Exception("Must specify coordinates")
        
        min_lat = round(lat - radius,4)
        min_long = round(long - radius,4)
        max_lat = round(lat + radius,4)
        max_long = round(long + radius,4)

        if active:
            startdate = active_date()
        else:
            startdate=None

        result = self.client.stations(extent=(min_lat,min_long,max_lat,max_long),
                                      startdate=startdate,
                                      datasetid=datasetid)
        
        return result
        
    def search_data_by_station(
            self,
            stationid: Optional[str],
            startdate: Optional[str],
            enddate: Optional[str],
            units: Optional[str],
            datasetid: Optional[str] = "GHCND"
    ):
        start = time.strptime(startdate, "%Y-%m-%d")
        end = time.strptime(enddate, "%Y-%m-%d")

        start_date = datetime(*start[:6])
        end_date = datetime(*end[:6])

        start = start_date.date()
        end = end_date.date()

        if (end - start).days <= 50:
            return {"results" : self.client.data(datasetid=datasetid,
                                    stationid=stationid,
                                    startdate=startdate,
                                    enddate=enddate,
                                    units=units,
                                    limit=1000)["results"]}

        combined_results = []
        current_start = start
        while current_start <= end:
            current_end = min(current_start + timedelta(days=49), end)
            chunk_result = self.client.data(
                datasetid=datasetid,
                stationid=stationid,
                startdate=current_start.isoformat(),
                enddate=current_end.isoformat(),
                units=units,
                limit=1000
            )
            combined_results.extend(chunk_result.get("results", []))
            current_start = current_end + timedelta(days=1)
        
        return {"results": combined_results}

    def search_stations_by_state(
        self,
        state: Optional[str],
        active: Optional[bool] = True,
        datasetid: Optional[str]= "GHCND",
        limit: Optional[int] = 1000
    ):
        states = [item.get("name", "") for item in STATES]
        i = states.index(state)

        stateid = STATES[i].get("id", "")

        if active:
            startdate = active_date()
        else:
            startdate=None

        
        result = self.client.stations(
            locationid=stateid,
            startdate=startdate,
            datasetid=datasetid,
            limit=limit
        )

        return result
    
    def search_cities_by_state(
        self,
        stateid: Optional[str],
        active: Optional[bool] = True,
        limit: Optional[int] = 1000
    ):
        if active:
            startdate = active_date()
        else:
            startdate=None

        result = self.client.locations(
            stateid=stateid,
            locationcategoryid="CITY",
            startdate=startdate,
            limit=limit
        )
    
    def search_stations_by_city(
            self,
            cityid: Optional[str],
            active: Optional[bool] = True,
            datasetid: Optional[str] = "GHCND",
            limit: Optional[int] = 1000
    ):
        if active:
            startdate = active_date()
        else:
            startdate=None

        result = self.client.stations(
            locationid=cityid,
            startdate=startdate,
            datasetid=datasetid,
            limit=limit
        )
        return result
    
    def get_all_us_cities(self, all:bool=True):
        return self.client.get_all_us_cities()

    def get_cities_by_state(self, state: Optional[str]):
        return self.client.get_cities_by_state(state)