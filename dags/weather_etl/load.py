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
    records = ti.xcom_pull(
        key="cleaned_weather_list",
        task_ids="transform_weather"
    )

    conn = psycopg2.connect(
        host=os.environ["WEATHER_DB_HOST"],
        database=os.environ["WEATHER_DB_NAME"],
        user=os.environ["WEATHER_DB_USER"],
        password=os.environ["WEATHER_DB_PASSWORD"],
        port=int(os.environ.get("WEATHER_DB_PORT", 5432)),
    )

    cur = conn.cursor()
    ensure_table_exists(cur)

    insert_sql = """
            INSERT INTO weather_data (
                city, country, temperature, feels_like,
                humidity, pressure, wind_speed,
                weather_main, weather_desc, timestamp_ist
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (city, timestamp_ist) DO NOTHING
        """

    values = [
        (
            d["city"], d["country"], d["temperature"],
            d["feels_like"], d["humidity"], d["pressure"],
            d["wind_speed"], d["weather_main"],
            d["weather_desc"], d["timestamp_ist"]
        )
        for d in records
    ]

    cur.executemany(insert_sql, values)

    conn.commit()
    cur.close()
    conn.close()
