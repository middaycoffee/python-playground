import time
import requests

def track_iss():
    print("Extracting the location...")

    # extraction from open-notify.org
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    data = response.json()

    # finding the location
    lat = data["iss_position"]["latitude"]
    long = data["iss_position"]["longitude"]
    timestamp = data["timestamp"]
    local_time = time.ctime(timestamp)
    maps = f"https://www.google.com/maps/search/?api=1&query={lat},{long}"

    # results
    print("We've succesfully extracted the current location of the International Space Station!")
    print("Time: ", local_time)
    print("Latitude: ", lat)
    print("Longitude ", long)
    print("View the location on maps: ", maps)

if __name__ == "__main__":
    track_iss()