import os
import json
from dotenv import load_dotenv
import requests

geo_url= "https://airportsapi.com/api/airports/"
headers = {"Accept": "application/json"}

def get_data(url, headers):
    r= requests.get(url, headers=headers)
    return r.json()

if __name__ == "__main__":
    with open("data/flight_data.json", "r") as f:
        flight_data= json.load(f)
        
        airports= list()
        for flight in flight_data['data']:
            airport_dept= flight['departure']['iata']
            airport_arr= flight['arrival']['iata']
            if airport_dept in airports: 
                continue
            elif airport_arr in airports:
                continue
            else:
                airports.append(airport_dept)
                airports.append(airport_arr)

    print(airports)
    geo_data= list()
    for airport in airports:
        geo= get_data(geo_url + airport, headers)
        geo_data.append(geo["data"])

    with open(f"data/geo_data.json", "w") as f:
        json.dump(geo_data, f)
        


