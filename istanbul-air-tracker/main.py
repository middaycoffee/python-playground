import datetime
import time
import requests
import os
import dotenv 
import database
import analyzer

# to create a .env file in the same directory
abs_path = os.path.abspath(__file__)
env_dir = os.path.dirname(abs_path)
env_loc = os.path.join(env_dir, ".env")


def track_air():
    print("extracting the stations")
    database.setup_database()

    
    st_input = input("Welcome to the Istanbul Air Quality Tracker. Write the name of the district you want to check (e.g. Tuzla, Kadıköy, Kartal): ")
    search_station(st_input)
        

def search_station(district):
    url = "https://api.ibb.gov.tr/havakalitesi/OpenDataPortalHandler/GetAQIStations"
    station = district.strip().capitalize()
    response = requests.get(url)
    data = response.json()

    station_id = ""
    for item in data:
        if station in item['Name']:
            station = item['Name']
            station_id = item['Id']
            dotenv.set_key(env_loc, "ACTIVE_STATION_ID", station_id)
            break
        elif data.index(item) == len(data)-1:
            print("Sorry, we couldn't find the district you've written in our database. Please try again.")
            return
    print(f"Station Name: {station}, Station ID: {station_id}")
    save_data(station, station_data(station_id))

def station_data(station_id):
    time_now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    now_f = time_now.strftime("%d.%m.%Y %H:%M:%S")
    now_f_1h = (time_now - datetime.timedelta(hours=1)).strftime("%d.%m.%Y %H:%M:%S")

    url = f"https://api.ibb.gov.tr/havakalitesi/OpenDataPortalHandler/GetAQIByStationId?StationId={station_id}&StartDate={now_f_1h}&EndDate={now_f}"

    response = requests.get(url)
    data = response.json()
    
    return data

def save_data(station, data):

    if len(data) > 0:
        latest_read = data[-1]
        database.insert_reading(station, latest_read)
        analysis = analyzer.generate_advice(station, latest_read)
        print(f"---The air quality analysis for the {station}---")
        print(analysis)

    else:
        print(f"Error! Data for the {station} is empty. Please try again later.")
        return

if __name__ == "__main__":
    track_air()