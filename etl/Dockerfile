# Use the official Python image
FROM python:3.8

WORKDIR /app

# Copy the ETL script into the container
COPY . .

# Install required dependencies
RUN pip install -r requirements.txt

# Define the command to run the ETL job
CMD ["python", "etl.py"]
