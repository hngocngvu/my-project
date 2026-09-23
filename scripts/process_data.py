import json

processed= list()


if __name__ == "__main__":
    with open("data/json/flight_data.json", "r") as f:
        flight_data= json.load(f)

    with open("data/json/meteo_data.json", "r") as m:
        meteo_data= json.load(m)

    for flight in flight_data["data"]:
        combined= {
            "arrival": dict(),
            "departure": dict(),
        }
        combined["flight_date"]= flight["flight_date"]
        combined["flight_status"]= flight["flight_status"]

        combined["arrival"]["airport"]= flight["arrival"]["airport"]
        combined["arrival"]["timezone"]= flight["arrival"]["timezone"]
        combined["arrival"]["iata"]= flight["arrival"]["iata"]
        combined["arrival"]["scheduled"]= flight["arrival"]["scheduled"]
        combined["arrival"]["delay"]= flight["arrival"]["delay"]

        combined["departure"]["airport"]= flight["departure"]["airport"]
        combined["departure"]["timezone"]= flight["departure"]["timezone"]
        combined["departure"]["iata"]= flight["departure"]["iata"]
        combined["departure"]["scheduled"]= flight["departure"]["scheduled"]
        combined["departure"]["delay"]= flight["departure"]["delay"]

        processed.append(combined)

    for meteo in meteo_data:
        for c in processed:
            if c["arrival"]["iata"] == meteo["iata"]:
                c["arrival"]["data"] = meteo["meteo_data"]
            elif c["departure"]["iata"] == meteo["iata"]:
                c["departure"]["data"] = meteo["meteo_data"]
            else:
                continue
    
    with open("data/json/processed.json", "w") as f:
        json.dump(processed, f)




    