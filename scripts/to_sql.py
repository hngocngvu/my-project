from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv("../.env")

DATABASE_URL= os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

flights= pd.read_csv("data/csv/flights.csv")
meteo= pd.read_csv("data/csv/meteo.csv")

if __name__ == "__main__":
    print(flights.info())
    print(meteo.info())