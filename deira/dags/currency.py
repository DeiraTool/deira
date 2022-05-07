from airflow import DAG
from datetime import datetime

from airflow.operators.python_operator import PythonOperator

def print_hello():
    return 'Hello world from first Airflow DAG!'

def print_bye():
    return 'That`s all folks!'

dag = DAG('hello_world', 
    description='Hello World DAG',
    schedule_interval='* * * * *',
    start_date=datetime(2022, 5, 1), 
    catchup=False)

hello_operator = PythonOperator(
    task_id='hello_task', 
    python_callable=print_hello, 
    dag=dag)

bye_operator = PythonOperator(
    task_id='bye_task', 
    python_callable=print_bye, 
    dag=dag)

hello_operator >> bye_operator
