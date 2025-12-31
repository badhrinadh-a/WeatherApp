import logging
from datetime import datetime, timezone, timedelta


log = logging.getLogger(__name__)
IST = timezone(timedelta(hours=5, minutes=30))

def transform_weather(**context):
    ti = context["ti"]
    raw_list = ti.xcom_pull(
        key="raw_weather_list",
        task_ids="extract_weather"
    )

    cleaned_rows = []

    for raw in raw_list:
        cleaned_rows.append({
            "city": raw["name"],
            "country": raw["sys"]["country"],
            "temperature": raw["main"]["temp"],
            "feels_like": raw["main"]["feels_like"],
            "humidity": raw["main"]["humidity"],
            "pressure": raw["main"]["pressure"],
            "wind_speed": raw["wind"]["speed"],
            "weather_main": raw["weather"][0]["main"],
            "weather_desc": raw["weather"][0]["description"],
            "timestamp_ist": datetime.fromtimestamp(
                raw["dt"], tz=timezone.utc
            ).astimezone(IST).isoformat()
        })

    ti.xcom_push(
        key="cleaned_weather_list",
        value=cleaned_rows
    )

    log.info(f"Transformed {len(cleaned_rows)} weather records")
