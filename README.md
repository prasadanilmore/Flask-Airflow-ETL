## Introduction
This documentation provides an overview of the tasks completed in this project. The project comprises three key tasks: ETL (Extract, Transform, Load), API development, and Data Orchestration using Airflow. Each task is detailed below along with explanations of design choices and considerations.

## ETL Task
### Implementation
The ETL (Extract, Transform, Load) task involves processing JSON data, calculating the net merchandise value for ordered products based on VAT rates, and persisting the results in a data storage system. The Python ETL script follows these steps:

- Data Loading: The ETL job reads JSON data from the /etl/resources directory.
- VAT Rate Calculation: Calculates the net merchandise value by applying VAT rates (7% for cold foods, 15% for hot foods, and 9% for beverages).
- Data Transformation: The processed data is transformed into a structured format.
- Data Loading: The transformed data is inserted into a PostgreSQL database.

### Choice of Data Storage System
For this project, we chose PostgreSQL as the data storage system due to its robustness, performance, and support for structured data. However, for real-time scenarios, we recommend using Apache Cassandra, a distributed NoSQL database known for its fault tolerance, scalability, and efficient handling of real-time data updates.

### Handling Real-Time Data
To adapt the ETL job for real-time data processing from a Kafka topic, the following steps can be taken:

- Kafka Producer: Introduce a Kafka producer container that sends real-time data to specific Kafka topics based on data types (e.g., hot foods, cold foods, beverages).

- Kafka Consumer: Implement a Kafka consumer using technologies like Apache Spark with Kafka Streams. The consumer subscribes to Kafka topics and performs real-time calculations.

- Data Storage: Store the real-time results in a distributed database like Cassandra, which is well-suited for handling real-time updates.

### Error Handling and Logging
Robust error handling and logging mechanisms are implemented in the ETL script to ensure data integrity and fault tolerance. Error handling includes catching exceptions and logging detailed error messages, allowing for easy debugging and troubleshooting.

## API Task
### Implementation
The API task involves developing a REST API to expose the data generated in the ETL task. The API is implemented using the Python Flask framework and follows these key points:

- Endpoint: The API provides a single endpoint, `GET /spend/${customerId}`, where `${customerId}` is a placeholder for the customer ID.
- Response: The API responds with customer spend information in JSON format, including `customerId`, the number of `orders`, and the `totalNetMerchandiseValueEur` value in EUR.
- Scalability: The API is designed to handle high loads and concurrent requests, ensuring its ability to perform efficiently under increased traffic.

### Scalability and Concurrency
The API is designed to handle high loads and concurrent requests. It's containerized and can be deployed in different environments to ensure compliance with DevOps practices. To handle increased traffic, scaling can be achieved by deploying multiple instances of the API behind a load balancer.

### API Documentation
The API is documented using Swagger, ensuring clear and comprehensive documentation for consumers of the API. The Swagger UI provides an interactive interface to explore and test the API.

## Data Orchestration Task

### Airflow DAG Design
For the data orchestration task, an Airflow DAG is designed to outline the steps and dependencies of the ETL job. The DAG orchestrates the ETL workflow, ensuring data extraction, transformation, and loading are performed efficiently.

The provided etl_dag.py script serves as a solution to this task, and this documentation provides a detailed explanation of the DAG's logic and structure.

### DAG Description
The Airflow DAG is named 'etl_dag' and is designed to perform the following ETL operations:

1. **load_data**: This task uses the `load_data_from_json` function to load data from a JSON file located at `/opt/airflow/plugins/resources/data.json`. The data is then stored as an XCom variable to be used in subsequent tasks.

2. **process_data**: The `process_data` task processes the data fetched from the previous task. It calls the `_process_data` function, which calculates the net merchandise value for the orders. The processed data is stored as an XCom variable to be used in the next task.

3. **connect_to_postgres**: This task establishes a connection to a PostgreSQL database using the connection parameters (`HOST`, `DATABASE`, `USER`, `PASSWORD`, `PORT`) obtained from the configuration file. The connection is stored as an XCom variable, and the processed data is also stored in XCom.

4. **insert_data**: The `insert_data_into_postgres` function is called to insert the processed data into the PostgreSQL database. It uses the database connection and processed data obtained from the previous tasks.

### Task Dependencies
The task dependencies ensure that each step is executed in the correct order, following the ETL process:

- load_data_task depends on the DAG's start date.
- process_data_task depends on load_data_task, as it requires the loaded data.
- connect_to_postgres_task depends on process_data_task, as it needs the processed data to store in the database.
- insert_data_task depends on connect_to_postgres_task to ensure that the database connection and processed data are available before insertion.

## Additional Questions

### Test Suites

A testing framework is provided for both the ETL job and the API. While the testing is limited due to computational limitations, it demonstrates the structure and concept of testing. I have added separate test directories for API and ETL. Due to resource limitations, the testing functions are kept limited, but in an ideal scenario, I would set up a test database and include assertions to verify data storage and connections.

### CI/CD Pipeline Setup

A concept for a CI/CD pipeline is provided in the ci-cd directory. To set up a full CI/CD pipeline, the following steps would be taken:

- Code is pushed to a version control system (e.g., Git).
- A CI tool (e.g., GitHub Actions, Jenkins) detects changes and triggers a build.
- The CI server runs tests and creates a Docker image for the application.
- The image is pushed to a container registry (e.g., Docker Hub).
- A CD tool (e.g., Kubernetes, AWS Elastic Beanstalk) deploys the new image to the production environment.
- Deployment includes rolling updates to ensure minimal downtime.
- Monitoring and alerting are set up to handle failures and performance issues.

## Docker Compose Configuration

The project includes a docker-compose.yaml file, which defines the services and configurations required to run the project. 

### Services

The `services` section defines multiple services that make up the project:

- **postgres:** This service uses the PostgreSQL Docker image and configures the database name, user, and password.

- **etl:** This service is built from the `./etl` directory and mounts the `config.ini` file for ETL configuration. It depends on the `postgres` service.

- **api:** This service is built from the `./api` directory and exposes port 8080 for the REST API. It also mounts the `config.ini` file and depends on the `postgres` service.

- **airflow-init:** This service initializes the Airflow database and creates an admin user. It depends on the `postgres` service.

- **airflow-webserver:** This service runs the Airflow webserver and exposes port 8081. It depends on the `postgres` service.

- **airflow-scheduler:** This service runs the Airflow scheduler. It depends on the `postgres` service.


## Running the Project
To run the project, follow these steps:

1. Ensure Docker and Docker Compose are installed.

2. Place project files, excluding `docker-compose.yaml`, in a directory.

3. Open a terminal and navigate to the project directory.

4. Run the following command to start the services:
   ```bash
   docker-compose up

This command will build the required Docker containers, start the services, and display logs in the terminal.

5. Once the services are up and running, you can access the API at http://localhost:8080 and the Airflow web UI at http://localhost:8081.

6. To stop the services, press Ctrl + C in the terminal where Docker Compose is running, and then run:

  ```bash
  docker-compose down

This setup allows you to run the ETL job, REST API, and data orchestration process using Docker containers. Please note that this is a basic setup, and for production use, you may need to configure additional settings such as security, scaling, and monitoring.