# Flight Delay Data Pipeline

This project builds a **Dockerized data processing pipeline** for analyzing flight delay data using **MySQL, dbt, and Python**. It follows the **Medallion Architecture (Bronze → Silver → Gold)** for efficient data transformation.

## 🚀 Features
- **Raw data ingestion (Bronze Layer) → MySQL**
- **Data Cleaning & Filtering (Silver Layer) → dbt**
- **Aggregated Analysis (Gold Layer) → dbt**
- **Dockerized pipeline with `docker-compose`**

---

## 📂 Project Structure
```
flight-delay-pipeline/
│── dbt_project/                 # dbt models (Silver & Gold layers)
│   ├── models/
│   │   ├── bronze/
│   │   │   ├── stg_raw_flight_delays.sql
│   │   ├── silver/
│   │   │   ├── silver_filtered_flight_delays.sql
│   │   ├── gold/
│   │   │   ├── gold_aggregated_flight_delays.sql
│── data/                        # Raw CSV files
│── processing.py                 # Python script to load raw data into MySQL
│── docker-compose.yml             # Docker setup
│── Dockerfile                     # Python environment setup
│── README.md                      # Documentation
```

---

## 🛠️ Setup Instructions

### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/your-repo/flight-delay-pipeline.git
cd flight-delay-pipeline
```

### 2️⃣ **Update the `.env` File (MySQL Credentials)**
Create a `.env` file in the root directory:
```ini
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=flight_delays
MYSQL_USER=user
MYSQL_PASSWORD=password
```

### 3️⃣ **Run the Pipeline (Dockerized)**
```sh
docker-compose up --build
```
This will:
✅ Start **MySQL**
✅ Load **raw flight delay data** into MySQL
✅ Run **dbt transformations (Silver & Gold layers)**

### 4️⃣ **Verify Results in MySQL**
Access the MySQL container:
```sh
docker exec -it mysql-db mysql -uuser -ppassword flight_delays
```
Run queries:
```sql
SELECT * FROM gold_aggregated_flight_delays LIMIT 10;
```

---

## 🛠️ MySQL Table Structure

### **Bronze Layer (Raw Data - `flight_delays_raw`)**
```sql
CREATE TABLE flight_delays_raw (
    flight_date DATE,
    airline VARCHAR(255),
    origin_airport VARCHAR(10),
    destination_airport VARCHAR(10),
    departure_delay INT,
    arrival_delay INT
);
```

### **Silver Layer (Filtered Data - `silver_filtered_flight_delays`)**
```sql
SELECT * FROM flight_delays_raw
WHERE departure_delay IS NOT NULL AND arrival_delay IS NOT NULL
AND (departure_delay > 5 OR arrival_delay > 5);
```

### **Gold Layer (Aggregated Data - `gold_aggregated_flight_delays`)**
```sql
SELECT 
    airline,
    origin_airport,
    COUNT(*) AS total_flights,
    AVG(departure_delay) AS avg_departure_delay,
    AVG(arrival_delay) AS avg_arrival_delay,
    SUM(CASE WHEN departure_delay > 60 THEN 1 ELSE 0 END) AS delayed_departures,
    SUM(CASE WHEN arrival_delay > 60 THEN 1 ELSE 0 END) AS delayed_arrivals
FROM silver_filtered_flight_delays
GROUP BY airline, origin_airport;
```

---

## 🏗️ Docker Compose Setup

### **`docker-compose.yml` (Simplified)**
```yaml
services:
  mysql-db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      - MYSQL_DATABASE=${MYSQL_DATABASE}
      - MYSQL_USER=${MYSQL_USER}
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  dbt:
    image: ghcr.io/dbt-labs/dbt-mysql:latest
    volumes:
      - ./dbt_project:/usr/app/dbt
    command: ["dbt", "run"]
    depends_on:
      - mysql-db
      - python-app

  python-app:
    build: .
    volumes:
      - .:/usr/src/app
    working_dir: /usr/src/app
    command: ["python", "processing.py"]
    depends_on:
      - mysql-db

volumes:
  mysql_data:
```

---

## 📌 Running dbt Manually
If you need to run dbt transformations manually, use:
```sh
docker-compose run dbt dbt run
```

To check dbt logs:
```sh
docker-compose logs dbt
```

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 📩 Need Help?
If you run into any issues, feel free to open an issue on **GitHub** or reach out! 😊