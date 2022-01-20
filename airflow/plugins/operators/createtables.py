# reference: https://airflow.apache.org/docs/apache-airflow/2.0.2/howto/custom-operator.html

from airflow.models import BaseOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.decorators import apply_defaults

class CreateTablesOperator(BaseOperator):
    @apply_defaults
    def __init__(self, redshift_id = "", sql_commands = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redshift_id = redshift_id
        self.sql_commands = sql_commands

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id = self.redshift_id)
        self.log.info("Recreating tables...")
        redshift.run(self.sql_commands)
        self.log.info("Finished recreating tables!")