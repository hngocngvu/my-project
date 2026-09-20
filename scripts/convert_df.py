import json 
import pandas as pd
import numpy as np
with open("data/processed.json", "r") as f:
    data= json.load(f)

"""
Flight: iata, arrival (True/False), status, date, timezone, scheduled, airport

Meteo: iata, time, temp_2m, humidity_2m, weather_code, precipitation, wind_speed_10m, wind_direction_10m, cloud_cover, wind_gusts_10m, apparent_temp

Weather_code: code, text
"""

columns_arrival_departure= ["iata", "delay", "timezone", "scheduled", "airport"]

columns_meteo= ["iata", "time", "temp_2m", "humidity_2m", "weather_code", "precipitation", "wind_speed_10m", "wind_direction_10m", "cloud_cover", "wind_gusts_10m", "apparent_temp"]

def clean_text(txt):
    return txt.replace("\r", "").replace("\n","").strip()

def convert_arrival_departure(data, columns):
    arrival= list()
    departure= list()

    for flight in data: 
        row1= dict()
        row2= dict()
        row1["iata"]= str(flight["arrival"]["iata"])
        row1["delay"]= np.nan if flight["arrival"]["delay"] is None else float(flight["arrival"]["delay"])
        row1["scheduled"]= flight["arrival"]["scheduled"]
        row1["timezone"]= flight["arrival"]["timezone"]
        row1["airport"]= clean_text(str((flight["arrival"]["airport"])))
        arrival.append(row1)

        row2["iata"]= str(flight["departure"]["iata"])
        row2["delay"]= np.nan if flight["departure"]["delay"] is None else float(flight["departure"]["delay"])
        row2["scheduled"]= flight["departure"]["scheduled"]
        row2["timezone"]= flight["departure"]["timezone"]
        row2["airport"]= clean_text(str((flight["departure"]["airport"])))
        departure.append(row2)

    df1= pd.DataFrame(arrival, columns=columns)
    df1["arrival"]= True
    df2= pd.DataFrame(departure, columns=columns)
    df2["arrival"]= False

    flight= pd.concat([df1, df2], axis= 0, ignore_index= True)
    flight= flight.drop_duplicates()

    return flight

def convert_meteo(data, columns):
    arrival= list() #arrival
    dept= list() # departure
    for flight in data:
        if "data" not in flight["arrival"].keys():
            continue

        for i in range(0,24):
            row1= [flight["arrival"]["iata"],
            flight["arrival"]["data"]["date"][i], 
            flight["arrival"]["data"]["temperature_2m"][i],
            flight["arrival"]["data"]["relative_humidity_2m"][i],
            flight["arrival"]["data"]["weather_code"][i],
            flight["arrival"]["data"]["precipitation"][i],
            flight["arrival"]["data"]["wind_speed_10m"][i],
            flight["arrival"]["data"]["wind_direction_10m"][i],
            flight["arrival"]["data"]["cloud_cover"][i],
            flight["arrival"]["data"]["wind_gusts_10m"][i],
            flight["arrival"]["data"]["apparent_temperature"][i]
            ]

            arrival.append(row1)


        for i in range(len(flight["departure"]["data"]["date"])):
            row2= [flight["departure"]["iata"],
            flight["departure"]["data"]["date"][i], 
            flight["departure"]["data"]["temperature_2m"][i],
            flight["departure"]["data"]["relative_humidity_2m"][i],
            flight["departure"]["data"]["weather_code"][i],
            flight["departure"]["data"]["precipitation"][i],
            flight["departure"]["data"]["wind_speed_10m"][i],
            flight["departure"]["data"]["wind_direction_10m"][i],
            flight["departure"]["data"]["cloud_cover"][i],
            flight["departure"]["data"]["wind_gusts_10m"][i],
            flight["departure"]["data"]["apparent_temperature"][i]
            ]

            dept.append(row2)

    meteo= pd.DataFrame(columns= columns)
    a= pd.DataFrame(arrival, columns= columns)
    d= pd.DataFrame(dept, columns= columns)
    meteo= pd.concat([a, d], ignore_index=True, axis=0)
    meteo= meteo.drop_duplicates()
    return meteo


if __name__ == "__main__":
    import os
    os.makedirs("data/csv", exist_ok= True)

    flights= convert_arrival_departure(data, columns_arrival_departure)
    print(flights.iloc[45])
    flights.to_csv("data/csv/flights.csv", index= False)

    meteo= convert_meteo(data, columns_meteo)
    print(meteo.iloc[0])
    meteo.to_csv("data/csv/meteo.csv", index= False)



    


