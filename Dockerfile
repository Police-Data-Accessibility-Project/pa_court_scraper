# Use an official Python image as the base
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for MongoDB driver

# Copy Python dependencies and install them
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium --with-deps

# Copy the Python script into the container
COPY get_docket_info.py .
COPY insert_into_mongodb.py .
COPY get_docket_numbers_from_yesterday.py .
COPY SimpleCache.py .

# Set the environment variable for MongoDB connection
ENV MONGO_URI="mongodb://mongo:27017/"

