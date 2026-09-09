import requests
import os
from dotenv import load_dotenv
import json

load_dotenv("../.env")

aviation_api= os.getenv("AVIATION_API_KEY")
aviation_url= "https://api.aviationstack.com/v1/flights"


def get_data(url, api):
    params= {
        "api": api,
        "access_key": aviation_api
    }
    r= requests.get(url, params= params)
    return r.json()

if __name__ == "__main__":
    flight_data= get_data(aviation_url, aviation_api)
    with open("data/flight_data.json", "w") as f:
        json.dump(flight_data, f)
    
