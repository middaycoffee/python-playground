## What is this?
This repository serves as a playground where I test new tools, languages by building small sized projects.

### Projects Directory
Here is a quick overview of the experiments currently living in this repository:

#### [Istanbul Air Tracker](./istanbul-air-tracker)
An end-to-end data pipeline that extracts live air quality metrics from the Istanbul Metropolitan Municipality (IBB) Open Data Portal, stores historical data locally, and generates real-time public health analysis using Generative AI.
* **Core Tech:** Python, SQLite, Google Gemini API, REST APIs
* **Key Features:** ETL pipeline, parameterized SQL, dynamic LLM prompt engineering.

#### [Alien Invasion Game](./invasion_game)
A classic 2D arcade-style shooter built to explore game physics, event handling, and object-oriented design in Python.
* **Core Tech:** Python, Pygame
* **Key Features:** Player movement, collision detection, score and dashboard.

#### [ISS Tracker](./iss_tracker)
A script that pulls real-time geospatial data from a public API to track the current location of the International Space Station over the Earth.
* **Core Tech:** Python, requests, JSON
* **Key Features:** Live API polling, JSON parsing.

### Local Setup
If you want to pull this repository down and run any of these projects on your local machine, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/middaycoffee/python-playground.git
cd python-playground
```
2. Install required libraries (e.g., using pip):
```bash
pip install pygame requests
```
3. Run the projects directly:
```bash
# To play the game:
python invasion_game/main.py

# To track the ISS:
python iss_tracker/main.py
```
