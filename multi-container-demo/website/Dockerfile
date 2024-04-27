# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask and other dependencies
RUN pip install --no-cache-dir Flask pymongo

# Expose the port on which the Flask app will run
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
