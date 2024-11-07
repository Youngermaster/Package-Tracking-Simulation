# Use an official lightweight Python 3.10 image.
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends gcc \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
  && pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . /app

# Specify the command to run on container start
CMD ["python", "app/main.py"]
