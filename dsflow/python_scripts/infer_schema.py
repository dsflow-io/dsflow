import os
from sys import argv
from sys import exit
import json
import yaml
import datetime as dt
from pprint import *
from pyspark.sql import SparkSession

if len(argv) == 1:
    print("usage: infer_schema.py DATA_PATH DATA_FORMAT")

    exit(0)

spark = SparkSession.builder.getOrCreate()

source_path = argv[1]
source_type = argv[2] if len(argv) > 2 else "parquet"

if source_type == "csv":
    source_options_1 = dict(wholeFile=True, inferSchema=True, header=True, delimiter=",")
    source_options_2 = dict(wholeFile=True, inferSchema=True, header=True, delimiter=";")
    source_options_3 = dict(wholeFile=True, inferSchema=True, header=True, delimiter="\t")

    df1 = spark.read.format(source_type).options(**source_options_1).load(source_path)
    df2 = spark.read.format(source_type).options(**source_options_2).load(source_path)
    df3 = spark.read.format(source_type).options(**source_options_3).load(source_path)

    df = df1 if len(df1.columns) > len(df2.columns) else df2
    df = df if len(df.columns) > len(df3.columns) else df3

else:
    df = spark.read.format(source_type).load(source_path)

print("Discovered schema:")
df.printSchema()

schema = df.schema.json()
schema_dict = json.loads(schema)

# def clean_keys(fields):
#    for item in fields:
#        if isinstance(item, dict):
#            item.pop('nullable', None)
#            item.pop('metadata', None)
#
#            if "fields" in item:
#                clean_keys(item["fields"])
#
#            if "type" in item and isinstance(item["type"], dict):
#                clean_keys([item["type"]])
#
#            if "elementType" in item and isinstance(item["elementType"], dict):
#                clean_keys(item["elementType"]["fields"])
#
# clean_keys(schema_dict["fields"])

with open('/tmp/schema-generator/schema.json', 'w') as outfile:
    yaml.dump(schema_dict, outfile, default_flow_style=False)
