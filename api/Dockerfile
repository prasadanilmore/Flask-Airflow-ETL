# Use the official Python image
FROM python:3.8

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the API code into the container
COPY . .

# Install required dependencies
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 8080

# Define the command to run the API
CMD ["python", "app.py"]
