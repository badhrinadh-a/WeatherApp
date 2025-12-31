import logging
import os
import psycopg2

log = logging.getLogger(__name__)

def ensure_table_exists(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id BIGSERIAL PRIMARY KEY,
            city TEXT NOT NULL,
            country TEXT NOT NULL,
            temperature REAL,
            feels_like REAL,
            humidity INTEGER,
            pressure INTEGER,
            wind_speed REAL,
            weather_main TEXT,
            weather_desc TEXT,
            timestamp_ist TIMESTAMP NOT NULL,
            CONSTRAINT uq_weather_city_time UNIQUE (city, timestamp_ist)
        )
    """)

def load_weather(**context):
    ti = context["ti"]
    data = ti.xcom_pull(key="cleaned_weather", task_ids="transform_weather")

    conn = psycopg2.connect(
        host=os.environ["WEATHER_DB_HOST"],
        database=os.environ["WEATHER_DB_NAME"],
        user=os.environ["WEATHER_DB_USER"],
        password=os.environ["WEATHER_DB_PASSWORD"],
        port=int(os.environ.get("WEATHER_DB_PORT", 5432)),
    )

    cur = conn.cursor()
    ensure_table_exists(cur)
    cur.execute("""
        INSERT INTO weather_data (
            city, country, temperature, feels_like,
            humidity, pressure, wind_speed,
            weather_main, weather_desc, timestamp_ist
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (city, timestamp_ist) DO NOTHING
    """, (
        data["city"],
        data["country"],
        data["temperature"],
        data["feels_like"],
        data["humidity"],
        data["pressure"],
        data["wind_speed"],
        data["weather_main"],
        data["weather_desc"],
        data["timestamp_ist"],
    ))

    conn.commit()
    cur.close()
    conn.close()
