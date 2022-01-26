"""
ETL DAG to be used in Airflow.
Using the helper operators and the helper SQL Query class,
these operators are run in Airflow to create tables in and 
to push data to Redshift.
"""

import operator
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator 

from operators import SourceToRedshiftOperator, FactOperator, DimensionOperator, CreateTablesOperator 
from helper import SQLQueries

default_args = {
    'owner': 'abelkartwii',
    'retries': 3,
    'retry_delay': timedelta(minutes = 10)
}

dag = DAG(
    'etl_dag',
    default_args = default_args,
    description = 'ETL pipeline to Redshift using Airflow'    
    schedule_interval = '0 * * * *'
)

## start operator that creates tables
start_operator = CreateTablesOperator(
    task_id = 'start_operator',
    dag = dag,
    redshift_id = 'redshift',
    sql = SQLQueries.create_table_queries
)

## uploads temporary tables to redshift, 6 total!
aisles_to_redshift = SourceToRedshiftOperator(
    task_id = 'aisles_redshift',
    dag = dag,
    table = temp_aisles,
    columns = """
        aisle_id, aisle
    """,
    redshift_id = 'redshift',
    aws_creds_id = 'aws_credentials',
    s3_bucket = 'instacart-warehouse',
    s3_key = 'source-data/aisles.csv'
)

departments_to_redshift = SourceToRedshiftOperator(
    task_id = 'departments_redshift',
    dag = dag,
    table = temp_departments,
    columns = """
        department_id, department
    """,
    redshift_id = 'redshift',
    aws_creds_id = 'aws_credentials',
    s3_bucket = 'instacart-warehouse',
    s3_key = 'source-data/departments.csv'
)

orders_prior_to_redshift = SourceToRedshiftOperator(
    task_id = 'orders_prior_redshift',
    dag = dag,
    table = temp_orders_prior,
    columns = """
        order_id, product_id, add_to_cart_order, reordered
    """,
    redshift_id = 'redshift',
    aws_creds_id = 'aws_credentials',
    s3_bucket = 'instacart-warehouse',
    s3_key = 'source-data/order_products__prior.csv'
)

orders_train_to_redshift = SourceToRedshiftOperator(
    task_id = 'orders_train_redshift',
    dag = dag,
    table = temp_orders_train,
    columns = """
        order_id, product_id, add_to_cart_order, reordered
    """,
    redshift_id = 'redshift',
    aws_creds_id = 'aws_credentials',
    s3_bucket = 'instacart-warehouse',
    s3_key = 'source-data/order_products__train.csv'
)

orders_to_redshift = SourceToRedshiftOperator(
    task_id = 'orders_redshift',
    dag = dag,
    table = temp_orders, # make staging table or go straight to dimension table???
    columns = """
        order_id, user_id, eval_set, order_number, order_dow, order_hour_of_day, days_since_prior_order
    """,
    redshift_id = 'redshift',
    aws_creds_id = 'aws_credentials',
    s3_bucket = 'instacart-warehouse',
    s3_key = 'source-data/orders.csv'
)

products_to_redshift = SourceToRedshiftOperator(
    task_id = 'products_redshift',
    dag = dag,
    table = temp_products,
    columns = """
        product_id, product_name, aisle_id, department_id
    """,
    redshift_id = 'redshift',
    aws_creds_id = 'aws_credentials',
    s3_bucket = 'instacart-warehouse',
    s3_key = 'source-data/products.csv'
)

## loads fact tables and dimension tables
load_fact_ratings = FactOperator(
    task_id = '',
    dag = dag,
    redshift_id = 'redshift',
    sql = SQLQueries.fact_table_insert
)

load_dimension_goods = DimensionOperator(
    task_id = '',
    dag = dag,
    append_only = False,
    table = 'goods',
    redshift_id = 'redshift',
    sql = SQLQueries.goods_table_insert
)

## ends stuff
end_operator = DummyOperator(task_id = 'stop_execution', dag = dag)

## main
start_operator >> aisles_to_redshift
start_operator >> departments_to_redshift
start_operator >> orders_to_redshift
start_operator >> orders_prior_to_redshift
start_operator >> orders_train_to_redshift
start_operator >> products_to_redshift

products_to_redshift >> load_dimension_goods
aisles_to_redshift >> load_dimension_goods
departments_to_redshift >> load_dimension_goods

load_fact_ratings >> end_operator