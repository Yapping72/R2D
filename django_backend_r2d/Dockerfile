# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install PostgreSQL client and any dependencies your Django project requires
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get install -y dos2unix && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/
RUN dos2unix /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose the port that the Django development server will run on
EXPOSE 8000
