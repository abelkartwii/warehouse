# reference: https://airflow.apache.org/docs/apache-airflow/2.0.2/howto/custom-operator.html

from airflow.models import BaseOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.decorators import apply_defaults

class FactOperator(BaseOperator):
    @apply_defaults
    def __init__(self, redshift_id = "", sql = "", *args, **kwargs):
        super(FactOperator, self).__init__(*args, **kwargs)
        self.redshift_id = redshift_id
        self.sql = sql

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id = self.redshift_id)
        self.log.info("Loading data into fact table...")
        redshift.run(self.sql)
        self.log.info("Finished loading data!")