import logging
from datetime import datetime, timezone, timedelta

log = logging.getLogger(__name__)

# Define IST timezone (UTC +5:30)
IST = timezone(timedelta(hours=5, minutes=30))

def transform_weather(**context):
    """
    Transforms raw OpenWeatherMap JSON
    into analytics-ready structure
    """

    ti = context["ti"]
    raw = ti.xcom_pull(
        key="raw_weather",
        task_ids="extract_weather"
    )

    cleaned = {
        "city": raw["name"],
        "country": raw["sys"]["country"],
        "temperature": raw["main"]["temp"],
        "feels_like": raw["main"]["feels_like"],
        "humidity": raw["main"]["humidity"],
        "pressure": raw["main"]["pressure"],
        "wind_speed": raw["wind"]["speed"],
        "weather_main": raw["weather"][0]["main"],
        "weather_desc": raw["weather"][0]["description"],

        #convert IST datetime → STRING (XCom-safe)
        "timestamp_ist": datetime.fromtimestamp(
            raw["dt"],
            tz=timezone.utc
        ).astimezone(IST).isoformat()
    }

    ti.xcom_push(
        key="cleaned_weather",
        value=cleaned
    )

    log.info("Weather data transformed successfully (IST as string)")
