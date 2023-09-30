# Intro
Dear Applicant,
Thank you for your interest in the Data Engineer position on JustEatTakeaway.com’s Food Catalogue Team.
The task in front of you is designed to assess the technical skills that you’ll need on the job. We hope you’ll enjoy it!

# Assignment
The challenge consists of three parts, each designed to assess a set of core competencies needed for the position. The tasks involve implementing an ETL job, developing a REST API interface, and designing a data orchestration process.

Please add your solutions to the respective sub-modules (`etl`, `api`, `orchestration`) which are already present.
**!! Please read the details of all assignments before starting the first one !!**

## ETL Task
You will find a json file under `/etl/resources`. Your first task is to read this data, validate its correctness, and calculate the _net_ merchandise value of the ordered products.

The calculation should consider the following VAT rates: 7% for cold foods, 15% for hot foods, and 9% for beverages. After processing the data, you should persist the results in a data storage system of your choice.

Your ETL job should include robust error handling and logging mechanisms.

Also, please describe how your ETL job could be adapted to handle a real-time data processing scenario, like a continuous stream of data coming from a Kafka topic.

## API Task
The second task is to develop a REST API that exposes the data generated in the ETL task. The API should implement a single endpoint: `GET /spend/${customerId}`, which should return the following response for a given `customerId`:

```json
{
  “customerId”: “123",
  “orders”: 3,
  “totalNetMerchandiseValueEur”: 52.13
}
```

Your API should be designed to handle high load and concurrent requests. Please also document your API using standards like Swagger.


## Data Orchestration Task
For the data orchestration task, you are required to design a data orchestration process using a tool like Airflow or Dagster.
However, please note that you do not need to set up and run an actual Airflow instance as part of the challenge.
Your task is to create the Airflow DAG (Directed Acyclic Graph) itself, which outlines the steps and dependencies of the ETL (Extract, Transform, Load) job.
Make sure to focus on the logic and structure of the DAG, demonstrating your understanding of data orchestration concepts and your ability to design an effective ETL workflow.


## Requirements
- The application should be written in Python
- Your applications should be modularized and reusable.
- Your applications need to be containerized and runnable in different environments, demonstrating compliance with devops practices.
- Both your ETL job and API should include a test suite and clear documentation.
- You should discuss your choice of data storage system, considering factors like performance, scalability, and the ability to handle real-time updates.

## Notes
- If either your API, ETL job, or data orchestration process require additional arguments, please specify these in your submission.
- Please explain how you would set up a CI/CD pipeline for your applications, and how this pipeline would manage deployments and handle failures.
- We’d appreciate seeing test cases for each part of the assignment.

Thanks and good luck!


- api
- etl
  - resources
    - data.json
  - docker-compose.yaml
  -etl.py
  -requirements.txt
- orchestration
-README.md


        customerid        |         orderid          | netmerchandisevalueeur 
--------------------------+--------------------------+------------------------
 5b6950c008c899c1a4caf2a1 | 5b6950c0fda5be24b51cfe47 |                  23.51
 5b6950c008c899c1a4caf2a1 | 5b6950c07ceef02d2044eb8d |                  31.15
 5b6950c008c899c1a4caf2a1 | 5b6950c0b1589dd9d3c9758c |                   5.07
 5b6950c008c899c1a4caf2a1 | 5b6950c05bbe2e59661c9eae |                  14.29
 5b6950c008c899c1a4caf2a1 | 5b6950c0340018c025fa6acf |                  18.24



{
  "customerId": "5b6950c008c899c1a4caf2a1", 
  "orders": 50, 
  "totalNetMerchandiseValueEur": 922.6
}