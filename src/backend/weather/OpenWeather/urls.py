OPENWEATHER_API_BASE = "https://api.openweathermap.org/data/3.0/onecall"

# lat,required, Latitude, decimal (-90; 90). If you need the geocoder to automatic convert city names and zip-codes to geo coordinates and the other way around, please use our Geocoding API
# 
# lon, required, Longitude, decimal (-180; 180). If you need the geocoder to automatic convert city names and zip-codes to geo coordinates and the other way around, please use our Geocoding API
# 
# appid,  required, Your unique API key (you can always find it on your account page under the "API key" tab)
# 
# exclude, optional, By using this parameter you can exclude some parts of the weather data from the API response. It should be a comma-delimited list (without spaces). Available values: current minutely hourly daily alerts
# 
# units, optional, Units of measurement. standard, metric and imperial units are available. If you do not use the units parameter, standard units will be applied by default. Learn more
# 
# lang, optional, You can use the lang parameter to get the output in your language. Learn more

OPENWEATHER_API_HISTORICAL = OPENWEATHER_API_BASE + "/timemachine"
# lat,required, Latitude, decimal (-90; 90). If you need the geocoder to automatic convert city names and zip-codes to geo coordinates and the other way around, please use our Geocoding API
# 
# lon, required, Longitude, decimal (-180; 180). If you need the geocoder to automatic convert city names and zip-codes to geo coordinates and the other way around, please use our Geocoding API
# 
# appid,  required, Your unique API key (you can always find it on your account page under the "API key" tab)
# 
# dt, required, Timestamp (Unix time, UTC time zone), e.g. dt=1586468027. Data is available from January 1st, 1979 till 4 days ahead
# 
# units, optional, Units of measurement. standard, metric and imperial units are available. If you do not use the units parameter, standard units will be applied by default. Learn more
# 
# lang, optional, You can use the lang parameter to get the output in your language. Learn more

OPENWEATHER_API_DAILY_AGG = OPENWEATHER_API_BASE + "/day_summary"
# lat,required, Latitude, decimal (-90; 90). If you need the geocoder to automatic convert city names and zip-codes to geo coordinates and the other way around, please use our Geocoding API
# 
# lon, required, Longitude, decimal (-180; 180). If you need the geocoder to automatic convert city names and zip-codes to geo coordinates and the other way around, please use our Geocoding API
# 
# appid,  required, Your unique API key (you can always find it on your account page under the "API key" tab)
# 
# date, required, required, Date in the `YYYY-MM-DD` format for which data is requested. Date is available for 447+ years archive (starting from 1979-01-02) up to the 1,5 years ahead forecast to the current date
#
# units, optional, Units of measurement. standard, metric and imperial units are available. If you do not use the units parameter, standard units will be applied by default. Learn more
# 
# lang, optional, You can use the lang parameter to get the output in your language. Learn more
