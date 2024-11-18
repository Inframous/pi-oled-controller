# Use the official Python slim image as a base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for libraries like psutil (e.g., build tools), font packages, and procps
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    fontconfig \
    fonts-dejavu \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt to the container
COPY requirements.txt /app/requirements.txt

# Install Python dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code (stats.py) into the container
COPY stats.py /app/stats.py

# Command to run the Python application
CMD ["python", "stats.py"]
