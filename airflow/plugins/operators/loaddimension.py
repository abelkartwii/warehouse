# reference: https://airflow.apache.org/docs/apache-airflow/2.0.2/howto/custom-operator.html

from airflow.models import BaseOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.decorators import apply_defaults

class DimensionOperator(BaseOperator):
    @apply_defaults
    def __init__(self, append_only = False, table = "", redshift_id = "", sql = "", *args, **kwargs):
        super(DimensionOperator, self).__init__(*args, **kwargs)
        self.append_only = append_only
        self.table = table
        self.redshift_id = redshift_id
        self.sql = sql

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id = self.redshift_id)
        # if not self.append_only: ? check if we need this
        self.log.info("Loading data into dimension tables...")
        redshift.run(self.sql)
        self.log.info("Finished loading data!")