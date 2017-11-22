import sys
import os
import re
import datetime as dt
import subprocess
import urllib.request
from python_scripts.dsflow_core.cli_utils import validate_env

validate_env()

def is_valid_dataset_name(s):
        return re.match("^[\_\da-z]+$", s)

# Input parameters
input_parameters = sys.argv[1:]

dataset_name = input_parameters[0]
url = input_parameters[1]
dataset_type = input_parameters[2]

if not is_valid_dataset_name(dataset_name):
    raise(Exception("invalid dataset name"))

# Paths, ids and env. variables
DSFLOW_WORKSPACE = os.environ["DSFLOW_WORKSPACE"]
datastore_abs_path = os.path.join(DSFLOW_WORKSPACE, "datastore")
jobs_abs_path = os.path.join(DSFLOW_WORKSPACE, "jobs")

docker_image_dir = "dsflow-job-generator"
docker_image_id = "dsflow/%s" % docker_image_dir

image_id = "dsflow-job-generator"
docker_compose_file = "dsflow/docker/%s/docker-compose.yaml" % image_id


# download file
# adapted from https://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
if "http" in url:
    file_name = url.split('/')[-1]
    file_path = os.path.join(datastore_abs_path, "raw", dataset_name, file_name)
    file_path_container = os.path.join("/data", "raw", dataset_name, file_name)

    dir_path = os.path.join(datastore_abs_path, "raw", dataset_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    print("\n========== file download ===========")
    print("writing to ", file_path)
    urllib.request.urlretrieve(url, file_path)
elif "datastore/" in url:
    file_path_container = "/data/" + url.split("datastore/")[1]
else:
    raise(Exception("URL is not valid. If using a local file, make sure it is located in the datastore"))


# infer schema
args = [
    "docker-compose",
    "-f", "dsflow/docker/dsflow-schema-generator/docker-compose.yaml",
    "run",
    "schema-generator",
    "python",
    "python_scripts/infer_schema.py",
    file_path_container,
    dataset_type
]

print("\n========== running docker container for schema inference ===========")
subprocess.call(args)

schema_output_path = DSFLOW_WORKSPACE + "/tmp/schema-generator/schema.json"

print(schema_output_path)
print(open(schema_output_path, 'r').read())


# copy path to adhoc dir:
schema_destination_path = os.path.join(DSFLOW_WORKSPACE, "adhoc", "%s-schema.yaml" % dataset_name)
subprocess.call(["mv", schema_output_path, schema_destination_path])


print("\n========== preview docker run command ===========")
args = [
    "docker-compose",
    "-f", docker_compose_file,
    "run",
    "job-generator",
    "python",
    "python_scripts/dsflow-generate-adhoc.py",
    dataset_type,
    dataset_name,
    file_path_container,
    os.path.join("/adhoc", "%s-schema.yaml" % dataset_name)
]

print(" ".join(args))

print("\n========== running docker container ===========")
subprocess.call(args)
