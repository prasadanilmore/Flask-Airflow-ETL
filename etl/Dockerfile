# Use the official Python image
FROM python:3.8

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the entire current directory (including ETL script and other files) into the container at /app
COPY . .

# Install required dependencies
RUN pip install -r requirements.txt

# Define the command to run the ETL job
CMD ["python", "etl.py"]
