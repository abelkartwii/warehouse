from __future__ import print_function
from airflow.plugins_manager import AirflowPlugin
import operators
import helpers

class InstacartPlugin(AirflowPlugin):
    name = "instacart_plugin"
    operators = [
        operators.SourceToRedshiftOperator,
        operators.FactOperator,
        operators.DimensionOperator,
        operators.CreateTablesOperator
    ]

    helper = [
        helper.SQLQueries
    ]