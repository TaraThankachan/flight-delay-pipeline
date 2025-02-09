import pandas as pd
import pymysql
from sqlalchemy import create_engine
import os

# MySQL connection details (Use environment variables for Docker)
db_user = os.getenv("MYSQL_USER", "root")
db_password = os.getenv("MYSQL_PASSWORD", "root")
db_host = os.getenv("MYSQL_HOST", "mysql")  # Matches the service name in docker-compose.yml
db_port = os.getenv("MYSQL_PORT", "3306")
db_name = os.getenv("MYSQL_DATABASE", "flight_data")

# Create connection
engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

# Read the raw CSV file from the landing zone
landing_path = "data/landing/flight_delays.csv"
df = pd.read_csv(landing_path)

# Bronze Layer: Save raw data to MySQL
df.to_sql("flight_delays_raw", engine, if_exists="replace", index=False)
print("Data ingested into Bronze Layer (MySQL).")

# Silver Layer: Apply filtering and store in MySQL
filtered_df = df[(df["ARRIVAL_DELAY"] > 60) & (df["DEPARTURE_DELAY"] > 60)]
filtered_df.to_sql("flight_delays_filtered", engine, if_exists="replace", index=False)
print("Filtered data saved to Silver Layer (MySQL).")
