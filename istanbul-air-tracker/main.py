import datetime
import time
import requests
import os
import dotenv 
import database
import analyzer
import logging
from logging import config

# Set up logger
logging.basicConfig(
    filename = "app.log",
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(module)s - %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
    encoding = 'utf-8'
)

# Mute third-party libraries
config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True
})

# to create a .env file in the same directory
abs_path = os.path.abspath(__file__)
env_dir = os.path.dirname(abs_path)
env_loc = os.path.join(env_dir, ".env")


def track_air():
    logging.info("Starting station extraction process.")
    database.setup_database()

    
    st_input = input("Welcome to the Istanbul Air Quality Tracker. Write the name of the district you want to check (e.g. Tuzla, Kadıköy, Kartal): ")
    search_station(st_input)
        

def search_station(district: str) -> None:
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
            logging.warning(f"Input station not found: {station}")
            print(f"ERROR: input station {station} not found. Please try again later.")
            return
    logging.info(f"Located Station: {station}, Station ID: {station_id}")
    save_data(station, station_data(station_id))

def station_data(station_id: str) -> list:
    time_now = datetime.datetime.now()
    if time_now.minute < 15:
        end_t = time_now.replace(minute=0, second=0, microsecond=0) - datetime.timedelta(hours=1)
    else:
        end_t = time_now.replace(minute=0, second=0, microsecond=0)

    start_t = end_t - datetime.timedelta(hours=1)

    # format

    start_t = start_t.strftime("%d.%m.%Y %H:%M:%S")
    end_t = end_t.strftime("%d.%m.%Y %H:%M:%S")

    url = f"https://api.ibb.gov.tr/havakalitesi/OpenDataPortalHandler/GetAQIByStationId?StationId={station_id}&StartDate={start_t}&EndDate={end_t}"

    response = requests.get(url)
    data = response.json()
    
    return data

def save_data(station: str, data: list) -> None:

    if len(data) > 0:
        latest_read = data[-1]
        if latest_read.get("Concentration") is None:
            logging.info(f"Error: Concentration metricts of {station} missing.")
            print(f"Error! Data for the {station} is empty. Please try again later.")
            return          

        database.insert_reading(station, latest_read)
        analysis = analyzer.generate_advice(station, latest_read)
        print(f"---The air quality analysis for the {station}---")
        print(analysis)

    else:
        logging.info(f"Error: Empyt list with {station} station.")
        print(f"Error! Data for the {station} is empty. Please try again later.")
        return

if __name__ == "__main__":
    track_air()