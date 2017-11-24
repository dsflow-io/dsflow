from pyspark.sql import SparkSession
from IPython.display import display
from IPython.display import HTML, Markdown
from pyspark.sql import SparkSession
import os
from pprint import *
import pandas as pd
import yaml
from jinja2 import Template
from textwrap import dedent
import subprocess

from .utils import get_datastore_path, get_flows_path


def display_html_h4(value):
    display(HTML("<h4>{}</h4>".format(value)))


class DsflowContext:

    def __init__(self):
        self.version = "0.1"

    @classmethod
    def create(self):
        self.spark = SparkSession.builder.enableHiveSupport().getOrCreate()

        return self

    @classmethod
    def execute_sql(self, query):
        self.spark.sql(query)

    @classmethod
    def sql(self, query):
        display(self.spark.sql(query).limit(1000).toPandas())

    @classmethod
    def load_tables(self):
        """Refresh Spark"""

        possible_tables = os.listdir(get_datastore_path() + '/tables')

        for table in possible_tables:
            if table != ".DS_Store":
                try:
                    self.execute_sql("DROP TABLE if exists " + table)

                    self.execute_sql("""
                      CREATE TABLE IF NOT EXISTS %s
                      USING parquet
                      OPTIONS (path='/data/tables/%s')
                    """ % (table, table))

                    self.execute_sql("MSCK REPAIR TABLE %s" % table)
                    self.execute_sql("REFRESH TABLE %s" % table)

                    print("INFO - %s was successful imported/updated" % table)
                except Exception as e:
                    print("ERROR - %s could not be imported" % table)
                    print(e)

        self.sql("show tables")

    @classmethod
    def list_tables(self):
        self.sql("show tables")

    @classmethod
    def list_raw(self):

        raw_contents = os.walk(get_datastore_path() + '/raw')

        for (path, dir_names, file_names) in raw_contents:
            if len(dir_names) > 0:
                display_html_h4(path)
                print("")

            if len(dir_names) == 0:
                print(path)
                for f in file_names[:2]:
                    print("        " + f)
                if len(file_names) > 2:
                    print("        ...%d additional files" % len(file_names))
                print("")

        return(raw_contents)

    @classmethod
    def validade_task_specs(self, task_specs):
        return "not implemented"

    @classmethod
    def validade_task_output(self, task_specs):
        return "not implemented"

    @classmethod
    def display(self, df, num_rows=10):
        print("Showing 10 random rows")

        return df.limit(10).toPandas()
