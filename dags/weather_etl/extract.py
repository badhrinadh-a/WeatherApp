import os
import requests
import logging
from airflow.models import Variable

log = logging.getLogger(__name__)

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def extract_weather(**context):
    api_key = os.environ["OPENWEATHER_API_KEY"]  # env, not Variable

    city = Variable.get("WEATHER_CITY")
    country = Variable.get("WEATHER_COUNTRY")
    units = Variable.get("WEATHER_UNITS", default_var="metric")

    params = {
        "q": f"{city},{country}",
        "appid": api_key,
        "units": units
    }

    response = requests.get(OPENWEATHER_URL, params=params, timeout=10)
    response.raise_for_status()

    context["ti"].xcom_push(
        key="raw_weather",
        value=response.json()
    )
