from airflow.models import BaseOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AWSHook
from airflow.utils.decorators import apply_defaults

class SourceToRedshiftOperator(BaseOperator):
    copy_sql = """
        COPY {} {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
    """

    @apply_defaults
    def __init__(self, table = "", columns = "", redshift_id = "", 
                 aws_creds_id = "", s3_bucket = "", s3_key = "", copy_extra = "", 
                 *args, **kwargs):

        super(SourceToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.columns = columns
        self.redshift_id = redshift_id
        self.aws_creds_id = aws_creds_id
        self.s3_bucket = s3_bucket
        self.s3_key
        self.copy_extra = copy_extra

    def execute(self, context):
        aws_hook = AWSHook(aws_conn_id = self.aws_creds_id)
        creds = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id = self.redshift_id)

        self.log.info("Clearing data from Redshift tables...")
        redshift.run("DELETE FROM {}".format(self.table))

        self.log.info("Copying data from S3 to Redshift...")
        rendered_key = self.s3_key.format(**context)
        s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_key)
        cols = f"({self.columns})"
        sql_done = SourceToRedshiftOperator.copy_sql.format(
            self.table,
            cols,
            s3_path,
            creds.ACCESS_KEY_ID,
            creds.SECRET_ACCESS_KEY,
            self.copy_extra
        )

        redshift.run(self.sql_done)
