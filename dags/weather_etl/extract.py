import os
import requests
import logging
from airflow.models import Variable

log = logging.getLogger(__name__)
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def extract_weather(**context):
    api_key = os.environ["OPENWEATHER_API_KEY"]
    units = Variable.get("WEATHER_UNITS", default_var="metric")

    cities = Variable.get("WEATHER_CITIES", deserialize_json=True)

    results = []

    for item in cities:
        city = item["city"]
        country = item["country"]

        params = {
            "q": f"{city},{country}",
            "appid": api_key,
            "units": units
        }

        response = requests.get(OPENWEATHER_URL, params=params, timeout=10)
        response.raise_for_status()

        results.append(response.json())

        log.info(f"Fetched weather for {city}")

    context["ti"].xcom_push(
        key="raw_weather_list",
        value=results
    )
