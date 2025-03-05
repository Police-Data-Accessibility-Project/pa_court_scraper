# Use an official Python image as the base
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for MongoDB driver
RUN apt-get update && apt-get install -y \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies and install them
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY app.py .

# Set the environment variable for MongoDB connection
ENV MONGO_URI="mongodb://mongo:27017/"

# Run the script
CMD ["python", "app.py"]
