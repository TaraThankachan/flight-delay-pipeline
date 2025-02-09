# Use an official Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y build-essential default-mysql-client

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Command to run when the container starts
CMD ["sh", "-c", "python scripts/data_processing.py && dbt run --project-dir dbt_project"]
