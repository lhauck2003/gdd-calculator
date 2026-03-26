# A class for holding a day's weather data
import time
from time import localtime, gmtime, strftime, struct_time
from typing import List, Dict, Optional, Union
from .weather_gov.weather_gov_client import WeatherRequest, StationRequest, GOVClient

class StationOptions:
    def __init__(self, latitude: int, longitude: int, client: GOVClient):
        self.latitude = latitude
        self.longitude = longitude
        self.client = client
        self.station_request: StationRequest = StationRequest(latitude=self.latitude, longitude=self.longitude)
        self.metadata = self.get_station_metadata()

    @property
    def city(self):
        return self.metadata["city"]

    @property
    def state(self):
        return self.metadata["state"]
    
    # returns list of stations
    def stations(self):
        return self.client.get_station_list(self.station_request, None)

    def get_station_metadata(self):
        index: int = self.client.add_to_requests(self.station_request)
        response = self.client.station_request(self.station_request)[index]
        return response["properties"]
    
class Station:
    def __init__(self, station_id, client: GOVClient):
        self.station_id = station_id
        self.client = client

    def get_todays_weather(self):
        pass

# holds a singular time_stamp's weather data
class WeatherInfo:
    def __init__(self, weather_data):
        self.properties = weather_data["properties"]
        self.station = weather_data["properties"]["station"]
        self.stationId = weather_data["properties"]["stationId"]
        self.stationName = weather_data["properties"]["stationName"]
        self.timestamp = weather_data["properties"]["timestamp"]
        self.rawMessage =  weather_data["properties"]["rawMessage"]
        self.textDescription = weather_data["properties"]["textDescription"]
        self.presentWeather = weather_data["properties"]["presentWeather"]
        self.temperature = weather_data["properties"].get("temperature", {})
        self.dewpoint = weather_data["properties"]["dewpoint"]
        self.windDirection = weather_data["properties"]["windDirection"]
        self.windSpeed = weather_data["properties"]["windSpeed"]
        self.windGust = weather_data["properties"]["windGust"]
        self.barometricPressure = weather_data["properties"]["barometricPressure"]
        self.seaLevelPressure = weather_data["properties"]["seaLevelPressure"]
        self.visibility = weather_data["properties"]["visibility"]
        self.maxTemperatureLast24Hours = weather_data["properties"]["maxTemperatureLast24Hours"]
        self.minTemperatureLast24Hours = weather_data["properties"]["minTemperatureLast24Hours"]
        #self.precipitationLastHour = weather_data["properties"]["precipitationLastHour"]
        #self.precipitationLast3Hours = weather_data["properties"]["precipitationLast3Hours"]
        #self.precipitationLast6Hours = weather_data["properties"]["precipitationLast6Hours"]
        #self.relativeHumidity = weather_data["properties"]["relativeHumidity"]
        #self.windChill = weather_data["properties"]["windChill"]
        #self.heatIndex = weather_data["properties"]["heatIndex"]
        #self.cloudLayers = weather_data["properties"]["cloudLayers"]
    
    @property
    def temp_high(self):
        if "maxValue" in self.temperature.keys():
            return self.temperature["maxValue"]
        else:
            return self.temperature["value"]

    @property
    def temp_low(self):
        if "minValue" in self.temperature.keys():
            return self.temperature["minValue"]
        return self.temperature["value"]
    
    @property
    def temp_avg(self):
        return self.temperature["value"]


class DailyWeatherRange:
    def __init__(
            self, 
            start_day: Union[str, Optional[struct_time]], 
            station_id: str, 
            client: GOVClient
        ):
        self.start_day = start_day #if isinstance(start_day, str) else strftime(start_day)
        self.curr_day = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
        self.client: GOVClient = client
        self.station = Station(station_id=station_id, client=self.client)
        self.weather_data = self.get_weather_data()
        self.daily_weather_list = self.get_daily_weather_list()

    @property
    def station_id(self):
        return self.station.station_id

    def __iter__(self):
        yield from self.daily_weather_list

    def get_daily_weather_list(self):
        daily_data: Dict[str, List[dict]] = {}

        for entry in self.weather_data:
            properties = entry.get("properties", {})
            timestamp = properties.get("timestamp")
            if not timestamp:
                continue

            # timestamp looks like 2026-03-24T00:00:00Z
            day = timestamp.split("T")[0]
            if day in daily_data:
                daily_data[day].append(entry)
            else:
                daily_data[day] = [entry]

        return [DayWeatherInfo(day_weather) for day_weather in daily_data.values()]

    def get_temperatures(self):
        return [entry.get_temperatures() 
                for entry in self.daily_weather_list]

    def get_weather_data(self):
        r: WeatherRequest = WeatherRequest(self.start_day, self.curr_day, cursor=None, limit=None, stationId=self.station_id)
        response = self.client.weather_request(r)
        return response
    
    def get_daily_temp_highs(self) -> List[int]:
        return [entry.get_temp_high() 
                for entry in self.daily_weather_list]

    def get_daily_temp_lows(self) -> List[int]:
        return [entry.get_temp_low() 
                for entry in self.daily_weather_list]

    def get_daily_temp_avg(self) -> List[int]:
        pass

# holds singular day weather info
class DayWeatherInfo:
    def __init__(self, weather_data):
        self.weather_data = weather_data
        self.weather_list: List[WeatherInfo] = self.get_weather_list()

    # TODO:
    # return the day if %Y-%M-%d format for the instance
    @property
    def day(self):
        pass
        
    def __iter__(self):
        yield from self.weather_list

    def get_temperatures(self):
        return [entry.temp_avg for entry in self.weather_list]

    def get_weather_list(self) -> List[WeatherInfo]:
        weather_list: List[WeatherInfo] = []
        for entry in self.weather_data:
            info = WeatherInfo(entry)
            weather_list.append(info)
        return weather_list

    def get_temp_high(self):
        return max([entry.temp_high for entry in self.weather_list if entry
                    if entry and entry.temp_high is not None])

    def get_temp_low(self):
        return min([entry.temp_low for entry in self.weather_list if entry
                    if entry and entry.temp_low is not None])

    def get_temp_avg(self):
        pass