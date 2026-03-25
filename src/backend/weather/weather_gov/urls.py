NOAA_API_URL = "https://api.weather.gov"

SEARCH_BY_LAT_LONG_URL = NOAA_API_URL + "/points/%.4f,%.4f" # expects Latitude, Longitude

SEARCH_BY_STATION_ID_URL = NOAA_API_URL + "/stations/%s/observations" # expects station_ID
# PARAMETERS
# - start: string($date-time) (expected format YYYY-MM-DDThh:mm:ssZ or YYYY-MM-DDThh:mm:ss+hh:mm")
# - end string($date-time) (expected format YYYY-MM-DDThh:mm:ssZ or YYYY-MM-DDThh:mm:ss+hh:mm")
# - cursor: string - Pagination cursor
# - limit: integer
# - stationId: string - REQUIRED

SEARCH_BY_GRID_ID = NOAA_API_URL + "/gridpoints/%s/%d,%d/stations"

