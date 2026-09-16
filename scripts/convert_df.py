import json 
import pandas as pd

with open("data/processed.json", "r") as f:
    data= json.load(f)

# schema flight
info = pd.DataFrame(columns= ["iata_arrival", "iata_departure", "date", "status"])
airport= pd.DataFrame(columns= ["iata", "name"])
arrival_departure= pd.DataFrame(columns=["iata", "airport", "timezone", "scheduled", "delay"])

# schema meteo


apparent_temperature= pd.DataFrame(columns= columns)
cloud_cover= pd.DataFrame(columns= columns)


