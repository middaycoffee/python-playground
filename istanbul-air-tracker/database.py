import sqlite3

DB_NAME = "ist_air_parameters.db"

def setup_database():
    with sqlite3.connect(DB_NAME) as conn: 
        # only the indented codes goes to connected database

        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS parameters
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       district VARCHAR,
                       read_time DATE,
                       pm10 REAL,
                       so2 REAL,
                       o3 REAL,
                       no2 REAL,
                       co REAL,
                       aqi_index REAL,
                       cont_parameter VARCHAR)""")

def insert_reading(district_name, latest_read):

    read_time = latest_read['ReadTime'] 
    pm10 = latest_read["Concentration"]["PM10"]
    so2 = latest_read["Concentration"]["SO2"]
    o3 = latest_read["Concentration"]["O3"]
    no2 = latest_read["Concentration"]["NO2"]
    co = latest_read["Concentration"]["CO"]
    aqi_index = latest_read["AQI"]["AQIIndex"]
    contaminant_parameter = latest_read["AQI"]["ContaminantParameter"]

    with sqlite3.connect(DB_NAME) as conn: 
        # only the indented codes goes to connected database
        cursor = conn.cursor()
        # ? placeholders used to avoid quote mark confusion of f-string: f"""({district}) """ -> VALUES (Ümraniye)
        cursor.execute("""INSERT INTO parameters 
                       (district, read_time, pm10, so2, o3, no2, co, aqi_index, cont_parameter)
                       VALUES
                       (?,?, ?, ?, ?, ?, ?, ?, ?)""", 
                       (district_name, read_time, pm10, so2, o3, no2, co, aqi_index, contaminant_parameter))

    print(f"Air quality data of {district_name} is succesfully saved to your database: {DB_NAME}")