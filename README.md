# InstaHouse
## Overview
This project features a data warehouse in a Docker infrastructure, used to identify proper inventory management for an Instacart warehouse. The infrastructure utilizes S3 for initial data storage, Airflow for data orchestration, AWS Redshift for a cloud data warehouse, and Metabase for data visualization.

## Workflow
### 1. Extract
The data used in this project is obtained from a Kaggle dataset [here](https://www.kaggle.com/c/instacart-market-basket-analysis/data), which will be further pushed to an S3 bucket on AWS (named `instacart-warehouse`). Once the data arrives, an ETL script will run to copy data from the S3 bucket to the staging process in Redshift.

### 2. Transform
Once the data is pushed to Redshift, an Airflow task will be triggered to read the data from the bucket, and we will be transforming the data! The data modeling is performed by creating fact and dimension tables as follows:

**Fact Tables**: `purchases`

**Dimension Tables**: `goods, orders, reorder`

Using Redshift staging tables and the UPSERT operation, the data is updated in the fact and dimension tables, which in turn updates the data warehouse. 

To ensure data correctness, an Airflow DAG runs a quality check on the fact and dimension tables.

### 3. Load
The data is pushed to Metabase, where it will be visualized! 

## Modeling
Kimball's model of data warehousing entails four design steps: 

**1. Select the business process**
The goal of the Kaggle dataset, and naturally this project, is to identify which products get reordered the most, and to predict what customers would order next. To do so, the data warehouse schema is set up to create the best view of this.

**2. Declare the grain**
The grain of a process is the level of detail in which information is stored in our data warehouse. Examples could be one storage event, one purchase, one customer response, and so on. Here, since we are predicting, we are using **orders** as the level of granularity.

**3. Identify the dimensions**
A dimension table contains a set of columns together for a certain purpose: to calculate reorder probability, to store all the IDs and names together, to aggregate certain departments, etc. 

**4. Identify the facts**
Finally, the fact table is the central table in the data warehouse. Here, the `purchases` fact table only contains IDs, which happen to be foreign keys in all the dimension tables. This creates a denormalized setup, which is ideal for data warehousing since it creates an optimal setup for analysis and joins.

## Configuration and Setup
This project utilizes Docker for a smooth running environment. Assuming Docker is installed, run `docker-compose up` to pull the latest images of Airflow and Metabase from the Docker Hub, using the Docker Compose file provided in the repository.

**Setting up AWS resources**
- To setup a Redshift cluster, follow this guide [here](https://docs.aws.amazon.com/redshift/latest/gsg/rs-gsg-launch-sample-cluster.html) using your AWS account! The cluster used is a `dc2.large` two-node cluster. 
- The S3 bucket has been provided at `instacart-warehouse`.

**Running Airflow**
Open the Airflow UI on `http://localhost:8080` to configure the required connections. The `etl_dag.py` should be displayed as such:

**Running Metabase**
Open the Metabase UI on `http://localhost:3000`, and configure a Metabase account and database.

## License
This project uses the [MIT license](https://choosealicense.com/licenses/mit/).