import json

"""
pagination
data: flight_date, flight_status, departure, arrival, airline, flight, aircraft, live

crawl weather following arrival & departure schedules
"""
if __name__ == "__main__":
    with open("data/flight_data.json", "r") as f:
        flight_data= json.load(f)
    print(flight_data['data'][0]['departure'])