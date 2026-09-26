from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import (Float, Boolean, DateTime, String, Text, Integer)
load_dotenv("../.env")

DATABASE_URL= os.getenv("DATABASE_URL")
DB_USER= os.getenv("DB_USER")
DB_PW= os.getenv("DB_PW")
DB_IP= os.getenv("DB_IP")
DB_PORT= os.getenv("DB_PORT")
DB_NAME= os.getenv("DB_NAME")

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PW}@{DB_IP}:{DB_PORT}/{DB_NAME}")

flights= pd.read_csv("data/csv/flights.csv")
meteo= pd.read_csv("data/csv/meteo.csv")

# validation

flights["iata"]= flights["iata"].astype(str)
flights["timezone"]= flights["timezone"].astype(str)
flights["scheduled"]= pd.to_datetime(flights["scheduled"])
flights["airport"]= flights["airport"].astype(str)

meteo["iata"]= meteo["iata"].astype(str)
meteo["time"] = pd.to_datetime(meteo["time"])
meteo["temp_2m"]= meteo["temp_2m"].round(2)
meteo["humidity_2m"]= meteo["humidity_2m"].round(2)
meteo["weather_code"]= meteo["weather_code"].astype(int)
meteo["precipitation"]= meteo["precipitation"].round(2)
meteo["wind_speed_10m"]= meteo["wind_speed_10m"].round(2)
meteo["wind_direction_10m"]= meteo["wind_direction_10m"].round(2)
meteo["cloud_cover"]= meteo["cloud_cover"].round(2)
meteo["wind_gusts_10m"]= meteo["wind_gusts_10m"].round(2)
meteo["apparent_temp"]= meteo["apparent_temp"].round(2)

flights_dtype={
    "iata": String(3),
    "delay": Float,
    "timezone": String(50),
    "schedule": DateTime,
    "airport": Text,
    "arrival": Boolean
}

meteo_dtype={
    "iata": String(3),
    "time": DateTime,
    "temp_2m": Float,
    "humidity_2m": Float,
    "weather_code": Integer, 
    "precipitation": Float,
    "wind_speed_10m": Float,
    "wind_direction_10m": Float,
    "cloud_cover": Float,
    "wind_gusts_10m": Float,
    "apparent_temp": Float
}

if __name__ == "__main__":
    flights.to_sql("flights", engine, "flight_meteo", if_exists= "fail", index=False, method= "multi", dtype= flights_dtype)
    meteo.to_sql("meteo", engine, "flight_meteo", if_exists= "fail", index=False, method= "multi", dtype= meteo_dtype)

