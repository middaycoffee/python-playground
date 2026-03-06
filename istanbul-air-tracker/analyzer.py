import os 
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_advice(district, latest_read):

    read_time = latest_read['ReadTime'] 
    pm10 = latest_read["Concentration"]["PM10"]
    so2 = latest_read["Concentration"]["SO2"]
    o3 = latest_read["Concentration"]["O3"]
    no2 = latest_read["Concentration"]["NO2"]
    co = latest_read["Concentration"]["CO"]
    aqi_index = latest_read["AQI"]["AQIIndex"]
    contaminant_parameter = latest_read["AQI"]["ContaminantParameter"]

    prompt = f"""(English) Act as a environmental health expert working on behalf of the public good in Istanbul. 
    You have the air data of Istanbul Metropolitan Municipality for the district {district}.
    The current air quality is driven primarily by {contaminant_parameter} with an AQI Index of {aqi_index}.
    And some of the *raw* metrics are:
    PM10: {pm10},
    SO2: {so2},
    O3: {o3},
    NO2: {no2},
    CO: {co}.

    Provide the citizen reading your answer a brief explanation of the air quality (not too technical),
    and a piece of health or activity advice.

    The answer format should be: 'Air quality analyses for Istanbul, {district} at {read_time} (just month, day, hour, and minute):
    General explanation
    Some technical details and metrics (what is pm10 in simple terms, or other contaminent parameter given)
    advices on activities
    have a nice day'
""" 
    response = client.models.generate_content(
        model = 'gemini-2.5-flash',
        contents = prompt
    )

    return response.text