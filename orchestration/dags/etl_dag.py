import configparser
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from etl import (
    load_data_from_json,
    process_data,
    connect_to_postgres,
    insert_data_into_postgres,
)


# Create a configuration object
config = configparser.ConfigParser()

# Load the configuration file using a relative path
config.read('/opt/airflow/plugins/config.ini') 

# Access variables from the configuration file
HOST = config['Database']['host']
DATABASE = config['Database']['database']
USER = config['Database']['user']
PASSWORD = config['Database']['password']
PORT = config['Database']['port']

# File Paths
FILE_PATH = config['FILE_PATH']['data_file']
ETL_LOG_FILE = config['FILE_PATH']['etl_log_file']

# Define your default_args and DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 10, 1),
}

dag = DAG(
    'etl_dag',
    default_args=default_args,
    description='ETL DAG for your project',
    schedule_interval=None,  # Set your desired schedule interval
    catchup=False,  # Set to False to prevent backfilling
)

# Define individual tasks as PythonOperators
load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data_from_json,
    op_args=['/opt/airflow/plugins/resources/data.json'],  
    dag=dag,
)

def _process_data(ti):
    data = ti.xcom_pull(task_ids='load_data')
    processed_data = process_data(data)
    ti.xcom_push(key='processed_data', value=processed_data)

process_data_task = PythonOperator(
    task_id='process_data',
    python_callable=_process_data,
    provide_context=True,  
    dag=dag,
)

def _connect_to_postgres(ti):
    processed_data = ti.xcom_pull(task_ids='process_data', key='processed_data')
    connection = connect_to_postgres(HOST, DATABASE, USER, PASSWORD, PORT)
    ti.xcom_push(key='db_connection', value=connection)
    ti.xcom_push(key='processed_data', value=processed_data)

connect_to_postgres_task = PythonOperator(
    task_id='connect_to_postgres',
    python_callable=_connect_to_postgres,
    provide_context=True,  
    dag=dag,
)

def _insert_data_into_postgres(ti):
    connection = ti.xcom_pull(task_ids='connect_to_postgres', key='db_connection')
    processed_data = ti.xcom_pull(task_ids='connect_to_postgres', key='processed_data')
    insert_data_into_postgres(connection, processed_data)

insert_data_task = PythonOperator(
    task_id='insert_data',
    python_callable=_insert_data_into_postgres,
    provide_context=True,  
    dag=dag,
)

# Set task dependencies
load_data_task >> process_data_task >> connect_to_postgres_task >> insert_data_task
