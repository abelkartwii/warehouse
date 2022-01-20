import operator
from datetime import datetime, timedelta
from operators
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator 

default_args = {
    'owner':
}

dag = DAG(
    'etl_dag',
    default_args = default_args,
    description = 'ETL pipeline to Redshift using Airflow'    
)


load_fact_ratings = LoadFactOperator(

)