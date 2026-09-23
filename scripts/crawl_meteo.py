import json
import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd 

"""
This script follows open-meteo document
temperature_2m: Temperature at 2 meters above ground level
relative_humidity_2m: Relative humidity at 2 meters above ground level
weather_code: Weather code (e.g., clear, cloudy, rain, snow)
precipitation: Total precipitation (rain + snow) in millimeters
wind_speed_10m: Wind speed at 10 meters above ground level
wind_direction_10m: Wind direction at 10 meters above ground level
cloud_cover: Cloud cover percentage
wind_gusts_10m: Wind gusts at 10 meters above ground level- gio giat
apparent_temperature: Apparent temperature (feels like)

"""
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)


meteo_url= "https://archive-api.open-meteo.com/v1/archive"

def get_data(url, lat, lon, start= "2026-09-12", end= "2026-09-12"):
    params= {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "relative_humidity_2m", "weather_code", "precipitation", "wind_speed_10m", "wind_direction_10m", "cloud_cover", "wind_gusts_10m", "apparent_temperature"],
        "start_date": start, 
        "end_date": end,
        "timeformat": "unixtime",

    }
    r= openmeteo.weather_api(url, params = params)

    return r[0]

if __name__ == "__main__":
    with open ("data/geo_data.json") as f:
        geo_data= json.load(f)

    geo_info_list= list()
    for geo in geo_data:
        geo_info= dict()
        
        geo_info["name"]= geo["attributes"]["name"]
        geo_info["lat"]= geo["attributes"]["latitude"]
        geo_info["lon"]= geo["attributes"]["longitude"]
        geo_info["iata"]= geo["attributes"]["iata_code"]
        geo_info_list.append(geo_info.copy())

    meteo= list()
    for geo_info in geo_info_list:
        response= get_data(meteo_url, geo_info["lat"], geo_info["lon"])
        hourly = response.Hourly()
        hourly_time = hourly.Time()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy().tolist()
        hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy().tolist()
        hourly_weather_code = hourly.Variables(2).ValuesAsNumpy().tolist()
        hourly_precipitation = hourly.Variables(3).ValuesAsNumpy().tolist()
        hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy().tolist()
        hourly_wind_direction_10m = hourly.Variables(5).ValuesAsNumpy().tolist()
        hourly_cloud_cover = hourly.Variables(6).ValuesAsNumpy().tolist()
        hourly_wind_gusts_10m = hourly.Variables(7).ValuesAsNumpy().tolist()
        hourly_apparent_temperature = hourly.Variables(8).ValuesAsNumpy().tolist()

        hourly_data= dict()

        hourly_data = {
        "date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        ).astype(str).tolist()
        }

        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
        hourly_data["weather_code"] = hourly_weather_code
        hourly_data["precipitation"] = hourly_precipitation
        hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
        hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
        hourly_data["cloud_cover"] = hourly_cloud_cover
        hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
        hourly_data["apparent_temperature"] = hourly_apparent_temperature

        m= dict()

        m["name"]= geo_info["name"]
        m["iata"]= geo_info["iata"]
        m["meteo_data"]= hourly_data

        meteo.append(m.copy())

    with open("data/json/meteo_data.json", "w") as f:
        json.dump(meteo, f)
