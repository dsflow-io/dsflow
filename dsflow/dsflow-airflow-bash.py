import sys
import os
import subprocess

from python_scripts.dsflow_core.cli_utils import validate_env

validate_env()

DSFLOW_WORKSPACE = os.environ["DSFLOW_WORKSPACE"]
DSFLOW_ROOT = os.environ["DSFLOW_ROOT"]

# Input parameters
dsflow_service_name = "airflow"
docker_compose_base_file = DSFLOW_ROOT + "/docker/base/docker-compose.yaml"
docker_compose_db = DSFLOW_ROOT + "/docker/db/docker-compose.yaml"
docker_compose_airflow = DSFLOW_ROOT + "/docker/airflow/docker-compose.yaml"
# sys.argv[1]

my_env = os.environ.copy()

args = ["docker-compose",
        "-f", docker_compose_base_file,
        "-f", docker_compose_db,
        "-f", docker_compose_airflow,
        ]

# preview
print(" ".join(args))

subprocess.call(args + ["exec", dsflow_service_name, "/bin/bash"], env=my_env)
