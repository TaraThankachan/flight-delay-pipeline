from dagster import job, op
import subprocess
import pandas as pd
from sqlalchemy import create_engine
import os

# MySQL connection settings
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
DB_HOST = os.getenv("MYSQL_HOST", "mysql")  # Docker container hostname
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DATABASE", "flight_data")

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)

@op
def ingest_data():
    """Loads flight delay CSV data into MySQL (Bronze Layer)."""
    df = pd.read_csv("data/landing/flight_delays.csv")
    df.to_sql("flight_delays_raw", engine, if_exists="replace", index=False)
    print("✅ Data ingested into Bronze Layer (MySQL).")

@op
def filter_data():
    """Filters data where arrival and departure delay > 1 hour (Silver Layer)."""
    df = pd.read_sql("SELECT * FROM flight_delays_raw", engine)
    filtered_df = df[(df["ARRIVAL_DELAY"] > 60) & (df["DEPARTURE_DELAY"] > 60)]
    filtered_df.to_sql("flight_delays_filtered", engine, if_exists="replace", index=False)
    print("✅ Filtered data saved to Silver Layer.")

@op
def run_dbt():
    """Runs dbt transformations to aggregate delays (Gold Layer)."""
    try:
        subprocess.run(["dbt", "run", "--project-dir", "dbt_project"], check=True)
        print("✅ dbt transformations completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ dbt failed: {e}")

@job
def flight_delay_pipeline():
    """Defines the Dagster job for the data pipeline."""
    ingest_data()
    filter_data()
    run_dbt()
