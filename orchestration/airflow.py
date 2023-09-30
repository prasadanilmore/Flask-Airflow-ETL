from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Define your DAG with appropriate settings (e.g., schedule_interval)
dag = DAG(
    'my_etl_dag',
    default_args={
        'owner': 'your_name',
        'start_date': datetime(2023, 1, 1),
        # Add more DAG configuration options as needed
    },
    schedule_interval=None,  # Set your desired schedule interval
)

# Define tasks to run each function
load_data_task = PythonOperator(
    task_id='load_data_task',
    python_callable=load_data_from_json,
    op_args=['/etl/resources/data.json'],
    dag=dag,
)

process_data_task = PythonOperator(
    task_id='process_data_task',
    python_callable=process_data,
    op_args=[load_data_task.output],
    dag=dag,
)

store_data_task = PythonOperator(
    task_id='store_data_task',
    python_callable=store_data_in_postgres,
    op_args=[process_data_task.output],
    dag=dag,
)

# Set task dependencies
load_data_task >> process_data_task >> store_data_task
