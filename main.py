from enum import Enum
import json
import os


class County(Enum):
    NAME = 0
    SEAT = 1
    PREFIX = 2


def load_cites_and_counties():
    """
    Loads all saved montana cities and counties
    """
    cities = {}
    counties = []
    if os.path.exists("cities.json"):
        with open("cities.json", "r") as file:
            cities = json.load(file)
            counties = list(cities.values())
        return cities, counties

    if os.path.exists("MontanaCounties.csv"):
        with open("MontanaCounties.csv", "r") as file:
            lines = file.readlines()[1:]
            counties = []
            for line in lines:
                line = line.strip().split(",")
                cities[line[County.SEAT.value].lower()] = line[County.NAME.value]
                counties.append(line[County.NAME.value])
        return cities, counties

    print("The MontanaCounties.csv file is missing. Please download the file "
          "from Github and place it in the same directory as this script.")
    exit()


cities, counties = load_cites_and_counties()

# UI Loop
while True:
    city = input("Enter a city (leave blank to quit): ")

    # Exit condition
    if city == "":
        break

    # The city isn't saved, ask for county
    county = cities.get(city.lower(), None)
    if county is None:
        while not county:
            county = input("Enter a county: ")
            # Clean up the input a bit
            county = county.replace(" County", "")
            county = county.replace(" county", "")
            # Check if the county exists
            if county not in counties:
                print("Please enter a valid Montana county")
                # Prevent the loop from exiting, we still don't have a valid county
                county = None
                continue
        cities[city.lower()] = county
        with open("cities.json", "w") as file:
            json.dump(cities, file, indent=2)
    else:
        # The city exists, print it
        print(cities[city.lower()])

    print()
